"""Native CAT-Seg scores under per-image vocabularies (adaptive-vocabulary experiment, stored scores for exp_adaptive_vocab.py).

The stored headroom-probe scores hold native CAT-Seg at two vocabularies only (the 150 source names and all 845); a native
score changes with the vocabulary, so a vocabulary chosen per image needs its own native pass. Every vocabulary here is the
150 source names plus a per-image set A(x) of the 695 added names, in manifest order, under five policies:
  rand50, rand200, rand500  A(x) = k added names drawn uniformly per image (seed fixed per image and policy; image-blind);
  present                   A(x) = the added names that label a sampled pixel in the A-847 annotation (a user adds what
                            they see; uses annotations, as an annotation tool's user would);
  tagger50                  A(x) = the 50 added names with the highest image-level maximum of the model's own 845-label
                            native score (an automatic tagger proposes labels; read from the stored native845 scores).
Converted (anchored) scores are candidate-independent, so for them any vocabulary is a column subset of the stored
anchored845 scores and no pass is needed. Same images, sampled pixels, inference and float16 logit storage as
exp_headroom_probe.py. --check first re-runs native at 150 and 845 names on a few images and compares with the stored
native150 / native845 scores. Development data (ADE validation); nothing is fitted; the confirmation reserve is not read.

--dataset pascal replicates this on Pascal Context 59 -> 458 (the 399 added names; stores of exp_headroom_probe_pascal.py
--tag T; the 459-label annotation plays the role of A-847). Its rules were fixed before any Pascal per-image score was
computed: rand50, rand100, rand300 (500 exceeds the 399 added names; 300 is about the
same share of them as 500 of ADE's 695), present and tagger50.

    PYTHONPATH=src python src/exp_adaptive_vocab_probe.py --tag vitl_bank683 --size large [--check] [--limit N]
    PYTHONPATH=src python src/exp_adaptive_vocab_probe.py --tag sed_bank683 --model sed [--check] [--limit N]
    PYTHONPATH=src python src/exp_adaptive_vocab_probe.py --dataset pascal --tag vitl_bank683 --size large [--check]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

import pascal_labels as PL
from catseg_probe_model import CATSegProbe, CKPT
from encode import ADE
from exp_added_label_risk import DATASETS, IGN847
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from probe_checkpoint import Checkpoint

S, T = 150, 845
POLICY_SETS = dict(
    ade=dict(rand50=('random', 50), rand200=('random', 200), rand500=('random', 500), present=('present', None), tagger50=('tagger', 50)),
    pascal=dict(rand50=('random', 50), rand100=('random', 100), rand300=('random', 300), present=('present', None), tagger50=('tagger', 50)))
POLICIES = POLICY_SETS['ade']
MANIFESTS = dict(ade='meta/natural_vocab_v1.json', pascal='meta/pascal_natural_vocab_v1.json')


def probe_paths(dataset, tag):
    """Headroom-probe runs and stores that hold the images and the source/full scores, and this probe's output dirs."""
    if dataset == 'ade':
        return ([f'results/headroom_probe_ade_{tag}', f'results/headroom_probe_ade_{tag}_rest'], [f'cache/headroom_probe_{tag}', f'cache/headroom_probe_{tag}_rest'],
                Path(f'results/adaptive_vocab_probe_{tag}'), Path(f'cache/adaptive_vocab_{tag}'))
    return ([f'results/headroom_probe_pascal_{tag}'], [f'cache/headroom_probe_pascal_{tag}'],
            Path(f'results/adaptive_vocab_probe_pascal_{tag}'), Path(f'cache/adaptive_vocab_pascal_{tag}'))


def load_image(dataset, info):
    if dataset == 'ade': return Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
    return Image.open(Path(PL.VOC)/'JPEGImages'/(info['file']+'.jpg')).convert('RGB')


def added_columns(policy, index, gt845_img, native845_img):
    """Sorted columns (>= S) of the added names in this image's vocabulary."""
    kind, k = POLICIES[policy]
    if kind == 'random':
        rng = np.random.default_rng([20260924, index, list(POLICIES).index(policy)])
        return np.sort(S+rng.choice(T-S, k, replace=False))
    if kind == 'present':
        return np.unique(gt845_img[gt845_img >= S])
    return np.sort(S+np.argsort(-native845_img[:, S:].astype(np.float32).max(0), kind='stable')[:k])


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(POLICY_SETS))
    ap.add_argument('--tag', default='vitl_bank683', help='headroom-probe run whose images and stored scores are used (ADE <run>_<tag> and _rest)')
    ap.add_argument('--size', default='large', choices=['base', 'large'])
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed'], help='CAT-Seg (default) or SED ConvNeXt-L (sed_probe_model.py, non-fast decoder)')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true', help='compare native at 150 / 845 names with the stored scores on 3 images, then stop')
    a = ap.parse_args()
    global S, T, POLICIES
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']; POLICIES = POLICY_SETS[a.dataset]
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs, caches, OUT, STORE = probe_paths(a.dataset, a.tag)
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p.get('model', 'catseg') == a.model for p in protos), 'probe run and --model disagree'
    if a.model == 'catseg': assert all(p['size'] == a.size for p in protos), 'probe run and --size disagree'
    else: assert all(not p.get('sed_fast_topk') for p in protos), 'native SED here is the non-fast decoder'
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)

    rows = d['manifest']()['rows']
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(names) == T
    lut = np.full(IGN847+1, -1, np.int64)
    for i, r in enumerate(rows[S:]): lut[r[d['fine_key']]] = S+r.get('position', i)
    assert (lut >= 0).sum() == T-S
    meta = json.loads(Path(f"{d['sclip']}/meta.json").read_text())
    gt150_all, gt847_all = np.load(f"{d['sclip']}/{d['gt_source']}"), np.load(f"{d['sclip']}/{d['gt_fine']}")
    native150 = [np.load(f'{c}/{d["stores"][0]}.npy', mmap_mode='r') for c in caches]
    native845 = [np.load(f'{c}/{d["stores"][1]}.npy', mmap_mode='r') for c in caches]

    def stored(parts, k):
        for part in parts:
            if k < len(part): return part[k]
            k -= len(part)

    def gt845(index):
        return np.where(gt150_all[index] < S, gt150_all[index].astype(np.int64), lut[gt847_all[index]])

    cols = {p: [added_columns(p, index, gt845(index), stored(native845, k)) for k, index in enumerate(ids)] for p in POLICIES}
    width = {p: max(len(c) for c in cols[p]) for p in POLICIES}
    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as SED_CKPT
        model = SEDProbe().cuda()
    else:
        model = CATSegProbe(None, a.size).cuda()
    text = model.encode_text(names)

    def native_at(feats, vocab, y, x, H, W):
        scores = stitched_samples(model, model.native(feats, text[torch.from_numpy(vocab).cuda()]), y, x, H, W)
        return torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()

    def image(index):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = load_image(a.dataset, info)
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        return model.image_features(model.windows(tensor)), y, x, H, W

    if a.check:
        report = {}
        for k, index in enumerate(ids[:3]):
            feats, y, x, H, W = image(index)
            d150 = np.abs(native_at(feats, np.arange(S), y, x, H, W).astype(np.float32)-stored(native150, k).astype(np.float32))
            d845 = np.abs(native_at(feats, np.arange(T), y, x, H, W).astype(np.float32)-stored(native845, k).astype(np.float32))
            report[int(index)] = dict(native150_max_abs_logit=float(d150.max()), native150_mean=float(d150.mean()),
                                      native845_max_abs_logit=float(d845.max()), native845_mean=float(d845.mean()))
            print(index, report[int(index)], flush=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    protocol = dict(image_ids=ids, tag=a.tag, model=a.model, size=a.size if a.model == 'catseg' else 'convnext_large', policies={p: dict(kind=v[0], k=v[1]) for p, v in POLICIES.items()},
                    vocabulary=f'{S} source names followed by the added names A(x) in manifest order; native pass on exactly this list.',
                    stores=f'{STORE}/<policy>.npy: float16 logits [image, pixel, {S}+width] (source columns first, then '
                           'A(x); padding columns 0 with column index -1 in <policy>_cols.npy).',
                    scope=f"Development data ({d['name']}). No fitting; no reserve access.",
                    added_names_per_image={p: dict(mean=float(np.mean([len(c) for c in cols[p]])), max=width[p]) for p in POLICIES},
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_adaptive_vocab_probe.py', MANIFESTS[a.dataset]] +
                            (['src/catseg_probe_model.py', str(CKPT)] if a.model == 'catseg' else ['src/sed_probe_model.py', str(SED_CKPT)])})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    ckpt = Checkpoint(STORE, protocol)   # resumes an interrupted run of the same protocol (probe_checkpoint.py)
    stores = ckpt.open_stores({p: ((len(ids), meta['npix'], S+width[p]), np.float16) for p in POLICIES})
    colstores = {}
    for p in POLICIES:
        c = np.full((len(ids), width[p]), -1, np.int16)
        for k, cc in enumerate(cols[p]): c[k, :len(cc)] = cc
        np.save(STORE/f'{p}_cols.npy', c); colstores[p] = c
    seconds = {p: 0.0 for p in POLICIES}
    if 'seconds' in ckpt.state: seconds = dict(zip(POLICIES, ckpt.state['seconds'].tolist()))
    t_start = time.time()
    for k, index in enumerate(ids):
        if k < ckpt.start: continue
        feats, y, x, H, W = image(index)
        for p in POLICIES:
            vocab = np.concatenate([np.arange(S), cols[p][k]])
            torch.cuda.synchronize(); t0 = time.perf_counter()
            z = native_at(feats, vocab, y, x, H, W)
            torch.cuda.synchronize(); seconds[p] += time.perf_counter()-t0
            stores[p][k, :, :len(vocab)] = z
            if len(vocab) < S+width[p]: stores[p][k, :, len(vocab):] = 0
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
        ckpt.step(k, seconds=np.array([seconds[p] for p in POLICIES]))
    for s in stores.values(): s.flush()
    result = dict(images=len(ids), seconds_per_image={p: v/len(ids) for p, v in seconds.items()}, gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, added_names_per_image=protocol['added_names_per_image'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    ckpt.finish()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
