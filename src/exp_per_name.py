"""Per-name (class-conditional) calibration on the stored scores (development data; nothing is fitted).

Each name c gets its own threshold from the calibration images that contain it:
    t_c = largest grid t with (sum_{i in cal, c in i} l_{i,c}(t) + 1)/(n_c + 1) <= alpha,
where l_{i,c}(t) is the fraction of the sampled pixels of c in image i whose score for c is below t (grid floor if no t
qualifies; with a loss in [0, 1] this happens when n_c < 1/alpha - 1). The images are split at random, so the calibration
and held-out images containing c are exchangeable, and the expected held-out loss of c is at most alpha for every name
(class-conditional CRC). With candidate-independent (anchored) scores l_{i,c} does not depend on the requested
vocabulary, so a name calibrated once keeps this guarantee in every later vocabulary, and adding a name never changes the
thresholds or guarantees of the names calibrated before it. With native scores, l_{i,c} changes when names are added.

Arms (per name, mean over held-out images containing it, averaged over splits):
  anchored, per-name              calibrate and evaluate on the anchored scores (every name; any vocabulary)
  anchored, per-name, k images    as above with at most k calibration images per name (an annotation budget)
  native, per-name, source->grown source names calibrated at the source vocabulary, evaluated at the grown vocabulary
  native, per-name, source        the same thresholds evaluated at the source vocabulary (before growth)
  native, per-name, grown         calibrated and evaluated at the grown vocabulary (needs it at calibration)
  anchored, image-level           the paper's single image-level threshold (source-labelled pixels), for reference
  hybrid, per-name or image-level per-name threshold for calibrated names, the image-level one for the rest
  hybrid, lower of both           calibrated names take the lower of the two thresholds, the rest the image-level one: misses
                                  can only fall relative to either arm, so both guarantees hold at once
  (calibrated names)              the same hybrid, risk recorded for the calibrated names only
Image risk: the paper's image-level loss (missed fraction of source-labelled pixels; names outside the sets count as missed).
Set size: labels per labelled pixel at the grown vocabulary, held-out images, first SIZE_SPLITS splits.

    PYTHONPATH=src python src/exp_per_name.py --dataset ade --tag vitl_bank683
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

SIZE_SPLITS = 20
BUDGETS = [10, 20, 50]
MIN_SPLITS = 10                       # over-alpha test and worst name: names calibrated in at least this many splits


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_{a.dataset}_{a.tag}'], [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    names = ['native_source', 'native', 'anchored']
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(names, d['stores'])}
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)
    is_src = torch.arange(T, device=dev) < S

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    def counts(true, lab, labs):
        true = true.double(); return torch.stack([torch.searchsorted(true[lab == c].sort().values, grid, right=False) for c in labs]).to(torch.int16).cpu()

    # pass 1: (image, label) pairs and their miss counts [pair, G] per store (native_source: source labels only)
    pair_img, pair_lab, pair_n = [], [], []
    miss = {k: [] for k in names}
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0
        labs = torch.unique(g[lab_px])
        pair_img.append(np.full(len(labs), i)); pair_lab.append(labs.cpu().numpy())
        pair_n.append(torch.stack([(g == c).sum() for c in labs]).cpu().numpy())
        for name in names:
            s = torch.from_numpy(np.array(part(stores[name], k))).to(dev)[lab_px].float()
            gl = g[lab_px]
            if name == 'native_source':                                   # source-vocabulary scores: source labels only
                src = gl < S
                m = counts(s[src].gather(1, gl[src][:, None])[:, 0], gl[src], labs[labs < S])
                full = torch.zeros(len(labs), G, dtype=torch.int16); full[(labs < S).cpu()] = m; m = full
            else:
                m = counts(s.gather(1, gl[:, None])[:, 0], gl, labs)
            miss[name].append(m)
        if i % 200 == 0: print(f'{i+1}/{n}', flush=True)
    pair_img, pair_lab, pair_n = map(np.concatenate, (pair_img, pair_lab, pair_n))
    NP = len(pair_img)
    pimg, plab = torch.from_numpy(pair_img).to(dev), torch.from_numpy(pair_lab).to(dev)
    pn = torch.from_numpy(pair_n).float().to(dev)
    loss = {k: torch.cat(v).float().to(dev)/pn[:, None] for k, v in miss.items()}   # per-pair loss curve [NP, G]
    del miss
    src_pair = plab < S

    def per_name_t(store, sel, alpha):
        """Per-name CRC grid index [T] from the pairs in sel (bool [NP]); calibrated [T]: some grid point qualifies (else the
        name is left uncalibrated: out of the sets and out of the guarantee)."""
        num = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], loss[store][sel])
        cnt = torch.zeros(T, device=dev).index_add_(0, plab[sel], torch.ones(int(sel.sum()), device=dev))
        ok = (num+1)/(cnt+1)[:, None] <= alpha
        cal_ok = ok.any(1)
        last = torch.where(cal_ok, G-1-ok.flip(1).float().argmax(1), torch.zeros(T, dtype=torch.long, device=dev))
        return last, cal_ok

    def image_t(store, sel, alpha):
        """The paper's image-level threshold: image loss over source-labelled pixels, CRC over images with any."""
        s2 = sel & src_pair
        num = torch.zeros(n, G, device=dev).index_add_(0, pimg[s2], loss[store][s2]*pn[s2][:, None])
        den = torch.zeros(n, device=dev).index_add_(0, pimg[s2], pn[s2])
        has = den > 0; L = num[has]/den[has][:, None]
        ok = torch.nonzero((L.sum(0)+1)/(len(L)+1) <= alpha)
        return int(ok[-1]) if len(ok) else 0

    def name_risk(store, sel, t):
        """Per-name mean held-out loss [T] at grid indices t [T] (nan where the name has no held-out image)."""
        l = loss[store][sel].gather(1, t[plab[sel]][:, None])[:, 0]
        num = torch.zeros(T, device=dev).index_add_(0, plab[sel], l)
        cnt = torch.zeros(T, device=dev).index_add_(0, plab[sel], torch.ones(int(sel.sum()), device=dev))
        return torch.where(cnt > 0, num/cnt.clamp(min=1), torch.full_like(num, float('nan')))

    def image_risk(store, sel, t, members):
        """The paper's image-level loss at grid indices t [T], mean over the held-out images with source-labelled pixels."""
        s2 = sel & src_pair
        l = loss[store][s2].gather(1, t[plab[s2]][:, None])[:, 0]
        l = torch.where(members[plab[s2]], l, torch.ones_like(l))
        num = torch.zeros(n, device=dev).index_add_(0, pimg[s2], l*pn[s2])
        den = torch.zeros(n, device=dev).index_add_(0, pimg[s2], pn[s2])
        has = den > 0
        return float((num[has]/den[has]).mean())

    present = torch.zeros(T, dtype=torch.bool, device=dev); present[plab] = True
    rng = np.random.default_rng(20260926)                                 # the image splits of exp_label_sample.py
    perms = [rng.permutation(n) for _ in range(a.splits)]
    brng = torch.Generator(device=dev).manual_seed(20261109)
    ARMS = ['anchored, per-name'] + [f'anchored, per-name, {k} images' for k in BUDGETS] + \
           ['native, per-name, source->grown', 'native, per-name, source', 'native, per-name, grown',
            'anchored, image-level, all names', 'anchored, image-level, per-name names',
            'hybrid, per-name or image-level', 'hybrid, per-name or image-level (calibrated names)',
            'hybrid, lower of both', 'hybrid, lower of both (calibrated names)']
    SIZE_STORE = {'native, per-name, grown': 'native'}
    NO_SIZE = ('native, per-name, source->grown', 'native, per-name, source',
               'hybrid, per-name or image-level (calibrated names)', 'hybrid, lower of both (calibrated names)')
    risk = {(al, arm): [] for al in ALPHAS for arm in ARMS}
    ncalib = {(al, arm): [] for al in ALPHAS for arm in ARMS}
    irisk = {(al, arm): [] for al in ALPHAS for arm in ARMS}
    thr_keep = {(al, arm): [] for al in ALPHAS for arm in ARMS}            # threshold values [T] (inf: not in the sets)
    for sp, perm in enumerate(perms):
        cal_img = torch.zeros(n, dtype=torch.bool, device=dev); cal_img[torch.from_numpy(perm[:n//2]).to(dev)] = True
        cal, ev = cal_img[pimg], ~cal_img[pimg]
        # budgets: at most k calibration images per name, chosen at random
        key = plab.double()*2 + torch.rand(NP, generator=brng, device=dev, dtype=torch.float64)
        key = torch.where(cal, key, torch.full_like(key, float('inf')))
        order = torch.argsort(key); rank = torch.empty(NP, dtype=torch.long, device=dev)
        lab_sorted = plab[order]
        first = torch.zeros(T+1, dtype=torch.long, device=dev)
        first.index_reduce_(0, lab_sorted, torch.arange(NP, device=dev), 'amin', include_self=False)
        rank[order] = torch.arange(NP, device=dev) - first[lab_sorted]
        for alpha in ALPHAS:
            def put(arm, store, t, members, sel_ev, record=None):
                """members [T]: names in the sets; per-name risk is recorded for record [T] (default: members)."""
                record = members if record is None else record
                r = name_risk(store, sel_ev, t)
                risk[alpha, arm].append(torch.where(record, r, torch.full_like(r, float('nan'))).cpu().numpy())
                ncalib[alpha, arm].append(int((record & present).sum()))
                irisk[alpha, arm].append(image_risk(store, sel_ev, t, members))
                if sp < SIZE_SPLITS: thr_keep[alpha, arm].append(torch.where(members, grid[t], torch.full_like(grid[t], float('inf'))).float())

            t, ok = per_name_t('anchored', cal, alpha); put('anchored, per-name', 'anchored', t, ok, ev)
            for k in BUDGETS:
                tk, okk = per_name_t('anchored', cal & (rank < k), alpha); put(f'anchored, per-name, {k} images', 'anchored', tk, okk, ev)
            ts, oks = per_name_t('native_source', cal & src_pair, alpha)
            put('native, per-name, source->grown', 'native', ts, oks & is_src, ev & src_pair)
            put('native, per-name, source', 'native_source', ts, oks & is_src, ev & src_pair)
            tg, okg = per_name_t('native', cal, alpha); put('native, per-name, grown', 'native', tg, okg, ev)
            ti = torch.full((T,), image_t('anchored', cal, alpha), dtype=torch.long, device=dev)
            put('anchored, image-level, all names', 'anchored', ti, torch.ones(T, dtype=torch.bool, device=dev), ev)
            put('anchored, image-level, per-name names', 'anchored', ti, ok, ev)
            every = torch.ones(T, dtype=torch.bool, device=dev)
            th = torch.where(ok, t, ti)
            put('hybrid, per-name or image-level', 'anchored', th, every, ev)
            put('hybrid, per-name or image-level (calibrated names)', 'anchored', th, every, ev, record=ok)
            tm = torch.where(ok, torch.minimum(t, ti), ti)
            put('hybrid, lower of both', 'anchored', tm, every, ev)
            put('hybrid, lower of both (calibrated names)', 'anchored', tm, every, ev, record=ok)
        if sp % 50 == 0: print(f'split {sp}', flush=True)

    # pass 2: set sizes at the grown vocabulary on held-out images, first SIZE_SPLITS splits
    size_arms = [(al, arm) for al in ALPHAS for arm in ARMS if arm not in NO_SIZE]
    tot = {x: torch.zeros(SIZE_SPLITS, device=dev, dtype=torch.float64) for x in size_arms}
    npx = torch.zeros(SIZE_SPLITS, device=dev, dtype=torch.float64)
    ev_masks = torch.stack([torch.from_numpy(np.isin(np.arange(n), perms[sp][n//2:])).to(dev) for sp in range(SIZE_SPLITS)])  # [K, n]
    thr_val = {x: torch.stack(thr_keep[x]) for x in size_arms}                                                               # [K, T]
    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0; m = ev_masks[:, i].double()
        npx += m*lab_px.sum()
        sc = {st: torch.from_numpy(np.array(part(stores[st], k))).to(dev)[lab_px].float() for st in ('anchored', 'native')}
        for al, arm in size_arms:
            c = (sc[SIZE_STORE.get(arm, 'anchored')][None] >= thr_val[al, arm][:, None, :]).sum((1, 2)).double()
            tot[al, arm] += m*c
        if i % 400 == 0: print(f'size {i+1}/{n}', flush=True)
    size = {x: (tot[x]/npx).mean().item() for x in tot}

    result = dict(dataset=a.dataset, tag=a.tag, images=n, pairs=NP, splits=a.splits, size_splits=SIZE_SPLITS, budgets=BUDGETS,
                  names_present=int(present.sum()), arms={})
    lines = ['# Per-name (class-conditional) calibration', '',
             f'{a.tag}, {n} {d["name"]} images, {T} names ({S} source; {int(present.sum())} present in some image), {a.splits} random '
             'half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 '
             'calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the '
             'held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most '
             'alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds '
             'alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. '
             'Image risk: the paper\'s image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), '
             f'mean over held-out images and splits. Size: labels per labelled pixel at {T} names, held-out images, first {SIZE_SPLITS} splits. '
             'Development data; nothing fitted.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', '| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for arm in ARMS:
            R = np.stack(risk[alpha, arm])                                  # [splits, T]
            seen = (~np.isnan(R)).sum(0); ok = seen > 0
            mu = np.full(T, np.nan); se = np.full(T, np.nan)
            mu[ok] = np.nanmean(R[:, ok], 0); se[ok] = np.nanstd(R[:, ok], 0)/np.sqrt(seen[ok])
            est = seen >= MIN_SPLITS                                       # enough splits for a standard error
            over = est & (mu - alpha > 3*se)
            srcm, addm = est & (np.arange(T) < S), est & (np.arange(T) >= S)
            sz = size.get((alpha, arm), float('nan'))
            stat = lambda m_, fn: float(fn(mu[m_])) if m_.any() else None
            row = dict(calibrated=float(np.mean(ncalib[alpha, arm])), evaluated=int(ok.sum()), macro=stat(ok, np.mean), worst=stat(est, np.max), estimated=int(est.sum()),
                       image_risk=float(np.mean(irisk[alpha, arm])),
                       over=int(over.sum()), src_macro=stat(srcm, np.mean), src_worst=stat(srcm, np.max), add_macro=stat(addm, np.mean),
                       add_worst=stat(addm, np.max), size=float(sz), per_name=[None if np.isnan(v) else float(v) for v in mu],
                       over_names=[(int(i), float(mu[i]), float(se[i]), int(seen[i])) for i in np.flatnonzero(over)])
            result['arms'][f'a{alpha}, {arm}'] = row
            f = lambda v: '-' if v is None else f'{100*v:.1f}'
            lines.append(f'| {arm} | {row["calibrated"]:.0f} | {f(row["macro"])} | {f(row["worst"])} | {row["over"]} | '
                         f'{f(row["src_macro"])} / {f(row["src_worst"])} | {f(row["add_macro"])} / {f(row["add_worst"])} | {f(row["image_risk"])} | {sz:.2f} |')
        lines.append('')
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_per_name.py', 'src/exp_label_exchange.py', f"{d['sclip']}/{d['gt_fine']}"]}
    OUT = Path(f'results/per_name_{a.dataset}_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    print('\n'.join(lines))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    (OUT/'results.json').write_text(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
