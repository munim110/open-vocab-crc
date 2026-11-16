"""Added-label excess risk against measured added-label hardness (development data, stored scores).

prop:shift: with candidate-independent scores, source labels drawn i.i.d. from P and the added label drawn independently
from Q, the added label's risk at the label-level threshold t_l is E[l_Q(t_l)] = E[l_P(t_l)] + E[Delta(t_l)] <= alpha +
E[Delta(t_l)] <= alpha + max_t Delta(t), with Delta(t) = l_Q(t) - l_P(t); if a fraction eps of Q is arbitrary and the rest
is P, the excess is at most eps. This script measures how the excess grows when Q is tilted toward hard names, with
hardness measured on other images, so a reader can see what a violation of the random-draw assumption costs.

Per trial (500; exp_label_exchange.py's design "exchangeable": the same random half/half image split and the same uniform
random S of the T names as calibration labels, so P = uniform over the names):
  * t_l: label-level CRC over the calibration labels present in the calibration images (as exp_label_exchange.py);
  * hardness of every remaining name present in both halves: its pooled loss on the HELD-OUT images at the label-level
    threshold computed the same way on the held-out images (so Q is fixed by the held-out half and independent of t_l
    given the image split);
  * Q_k = uniform over the k-th fifth of the remaining names by hardness (k = 1 easiest ... 5 hardest), and Q_all =
    uniform over all remaining names;
  * reported on the calibration images (the proposition's quantity, images fixed): the realised added risk l_Q(t_l), the
    P risk l_P(t_l) (mean over all names present, = a further draw from P), Delta(t_l), max_t Delta(t), and the mean
    held-out hardness of Q_k;
  * contamination: Q_eps = (1 - eps) P + eps Q_5; realised risk against the bound alpha + eps.

    PYTHONPATH=src python src/exp_label_hardness.py --dataset ade --tag vitl_bank683
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_label_exchange import gt_all
from exp_label_sample import DATASETS

EPS = [0, .05, .1, .25, .5, 1]
FIFTHS = 5


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--trials', type=int, default=500)
    ap.add_argument('--device', default=None)
    ap.add_argument('--limit', type=int, default=0, help='first N kept images only (smoke test; nothing is written)')
    a = ap.parse_args()
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    dev = a.device or ('cuda' if torch.cuda.is_available() else 'cpu')
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_{a.dataset}_{a.tag}'], [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    store = [np.load(f'{c}/{d["stores"][2]}.npy', mmap_mode='r') for c in caches]    # anchored at the grown vocabulary
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n_all = len(keep)
    if a.limit: keep = keep[:a.limit]
    n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)

    def part(parts, k):
        for q in parts:
            if k < len(q): return q[k]
            k -= len(q)

    # (image, label) pairs present in the image: miss counts [pair, G] (pixels of the label scored below each threshold)
    pair_img, pair_lab, pair_n, miss = [], [], [], []
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab = g >= 0
        labs = torch.unique(g[lab])
        s = torch.from_numpy(np.array(part(store, k))).to(dev)[lab].float()
        true = s.gather(1, g[lab][:, None])[:, 0].double()
        miss.append(torch.stack([torch.searchsorted(true[g[lab] == c].sort().values, grid, right=False) for c in labs]).to(torch.int16).cpu())
        pair_img.append(np.full(len(labs), i)); pair_lab.append(labs.cpu().numpy()); pair_n.append(torch.stack([(g == c).sum() for c in labs]).cpu().numpy())
        if i % 250 == 0: print(f'{i+1}/{n}', flush=True)
    pimg, plab, pn = (torch.from_numpy(np.concatenate(x)).to(dev) for x in (pair_img, pair_lab, pair_n))
    pn = pn.float(); miss = torch.cat(miss).float().to(dev)

    def label_loss(imgmask):
        sel = imgmask[pimg]
        num = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], miss[sel])
        den = torch.zeros(T, device=dev).index_add_(0, plab[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def crc(losses, alpha):
        ok = torch.nonzero((losses.sum(0)+1)/(len(losses)+1) <= alpha)
        return int(ok[-1]) if len(ok) else 0

    rng = np.random.default_rng(20260926)                                 # exp_label_exchange.py's draws, in its order
    perms = [rng.permutation(n_all) for _ in range(a.trials)]
    random_sets = [np.sort(rng.choice(T, S, replace=False)) for _ in range(a.trials)]
    if a.limit: perms = [p_[p_ < n] for p_ in perms]
    acc = {}
    for tr, perm in enumerate(perms):
        cal = torch.zeros(n, dtype=torch.bool, device=dev); cal[torch.from_numpy(perm[:len(perm)//2]).to(dev)] = True; ev = ~cal
        lc, pc = label_loss(cal); le, pe = label_loss(ev)
        drawn = torch.zeros(T, dtype=torch.bool, device=dev); drawn[torch.from_numpy(random_sets[tr]).to(dev)] = True
        rest = pc & pe & ~drawn
        names = torch.nonzero(rest)[:, 0]
        for alpha in ALPHAS:
            t = crc(lc[pc & drawn], alpha)
            t_ref = crc(le[pe & drawn], alpha)                           # the same rule on the held-out half
            hard = le[names, t_ref]
            order = names[hard.argsort()]
            groups = dict(zip([f'Q{k+1}' for k in range(FIFTHS)], torch.tensor_split(order, FIFTHS)))
            groups['Q_all'] = order
            lp_curve = lc[pc].mean(0)                                    # P = uniform over the names (all present in cal)
            lp = lp_curve[t].item()
            for key, grp in groups.items():
                q_curve = lc[grp].mean(0)
                acc.setdefault((alpha, key), []).append((q_curve[t].item(), lp, (q_curve-lp_curve)[t].item(), (q_curve-lp_curve).max().item(),
                                                         le[grp, t_ref].mean().item(), len(grp)))
            h_curve = lc[groups[f'Q{FIFTHS}']].mean(0)
            for eps in EPS:
                acc.setdefault((alpha, f'eps={eps}'), []).append((((1-eps)*lp_curve+eps*h_curve)[t].item(), lp))
        if tr % 50 == 0: print(f'trial {tr}', flush=True)

    result = dict(dataset=a.dataset, tag=a.tag, images=n, trials=len(perms), fifths={}, contamination={})
    lines = ['# Added-label excess risk against measured hardness (prop:shift)', '',
             f'{a.tag}, {n} {d["name"]} images, {T} names, {len(perms)} trials (design "exchangeable" of exp_label_exchange.py: '
             f'{S} uniformly drawn names are the calibration labels). Q_k = uniform over the k-th fifth of the remaining names '
             'by hardness (pooled loss on the held-out images at the label-level threshold of the held-out images; Q1 easiest). '
             'All risks on the calibration images at the label-level threshold t_l (the proposition\'s quantity), in %, mean over '
             'trials: realised = l_Q(t_l); P = l_P(t_l), a further uniform draw; bound = alpha + Delta(t_l) and alpha + max_t Delta(t). '
             'Development data; nothing fitted.' if not a.limit else f'smoke test, {n} images', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', '| Added names | Names | Held-out hardness | Realised | P | alpha + Delta(t_l) | alpha + max Delta | Trials above alpha |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|']
        for key in [f'Q{k+1}' for k in range(FIFTHS)]+['Q_all']:
            v = np.array(acc[(alpha, key)]); mu = v.mean(0); above = (v[:, 0] > alpha).mean()
            result['fifths'][f'a{alpha}, {key}'] = dict(realised=mu[0], p_risk=mu[1], delta_at_t=mu[2], max_delta=mu[3], hardness=mu[4],
                                                        names=mu[5], frac_trials_above_alpha=float(above))
            lines.append(f'| {key} | {mu[5]:.0f} | {100*mu[4]:.1f} | {100*mu[0]:.2f} | {100*mu[1]:.2f} | {100*(alpha+mu[2]):.2f} | '
                         f'{100*(alpha+mu[3]):.2f} | {100*above:.0f}% |')
        lines += ['', f'Contamination, Q = (1 - eps) P + eps Q{FIFTHS}:', '', '| eps | Realised | Bound alpha + eps | Excess over alpha |', '|---:|---:|---:|---:|']
        for eps in EPS:
            v = np.array(acc[(alpha, f'eps={eps}')]); mu = v.mean(0)
            result['contamination'][f'a{alpha}, eps={eps}'] = dict(realised=mu[0], p_risk=mu[1], bound=alpha+eps)
            lines.append(f'| {eps} | {100*mu[0]:.2f} | {100*(alpha+eps):.0f} | {100*(mu[0]-alpha):+.2f} |')
        lines.append('')
    result = json.loads(json.dumps(result, default=float))
    print('\n'.join(lines))
    if a.limit: return
    result['hashes'] = {q: digest(Path(q)) for q in ['src/exp_label_hardness.py', 'src/exp_label_exchange.py', f"{d['sclip']}/{d['gt_fine']}"]}
    OUT = Path(f'results/label_hardness_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')


if __name__ == '__main__':
    main()
