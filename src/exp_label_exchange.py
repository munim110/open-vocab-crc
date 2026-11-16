"""A guarantee for the added labels under label exchangeability (development data, stored scores).

With candidate-independent scores the loss of a label, l_c(t) = fraction of the pixels of label c (in a fixed image set)
whose score for c is below t, is a property of the label alone: it does not depend on the vocabulary the label is scored
in. If the m source labels and an added label are exchangeable (e.g. the source vocabulary is a uniformly random subset
of the names that will ever be requested), CRC with labels as the units,
    t_lab = largest grid t with (sum_{c in source} l_c(t) + 1)/(m + 1) <= alpha,
gives E[l_c(t_lab)] <= alpha for every added label c, hence for their mean; the loss is measured on the calibration
images (exact, conditional on the images) and we also report it on held-out images. For native scores l_c depends on
the vocabulary, so the source labels' losses at the source vocabulary are not exchangeable with an added label's loss
after growth. Deploying min(t_img, t_lab) keeps both the image-level source guarantee and this one.

When the source vocabulary is not a random draw (the dataset's own split: its source classes are the frequent ones),
labels are weighted-exchangeable if they differ only through a feature computable without annotations. The feature is
the predicted prevalence (# sampled pixels, labelled or not, with score >= 0 logit), cut into bins by a scheme:
  allB   B quantile bins of the feature over all grown-vocabulary names;
  srcB   B bins whose edges are the feature's quantiles over the source names (equal source counts per bin).
Weighted CRC uses w_b = (added names in b / added names)/(source names in b / source names); for a label of bin b the
threshold is the largest t with (sum_i w_i l_i(t) + w_b)/(sum_i w_i + w_b) <= alpha. The test point's mass
w_b/(sum_i w_i + w_b) must be <= alpha for any threshold above the grid floor to be feasible; the "floor" column is the
share of added labels whose bin has no feasible threshold (all labels then enter the set). Stratified = CRC per bin.
--oracle adds the same weighted arms with the feature replaced by the true prevalence (# annotated sampled pixels of the
label over all images, calibration and held-out): estimated vs oracle weights. It needs annotations of the added labels,
so it is a diagnostic, not a deployable method.

Designs (500 trials each, fresh random half/half image split per trial; a label enters a trial's calibration if it has a
sampled pixel in the calibration images):
  exchangeable   source = a uniformly random S of the T names (fresh per trial).
  exchangeable, native frozen   (ADE, when exp_label_exchange_probe.py has run) source = one of its K sets; native
                 calibrated on its own pass at the source set, deployed at T.
  dataset split  source = the dataset's S names.
Reported per arm: mean over trials of the added-label mean loss on calibration and held-out images (and % of trials
above alpha), class-averaged source loss, image-level source risk, set size at T on held-out images (exact, per-label
thresholds), share of added labels at the grid floor, and the decomposition of prop:shift: the source labels' mean loss
at the threshold, Delta(t) = added minus source mean loss there, and max over the grid of Delta (the worst-case bound).

    PYTHONPATH=src python src/exp_label_exchange.py --dataset ade --tag vitl_bank683 [--schemes all2,all3,src3]
        [--designs "dataset split"] [--oracle] [--suffix _oracle]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_added_label_risk import DATASETS, IGN847
from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID

# the reserved ADE training images (docs/PROTOCOL_ADDED_LABEL_RESERVE.md): scores of the first reserve read, A-847 labels
# from build_gt_reserve.py; --reserve-dir cache/confirmation_vitl_bank683_smoke runs the same path on 40 validation images
RESERVE_DIR = 'cache/confirmation_vitl_bank683'
DATASETS = dict(DATASETS, ade_reserve=dict(DATASETS['ade'], sclip=RESERVE_DIR, name='reserved ADE training'))


def gt_all(d, ids):
    """Column in the grown vocabulary of every sampled pixel's label (source annotation first; -1: none) [N, P]."""
    S, T = d['S'], d['T']
    rows = d['manifest']()['rows']
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(rows) == T
    lut = np.full(IGN847+1, -1, np.int64)
    for i, r in enumerate(rows[S:]): lut[r[d['fine_key']]] = S+r.get('position', i)
    assert (lut >= 0).sum() == T-S
    gs, gf = np.load(f"{d['sclip']}/{d['gt_source']}")[ids], np.load(f"{d['sclip']}/{d['gt_fine']}")[ids]
    return np.where(gs < S, gs.astype(np.int64), lut[gf])


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--trials', type=int, default=500)
    ap.add_argument('--schemes', default='all2,all3,all5,src2,src3,src5', help='prevalence binning schemes (allB / srcB)')
    ap.add_argument('--designs', default='', help='comma-separated subset of the designs (default: all)')
    ap.add_argument('--oracle', action='store_true', help='also weight by the true (annotated) prevalence')
    ap.add_argument('--suffix', default='', help='appended to the output directory name')
    ap.add_argument('--reserve-dir', default=RESERVE_DIR, help='ade_reserve: score and label directory')
    ap.add_argument('--reserve-read', action='store_true', help='ade_reserve: required to read the reserve itself (user approval)')
    a = ap.parse_args()
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    reserve = a.dataset == 'ade_reserve'
    if reserve:
        assert a.tag == 'vitl_bank683', 'the reserve holds CAT-Seg ViT-L scores with the 683-name bank only'
        assert a.reserve_read or a.reserve_dir != RESERVE_DIR, 'reading the reserve needs --reserve-read (protocol: user approval)'
        checks = json.loads((Path(a.reserve_dir)/'gt_checks.json').read_text())
        assert checks['C1_pass'] and checks['C2_pass'] and checks['C3_pass'], 'integrity checks failed: protocol says stop'
        d = dict(d, sclip=a.reserve_dir, name=d['name'] if a.reserve_dir == RESERVE_DIR else 'ADE validation (reserve-path smoke)')
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    if reserve:
        runs, caches = [], [a.reserve_dir]
    elif a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    else:
        runs, caches = [f'results/headroom_probe_pascal_{a.tag}'], [f'cache/headroom_probe_pascal_{a.tag}']
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], []) if runs else \
        list(range(len(np.load(f'{a.reserve_dir}/gt150.npy', mmap_mode='r'))))
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(['native150', 'native845', 'anchored845'], d['stores'])}
    PROBE = Path(f'results/label_exchange_probe_{a.tag}')
    frozen_sets = None
    if a.dataset == 'ade' and (PROBE/'results.json').exists():
        proto = json.loads((PROBE/'protocol.json').read_text())
        assert proto['image_ids'] == ids
        frozen_sets = [np.array(s) for s in proto['source_sets']]
        native_sets = np.load(f'cache/label_exchange_{a.tag}/native_sets.npy', mmap_mode='r')
    gt = gt_all(d, ids)
    keep = np.flatnonzero((gt >= 0).any(1)); n = len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev); G = len(grid)
    names_t = torch.arange(T, device=dev)
    schemes = [(s[:3], int(s[3:])) for s in a.schemes.split(',')]

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    # label feature without annotations: predicted prevalence = # sampled pixels (all images, labelled or not) with score >= 0
    # logit; candidate-independent for the anchored scores, at the fixed T-name vocabulary for native845. Rank ties broken
    # by name order.
    prev = {k: torch.zeros(T, dtype=torch.float64, device=dev) for k in ['anchored845', 'native845']}
    for k in keep:
        for name in prev:
            prev[name] += (torch.from_numpy(np.array(part(stores[name], k))).to(dev) >= 0).sum(0).double()
    if a.oracle:
        g = gt[keep]; prev['oracle'] = torch.from_numpy(np.bincount(g[g >= 0], minlength=T)).double().to(dev)
    rank = {}
    for name, v in prev.items():
        r = np.empty(T, np.int64); r[np.argsort(v.cpu().numpy(), kind='stable')] = np.arange(T)
        rank[name] = torch.from_numpy(r).to(dev)

    def bins(scheme, store, src_t):
        """Prevalence bin of every name [T] under a scheme for a given source set."""
        kind, B = scheme; r = rank[store]
        if kind == 'all': return r*B//T
        rs = r[src_t].sort().values; m = len(rs)
        edges = rs[torch.tensor([j*m//B for j in range(1, B)], device=dev)]
        return torch.searchsorted(edges, r, right=True)

    # (image, label) pairs: miss counts [pair, G] (# pixels of the label with score < t) per store, pixel counts [pair];
    # per image and label, # labelled pixels whose score for the label is >= t [image, T, G] (exact set size for any
    # per-label thresholds)
    pair_img, pair_lab, pair_n = [], [], []
    miss = {k: [] for k in ['anchored845', 'native845', 'native150'] + [f'set{j}' for j in range(len(frozen_sets or []))]}
    above = {k: torch.empty(n, T, G, dtype=torch.int16, device=dev) for k in ['anchored845', 'native845']}
    nlab = torch.zeros(n, device=dev)

    def counts(true, lab, labs):
        true = true.double(); return torch.stack([torch.searchsorted(true[lab == c].sort().values, grid, right=False) for c in labs]).to(torch.int16).cpu()

    for i, k in enumerate(keep):
        g = torch.from_numpy(gt[k]).to(dev); lab_px = g >= 0
        labs = torch.unique(g[lab_px]); nlab[i] = lab_px.sum()
        pair_img.append(np.full(len(labs), i)); pair_lab.append(labs.cpu().numpy())
        pair_n.append(torch.stack([(g == c).sum() for c in labs]).cpu().numpy())
        for name in ['anchored845', 'native845']:
            s = torch.from_numpy(np.array(part(stores[name], k))).to(dev)[lab_px].float()
            true = s.gather(1, g[lab_px][:, None])[:, 0]
            miss[name].append(counts(true, g[lab_px], labs))
            srt = s.double().T.sort(1).values.contiguous()                      # [T, pixels]
            above[name][i] = (len(s)-torch.searchsorted(srt, grid[None].expand(T, G).contiguous(), right=False)).to(torch.int16)
        src = lab_px & (g < S); ls = labs[labs < S]
        s = torch.from_numpy(np.array(part(stores['native150'], k))).to(dev)[src].float()
        m150 = torch.zeros(len(labs), G, dtype=torch.int16)
        if len(ls): m150[:len(ls)] = counts(s.gather(1, g[src][:, None])[:, 0], g[src], ls)   # labs is sorted: source labels first
        miss['native150'].append(m150)
        for j, vocab in enumerate(frozen_sets or []):
            true = torch.from_numpy(native_sets[j, k].astype(np.float32)).to(dev)
            insub = torch.zeros(T, dtype=torch.bool, device=dev); insub[torch.from_numpy(vocab).to(dev)] = True
            mj = torch.zeros(len(labs), G, dtype=torch.int16)
            sel = insub[labs]
            if sel.any():
                px = lab_px & insub[g.clamp(min=0)]
                assert not torch.isnan(true[px]).any()
                mj[sel.cpu()] = counts(true[px].double(), g[px], labs[sel])
            miss[f'set{j}'].append(mj)
        if i % 200 == 0: print(f'{i+1}/{n}', flush=True)
    pair_img, pair_lab, pair_n = map(np.concatenate, (pair_img, pair_lab, pair_n))
    miss = {k: torch.cat(v).float().to(dev) for k, v in miss.items()}
    P = len(pair_img); pimg, plab, pn = torch.from_numpy(pair_img).to(dev), torch.from_numpy(pair_lab).to(dev), torch.from_numpy(pair_n).float().to(dev)

    def label_loss(store, imgmask):
        """Per-label pooled loss [T, G] over the images in imgmask, and the labels present there [T]."""
        sel = torch.from_numpy(imgmask).to(dev)[pimg]
        num = torch.zeros(T, G, device=dev).index_add_(0, plab[sel], miss[store][sel])
        den = torch.zeros(T, device=dev).index_add_(0, plab[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def image_loss(store, labmask):
        """Per-image source-pixel loss [n, G] (labels in labmask), images with such a pixel [n]."""
        sel = torch.from_numpy(labmask).to(dev)[plab]
        num = torch.zeros(n, G, device=dev).index_add_(0, pimg[sel], miss[store][sel])
        den = torch.zeros(n, device=dev).index_add_(0, pimg[sel], pn[sel])
        return num/den.clamp(min=1)[:, None], den > 0

    def crc(losses, alpha):
        bound = (losses.sum(0)+1)/(len(losses)+1)
        ok = torch.nonzero(bound <= alpha)
        return int(ok[-1]) if len(ok) else 0

    def binned_t(b, cal_loss, src_t, alpha, how):
        """One grid threshold per prevalence bin [B] from the source labels present in the calibration images (bin
        without a source name, or no feasible threshold: lowest grid point)."""
        l, present = cal_loss; B = int(b.max())+1; out = []
        nb = torch.stack([(src_t & (b == i)).sum() for i in range(B)]).double(); na = torch.stack([(~src_t & (b == i)).sum() for i in range(B)]).double()
        w = torch.where(nb > 0, (na/na.sum())/(nb/nb.sum()).clamp(min=1e-12), torch.zeros_like(nb))
        for j in range(B):
            if nb[j] == 0: out.append(0); continue
            if how == 'stratified':
                out.append(crc(l[present & src_t & (b == j)], alpha)); continue
            wi = w[b[present & src_t]]
            bound = ((wi[:, None]*l[present & src_t]).sum(0)+w[j])/(wi.sum()+w[j])
            ok = torch.nonzero(bound <= alpha)
            out.append(int(ok[-1]) if len(ok) else 0)
        return torch.tensor(out, device=dev)[b]                              # threshold of every name [T]

    rng = np.random.default_rng(20260926)
    perms = [rng.permutation(n) for _ in range(a.trials)]
    random_sets = [np.sort(rng.choice(T, S, replace=False)) for _ in range(a.trials)]
    designs = {'exchangeable': [(p, s, None) for p, s in zip(perms, random_sets)],
               'dataset split': [(p, np.arange(S), 'native150') for p in perms]}
    if frozen_sets:
        designs['exchangeable, native frozen'] = [(p, frozen_sets[t % len(frozen_sets)], f'set{t % len(frozen_sets)}') for t, p in enumerate(perms)]
    if a.designs:
        designs = {k: designs[k] for k in a.designs.split(',')}
    result = dict(dataset=a.dataset, tag=a.tag, images=n, pairs=P, trials=a.trials, schemes=a.schemes, frozen_sets=len(frozen_sets or []), designs={})
    lines = ['# A guarantee for the added labels under (weighted) label exchangeability', '',
             f'CAT-Seg ({a.tag}), {n} {d["name"]} images with a labelled sampled pixel ({T}-name vocabulary: {S} source names, then '
             f'the {d["fine"]} annotation mapped to the added names), {a.trials} trials (random half/half image split; source vocabulary as per design). '
             'Label loss = pooled fraction of the label\'s sampled pixels whose score for it is below the threshold. "Added, cal" = mean '
             'over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on '
             'the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source '
             f'risk (the paper\'s guarantee); size = labels per labelled pixel at {T} names, held-out images; floor = % of added labels '
             'present whose threshold is the grid floor. Risks in % (and % of trials above alpha). ' + ('Reserved images, read once under docs/PROTOCOL_ADDED_LABEL_RESERVE.md; nothing fitted.'
                                                 if reserve and a.reserve_dir == RESERVE_DIR else 'Development data; nothing fitted.'), '']
    for design, trials in designs.items():
        acc = {}
        for perm, src, frozen_store in trials:
            cal = np.zeros(n, bool); cal[perm[:n//2]] = True; ev = ~cal
            cal_t, ev_t = torch.from_numpy(cal).to(dev), torch.from_numpy(ev).to(dev)
            srcmask = np.zeros(T, bool); srcmask[src] = True; src_t = torch.from_numpy(srcmask).to(dev)
            ll, il = {}, {}
            for store in ['anchored845', 'native845'] + ([frozen_store] if frozen_store else []):
                ll[store, 'cal'] = label_loss(store, cal); ll[store, 'ev'] = label_loss(store, ev); il[store] = image_loss(store, srcmask)
            sb = {(sc, store): bins(sc, store, src_t) for sc in schemes for store in prev}
            for alpha in ALPHAS:
                def lab_t(store):
                    l, present = ll[store, 'cal']; return crc(l[present & src_t], alpha)

                def img_t(store):
                    l, has = il[store]; return crc(l[cal_t & has], alpha)

                arms = {'anchored, label-level': ('anchored845', lab_t('anchored845')),
                        'anchored, image-level (paper)': ('anchored845', img_t('anchored845'))}
                arms['anchored, both'] = ('anchored845', min(arms['anchored, label-level'][1], arms['anchored, image-level (paper)'][1]))
                arms['native, full known, label-level'] = ('native845', lab_t('native845'))
                if frozen_store:
                    arms['native, frozen at source, label-level'] = ('native845', lab_t(frozen_store))
                    arms['native, frozen at source, image-level'] = ('native845', img_t(frozen_store))
                for sc in schemes:
                    tag = f'{sc[0]}{sc[1]}'
                    for model, store in [('anchored', 'anchored845'), ('native, full known', 'native845')]:
                        arms[f'{model}, weighted, {tag}'] = (store, binned_t(sb[sc, store], ll[store, 'cal'], src_t, alpha, 'weighted'))
                    arms[f'anchored, stratified, {tag}'] = ('anchored845', binned_t(sb[sc, 'anchored845'], ll['anchored845', 'cal'], src_t, alpha, 'stratified'))
                    if a.oracle:
                        for model, store in [('anchored', 'anchored845'), ('native, full known', 'native845')]:
                            arms[f'{model}, weighted by true prevalence, {tag}'] = (store, binned_t(sb[sc, 'oracle'], ll[store, 'cal'], src_t, alpha, 'weighted'))
                for arm, (store, gi) in arms.items():
                    lc, pc = ll[store, 'cal']; le, pe = ll[store, 'ev']
                    tl = torch.full((T,), gi, device=dev) if np.ndim(gi) == 0 else gi          # threshold of every name [T]
                    at = lambda l: l.gather(1, tl[:, None])[:, 0]
                    sel = src_t[plab] & ev_t[pimg]
                    num = torch.zeros(n, device=dev).index_add_(0, pimg[sel], miss[store][sel].gather(1, tl[plab[sel]][:, None])[:, 0])
                    den = torch.zeros(n, device=dev).index_add_(0, pimg[sel], pn[sel]); hs = den > 0
                    sz = above[store].gather(2, tl[None, :, None].expand(n, T, 1))[:, :, 0].float().sum(1)/nlab
                    row = (at(lc)[pc & ~src_t].mean().item(), at(le)[pe & ~src_t].mean().item(), at(le)[pe & src_t].mean().item(),
                           (num[hs]/den[hs]).mean().item(), sz[ev_t].mean().item(), (tl[pc & ~src_t] == 0).float().mean().item())
                    # harder-added-labels decomposition (prop:shift): added mean = source mean at t + Delta(t), with the
                    # mean label-loss curves of the source and added labels present in the calibration images; max_t Delta
                    # is the worst-case bound (single-threshold arms only). Source curve from the arm's own store (for the
                    # native frozen arm: the source vocabulary pass).
                    ls_cal = ll[frozen_store, 'cal'] if store == 'native845' and 'frozen' in arm and frozen_store else (lc, pc)
                    src_at = ls_cal[0].gather(1, tl[:, None])[:, 0][ls_cal[1] & src_t].mean().item()
                    dmax = ((lc[pc & ~src_t].mean(0)-ls_cal[0][ls_cal[1] & src_t].mean(0)).max().item()
                            if np.ndim(gi) == 0 else float('nan'))
                    acc.setdefault((alpha, arm), []).append(row + (int((pc & src_t).sum()), int((pc & ~src_t).sum()), src_at, dmax))
        for alpha in ALPHAS:
            rows = {}
            lines += [f'## alpha = {alpha}, {design}', '',
                      f'| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at {T} | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |',
                      '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
            for (al, arm), v in acc.items():
                if al != alpha: continue
                v = np.array(v); m = v.mean(0); abv = (v[:, :4] > alpha).mean(0)
                rows[arm] = dict(added_cal=m[0], added_heldout=m[1], source_class=m[2], source_image=m[3], size=m[4], floor=m[5],
                                 above_added_cal=abv[0], above_added_heldout=abv[1], above_source_class=abv[2], above_source_image=abv[3],
                                 source_labels_present=m[6], added_labels_present=m[7],
                                 source_cal_at_t=m[8], delta_at_t=m[0]-m[8], delta_max=m[9],
                                 added_cal_q025_q975=np.quantile(v[:, 0], [.025, .975]).tolist())
                lines.append(f'| {arm} | {100*m[0]:.2f} ({100*abv[0]:.0f}) | {100*m[1]:.2f} ({100*abv[1]:.0f}) | {100*m[2]:.2f} ({100*abv[2]:.0f}) | '
                             f'{100*m[3]:.2f} ({100*abv[3]:.0f}) | {m[4]:.2f} | {100*m[5]:.1f} | {m[6]:.0f} / {m[7]:.0f} | '
                             f'{100*m[8]:.2f} | {100*(m[0]-m[8]):.2f} | {100*m[9]:.2f} |')
            lines.append('')
            result['designs'][f'a{alpha}, {design}'] = {k: {kk: (float(vv) if not isinstance(vv, list) else vv) for kk, vv in r.items()} for k, r in rows.items()}
            print('\n'.join(lines[-len(rows)-4:]), flush=True)
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_label_exchange.py', 'src/exp_label_exchange_probe.py', f"{d['sclip']}/{d['gt_fine']}"]
                        + (['src/build_gt_reserve.py', 'docs/PROTOCOL_ADDED_LABEL_RESERVE.md', 'meta/natural_vocab_v1.json',
                            'meta/ade_confirmation_reserve_v1.json', f"{d['sclip']}/gt_checks.json"] if reserve else [])}
    OUT = Path(f'results/label_exchange_{a.dataset}_{a.tag}{a.suffix}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
