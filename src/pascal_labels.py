"""Vocabulary and label spaces for Pascal Context 59 / 459.

Both label spaces come from a *single* annotation source: the 459-class
`trainval/*.mat` LabelMap released by Mottaghi et al.  The official 59-class
vocabulary is a curated subset of the 459 names (verified below: every one of the
59 strings occurs verbatim in the 459 list), so the coarse map is the fine map
restricted to those indices.

This differs from ADE20K-150 / ADE20K-847, where the two label spaces are two
separate annotation files that agree on 99.5% of jointly-labelled pixels but not
100%.  The consequence is recorded in the pre-registration addendum: on Pascal the
carrier of a calibration class under the fine vocabulary is exactly itself, so the
granularity regime cannot test the carrier assumption here.

`unknown` is one of the 459 names and denotes unlabelled pixels, not a class; it
is mapped to ignore in both spaces.
"""
import os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PC = os.path.join(ROOT, 'data/pascal')
VOC = os.path.join(PC, 'VOCdevkit/VOC2010')
IGN = 65535


def _read(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        i, n = line.split(':', 1)
        d[int(i)] = n.strip()
    return d


def load_459():
    d = _read(os.path.join(PC, 'labels.txt'))
    assert len(d) == 459 and set(d) == set(range(1, 460))
    return [d[i] for i in range(1, 460)]


def load_59():
    d = _read(os.path.join(PC, '59_labels.txt'))
    assert len(d) == 59 and set(d) == set(range(1, 60))
    return [d[i] for i in range(1, 60)]


def index_maps():
    """Return (idx59_to_459, unknown_id) with 459 ids 1-based as stored in the .mat."""
    n459, n59 = load_459(), load_59()
    inv = {n: i + 1 for i, n in enumerate(n459)}
    assert len(inv) == 459, 'duplicate name in the 459 list'
    missing = [n for n in n59 if n not in inv]
    assert not missing, missing
    return np.array([inv[n] for n in n59], np.int64), inv['unknown']


def luts():
    """Lookup tables from the raw .mat value to (coarse, fine) train ids.

    Coarse: 0..58 for the 59 official classes, IGN elsewhere.
    Fine:   0..458 for the 459 classes except `unknown`, IGN for `unknown`.
    """
    m59, unk = index_maps()
    coarse = np.full(512, IGN, np.uint16)
    coarse[m59] = np.arange(59, dtype=np.uint16)
    coarse[unk] = IGN
    fine = np.full(512, IGN, np.uint16)
    fine[1:460] = np.arange(459, dtype=np.uint16)
    fine[unk] = IGN
    return coarse, fine


def map59_459():
    """Index in the 459 vocabulary of each of the 59 calibration classes (0-based)."""
    m59, _ = index_maps()
    return m59 - 1


def val_files(limit=0):
    files = [l.strip() for l in open(os.path.join(VOC, 'ImageSets/Main/val.txt')) if l.strip()]
    files = sorted(files)
    return files[:limit] if limit else files


if __name__ == '__main__':
    n459, n59 = load_459(), load_59()
    m = map59_459()
    print(f'459: {len(n459)}  59: {len(n59)}  val images: {len(val_files())}')
    print('59 subset of 459 by string:', all(n in set(n459) for n in n59))
    print('carrier identity check:', all(n459[m[i]] == n59[i] for i in range(59)))
    print('first 8 pairs:', [(n59[i], m[i], n459[m[i]]) for i in range(8)])
