"""Conditional (stratified) risk under the source-calibrated threshold, on the stored headroom-probe scores.

Image-level CRC controls the marginal mean of the image loss. This script reports what the same thresholds do
inside strata that the guarantee does not cover, for the frozen anchored threshold, the frozen native threshold,
native recalibrated on the grown vocabulary, and native at the source vocabulary (the pre-growth profile):
  * per source class: pixel-pooled miss rate over evaluation images, the macro (class-mean) risk, the worst class,
    the number of classes above 2*alpha, and the risk of the frequent / medium / rare thirds of the classes (by
    pixel count);
  * per scene (ADE only, sceneCategories.txt): image-level risk in scenes with at least MIN_SCENE kept images;
  * per image: quantiles of the image loss and the fraction of images losing more than 25% / 50% of their pixels;
  * by the number of distinct source labels in the image.
Same stores, exclusion and 500 half/half splits as exp_added_label_risk.py. Nothing is fitted.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_splits import curves
from headroom_scores import ALPHAS, LOGIT_GRID, Probe, crc_pick

MIN_SCENE = 20
LABEL_BINS = [(1, 3), (4, 6), (7, 10), (11, 10**6)]
# arm -> (calibration store, evaluation store)
ARMS = dict(native_source=('native_source', 'native_source'), native_frozen=('native_source', 'native_full'),
            native_replay=('native_full', 'native_full'), anchored_frozen=('anchored_full', 'anchored_full'))


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade')
    ap.add_argument('--tag', default='')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    P = Probe(a.dataset, a.tag)
    OUT = Path(f'results/conditional_risk_{a.dataset}{P.suffix}'); OUT.mkdir(parents=True, exist_ok=True)
    S, grid_np = P.S, LOGIT_GRID; grid = torch.from_numpy(grid_np).to(P.dev)
    gt = torch.from_numpy(P.gt.astype(np.int64)).to(P.dev)
    valid = gt < S
    # true-class score per pixel [N, P] (nan where unlabelled) and image loss curves [N, G] per store
    U, L = {}, {}
    for store in ('native_source', 'native_full', 'anchored_full'):
        u, l = [], []
        for j in range(P.n_img):
            s = P.scores(store, j)
            t = s.gather(1, gt[j].clamp(max=S-1)[:, None])[:, 0]
            u.append(torch.where(valid[j], t, torch.full_like(t, float('nan'))).float())
            l.append(curves(s, gt[j], grid, S, [S])[0])
        U[store] = torch.stack(u); L[store] = np.stack(l)
        print(store, 'loaded', flush=True)
    # per-image per-class pixel counts [N, S]
    cls = torch.where(valid, gt, torch.full_like(gt, S))
    count = torch.stack([torch.bincount(c, minlength=S+1)[:S] for c in cls]).double()          # [N, S]
    n_labels = (count > 0).sum(1).cpu().numpy()
    tot = count.sum(0).cpu().numpy(); order = np.argsort(-tot); thirds = np.array_split(order, 3)   # frequent, medium, rare
    scenes = P.scenes(); scene_names = None
    if scenes is not None:
        scenes = np.array(scenes); names_, cnt = np.unique(scenes, return_counts=True)
        scene_names = [n for n, c in zip(names_, cnt) if c >= MIN_SCENE]
    perms = P.splits(a.splits); n_cal = P.n_cal
    result = dict(config=P.config, dataset=a.dataset, images=P.n_img, excluded_images=P.dropped, splits=a.splits, alphas=ALPHAS,
                  class_names=P.class_names, class_pixels=tot.tolist(), thirds=[t.tolist() for t in thirds], scene_min_images=MIN_SCENE,
                  scenes=scene_names, label_bins=LABEL_BINS, designs={})
    lines = [f'# Conditional risk under source-calibrated thresholds: {P.config}', '', P.describe(a.splits),
             'The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).', '']
    for alpha in ALPHAS:
        key = f'a{alpha}'; result['designs'][key] = {}
        lines += [f'## alpha = {alpha}', '',
                  '| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | '
                  + ('Worst scene (%) | Scenes > 2 alpha | ' if scene_names else '') + 'Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | '
                  + ' | '.join(f'{lo}-{hi if hi < 10**6 else ""} labels (%)' for lo, hi in LABEL_BINS)+' |',
                  '|---|'+'---:|'*(11+(2 if scene_names else 0)+len(LABEL_BINS))]
        for arm, (cal_store, ev_store) in ARMS.items():
            gs = [crc_pick(L[cal_store], perm[:n_cal], alpha) for perm in perms]
            miss_cache = {}
            acc = dict(marginal=[], macro=[], worst=[], n_over=[], thirds=[], scene=[], q=[], over25=[], over50=[], bins=[], per_class=[])
            for perm, g in zip(perms, gs):
                ev = perm[n_cal:]; ev_t = torch.from_numpy(ev).to(P.dev)
                if g not in miss_cache:
                    miss = (U[ev_store] < grid[g]) & valid                                              # [N, P]
                    flat = (torch.arange(P.n_img, device=P.dev)[:, None]*(S+1)+cls)[miss]
                    miss_cache[g] = torch.bincount(flat, minlength=P.n_img*(S+1)).reshape(P.n_img, S+1)[:, :S].double()
                mc = miss_cache[g][ev_t].sum(0).cpu().numpy(); ct = count[ev_t].sum(0).cpu().numpy()
                with np.errstate(invalid='ignore', divide='ignore'):
                    pc = mc/ct                                                                          # per-class risk (nan: class absent)
                acc['per_class'].append(pc)
                acc['macro'].append(np.nanmean(pc)); acc['worst'].append(np.nanmax(pc)); acc['n_over'].append(int(np.nansum(pc > 2*alpha)))
                acc['thirds'].append([mc[t].sum()/ct[t].sum() for t in thirds])
                li = L[ev_store][ev, g]
                acc['marginal'].append(li.mean()); acc['q'].append(np.quantile(li, .9))
                acc['over25'].append((li > .25).mean()); acc['over50'].append((li > .5).mean())
                acc['bins'].append([li[(n_labels[ev] >= lo) & (n_labels[ev] <= hi)].mean() if ((n_labels[ev] >= lo) & (n_labels[ev] <= hi)).any() else np.nan for lo, hi in LABEL_BINS])
                if scene_names:
                    sc = scenes[ev]
                    acc['scene'].append([li[sc == s].mean() if (sc == s).any() else np.nan for s in scene_names])
            per_class = np.nanmean(np.stack(acc['per_class']), 0)
            row = dict(marginal=float(np.mean(acc['marginal'])), macro=float(np.mean(acc['macro'])), worst_class=float(np.mean(acc['worst'])),
                       classes_over_2alpha=float(np.mean(acc['n_over'])), thirds=np.mean(acc['thirds'], 0).tolist(),
                       images_over_25=float(np.mean(acc['over25'])), images_over_50=float(np.mean(acc['over50'])), image_loss_q90=float(np.mean(acc['q'])),
                       label_bins=np.nanmean(np.array(acc['bins'], dtype=float), 0).tolist(), per_class=per_class.tolist(),
                       worst_classes=[(P.class_names[i], float(per_class[i])) for i in np.argsort(-np.nan_to_num(per_class))[:10]])
            if scene_names:
                ps = np.nanmean(np.array(acc['scene'], dtype=float), 0)
                row.update(per_scene=ps.tolist(), worst_scene=float(np.nanmax(ps)), scenes_over_2alpha=int(np.nansum(ps > 2*alpha)),
                           worst_scenes=[(scene_names[i], float(ps[i])) for i in np.argsort(-np.nan_to_num(ps))[:5]])
            result['designs'][key][arm] = row
            cells = [f'{100*row["marginal"]:.2f}', f'{100*row["macro"]:.2f}', f'{100*row["worst_class"]:.1f}', f'{row["classes_over_2alpha"]:.1f}'] + [f'{100*v:.2f}' for v in row['thirds']]
            if scene_names: cells += [f'{100*row["worst_scene"]:.1f}', f'{row["scenes_over_2alpha"]}']
            cells += [f'{100*row["images_over_25"]:.1f}', f'{100*row["images_over_50"]:.1f}', f'{100*row["image_loss_q90"]:.1f}'] + [f'{100*v:.2f}' for v in row['label_bins']]
            lines.append(f'| {arm} | '+' | '.join(cells)+' |')
        lines.append('')
        lines += ['Worst classes (pixel-pooled miss rate, %):', '']
        for arm in ARMS:
            lines.append(f'- {arm}: '+', '.join(f'{n} {100*v:.0f}' for n, v in result['designs'][key][arm]['worst_classes']))
        if scene_names:
            lines += ['', 'Worst scenes (image-level risk, %):', '']
            for arm in ARMS:
                lines.append(f'- {arm}: '+', '.join(f'{n} {100*v:.0f}' for n, v in result['designs'][key][arm]['worst_scenes']))
        lines.append('')
    lines += [f'Classes are split into thirds by total sampled-pixel count (frequent third: {", ".join(P.class_names[i] for i in thirds[0][:5])}, ...; rare third: {", ".join(P.class_names[i] for i in thirds[2][-5:])}, ...). '
              + (f'Scenes with at least {MIN_SCENE} kept images: {len(scene_names)}. ' if scene_names else '')
              + 'native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_conditional_risk.py', 'src/headroom_scores.py', 'src/exp_headroom_splits.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
