"""Box-level scores of open-vocabulary detectors before and after vocabulary growth (docs/OVD_DETECTION_BENCHMARK.md).

For every ground-truth box g (COCO-80 boxes of the source classes, LVIS boxes of the added classes) and every label c,
the stored score is the maximum over the predicted boxes d with IoU(d, g) >= 0.5 of the detection logit of c at d (the
maximum over c's phrase tokens of the token logit; sigmoid of it is the model's score), clamped to [-30, 30] and stored
in float16 as the segmentation scores are; -30 if no predicted box overlaps g. Arms (Grounding DINO
family):
  native_src   the 80 COCO names as the whole prompt (calibration vocabulary);
  native_one   the 80 COCO names and the first added names that fit in 256 tokens, one prompt (the deployer extends it);
  native_lvis  all names in consecutive chunks of 40 (source then added), each label scored by its own chunk;
  anch_a/b     anchored: the image side (fusion, query selection, decoder) sees bank A or B only, and every label is
               scored against the bank-conditioned queries (candidate tokens are padding for the image side; each
               phrase attends only to itself in the text branch).
OWLv2 (--model owlv2) has one arm, owl: every name as its own query; it is candidate-independent by construction.

    PYTHONPATH=src python src/exp_ovd_probe.py --model gdino_t --check      # exactness tests on 5 images, then stop
    PYTHONPATH=src python src/exp_ovd_probe.py --model gdino_t [--limit N]
Development data (COCO val2017); nothing is fitted; no reserve access.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from ovd_vocab import COCO, LVIS, load_manifest

REPOS = dict(gdino_t='IDEA-Research/grounding-dino-tiny', gdino_b='IDEA-Research/grounding-dino-base',
             mmgdino_t='openmmlab-community/mm_grounding_dino_tiny_o365v1_goldg_v3det', owlv2='google/owlv2-base-patch16-ensemble')
IMAGES = Path('data/coco-stuff/images/val2017')
N_IMAGES, CHUNK, CAP = 2000, 40, 256


def image_list(limit):
    """The COCO-Stuff benchmark images: val2017 images annotated by LVIS v1 val, sorted by file name, the first 2,000."""
    lvis = json.loads(LVIS.read_text())
    images = sorted((i for i in lvis['images'] if '/val2017/' in i['coco_url']), key=lambda i: i['coco_url'])[:N_IMAGES]
    meta = Path('cache/coco_pixels/meta.json')
    if meta.exists(): assert [i['coco_url'].split('/')[-1] for i in images] == [m['file'] for m in json.loads(meta.read_text())['meta']]
    return images[:limit or None], lvis


def ground_truth(images, lvis, rows):
    """Per image: boxes [G,4] xyxy, label index into rows, source flag. Source: COCO iscrowd=0; added: LVIS boxes of added labels."""
    coco = json.loads(COCO.read_text())
    src_of = {r['coco_id']: i for i, r in enumerate(rows) if r['role'] == 'source'}
    add_of = {r['lvis_id']: i for i, r in enumerate(rows) if r['role'] == 'added'}
    by_c, by_l = {}, {}
    for a in coco['annotations']:
        if not a['iscrowd']: by_c.setdefault(a['image_id'], []).append(a)
    for a in lvis['annotations']: by_l.setdefault(a['image_id'], []).append(a)
    xyxy = lambda b: [b[0], b[1], b[0]+b[2], b[1]+b[3]]
    out = []
    for im in images:
        cid = int(im['coco_url'].split('/')[-1][:-4])
        g = [(xyxy(a['bbox']), src_of[a['category_id']], 1) for a in by_c.get(cid, [])] + \
            [(xyxy(a['bbox']), add_of[a['category_id']], 0) for a in by_l.get(im['id'], []) if a['category_id'] in add_of]
        out.append((np.array([b for b, _, _ in g], np.float32).reshape(-1, 4), np.array([l for _, l, _ in g], np.int64), np.array([s for _, _, s in g], bool)))
    return out


def box_scores(pred, probs, gt, thr=0.5):
    """max over predicted boxes with IoU >= thr of the logits; pred [Q,4], logits [Q,L], gt [G,4] -> [G,L] in [-30, 30] (-30: nothing overlaps)."""
    if len(gt) == 0: return probs.new_zeros((0, probs.shape[1]))
    lt = torch.maximum(gt[:, None, :2], pred[None, :, :2]); rb = torch.minimum(gt[:, None, 2:], pred[None, :, 2:])
    inter = (rb-lt).clamp(min=0).prod(-1)
    area = lambda b: (b[..., 2]-b[..., 0]).clamp(min=0)*(b[..., 3]-b[..., 1]).clamp(min=0)
    iou = inter/(area(gt)[:, None]+area(pred)[None]-inter).clamp(min=1e-9)
    ok = iou >= thr
    return torch.cat([torch.where(ok[:, :, None], probs[None, :, s:s+256], -torch.inf).amax(1) for s in range(0, probs.shape[1], 256)], 1).clamp(-30, 30)


def restore_heads(model, repo):
    """Copy the decoder's per-layer box and class heads from the checkpoint file into the model. transformers 5.17 ties
    them on loading: MM-Grounding DINO (decoder_bbox_embed_share=False) gets layer 0's heads in layers 1-5 (precision
    .06, recall .03 on 50 images, against .70/.70 restored), and Grounding DINO B gets a shared box head that differs from
    the checkpoint's. Grounding DINO T already loads the checkpoint (restoring changes nothing). A shared head (config)
    is copied from layer 0's key into every layer. Returns {layer head: checkpoint key}."""
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    sd = load_file(hf_hub_download(repo, 'model.safetensors'))
    dec, share, used = model.model.decoder, model.config.decoder_bbox_embed_share, {}
    with torch.no_grad():
        for kind in ['bbox_embed', 'class_embed']:
            heads = getattr(dec, kind)
            assert heads is getattr(model, kind) and len({id(h) for h in heads}) == len(heads)   # one module per layer, used by both
            for i in range(len(heads)):
                keys = [f'model.decoder.{kind}.{i}', f'{kind}.{i}'] + ([f'model.decoder.{kind}.0', f'{kind}.0'] if share else [])
                k = next((k for k in keys if any(x.startswith(k+'.') for x in sd)), None)
                if k is None: continue
                for name, p in heads[i].named_parameters(): p.copy_(sd[f'{k}.{name}'])
                used[f'{kind}.{i}'] = k
    return used


class GDino:
    def __init__(self, repo):
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
        self.proc = AutoProcessor.from_pretrained(repo)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(repo)
        print('decoder heads restored from', restore_heads(self.model, repo), flush=True)
        self.model = self.model.cuda().eval()
        self.tok = self.proc.tokenizer
        self.dot, self.cls, self.sep = (self.tok.convert_tokens_to_ids(t) for t in ['.', '[CLS]', '[SEP]'])
        self.cache = {}

    def phrase(self, name):
        if name not in self.cache: self.cache[name] = self.tok(name.lower(), add_special_tokens=False)['input_ids']
        return self.cache[name]

    def prompt(self, names):
        """[CLS] name . name . ... [SEP] as in the official caption format; returns ids and the label index of each token (-1 otherwise)."""
        ids, lab = [self.cls], [-1]
        for k, n in enumerate(names):
            p = self.phrase(n); ids += p + [self.dot]; lab += [k]*len(p) + [-1]
        return ids+[self.sep], lab+[-1]

    def length(self, names):
        return len(self.prompt(names)[0])

    def set_cap(self, cap):
        for m in [self.model, *self.model.modules()]:
            if hasattr(m, 'max_text_len'): m.max_text_len = cap
        self.model.config.max_text_len = cap

    def pixels(self, img):
        x = self.proc.image_processor(images=img, return_tensors='pt')
        return x['pixel_values'].cuda(), x['pixel_mask'].cuda()

    @torch.no_grad()
    def run(self, px, names, image_side, W, H):
        """One pass. image_side[k]: label k is seen by the image side (a prompt label or a bank name); False: candidate only.
        Returns boxes [Q,4] (pixels, xyxy) and per-label probabilities [Q, len(names)] from the model's contrastive head."""
        ids, lab = self.prompt(names)
        lab = torch.tensor(lab).cuda(); ids = torch.tensor(ids)[None].cuda()
        vis = torch.tensor([True]+[image_side[k] if k >= 0 else True for k in lab[1:-1].tolist()]+[True]).cuda()
        # delimiters after a candidate phrase are candidate-side too, so the image side sees exactly the bank caption
        for i in range(1, len(vis)-1):
            if lab[i] < 0 and lab[i-1] >= 0 and not image_side[lab[i-1]]: vis[i] = False
        self.set_cap(max(CAP, ids.shape[1]))
        out = self.model(pixel_values=px[0], pixel_mask=px[1], input_ids=ids, attention_mask=vis[None].long(),
                         token_type_ids=torch.zeros_like(ids), return_dict=True)
        hs = out.intermediate_hidden_states[:, -1]
        logits = self.model.class_embed[-1](hs, out.encoder_last_hidden_state_text, torch.ones_like(vis)[None])[0, :, :ids.shape[1]]
        tok = lab >= 0
        probs = torch.full((logits.shape[0], len(names)), -torch.inf, device=logits.device)
        probs = probs.scatter_reduce(1, lab[tok][None].expand(logits.shape[0], -1), logits[:, tok], 'amax')    # logits
        b = out.pred_boxes[0]; scale = torch.tensor([W, H, W, H], device=b.device)
        boxes = torch.cat([b[:, :2]-b[:, 2:]/2, b[:, :2]+b[:, 2:]/2], 1)*scale
        return (boxes, probs, hs) if self.keep else (boxes, probs)

    keep = False

    @torch.no_grad()
    def anchored(self, px, bank, cands, W, H):
        """Boxes and queries from the bank alone (the native pass with the bank as the prompt), candidate text features from
        the pass in which the candidates are padding for the image side. In exact arithmetic the joint pass's image side
        equals the bank pass; taking the queries from the bank pass keeps float rounding in the joint pass (which depends
        on the sequence length) away from the top-900 query selection."""
        self.keep = True
        try:
            boxes, _, hs = self.run(px, bank, [True]*len(bank), W, H)
        finally:
            self.keep = False
        names = bank+cands
        ids, lab = self.prompt(names)
        lab = torch.tensor(lab).cuda(); ids = torch.tensor(ids)[None].cuda()
        side = [True]*len(bank)+[False]*len(cands)
        vis = torch.tensor([True]+[side[k] if k >= 0 else True for k in lab[1:-1].tolist()]+[True]).cuda()
        for i in range(1, len(vis)-1):
            if lab[i] < 0 and lab[i-1] >= 0 and not side[lab[i-1]]: vis[i] = False
        self.set_cap(max(CAP, ids.shape[1]))
        text = self.model(pixel_values=px[0], pixel_mask=px[1], input_ids=ids, attention_mask=vis[None].long(),
                          token_type_ids=torch.zeros_like(ids), return_dict=True).encoder_last_hidden_state_text
        tok = lab >= len(bank)
        logits = self.model.class_embed[-1](hs, text[:, tok], torch.ones((1, int(tok.sum())), dtype=torch.bool, device=hs.device))[0, :, :int(tok.sum())]
        probs = torch.full((logits.shape[0], len(cands)), -torch.inf, device=logits.device)
        probs = probs.scatter_reduce(1, (lab[tok]-len(bank))[None].expand(logits.shape[0], -1), logits, 'amax')
        return boxes, probs


class Owl:
    def __init__(self, repo, names):
        from transformers import Owlv2ForObjectDetection, Owlv2Processor
        self.proc = Owlv2Processor.from_pretrained(repo)
        self.model = Owlv2ForObjectDetection.from_pretrained(repo).cuda().eval()
        self.text = self.proc(text=[names], return_tensors='pt')

    @torch.no_grad()
    def run(self, img, W, H):
        x = self.proc(images=img, return_tensors='pt')
        out = self.model(input_ids=self.text['input_ids'].cuda(), attention_mask=self.text['attention_mask'].cuda(), pixel_values=x['pixel_values'].cuda())
        b = out.pred_boxes[0]; side = max(W, H)                       # OWLv2 boxes are relative to the padded square
        boxes = torch.cat([b[:, :2]-b[:, 2:]/2, b[:, :2]+b[:, 2:]/2], 1)*side
        return boxes, out.logits[0]


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True, choices=list(REPOS))
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--tag', default='', help='suffix of the output directories (e.g. _timing for the clean timing run); scores are unchanged')
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
    man = load_manifest(); rows = man['rows']; names = [r['prompt'] for r in rows]; S = man['source_labels']; L = len(names)
    banks = {k: json.loads(Path(f'meta/bank_ovd_{k}_v1.json').read_text())['names'] for k in 'ab'}
    images, lvis = image_list(5 if a.check else a.limit)
    gts = ground_truth(images, lvis, rows)
    if a.model == 'owlv2':
        det = Owl(REPOS[a.model], names); arms = {'owl': L}
    else:
        det = GDino(REPOS[a.model])
        one = S
        while det.length(names[:one+1]) <= CAP: one += 1
        arms = dict(native_src=S, native_one=one, native_lvis=L, anch_a=L, anch_b=L)

    def arm_scores(arm, img, px, W, H, gt):
        if arm == 'owl':
            return box_scores(*det.run(img, W, H), gt)
        if arm in ('native_src', 'native_one'):
            n = arms[arm]; return box_scores(*det.run(px, names[:n], [True]*n, W, H), gt)
        if arm == 'native_lvis':
            return torch.cat([box_scores(*det.run(px, names[s:s+CHUNK], [True]*len(names[s:s+CHUNK]), W, H), gt)
                              for s in range(0, L, CHUNK)], 1)
        return box_scores(*det.anchored(px, banks[arm[-1]], names, W, H), gt)

    if a.check:
        report = {}
        for k, im in enumerate(images):
            img = Image.open(IMAGES/im['coco_url'].split('/')[-1]).convert('RGB'); W, H = img.size
            px = det.pixels(img)
            gt = torch.from_numpy(gts[k][0]).cuda()
            r = {}
            full = arm_scores('anch_a', img, px, W, H, gt)
            half = L//2; rev = names[half:]+names[:half]
            bank = banks['a']
            swapped = box_scores(*det.anchored(px, bank, rev, W, H), gt)
            swapped = torch.cat([swapped[:, L-half:], swapped[:, :L-half]], 1)
            r['anchored_order_invariance_max_abs'] = float((full-swapped).abs().max()) if len(gt) else 0.0
            r['anchored_subset_invariance_max_abs'] = float((full[:, :40]-box_scores(*det.anchored(px, bank, names[:40], W, H), gt)).abs().max()) if len(gt) else 0.0
            nat = arm_scores('native_src', img, px, W, H, gt)
            r['anchored_bankA_vs_native_src_max_abs'] = float((full[:, :S]-nat).abs().max()) if len(gt) else 0.0
            one = arm_scores('native_one', img, px, W, H, gt)
            r['native_src_vs_one_prompt_max_abs'] = float((nat-one[:, :S]).abs().max()) if len(gt) else 0.0
            report[im['id']] = r; print(im['id'], r, flush=True)
        OUT = Path(f'results/ovd_probe_{a.model}{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    OUT, STORE = Path(f'results/ovd_probe_{a.model}{a.tag}'), Path(f'cache/ovd_probe_{a.model}{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    offs = np.cumsum([0]+[len(g[1]) for g in gts])
    np.savez(STORE/'gt.npz', boxes=np.concatenate([g[0] for g in gts]), labels=np.concatenate([g[1] for g in gts]),
             source=np.concatenate([g[2] for g in gts]), offsets=offs, image_ids=np.array([im['id'] for im in images]))
    stores = {arm: np.lib.format.open_memmap(STORE/f'{arm}.npy', mode='w+', dtype=np.float16, shape=(int(offs[-1]), n)) for arm, n in arms.items()}
    code = ['src/exp_ovd_probe.py', 'src/ovd_vocab.py', 'meta/ovd_coco_lvis_vocab_v1.json', 'meta/bank_ovd_a_v1.json', 'meta/bank_ovd_b_v1.json']
    protocol = dict(model=a.model, repo=REPOS[a.model], images=len(images), arms={k: int(v) for k, v in arms.items()}, labels=L, source_labels=S,
                    chunk=CHUNK, boxes=int(offs[-1]), source_boxes=int(np.concatenate([g[2] for g in gts]).sum()),
                    doc='docs/OVD_DETECTION_BENCHMARK.md', scope='Development data (COCO val2017). No fitting; no reserve access.',
                    hashes={p: digest(p) for p in code})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    seconds = {arm: 0.0 for arm in arms}; t0 = time.time()
    for k, im in enumerate(images):
        img = Image.open(IMAGES/im['coco_url'].split('/')[-1]).convert('RGB'); W, H = img.size
        px = None if a.model == 'owlv2' else det.pixels(img)
        gt = torch.from_numpy(gts[k][0]).cuda()
        for arm in arms:
            torch.cuda.synchronize(); t = time.perf_counter()
            s = arm_scores(arm, img, px, W, H, gt)
            torch.cuda.synchronize(); seconds[arm] += time.perf_counter()-t
            stores[arm][offs[k]:offs[k+1]] = s.half().cpu().numpy()
        if k % 50 == 0: print(f'{k+1}/{len(images)} {time.time()-t0:.0f}s', flush=True)
    for s in stores.values(): s.flush()
    (STORE/'.complete').write_text('ok')
    result = dict(images=len(images), seconds_per_image={k: v/len(images) for k, v in seconds.items()}, gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2)); print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
