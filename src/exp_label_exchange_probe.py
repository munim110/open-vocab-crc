"""Native CAT-Seg at random source vocabularies (stored scores for exp_label_exchange.py).

The label-exchangeability experiment draws the source vocabulary as a uniformly random 150 of the 845 names, so that
source and added labels are exchangeable. The converted (anchored) scores are candidate-independent and any source set
is a column subset of the stored anchored845 scores; native scores change with the vocabulary, so the frozen native arm
needs a native pass at each random source set. K sets are drawn once (seeded); for each, native CAT-Seg is run on
exactly those names (manifest order) and the logit of the true label is kept at every sampled pixel whose A-847 / A-150
label lies in the set (NaN elsewhere). Same images, sampled pixels, inference and float16 logits as
exp_headroom_probe.py. --check runs the set 0..149 on 3 images and compares with the stored native150 scores.
Development data (ADE validation); nothing is fitted; the confirmation reserve is not read.

    PYTHONPATH=src python src/exp_label_exchange_probe.py --tag vitl_bank683 --size large [--check] [--limit N]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CKPT
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from natural_vocab import load_manifest

S, T = 150, 845
IGN847 = 65535
K = 10


def source_sets(k=K, seed=20260925):
    """K sorted random sets of S of the T columns."""
    rng = np.random.default_rng(seed)
    return [np.sort(rng.choice(T, S, replace=False)) for _ in range(k)]


def gt845_all(ids):
    """Column in the 845-name vocabulary of every sampled pixel's label (source annotation first; -1: none) [N, P]."""
    rows = load_manifest()['rows']
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(rows) == T
    lut = np.full(IGN847+1, -1, np.int64)
    for i, r in enumerate(rows[S:]): lut[r['train_id']] = S+r.get('position', i)
    gt150, gt847 = np.load('cache/sclip/gt150.npy')[ids], np.load('cache/sclip/gt847.npy')[ids]
    return np.where(gt150 < S, gt150.astype(np.int64), lut[gt847])


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--size', default='large', choices=['base', 'large'])
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
    caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p['size'] == a.size for p in protos), 'probe run and --size disagree'
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT = Path(f'results/label_exchange_probe_{a.tag}'); STORE = Path(f'cache/label_exchange_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    names = [r['prompt'] for r in load_manifest()['rows']]
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt = gt845_all(ids)
    native150 = [np.load(f'{c}/native150.npy', mmap_mode='r') for c in caches]

    def stored(parts, k):
        for part in parts:
            if k < len(part): return part[k]
            k -= len(part)

    model = CATSegProbe(None, a.size).cuda()
    text = model.encode_text(names)

    def native_at(feats, vocab, y, x, H, W):
        scores = stitched_samples(model, model.native(feats, text[torch.from_numpy(vocab).cuda()]), y, x, H, W)
        return torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()

    def image(index):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        return model.image_features(model.windows(tensor)), y, x, H, W

    def true_logit(z, vocab, g):
        """Logit of the true label where it lies in vocab (NaN elsewhere) [P]."""
        pos = np.full(T, -1, np.int64); pos[vocab] = np.arange(len(vocab))
        p = np.where(g >= 0, pos[np.maximum(g, 0)], -1)
        out = np.full(len(g), np.nan, np.float16)
        out[p >= 0] = z[np.flatnonzero(p >= 0), p[p >= 0]]
        return out

    if a.check:
        report = {}
        for k, index in enumerate(ids[:3]):
            feats, y, x, H, W = image(index)
            d = np.abs(native_at(feats, np.arange(S), y, x, H, W).astype(np.float32)-stored(native150, k).astype(np.float32))
            report[int(index)] = dict(native150_max_abs_logit=float(d.max()), native150_mean=float(d.mean()))
            print(index, report[int(index)], flush=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    sets = source_sets()
    protocol = dict(image_ids=ids, tag=a.tag, size=a.size, source_sets=[s.tolist() for s in sets], seed=20260925,
                    store='cache/label_exchange_<tag>/native_sets.npy: float16 [set, image, pixel], native logit of the true label '
                          'with the vocabulary = that set (manifest order); NaN where the pixel label is not in the set.',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_label_exchange_probe.py', 'src/catseg_probe_model.py', 'meta/natural_vocab_v1.json', str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    store = np.lib.format.open_memmap(STORE/'native_sets.npy', mode='w+', dtype=np.float16, shape=(len(sets), len(ids), meta['npix']))
    t_start = time.time()
    for k, index in enumerate(ids):
        feats, y, x, H, W = image(index)
        for j, vocab in enumerate(sets):
            store[j, k] = true_logit(native_at(feats, vocab, y, x, H, W), vocab, gt[k])
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
    store.flush()
    result = dict(images=len(ids), sets=len(sets), seconds_per_image=(time.time()-t_start)/len(ids), gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
