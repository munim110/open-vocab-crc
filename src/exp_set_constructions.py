"""Standard conformal set constructions on the same stored scores, before and after vocabulary growth.

Every headline result builds the set as {label : score >= t} on the raw per-label logit (LAC/THR on the logit).
This script runs the other standard constructions on the same scores for a direct comparison:
  * logit      C = {j : z_j >= t}                                    (headline; projective for anchored scores)
  * softmax    C = {j : softmax(z)_j >= t}, temperature 1            (probability cutoff)
  * aps        C = smallest prefix of the descending-softmax ranking whose mass reaches t (crossing label included,
                 membership "mass strictly preceding j < t", no randomisation; conventions of conformal.py)
  * raps       APS with the penalty lambda * max(0, rank - k_reg) added to the preceding mass (lambda 0.01, k_reg 5)
The softmax, APS and RAPS scores normalise over the deployed vocabulary, so they are candidate-dependent for the
anchored scores too; the frozen anchored arm under those constructions shows what breaks when the set construction
itself is not projective. Uncalibrated references: top-1, top-5 and softmax >= 0.5.
Arms: native_source (calibrate and evaluate at the source vocabulary), native_frozen (source threshold reused after
growth), native_replay (recalibrated after growth), anchored_frozen (anchored scores, source threshold reused),
anchored_replay (anchored scores recalibrated after growth). Same exclusion and 500 half/half splits as the other
scripts; loss = image-level fraction of source-labelled sampled pixels whose label is missing. Nothing is fitted.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from headroom_scores import ALPHAS, LOGIT_GRID, Probe, crc_pick

LAMBDA, K_REG = .01, 5
CONSTRUCTIONS = ['logit', 'softmax', 'aps', 'raps']
INCREASING = dict(logit=True, softmax=True, aps=False, raps=False)      # loss grows with the grid index?
TOPK = [1, 5]
# arm -> ((calibration store, width key), (evaluation store, width key)); width key 'S' = first S columns, 'T' = all
ARMS = dict(native_source=(('native_source', 'S'), ('native_source', 'S')), native_frozen=(('native_source', 'S'), ('native_full', 'T')),
            native_replay=(('native_full', 'T'), ('native_full', 'T')), anchored_frozen=(('anchored_full', 'S'), ('anchored_full', 'T')),
            anchored_replay=(('anchored_full', 'T'), ('anchored_full', 'T')))


def grids(T):
    mass = torch.linspace(0, 1, 1025, dtype=torch.float64)
    raps = torch.arange(0, 1+LAMBDA*(T-K_REG)+1e-9, 1/1024, dtype=torch.float64)
    return dict(logit=torch.from_numpy(LOGIT_GRID), softmax=mass, aps=mass, raps=raps)


@torch.no_grad()
def per_image(z, y, G):
    """z [n, W] double scores of the labelled pixels, y [n] true labels. Returns loss curves {c: [G_c]}, size curves {c: [G_c]},
    and the top-k / fixed-cutoff references."""
    n, W = z.shape
    p = z.softmax(-1)
    order = p.argsort(dim=-1, descending=True, stable=True)
    ps = p.gather(1, order)
    excl = ps.cumsum(-1)-ps                                              # mass strictly preceding each ranked label
    rank = torch.empty_like(order); rank.scatter_(1, order, torch.arange(W, device=z.device).expand(n, W))   # 0-based rank of each label
    pen = LAMBDA*(torch.arange(1, W+1, device=z.device, dtype=torch.float64)-K_REG).clamp(min=0)
    values = dict(logit=z, softmax=p, aps=excl.gather(1, rank), raps=(excl+pen).gather(1, rank))          # per-label membership value, label order
    iy = y[:, None]
    loss, size = {}, {}
    for c in CONSTRUCTIONS:
        v = values[c]; g = G[c]; u = v.gather(1, iy)[:, 0].sort().values
        below = torch.searchsorted(u, g, right=False).double()           # #{u < t}
        if INCREASING[c]:
            loss[c] = (below/n).cpu().numpy()
            idx = torch.searchsorted(g, v.reshape(-1), right=True)      # #{grid <= v}; member iff idx >= g+1
            cnt = torch.bincount(idx, minlength=len(g)+1).double().cumsum(0)[:-1]
            size[c] = ((W*n-cnt)/n).cpu().numpy()
        else:
            loss[c] = ((n-below)/n).cpu().numpy()                       # member iff u < t
            idx = torch.searchsorted(g, v.reshape(-1), right=True)      # member iff idx <= g
            cnt = torch.bincount(idx, minlength=len(g)+1).double().cumsum(0)[:-1]
            size[c] = (cnt/n).cpu().numpy()
    ry = rank.gather(1, iy)[:, 0]
    ref = {f'top{k}': float((ry >= k).double().mean()) for k in TOPK}
    py = p.gather(1, iy)[:, 0]
    ref['softmax_ge_0.5'] = float((py < .5).double().mean()); ref['softmax_ge_0.5_size'] = float((p >= .5).sum(1).double().mean())
    return loss, size, ref


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade')
    ap.add_argument('--tag', default='')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    P = Probe(a.dataset, a.tag)
    OUT = Path(f'results/set_constructions_{a.dataset}{P.suffix}'); OUT.mkdir(parents=True, exist_ok=True)
    S, T = P.S, P.T
    G = {c: g.to(P.dev) for c, g in grids(T).items()}
    gt = torch.from_numpy(P.gt.astype(np.int64)).to(P.dev)
    combos = [('native_source', 'S'), ('native_full', 'T'), ('anchored_full', 'S'), ('anchored_full', 'T')]
    L, Z, R = {}, {}, {}
    for store, wk in combos:
        rows = {c: [] for c in CONSTRUCTIONS}; sizes = {c: [] for c in CONSTRUCTIONS}; refs = []
        for j in range(P.n_img):
            s = P.scores(store, j); y = gt[j]; v = y < S
            z = s[v][:, :S] if wk == 'S' else s[v]
            loss, size, ref = per_image(z, y[v], G)
            for c in CONSTRUCTIONS: rows[c].append(loss[c]); sizes[c].append(size[c])
            refs.append(ref)
        L[store, wk] = {c: np.stack(v) for c, v in rows.items()}; Z[store, wk] = {c: np.stack(v).astype(np.float32) for c, v in sizes.items()}
        R[store, wk] = {k: np.array([r[k] for r in refs]) for k in refs[0]}
        print(store, wk, 'loaded', flush=True)
    perms = P.splits(a.splits); n_cal = P.n_cal
    result = dict(config=P.config, dataset=a.dataset, images=P.n_img, excluded_images=P.dropped, splits=a.splits, alphas=ALPHAS,
                  constructions=CONSTRUCTIONS, raps=dict(lam=LAMBDA, k_reg=K_REG), designs={}, uncalibrated={})
    lines = [f'# Set constructions on the same scores: {P.config}', '', P.describe(a.splits),
             'Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.', '']
    for alpha in ALPHAS:
        key = f'a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha}', '', '| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |', '|---|---|---:|---:|---:|---:|']
        for c in CONSTRUCTIONS:
            result['designs'][key][c] = {}
            for arm, (cal, ev) in ARMS.items():
                risk, sz = [], []
                for perm in perms:
                    g = crc_pick(L[cal][c], perm[:n_cal], alpha, INCREASING[c])
                    risk.append(L[ev][c][perm[n_cal:], g].mean()); sz.append(Z[ev][c][perm[n_cal:], g].mean())
                risk, sz = np.array(risk), np.array(sz)
                result['designs'][key][c][arm] = dict(mean_risk=float(risk.mean()), risk_sd=float(risk.std(ddof=1)), frac_splits_above_alpha=float((risk > alpha).mean()),
                                                      mean_size=float(sz.mean()), size_q025_q975=np.quantile(sz, [.025, .975]).tolist())
                lines.append(f'| {c} | {arm} | {100*risk.mean():.2f} | {100*risk.std(ddof=1):.2f} | {100*(risk > alpha).mean():.1f} | {sz.mean():.2f} |')
        lines.append('')
    lines += ['## Uncalibrated references (all kept images)', '', '| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |', '|---|---|---:|---:|---:|---:|']
    for (store, wk), r in R.items():
        row = {k: float(v.mean()) for k, v in r.items()}; result['uncalibrated'][f'{store}_{wk}'] = row
        lines.append(f'| {store} | {S if wk == "S" else T} | {100*row["top1"]:.2f} | {100*row["top5"]:.2f} | {100*row["softmax_ge_0.5"]:.2f} | {row["softmax_ge_0.5_size"]:.2f} |')
    lines += ['', f'Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda {LAMBDA}, k_reg {K_REG}, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_set_constructions.py', 'src/headroom_scores.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
