"""Distribution of the per-pixel set size at the grown vocabulary, on the splits and thresholds of exp_headroom_splits.py.

Tab. 1 reports the mean number of labels per source-labelled pixel. This script keeps the same images, the same
500 random splits (same seed and draw order), the same CRC thresholds and the same image-weighted average, and
tabulates the whole distribution of |C(x,p)| over the evaluation pixels: the fraction of pixels whose set is empty,
has exactly one label, at most three, at most ten, more than ten, and the median and 90th percentile. Arms: native
calibrated and deployed at the source vocabulary, native reused after growth, native recalibrated at the grown
vocabulary, anchored calibrated at the source vocabulary. Development data; nothing is fitted.

Usage: python src/exp_set_size_dist.py --dataset ade --tag vitl_bank683
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS, curves

SEED, SPLITS = 20261003, 500        # as in exp_headroom_splits.py
# arm -> (store calibrated on, store evaluated on)
ARMS = dict(catseg_native_source=('native150', 'native150'), catseg_native_frozen_full=('native150', 'native845'),
            catseg_native_replay_full=('native845', 'native845'), catseg_anchored=('anchored845', 'anchored845'))
AT_MOST = [1, 3, 10]


def stats(dist):
    """Summary of a distribution over set sizes 0..T (sums to 1)."""
    cum = np.cumsum(dist); sizes = np.arange(len(dist))
    out = dict(frac_empty=float(dist[0]), frac_one=float(dist[1]), mean=float((dist*sizes).sum()),
               median=int(np.searchsorted(cum, .5)), p90=int(np.searchsorted(cum, .9)))
    for k in AT_MOST: out[f'frac_le{k}'] = float(cum[k])
    out['frac_gt10'] = float(dist[11:].sum())
    return out


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    d = dict(DATASETS[a.dataset])
    if a.tag and a.dataset == 'ade':
        d['runs'] = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        d['caches'] = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    elif a.tag:
        d['runs'] = [f'results/headroom_probe_{a.dataset}_{a.tag}']
        d['caches'] = [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    S, ADDITIONS = d['source'], d['additions']; T = S+ADDITIONS[-1]
    sfx = f'_{a.tag}' if a.tag else ''
    OUT = Path(f'results/set_size_dist_{a.dataset}{sfx}'); OUT.mkdir(parents=True, exist_ok=True)
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in d['runs']], [])
    assert len(set(ids)) == len(ids)
    gt_all = np.load(f"{d['sclip']}/{d['gt']}")[ids]
    names = dict(zip(['native150', 'native845', 'anchored845'], d['stores']))
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in d['caches']] for k, v in names.items()}
    keep = np.flatnonzero((gt_all < S).any(1)); n_img = len(keep)
    ref = json.loads(Path(f'results/headroom_splits_{a.dataset}{sfx}/results.json').read_text())
    assert ref['images'] == n_img and ref['splits'] == SPLITS, 'splits analysis out of step with the stores'

    def scores(store, k):
        for part in stores[store]:
            if k < len(part): return torch.from_numpy(np.array(part[k])).cuda().double()
            k -= len(part)

    grid = torch.from_numpy(LOGIT_GRID).cuda()
    # pass 1: image-level loss curves on the grid (the same tabulation as exp_headroom_splits.py, loss only)
    loss = {}
    for store in ['native150', 'native845', 'anchored845']:
        loss[store] = np.stack([curves(scores(store, k), torch.from_numpy(gt_all[k].astype(np.int64)).cuda(), grid, S, [S])[0] for k in keep])
        print('loss curves', store, loss[store].shape, flush=True)

    def pick(store, cal, alpha):
        return int(np.flatnonzero((loss[store][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1])

    # the same permutations as exp_headroom_splits.py: 500 for the 200-image design are drawn first, then 500 for the half split
    rng = np.random.default_rng(SEED)
    for _ in range(SPLITS): rng.permutation(n_img)
    perms = [rng.permutation(n_img) for _ in range(SPLITS)]
    n_cal = n_img//2
    chosen = {(alpha, arm): [pick(cal_store, p[:n_cal], alpha) for p in perms] for alpha in ALPHAS for arm, (cal_store, _) in ARMS.items()}
    need = {}      # eval store -> sorted unique grid indices
    for (alpha, arm), gs in chosen.items():
        need.setdefault(ARMS[arm][1], set()).update(gs)
    need = {s: sorted(g) for s, g in need.items()}
    print('thresholds per evaluation store:', {s: len(g) for s, g in need.items()}, flush=True)

    # pass 2: per-image normalised histogram of the set size at every needed threshold
    hist = {s: {g: np.zeros((n_img, T+1), dtype=np.float32) for g in gs} for s, gs in need.items()}
    for store, gs in need.items():
        thr = grid[torch.tensor(gs, device=grid.device)]
        for i, k in enumerate(keep):
            s = scores(store, k); valid = torch.from_numpy(gt_all[k] < S).cuda()
            s = s[valid]
            sizes = (s[None, :, :] >= thr[:, None, None]).sum(2)                         # [len(gs), n_valid]
            for j, g in enumerate(gs):
                hist[store][g][i] = (torch.bincount(sizes[j], minlength=T+1).double()/len(s)).cpu().numpy()
        print('histograms', store, flush=True)

    result = dict(dataset=a.dataset, tag=a.tag, images=n_img, splits=SPLITS, n_cal=n_cal, alphas=ALPHAS, source=S, total=T, at_most=AT_MOST, designs={})
    lines = ['# Distribution of the per-pixel set size at the grown vocabulary', '',
             f"{n_img} {d['name']} images, {S} source labels, {T} after growth; {SPLITS} random half splits (the splits of results/headroom_splits_{a.dataset}{sfx}); "
             'thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.', '']
    for alpha in ALPHAS:
        key = f'cal{n_cal}_a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha}', '', '| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for arm, (cal_store, ev_store) in ARMS.items():
            per_split = []
            dist_sum = np.zeros(T+1)
            for p, g in zip(perms, chosen[(alpha, arm)]):
                dist = hist[ev_store][g][p[n_cal:]].mean(0).astype(np.float64)
                dist_sum += dist; per_split.append(stats(dist))
            mean_dist = dist_sum/SPLITS
            agg = {k: float(np.mean([s[k] for s in per_split])) for k in per_split[0]}
            agg.update({k+'_sd': float(np.std([s[k] for s in per_split], ddof=1)) for k in ['frac_one', 'frac_le3', 'frac_le10', 'frac_gt10']})
            agg['median_of_mean_dist'] = stats(mean_dist)['median']; agg['p90_of_mean_dist'] = stats(mean_dist)['p90']
            ref_arm = ref['designs'][key][arm]; ref_mean = ref_arm['mean_size'][-1] if ev_store != 'native150' else ref_arm['mean_size'][0]
            assert abs(agg['mean']-ref_mean) < 2e-3, (arm, agg['mean'], ref_mean)
            agg['tab1_mean'] = ref_mean; agg['distribution'] = mean_dist.tolist()
            result['designs'][key][arm] = agg
            lines.append(f"| {arm} | {S if ev_store == 'native150' else T} | {100*agg['frac_empty']:.1f} | {100*agg['frac_one']:.1f} | {100*agg['frac_le3']:.1f} | {100*agg['frac_le10']:.1f} | "
                         f"{100*agg['frac_gt10']:.1f} | {agg['median']:.1f} | {agg['p90']:.1f} | {agg['mean']:.2f} | {ref_mean:.2f} |")
        lines.append('')
    lines += ['Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_set_size_dist.py', 'src/exp_headroom_splits.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
