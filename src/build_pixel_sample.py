"""Ground truth at the fixed per-image pixel sample, without any model.

The stored-score analyses (exp_headroom_splits.py, headroom_scores.Probe, exp_added_label_risk.py) read the labels of
the 4,096 sampled pixels per image from cache/sclip/{gt150,gt847,meta.json} (ADE20K) and cache/pascal_sclip/{gt59,gt459,
meta.json} (Pascal Context). Those files were first written by the Stage-A encoders (encode.py, encode_pascal.py), which
also cache SCLIP features and so need a GPU and the SCLIP weights. The pixel sample itself depends only on the image
size and the seed (pixseed + image index), so this script rebuilds the same ground truth on a CPU from the datasets
alone. Its --check mode compares the result with existing files array for array.

    PYTHONPATH=src python src/build_pixel_sample.py --dataset ade [--check]
    PYTHONPATH=src python src/build_pixel_sample.py --dataset pascal [--check]
    PYTHONPATH=src python src/build_pixel_sample.py --dataset coco [--check]      # COCO-Stuff 171 + LVIS v1 (cache/coco_pixels)
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

from labels import ROOT

ADE = os.path.join(ROOT, 'data/ADEChallengeData2016')
GT847 = os.path.join(ROOT, 'data/gt847')
OUT = dict(ade='cache/sclip', pascal='cache/pascal_sclip', coco='cache/coco_pixels')
# meta.json fields the encoders wrote besides the image list; kept so the rebuilt file is interchangeable with theirs
ENCODER_FIELDS = dict(dim=512, backbone='sclip', short=336)


def sample(H, W, i, npix, pixseed):
    flat = np.random.default_rng(pixseed + i).choice(H * W, size=npix, replace=False)
    return flat // W, flat % W


def build_ade(npix, pixseed):
    files = sorted(os.listdir(os.path.join(ADE, 'images/validation')))
    g150 = np.zeros((len(files), npix), np.uint8)      # 0..149, 255 ignore
    g847 = np.zeros((len(files), npix), np.uint16)
    meta = []
    for i, fn in enumerate(files):
        W, H = Image.open(os.path.join(ADE, 'images/validation', fn)).size
        lab = np.array(Image.open(os.path.join(ADE, 'annotations/validation', fn.replace('.jpg', '.png'))))
        l847 = np.load(os.path.join(GT847, fn.replace('.jpg', '.npy')))
        ys, xs = sample(H, W, i, npix, pixseed)
        g = lab[ys, xs].astype(np.int32) - 1                   # reduce_zero_label
        g150[i] = np.where(g < 0, 255, g).astype(np.uint8)
        g847[i] = l847[ys, xs]
        meta.append(dict(file=fn, H=int(H), W=int(W)))
    return dict(gt150=g150, gt847=g847), dict(meta=meta, npix=npix, pixseed=pixseed)


def build_pascal(npix, pixseed, limit=2000):
    import scipy.io as sio
    import pascal_labels as PL
    files = PL.val_files(limit)
    coarse_lut, fine_lut = PL.luts()
    g59 = np.zeros((len(files), npix), np.uint16)
    g459 = np.zeros((len(files), npix), np.uint16)
    meta, nval = [], dict(c=0, f=0, tot=0)
    for i, fn in enumerate(files):
        W, H = Image.open(os.path.join(PL.VOC, 'JPEGImages', fn + '.jpg')).size
        lab = sio.loadmat(os.path.join(PL.PC, 'trainval', fn + '.mat'))['LabelMap']
        assert lab.shape == (H, W), (fn, lab.shape, (H, W))
        ys, xs = sample(H, W, i, npix, pixseed)
        raw = np.clip(lab[ys, xs].astype(np.int64), 0, 511)
        g59[i], g459[i] = coarse_lut[raw], fine_lut[raw]
        nval['c'] += int((g59[i] != PL.IGN).sum()); nval['f'] += int((g459[i] != PL.IGN).sum()); nval['tot'] += npix
        meta.append(dict(file=fn, H=int(H), W=int(W)))
    stats = dict(valid59=nval['c'] / nval['tot'], valid459=nval['f'] / nval['tot'])
    return dict(gt59=g59, gt459=g459), dict(meta=meta, npix=npix, pixseed=pixseed, dataset='pascal_context', n_images=len(files), **stats)


def coco_files(limit=2000):
    """COCO val2017 images that LVIS v1 val annotates, sorted by file name, first `limit` (docs/COCO_LVIS_BENCHMARK.md)."""
    lvis = json.load(open(os.path.join(ROOT, 'data/lvis/lvis_v1_val.json')))
    images = sorted((i for i in lvis['images'] if '/val2017/' in i['coco_url']), key=lambda i: i['coco_url'])
    return images[:limit], lvis


def build_coco(npix, pixseed, limit=2000):
    """COCO-Stuff 171 train ids (gt171, 255: none) and the LVIS v1 category id of an added label (gtlvis, 65535: none).

    At every sampled pixel the smallest LVIS instance covering it decides: if its category is an added label and the
    COCO-Stuff label is a stuff class (train id >= 80) or unlabelled, the pixel takes that added label and loses its
    source label (the object occludes the region COCO-Stuff labelled around it). COCO thing masks are never overridden
    (LVIS also annotates parts and worn items, e.g. wheels and shirts); LVIS categories that are source concepts
    change nothing.
    """
    from pycocotools import mask as mask_utils
    from coco_lvis_vocab import load_manifest
    added = {r['lvis_id'] for r in load_manifest()['rows'] if r['role'] == 'added'}
    images, lvis = coco_files(limit)
    anns = {}
    for a in lvis['annotations']: anns.setdefault(a['image_id'], []).append(a)
    g171 = np.zeros((len(images), npix), np.uint8)
    glvis = np.full((len(images), npix), 65535, np.uint16)
    meta, stats = [], dict(overridden=0, added_under_thing=0, tot=0)
    for i, im in enumerate(images):
        fn = im['coco_url'].split('/')[-1]; H, W = im['height'], im['width']
        lab = np.array(Image.open(os.path.join(ROOT, 'data/coco-stuff/annotations_detectron2/val2017', fn.replace('.jpg', '.png'))))
        assert lab.shape == (H, W), (fn, lab.shape, (H, W))
        ys, xs = sample(H, W, i, npix, pixseed)
        src = lab[ys, xs].copy()
        area = np.full(npix, np.inf); cat = np.zeros(npix, np.int64)
        for a in anns.get(im['id'], []):
            m = mask_utils.decode(mask_utils.merge(mask_utils.frPyObjects(a['segmentation'], H, W)))[ys, xs].astype(bool)
            win = m & (a['area'] < area)
            area[win], cat[win] = a['area'], a['category_id']
        is_added = np.isin(cat, list(added))
        take = is_added & ((src >= 80) | (src == 255))
        stats['overridden'] += int(take.sum()); stats['added_under_thing'] += int((is_added & (src < 80)).sum()); stats['tot'] += npix
        glvis[i][take] = cat[take]; src[take] = 255
        g171[i] = src
        meta.append(dict(file=fn, H=int(H), W=int(W), lvis_image_id=int(im['id'])))
    stats = dict(source_labelled=float((g171 < 171).mean()), added_labelled=stats['overridden']/stats['tot'],
                 added_under_thing_kept_as_source=stats['added_under_thing']/stats['tot'])
    return dict(gt171=g171, gtlvis=glvis), dict(meta=meta, npix=npix, pixseed=pixseed, dataset='coco_stuff_lvis', n_images=len(images), **stats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(OUT))
    ap.add_argument('--npix', type=int, default=4096)
    ap.add_argument('--pixseed', type=int, default=1234)
    ap.add_argument('--out', default=None, help=f'output directory (default {OUT})')
    ap.add_argument('--check', action='store_true', help='compare with the files already in the output directory instead of writing')
    a = ap.parse_args()
    out = os.path.join(ROOT, a.out or OUT[a.dataset])
    arrays, meta = dict(ade=build_ade, pascal=build_pascal, coco=build_coco)[a.dataset](a.npix, a.pixseed)
    meta = {**meta, **{k: v for k, v in ENCODER_FIELDS.items() if k not in meta}}
    if a.check:
        old = json.load(open(os.path.join(out, 'meta.json')))
        ok = old['meta'] == meta['meta'] and old['npix'] == a.npix and old['pixseed'] == a.pixseed
        print(f'meta.json image list, sizes, npix, pixseed: {"identical" if ok else "DIFFERENT"}')
        for k, v in arrays.items():
            same = np.array_equal(np.load(os.path.join(out, f'{k}.npy')), v); ok &= same
            print(f'{k}.npy {v.shape}: {"identical" if same else "DIFFERENT"}')
        raise SystemExit(0 if ok else 1)
    os.makedirs(out, exist_ok=True)
    for k, v in arrays.items():
        np.save(os.path.join(out, f'{k}.npy'), v)
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'))
    print(f'{len(meta["meta"])} images, {a.npix} pixels each -> {out}: {", ".join(arrays)}, meta.json')


if __name__ == '__main__':
    main()
