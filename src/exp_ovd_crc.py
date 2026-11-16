"""CRC on the stored box-level detector scores (exp_ovd_probe.py; docs/OVD_DETECTION_BENCHMARK.md).

Image-level CRC (Sec. 3.1): the loss of an image is the fraction of its source-class (COCO-80) ground-truth boxes whose
true label scores below t; images without a source box are excluded. 500 random half/half splits, alpha in {.10, .05},
the logit grid of the segmentation experiments. Arms (threshold calibrated on the calibration half, risk and set size on
the other half):
  native, source         calibrated and deployed with the 80-name prompt (reference);
  native reused, one     calibrated with the 80-name prompt, deployed with the extended 256-token prompt;
  native reused, LVIS    calibrated with the 80-name prompt, deployed with all names in chunks of 40;
  native recal., one/LVIS calibrated and deployed at the grown vocabulary;
  anchored A/B           calibrated once; candidate-independent, so the source-box loss is the same at every vocabulary;
  OWLv2                  candidate-independent by construction.
Set size = mean over the held-out source boxes of the number of labels scoring >= t at the deployed vocabulary.

Label-level CRC (prop:labels, prop:newimages) for anchored A and native recalibrated at LVIS scale: labels are the units;
a label's loss is the pooled fraction of its ground-truth boxes (COCO for the 80 source names, LVIS for the added ones)
missed in the calibration images, or the image-averaged fraction. Designs: exchangeable (a random 80 of the 1,204 names,
fresh per trial, with a fresh image split) and the benchmark's own split (source = COCO 80), with the decomposition of
prop:shift. Added-label risk on the calibration and the held-out images, % of trials above alpha.

    PYTHONPATH=src python src/exp_ovd_crc.py --model gdino_t
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ALPHAS = [.1, .05]
GRID = np.arange(-30, 30+1e-9, 1/64)            # LOGIT_GRID of exp_headroom_sets.py
G = len(GRID)


def first_miss(s):
    """Grid index from which a score s is missed (s < GRID[j] for j >= index)."""
    return np.searchsorted(GRID, s.astype(np.float64), side='right')


def crc(loss, alpha):
    ok = np.nonzero((loss.sum(0)+1)/(len(loss)+1) <= alpha)[0]
    return int(ok[-1]) if len(ok) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--trials', type=int, default=500)
    a = ap.parse_args()
    STORE = Path(f'cache/ovd_probe_{a.model}'); proto = json.loads(Path(f'results/ovd_probe_{a.model}/protocol.json').read_text())
    gt = np.load(STORE/'gt.npz'); lab, src, offs = gt['labels'], gt['source'], gt['offsets']
    n_img = len(offs)-1; S, L = proto['source_labels'], proto['labels']
    img_of = np.repeat(np.arange(n_img), np.diff(offs))
    arms = {k: np.load(STORE/f'{k}.npy', mmap_mode='r') for k in proto['arms']}
    true = {k: np.asarray(v[np.arange(len(lab)), np.minimum(lab, v.shape[1]-1)], np.float32) for k, v in arms.items()}
    # per image: source-box miss curve [n_img, G] and number of source boxes
    nsrc = np.bincount(img_of[src], minlength=n_img).astype(float); keep = nsrc > 0

    def image_loss(k):
        fm = first_miss(true[k][src]); m = np.zeros((n_img, G+1))
        np.add.at(m, (img_of[src], fm), 1)
        return (np.cumsum(m, 1)[:, :G]/np.maximum(nsrc, 1)[:, None])[keep]

    def size_curve(k, cols):
        """Mean over an image's source boxes of # labels (among cols) scoring >= GRID[j] [n_img(keep), G]."""
        sc = np.sort(np.asarray(arms[k][np.flatnonzero(src)][:, :cols], np.float32), 1)
        cnt = cols-np.stack([np.searchsorted(r, GRID, side='left') for r in sc])
        out = np.zeros((n_img, G)); np.add.at(out, img_of[src], cnt)
        return (out/np.maximum(nsrc, 1)[:, None])[keep]

    one, grown = proto['arms'].get('native_one'), L
    if a.model == 'owlv2':
        plan = {'OWLv2': ('owl', 'owl', [(S, 'source'), (grown, 'LVIS')])}
    else:
        plan = {'native, source': ('native_src', 'native_src', [(S, 'source')]),
                'native reused, one prompt': ('native_src', 'native_one', [(one, 'one prompt')]),
                'native reused, LVIS': ('native_src', 'native_lvis', [(grown, 'LVIS')]),
                'native recal., one prompt': ('native_one', 'native_one', [(one, 'one prompt')]),
                'native recal., LVIS': ('native_lvis', 'native_lvis', [(grown, 'LVIS')]),
                'anchored A': ('anch_a', 'anch_a', [(S, 'source'), (one, 'one prompt'), (grown, 'LVIS')]),
                'anchored B': ('anch_b', 'anch_b', [(S, 'source'), (one, 'one prompt'), (grown, 'LVIS')])}
    losses = {k: image_loss(k) for k in arms}
    sizes = {(k, c): size_curve(k, c) for _, (_, k, vs) in plan.items() for c, _ in vs}
    n = int(keep.sum()); rng = np.random.default_rng(20260925)
    perms = [rng.permutation(n) for _ in range(a.trials)]
    res = dict(model=a.model, images=n, source_boxes=int(src[np.isin(img_of, np.flatnonzero(keep))].sum()), trials=a.trials,
               one_prompt_labels=one, labels=L, image_level={}, label_level={})
    lines = [f'# Detection, image-level CRC ({a.model}, {n} images with a source box, {a.trials} splits)', '',
             '| alpha | arm | risk % | splits > alpha % | set size (vocabulary) |', '|---|---|---:|---:|---|']
    for alpha in ALPHAS:
        for arm, (cal_k, dep_k, vs) in plan.items():
            r, sz = [], {v: [] for _, v in vs}
            for p in perms:
                c, e = p[:n//2], p[n//2:]
                t = crc(losses[cal_k][c], alpha)
                r.append(losses[dep_k][e, t].mean())
                for cols, v in vs: sz[v].append(sizes[dep_k, cols][e, t].mean())
            r = np.array(r)
            d = dict(risk=float(r.mean()), above=float((r > alpha).mean()), size={v: float(np.mean(x)) for v, x in sz.items()})
            res['image_level'].setdefault(str(alpha), {})[arm] = d
            lines.append(f'| {alpha} | {arm} | {100*d["risk"]:.2f} | {100*d["above"]:.0f} | ' + ', '.join(f'{x:.2f} ({v})' for v, x in d['size'].items()) + ' |')

    # label level
    lines += ['', '# Label-level CRC (labels as units)', '', '| alpha | design | store | loss | added, cal | added, held-out | trials > alpha (cal / held-out) | src at t | Delta(t) |',
              '|---|---|---|---|---:|---:|---:|---:|---:|']
    lab_stores = ['owl'] if a.model == 'owlv2' else ['anch_a', 'native_lvis']
    rng2 = np.random.default_rng(20260926)
    trials = [(rng2.permutation(n_img), np.sort(rng2.choice(L, S, replace=False))) for _ in range(a.trials)]
    for k in lab_stores:
        fm = first_miss(true[k])                                   # every box, own label
        pair = img_of*L+lab; up, inv = np.unique(pair, return_inverse=True)
        pimg, plab = up//L, up % L
        pm = np.zeros((len(up), G+1)); np.add.at(pm, (inv, fm), 1)
        pn = np.bincount(inv).astype(float); pmiss = np.cumsum(pm, 1)[:, :G]
        pfrac = pmiss/pn[:, None]

        def label_loss(imgmask):
            sel = imgmask[pimg]
            pooled = np.zeros((L, G)); np.add.at(pooled, plab[sel], pmiss[sel]); den = np.bincount(plab[sel], weights=pn[sel], minlength=L)
            avg = np.zeros((L, G)); np.add.at(avg, plab[sel], pfrac[sel]); cnt = np.bincount(plab[sel], minlength=L)
            return dict(pooled=pooled/np.maximum(den, 1)[:, None], images=avg/np.maximum(cnt, 1)[:, None]), den > 0

        for design in ['exchangeable', 'benchmark split']:
            acc = {}
            for perm, rs in trials:
                cal = np.zeros(n_img, bool); cal[perm[:n_img//2]] = True
                srcm = np.zeros(L, bool); srcm[rs if design == 'exchangeable' else np.arange(S)] = True
                (lc, pc), (le, pe) = label_loss(cal), label_loss(~cal)
                for alpha in ALPHAS:
                    for loss in ['pooled', 'images']:
                        t = crc(lc[loss][pc & srcm], alpha)
                        acc.setdefault((alpha, loss), []).append((lc[loss][pc & ~srcm, t].mean(), le[loss][pe & ~srcm, t].mean(), lc[loss][pc & srcm, t].mean()))
            for (alpha, loss), v in acc.items():
                v = np.array(v); m = v.mean(0); ab = (v[:, :2] > alpha).mean(0)
                res['label_level'].setdefault(k, {}).setdefault(design, {}).setdefault(str(alpha), {})[loss] = dict(
                    added_cal=m[0], added_heldout=m[1], above_cal=ab[0], above_heldout=ab[1], source_cal_at_t=m[2], delta_at_t=m[0]-m[2])
                lines.append(f'| {alpha} | {design} | {k} | {loss} | {100*m[0]:.2f} | {100*m[1]:.2f} | {100*ab[0]:.0f} / {100*ab[1]:.0f} | {100*m[2]:.2f} | {100*(m[0]-m[2]):.2f} |')
    res['hashes'] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['src/exp_ovd_crc.py', 'src/exp_ovd_probe.py', str(STORE/'gt.npz')]}
    OUT = Path(f'results/ovd_crc_{a.model}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(res, indent=2, default=float)); (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
