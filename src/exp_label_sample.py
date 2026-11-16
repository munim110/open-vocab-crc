"""The added-label guarantee when the source classes are the benchmark's own: annotate m random names (development data,
stored scores).

prop:labels needs the calibration labels to be exchangeable with the added label. A deployment inherits its source
classes (the frequent ones), so label-level CRC over them leaves the added labels above the target (exp_label_exchange.py,
design "dataset split"). The practical alternative: draw m names uniformly from the names that may be added, annotate the
calibration images for them, and run label-level CRC over the drawn names present in the calibration images only,
    t_m = largest grid t with (sum_{c drawn, present} l_c(t) + 1)/(m' + 1) <= alpha,   m' = # drawn names present.
Conditional on m', the present drawn names are a uniform m'-subset of the added names present in the calibration images, so
a remaining present added label is exchangeable with them and E[l_c(t_m)] <= alpha (images fixed). The source classes keep
the image-level threshold t_img calibrated on their pixels: with candidate-independent scores a pixel's loss depends only
on its true label's threshold, so the per-label deployment (source names at t_img, added names at t_m) keeps the paper's
image-level source guarantee exactly and adds this one.

Per trial (500; fresh random half/half image split; the drawn names are nested prefixes of one random order of the added
names, so larger m adds names to smaller m): the mean loss over the remaining added labels present in the calibration
images ("added, cal", the proposition's quantity) and in the held-out images, the % of trials above alpha, m', the share of
trials at the grid floor, the image-level source risk and the set size at the grown vocabulary (labels per labelled pixel,
held-out images) of the per-label deployment. Reference arms, same trials: the benchmark's own source classes as the
calibration labels (m = S, not random), and the native model at the grown vocabulary with the same drawn names (needs the
grown vocabulary at calibration time).

Check: the arms "random S of T" and "dataset split" replay exp_label_exchange.py's designs "exchangeable" and "dataset split"
(same seed and draws, same loss and size computations; anchored, label-level) and must reproduce its results.json.

    PYTHONPATH=src python src/exp_label_sample.py --dataset ade --tag sed_bank683 [--ms 10,20,50,100,200]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

import exp_added_label_risk
from coco_frozen_analyses import coco_entry
from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_label_exchange import gt_all

DATASETS = dict(exp_added_label_risk.DATASETS, coco=coco_entry())


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--trials', type=int, default=500)
    ap.add_argument('--ms', default='10,20,50,100,200', help='numbers of randomly drawn added names to annotate')
    a = ap.parse_args()
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    ms = [int(m) for m in a.ms.split(',')]
    assert max(ms) < T-S
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_{a.dataset}_{a.tag}'], [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    names = ['anchored', 'native']
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(names, d['stores'][2:0:-1])}
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)
    is_src = torch.arange(T, device=dev) < S

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    def counts(true, lab, labs):                                           # as exp_label_exchange.py
        true = true.double(); return torch.stack([torch.searchsorted(true[lab == c].sort().values, grid, right=False) for c in labs]).to(torch.int16).cpu()

    # (image, label) pairs: miss counts [pair, G]; per image, # (labelled pixel, name) with score >= t summed over the source
    # names and over the added names [n, G] (set size for any thresholds that are shared within each of the two groups)
    pair_img, pair_lab, pair_n = [], [], []
    miss = {k: [] for k in names}
    above = {(k, grp): torch.zeros(n, G, dtype=torch.float64, device=dev) for k in names for grp in ['src', 'add']}
    nlab = torch.zeros(n, device=dev)
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0
        labs = torch.unique(g[lab_px]); nlab[i] = lab_px.sum()
        pair_img.append(np.full(len(labs), i)); pair_lab.append(labs.cpu().numpy())
        pair_n.append(torch.stack([(g == c).sum() for c in labs]).cpu().numpy())
        for name in names:
            s = torch.from_numpy(np.array(part(stores[name], k))).to(dev)[lab_px].float()
            miss[name].append(counts(s.gather(1, g[lab_px][:, None])[:, 0], g[lab_px], labs))
            for grp, cols in [('src', slice(0, S)), ('add', slice(S, T))]:
                idx = torch.searchsorted(grid, s[:, cols].double().reshape(-1), right=True)   # score >= grid[j] iff j < idx
                h = torch.bincount(idx, minlength=G+1).double()
                above[name, grp][i] = h.flip(0).cumsum(0).flip(0)[1:]
        if i % 200 == 0: print(f'{i+1}/{n}', flush=True)
    pair_img, pair_lab, pair_n = map(np.concatenate, (pair_img, pair_lab, pair_n))
    miss = {k: torch.cat(v).float().to(dev) for k, v in miss.items()}
    P = len(pair_img); pimg, plab, pn = torch.from_numpy(pair_img).to(dev), torch.from_numpy(pair_lab).to(dev), torch.from_numpy(pair_n).float().to(dev)

    def label_loss(store, imgmask):
        sel = imgmask[pimg]
        num = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], miss[store][sel])
        den = torch.zeros(T, device=dev).index_add_(0, plab[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def image_loss(store, labmask, imgmask):
        sel = labmask[plab] & imgmask[pimg]
        num = torch.zeros(n, G, device=dev).index_add_(0, pimg[sel], miss[store][sel])
        den = torch.zeros(n, device=dev).index_add_(0, pimg[sel], pn[sel])
        return num, den

    def crc(losses, alpha):
        bound = (losses.sum(0)+1)/(len(losses)+1)
        ok = torch.nonzero(bound <= alpha)
        return int(ok[-1]) if len(ok) else 0

    rng = np.random.default_rng(20260926)                                 # exp_label_exchange.py's draws, in its order
    perms = [rng.permutation(n) for _ in range(a.trials)]
    random_sets = [np.sort(rng.choice(T, S, replace=False)) for _ in range(a.trials)]
    rng2 = np.random.default_rng(20261001)
    orders = [S+rng2.permutation(T-S) for _ in range(a.trials)]
    acc = {}
    for tr, perm in enumerate(perms):
        cal = torch.zeros(n, dtype=torch.bool, device=dev); cal[torch.from_numpy(perm[:n//2]).to(dev)] = True; ev = ~cal
        ll = {(s, w): label_loss(s, m) for s in names for w, m in [('cal', cal), ('ev', ev)]}
        for alpha in ALPHAS:
            def arm(key, store, calib, target, t_src, t_add):
                """calib/target: name masks [T]; t_src/t_add: grid index of the source / added names."""
                lc, pc = ll[store, 'cal']; le, pe = ll[store, 'ev']
                tl = torch.where(is_src, t_src, t_add)
                at = lambda l: l.gather(1, tl[:, None])[:, 0]
                _, den = image_loss(store, is_src, ev)                   # image-level source risk, held-out images
                sel = is_src[plab] & ev[pimg]
                inum = torch.zeros(n, device=dev).index_add_(0, pimg[sel], miss[store][sel][:, t_src])
                hs = den > 0
                sz = (above[store, 'src'][:, t_src] + above[store, 'add'][:, t_add])/nlab
                row = (at(lc)[pc & target].mean().item(), at(le)[pe & target].mean().item(), (inum[hs]/den[hs]).mean().item(),
                       sz[ev].mean().item(), float(t_add == 0), int((pc & calib).sum()))
                acc.setdefault((alpha, key), []).append(row)

            def lab_t(store, mask):
                l, present = ll[store, 'cal']; return crc(l[present & mask], alpha)

            def img_t(store):
                num, den = image_loss(store, is_src, cal); has = den > 0
                return crc((num/den.clamp(min=1)[:, None])[has], alpha)

            t_img = img_t('anchored')
            rs = torch.zeros(T, dtype=torch.bool, device=dev); rs[torch.from_numpy(random_sets[tr]).to(dev)] = True
            t = lab_t('anchored', rs)                                     # replay: one threshold for every name
            arm('check: random S of T', 'anchored', rs, ~rs, t, t)
            t = lab_t('anchored', is_src)
            arm('check: dataset split', 'anchored', is_src, ~is_src, t, t)
            arm('source classes (benchmark split), per-label', 'anchored', is_src, ~is_src, t_img, t)
            t_img_nat = img_t('native')
            for m in ms:
                dr = torch.zeros(T, dtype=torch.bool, device=dev); dr[torch.from_numpy(orders[tr][:m]).to(dev)] = True
                arm(f'anchored, m={m}', 'anchored', dr, ~is_src & ~dr, t_img, lab_t('anchored', dr))
                arm(f'native at grown vocabulary, m={m}', 'native', dr, ~is_src & ~dr, t_img_nat, lab_t('native', dr))
        if tr % 50 == 0: print(f'trial {tr}', flush=True)

    ref = Path(f'results/label_exchange_{a.dataset}_{a.tag}_schemes/results.json')
    if not ref.exists(): ref = Path(f'results/label_exchange_{a.dataset}_{a.tag}/results.json')
    refj = json.loads(ref.read_text()) if ref.exists() else None
    result = dict(dataset=a.dataset, tag=a.tag, images=n, pairs=P, trials=a.trials, ms=ms, reference=str(ref) if refj else None, arms={})
    lines = ['# Added-label guarantee from m randomly drawn, annotated names', '',
             f'{a.tag}, {n} {d["name"]} images, {T}-name vocabulary ({S} source names), {a.trials} trials. m = drawn added names; '
             'm\' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining '
             'added labels present (cal: calibration images, the proposition\'s quantity; held-out: other half). Src, image = '
             'image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown '
             'vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of '
             'trials above alpha). Development data; nothing fitted.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', '| Arm | m\' | Added, cal | Added, held-out | Src, image | Size | Floor |', '|---|---:|---:|---:|---:|---:|---:|']
        for (al, key), v in acc.items():
            if al != alpha: continue
            v = np.array(v); mu = v.mean(0); abv = (v[:, :3] > alpha).mean(0)
            r = dict(added_cal=mu[0], added_heldout=mu[1], source_image=mu[2], size=mu[3], floor=mu[4], m_present=mu[5],
                     above_added_cal=abv[0], above_added_heldout=abv[1], above_source_image=abv[2],
                     added_cal_q025_q975=np.quantile(v[:, 0], [.025, .975]).tolist())
            result['arms'][f'a{alpha}, {key}'] = {kk: (float(vv) if not isinstance(vv, list) else vv) for kk, vv in r.items()}
            lines.append(f'| {key} | {mu[5]:.1f} | {100*mu[0]:.2f} ({100*abv[0]:.0f}) | {100*mu[1]:.2f} ({100*abv[1]:.0f}) | '
                         f'{100*mu[2]:.2f} ({100*abv[2]:.0f}) | {mu[3]:.2f} | {100*mu[4]:.1f} |')
        lines.append('')
    if refj:
        checks = {}
        for key, design in [('check: random S of T', 'exchangeable'), ('check: dataset split', 'dataset split')]:
            for alpha in ALPHAS:
                mine = result['arms'][f'a{alpha}, {key}']; theirs = refj['designs'][f'a{alpha}, {design}']['anchored, label-level']
                checks[f'a{alpha}, {design}'] = {k: abs(mine[k2]-theirs[k]) for k, k2 in [('added_cal', 'added_cal'), ('added_heldout', 'added_heldout'), ('size', 'size')]}
        result['checks'] = checks
        worst = max(v for c in checks.values() for v in c.values())
        lines += [f'Replay of {ref.parent.name} (anchored, label-level; added cal / held-out / size): max abs difference {worst:.2e}.', '']
        print('check max abs difference', worst, flush=True)
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_label_sample.py', 'src/exp_label_exchange.py', f"{d['sclip']}/{d['gt_fine']}"]}
    OUT = Path(f'results/label_sample_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
