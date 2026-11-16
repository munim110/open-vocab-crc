"""Distribution of the per-pixel set size under the label-level threshold, on the trials of exp_label_exchange.py.

Tab. 2 and Tab. S-labelmodels report, per arm, the mean number of labels per labelled pixel at the grown vocabulary on
the held-out images. This script replays the same trials (same seed and draw order: 500 random half splits, a random
source vocabulary per trial or one of the K frozen sets on ADE20K, or the dataset's own split), selects the same
thresholds (label-level CRC over the source labels present in the calibration images, image-level CRC on the
calibration images, and their minimum), and tabulates the whole distribution of |C(x,p)| over the labelled pixels of
the held-out images: fraction of pixels whose set is empty, has exactly one label, at most three, at most ten, more
than ten, and the median. Arms: anchored label-level, anchored image-level, anchored both (min), native calibrated at
the grown vocabulary label-level. Development data; nothing is fitted. The mean is checked against the stored
label-exchange results.

    PYTHONPATH=src python src/exp_set_size_dist_label.py --dataset ade --tag vitl_bank683
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_label_exchange import DATASETS as LX_DATASETS, gt_all
from exp_set_size_dist import stats

SEED, TRIALS = 20260926, 500          # as in exp_label_exchange.py
ARMS = {'anchored, label-level': 'anchored845', 'anchored, image-level (paper)': 'anchored845', 'anchored, both': 'anchored845',
        'native, full known, label-level': 'native845'}
CHUNK = 32


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=['ade', 'pascal', 'coco'])
    ap.add_argument('--tag', default='vitl_bank683')
    a = ap.parse_args()
    if a.dataset == 'coco':
        from coco_frozen_analyses import coco_entry
        d = coco_entry()
    else:
        d = LX_DATASETS[a.dataset]
    S, T = d['S'], d['T']
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_{a.dataset}_{a.tag}'], [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(['native845', 'anchored845'], d['stores'][1:])}
    PROBE = Path(f'results/label_exchange_probe_{a.tag}')
    frozen_sets = None
    if a.dataset == 'ade' and (PROBE/'results.json').exists():
        proto = json.loads((PROBE/'protocol.json').read_text())
        assert proto['image_ids'] == ids
        frozen_sets = [np.array(s) for s in proto['source_sets']]
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)
    ref_dir = 'results/label_exchange_ade_vitl_bank683' if (a.dataset, a.tag) == ('ade', 'vitl_bank683') else f'results/label_exchange_{a.dataset}_{a.tag}_schemes'
    ref = json.loads(Path(f'{ref_dir}/results.json').read_text())
    assert ref['images'] == n and ref['trials'] == TRIALS, 'label-exchange results out of step with the stores'

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    def counts(true, lab, labs):
        true = true.double(); return torch.stack([torch.searchsorted(true[lab == c].sort().values, grid, right=False) for c in labs]).to(torch.int16).cpu()

    # pass 1: miss counts per (image, label) pair on the grid, as in exp_label_exchange.py
    pair_img, pair_lab, pair_n = [], [], []
    miss = {k: [] for k in stores}
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0
        labs = torch.unique(g[lab_px])
        pair_img.append(np.full(len(labs), i)); pair_lab.append(labs.cpu().numpy())
        pair_n.append(torch.stack([(g == c).sum() for c in labs]).cpu().numpy())
        for name in stores:
            s = torch.from_numpy(np.array(part(stores[name], k))).to(dev)[lab_px].float()
            miss[name].append(counts(s.gather(1, g[lab_px][:, None])[:, 0], g[lab_px], labs))
        if i % 400 == 0: print(f'pass 1 {i+1}/{n}', flush=True)
    pair_img, pair_lab, pair_n = map(np.concatenate, (pair_img, pair_lab, pair_n))
    miss = {k: torch.cat(v).float().to(dev) for k, v in miss.items()}
    pimg, plab, pn = torch.from_numpy(pair_img).to(dev), torch.from_numpy(pair_lab).to(dev), torch.from_numpy(pair_n).float().to(dev)

    def label_loss(store, imgmask):
        sel = torch.from_numpy(imgmask).to(dev)[pimg]
        num = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], miss[store][sel])
        den = torch.zeros(T, device=dev).index_add_(0, plab[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def image_loss(store, labmask):
        sel = torch.from_numpy(labmask).to(dev)[plab]
        num = torch.zeros(n, G, device=dev).index_add_(0, pimg[sel], miss[store][sel])
        den = torch.zeros(n, device=dev).index_add_(0, pimg[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def crc(losses, alpha):
        bound = (losses.sum(0)+1)/(len(losses)+1)
        ok = torch.nonzero(bound <= alpha)
        return int(ok[-1]) if len(ok) else 0

    rng = np.random.default_rng(SEED)
    perms = [rng.permutation(n) for _ in range(TRIALS)]
    random_sets = [np.sort(rng.choice(T, S, replace=False)) for _ in range(TRIALS)]
    designs = {'exchangeable': [(p, s) for p, s in zip(perms, random_sets)], 'dataset split': [(p, np.arange(S)) for p in perms]}
    if frozen_sets:
        designs['exchangeable, native frozen'] = [(p, frozen_sets[t % len(frozen_sets)]) for t, p in enumerate(perms)]
    chosen = {}
    for design, trials in designs.items():
        for perm, src in trials:
            cal = np.zeros(n, bool); cal[perm[:n//2]] = True
            cal_t = torch.from_numpy(cal).to(dev)
            srcmask = np.zeros(T, bool); srcmask[src] = True; src_t = torch.from_numpy(srcmask).to(dev)
            ll = {store: label_loss(store, cal) for store in stores}
            l_img, has = image_loss('anchored845', srcmask)
            for alpha in ALPHAS:
                lab = {store: crc(ll[store][0][ll[store][1] & src_t], alpha) for store in stores}
                img = crc(l_img[cal_t & has], alpha)
                arms = {'anchored, label-level': lab['anchored845'], 'anchored, image-level (paper)': img, 'anchored, both': min(lab['anchored845'], img),
                        'native, full known, label-level': lab['native845']}
                for arm, gi in arms.items(): chosen.setdefault((design, alpha, arm), []).append(gi)
        print('thresholds chosen for', design, flush=True)
    need = {}
    for (design, alpha, arm), gs in chosen.items(): need.setdefault(ARMS[arm], set()).update(gs)
    need = {s: sorted(g) for s, g in need.items()}
    print('thresholds per store:', {s: len(g) for s, g in need.items()}, flush=True)

    # pass 2: per-image normalised histogram of the set size over labelled pixels at every needed threshold
    hist = {s: {g: np.zeros((n, T+1), dtype=np.float32) for g in gs} for s, gs in need.items()}
    for store, gs in need.items():
        thr = grid[torch.tensor(gs, device=dev)]
        for i, k in enumerate(keep):
            lab_px = torch.from_numpy(gt[k] >= 0).to(dev)
            s = torch.from_numpy(np.array(part(stores[store], k))).to(dev)[lab_px]
            for j0 in range(0, len(gs), CHUNK):
                sizes = (s[None, :, :] >= thr[j0:j0+CHUNK, None, None]).sum(2)
                for jj in range(sizes.shape[0]):
                    hist[store][gs[j0+jj]][i] = (torch.bincount(sizes[jj], minlength=T+1).double()/len(s)).cpu().numpy()
            if i % 400 == 0: print(f'pass 2 {store} {i+1}/{n}', flush=True)

    result = dict(dataset=a.dataset, tag=a.tag, images=n, trials=TRIALS, alphas=ALPHAS, source=S, total=T, frozen_sets=len(frozen_sets or []), designs={})
    lines = ['# Distribution of the per-pixel set size under the label-level threshold', '',
             f"{n} {d['name']} images, {S} source and {T} grown names; the {TRIALS} trials of {ref_dir} (random half split per trial); distribution over labelled pixels "
             '(source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.', '']
    for design, trials in designs.items():
        for alpha in ALPHAS:
            key = f'a{alpha}, {design}'; result['designs'][key] = {}
            lines += [f'## {key}', '', '| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
            for arm, store in ARMS.items():
                per_trial = []; dist_sum = np.zeros(T+1)
                for (perm, _), g in zip(trials, chosen[(design, alpha, arm)]):
                    ev = perm[n//2:]
                    dist = hist[store][g][ev].mean(0).astype(np.float64)
                    dist_sum += dist; per_trial.append(stats(dist))
                mean_dist = dist_sum/TRIALS
                agg = {k: float(np.mean([s[k] for s in per_trial])) for k in per_trial[0]}
                agg['median_of_mean_dist'] = stats(mean_dist)['median']; agg['p90_of_mean_dist'] = stats(mean_dist)['p90']
                r = ref['designs'].get(key, {}).get(arm)
                ref_mean = r['size'] if r else float('nan')
                if r: assert abs(agg['mean']-ref_mean) < 0.02, (key, arm, agg['mean'], ref_mean)
                agg['reference_mean'] = ref_mean; agg['distribution'] = mean_dist.tolist()
                result['designs'][key][arm] = agg
                lines.append(f"| {arm} | {100*agg['frac_empty']:.1f} | {100*agg['frac_one']:.1f} | {100*agg['frac_le3']:.1f} | {100*agg['frac_le10']:.1f} | {100*agg['frac_gt10']:.1f} | "
                             f"{agg['median_of_mean_dist']} | {agg['p90_of_mean_dist']} | {agg['mean']:.2f} | {ref_mean:.2f} |")
            lines.append('')
    lines += ['Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_set_size_dist_label.py', 'src/exp_label_exchange.py']}
    OUT = Path(f'results/set_size_dist_label_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
