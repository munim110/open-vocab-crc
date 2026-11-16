"""Miss risk on the ADDED labels under the source-calibrated threshold (development data, ADE validation).

Every headroom result measures the miss risk on pixels whose true label is one of the 150 source labels, which is
where the CRC guarantee lives; a recipe that quietly suppressed the added labels would look free there. The full
ADE20K annotations (A-847 train ids at the probe's sampled pixels, cache/sclip/gt847.npy, built by build_gt.py and
encode.py with the same pixel seed) label 8.4% of the sampled pixels with one of the 695 added names and no source
label, so that miss rate can be measured directly on the stored scores:
  * arms: anchored (threshold from source-label pixels at 150 labels, frozen), native frozen (same, native scores),
    native replay (threshold from source-label pixels at 845 labels), and two references that use the added-label
    annotations at calibration time (anchored / native at 845, threshold from all 845-labelled pixels);
  * populations: source-label pixels (guaranteed), added-label pixels, all 845-labelled pixels; image-level means,
    images without a pixel of a population excluded from that population's mean; set size over all labelled pixels;
  * two size-matched diagnostics that separate the threshold from the set size: native at the grid point whose
    calibration-image set size is closest to the anchored frozen threshold's, and anchored shrunk to the native replay
    threshold's set size (matched on calibration images, evaluated on the held-out half; no guarantee for either).
Same design as exp_headroom_splits.py (random half/half splits). Nothing is fitted; no guarantee is claimed for the
added labels: this is a report of what the frozen threshold does to labels it was never calibrated on.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID

S, T = 150, 845
IGN847 = 65535          # ignore value of the fine annotations (A-847 train ids and the Pascal 459 ids alike)


def _ade_manifest():
    from natural_vocab import load_manifest
    return load_manifest()


def _pascal_manifest():
    from pascal_natural_vocab import load_manifest
    return load_manifest()


# Pascal Context: the 459-label annotation at the sampled pixels (cache/pascal_sclip/gt459.npy, encode_pascal.py) plays the
# role of A-847; the 399 added names are the 459 minus the 59 source names and 'unknown'. One probe run over all images.
DATASETS = dict(
    ade=dict(S=150, T=845, sclip='cache/sclip', gt_source='gt150.npy', gt_fine='gt847.npy', stores=('native150', 'native845', 'anchored845'),
             manifest=_ade_manifest, fine_key='train_id', fine='A-847', name='ADE validation'),
    pascal=dict(S=59, T=458, sclip='cache/pascal_sclip', gt_source='gt59.npy', gt_fine='gt459.npy', stores=('native_source', 'native_full', 'anchored_full'),
                manifest=_pascal_manifest, fine_key='fine_id', fine='PC-459', name='Pascal Context validation'))


def loss_curve(true, grid):
    """Fraction of the population whose true-label score is below each grid threshold [G] (empty population: nan)."""
    if len(true) == 0: return np.full(len(grid), np.nan)
    return (torch.searchsorted(true.sort().values, grid, right=False).double()/len(true)).cpu().numpy()


def size_curve(s, grid):
    """Mean set size over the given pixels at each grid threshold [G] (member: score >= threshold)."""
    if len(s) == 0: return np.full(len(grid), np.nan)
    idx = torch.searchsorted(grid, s.reshape(-1), right=True)
    below = torch.bincount(idx, minlength=len(grid)+1).double().cumsum(0)[:-1]
    return ((s.shape[1]*len(s)-below)/len(s)).cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='', help='probe run tag as in exp_headroom_splits.py (empty: released ViT-B, COCO-171 bank)')
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS), help='ADE 150 -> 845 (A-847 annotations) or Pascal Context 59 -> 458 (459-label annotations)')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    global S, T
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    sfx = f'_{a.tag}' if a.tag else ''
    if a.dataset == 'ade':
        runs = [f'results/headroom_probe_ade{sfx}', f'results/headroom_probe_ade{sfx}_rest']
        caches = [f'cache/headroom_probe{sfx}', f'cache/headroom_probe{sfx}_rest']
    else:                                                                  # one probe run over all cached images (exp_headroom_probe_pascal.py)
        runs, caches = [f'results/headroom_probe_pascal{sfx}'], [f'cache/headroom_probe_pascal{sfx}']
    OUT = Path(f'results/added_label_risk_{a.dataset}{sfx}'); OUT.mkdir(parents=True, exist_ok=True)
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])
    assert len(set(ids)) == len(ids)
    gt150 = np.load(f"{d['sclip']}/{d['gt_source']}")[ids]                  # source-vocabulary annotation (>= S: none)
    gt847 = np.load(f"{d['sclip']}/{d['gt_fine']}")[ids]                    # fine annotation (IGN847: none)
    rows = d['manifest']()['rows']
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(rows) == T
    lut = np.full(IGN847+1, -1, np.int64)                                 # fine annotation id -> column in the grown vocabulary (-1: none)
    for i, r in enumerate(rows[S:]): lut[r[d['fine_key']]] = S+r.get('position', i)
    assert (lut >= 0).sum() == T-S
    gt845 = np.where(gt150 < S, gt150.astype(np.int64), lut[gt847])      # source annotation first, then an added label, else -1 (ignore)
    pops = dict(source=(gt845 >= 0) & (gt845 < S), added=gt845 >= S, all=gt845 >= 0)
    unlabelled_847 = (gt847 != IGN847) & (gt845 < 0)                     # fine labels outside the grown vocabulary
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(['native150', 'native845', 'anchored845'], d['stores'])}
    keep = np.flatnonzero(pops['source'].any(1)); dropped = len(ids)-len(keep)   # same exclusion as the splits script

    def scores(store, k):
        for part in stores[store]:
            if k < len(part): return torch.from_numpy(np.array(part[k])).to(dev).double()
            k -= len(part)

    grid = torch.from_numpy(LOGIT_GRID).to(dev)
    # loss[(store, pop)][image, G]; size[store][image, G] over all labelled pixels; n[pop][image] population sizes
    loss, size = {}, {}
    n = {p: m[keep].sum(1) for p, m in pops.items()}
    for store in stores:
        for pop in (['source'] if store == 'native150' else pops):
            rows_ = []
            for k in keep:
                s = scores(store, k); m = torch.from_numpy(pops[pop][k]).to(dev); g = torch.from_numpy(gt845[k]).to(dev)
                rows_.append(loss_curve(s[m].gather(1, g[m][:, None])[:, 0], grid))
            loss[store, pop] = np.stack(rows_)
        if store != 'native150':
            size[store] = np.stack([size_curve(scores(store, k)[torch.from_numpy(pops['all'][k]).to(dev)], grid) for k in keep]).astype(np.float32)
        print(store, 'done', flush=True)

    def pick(store, pop, cal, alpha):
        L = loss[store, pop][cal]; ok = ~np.isnan(L).any(0)
        bound = (np.nan_to_num(L).sum(0)+1)/(len(cal)+1)
        return np.flatnonzero((bound <= alpha) & ok)[-1]

    def mean_over(store, pop, ev, g):
        v = loss[store, pop][ev, g]; return float(np.nanmean(v)), int((~np.isnan(v)).sum())

    def match(store, cal, target):
        """Grid point whose mean set size over the calibration images is closest to target."""
        return int(np.nanargmin(np.abs(np.nanmean(size[store][cal], 0)-target)))

    # arm -> (calibration store, calibration population, evaluation store)
    arms = dict(anchored_frozen=('anchored845', 'source', 'anchored845'), native_frozen=('native150', 'source', 'native845'),
                native_replay=('native845', 'source', 'native845'),
                anchored_calibrated_on_all845=('anchored845', 'all', 'anchored845'), native_calibrated_on_all845=('native845', 'all', 'native845'))
    # size-matched diagnostic -> (evaluation store, arm whose calibration-image set size is matched)
    matched = dict(native_at_anchored_frozen_size=('native845', 'anchored_frozen'), anchored_at_native_replay_size=('anchored845', 'native_replay'))
    n_img = len(keep); n_cal = n_img//2
    rng = np.random.default_rng(20261003)                                  # same seed as exp_headroom_splits.py
    perms = [rng.permutation(n_img) for _ in range(a.splits)]
    frac = {p: float(m[keep].mean()) for p, m in pops.items()}
    result = dict(tag=a.tag or 'vitb_coco171', dataset=a.dataset, source_labels=S, labels=T, images=n_img, excluded_images=dropped, splits=a.splits, alphas=ALPHAS,
                  pixel_fraction=frac, pixel_fraction_a847_outside_vocab=float(unlabelled_847[keep].mean()),
                  images_with_added_pixels=int((n['added'] > 0).sum()), designs={})
    lines = [f'# Miss risk on the added labels: {a.tag or "ViT-B, COCO-171 bank"} ({d["name"]}, {S} -> {T})', '',
             f'{n_img} {d["name"]} images ({dropped} without a source-labelled sampled pixel excluded), {a.splits} random {n_cal}/{n_img-n_cal} splits. Sampled pixels: {100*frac["source"]:.1f}% carry a source label, {100*frac["added"]:.1f}% one of the {T-S} added labels ({d["fine"]} annotation, no source label), {100*result["pixel_fraction_a847_outside_vocab"]:.2f}% a {d["fine"]} label outside the {T} names (ignored); {result["images_with_added_pixels"]} images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all {T}-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at {T} labels. Development data; nothing fitted.', '']
    for alpha in ALPHAS:
        key = f'a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha}', '', f'| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at {T} |',
                  '|---|---:|---:|---:|---:|---:|---:|']
        gs = {arm: [] for arm in list(arms)+list(matched)}                # grid point per split, per arm
        for perm in perms:
            cal = perm[:n_cal]
            for arm, (cal_store, cal_pop, _) in arms.items(): gs[arm].append(pick(cal_store, cal_pop, cal, alpha))
            for arm, (store, ref) in matched.items(): gs[arm].append(match(store, cal, float(np.nanmean(size[arms[ref][2]][cal, gs[ref][-1]]))))
        for arm in gs:
            ev_store = arms[arm][2] if arm in arms else matched[arm][0]
            r = {p: [] for p in pops}; sz = []
            for perm, g in zip(perms, gs[arm]):
                ev = perm[n_cal:]
                for p in pops: r[p].append(mean_over(ev_store, p, ev, g)[0])
                sz.append(float(np.nanmean(size[ev_store][ev, g])))
            r = {p: np.array(v) for p, v in r.items()}; sz = np.array(sz)
            result['designs'][key][arm] = dict({f'risk_{p}': float(v.mean()) for p, v in r.items()},
                                               **{f'frac_above_{p}': float((v > alpha).mean()) for p, v in r.items()}, size_845=float(sz.mean()),
                                               **{f'risk_{p}_q025_q975': np.quantile(v, [.025, .975]).tolist() for p, v in r.items()})
            lines.append(f'| {arm} | {100*r["source"].mean():.2f} | {100*r["added"].mean():.2f} | {100*(r["added"] > alpha).mean():.1f} | {100*r["all"].mean():.2f} | {100*(r["all"] > alpha).mean():.1f} | {sz.mean():.2f} |')
        lines.append('')
    lines += ['The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold\'s (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_added_label_risk.py', 'src/exp_headroom_sets.py', f"{d['sclip']}/{d['gt_fine']}"]}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
