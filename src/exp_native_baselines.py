"""Native baselines on the stored headroom-probe scores (development data).

Two native references are reported next to the anchored threshold calibrated once at the source vocabulary V0:
  * the native model's own set size at V0 (calibrated and deployed at V0), beside anchored at V0;
  * native reuse with a tightened alpha: calibrate native at V0 with alpha' < alpha and deploy it at the grown
    vocabulary. The alpha' that brings the grown-vocabulary risk to alpha is read off the EVALUATION images at the
    grown vocabulary (an oracle: it needs labelled data at the vocabulary that is deployed), so it is a reference for
    the set size such a correction would cost, not a deployable method. SED's reused threshold is over-conservative,
    so its alpha' is above alpha.
It also reports how often the native arg-max at the grown vocabulary falls outside the anchored set: per labelled source pixel of
the evaluation images, is the native top-1 label (over all grown names) a member of the anchored set at the anchored
threshold? Reported pooled over pixels, and among the pixels where the native top-1 is correct.

Same images, exclusion and 500 random half/half splits as exp_added_label_risk.py (headroom_scores.Probe), same grid
and image-level CRC rule as exp_headroom_splits.py. Nothing is fitted; the confirmation reserve is not read.

    PYTHONPATH=src python src/exp_native_baselines.py --dataset ade --tag vitl_bank683
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_splits import curves
from headroom_scores import ALPHAS, LOGIT_GRID, Probe

ALPHA_PRIME = np.round(np.arange(.0025, .2+1e-9, .0025), 4)          # tightened (or loosened) alpha' grid


def pick(bound_sum, n_cal, alpha):
    """Image-level CRC: last grid index with (sum of calibration losses + 1)/(n + 1) <= alpha (0 if none)."""
    ok = np.flatnonzero((bound_sum+1)/(n_cal+1) <= alpha)
    return int(ok[-1]) if len(ok) else 0


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=['ade', 'pascal', 'coco'])
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--splits', type=int, default=500)
    ap.add_argument('--device', default=None)
    ap.add_argument('--limit', type=int, default=0, help='first N kept images only (smoke test; nothing is written)')
    a = ap.parse_args()
    p = Probe(a.dataset, a.tag, device=a.device)
    S, T, dev = p.S, p.T, p.dev
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)
    n = a.limit or p.n_img
    loss = {k: np.zeros((n, G)) for k in ['nsrc', 'nfull', 'anch']}
    size = {k: np.zeros((n, G), np.float32) for k in ['nsrc_at_src', 'nfull_at_full', 'anch_at_src', 'anch_at_full']}
    out_all = np.zeros((n, G)); out_cor = np.zeros((n, G)); n_pix = np.zeros(n); n_cor = np.zeros(n)

    def below(v):
        """[G]: number of entries of v strictly below each grid threshold (not a member at that threshold)."""
        return torch.searchsorted(v.sort().values, grid, right=False).double().cpu().numpy()

    for j in range(n):
        gt = torch.from_numpy(p.gt[j].astype(np.int64)).to(dev)
        ns, nf, an = (p.scores(k, j) for k in ['native_source', 'native_full', 'anchored_full'])
        l, s = curves(ns, gt, grid, S, [S]); loss['nsrc'][j] = l; size['nsrc_at_src'][j] = s[0]
        l, s = curves(nf, gt, grid, S, [T]); loss['nfull'][j] = l; size['nfull_at_full'][j] = s[0]
        l, s = curves(an, gt, grid, S, [S, T]); loss['anch'][j] = l; size['anch_at_src'][j], size['anch_at_full'][j] = s
        valid = gt < S
        top = nf[valid].argmax(1)                                       # native top-1 over all grown names
        a_top = an[valid].gather(1, top[:, None])[:, 0]                 # its anchored score
        correct = top == gt[valid]
        out_all[j] = below(a_top); out_cor[j] = below(a_top[correct])
        n_pix[j] = valid.sum().item(); n_cor[j] = correct.sum().item()
        if j % 250 == 0: print(f'{j+1}/{n}', flush=True)

    perms = [perm[perm < n] for perm in p.splits(a.splits)] if a.limit else p.splits(a.splits)
    n_cal = n//2
    acc = {}
    for perm in perms:
        cal, ev = perm[:n_cal], perm[n_cal:]
        sums = {k: v[cal].sum(0) for k, v in loss.items()}
        for alpha in ALPHAS:
            ta, ts, tf = pick(sums['anch'], n_cal, alpha), pick(sums['nsrc'], n_cal, alpha), pick(sums['nfull'], n_cal, alpha)
            rows = {'anchored, calibrated at V0': (loss['anch'][ev, ta].mean(), size['anch_at_src'][ev, ta].mean(), size['anch_at_full'][ev, ta].mean()),
                    'native at V0 (calibrated and deployed at V0)': (loss['nsrc'][ev, ts].mean(), size['nsrc_at_src'][ev, ts].mean(), np.nan),
                    'native reused (V0 threshold at the grown vocabulary)': (loss['nfull'][ev, ts].mean(), np.nan, size['nfull_at_full'][ev, ts].mean()),
                    'native recalibrated at the grown vocabulary': (loss['nfull'][ev, tf].mean(), np.nan, size['nfull_at_full'][ev, tf].mean())}
            for k, v in rows.items(): acc.setdefault((alpha, k), []).append(v)
            # native top-1 outside the anchored set at the anchored threshold, pooled over evaluation pixels
            acc.setdefault((alpha, 'n5'), []).append((out_all[ev, ta].sum()/n_pix[ev].sum(), out_cor[ev, ta].sum()/max(n_cor[ev].sum(), 1),
                                                      n_cor[ev].sum()/n_pix[ev].sum()))
        # native reuse at every alpha' (risk and size at the grown vocabulary)
        tp = [pick(sums['nsrc'], n_cal, ap_) for ap_ in ALPHA_PRIME]
        acc.setdefault('w7', []).append([(loss['nfull'][ev, t].mean(), size['nfull_at_full'][ev, t].mean()) for t in tp])

    result = dict(dataset=a.dataset, tag=a.tag, images=n, splits=len(perms), alphas=ALPHAS, arms={}, n5={}, tightened={})
    lines = ['# Native baselines: set size at V0, tightened alpha, native arg-max outside the anchored set', '',
             p.describe(len(perms)) if not a.limit else f'smoke test, {n} images', '',
             'Risk = image-level miss risk on source-labelled pixels (%, mean over splits; % of splits above alpha in brackets). '
             f'Size = labels per source-labelled pixel at V0 ({S} names) and at the grown vocabulary ({T} names), evaluation images.', '']
    w7 = np.array(acc.pop('w7'))                                        # [splits, alpha', 2]
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', f'| Arm | Risk | Size at V0 | Size at {T} |', '|---|---:|---:|---:|']
        for (al, k), v in acc.items():
            if al != alpha or k == 'n5': continue
            v = np.array(v); above = (v[:, 0] > alpha).mean()
            sz = [None if np.isnan(v[0, c]) else float(v[:, c].mean()) for c in (1, 2)]
            result['arms'][f'a{alpha}, {k}'] = dict(risk=float(v[:, 0].mean()), frac_splits_above_alpha=float(above), size_v0=sz[0], size_full=sz[1])
            cell = lambda x: '--' if x is None else f'{x:.2f}'
            lines.append(f'| {k} | {100*v[:, 0].mean():.2f} ({100*above:.0f}) | {cell(sz[0])} | {cell(sz[1])} |')
        # oracle alpha': the largest alpha' whose reused threshold has mean grown-vocabulary risk <= alpha
        risk_ap = w7[:, :, 0].mean(0); ok = np.flatnonzero(risk_ap <= alpha)
        if len(ok):
            i = ok[-1]; r = w7[:, i, 0]
            result['tightened'][f'a{alpha}'] = dict(alpha_prime=float(ALPHA_PRIME[i]), risk=float(r.mean()), frac_splits_above_alpha=float((r > alpha).mean()),
                                                     size_full=float(w7[:, i, 1].mean()))
            lines.append(f"| native reused with alpha' = {ALPHA_PRIME[i]:.4f} (oracle: chosen on the evaluation images at {T} names) | "
                         f'{100*r.mean():.2f} ({100*(r > alpha).mean():.0f}) | -- | {w7[:, i, 1].mean():.2f} |')
        v = np.array(acc[(alpha, 'n5')]); mu = v.mean(0)
        result['n5'][f'a{alpha}'] = dict(outside_all=float(mu[0]), outside_when_native_correct=float(mu[1]), native_top1_accuracy=float(mu[2]))
        lines += ['', f'The native top-1 label at {T} names is outside the anchored set on {100*mu[0]:.2f}% of the evaluation '
                  f'source-labelled pixels, and on {100*mu[1]:.2f}% of those where it is correct (native top-1 accuracy {100*mu[2]:.1f}%).', '']
    result['tightened_curve'] = dict(alpha_prime=ALPHA_PRIME.tolist(), risk=w7[:, :, 0].mean(0).tolist(), size_full=w7[:, :, 1].mean(0).tolist())
    lines += ["The alpha' row is a reference for the set size a tightened reuse would cost: choosing alpha' used the labels of the "
              'evaluation images at the grown vocabulary, which a deployment that reuses its V0 calibration does not have.']
    print('\n'.join(lines))
    if a.limit: return
    result['hashes'] = {q: digest(Path(q)) for q in ['src/exp_native_baselines.py', 'src/exp_headroom_splits.py', 'src/headroom_scores.py']}
    OUT = Path(f'results/native_baselines_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')


if __name__ == '__main__':
    main()
