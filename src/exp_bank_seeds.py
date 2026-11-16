"""Redraws of the 512 Open Images names in the 683-name reference bank (released weights, nothing fitted).

The 683-name bank is the 171 COCO-Stuff names plus 512 names drawn once from the Open Images list
(meta/bank_coco_oi683_v1.json). Here the 171 COCO-Stuff names stay fixed and the 512 names are redrawn with the
seeds in SEEDS. Images, pixels, prompts, candidate names and the CRC rule are those of exp_anchor_bank.py: the 400
ADE development images of the headroom probe, 845 names, image-level CRC calibrated at the 150 source names, 200
random 200/200 splits. The published draw is scored again by the same code and compared with the stored scores.

  python src/exp_bank_seeds.py --model sed
  python src/exp_bank_seeds.py --model vitl
  python src/exp_bank_seeds.py --model vitb      # no stored native scores: anchored rows only
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS, curves
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

SEEDS = [101, 102, 103, 104, 105]     # fixed 2026-11-12 before any redraw was scored; seeds 0 and 1 drew the earlier bank lists
PUBLISHED = 'published'
S, ADDITIONS = DATASETS['ade']['source'], DATASETS['ade']['additions']
STORES = dict(vitl='cache/headroom_probe_vitl_bank683', sed='cache/headroom_probe_sed_bank683', vitb=None)
RUNS = dict(vitl='results/headroom_probe_ade_vitl_bank683', sed='results/headroom_probe_ade_sed_bank683', vitb='results/headroom_probe_ade')
RANKS = ['source_rank', 'rank_at_845', 'source_top1', 'top1_at_845', 'top10_at_845']


def build_banks():
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    published = json.loads(Path('meta/bank_coco_oi683_v1.json').read_text())['names']
    assert published[:171] == coco and len(published) == 683
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']     # no evaluated label name is in this list
    banks = {PUBLISHED: published}
    for seed in SEEDS:
        banks[f'seed{seed}'] = coco+[oi[i] for i in np.random.default_rng(seed).permutation(len(oi))[:512]]
        assert len(set(banks[f'seed{seed}'])) == 683
    return banks


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True, choices=list(STORES))
    ap.add_argument('--limit', type=int, default=0, help='score only the first N images and stop before calibration (testing)')
    a = ap.parse_args()
    OUT = Path(f'results/bank_seeds_ade_{a.model}'+(f'_limit{a.limit}' if a.limit else '')); OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    ids = json.loads(Path('results/headroom_probe_ade/protocol.json').read_text())['image_ids']
    assert ids == json.loads((Path(RUNS[a.model])/'protocol.json').read_text())['image_ids']
    if a.limit: ids = ids[:a.limit]
    names = [r['prompt'] for r in load_manifest()['rows']]
    assert len(names) == S+ADDITIONS[-1]
    banks = build_banks()
    published_oi = set(banks[PUBLISHED][171:])
    protocol = dict(model=a.model, image_ids=ids, seeds=SEEDS, banks=banks,
        draw='171 COCO-Stuff names in released order, then names[permutation(len(names))[:512]] of meta/distractors_openimages_v1.json with numpy default_rng(seed)',
        shared_with_published_draw={k: len(set(v[171:]) & published_oi) for k, v in banks.items()},
        candidate_overlap={k: len(set(v) & set(names)) for k, v in banks.items()},
        hashes={p: digest(Path(p)) for p in ['src/exp_bank_seeds.py', 'src/catseg_probe_model.py', 'src/sed_probe_model.py', 'meta/natural_vocab_v1.json',
                                             'meta/bank_coco_oi683_v1.json', 'meta/distractors_openimages_v1.json']})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=1))
    state = hashlib.sha256(json.dumps([a.model, ids, banks]).encode()).hexdigest()

    if a.model == 'sed':
        from sed_probe_model import SEDProbe
        model = SEDProbe().cuda()
        context = lambda feats, ref: model.context(feats, ref, lean=True)
    else:
        model = CATSegProbe(None, dict(vitb='base', vitl='large')[a.model]).cuda()
        context = lambda feats, ref: bank_context(model, feats, ref, lean=True)
    text = model.encode_text(names)
    bank_text = {k: model.encode_text(v) for k, v in banks.items()}
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt = np.load('cache/sclip/gt150.npy')
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    widths = [S+x for x in ADDITIONS]
    stored = {k: np.load(f'{STORES[a.model]}/{k}.npy', mmap_mode='r') for k in ['native150', 'native845', 'anchored845']} if STORES[a.model] else {}
    keys = list(banks)+[f'stored_{k}' for k in stored]
    loss = {k: [] for k in keys}; size = {k: [] for k in keys}; ranks = {k: [] for k in keys}
    gap = []                                       # recomputed published draw against the stored scores, per image
    seconds, start = 0., 0
    partial = OUT/'partial.npz'
    if partial.exists():
        z = np.load(partial, allow_pickle=False)
        if str(z['state']) == state:
            start = int(z['done']); seconds = float(z['seconds']); gap = z['gap'].tolist()
            for k in keys:
                loss[k], size[k], ranks[k] = list(z[f'loss_{k}']), list(z[f'size_{k}']), z[f'ranks_{k}'].tolist()
            print(f'resuming after {start} images', flush=True)

    def record(key, logits, target):
        l, s = curves(logits, target, grid, S, widths)
        loss[key].append(l); size[key].append(s.astype(np.float32))
        valid = target < S; t = target.clamp(max=S-1)
        r0, r1 = true_ranks(logits[:, :S], t)[valid].double(), true_ranks(logits, t)[valid].double()
        ranks[key].append([r0.mean().item(), r1.mean().item(), (r0 == 1).double().mean().item(), (r1 == 1).double().mean().item(), (r1 <= 10).double().mean().item()])

    def save_partial(done):
        np.savez(partial, state=state, done=done, seconds=seconds, gap=np.array(gap).reshape(-1, 2),
                 **{f'loss_{k}': np.stack(loss[k]) for k in keys}, **{f'size_{k}': np.stack(size[k]) for k in keys}, **{f'ranks_{k}': np.array(ranks[k]) for k in keys})

    for k, index in enumerate(ids):
        if k < start: continue
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda()
        feats = model.image_features(model.windows(torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()))
        torch.cuda.synchronize(); t0 = time.perf_counter()
        for key in banks:
            prob = stitched_samples(model, model.anchored(feats, context(feats, bank_text[key]), text), y, x, H, W)
            # same float16 round trip as the stored probe scores
            logits = torch.logit(prob.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half()
            record(key, logits.double(), target)
            if key == PUBLISHED and stored:
                ref = torch.from_numpy(np.array(stored['anchored845'][k])).cuda()
                gap.append([(logits.float()-ref.float()).abs().max().item(), (logits != ref).float().mean().item()])
        torch.cuda.synchronize(); seconds += time.perf_counter()-t0
        for name, part in stored.items():
            record(f'stored_{name}', torch.from_numpy(np.array(part[k])).cuda().double(), target)
        if (k+1) % 25 == 0: save_partial(k+1)
        if k % 20 == 0:
            print(f'{k+1}/{len(ids)} top10 at 845 '+' '.join(f'{key}={ranks[key][-1][4]:.3f}' for key in banks)
                  + f' | {seconds/(k+1-start if start <= k else 1)/len(banks):.2f} s per image and bank', flush=True)
    per_bank = seconds/max(len(ids)-start, 1)/len(banks)
    gap = np.array(gap).reshape(-1, 2)
    if a.limit:
        print({key: np.round(np.mean(v, 0), 4).tolist() for key, v in ranks.items()})
        print(f'{per_bank:.2f} s per image and bank; published draw against stored scores: max |logit difference| {gap[:, 0].max() if len(gap) else float("nan"):.4f}, '
              f'entries that differ {100*gap[:, 1].mean() if len(gap) else float("nan"):.3f}%; peak memory {torch.cuda.max_memory_allocated()/2**30:.1f} GB')
        return
    loss = {k: np.stack(v) for k, v in loss.items()}; size = {k: np.stack(v) for k, v in size.items()}; ranks = {k: np.mean(v, 0) for k, v in ranks.items()}
    np.savez_compressed(OUT/'curves.npz', **{f'loss_{k}': v for k, v in loss.items()}, **{f'size_{k}': v for k, v in size.items()})

    n = len(ids)
    split_rng = np.random.default_rng(20261004); perms = [split_rng.permutation(n) for _ in range(200)]      # the splits of exp_anchor_bank.py

    def evaluate(cal_key, ev_key, alpha):
        risk, sizes = [], []
        for p in perms:
            cal, ev = p[:n//2], p[n//2:]
            g = np.flatnonzero((loss[cal_key][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
            risk.append(loss[ev_key][ev, g].mean()); sizes.append(size[ev_key][ev][:, :, g].mean(0))
        return np.array(risk), np.array(sizes)

    result = dict(model=a.model, images=n, splits=len(perms), seeds=SEEDS, additions=ADDITIONS, seconds_per_image_and_bank=per_bank,
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, alphas={})
    if len(gap):
        result['published_draw_against_stored_scores'] = dict(max_abs_logit_difference=float(gap[:, 0].max()), fraction_of_entries_that_differ=float(gap[:, 1].mean()))
    lines = ['# Redraws of the 512 Open Images names in the reference bank', '',
             f'{dict(vitb="CAT-Seg ViT-B", vitl="CAT-Seg ViT-L", sed="SED ConvNeXt-L")[a.model]}, released weights. {n} ADE development images (the bank-sweep images), {S} source names, {S+ADDITIONS[-1]} names after growth. '
             f'Every bank is the 171 COCO-Stuff names plus 512 Open Images names; `{PUBLISHED}` is the draw used in the paper, scored again here, and the others redraw the 512 names with seeds {SEEDS[0]}-{SEEDS[-1]}. '
             f'Image-level CRC calibrated once at the source names; mean over {len(perms)} random {n//2}/{n-n//2} splits, the same splits for every row. Accuracy is over source-labelled sampled pixels, image-averaged.', '']
    for alpha in ALPHAS:
        rows = {}
        native = None
        if stored:
            reused, recal = evaluate('stored_native150', 'stored_native845', alpha), evaluate('stored_native845', 'stored_native845', alpha)
            native = dict(reused_risk=float(reused[0].mean()), reused_size=float(reused[1][:, -1].mean()), recalibrated_risk=float(recal[0].mean()), recalibrated_size=float(recal[1][:, -1].mean()))
            keys_here = list(banks)+['stored_anchored845']
        else:
            keys_here = list(banks)
        for key in keys_here:
            risk, sizes = evaluate(key, key, alpha)
            rows[key] = dict(risk=float(risk.mean()), risk_split_sd=float(risk.std(ddof=1)), splits_above_alpha=float((risk > alpha).mean()), size=sizes.mean(0).tolist(),
                             size_split_sd=float(sizes[:, -1].std(ddof=1)), **dict(zip(RANKS, ranks[key].tolist())))
            if native: rows[key]['overhead'] = rows[key]['size'][-1]-native['recalibrated_size']
            if key in banks: rows[key]['open_images_names_shared_with_published'] = protocol['shared_with_published_draw'][key]
        fields = ['risk', 'size_source', 'size_grown']+(['overhead'] if native else [])+['source_top1', 'top1_at_845', 'top10_at_845']
        value = lambda r, f: r['size'][0] if f == 'size_source' else r['size'][-1] if f == 'size_grown' else r[f]
        draws = np.array([[value(rows[f'seed{s}'], f) for f in fields] for s in SEEDS])
        summary = {f: dict(mean=float(draws[:, j].mean()), sd=float(draws[:, j].std(ddof=1)), min=float(draws[:, j].min()), max=float(draws[:, j].max()), published=value(rows[PUBLISHED], f))
                   for j, f in enumerate(fields)}
        result['alphas'][str(alpha)] = dict(rows=rows, native=native, redraw_summary=summary)
        pct = lambda f: f in ('risk', 'source_top1', 'top1_at_845', 'top10_at_845')
        cell = lambda f, v: f'{100*v:.2f}' if pct(f) else f'{v:.2f}'
        head = dict(risk='Risk at 845 (%)', size_source='Size at 150', size_grown='Size at 845', overhead='Overhead', source_top1='Top-1 at 150 (%)', top1_at_845='Top-1 at 845 (%)', top10_at_845='Top-10 at 845 (%)')
        lines += [f'## alpha = {alpha}', '', '| Bank | Shared names | '+' | '.join(head[f] for f in fields)+' |', '|---|---:|'+'---:|'*len(fields)]
        for key in keys_here:
            label = 'published draw, stored scores' if key == 'stored_anchored845' else key
            lines.append(f"| {label} | {rows[key].get('open_images_names_shared_with_published', '')} | "+' | '.join(cell(f, value(rows[key], f)) for f in fields)+' |')
        lines += ['| **five redraws: mean** | | '+' | '.join(cell(f, summary[f]['mean']) for f in fields)+' |',
                  '| **five redraws: sd** | | '+' | '.join(cell(f, summary[f]['sd']) for f in fields)+' |',
                  '| **five redraws: min** | | '+' | '.join(cell(f, summary[f]['min']) for f in fields)+' |',
                  '| **five redraws: max** | | '+' | '.join(cell(f, summary[f]['max']) for f in fields)+' |', '']
        if native:
            lines += [f"Native model on the same images and splits: reused threshold {100*native['reused_risk']:.2f}% risk, {native['reused_size']:.2f} labels per pixel; "
                      f"recalibrated at 845 names {100*native['recalibrated_risk']:.2f}% risk, {native['recalibrated_size']:.2f} labels per pixel. Overhead is the anchored size at 845 minus the recalibrated native size.", '']
        lines += [f"Across the {len(perms)} splits the size at 845 of the published draw has a standard deviation of {rows[PUBLISHED]['size_split_sd']:.2f} labels per pixel "
                  f"and its risk {100*rows[PUBLISHED]['risk_split_sd']:.2f} points.", '']
    lines += ['Shared names: Open Images names a redraw has in common with the published draw. Standard deviations over redraws use n-1.']
    if len(gap):
        lines += ['', f'Published draw scored here against the stored scores: largest logit difference {gap[:, 0].max():.4f}, {100*gap[:, 1].mean():.3f}% of stored float16 entries differ.']
    lines += ['', f"{per_bank:.2f} s per image and bank on {result['gpu']} (bank pass and 845 candidates; image features excluded); peak memory {result['peak_memory_gb']:.1f} GB."]
    (OUT/'results.json').write_text(json.dumps(result, indent=1))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    partial.unlink(missing_ok=True)
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
