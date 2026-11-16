"""Label-level CRC with the image-averaged label loss: the quantity of the new-image result (prop:newimages).

prop:labels holds for any bounded label loss that is non-decreasing in t; exp_label_exchange.py (protocol-frozen) uses the
pooled loss, the fraction of all of a label's sampled pixels in the calibration images that are missed. The new-image
result needs the image-averaged loss instead: for each image containing the label, the fraction of the label's sampled
pixels missed, averaged over those images. Its value on held-out images estimates the expected miss rate of the label on
a new image that contains it. This script replays the "exchangeable" design of exp_label_exchange.py (the same seed,
image splits and random source vocabularies, drawn in the same order) for the anchored scores and reports both losses;
the pooled columns reproduce the frozen script's "anchored, label-level" row, which checks the replay.

    PYTHONPATH=src python src/exp_label_exchange_images.py --dataset ade --tag vitl_bank683 [--device cpu]
    (--dataset coco registers the COCO entry of coco_frozen_analyses.py; nothing frozen is edited or executed)
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_added_label_risk import DATASETS
from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_label_exchange import gt_all


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=['ade', 'pascal', 'coco'])
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--trials', type=int, default=500)
    ap.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    a = ap.parse_args()
    if a.dataset == 'coco':
        from coco_frozen_analyses import coco_entry
        DATASETS.setdefault('coco', coco_entry())
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']; dev = a.device
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_{a.dataset}_{a.tag}'], [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    store = [np.load(f'{c}/{d["stores"][2]}.npy', mmap_mode='r') for c in caches]
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)

    def part(k):
        for p in store:
            if k < len(p): return p[k]
            k -= len(p)

    pimg, plab, pn, miss = [], [], [], []
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0
        labs = torch.unique(g[lab_px])
        s = torch.from_numpy(np.array(part(k))).to(dev)[lab_px].float()
        true = s.gather(1, g[lab_px][:, None])[:, 0].double(); gl = g[lab_px]
        miss.append(torch.stack([torch.searchsorted(true[gl == c].sort().values, grid, right=False) for c in labs]).float())
        pimg.append(torch.full((len(labs),), i, device=dev)); plab.append(labs); pn.append(torch.stack([(gl == c).sum() for c in labs]).float())
        if i % 400 == 0: print(f'{i+1}/{n}', flush=True)
    pimg, plab, pn, miss = torch.cat(pimg), torch.cat(plab), torch.cat(pn), torch.cat(miss)
    frac = miss/pn[:, None]                                            # per-image fraction of the label's pixels missed [pair, G]

    def label_losses(imgmask):
        sel = imgmask[pimg]
        pooled = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], miss[sel])
        den = torch.zeros(T, device=dev).index_add_(0, plab[sel], pn[sel])
        avg = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], frac[sel])
        cnt = torch.zeros(T, device=dev).index_add_(0, plab[sel], torch.ones_like(pn[sel]))
        return dict(pooled=pooled/den.clamp(min=1)[:, None], images=avg/cnt.clamp(min=1)[:, None]), den > 0

    def crc(losses, alpha):
        ok = torch.nonzero((losses.sum(0)+1)/(len(losses)+1) <= alpha)
        return int(ok[-1]) if len(ok) else 0

    rng = np.random.default_rng(20260926)                              # exp_label_exchange.py: same draws, same order
    perms = [rng.permutation(n) for _ in range(a.trials)]
    random_sets = [np.sort(rng.choice(T, S, replace=False)) for _ in range(a.trials)]
    acc = {}
    for perm, src in zip(perms, random_sets):
        cal = torch.zeros(n, dtype=torch.bool, device=dev); cal[torch.from_numpy(perm[:n//2]).to(dev)] = True
        srcm = torch.zeros(T, dtype=torch.bool, device=dev); srcm[torch.from_numpy(src).to(dev)] = True
        lc, pc = label_losses(cal); le, pe = label_losses(~cal)
        for alpha in ALPHAS:
            for loss in ['pooled', 'images']:
                t = crc(lc[loss][pc & srcm], alpha)
                acc.setdefault((alpha, loss), []).append((lc[loss][pc & ~srcm, t].mean().item(), le[loss][pe & ~srcm, t].mean().item(), t))
    result = dict(dataset=a.dataset, tag=a.tag, images=n, trials=a.trials, design='exchangeable (random source vocabulary), anchored scores', alphas={})
    lines = [f'# Label-level CRC, pooled vs image-averaged label loss ({a.dataset}, {a.tag}, {n} images, {a.trials} trials)', '',
             '| alpha | loss | added, cal | added, held-out | % trials above alpha (cal / held-out) |', '|---|---|---:|---:|---:|']
    for (alpha, loss), v in acc.items():
        v = np.array(v); m = v[:, :2].mean(0); ab = (v[:, :2] > alpha).mean(0)
        result['alphas'].setdefault(str(alpha), {})[loss] = dict(added_cal=m[0], added_heldout=m[1], above_added_cal=ab[0], above_added_heldout=ab[1])
        lines.append(f'| {alpha} | {loss} | {100*m[0]:.2f} | {100*m[1]:.2f} | {100*ab[0]:.0f} / {100*ab[1]:.0f} |')
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_label_exchange_images.py', 'src/exp_label_exchange.py', f"{d['sclip']}/{d['gt_fine']}"]}
    OUT = Path(f'results/label_exchange_images_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2)); (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
