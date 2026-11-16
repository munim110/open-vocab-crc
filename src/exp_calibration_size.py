"""Calibration-set size: how many calibration images does the source-vocabulary threshold need, and does the answer
differ between native recalibration on the grown vocabulary and the anchored frozen threshold?

Same stored scores, exclusion rule and 500 permutations (seed 20261003) as the other stored-score experiments. In every
permutation the evaluation images are the second half (fixed size); the calibration set is the first n images of the
first half for n in N_CAL, so the calibration sets are nested. Arms as in exp_alternative_losses.py (native_frozen,
native_replay, anchored_frozen) under the headline loss. Reports the mean risk, its spread over splits (sd and 90th
percentile), the fraction of splits above alpha, and the set size at the grown vocabulary (mean, sd, 2.5-97.5% range).
CRC needs n >= (1 - alpha)/alpha calibration images for a non-trivial threshold; below that the first grid index is
selected and every label is included. Nothing is fitted.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_splits import curves
from headroom_scores import ALPHAS, LOGIT_GRID, Probe, crc_pick

N_CAL = [10, 20, 50, 100, 200, 400]
ARMS = dict(native_frozen=('native_source', 'native_full'), native_replay=('native_full', 'native_full'), anchored_frozen=('anchored_full', 'anchored_full'))


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade')
    ap.add_argument('--tag', default='')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    P = Probe(a.dataset, a.tag)
    OUT = Path(f'results/calibration_size_{a.dataset}{P.suffix}'); OUT.mkdir(parents=True, exist_ok=True)
    S, T = P.S, P.T; grid = torch.from_numpy(LOGIT_GRID).to(P.dev)
    gt = torch.from_numpy(P.gt.astype(np.int64)).to(P.dev)
    n_half = P.n_cal; sizes_n = [n for n in N_CAL if n < n_half]+[n_half]
    L = {}; size = {}
    for store in ('native_source', 'native_full', 'anchored_full'):
        fnr_rows, sz_rows = [], []
        for j in range(P.n_img):
            fnr, sizes = curves(P.scores(store, j), gt[j], grid, S, [S] if store == 'native_source' else [S, T])
            fnr_rows.append(fnr); sz_rows.append(sizes[-1])
        L[store] = np.stack(fnr_rows); size[store] = np.stack(sz_rows).astype(np.float32)
        print(store, 'loaded', flush=True)
    perms = P.splits(a.splits)
    result = dict(config=P.config, dataset=a.dataset, images=P.n_img, excluded_images=P.dropped, splits=a.splits, alphas=ALPHAS, n_cal=sizes_n,
                  n_eval=P.n_img-n_half, min_feasible_n={f'a{al}': math.ceil((1-al)/al) for al in ALPHAS}, designs={})
    lines = [f'# Calibration-set size under source-calibrated thresholds: {P.config}', '', P.describe(a.splits),
             f'Evaluation images: the second half of every permutation ({P.n_img-n_half} images). Calibration: the first n images of the first half (nested). '
             'Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.', '']
    for alpha in ALPHAS:
        key = f'a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha} (needs n >= {math.ceil((1-alpha)/alpha)})', '', '| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |', '|---:|---|---:|---:|---:|---:|---:|---:|']
        for n in sizes_n:
            result['designs'][key][str(n)] = {}
            for arm, (cal_store, ev_store) in ARMS.items():
                risk, sz = [], []
                for perm in perms:
                    cal, ev = perm[:n], perm[n_half:]
                    g = crc_pick(L[cal_store], cal, alpha)
                    risk.append(L[ev_store][ev, g].mean()); sz.append(size[ev_store][ev, g].mean())
                risk, sz = np.array(risk), np.array(sz)
                result['designs'][key][str(n)][arm] = dict(mean_risk=float(risk.mean()), risk_sd=float(risk.std(ddof=1)), risk_q90=float(np.quantile(risk, .9)),
                                                           frac_splits_above_alpha=float((risk > alpha).mean()), mean_size=float(sz.mean()), size_sd=float(sz.std(ddof=1)),
                                                           size_q025_q975=np.quantile(sz, [.025, .975]).tolist())
                lines.append(f'| {n} | {arm} | {100*risk.mean():.2f} | {100*risk.std(ddof=1):.2f} | {100*np.quantile(risk, .9):.2f} | {100*(risk > alpha).mean():.1f} | {sz.mean():.2f} | {sz.std(ddof=1):.2f} |')
        lines.append('')
    lines += ['CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_calibration_size.py', 'src/headroom_scores.py', 'src/exp_headroom_splits.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
