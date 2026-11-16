"""Bank size chosen on the training domain: the bank list of the ADE20K sweep, scored on COCO-Stuff validation images.

The paper's 683-name bank was chosen on ADE20K development images (results/anchor_bank*_ade). This run asks whether
the same choice is reached without any evaluation dataset. CAT-Seg was trained on COCO-Stuff train2017; its val2017
images are neither training nor evaluation data in the paper. The banks are exactly those of the ADE sweep (rebuilt
here from the same seeds and checked against meta/bank_coco_oi*_v1.json), minus the Pascal-name bank. The vocabulary
is the 171 COCO-Stuff names (source, annotated) grown by 695 Open Images names that are in no bank (unannotated, so
they only enlarge the sets), mirroring ADE20K 150 -> 845.

Criterion, fixed before scoring: the anchored set size at the grown vocabulary under the CRC threshold calibrated on
the source labels, alpha = 0.10, mean over 200 random half/half splits. The released native model recalibrated on the
grown vocabulary is scored for reference (the price). Released weights; nothing fitted; no ADE20K or Pascal Context
image is read (the Open Images list was filtered against their label names when it was built).

    PYTHONPATH=src python src/exp_bank_select_coco.py [--size large] [--images 500] [--tag T] [--smoke]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from exp_anchor_bank import padding_only_context
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import curves
from pascal_natural_vocab import load_manifest as load_pascal

COCO = Path('data/coco-stuff')
S, GROWTH = 171, 695
SEED = 20260924           # image draw, pixel sample and growth names of this experiment


def bank_list(coco):
    """The ADE sweep's banks, from the same seeds (exp_anchor_bank.py), without the Pascal-name bank."""
    oi_all = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    rng = np.random.default_rng(0)
    c85 = [coco[i] for i in sorted(rng.choice(171, 85, replace=False))]
    c20 = [coco[i] for i in sorted(rng.choice(171, 20, replace=False))]
    pool = [r['prompt'] for r in load_pascal()['rows'] if r['prompt'] not in set(coco)]
    rng.choice(len(pool), 171, replace=False)                        # advances the generator exactly as the sweep did
    oi0 = [oi_all[i] for i in rng.permutation(len(oi_all))]
    oi1 = [oi_all[i] for i in np.random.default_rng(1).permutation(len(oi_all))]
    banks = dict(candidate_only=[], coco20=c20, coco85=c85, coco171=list(coco), coco_oi255=coco+oi0[:84], coco_oi342=coco+oi0[:171],
                 coco_oi683=coco+oi0[:512], coco_oi1366=coco+oi1[:1195], coco_oi2731=coco+oi1[:2560], coco_oi5462=coco+oi1[:5291],
                 oi683=oi1[:683])
    for n in [683, 1366, 2731]:
        assert banks[f'coco_oi{n}'] == json.loads(Path(f'meta/bank_coco_oi{n}_v1.json').read_text())['names'], n
    used = set().union(*banks.values())
    free = sorted(set(oi_all) - used - set(coco))
    growth = [free[i] for i in sorted(np.random.default_rng(SEED).choice(len(free), GROWTH, replace=False))]
    return banks, growth


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--images', type=int, default=500)
    ap.add_argument('--npix', type=int, default=4096)
    ap.add_argument('--tag', default='')
    ap.add_argument('--smoke', action='store_true', help='two images, print, write nothing')
    a = ap.parse_args()
    out = Path(f'results/bank_select_coco{"_" + a.tag if a.tag else ""}')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    assert len(coco) == S
    banks, growth = bank_list(coco)
    files = sorted(p.name for p in (COCO/'images/val2017').glob('*.jpg'))
    assert len(files) == 5000, len(files)
    files = [files[i] for i in sorted(np.random.default_rng(SEED).choice(len(files), a.images, replace=False))]
    if not a.smoke:
        out.mkdir(parents=True, exist_ok=True)
        (out/'protocol.json').write_text(json.dumps(dict(images=files, size=a.size, npix=a.npix, seed=SEED, growth=growth, banks=banks,
            hashes={p: digest(Path(p)) for p in ['src/exp_bank_select_coco.py', 'src/catseg_probe_model.py', 'meta/distractors_openimages_v1.json']}), indent=1))

    model = CATSegProbe(None, a.size).cuda()
    text = model.encode_text(coco + growth)
    bank_text = {k: model.encode_text(v) for k, v in banks.items() if v}
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
        for key, names in banks.items():
            if not names: ctx = padding_only_context(model, feats)
            else:   # windows are independent; one at a time bounds memory for the large banks
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
    rng =np.random.default_rng(20261004); perms = [rng.permutation(n) for _ in range(200)]
    result = dict(images=n, excluded=len(files)-n, size=a.size, banks={k: len(v) for k, v in banks.items()}, alphas={})
    lines = ['# Bank size chosen on COCO-Stuff validation images', '',
             f'CAT-Seg {"ViT-L" if a.size == "large" else "ViT-B"}, released weights. {n} COCO-Stuff val2017 images ({len(files)-n} without a source-labelled sampled pixel excluded), '
             f'{a.npix} sampled pixels each; source = the {S} COCO-Stuff names, grown by {GROWTH} Open Images names that are in no bank. '
             'Image-level CRC calibrated on the source labels; mean over 200 random half/half splits. Anchored thresholds are frozen (the source-label '
             'loss does not depend on the other candidates); native is recalibrated on the grown vocabulary. No ADE20K or Pascal Context image is read.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', f'| Arm | Labels in bank | Risk (%) | Size at {S} | Size at {S+GROWTH} |', '|---|---:|---:|---:|---:|']
        rows = {}
        for key in arms:
            reps = []
            for p in perms:
                cal, ev = p[:n//2], p[n//2:]
                g = np.flatnonzero((loss[key][cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
                reps.append((loss[key][ev, g].mean(), size[key][ev][:, :, g].mean(0)))
            risk = float(np.mean([r for r, _ in reps])); sz = np.mean([s for _, s in reps], 0)
            rows[key] = dict(bank_size=len(banks.get(key, [])), risk=risk, size_source=float(sz[0]), size_grown=float(sz[1]))
            lines.append(f"| {key} | {'--' if key == 'native_grown' else len(banks[key])} | {100*risk:.2f} | {sz[0]:.2f} | {sz[1]:.2f} |")
        best = min((k for k in banks), key=lambda k: rows[k]['size_grown'])
        result['alphas'][str(alpha)] = dict(rows=rows, smallest_grown_set=best)
        lines += ['', f'Smallest anchored set at {S+GROWTH} labels: **{best}** ({rows[best]["size_grown"]:.2f} labels per pixel; '
                      f'native recalibrated {rows["native_grown"]["size_grown"]:.2f}).', '']
    (out/'results.json').write_text(json.dumps(result, indent=1))
    (out/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
