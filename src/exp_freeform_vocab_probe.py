"""Native and anchored CAT-Seg / SED scores under free-form per-image names (docs/FREEFORM_NAMES_PROTOCOL.md).

Each image's deployed vocabulary is the 150 source names followed by its added names A(x) from a language model
(exp_freeform_names.py, results/freeform_names_ade/names.json), most of them outside ADE20K-847. Native: one pass at
exactly that list. Anchored: the A(x) candidates against the run's reference bank (lean bank pass; candidate scores
identical to the full pass, tests/check_lean_bank.py); the anchored source columns do not depend on A(x) and are the
stored anchored845 source columns, which --check recomputes. Same images, sampled pixels, inference and float16 logit
storage as exp_adaptive_vocab_probe.py. Development data (ADE validation); nothing is fitted; the reserve is not read.

    PYTHONPATH=src .venv-probe/Scripts/python.exe src/exp_freeform_vocab_probe.py --tag vitl_bank683 --size large [--check]
    PYTHONPATH=src .venv-probe/Scripts/python.exe src/exp_freeform_vocab_probe.py --tag sed_bank683 --model sed [--check]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from catseg_probe_model import CATSegProbe, CKPT, bank_context
from exp_adaptive_vocab_probe import load_image, probe_paths
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from natural_vocab import load_manifest
from probe_checkpoint import Checkpoint

S = 150
NAMES = Path('results/freeform_names_ade/names.json')


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--size', default='large', choices=['base', 'large'])
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed'])
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true', help='compare native at 150 names and the anchored source columns with the stored scores on 3 images, then stop')
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs, caches, _, _ = probe_paths('ade', a.tag)
    OUT, STORE = Path(f'results/freeform_vocab_probe_{a.tag}'), Path(f'cache/freeform_vocab_{a.tag}')
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p.get('model', 'catseg') == a.model for p in protos), 'probe run and --model disagree'
    if a.model == 'catseg': assert all(p['size'] == a.size for p in protos), 'probe run and --size disagree'
    else: assert all(not p.get('sed_fast_topk') for p in protos), 'native SED here is the non-fast decoder'
    assert len({p['bank'] for p in protos}) == 1 and protos[0]['bank'].endswith('.json'), 'a run with a JSON reference bank'
    ids = sum([p['image_ids'] for p in protos], [])
    free = json.loads(NAMES.read_text())
    assert free['image_ids'] == ids, 'names.json must cover the probe images in probe order'
    if a.limit: ids = ids[:a.limit]
    added = [free['added'][str(i)] for i in ids]
    unique = sorted({n for A in added for n in A}); col = {n: j for j, n in enumerate(unique)}
    width = max(len(A) for A in added)
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)

    names = [r['prompt'] for r in load_manifest()['rows']][:S]
    bank = json.loads(Path(protos[0]['bank']).read_text())['names']
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    stored = {k: [np.load(f'{c}/{k}.npy', mmap_mode='r') for c in caches] for k in ['native150', 'anchored845']}

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as MODEL_CKPT
        model = SEDProbe().cuda()
        context = lambda feats: model.context(feats, ref_text, lean=True)
    else:
        MODEL_CKPT = CKPT
        model = CATSegProbe(None, a.size).cuda()
        context = lambda feats: bank_context(model, feats, ref_text, lean=True)
    src_text, ref_text = model.encode_text(names), model.encode_text(bank)
    free_text = model.encode_text(unique)

    def logits(scores):
        return torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()

    def image(index):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(load_image('ade', info)))).permute(2, 0, 1).float().cuda()
        return model.image_features(model.windows(tensor)), y, x, H, W

    if a.check:
        report = {}
        for k, index in enumerate(ids[:3]):
            feats, y, x, H, W = image(index)
            n150 = logits(stitched_samples(model, model.native(feats, src_text), y, x, H, W)).astype(np.float32)
            anch = logits(stitched_samples(model, model.anchored(feats, context(feats), src_text), y, x, H, W)).astype(np.float32)
            d0 = np.abs(n150-part(stored['native150'], k).astype(np.float32))
            d1 = np.abs(anch-part(stored['anchored845'], k)[:, :S].astype(np.float32))
            report[int(index)] = dict(native150_max_abs_logit=float(d0.max()), native150_mean=float(d0.mean()),
                                      anchored_source_max_abs_logit=float(d1.max()), anchored_source_mean=float(d1.mean()))
            print(index, report[int(index)], flush=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    protocol = dict(image_ids=ids, tag=a.tag, model=a.model, size=a.size if a.model == 'catseg' else 'convnext_large', bank=protos[0]['bank'],
                    names=str(NAMES), names_sha256=digest(NAMES), unique_added_names=len(unique),
                    added_names_per_image=dict(mean=float(np.mean([len(A) for A in added])), max=width),
                    vocabulary=f'{S} source names followed by the image\'s added names in the order of the answer; native pass on exactly this list.',
                    stores=f'{STORE}/native.npy: float16 logits [image, pixel, {S}+width] (source columns first, then A(x)); anchored_added.npy: '
                           'float16 anchored logits of A(x) [image, pixel, width]; padding columns 0; n_added.npy gives |A(x)|.',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_freeform_vocab_probe.py', 'meta/natural_vocab_v1.json', protos[0]['bank'], str(MODEL_CKPT),
                                                              'src/sed_probe_model.py' if a.model == 'sed' else 'src/catseg_probe_model.py']})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    np.save(STORE/'n_added.npy', np.array([len(A) for A in added], np.int16))
    ckpt = Checkpoint(STORE, protocol)
    stores = ckpt.open_stores({'native': ((len(ids), meta['npix'], S+width), np.float16), 'anchored_added': ((len(ids), meta['npix'], width), np.float16)})
    seconds = np.zeros(3)
    ckpt.restore(seconds=seconds)
    t_start = time.time()
    for k, index in enumerate(ids):
        if k < ckpt.start: continue
        cand = free_text[torch.tensor([col[n] for n in added[k]], dtype=torch.long, device=free_text.device)]
        torch.cuda.synchronize(); t0 = time.perf_counter()
        feats, y, x, H, W = image(index)
        torch.cuda.synchronize(); t1 = time.perf_counter()
        nat = logits(stitched_samples(model, model.native(feats, torch.cat([src_text, cand])), y, x, H, W))
        torch.cuda.synchronize(); t2 = time.perf_counter()
        stores['native'][k, :, :nat.shape[1]] = nat
        if nat.shape[1] < S+width: stores['native'][k, :, nat.shape[1]:] = 0
        stores['anchored_added'][k] = 0
        if len(cand):
            anch = logits(stitched_samples(model, model.anchored(feats, context(feats), cand), y, x, H, W))
            stores['anchored_added'][k, :, :anch.shape[1]] = anch
        torch.cuda.synchronize(); seconds += [t1-t0, t2-t1, time.perf_counter()-t2]
        if k % 50 == 0: print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
        ckpt.step(k, seconds=seconds)
    result = dict(images=len(ids), seconds_per_image=dict(zip(['features', 'native', 'anchored_bank_plus_added'], (seconds/len(ids)).tolist())),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, added_names_per_image=protocol['added_names_per_image'])
    ckpt.finish()
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
