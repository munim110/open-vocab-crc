"""Controls for the anchored conversion (released CAT-Seg ViT-B, nothing fitted).

  native_untruncated  released class attention over all 845 deployed labels, top-256 pruning removed.
                      Separates attention-induced from pruning-induced threshold breakage (all 400 probe images).
  native_bank_plus_one  released CAT-Seg run separately on COCO-171 + {c} for each candidate c: the obvious
                      candidate-independent construction, with candidate-to-reference feedback. Compared with the
                      shared frozen reference context for agreement and cost (first --pairs images, all 845 labels).
Same images, pixels, prompts and float16 round trip as the headroom probe. Development data.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS, curves
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

OUT = Path('results/audit_controls_ade')
S, ADDITIONS = DATASETS['ade']['source'], DATASETS['ade']['additions']


def untruncated(model, feats, text, last_only=False):
    """Aggregator.forward over every deployed label: no pruning (padding as released when T < pad_len).

    last_only decodes just the final label; the decoder treats labels independently, so its logits are unchanged."""
    agg = model.transformer
    img, guidance = feats
    if img.shape[0] > 1:                                             # windows are independent; one at a time bounds memory
        return torch.cat([untruncated(model, (img[i:i+1], [g[i:i+1] for g in guidance]), text, last_only) for i in range(img.shape[0])])
    t = text[None, :, None].expand(img.shape[0], -1, -1, -1)
    x = agg.corr_embed(agg.correlation(img, t))
    g_app = agg.guidance_projection(guidance[0])
    g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
    g_text = agg.text_guidance_projection(t.mean(-2))
    for layer in agg.layers:                                         # swin_block is per label, so chunking it is exact
        x = torch.cat([layer.swin_block(x[:, :, i:i+32], g_app) for i in range(0, x.shape[2], 32)], 2)
        x = layer.attention(x, g_text)
    return model.decode(x[:, :, -1:] if last_only else x, g_dec)


def roundtrip(prob):
    return torch.logit(prob.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().double()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pairs', type=int, default=16, help='images for the per-candidate native construction')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    ids = json.loads(Path('results/headroom_probe_ade/protocol.json').read_text())['image_ids']
    if a.limit: ids = ids[:a.limit]
    names = [r['prompt'] for r in load_manifest()['rows']]
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    model = CATSegProbe().cuda()
    text, ref_text = model.encode_text(names), model.encode_text(coco)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt = np.load('cache/sclip/gt150.npy')
    grid = torch.from_numpy(LOGIT_GRID).cuda(); widths = [S+x for x in ADDITIONS]
    stored = {k: np.load(f'cache/headroom_probe/{k}.npy', mmap_mode='r') for k in ['native150', 'native845', 'anchored845']}
    loss = {k: [] for k in ['native150', 'native845', 'untruncated845']}; size = {k: [] for k in loss}
    top10, agreement, seconds = [], [], np.zeros(2)
    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda(); valid = target < S
        feats = model.image_features(model.windows(torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()))
        if k == 0:   # below pad_len nothing is pruned, so the control must reproduce the released forward
            drift = float((untruncated(model, feats, text[:S])-model.native(feats, text[:S])).abs().max())
            assert drift < 1e-3, drift
        full = roundtrip(stitched_samples(model, untruncated(model, feats, text), y, x, H, W))
        for key, scores, w in [('native150', torch.from_numpy(np.array(stored['native150'][k])).cuda().double(), widths[:1]),
                               ('native845', torch.from_numpy(np.array(stored['native845'][k])).cuda().double(), widths), ('untruncated845', full, widths)]:
            l, s = curves(scores, target, grid, S, w); loss[key].append(l); size[key].append(s.astype(np.float32))
        top10.append((true_ranks(full, target.clamp(max=S-1))[valid] <= 10).double().mean().item())
        if k < a.pairs:
            anchored = torch.from_numpy(np.array(stored['anchored845'][k])).cuda().double()
            torch.cuda.synchronize(); t0 = time.perf_counter()
            separate = []
            for c in range(len(names)):
                logits = untruncated(model, feats, torch.cat([ref_text, text[c:c+1]]), last_only=True)
                separate.append(stitched_samples(model, logits, y, x, H, W))
            torch.cuda.synchronize(); t1 = time.perf_counter()
            model.anchored(feats, model.context(feats, ref_text), text)
            torch.cuda.synchronize(); seconds += [t1-t0, time.perf_counter()-t1]
            separate = roundtrip(torch.cat(separate, -1))
            live = (separate[valid] > -12) | (anchored[valid] > -12)                 # ignore the saturated tail
            d = (separate[valid]-anchored[valid]).abs()
            t = target[valid]
            r_sep, r_anc = true_ranks(separate[valid], t), true_ranks(anchored[valid], t)
            agreement.append([d[live].mean().item(), d[live].quantile(.99).item(), (r_sep == r_anc).double().mean().item(),
                              r_sep.double().mean().item(), r_anc.double().mean().item(),
                              (separate[valid].argmax(-1) == anchored[valid].argmax(-1)).double().mean().item()])
            print(f'pair {k+1}/{a.pairs} mean|d|={agreement[-1][0]:.3f} same true rank={agreement[-1][2]:.3f} seconds={t1-t0:.0f}', flush=True)
        elif k % 20 == 0 or k < 3:
            print(f'{k+1}/{len(ids)} untruncated +695 top10={top10[-1]:.3f} peak_gb={torch.cuda.max_memory_allocated()/2**30:.1f} t={time.perf_counter():.0f}', flush=True)
    loss = {k: np.stack(v) for k, v in loss.items()}; size = {k: np.stack(v) for k, v in size.items()}
    np.savez_compressed(OUT/'curves.npz', **{f'loss_{k}': v for k, v in loss.items()}, **{f'size_{k}': v for k, v in size.items()}, agreement=np.array(agreement))
    n = len(ids); rng = np.random.default_rng(20261005); perms = [rng.permutation(n) for _ in range(200)]
    result = dict(images=n, untruncated_top10_plus695=float(np.mean(top10)), splits={})
    lines = ['# Audit controls on released CAT-Seg (ADE development images)', '', '## Frozen source threshold under the full vocabulary: attention versus pruning', '',
             f'{n} images, mean over 200 random {n//2}/{n-n//2} splits. The threshold is calibrated by CRC under the {S}-label deployment and reused after 695 labels are added; "replayed" recalibrates under the full vocabulary.', '',
             '| alpha | Deployment at +695 | Risk with frozen threshold (%) | Frozen size | Risk replayed (%) | Replayed size |', '|---:|---|---:|---:|---:|---:|']
    for alpha in ALPHAS:
        for key in ['native845', 'untruncated845']:
            rows = []
            for p in perms:
                cal, ev = p[:n//2], p[n//2:]
                pick = lambda store: np.flatnonzero((loss[store][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
                gf, gr = pick('native150'), pick(key)
                rows.append([loss[key][ev, gf].mean(), size[key][ev, -1, gf].mean(), loss[key][ev, gr].mean(), size[key][ev, -1, gr].mean()])
            m = np.mean(rows, 0); result['splits'][f'{key}_a{alpha}'] = m.tolist()
            lines.append(f"| {alpha} | {'released (top-256 pruning)' if key == 'native845' else 'pruning removed'} | {100*m[0]:.2f} | {m[1]:.2f} | {100*m[2]:.2f} | {m[3]:.2f} |")
    if agreement:
        g = np.mean(agreement, 0); per = seconds/len(agreement)
        result['bank_plus_one'] = dict(images=len(agreement), mean_abs_logit_diff=g[0], p99_abs_logit_diff=g[1], same_true_rank=g[2], true_rank_separate=g[3],
                                       true_rank_shared=g[4], same_top1=g[5], seconds_separate=per[0], seconds_shared=per[1])
        lines += ['', '## Native CAT-Seg on COCO-171 + {c}, one run per candidate, versus the shared frozen reference context', '',
                  f'{len(agreement)} images, all 845 labels, valid sampled pixels; logit differences over entries where either logit exceeds -12.', '',
                  f'- mean |logit difference| {g[0]:.3f}, 99th percentile {g[1]:.3f}', f'- true label has the same rank at +695 on {100*g[2]:.2f}% of pixels; mean rank {g[3]:.2f} (separate runs) vs {g[4]:.2f} (shared context); same top-1 label {100*g[5]:.2f}%',
                  f'- aggregation and decoding time per image: {per[0]:.1f} s (separate runs) vs {per[1]:.1f} s (shared context), CLIP image features excluded from both']
    lines += ['', 'Development data, previously inspected; released ViT-B weights; stored float16 logits.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_audit_controls.py', 'src/catseg_probe_model.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=1))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
