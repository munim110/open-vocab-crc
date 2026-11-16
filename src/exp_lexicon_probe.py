"""Native CAT-Seg source-label scores with a large known lexicon deployed (for exp_adaptive_vocab.py).

The fallback to "why not recalibrate?" is to recalibrate once at a large known lexicon and deploy any subset of it. The
lexicon here is the 845 evaluated names followed by the first M Open Images names of meta/distractors_openimages_v1.json
(no evaluated label among them) in the seed-1 permutation of exp_anchor_bank.py --huge, for total sizes 1,690, 3,380,
6,760 and 17,001 (all names). Calibration needs only the source-label loss, so only the 150 source columns are stitched
and stored; set sizes at deployment come from the per-image vocabularies of exp_adaptive_vocab_probe.py, which are
subsets of every lexicon. Same images, pixels, inference and float16 logits as exp_headroom_probe.py; above 256 names the
released per-crop top-256 truncation applies, as at 845. Development data; nothing fitted; no reserve access.

    PYTHONPATH=src python src/exp_lexicon_probe.py --tag vitl_bank683 --size large [--limit N]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from catseg_probe_model import CATSegProbe, CKPT
from exp_adaptive_vocab_probe import S, T
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from encode import ADE
from natural_vocab import load_manifest
from PIL import Image

LEXICONS = [1690, 3380, 6760, 17001]


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--size', default='large', choices=['base', 'large'])
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p['size'] == a.size for p in protos)
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT = Path(f'results/lexicon_probe_{a.tag}'); STORE = Path(f'cache/lexicon_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    names = [r['prompt'] for r in load_manifest()['rows']]
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    oi = [oi[i] for i in np.random.default_rng(1).permutation(len(oi))]
    assert not set(oi) & set(names) and T+len(oi) == LEXICONS[-1]
    lexicon = names+oi
    model = CATSegProbe(None, a.size).cuda()
    text = model.encode_text(lexicon)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    protocol = dict(image_ids=ids, tag=a.tag, size=a.size, lexicon_sizes=LEXICONS,
                    lexicon='845 evaluated names, then Open Images names (distractors_openimages_v1, seed-1 permutation) up to each size',
                    stores='cache/lexicon_<tag>/lex<N>.npy: float16 logits of the 150 source names [image, pixel, 150] with the N-name lexicon deployed',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_lexicon_probe.py', 'src/catseg_probe_model.py', 'meta/natural_vocab_v1.json',
                                                              'meta/distractors_openimages_v1.json', str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    stores = {n: np.lib.format.open_memmap(STORE/f'lex{n}.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], S)) for n in LEXICONS}
    seconds = {n: 0.0 for n in LEXICONS}; t_start = time.time()
    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        feats = model.image_features(model.windows(tensor))
        for n in LEXICONS:
            torch.cuda.synchronize(); t0 = time.perf_counter()
            logits = model.native(feats, text[:n])[:, :S]            # stitching is per label: the source columns suffice
            z = stitched_samples(model, logits, y, x, H, W)
            stores[n][k] = torch.logit(z.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()
            torch.cuda.synchronize(); seconds[n] += time.perf_counter()-t0
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
    for s in stores.values(): s.flush()
    result = dict(images=len(ids), seconds_per_image={str(n): v/len(ids) for n, v in seconds.items()}, gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
