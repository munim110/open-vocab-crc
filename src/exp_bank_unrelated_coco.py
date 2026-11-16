"""Unrelated reference banks: what the conversion does when the bank is not a list of visual categories.

Same protocol as exp_bank_select_coco.py (same 500 COCO-Stuff val2017 images, pixel samples, 171 -> 866 growth, CRC
splits), with banks from meta/bank_unrelated_v1.json (build_unrelated_banks.py): 683 abstract WordNet nouns, 683
pronounceable non-words, and the COCO-171 core extended by 512 of each (the counterparts of the 683-name bank). Three
banks of the selection run (COCO-171, COCO + OI 683, OI 683) and native recalibrated are re-scored as references, which
also checks this machine against that run. Released weights; nothing fitted; no ADE20K or Pascal Context image is read.

    PYTHONPATH=src python src/exp_bank_unrelated_coco.py [--size large] [--images 500] [--tag T] [--smoke]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from exp_bank_select_coco import COCO, S, GROWTH, SEED, bank_list
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import curves

REFERENCE = ['coco171', 'coco_oi683', 'oi683']


def unrelated_banks(coco):
    u = json.loads(Path('meta/bank_unrelated_v1.json').read_text())
    return dict(abstract683=u['abstract'][:683], pseudo683=u['pseudo'][:683],
                coco_abstract683=list(coco)+u['abstract'][:512], coco_pseudo683=list(coco)+u['pseudo'][:512])


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--images', type=int, default=500)
    ap.add_argument('--npix', type=int, default=4096)
    ap.add_argument('--tag', default='')
    ap.add_argument('--smoke', action='store_true', help='two images, print, write nothing')
    a = ap.parse_args()
    out = Path(f'results/bank_unrelated_coco{"_" + a.tag if a.tag else ""}')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    assert len(coco) == S
    ref, growth = bank_list(coco)
    banks = {k: ref[k] for k in REFERENCE} | unrelated_banks(coco)
    assert not {n.lower() for n in growth} & {n.lower() for k in unrelated_banks(coco) for n in banks[k]}
    files = sorted(p.name for p in (COCO/'images/val2017').glob('*.jpg'))
    assert len(files) == 5000, len(files)
    files = [files[i] for i in sorted(np.random.default_rng(SEED).choice(len(files), a.images, replace=False))]
    if not a.smoke:
        out.mkdir(parents=True, exist_ok=True)
        (out/'protocol.json').write_text(json.dumps(dict(images=files, size=a.size, npix=a.npix, seed=SEED, growth=growth, banks=banks,
            hashes={p: digest(Path(p)) for p in ['src/exp_bank_unrelated_coco.py', 'src/exp_bank_select_coco.py', 'src/catseg_probe_model.py',
                                                 'meta/distractors_openimages_v1.json', 'meta/bank_unrelated_v1.json']}), indent=1))

    model = CATSegProbe(None, a.size).cuda()
    text = model.encode_text(coco + growth)
    bank_text = {k: model.encode_text(v) for k, v in banks.items()}
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    widths = [S, S+GROWTH]
    arms = ['native_grown', *banks]
    loss = {k: [] for k in arms}; size = {k: [] for k in arms}
    for k, fn in enumerate(files[:2] if a.smoke else files):
        img = Image.open(COCO/'images/val2017'/fn).convert('RGB'); W, H = img.size
        lab = np.array(Image.open(COCO/'annotations_detectron2/val2017'/fn.replace('.jpg', '.png')))
        assert lab.shape == (H, W)
        flat = np.random.default_rng(SEED+k).choice(H*W, a.npix, replace=False)
        target = torch.from_numpy(lab.ravel()[flat].astype(np.int64)).cuda()          # 0..170, 255 ignore (>= S)
        if not (target < S).any():
            continue
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        feats = model.image_features(model.windows(torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()))

        def record(key, prob):   # same float16 logit round trip as the stored probe scores
            l, s = curves(torch.logit(prob.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().double(), target, grid, S, widths)
            loss[key].append(l); size[key].append(s.astype(np.float32))

        record('native_grown', stitched_samples(model, model.native(feats, text), y, x, H, W))
        for key in banks:   # windows are independent; one at a time bounds memory
            parts = [bank_context(model, (feats[0][i:i+1], [g[i:i+1] for g in feats[1]]), bank_text[key]) for i in range(feats[0].shape[0])]
            ctx = dict(g_app=torch.cat([c['g_app'] for c in parts]), g_dec=[torch.cat(g) for g in zip(*[c['g_dec'] for c in parts])],
                       sums=[(torch.cat([c['sums'][j][0] for c in parts]), torch.cat([c['sums'][j][1] for c in parts])) for j in range(len(parts[0]['sums']))])
            record(key, stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W))
        if a.smoke:
            print(fn, {key: round(float(size[key][-1][1, np.flatnonzero(loss[key][-1] <= .1)[-1]]), 2) for key in arms}, flush=True)
        elif k % 25 == 0:
            print(f'{k+1}/{len(files)}', flush=True)
    if a.smoke:
        return

    loss = {k: np.stack(v) for k, v in loss.items()}; size = {k: np.stack(v) for k, v in size.items()}
    n = len(loss['coco171'])
    np.savez_compressed(out/'curves.npz', **{f'loss_{k}': v for k, v in loss.items()}, **{f'size_{k}': v for k, v in size.items()})
    rng = np.random.default_rng(20261004); perms = [rng.permutation(n) for _ in range(200)]      # the selection run's splits
    result = dict(images=n, excluded=len(files)-n, size=a.size, banks={k: len(v) for k, v in banks.items()}, alphas={})
    lines = ['# Unrelated reference banks on COCO-Stuff validation images', '',
             f'CAT-Seg {"ViT-L" if a.size == "large" else "ViT-B"}, released weights. {n} COCO-Stuff val2017 images ({len(files)-n} excluded), '
             f'{a.npix} sampled pixels each; source = the {S} COCO-Stuff names, grown by {GROWTH} Open Images names in no bank; protocol and splits '
             'of exp_bank_select_coco.py. abstract = WordNet nouns with only abstract senses; pseudo = pronounceable non-words; coco_* = the COCO-171 '
             'core plus 512 of them. Anchored thresholds frozen; native recalibrated on the grown vocabulary. No ADE20K or Pascal Context image is read.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', f'| Arm | Labels in bank | Risk (%) | Splits above alpha (%) | Size at {S} | Size at {S+GROWTH} |',
                  '|---|---:|---:|---:|---:|---:|']
        rows = {}
        for key in arms:
            reps = []
            for p in perms:
                cal, ev = p[:n//2], p[n//2:]
                g = np.flatnonzero((loss[key][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
                reps.append((loss[key][ev, g].mean(), size[key][ev][:, :, g].mean(0)))
            risk = float(np.mean([r for r, _ in reps])); above = float(np.mean([r > alpha for r, _ in reps])); sz = np.mean([s for _, s in reps], 0)
            rows[key] = dict(bank_size=len(banks.get(key, [])), risk=risk, above=above, size_source=float(sz[0]), size_grown=float(sz[1]))
            lines.append(f"| {key} | {'--' if key == 'native_grown' else len(banks[key])} | {100*risk:.2f} | {100*above:.1f} | {sz[0]:.2f} | {sz[1]:.2f} |")
        result['alphas'][str(alpha)] = dict(rows=rows)
        lines.append('')
    (out/'results.json').write_text(json.dumps(result, indent=1))
    (out/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
