"""Full-resolution mIoU of released and reference-anchored FC-CLIP on the standard open-vocabulary benchmarks.

The FC-CLIP counterpart of exp_miou_full.py: the released semantic inference (a847 evaluation config, shortest edge 800,
250 queries; per-query class probabilities times sigmoid masks, summed over queries, arg-max) with the deployed vocabulary
equal to the benchmark vocabulary, against the reference-anchored conversion of exp_fcclip_probe.py (every softmax over
the deployed vocabulary replaced by a softmax over {label} + bank) with the training-vocabulary bank (COCO panoptic 133
with the released synonym lists) and with that bank plus the 683-name bank (701 entries). Benchmark names come from the
CAT-Seg checkout's datasets/*.json; comma-separated synonyms are passed as FC-CLIP synonym lists (max over synonyms, its
released behaviour). Confusion over all annotated pixels, mIoU over classes with ground-truth pixels. Development data;
nothing is fitted. Runs in .venv-fcclip on the GH200.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from exp_fcclip_probe import CKPT, load_model, resize_shortest, text_classifier
from exp_fixed_source import digest
from exp_miou_full import ade_items, benchmark_names, load_gt, miou, pascal_items, pascal_lut

ARMS = ['native', 'anchored_133', 'anchored_bank683']


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade150', choices=['ade150', 'ade847', 'pc459', 'pc59'])
    ap.add_argument('--bank683', default='meta/bank_coco_oi683_v1.json')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--tag', default='fcclip')
    ap.add_argument('--check', action='store_true', help='first image: the anchored scores of bank labels equal the released pipeline on the bank vocabulary')
    a = ap.parse_args()
    OUT = Path(f'results/miou_full_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    names = benchmark_names(a.dataset); K = len(names)
    class_lists = [n.split(', ') if ', ' in n else [n] for n in names]
    if a.dataset.startswith('ade'):
        items, lut = ade_items(a.dataset, a.limit), None
    else:
        items, lut = pascal_items(a.dataset, a.limit), pascal_lut(a.dataset, names)

    from detectron2.data import MetadataCatalog
    from detectron2.structures import ImageList
    model, cfg = load_model()
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    model.set_metadata(MetadataCatalog.get(f'vscrc_{a.dataset}_miou').set(stuff_classes=list(names)))
    bank_lists = [c.replace(', ', ',').split(',') for c in model.train_metadata.stuff_classes]          # COCO panoptic 133 with FC-CLIP's synonyms
    B0 = len(bank_lists); known = {s.lower() for syns in bank_lists for s in syns}
    extras = [n for n in json.loads(Path(a.bank683).read_text())['names'] if n.lower() not in known]
    bank_lists = bank_lists+[[n] for n in extras]; B = len(bank_lists)
    text_cand, nt_cand = text_classifier(model, class_lists)
    text_bank, nt_bank = text_classifier(model, bank_lists)
    text = torch.cat([text_cand, text_bank, F.normalize(model.void_embedding.weight, dim=-1)], 0)
    nt = nt_cand+nt_bank
    self_idx = torch.tensor([next((j for j, syns in enumerate(bank_lists) if any(s in syns for s in cl)), -1) for cl in class_lists], device=model.device)
    overlap = model.category_overlapping_mask.to(model.device).bool()
    assert torch.equal(overlap, (self_idx >= 0) & (self_idx < B0)) and B0 == 133 and not model.ensemble_on_valid_mask
    alpha, beta = model.geometric_ensemble_alpha, model.geometric_ensemble_beta
    ens = torch.where(overlap, alpha, beta).double()
    ens_bank = torch.where(torch.arange(B, device=model.device) < B0, alpha, beta).double()
    bank_mask = torch.zeros(K, B, dtype=torch.double, device=model.device)
    bank_mask[self_idx >= 0, self_idx[self_idx >= 0]] = -float('inf')
    protocol = dict(model='fcclip', size='convnext_large', dataset=a.dataset, classes=K, images=len(items), arms=ARMS, bank683=a.bank683, bank_sizes=dict(anchored_133=B0, anchored_bank683=B),
        names='CAT-Seg checkout datasets/%s.json; comma-separated synonyms as FC-CLIP synonym lists (max over synonyms), 14 ViLD templates averaged.' % a.dataset,
        inference='Released FC-CLIP ConvNeXt-L (COCO panoptic weights), a847 evaluation config: shortest edge 800 (max 1333), 250 queries; masks resampled to the annotation grid, sigmoid, weighted by per-query class probabilities, summed over queries, arg-max.',
        native='Released semantic inference: in-/out-of-vocabulary logits softmaxed over the deployed (= benchmark) vocabulary, geometric ensemble (alpha .4 training names, beta .8 others), softmax, times one minus the void probability.',
        anchored='Every softmax over the deployed vocabulary replaced by a softmax over {label} + bank (the label\'s own bank entry removed), void from bank + void; bank = training vocabulary (133) or training vocabulary + 683-name bank (%d).' % B,
        metric='Confusion over all annotated pixels; mIoU over classes with ground-truth pixels; pc459 keeps "unknown" as a class.',
        scope='Development data (ADE validation, Pascal Context validation); nothing is fitted; no reserve access.',
        hashes={str(p): digest(Path(p)) for p in ['src/exp_fcclip_miou.py', 'src/exp_fcclip_probe.py', 'src/exp_miou_full.py', str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))

    def native(in_l, out_l, V, e=None):
        in_p, out_p = in_l[:, :V].softmax(-1), out_l[:, :V].softmax(-1)
        e = ens[:V] if e is None else e
        cls = (in_p**(1-e)*out_p**e).log()
        void = torch.cat([in_l[:, :V], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return cls.softmax(-1)*(1-void)

    def vs_bank(cand, bank, Bs):
        lse = torch.logsumexp(bank[:, None, :]+bank_mask[:, :Bs], -1)
        return cand-torch.logaddexp(cand, lse)

    def anchored(in_l, out_l, Bs):
        """Reference-anchored per-query class probabilities [Q, K] against the first Bs bank entries."""
        ib, ob = in_l[:, K:K+Bs], out_l[:, K:K+Bs]
        lp_in, lp_out = vs_bank(in_l[:, :K], ib, Bs), vs_bank(out_l[:, :K], ob, Bs)
        g = (1-ens)*lp_in+ens*lp_out
        g_bank = (1-ens_bank[:Bs])*ib.log_softmax(-1)+ens_bank[:Bs]*ob.log_softmax(-1)
        void = torch.cat([ib, in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return vs_bank(g, g_bank, Bs).exp()*(1-void)

    def forward(images):
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        return mask_cls, out_cls, mask_pred

    def argmax_full(P, m, chunk=128):
        """P [Q, K] class probabilities, m [Q, H*W] sigmoid masks: arg-max over classes of the mask-weighted sum, chunked over classes."""
        best = arg = None
        for i in range(0, K, chunk):
            s = m.T@P[:, i:i+chunk]                                       # [HW, c]
            v, j = s.max(1)
            if best is None: best, arg = v, j+i
            else:
                upd = v > best; best = torch.where(upd, v, best); arg = torch.where(upd, j+i, arg)
        return arg

    conf = {arm: torch.zeros(K*K, dtype=torch.long, device='cuda') for arm in ARMS}
    seconds = dict.fromkeys(ARMS, 0.); t_feat = 0.
    mean, std = model.pixel_mean, model.pixel_std
    for k, (stem, path, key) in enumerate(items):
        gt = torch.from_numpy(load_gt(a.dataset, key, K, lut)).cuda(); H, W = gt.shape
        valid = (gt >= 0).reshape(-1); gtf = gt.reshape(-1)
        img = Image.open(path).convert('RGB')
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        mask_cls, out_cls, mask_pred = forward(images)
        ih, iw = images.image_sizes[0]
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0][:, :ih, :iw]
        m = F.interpolate(up[None], size=(H, W), mode='bilinear', align_corners=False)[0].sigmoid().reshape(up.shape[0], -1).double()   # [Q, HW]
        in_l, out_l = mask_cls.double(), out_cls.double()
        torch.cuda.synchronize(); t_feat += time.perf_counter()-t0
        if a.check and k == 0:
            single = torch.tensor([len(s) == 1 for s in bank_lists], device=model.device)
            j = torch.nonzero((self_idx >= 0) & single[self_idx.clamp(min=0)] & torch.tensor([len(c) == 1 for c in class_lists], device=model.device))[:, 0]
            ref = native(torch.cat([in_l[:, K:K+B], in_l[:, -1:]], -1), out_l[:, K:K+B], B, ens_bank)
            assert torch.allclose(anchored(in_l, out_l, B)[:, j], ref[:, self_idx[j]], atol=1e-6), 'anchored != native on the bank'
            print(f'check ok: anchored equals the released pipeline on the bank vocabulary for {len(j)} single-synonym labels (bank {B})', flush=True)
        for arm in ARMS:
            torch.cuda.synchronize(); t0 = time.perf_counter()
            P = native(in_l, out_l, K) if arm == 'native' else anchored(in_l, out_l, B0 if arm == 'anchored_133' else B)
            pred = argmax_full(P, m)
            conf[arm] += torch.bincount(gtf[valid]*K+pred[valid], minlength=K*K)
            torch.cuda.synchronize(); seconds[arm] += time.perf_counter()-t0
        if k % 100 == 0:
            print(f'{k+1}/{len(items)} '+' '.join(f'{arm}={100*miou(conf[arm].view(K, K))[0]:.2f}' for arm in ARMS), flush=True)
    result = dict(images=len(items), classes=K, per_arm={}, seconds_per_image=dict(features_masks_logits=t_feat/len(items), **{arm: s/len(items) for arm, s in seconds.items()}),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    for arm in ARMS:
        c = conf[arm].view(K, K); mi, iou, present = miou(c)
        result['per_arm'][arm] = dict(miou=mi, pixel_accuracy=float(c.diag().sum()/c.sum()), classes_present=int(present.sum()), per_class_iou=iou.tolist())
    np.savez_compressed(OUT/'confusion.npz', **{arm: conf[arm].view(K, K).cpu().numpy() for arm in ARMS})
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = [f'# Full-resolution mIoU, {a.dataset} ({K} classes), FC-CLIP ConvNeXt-L', '', f'{len(items)} validation images; arg-max prediction; mIoU over classes with ground-truth pixels.', '',
             '| Arm | mIoU | Pixel accuracy | Seconds / image |', '|---|---:|---:|---:|']
    lines += [f"| {arm} | {100*result['per_arm'][arm]['miou']:.2f} | {100*result['per_arm'][arm]['pixel_accuracy']:.2f}% | {result['seconds_per_image'][arm]:.2f} |" for arm in ARMS]
    lines += ['', f"Backbone, masks and logits {result['seconds_per_image']['features_masks_logits']:.2f} s/image on {result['gpu']}; peak memory {result['peak_memory_gb']:.1f} GB. Development data; nothing fitted."]
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
