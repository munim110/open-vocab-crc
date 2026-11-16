"""Box-level accuracy of the stored detector scores (post hoc addition, see the Deviations of docs/OVD_DETECTION_BENCHMARK.md).

The detection counterpart of the pixel accuracy of the segmentation experiments: at every ground-truth box, the label with
the largest box-level score (exp_ovd_probe.box_scores: max logit over predicted boxes with IoU >= 0.5) over all 1,204
names is compared with the true label. Computed from the stored scores; no model is run.

Reported per store (deployed at all 1,204 names: native in chunks of 40, anchored with bank A or B, OWLv2), separately for
source (COCO) and added (LVIS) boxes:
  localised   fraction of boxes that some predicted box overlaps (score > -30 for the true label);
  top-1/top-5 fraction of boxes whose true label ranks first / within the first five. Ties count against the true label
              (rank = number of other labels scoring >= the true label), so an unlocalised box (every label at -30) is wrong;
  top-1 | loc top-1 among localised boxes (classification given localisation);
  class mean  top-1 averaged over the labels present (each label weighted equally, as in mIoU).
Labels are not exhaustive in LVIS, so a box whose top label is a correct but unannotated name counts as wrong; this affects
every store alike.

    PYTHONPATH=src python src/exp_ovd_accuracy.py --model gdino_t
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

FLOOR = -30+1e-3


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rank_of_true(v, lab, block=2048):
    """Number of labels other than the true one scoring >= the true label, per box (float16 store, compared exactly)."""
    out = np.empty(len(lab), np.int64)
    for s in range(0, len(lab), block):
        x = np.asarray(v[s:s+block], np.float32); y = lab[s:s+block]
        t = x[np.arange(len(y)), y]
        out[s:s+block] = (x >= t[:, None]).sum(1)-1
    return out


def summary(rank, loc, lab, mask):
    r, l, y = rank[mask], loc[mask], lab[mask]
    top1 = r == 0
    present = np.unique(y)
    return dict(boxes=int(mask.sum()), labels=int(len(present)),
                localised=float(l.mean()), top1=float(top1.mean()), top5=float((r < 5).mean()),
                top1_given_localised=float(top1[l].mean()) if l.any() else 0.0,
                class_mean_top1=float(np.mean([top1[y == c].mean() for c in present])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    a = ap.parse_args()
    STORE = Path(f'cache/ovd_probe_{a.model}'); proto = json.loads(Path(f'results/ovd_probe_{a.model}/protocol.json').read_text())
    gt = np.load(STORE/'gt.npz'); lab, src = gt['labels'], gt['source'].astype(bool)
    L = proto['labels']
    stores = ['owl'] if a.model == 'owlv2' else ['native_lvis', 'anch_a', 'anch_b']
    res = dict(model=a.model, labels=L, source_labels=proto['source_labels'], stores={})
    for k in stores:
        v = np.load(STORE/f'{k}.npy', mmap_mode='r'); assert v.shape == (len(lab), L), (k, v.shape)
        loc = np.asarray(v[np.arange(len(lab)), lab], np.float32) > FLOOR
        rank = rank_of_true(v, lab)
        res['stores'][k] = dict(source=summary(rank, loc, lab, src), added=summary(rank, loc, lab, ~src))
        print(k, json.dumps(res['stores'][k]), flush=True)
    res['hashes'] = {p: digest(p) for p in ['src/exp_ovd_accuracy.py', str(STORE/'gt.npz')]}
    OUT = Path(f'results/ovd_accuracy_{a.model}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(res, indent=2))


if __name__ == '__main__':
    main()
