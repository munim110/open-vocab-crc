"""A-847 ground truth at the stored sampled pixels of the reserve (docs/PROTOCOL_ADDED_LABEL_RESERVE.md).

The first reserve read (exp_confirm_reserve.py) stored scores and the A-150 label of 4,096 sampled pixels per reserved
ADE training image (seed = reserve seed + index, drawn on the A-150 annotation grid). This script adds the A-847 label of
the same pixels, decoded from the ADE20K-full (2021_17_01) parquet export exactly as build_gt.py decodes the validation
split, and runs the protocol's integrity checks:
  C1  every requested filename is in the parquet's filename column (only that column is read);
  C2  the A-150 annotation re-sampled at the regenerated pixels equals the stored gt150.npy;
  C3  on sampled pixels labelled in both, A-150 mapped into A-847 agrees with the decoded A-847 label at >= 0.98;
  C4  share of sampled pixels with an A-847 label outside the A-150 classes (reported).
gt847.npy is written only if C1-C3 pass. Modes:
  --dev          validation parquet, development pixel sample (cache/sclip/meta.json); must equal cache/sclip/gt847.npy
  --smoke        the first 40 validation images with the reserve seed, as exp_confirm_reserve.py --smoke 40 sampled them;
                 writes cache/confirmation_vitl_bank683_smoke/gt847.npy (the reserve code path on validation images)
  --filenames    C1 on the reserve against the training shards (no annotation content read)
  --reserve-read the protocol's read: writes cache/confirmation_vitl_bank683/{gt847.npy,gt_checks.json}

    PYTHONPATH=src python src/build_gt_reserve.py --dev
    PYTHONPATH=src python src/build_gt_reserve.py --smoke
    PYTHONPATH=src python src/build_gt_reserve.py --filenames
    PYTHONPATH=src python src/build_gt_reserve.py --reserve-read
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from PIL import Image

from build_gt import IGN, build_maps

ADE = Path('data/ADEChallengeData2016')
VAL_PARQUET = [Path('data/ade_full_val.parquet')]
TRAIN_PARQUET = sorted(Path('data/ade_full_train').glob('train-*-of-00010.parquet'))
RESERVE = Path('meta/ade_confirmation_reserve_v1.json')
NPIX = 4096
MIN_AGREEMENT = 0.98


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    return h.hexdigest()


def locate(shards, names):
    """(shard, row group, row) of every requested filename; only the filename column is read (C1)."""
    where = {}
    for s in shards:
        f = pq.ParquetFile(s)
        for rg in range(f.num_row_groups):
            for i, fn in enumerate(f.read_row_group(rg, columns=['filename']).column('filename').to_pylist()):
                if fn in names: where[fn] = (s, rg, i)
    return where


def decode(seg_bytes, lut, shape):
    """A-847 train ids on the A-150 grid, as build_gt.py (IGN: none)."""
    seg = np.array(Image.open(io.BytesIO(seg_bytes)))
    ndx = (seg[:, :, 0].astype(np.int32) // 10) * 256 + seg[:, :, 1].astype(np.int32)
    g = lut[np.clip(ndx, 0, 4095)]
    g[ndx >= 4096] = IGN
    if g.shape != shape:
        g = np.array(Image.fromarray(g).resize((shape[1], shape[0]), Image.NEAREST))
    return g


def build(files, split, seeds, shards):
    """gt150 [N, NPIX] (0..149, 255 none), gt847 [N, NPIX] (A-847 train id, IGN none) at the sampled pixels, and C1."""
    m150_847, ndx2train = build_maps()
    lut = np.full(4096, IGN, np.uint16)
    for ndx, t in ndx2train.items():
        if ndx < 4096: lut[ndx] = t
    names = [f.name for f in files]
    where = locate(shards, set(names))
    missing = [n for n in names if n not in where]
    g150 = np.full((len(files), NPIX), 255, np.uint8)
    g847 = np.full((len(files), NPIX), IGN, np.uint16)
    if missing: return g150, g847, missing, m150_847
    by_group = {}
    for k, n in enumerate(names): by_group.setdefault(where[n][:2], []).append((where[n][2], k))
    for (s, rg), rows in sorted(by_group.items()):
        col = pq.ParquetFile(s).read_row_group(rg, columns=['segmentations']).column('segmentations')
        for i, k in rows:
            lab = np.array(Image.open(ADE/'annotations'/split/names[k].replace('.jpg', '.png')))
            H, W = lab.shape
            flat = np.random.default_rng(seeds[k]).choice(H*W, NPIX, replace=False)
            g150[k] = np.where(lab.ravel()[flat] > 0, lab.ravel()[flat].astype(int)-1, 255)
            g847[k] = decode(col[i].as_py()[0]['bytes'], lut, (H, W)).ravel()[flat]
        print(f'{s.name} row group {rg}: {len(rows)} files', flush=True)
    return g150, g847, missing, m150_847


def checks(g150, g847, stored150, missing, m150_847):
    both = (g150 < 150) & (g847 != IGN)
    mapped = np.array([m150_847[c] for c in range(150)], np.uint16)
    agree = float((mapped[g150[both]] == g847[both]).mean()) if both.any() else float('nan')
    added = (g847 != IGN) & (g150 >= 150)
    return dict(C1_missing=missing, C1_pass=not missing, C2_pass=bool(np.array_equal(g150, stored150)),
                C3_agreement=agree, C3_pass=bool(agree >= MIN_AGREEMENT), C4_fine_only_frac=float(added.mean()),
                C4_fine_frac=float((g847 != IGN).mean()), pixels=int(g150.size))


def main():
    ap = argparse.ArgumentParser()
    m = ap.add_mutually_exclusive_group(required=True)
    for k in ['--dev', '--smoke', '--filenames', '--reserve-read']: m.add_argument(k, action='store_true')
    a = ap.parse_args()
    if a.dev:
        meta = json.loads(Path('cache/sclip/meta.json').read_text())
        files = [ADE/'images/validation'/r['file'] for r in meta['meta']]
        g150, g847, missing, m = build(files, 'validation', [meta['pixseed']+i for i in range(len(files))], VAL_PARQUET)
        c = checks(g150, g847, np.load('cache/sclip/gt150.npy'), missing, m)
        c['dev_gt847_equal'] = bool(np.array_equal(g847, np.load('cache/sclip/gt847.npy')))
        print(json.dumps(c, indent=2))
        return
    reserve = json.loads(RESERVE.read_text())
    if a.filenames:
        names = [Path(f.replace('\\', '/')).name for f in reserve['files']]
        where = locate(TRAIN_PARQUET, set(names))
        missing = [n for n in names if n not in where]
        out = dict(C1_pass=not missing, C1_missing=missing, requested=len(names), shards={s.name: sha256(s) for s in TRAIN_PARQUET})
        Path('results/reserve_filenames_check.json').write_text(json.dumps(out, indent=2))
        print(json.dumps(dict(out, shards=len(out['shards'])), indent=2))
        return
    if a.smoke:
        files = sorted((ADE/'images/validation').glob('*.jpg'))[:40]
        split, shards, store = 'validation', VAL_PARQUET, Path('cache/confirmation_vitl_bank683_smoke')
    else:
        files = [Path(f.replace('\\', '/')) for f in reserve['files']]
        split, shards, store = 'training', TRAIN_PARQUET, Path('cache/confirmation_vitl_bank683')
        assert len(shards) == 10, 'training shards missing'
    g150, g847, missing, m = build(files, split, [reserve['seed']+k for k in range(len(files))], shards)
    c = checks(g150, g847, np.load(store/'gt150.npy'), missing, m)
    c['shards'] = {s.name: sha256(s) for s in shards}
    c['hashes'] = {p: sha256(p) for p in ['src/build_gt_reserve.py', 'src/build_gt.py', str(RESERVE), 'docs/PROTOCOL_ADDED_LABEL_RESERVE.md']}
    (store/'gt_checks.json').write_text(json.dumps(c, indent=2))
    print(json.dumps(dict(c, shards=len(c['shards'])), indent=2))
    if c['C1_pass'] and c['C2_pass'] and c['C3_pass']:
        np.save(store/'gt847.npy', g847)
        print('CHECKS PASSED; wrote', store/'gt847.npy')
    else:
        raise SystemExit('CHECKS FAILED; gt847.npy not written (protocol: stop)')


if __name__ == '__main__':
    main()
