"""Peak GPU memory per arm for FC-CLIP, native against anchored, as the vocabulary grows (FC-CLIP counterpart of exp_memory.py).

  features  not separated: FC-CLIP's backbone, pixel decoder and mask proposals run inside one forward with the text classifier;
  native    the deployment pass of exp_fcclip_probe.py --time-native-only: V candidates + void in the classifier, the released
            semantic inference at the sampled pixels;
  anchored  V candidates + the reference bank (FC-CLIP's 133 training classes with their synonyms plus the names of
            meta/bank_coco_oi683_v1.json not among them, as --extra-bank in the probe) + void, scored against the bank.
The peak is reset before each arm; "peak" is the maximum of torch.cuda.max_memory_allocated() over the images. The geometric
ensemble weight is beta for every candidate here (the weight changes values, not memory); scores are not stored. Same
vocabularies, images and pixel samples as exp_memory.py. Development images; nothing fitted.

    PYTHONPATH=src .venv-fcclip/Scripts/python.exe src/exp_memory_fcclip.py [--limit 20]
"""
import argparse
import gc
import json
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from encode import ADE, sample_phi
from exp_fcclip_probe import CKPT, load_model, resize_shortest, text_classifier
from exp_fixed_source import digest
from natural_vocab import load_manifest

SIZES = [150, 845, 1690, 3380, 6760]          # as exp_memory.py (not imported: it loads the CAT-Seg checkout)
BANK = 'meta/bank_coco_oi683_v1.json'
GiB = 2**30


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=20)
    ap.add_argument('--sizes', default=','.join(map(str, SIZES)))
    a = ap.parse_args()
    OUT = Path('results/memory_fcclip'); OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    sizes = [int(s) for s in a.sizes.split(',')]
    split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
    ids = [r['index'] for role in ['tune_cal', 'tune_eval'] for r in split['roles'][role]][:a.limit]
    names = [r['prompt'] for r in load_manifest()['rows']]
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    lexicon = (names+[oi[i] for i in np.random.default_rng(1).permutation(len(oi))])[:max(sizes)]

    from detectron2.structures import ImageList
    model, _ = load_model()  # puts the fc-clip checkout on sys.path
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    torch.cuda.synchronize(); weights = torch.cuda.memory_allocated()
    bank_lists = [c.replace(', ', ',').split(',') for c in model.train_metadata.stuff_classes]
    known = {s.lower() for syns in bank_lists for s in syns}
    bank_lists = bank_lists+[[n] for n in json.loads(Path(BANK).read_text())['names'] if n.lower() not in known]
    B = len(bank_lists)
    text_cand, nt_cand = text_classifier(model, [[n] for n in lexicon]); text_cand = text_cand.cpu()
    text_bank, nt_bank = text_classifier(model, bank_lists)
    void = F.normalize(model.void_embedding.weight, dim=-1)
    beta = model.geometric_ensemble_beta
    mean, std = model.pixel_mean, model.pixel_std
    meta = json.loads(Path('cache/sclip/meta.json').read_text())

    def forward(images, text, nt):
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        return mask_cls, out_cls, mask_pred

    def masks(images, mask_pred, y, x, H, W):
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
        ih, iw = images.image_sizes[0]
        return sample_phi(up[None, :, :ih, :iw], y, x, H, W).double().sigmoid()

    def native(images, V, y, x, H, W):
        in_l, out_l, mask_pred = forward(images, torch.cat([text_cand[:V].cuda(), void]), nt_cand[:V])
        in_l, out_l = in_l.double(), out_l.double()
        cls = (in_l[:, :V].softmax(-1)**(1-beta)*out_l[:, :V].softmax(-1)**beta).log()
        v = in_l.softmax(-1)[:, -1:]
        return masks(images, mask_pred, y, x, H, W)@(cls.softmax(-1)*(1-v))

    def anchored(images, V, y, x, H, W):
        in_l, out_l, mask_pred = forward(images, torch.cat([text_cand[:V].cuda(), text_bank, void]), nt_cand[:V]+nt_bank)
        in_l, out_l = in_l.double(), out_l.double()
        vs_bank = lambda cand, bank: cand-torch.logaddexp(cand, torch.logsumexp(bank, -1, keepdim=True))
        g = (1-beta)*vs_bank(in_l[:, :V], in_l[:, V:V+B])+beta*vs_bank(out_l[:, :V], out_l[:, V:V+B])
        g_bank = (1-beta)*in_l[:, V:V+B].log_softmax(-1)+beta*out_l[:, V:V+B].log_softmax(-1)
        v = torch.cat([in_l[:, V:V+B], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return masks(images, mask_pred, y, x, H, W)@(vs_bank(g, g_bank).exp()*(1-v))

    arms = dict(native=native, anchored=anchored)
    peak = {k: {V: 0. for V in sizes} for k in arms}; oom = {k: [] for k in arms}
    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        for arm, fn in arms.items():
            for V in sizes:
                if V in oom[arm]: continue
                gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
                try:
                    out = fn(images, V, y, x, H, W); torch.cuda.synchronize(); del out
                    peak[arm][V] = max(peak[arm][V], torch.cuda.max_memory_allocated())
                except torch.cuda.OutOfMemoryError:
                    oom[arm].append(V); print(f'{arm} V={V}: out of memory', flush=True)
        print(f'{k+1}/{len(ids)} '+' '.join(f'{arm}@{sizes[-1]}={peak[arm][sizes[-1]]/GiB:.2f}' for arm in arms), flush=True)

    result = dict(model='fcclip', tag='fcclip', gpu=torch.cuda.get_device_name(0), images=len(ids), vocab_sizes=sizes, weights_gb=weights/GiB,
                  peak_gb={arm: {str(V): v/GiB for V, v in d.items()} for arm, d in peak.items()}, out_of_memory=oom,
                  bank_size=B, bank_text_bytes=text_bank.numel()*text_bank.element_size())
    protocol = dict(image_ids=ids, bank=BANK, note=__doc__.split('\n\n')[0],
                    hashes={p: digest(Path(p)) for p in ['src/exp_memory_fcclip.py', 'src/exp_fcclip_probe.py', 'meta/natural_vocab_v1.json', BANK, str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = ['# Peak GPU memory per arm, fcclip', '', f"{len(ids)} development images, {result['gpu']}, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.", '',
             f"Weights {result['weights_gb']:.2f} GiB; bank {B} classes.", '', '| Arm | '+' | '.join(f'V={V:,}' for V in sizes)+' |', '|---|'+'---:|'*len(sizes)]
    for arm in arms:
        lines.append(f'| {arm} | '+' | '.join('OOM' if V in oom[arm] else f'{peak[arm][V]/GiB:.2f}' for V in sizes)+' |')
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
