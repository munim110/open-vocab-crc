"""Cost of repeated recalibration under a calibration-conditional guarantee, on the stored headroom-probe scores.

CRC controls the risk in expectation over calibration draws, one vocabulary at a time. A deployer who recalibrates the
native model for K vocabularies and wants all K thresholds valid at once with probability 1 - delta needs each at level
delta/K (union bound). The anchored threshold is calibrated once on source labels whose scores do not depend on the
other candidates, so one event at level delta covers every vocabulary. Thresholds here are RCPS with the
Hoeffding-Bentkus bound (Bates et al., 2021), tested in fixed sequence from the largest sets down. Same images, splits,
grid and loss as exp_headroom_splits.py; the CRC rows must reproduce its results. Development data; nothing is fitted.
Usage: python src/exp_repeated_recal.py -> results/repeated_recal/{results.json,REPORT.md}
"""
import json
from pathlib import Path

import numpy as np
import torch
from scipy.stats import binom

from exp_fixed_source import digest
from exp_headroom_sets import LOGIT_GRID
from exp_headroom_splits import DATASETS, curves

ALPHA, DELTA, SPLITS = .1, .1, 500
KS = [1, 2, 5, 10, 20, 50, 100, 1000, 10**4, 10**6]
# (label, dataset, tag): the configurations whose score stores are still on disk
CONFIGS = [('CAT-Seg ViT-L', 'ade', 'vitl_bank683'), ('SED', 'ade', 'sed_bank683'), ('FC-CLIP', 'ade', 'fcclip_bank683'),
           ('CAT-Seg ViT-L', 'pascal', 'vitl_bank683'), ('SED', 'pascal', 'sed_bank683'), ('SED', 'coco', 'sed_bank683')]
OUT = Path('results/repeated_recal')


def hb_pvalue(rhat, n, alpha):
    """Hoeffding-Bentkus p-value for H0: risk > alpha, losses in [0, 1] (Bates et al., 2021, Sec. 3.1)."""
    a = np.minimum(rhat, alpha)
    with np.errstate(divide='ignore', invalid='ignore'):
        h1 = np.where(a > 0, a*np.log(a/alpha), 0)+(1-a)*np.log((1-a)/(1-alpha))
    return np.minimum(np.exp(-n*h1), np.e*binom.cdf(np.ceil(n*rhat), n, alpha))


def rcps(loss_cal, level):
    """Largest grid index such that every threshold up to it rejects H0 at the level (fixed-sequence test)."""
    ok = hb_pvalue(loss_cal.mean(0), len(loss_cal), ALPHA) <= level
    assert ok[0], 'the largest sets must already pass'
    return np.argmin(ok)-1 if not ok.all() else len(ok)-1


def crc(loss_cal):
    return np.flatnonzero((loss_cal.sum(0)+1)/(len(loss_cal)+1) <= ALPHA)[-1]


@torch.no_grad()
def tabulate(dataset, tag):
    d = DATASETS[dataset]
    runs = [f'results/headroom_probe_ade_{tag}', f'results/headroom_probe_ade_{tag}_rest'] if dataset == 'ade' else [f'results/headroom_probe_{dataset}_{tag}']
    caches = [f'cache/headroom_probe_{tag}', f'cache/headroom_probe_{tag}_rest'] if dataset == 'ade' else [f'cache/headroom_probe_{dataset}_{tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    gt_all = np.load(f"{d['sclip']}/{d['gt']}")[ids]
    S, T = d['source'], d['source']+d['additions'][-1]
    keep = np.flatnonzero((gt_all < S).any(1))
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    out = {}
    for arm, store in [('native_recal', d['stores'][1]), ('anchored', d['stores'][2])]:
        parts = [np.load(f'{c}/{store}.npy', mmap_mode='r') for c in caches]
        flat = [(p, i) for p in parts for i in range(len(p))]
        rows = [curves(torch.from_numpy(np.array(flat[k][0][flat[k][1]])).cuda().double(), torch.from_numpy(gt_all[k].astype(np.int64)).cuda(), grid, S, [T]) for k in keep]
        out[arm] = (np.stack([r[0] for r in rows]), np.stack([r[1][-1] for r in rows]).astype(np.float32))
        print(dataset, tag, arm, out[arm][0].shape, flush=True)
    return out, len(keep)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    result = dict(alpha=ALPHA, delta=DELTA, splits=SPLITS, ks=KS, configs={})
    lines = ['# Repeated recalibration: set size of a simultaneous calibration-conditional guarantee', '',
             f'Half of the images calibrate, half evaluate, {SPLITS} random splits (the splits of exp_headroom_splits.py), alpha = {ALPHA}, delta = {DELTA}. '
             'Native: recalibrated at the grown vocabulary, at level delta/K so that K recalibrations hold at once (union bound). '
             'Anchored: calibrated once at the source labels, level delta for every vocabulary. RCPS with the Hoeffding-Bentkus bound. '
             'Sizes are labels per pixel at the grown vocabulary; risk is the mean evaluation risk; "fail" is the share of splits with evaluation risk above alpha.', '']
    for label, dataset, tag in CONFIGS:
        curves_, n_img = tabulate(dataset, tag)
        rng = np.random.default_rng(20261003)                        # same draws as exp_headroom_splits.py
        [rng.permutation(n_img) for _ in range(SPLITS)]
        perms = [rng.permutation(n_img) for _ in range(SPLITS)]
        n_cal = n_img//2

        def run(arm, pick):
            loss, size = curves_[arm]; risk, sz = [], []
            for perm in perms:
                cal, ev = perm[:n_cal], perm[n_cal:]
                g = pick(loss[cal]); risk.append(loss[ev, g].mean()); sz.append(size[ev, g].mean())
            return dict(mean_size=float(np.mean(sz)), mean_risk=float(np.mean(risk)), frac_splits_above_alpha=float(np.mean(np.array(risk) > ALPHA)))

        r = dict(dataset=dataset, tag=tag, images=n_img, crc={arm: run(arm, crc) for arm in curves_},
                 anchored_rcps=run('anchored', lambda l: rcps(l, DELTA)),
                 native_rcps={str(k): run('native_recal', lambda l, k=k: rcps(l, DELTA/k)) for k in KS})
        ref = json.loads(Path(f'results/headroom_splits_{dataset}_{tag}/results.json').read_text())['designs'][f'cal{n_cal}_a{ALPHA}']
        # sizes accumulate in float32 over one width here and over all widths there: equal up to summation order
        np.testing.assert_allclose(r['crc']['native_recal']['mean_size'], ref['catseg_native_replay_full']['mean_size'][-1], rtol=1e-4)
        np.testing.assert_allclose(r['crc']['anchored']['mean_size'], ref['catseg_anchored']['mean_size'][-1], rtol=1e-4)
        cross = [k for k in KS if r['native_rcps'][str(k)]['mean_size'] >= r['anchored_rcps']['mean_size']]
        r['crossover_k'] = cross[0] if cross else None
        key = f'{dataset}_{tag}'; result['configs'][key] = r
        a = r['anchored_rcps']
        lines += [f'## {label}, {dataset} ({n_img} images)', '',
                  f"CRC (marginal, one vocabulary): native recal. {r['crc']['native_recal']['mean_size']:.2f}, anchored {r['crc']['anchored']['mean_size']:.2f}. "
                  f"Anchored RCPS at delta: size {a['mean_size']:.2f}, risk {100*a['mean_risk']:.2f}%, fail {100*a['frac_splits_above_alpha']:.1f}%. "
                  f"Smallest K with native size >= anchored: {r['crossover_k']}.", '',
                  '| K | native size | risk (%) | fail (%) |', '|---:|---:|---:|---:|']
        lines += [f"| {k:,} | {v['mean_size']:.2f} | {100*v['mean_risk']:.2f} | {100*v['frac_splits_above_alpha']:.1f} |" for k, v in ((k, r['native_rcps'][str(k)]) for k in KS)]
        lines.append('')
        del curves_
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_repeated_recal.py', 'src/exp_headroom_splits.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
