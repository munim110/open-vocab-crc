"""Localisation floor of the detection experiments (diagnostic for exp_ovd_crc.py; post hoc, see the Deviations of
docs/OVD_DETECTION_BENCHMARK.md).

A ground-truth box that no predicted box overlaps with IoU >= 0.5 has box-level score -30 for every label, so only the
lowest grid point covers it. Reported per store: the fraction of source and added boxes so unlocalised, and, for the
label-level trials of exp_ovd_crc.py (same seed and draws), the fraction of trials in which the calibrated label-level
threshold is the lowest grid point (every label in the set), i.e. in which the unlocalised boxes of the calibration
labels alone exceed alpha. Label losses are monotone in the threshold, so this happens exactly when the loss at the
second grid point already fails the CRC condition.

    PYTHONPATH=src python src/exp_ovd_floor.py --model gdino_t
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from exp_ovd_crc import ALPHAS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--trials', type=int, default=500)
    a = ap.parse_args()
    STORE = Path(f'cache/ovd_probe_{a.model}'); proto = json.loads(Path(f'results/ovd_probe_{a.model}/protocol.json').read_text())
    gt = np.load(STORE/'gt.npz'); lab, src, offs = gt['labels'], gt['source'], gt['offsets']
    n_img = len(offs)-1; S, L = proto['source_labels'], proto['labels']
    img_of = np.repeat(np.arange(n_img), np.diff(offs))
    stores = ['owl'] if a.model == 'owlv2' else ['anch_a', 'native_lvis']
    # the label-level trials of exp_ovd_crc.py
    rng2 = np.random.default_rng(20260926)
    trials = [(rng2.permutation(n_img), np.sort(rng2.choice(L, S, replace=False))) for _ in range(a.trials)]
    res = dict(model=a.model, labels_present=int((np.bincount(lab, minlength=L) > 0).sum()), stores={})
    for k in stores:
        v = np.load(STORE/f'{k}.npy', mmap_mode='r')
        floor = np.asarray(v[np.arange(len(lab)), np.minimum(lab, v.shape[1]-1)], np.float32) <= -30+1e-3
        pair = img_of*L+lab; up, inv = np.unique(pair, return_inverse=True)
        pimg, plab = up//L, up % L
        pn = np.bincount(inv).astype(float); pmiss = np.bincount(inv, weights=floor.astype(float))
        trivial = {}
        for design in ['exchangeable', 'benchmark split']:
            for perm, rs in trials:
                cal = np.zeros(n_img, bool); cal[perm[:n_img//2]] = True; sel = cal[pimg]
                srcm = np.zeros(L, bool); srcm[rs if design == 'exchangeable' else np.arange(S)] = True
                den = np.bincount(plab[sel], weights=pn[sel], minlength=L); cnt = np.bincount(plab[sel], minlength=L)
                loss = dict(pooled=np.bincount(plab[sel], weights=pmiss[sel], minlength=L)/np.maximum(den, 1),
                            images=np.bincount(plab[sel], weights=(pmiss/pn)[sel], minlength=L)/np.maximum(cnt, 1))
                use = (den > 0) & srcm
                for alpha in ALPHAS:
                    for name, l in loss.items():
                        trivial.setdefault(f'{design}, {alpha}, {name}', []).append((l[use].sum()+1)/(use.sum()+1) > alpha)
        res['stores'][k] = dict(unlocalised_source=float(floor[src].mean()), unlocalised_added=float(floor[~src].mean()),
                                trivial_threshold={d: float(np.mean(x)) for d, x in trivial.items()})
    res['hashes'] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['src/exp_ovd_floor.py', 'src/exp_ovd_crc.py', str(STORE/'gt.npz')]}
    OUT = Path(f'results/ovd_floor_{a.model}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != 'hashes'}, indent=2))


if __name__ == '__main__':
    main()
