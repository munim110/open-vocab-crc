"""Decode ADE20K-full val segmentations -> A-847 label maps on the A-150 pixel grid.

Also records agreement between A-150 GT and the A-847 GT mapped back to 150,
which quantifies annotation-level consistency between the two label spaces.
"""
import os, sys, io, json
import numpy as np, pyarrow.parquet as pq
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import load_847, load_150, first_syn, ROOT

OUT = os.path.join(ROOT, 'data/gt847')
ADE = os.path.join(ROOT, 'data/ADEChallengeData2016')
IGN = 65535

def build_maps():
    c847, n150 = load_847(), load_150()
    by_name = {c['name']: c for c in c847}
    by_first = {}
    for c in c847: by_first.setdefault(first_syn(c['name']), []).append(c)
    manual = {'door, double door': 'door', 'crt screen': 'screen, crt screen'}
    m150_to_847 = {}
    for i, n in enumerate(n150):
        c = by_name.get(n) or by_name.get(manual.get(n, '\0'))
        assert c is not None, n
        m150_to_847[i] = c['trainId']
    nameidx_to_train = {c['id']: c['trainId'] for c in c847}
    return m150_to_847, nameidx_to_train

def main():
    os.makedirs(OUT, exist_ok=True)
    m150_847, ndx2train = build_maps()
    lut = np.full(4096, IGN, np.uint16)
    for ndx, t in ndx2train.items():
        if ndx < 4096: lut[ndx] = t
    f = pq.ParquetFile(os.path.join(ROOT, 'data/ade_full_val.parquet'))
    stats = dict(n=0, agree=0, total=0, gt150_valid=0, gt847_valid=0, both_valid=0)
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=['filename', 'segmentations'])
        for i in range(t.num_rows):
            fn = t.column('filename')[i].as_py()
            seg = np.array(Image.open(io.BytesIO(t.column('segmentations')[i].as_py()[0]['bytes'])))
            ndx = (seg[:, :, 0].astype(np.int32) // 10) * 256 + seg[:, :, 1].astype(np.int32)
            g847 = lut[np.clip(ndx, 0, 4095)]
            g847[ndx >= 4096] = IGN
            g150 = np.array(Image.open(os.path.join(ADE, 'annotations/validation', fn.replace('.jpg', '.png'))))
            if g847.shape != g150.shape:
                g847 = np.array(Image.fromarray(g847).resize((g150.shape[1], g150.shape[0]), Image.NEAREST))
            np.save(os.path.join(OUT, fn.replace('.jpg', '.npy')), g847)
            # diagnostic: A-150 label (1..150, 0=ignore) mapped into 847 vs decoded 847
            v150 = g150 > 0
            mapped = np.full(g150.shape, IGN, np.uint16)
            idx = np.where(v150)
            mapped[idx] = np.array([m150_847[c - 1] for c in g150[idx]], np.uint16) if idx[0].size else 0
            both = v150 & (g847 != IGN)
            stats['n'] += 1
            stats['total'] += g150.size
            stats['gt150_valid'] += int(v150.sum())
            stats['gt847_valid'] += int((g847 != IGN).sum())
            stats['both_valid'] += int(both.sum())
            stats['agree'] += int((mapped[both] == g847[both]).sum())
        print(f'rg {rg+1}/{f.num_row_groups} done n={stats["n"]}', flush=True)
    stats['agreement_rate'] = stats['agree'] / max(stats['both_valid'], 1)
    stats['gt150_valid_frac'] = stats['gt150_valid'] / stats['total']
    stats['gt847_valid_frac'] = stats['gt847_valid'] / stats['total']
    json.dump(stats, open(os.path.join(ROOT, 'meta/gt847_stats.json'), 'w'), indent=2)
    print(json.dumps(stats, indent=2))

if __name__ == '__main__':
    main()
