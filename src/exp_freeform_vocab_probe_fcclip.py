"""Native and anchored FC-CLIP scores under free-form per-image names: exp_freeform_vocab_probe.py for FC-CLIP.

Same names, images, sampled pixels and store layout as exp_freeform_vocab_probe.py, so exp_freeform_vocab.py runs
unchanged with --tag fcclip_bank683. One forward pass per image with the text classifier [150 source names, the image's
added names A(x), the run's reference bank, void]; FC-CLIP's per-query logits and masks do not depend on the other
classifier rows (exp_fcclip_probe.py --check), so the source columns equal those of the stored scores. Native = the
released semantic inference over the deployed columns; anchored = the conversion of exp_fcclip_probe.py (each label against
{label} + bank, its own bank entry removed). Out-of-vocabulary ensemble weight per name by FC-CLIP's own rule (alpha if
the name is a COCO panoptic training synonym, beta otherwise). Stores hold log(score + 1e-8) clamped to [-30, 30] in
float16, as the FC-CLIP headroom stores. Runs in .venv-fcclip. Development data; nothing is fitted; the reserve is not read.

    PYTHONPATH=src .venv-fcclip/Scripts/python.exe src/exp_freeform_vocab_probe_fcclip.py --tag fcclip_bank683 [--check]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from encode import ADE, sample_phi
from exp_fixed_source import digest
from natural_vocab import load_manifest

S = 150
NAMES = Path('results/freeform_names_ade/names.json')


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='fcclip_bank683')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true', help='compare native at 150 names and the anchored source columns with the stored scores on 3 images, then stop')
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
    caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p['model'] == 'fcclip' for p in protos) and len({p['extra_bank'] for p in protos}) == 1
    ids = sum([p['image_ids'] for p in protos], [])
    free = json.loads(NAMES.read_text())
    assert free['image_ids'] == ids, 'names.json must cover the probe images in probe order'
    if a.limit: ids = ids[:a.limit]
    added = [free['added'][str(i)] for i in ids]
    unique = sorted({n for A in added for n in A}); col = {n: j for j, n in enumerate(unique)}
    width = max(len(A) for A in added)
    OUT, STORE = Path(f'results/freeform_vocab_probe_{a.tag}'), Path(f'cache/freeform_vocab_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    stored = {k: [np.load(f'{c}/{k}.npy', mmap_mode='r') for c in caches] for k in ['native150', 'anchored845']}

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    from detectron2.data import MetadataCatalog
    from detectron2.structures import ImageList
    from exp_fcclip_probe import CKPT, load_model, resize_shortest, text_classifier
    model, cfg = load_model()
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    rows = load_manifest()['rows']; names = [r['prompt'] for r in rows]
    model.set_metadata(MetadataCatalog.get(f'vscrc_ade_natural_{len(names)}').set(stuff_classes=list(names)))
    bank_lists = [c.replace(', ', ',').split(',') for c in model.train_metadata.stuff_classes]
    B0, extra_bank = len(bank_lists), protos[0]['extra_bank']
    train_names = {s for syns in bank_lists for s in syns}
    if extra_bank:
        known = {s.lower() for syns in bank_lists for s in syns}
        bank_lists = bank_lists+[[n] for n in json.loads(Path(extra_bank).read_text())['names'] if n.lower() not in known]
    B = len(bank_lists)
    assert B == protos[0]['bank_size']
    alpha, beta = model.geometric_ensemble_alpha, model.geometric_ensemble_beta
    overlap = model.category_overlapping_mask.to(model.device).bool()
    assert torch.equal(overlap[:S], torch.tensor([n in train_names for n in names[:S]], device=model.device)), 'FC-CLIP overlap rule'
    ens_bank = torch.where(torch.arange(B, device=model.device) < B0, alpha, beta).double()
    text_src, nt_src = text_classifier(model, [[n] for n in names[:S]])
    text_free, nt_free = text_classifier(model, [[n] for n in unique])
    text_bank, nt_bank = text_classifier(model, bank_lists)
    void = F.normalize(model.void_embedding.weight, dim=-1)
    mean, std = model.pixel_mean, model.pixel_std
    meta = json.loads(Path('cache/sclip/meta.json').read_text())

    def label_info(labels):
        ens = torch.tensor([alpha if n in train_names else beta for n in labels], dtype=torch.double, device=model.device)
        self_idx = torch.tensor([next((j for j, syns in enumerate(bank_lists) if n in syns), -1) for n in labels], device=model.device)
        mask = torch.zeros(len(labels), B, dtype=torch.double, device=model.device)
        mask[self_idx >= 0, self_idx[self_idx >= 0]] = -float('inf')
        return ens, mask

    def scores(index, labels, text_rows, nt_rows):
        """(native, anchored) per-query class probabilities times the void term, sampled at the image's pixels: [P, L] each."""
        info = meta['meta'][index]; H, W = info['H'], info['W']
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        text, nt = torch.cat([text_rows, text_bank, void]), nt_rows+nt_bank
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
        ih, iw = images.image_sizes[0]
        m = sample_phi(up[None, :, :ih, :iw], y, x, H, W).double().sigmoid()
        in_l, out_l = mask_cls.double(), out_cls.double(); L = len(labels)
        ens, bank_mask = label_info(labels)
        # native: released semantic inference over the deployed columns (exp_fcclip_probe.native)
        cls = (in_l[:, :L].softmax(-1)**(1-ens)*out_l[:, :L].softmax(-1)**ens).log()
        void_p = torch.cat([in_l[:, :L], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        native = m@(cls.softmax(-1)*(1-void_p))
        # anchored (exp_fcclip_probe.anchored)
        vs_bank = lambda cand, bank: cand-torch.logaddexp(cand, torch.logsumexp(bank[:, None, :]+bank_mask, -1))
        g = (1-ens)*vs_bank(in_l[:, :L], in_l[:, L:L+B])+ens*vs_bank(out_l[:, :L], out_l[:, L:L+B])
        g_bank = (1-ens_bank)*in_l[:, L:L+B].log_softmax(-1)+ens_bank*out_l[:, L:L+B].log_softmax(-1)
        void_b = torch.cat([in_l[:, L:L+B], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        anchored = m@(vs_bank(g, g_bank).exp()*(1-void_b))
        store = lambda s: (s+1e-8).log().clamp(-30, 30).half().cpu().numpy()
        return store(native), store(anchored)

    def rows_for(A):
        idx = torch.tensor([col[n] for n in A], dtype=torch.long, device=model.device)
        return names[:S]+A, torch.cat([text_src, text_free[idx]]), nt_src+[nt_free[col[n]] for n in A]

    if a.check:
        report = {}
        for k, index in enumerate(ids[:3]):
            labels, tr, nr = rows_for(added[k])
            n150, _ = scores(index, names[:S], text_src, nt_src)                   # source vocabulary alone
            _, anch = scores(index, labels, tr, nr)                                 # anchored source columns with A(x) in the classifier
            d0 = np.abs(n150.astype(np.float32)-part(stored['native150'], k).astype(np.float32))
            d1 = np.abs(anch[:, :S].astype(np.float32)-part(stored['anchored845'], k)[:, :S].astype(np.float32))
            report[int(index)] = dict(native150_max_abs=float(d0.max()), native150_mean=float(d0.mean()),
                                      anchored_source_max_abs=float(d1.max()), anchored_source_mean=float(d1.mean()))
            print(index, report[int(index)], flush=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    protocol = dict(image_ids=ids, tag=a.tag, model='fcclip', size='convnext_large', bank=f'training vocabulary + {extra_bank}', bank_size=B,
                    names=str(NAMES), names_sha256=digest(NAMES), unique_added_names=len(unique),
                    added_names_per_image=dict(mean=float(np.mean([len(A) for A in added])), max=width),
                    vocabulary=f'{S} source names followed by the image\'s added names in the order of the answer; released semantic inference over exactly this list.',
                    stores=f'{STORE}/native.npy: float16 log(score + 1e-8) [image, pixel, {S}+width]; anchored_added.npy: anchored scores of A(x) '
                           '[image, pixel, width]; padding columns 0; n_added.npy gives |A(x)|.',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_freeform_vocab_probe_fcclip.py', 'src/exp_fcclip_probe.py', 'meta/natural_vocab_v1.json', str(CKPT)] + ([extra_bank] if extra_bank else [])})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    np.save(STORE/'n_added.npy', np.array([len(A) for A in added], np.int16))
    stores = {'native': np.lib.format.open_memmap(STORE/'native.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], S+width)),
              'anchored_added': np.lib.format.open_memmap(STORE/'anchored_added.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], width))}
    t_start = time.time()
    for k, index in enumerate(ids):
        labels, tr, nr = rows_for(added[k])
        nat, anch = scores(index, labels, tr, nr)
        stores['native'][k] = 0; stores['native'][k, :, :len(labels)] = nat
        stores['anchored_added'][k] = 0; stores['anchored_added'][k, :, :len(added[k])] = anch[:, S:]
        if k % 50 == 0: print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
    for s in stores.values(): s.flush()
    result = dict(images=len(ids), seconds_total=time.time()-t_start, gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, added_names_per_image=protocol['added_names_per_image'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
