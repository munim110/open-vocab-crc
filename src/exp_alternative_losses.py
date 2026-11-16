"""Other image losses under the same thresholds: does the vocabulary-growth story depend on the loss?

The headline loss is the per-image fraction of source-labelled sampled pixels whose label is missing from the set
(a per-image false-negative rate, controlled in expectation). For finer
or stricter guarantees, the same stored scores, stores, exclusion and 500 half/half splits are run with:
  * fnr: the headline loss (reference);
  * fnr_gt_0.25 / fnr_gt_0.10: binary loss 1[fnr > tau], so CRC at alpha means "at most alpha of the images lose more
    than tau of their source pixels" (a high-probability, per-image statement rather than a mean);
  * class_balanced: mean over the source classes present in the image of the per-class miss fraction, so a small
    object counts as much as the wall behind it;
  * worst_class: the largest per-class miss fraction among the classes present in the image.
All four are monotone in the threshold and bounded in [0, 1]. Arms as in exp_conditional_risk.py; set size at the
grown vocabulary from the evaluation store. Nothing is fitted.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_splits import curves
from headroom_scores import ALPHAS, LOGIT_GRID, Probe, crc_pick

TAUS = [.25, .10]
ARMS = dict(native_source=('native_source', 'native_source'), native_frozen=('native_source', 'native_full'),
            native_replay=('native_full', 'native_full'), anchored_frozen=('anchored_full', 'anchored_full'))


def class_curves(true, cls, S, grid):
    """Per-class miss fraction at every grid threshold for the classes present: [C_present, G]."""
    out = []
    for c in torch.unique(cls):
        t = true[cls == c].sort().values
        out.append(torch.searchsorted(t, grid, right=False).double()/len(t))
    return torch.stack(out)


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade')
    ap.add_argument('--tag', default='')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    P = Probe(a.dataset, a.tag)
    OUT = Path(f'results/alternative_losses_{a.dataset}{P.suffix}'); OUT.mkdir(parents=True, exist_ok=True)
    S, T = P.S, P.T; grid = torch.from_numpy(LOGIT_GRID).to(P.dev)
    gt = torch.from_numpy(P.gt.astype(np.int64)).to(P.dev)
    LOSSES = ['fnr']+[f'fnr_gt_{t:.2f}' for t in TAUS]+['class_balanced', 'worst_class']
    L = {}; size = {}
    for store in ('native_source', 'native_full', 'anchored_full'):
        rows = {k: [] for k in LOSSES}; sz = []
        for j in range(P.n_img):
            s = P.scores(store, j); g = gt[j]; v = g < S
            widths = [S] if store == 'native_source' else [S, T]
            fnr, sizes = curves(s, g, grid, S, widths)
            rows['fnr'].append(fnr)
            for t in TAUS: rows[f'fnr_gt_{t:.2f}'].append((fnr > t).astype(np.float64))
            true = s[v].gather(1, g[v][:, None])[:, 0]
            cc = class_curves(true, g[v], S, grid)
            rows['class_balanced'].append(cc.mean(0).cpu().numpy()); rows['worst_class'].append(cc.max(0).values.cpu().numpy())
            sz.append(sizes[-1])
        L[store] = {k: np.stack(v) for k, v in rows.items()}; size[store] = np.stack(sz).astype(np.float32)
        print(store, 'loaded', flush=True)
    perms = P.splits(a.splits); n_cal = P.n_cal
    result = dict(config=P.config, dataset=a.dataset, images=P.n_img, excluded_images=P.dropped, splits=a.splits, alphas=ALPHAS, losses=LOSSES, taus=TAUS, designs={})
    lines = [f'# Alternative image losses under source-calibrated thresholds: {P.config}', '', P.describe(a.splits),
             'Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.', '']
    for alpha in ALPHAS:
        key = f'a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha}', '', '| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |', '|---|---|---:|---:|---:|---:|']
        for loss in LOSSES:
            result['designs'][key][loss] = {}
            for arm, (cal_store, ev_store) in ARMS.items():
                risk, sz = [], []
                for perm in perms:
                    cal, ev = perm[:n_cal], perm[n_cal:]
                    g = crc_pick(L[cal_store][loss], cal, alpha)
                    risk.append(L[ev_store][loss][ev, g].mean()); sz.append(size[ev_store][ev, g].mean())
                risk, sz = np.array(risk), np.array(sz)
                result['designs'][key][loss][arm] = dict(mean_risk=float(risk.mean()), risk_sd=float(risk.std(ddof=1)), frac_splits_above_alpha=float((risk > alpha).mean()),
                                                         mean_size=float(sz.mean()), size_q025_q975=np.quantile(sz, [.025, .975]).tolist())
                lines.append(f'| {loss} | {arm} | {100*risk.mean():.2f} | {100*risk.std(ddof=1):.2f} | {100*(risk > alpha).mean():.1f} | {sz.mean():.2f} |')
        lines.append('')
    lines += ['CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_alternative_losses.py', 'src/headroom_scores.py', 'src/exp_headroom_splits.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
