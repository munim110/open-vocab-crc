"""Segmentation accuracy split into source and added classes (post hoc addition; computed from stored confusion matrices).

The segmentation counterpart of the box-level split of exp_ovd_accuracy.py. The full-resolution runs of exp_miou_full.py /
exp_fcclip_miou.py store, per benchmark and arm, the confusion matrix over all annotated pixels (rows: ground truth,
columns: arg-max over the benchmark vocabulary). Here the classes of the large benchmarks are split into
  source  the classes of the small benchmark (A-150 inside A-847; PC-59 inside PC-459), and
  added   the remaining classes (697 on A-847; 399 on PC-459, where "unknown" is kept as a benchmark class, as in the
          released preparation, but belongs to neither group).
Reported per group: pixel accuracy (pooled over the group's pixels), class-mean accuracy and mIoU over the classes with
ground-truth pixels (detectron2 convention), and the group's share of annotated pixels. The prediction is always the
arg-max over the whole benchmark vocabulary; no model is run.

    PYTHONPATH=src python src/exp_seg_added_accuracy.py
"""
import hashlib
import json
from pathlib import Path

import numpy as np

from labels import load_150, load_847
import pascal_labels

LANES = ['vitb', 'vitl', 'declip', 'sed', 'fcclip']
OUT = Path('results/seg_added_accuracy')


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def groups(ds):
    """(source mask, added mask) over the benchmark classes."""
    if ds == 'ade847':
        c847 = load_847(); by_name = {c['name']: c for c in c847}
        manual = {'door, double door': 'door', 'crt screen': 'screen, crt screen'}  # as in vocab.build_configs
        idx = np.array([(by_name.get(n) or by_name[manual[n]])['trainId'] for n in load_150()])
        n, other = 847, []
    else:
        idx = pascal_labels.map59_459()
        n, other = 459, [pascal_labels.load_459().index('unknown')]
    src = np.zeros(n, bool); src[idx] = True
    add = ~src; add[other] = False
    assert len(set(idx.tolist())) == len(idx)
    return src, add


def stats(C, sel):
    row, col, d = C.sum(1), C.sum(0), np.diag(C)
    pres = sel & (row > 0)
    return dict(classes=int(sel.sum()), classes_present=int(pres.sum()),
                pixel_accuracy=float(d[sel].sum()/row[sel].sum()),
                class_mean_accuracy=float((d[pres]/row[pres]).mean()),
                miou=float((d[pres]/(row[pres]+col[pres]-d[pres])).mean()),
                pixel_share=float(row[sel].sum()/row.sum()))


def main():
    res = dict(note='source/added split of the stored full-resolution confusion matrices; arg-max over the whole benchmark vocabulary',
               datasets={}, hashes={'src/exp_seg_added_accuracy.py': digest('src/exp_seg_added_accuracy.py')})
    for ds in ['ade847', 'pc459']:
        src, add = groups(ds)
        res['datasets'][ds] = dict(source_classes=int(src.sum()), added_classes=int(add.sum()), lanes={})
        for lane in LANES:
            run = Path(f'results/miou_full_{ds}_{lane}')
            z = np.load(run/'confusion.npz'); stored = json.loads((run/'results.json').read_text())['per_arm']
            arms = {}
            for arm in z.files:
                C = z[arm].astype(np.float64)
                tot = stats(C, np.ones(len(C), bool))
                assert abs(tot['pixel_accuracy']-stored[arm]['pixel_accuracy']) < 1e-6, (ds, lane, arm)  # stored in float32
                assert abs(tot['miou']-stored[arm]['miou']) < 1e-9, (ds, lane, arm, tot['miou'], stored[arm]['miou'])
                arms[arm] = dict(source=stats(C, src), added=stats(C, add))
                print(ds, lane, arm, f"src {100*arms[arm]['source']['pixel_accuracy']:.1f}",
                      f"add {100*arms[arm]['added']['pixel_accuracy']:.1f} / {100*arms[arm]['added']['miou']:.1f}", flush=True)
            res['datasets'][ds]['lanes'][lane] = arms
            res['hashes'][str(run/'confusion.npz')] = digest(run/'confusion.npz')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(res, indent=2))


if __name__ == '__main__':
    main()
