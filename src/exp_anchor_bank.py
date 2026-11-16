"""Reference-bank sensitivity of anchored CAT-Seg (released weights, nothing fitted).

Same 400 ADE development images, pixels, prompts and CRC rule as the headroom probe; only the
bank that candidates attend to changes. The bank list below was fixed before any variant was scored.
  coco171        the training vocabulary (scores reused from the headroom probe)
  coco85, coco20 random subsets of it (seed 0)
  pascal171      171 Pascal Context-459 names that are not COCO-Stuff names (seed 0): a bank the model was not trained on
  candidate_only no reference labels: each candidate attends to pad_len-1 padding tokens and itself, which is exactly
                 the released CAT-Seg run on that one label alone (the obvious independent-query construction)
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from einops import rearrange
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS, curves
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest
from pascal_natural_vocab import load_manifest as load_pascal

OUT = Path('results/anchor_bank_ade')
S, ADDITIONS = DATASETS['ade']['source'], DATASETS['ade']['additions']


def padding_only_context(model, feats):
    """Key/value sums of pad_len-1 copies of the learned padding token: the native context of a one-label vocabulary."""
    agg = model.transformer
    img, guidance = feats
    ctx = dict(g_app=agg.guidance_projection(guidance[0]), g_dec=[p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])], sums=[])
    n = img.shape[0]*img.shape[-2]*img.shape[-1]
    for block in agg.layers:
        layer = block.attention; att = layer.attention
        normed = layer.norm1(layer.padding_tokens)
        joint = torch.cat([normed, layer.padding_guidance], -1)
        k = F.elu(rearrange(att.k(joint), 'N T (H D) -> N T H D', H=att.nheads))+1
        v = rearrange(att.v(normed), 'N T (H D) -> N T H D', H=att.nheads)
        assert k.shape[:2] == (1, 1)
        KV = (layer.pad_len-1)*torch.einsum('nshd,nshv->nhdv', k, v)
        ctx['sums'].append((KV.expand(n, -1, -1, -1), ((layer.pad_len-1)*k.sum(1)).expand(n, -1, -1)))
    return ctx


@torch.no_grad()
def main():
    global OUT
    OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    ids = json.loads(Path('results/headroom_probe_ade/protocol.json').read_text())['image_ids']
    names = [r['prompt'] for r in load_manifest()['rows']]
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    rng = np.random.default_rng(0)
    pool = [r['prompt'] for r in load_pascal()['rows'] if r['prompt'] not in set(coco)]
    banks = dict(coco85=[coco[i] for i in sorted(rng.choice(171, 85, replace=False))],
                 coco20=[coco[i] for i in sorted(rng.choice(171, 20, replace=False))],
                 pascal171=[pool[i] for i in sorted(rng.choice(len(pool), 171, replace=False))], candidate_only=[])
    if '--large' in sys.argv:   # second, later bank list (fixed 2026-09-22 before scoring): does a bank larger than COCO-171 shrink the sets?
        OUT = Path('results/anchor_bank_large_ade'); OUT.mkdir(parents=True, exist_ok=True)
        oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']     # no evaluated label name is in this list
        oi = [oi[i] for i in rng.permutation(len(oi))]
        banks = dict(coco_pascal255=coco+banks['pascal171'][:84], coco_oi255=coco+oi[:84], coco_pascal342=coco+banks['pascal171'],
                     coco_oi342=coco+oi[:171], coco_oi683=coco+oi[:512])
    if '--huge' in sys.argv:    # third list (fixed 2026-09-22 after the --large result: sets kept shrinking up to 683 labels)
        OUT = Path('results/anchor_bank_huge_ade'); OUT.mkdir(parents=True, exist_ok=True)
        oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
        oi = [oi[i] for i in np.random.default_rng(1).permutation(len(oi))]
        banks = dict(coco_oi1366=coco+oi[:1195], coco_oi2731=coco+oi[:2560], coco_oi5462=coco+oi[:5291], oi683=oi[:683])
    (OUT/'protocol.json').write_text(json.dumps(dict(image_ids=ids, banks=banks, candidate_overlap={k: len(set(v) & set(names)) for k, v in banks.items()},
        hashes={p: digest(Path(p)) for p in ['src/exp_anchor_bank.py', 'src/catseg_probe_model.py', 'meta/natural_vocab_v1.json', 'meta/pascal_natural_vocab_v1.json']}), indent=1))
    model = CATSegProbe().cuda()
    text = model.encode_text(names)
    bank_text = {k: model.encode_text(v) for k, v in banks.items() if v}
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt = np.load('cache/sclip/gt150.npy')
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    widths = [S+a for a in ADDITIONS]
    stored = np.load('cache/headroom_probe/anchored845.npy', mmap_mode='r')
    loss = {k: [] for k in ['coco171', *banks]}; size = {k: [] for k in loss}; ranks = {k: [] for k in loss}

    def record(key, logits, target):
        l, s = curves(logits, target, grid, S, widths)
        loss[key].append(l); size[key].append(s.astype(np.float32))
        valid = target < S; t = target.clamp(max=S-1)
        r0, r1 = true_ranks(logits[:, :S], t)[valid].double(), true_ranks(logits, t)[valid].double()
        ranks[key].append([r0.mean().item(), r1.mean().item(), (r0 == 1).double().mean().item(), (r1 <= 10).double().mean().item()])

    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda()
        feats = model.image_features(model.windows(torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()))
        record('coco171', torch.from_numpy(np.array(stored[k])).cuda().double(), target)
        for key in banks:
            if not banks[key]: ctx = padding_only_context(model, feats)
            else:   # windows are independent; one at a time bounds memory for the large banks
                parts = [bank_context(model, (feats[0][i:i+1], [g[i:i+1] for g in feats[1]]), bank_text[key]) for i in range(feats[0].shape[0])]
                ctx = dict(g_app=torch.cat([c['g_app'] for c in parts]), g_dec=[torch.cat(g) for g in zip(*[c['g_dec'] for c in parts])],
                           sums=[(torch.cat([c['sums'][j][0] for c in parts]), torch.cat([c['sums'][j][1] for c in parts])) for j in range(len(parts[0]['sums']))])
            prob = stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W)
            # same float16 round trip as the stored probe scores, so coco171 is comparable
            record(key, torch.logit(prob.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().double(), target)
        if '--smoke' in sys.argv and k == 1:
            print({key: np.round(v[-1], 3).tolist() for key, v in ranks.items()}); return
        if k % 20 == 0:
            print(f'{k+1}/{len(ids)} +695 top10 '+' '.join(f'{key}={ranks[key][-1][3]:.3f}' for key in loss), flush=True)
    loss = {k: np.stack(v) for k, v in loss.items()}; size = {k: np.stack(v) for k, v in size.items()}
    np.savez_compressed(OUT/'curves.npz', **{f'loss_{k}': v for k, v in loss.items()}, **{f'size_{k}': v for k, v in size.items()})

    split_rng = np.random.default_rng(20261004); perms = [split_rng.permutation(len(ids)) for _ in range(200)]
    result, lines = {}, ['# Reference-bank sensitivity of anchored CAT-Seg', '',
        f'{len(ids)} ADE development images (the headroom-probe 400). Released weights; only the bank changes. Sets: image-level CRC calibrated once at the {S} source labels; mean over 200 random 200/200 splits, fixed original split in brackets. Ranks are image-averaged.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', '| Bank | Labels in bank | Source rank | Rank at +695 | Source top1 | +695 top10 | Risk (%) | '+' | '.join(f'+{a}' for a in ADDITIONS)+' |', '|---|---:|---:|---:|---:|---:|---:|'+'---:|'*len(ADDITIONS)]
        for key in loss:
            def run(cal, ev):
                g = np.flatnonzero((loss[key][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
                return loss[key][ev, g].mean(), size[key][ev][:, :, g].mean(0)
            reps = [run(p[:200], p[200:]) for p in perms]
            fixed = run(np.arange(200), np.arange(200, 400))
            r = np.mean(ranks[key], 0)
            mean_size = np.mean([s for _, s in reps], 0)
            result[f'{key}_a{alpha}'] = dict(bank_size=len(banks.get(key, coco)), source_rank=r[0], expanded_rank=r[1], source_top1=r[2], expanded_top10=r[3],
                                             mean_risk=float(np.mean([x for x, _ in reps])), mean_size=mean_size.tolist(), fixed_split_risk=float(fixed[0]), fixed_split_size=fixed[1].tolist())
            lines.append(f"| {key} | {len(banks.get(key, coco))} | {r[0]:.2f} | {r[1]:.2f} | {100*r[2]:.2f}% | {100*r[3]:.2f}% | {100*np.mean([x for x, _ in reps]):.2f} ({100*fixed[0]:.2f}) | "
                         + ' | '.join(f'{m:.2f} ({f:.2f})' for m, f in zip(mean_size, fixed[1]))+' |')
        lines.append('')
    lines += ['Every bank gives a candidate-independent score; the bank is part of the frozen scoring rule, so the risk guarantee holds for each. Differences are efficiency only. Development data, previously inspected; one model size.']
    (OUT/'results.json').write_text(json.dumps(result, indent=1))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
