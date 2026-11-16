"""Native SED source-label scores with a large known lexicon deployed (SED counterpart of exp_lexicon_probe.py, read by
exp_adaptive_vocab.py --tag sed_bank683).

Same lexicons as the CAT-Seg run: the 845 evaluated names followed by Open Images names (meta/distractors_openimages_v1.json,
seed-1 permutation, no evaluated label among them) up to 1,690, 3,380, 6,760 and 17,001 names. Same 2,000 ADE validation
images, pixel samples and float16 logits as the SED headroom probe (results/headroom_probe_ade_sed_bank683 and _rest);
calibration needs only the source-label loss, so only the 150 source columns are stored.

SED's released (non-fast) decoder keeps every label's activations through its three stages, which does not fit in memory at
17k labels. This probe streams the same computation: at each stage, the class-attention key/value sums over the whole lexicon
are accumulated chunk by chunk, each chunk recomputed from its cost volume with the sums of the earlier stages; the three
stages' sums then score the 150 source names alone. Every per-label operation is the released one, applied in the released
chunk order (sed_probe_model.forward_bank), so the sums are those of SEDProbe.native; --check compares the streamed source
logits with SEDProbe.native at the 845-name vocabulary and with the stored native845 scores. Development data; nothing fitted.

    PYTHONPATH=src python src/exp_lexicon_probe_sed.py [--check] [--limit N] [--lexicons 1690,3380,6760,17001]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from einops import rearrange
from PIL import Image

from encode import ADE
from exp_adaptive_vocab_probe import S, T
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from natural_vocab import load_manifest
from probe_checkpoint import Checkpoint
from sed_probe_model import CKPT as SED_CKPT, SEDProbe, _fuse

LEXICONS = [1690, 3380, 6760, 17001]
TAG = 'sed_bank683'
CHUNK = 128                                   # the released chunk size (sed_probe_model), kept so the sums accumulate in the same order


def _tokens(layer, x):
    """Pooled label tokens of a chunk [B,C,T,H,W] -> ([(B H W),T,C], normed, (Hp,Wp)); pooling is per label."""
    pooled = layer.pool_features(x)
    tok = rearrange(pooled, 'B C T H W -> (B H W) T C')
    return tok, layer.norm1(tok), pooled.shape[-2:]


def _split(att, z):
    return rearrange(z, 'N T (H D) -> N T H D', H=att.nheads)


def kv_sums(layer, x):
    """Key/value sums of a chunk of labels (the context=None branch of sed_class_attention, one chunk)."""
    att = layer.attention
    _, normed, _ = _tokens(layer, x)
    k = F.elu(_split(att, att.k(normed)))+1
    v = _split(att, att.v(normed))
    return torch.einsum('nshd,nshv->nhdv', k, v), k.sum(1)


def attend(layer, x, sums):
    """Class attention of a chunk of labels against recorded sums that already include these labels (native semantics)."""
    att = layer.attention
    KV, Ks = sums
    B, C, T, H, W = x.shape
    tok, normed, (Hp, Wp) = _tokens(layer, x)
    q = F.elu(_split(att, att.q(normed)))+1
    num = torch.einsum('nlhd,nhdv->nlhv', q, KV)
    den = torch.einsum('nlhd,nhd->nlh', q, Ks)
    tok = tok+rearrange(num/(den[..., None]+att.attention.eps), 'N T H D -> N T (H D)')
    tok = tok+layer.MLP(layer.norm2(tok))
    tok = rearrange(tok, '(B H W) T C -> (B T) C H W', B=B, H=Hp, W=Wp)
    tok = F.interpolate(tok, size=(H, W), mode='bilinear', align_corners=True)
    return x+rearrange(tok, '(B T) C H W -> B C T H W', B=B)


@torch.no_grad()
def source_logits(model, feats, text, n_src, chunk=CHUNK):
    """Released SED logits of the first n_src labels under the whole vocabulary `text` [T,80,768]: [B,n_src,192,192].
    Equals SEDProbe.native(feats, text)[:, :n_src] up to floating-point order, for any T."""
    agg = model.transformer
    img, guidance = feats
    B = img.shape[0]
    g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
    ups = [agg.decoder1, agg.decoder2, agg.decoder3]
    projections = list(agg.decoder_corr_guidance_projection)

    def prepare(t, stages):
        corr = agg.correlation(img, t[None].expand(B, -1, -1, -1), model.clip_model.logit_scale)
        x = rearrange(agg.corr_embed(corr), 'B C T H W -> (B T) C H W')
        c = rearrange(corr, 'B P T H W -> (B T) P H W')
        cg = []
        for proj in projections[:stages]:
            c = proj(c); cg.append(c)
        return x, cg

    def run_stage(x, s, sums, cg):
        up = ups[s]
        x = up.cnext(x)
        x = attend(up.attention, rearrange(x, '(B T) C H W -> B C T H W', B=B), sums)
        return _fuse(up, rearrange(x, 'B C T H W -> (B T) C H W'), g_dec[s], cg)

    sums = []
    for s in range(3):
        KV = Ks = 0
        for i in range(0, len(text), chunk):
            x, cg = prepare(text[i:i+chunk], s)
            for r in range(s):
                x = run_stage(x, r, sums[r], cg[r])
            x = ups[s].cnext(x)
            kv, ks = kv_sums(ups[s].attention, rearrange(x, '(B T) C H W -> B C T H W', B=B))
            KV = KV+kv; Ks = Ks+ks
        sums.append((KV, Ks))
    x, cg = prepare(text[:n_src], 3)
    for r in range(3):
        x = run_stage(x, r, sums[r], cg[r])
    return rearrange(agg.head(x), '(B T) () H W -> B T H W', B=B)


def to_store(model, logits, y, x, H, W):
    z = stitched_samples(model, logits, y, x, H, W)
    return torch.logit(z.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--lexicons', default=','.join(map(str, LEXICONS)))
    ap.add_argument('--check', action='store_true', help='first images: streamed 845-name source logits vs SEDProbe.native and the stored native845')
    ap.add_argument('--check-images', type=int, default=3)
    a = ap.parse_args()
    lexicons = [int(v) for v in a.lexicons.split(',')]
    assert all(n in LEXICONS for n in lexicons) and lexicons == sorted(lexicons)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{TAG}', f'results/headroom_probe_ade_{TAG}_rest']
    caches = [f'cache/headroom_probe_{TAG}', f'cache/headroom_probe_{TAG}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p.get('model') == 'sed' and not p.get('sed_fast_topk') for p in protos), 'native SED here is the non-fast decoder'
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT = Path(f'results/lexicon_probe_{TAG}'); STORE = Path(f'cache/lexicon_{TAG}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    names = [r['prompt'] for r in load_manifest()['rows']]
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    oi = [oi[i] for i in np.random.default_rng(1).permutation(len(oi))]
    assert not set(oi) & set(names) and T+len(oi) == LEXICONS[-1]
    lexicon = names+oi
    model = SEDProbe().cuda()
    t0 = time.time()
    text = model.encode_text(lexicon[:max(lexicons)])
    print(f'text {tuple(text.shape)} in {time.time()-t0:.0f}s', flush=True)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())

    def image(index):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        return model.image_features(model.windows(tensor)), y, x, H, W

    if a.check:
        native845 = [np.load(f'{c}/native845.npy', mmap_mode='r') for c in caches]
        report = []
        for k in range(min(a.check_images, len(ids))):
            feats, y, x, H, W = image(ids[k])
            torch.cuda.synchronize(); t0 = time.perf_counter()
            streamed = source_logits(model, feats, text[:T], S)
            torch.cuda.synchronize(); t_stream = time.perf_counter()-t0; t0 = time.perf_counter()
            native = model.native(feats, text[:T])[:, :S]
            torch.cuda.synchronize(); t_native = time.perf_counter()-t0
            stored = np.array(native845[0][k] if k < len(native845[0]) else native845[1][k-len(native845[0])])[:, :S]
            ours = to_store(model, streamed, y, x, H, W)
            report.append(dict(image=ids[k], logits_max_abs_diff=float((streamed-native).abs().max()), logits_max_abs=float(native.abs().max()),
                               stored_max_abs_diff=float(np.abs(ours.astype(np.float32)-stored.astype(np.float32)).max()),
                               stored_bitwise_equal=bool(np.array_equal(ours, stored)), seconds_streamed=t_stream, seconds_native=t_native))
            print(json.dumps(report[-1]), flush=True)
        (OUT/'check.json').write_text(json.dumps(dict(vocabulary=T, source=S, chunk=CHUNK, images=report), indent=2))
        return

    protocol = dict(image_ids=ids, tag=TAG, model='sed', lexicon_sizes=lexicons, chunk=CHUNK,
                    lexicon='845 evaluated names, then Open Images names (distractors_openimages_v1, seed-1 permutation) up to each size',
                    stores=f'cache/lexicon_{TAG}/lex<N>.npy: float16 logits of the 150 source names [image, pixel, 150] with the N-name lexicon deployed natively (non-fast decoder, streamed class-attention sums)',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_lexicon_probe_sed.py', 'src/sed_probe_model.py', 'meta/natural_vocab_v1.json',
                                                              'meta/distractors_openimages_v1.json', str(SED_CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    ckpt = Checkpoint(STORE, protocol)
    stores = ckpt.open_stores({f'lex{n}': ((len(ids), meta['npix'], S), np.float16) for n in lexicons})
    seconds = np.zeros(len(lexicons)); ckpt.restore(seconds=seconds)
    t_start = time.time()
    for k, index in enumerate(ids):
        if k < ckpt.start: continue
        feats, y, x, H, W = image(index)
        for j, n in enumerate(lexicons):
            torch.cuda.synchronize(); t0 = time.perf_counter()
            logits = source_logits(model, feats, text[:n], S)
            stores[f'lex{n}'][k] = to_store(model, logits, y, x, H, W)
            torch.cuda.synchronize(); seconds[j] += time.perf_counter()-t0
        if k % 25 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
        ckpt.step(k, seconds=seconds)
    result = dict(images=len(ids), seconds_per_image={str(n): float(v/len(ids)) for n, v in zip(lexicons, seconds)},
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    ckpt.finish()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
