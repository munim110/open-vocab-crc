"""Ranking headroom probe: frozen SCLIP vs native CAT-Seg vs reference-anchored CAT-Seg.

Diagnostic only: true-label ranks at the cached sampled pixels, no calibration and no
fitting. Run with .venv-probe (see catseg_probe_model.py for the external checkout).
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, CKPT, TEMPLATE, bank_context
from diagnose_pixels import spatial_strata
from encode import ADE, sample_phi
from exp_fixed_source import digest
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

OUT = Path('results/headroom_probe_ade')
STORE = Path('cache/headroom_probe')
ARMS = ['sclip_cached', 'catseg_native', 'catseg_anchored']
GROUPS = ['all', 'boundary', 'interior', 'small_class', 'held_out', 'seen', 'name_in_coco', 'name_not_in_coco']
METRICS = ['source_rank', 'expanded_rank', 'source_top1', 'source_top10', 'expanded_top1', 'expanded_top10', 'expanded_top50']


def resize_short(img, short=640, long_max=2560):
    w, h = img.size
    scale = min(short/min(h, w), long_max/max(h, w))
    return img.resize((int(w*scale+.5), int(h*scale+.5)), Image.BILINEAR)


def stitched_samples(model, logits, y, x, H, W, block=128):
    """Official window merge, then bilinear sampling at original-image pixel centres."""
    out = []
    for i in range(0, logits.shape[1], block):
        prob = model.stitch(logits[:, i:i+block])
        out.append(sample_phi(prob[None], y, x, H, W))
    return torch.cat(out, -1).double()                               # [P,T]


def pixel_metrics(source, expanded, target):
    r0, r1 = true_ranks(source, target), true_ranks(expanded, target)
    return torch.stack([r0, r1, r0 == 1, r0 <= 10, r1 == 1, r1 <= 10, r1 <= 50], -1).double().cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--roles', default='tune_cal,tune_eval')
    ap.add_argument('--aggregator', default='', help='fine-tuned aggregator checkpoint; use with --tag')
    ap.add_argument('--size', default='base', choices=['base', 'large'], help='released CAT-Seg ViT-B or ViT-L; use with --tag')
    ap.add_argument('--bank', default='', help='JSON with a "names" list replacing the COCO-171 reference bank (any size; chunked context)')
    ap.add_argument('--tag', default='', help='suffix for the output and store directories, so earlier runs are kept')
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed', 'declip'], help='CAT-Seg (default), SED ConvNeXt-L (sed_probe_model.py) or CAT-Seg + DeCLIP EVA-L (declip_probe_model.py); use with --tag')
    ap.add_argument('--sed-fast', type=int, default=0, help='SED only: native arm uses the released fast mode with category early rejection at this top-K (0 = off)')
    ap.add_argument('--lean', action='store_true', help='bank pass stops once its key/value sums are recorded (no bank logits, no last attention output): same candidate scores, less time and memory; use with --tag')
    a = ap.parse_args()
    global OUT, STORE
    if a.tag: OUT, STORE = Path(f'{OUT}_{a.tag}'), Path(f'{STORE}_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
    ids = [r['index'] for role in a.roles.split(',') for r in split['roles'][role]]
    if a.limit: ids = ids[:a.limit]
    held = json.loads(Path('results/match_correction_sclip_ade/protocol.json').read_text())['held_out_ids']
    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:150]] == ['source']*150 and len(names) == 845
    reference = json.loads(Path(a.bank).read_text())['names'] if a.bank else json.loads((CATSEG/'datasets/coco.json').read_text())
    coco_names = set(json.loads((CATSEG/'datasets/coco.json').read_text()))
    in_coco = np.array([n in coco_names for n in names[:150]])
    protocol = dict(image_ids=ids, arms=ARMS, groups=GROUPS, metrics=METRICS,
        images=f'roles {a.roles} of the saved match-correction split (ADE validation, development data); no filtering.',
        wording='ade-natural-v1 prompts for every arm. SCLIP: 80-template bank from natural_ranks. CAT-Seg: its training template "%s".' % TEMPLATE,
        catseg='Released ViT-B checkpoint, official sliding-window inference (640 square, kernel 384, overlap .333, global view, pooling 1x1), sigmoid probabilities.',
        native='Source rank uses deployed V=150; expanded rank uses deployed V=845 (includes the native per-crop top-256 truncation).',
        anchored='Reference bank = 171 COCO-Stuff training names in released order; candidates attend to reference+padding+self only; one scoring of all 845 labels yields both ranks.',
        reference_overlap=f'{int(in_coco.sum())} of 150 source prompts are exact COCO-Stuff names.',
        scope='Ranking diagnostic on previously inspected development images. No fitting, no calibration, no reserve access. CAT-Seg was trained on COCO-Stuff; ADE images are unseen by it but many ADE concepts are not.',
        aggregator=a.aggregator or 'released', size=a.size, bank=a.bank or 'coco171', bank_size=len(reference), lean_bank_pass=a.lean,
        hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe.py', 'src/catseg_probe_model.py', 'meta/natural_vocab_v1.json', str(CKPT)]})
    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as SED_CKPT
        protocol.update(model='sed', size='convnext_large', sed_fast_topk=a.sed_fast,
            catseg='Released SED ConvNeXt-L checkpoint (CVPR 2024), whole image at 768x768 as in the release (no sliding window), 80-template ensemble, sigmoid probabilities.',
            native='Released non-fast decoder (three stages of class attention across the deployed vocabulary; no truncation)' if not a.sed_fast else
                   f'Released fast mode: category early rejection keeps labels in some pixel\'s top-{a.sed_fast} at each stage; rejected labels get probability 0.',
            anchored='Reference bank run natively; candidates attend to the bank\'s per-stage keys/values plus themselves only (sed_probe_model.py).',
            hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe.py', 'src/sed_probe_model.py', 'meta/natural_vocab_v1.json', str(SED_CKPT)]})
    elif a.model == 'declip':
        from declip_probe_model import DeCLIPProbe, CKPT as DECLIP_CKPT
        protocol.update(model='declip', size='eva02_large', catseg='Released CAT-Seg + DeCLIP EVA02-CLIP-L checkpoint (CVPR 2025, CATSeg_DeCLIP_EVA-L_DINOv2-L_csa_0.05_2.0), the same sliding-window inference and cost aggregator as CAT-Seg (declip_probe_model.py), sigmoid probabilities.',
            hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe.py', 'src/catseg_probe_model.py', 'src/declip_probe_model.py', 'meta/natural_vocab_v1.json', str(DECLIP_CKPT)]})
    else:
        protocol.update(model='catseg')
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))

    if a.model == 'sed':
        assert not a.aggregator and not a.size == 'large', 'no fine-tuned or resized SED'
        model = SEDProbe().cuda()
        if a.sed_fast: model.native = lambda feats, text: model.native_fast(feats, text, a.sed_fast)
    elif a.model == 'declip':
        assert not a.aggregator and a.size == 'base', 'released DeCLIP EVA-L only; do not pass --size'
        model = DeCLIPProbe().cuda()
    else:
        model = CATSegProbe(a.aggregator or None, a.size).cuda()
    text = model.encode_text(names)
    ref_text = model.encode_text(reference)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    cache = np.load('cache/sclip/phi.npy', mmap_mode='r') if Path('cache/sclip/phi.npy').exists() else None   # absent on the training box: SCLIP rows are then uninformative
    gt = np.load('cache/sclip/gt150.npy')
    sclip_text = torch.from_numpy(np.load('results/natural_ranks_sclip_ade/text_embeddings.npy')).cuda().float()
    stores = {k: np.lib.format.open_memmap(STORE/f'{k}.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], n))
              for k, n in [('native150', 150), ('native845', 845), ('anchored845', 845)]}
    values = np.full((len(ARMS), len(ids), len(GROUPS), len(METRICS)), np.nan)
    counts = np.zeros((len(ids), len(GROUPS)), int)
    confusion = np.zeros((len(ARMS), 150, 150), np.int64)
    seconds = np.zeros(5)
    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        lab = np.array(Image.open(Path(ADE)/'annotations/validation'/info['file'].replace('.jpg', '.png')))
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        np.testing.assert_array_equal(np.where(lab.ravel()[flat] > 0, lab.ravel()[flat].astype(int)-1, 255), gt[index])
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        feats = model.image_features(model.windows(tensor))
        torch.cuda.synchronize(); t1 = time.perf_counter()
        n150 = stitched_samples(model, model.native(feats, text[:150]), y, x, H, W)
        torch.cuda.synchronize(); t15 = time.perf_counter()     # the source pass is calibration-only; deployment runs the grown pass alone
        n845 = stitched_samples(model, model.native(feats, text), y, x, H, W)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        ctx = model.context(feats, ref_text, lean=a.lean) if (not a.bank or a.model == 'sed') else bank_context(model, feats, ref_text, lean=a.lean)
        anch = stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W)
        torch.cuda.synchronize(); t3 = time.perf_counter()
        seconds += [t1-t0, t2-t1, t3-t2, t15-t1, t2-t15]
        f = torch.from_numpy(np.array(cache[index])).cuda().float() if cache is not None else torch.zeros(meta['npix'], sclip_text.shape[1], device='cuda')
        z = 40*torch.cat([f@sclip_text[j:j+64].T for j in range(0, 845, 64)], -1).double()
        for name, scores in [('native150', n150), ('native845', n845), ('anchored845', anch)]:
            stores[name][k] = torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()
        near, area = spatial_strata(lab, flat, meta['short'])
        valid = gt[index] < 150; hm = np.isin(gt[index], held)
        coco = np.zeros_like(valid); coco[valid] = in_coco[gt[index][valid]]
        masks = [valid, valid & near, valid & ~near, valid & (area < .01), valid & hm, valid & ~hm, valid & coco, valid & ~coco]
        counts[k] = [m.sum() for m in masks]
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda().clamp(max=149)
        for ai, (source, expanded) in enumerate([(z[:, :150], z), (n150, n845), (anch[:, :150], anch)]):
            pix = pixel_metrics(source, expanded, target)
            for gi, m in enumerate(masks):
                if m.any(): values[ai, k, gi] = pix[m].mean(0)
            pred = source.argmax(-1).cpu().numpy()[valid]
            np.add.at(confusion[ai], (gt[index][valid].astype(int), pred), 1)
        if k % 20 == 0:
            print(f'{k+1}/{len(ids)} source top10 '+' '.join(f'{ARMS[i]}={values[i, k, 0, 3]:.3f}' for i in range(3)), flush=True)
    for s in stores.values(): s.flush()
    np.savez_compressed(OUT/'per_image.npz', values=values, counts=counts, image_ids=ids, confusion=confusion)

    rng = np.random.default_rng(20261001); draws = rng.integers(0, len(ids), (2000, len(ids)))
    table = []
    for ai, arm in enumerate(ARMS):
        for gi, group in enumerate(GROUPS):
            v = values[ai, :, gi]
            delta = v-values[0, :, gi]
            ci = np.nanquantile(np.nanmean(delta[draws], axis=1), [.025, .975], axis=0).T
            table.append(dict(arm=arm, group=group, images=int((counts[:, gi] > 0).sum()),
                              mean=np.nanmean(v, axis=0).tolist(), delta_vs_sclip_ci95=ci.tolist()))
    iou = []
    for c in confusion:
        inter = np.diag(c); union = c.sum(0)+c.sum(1)-inter
        iou.append(float(np.mean(inter[union > 0]/union[union > 0])))
    result = dict(rows=table, sampled_pixel_miou=dict(zip(ARMS, iou)), pixel_accuracy={a: float(np.diag(c).sum()/c.sum()) for a, c in zip(ARMS, confusion)},
                  mean_seconds_per_image=dict(clip_features=seconds[0]/len(ids), native_150_plus_845=seconds[1]/len(ids), anchored_reference_plus_845=seconds[2]/len(ids),
                                             native_150=seconds[3]/len(ids), native_845=seconds[4]/len(ids)),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = ['# Ranking headroom probe', '', f'{len(ids)} development images (roles {a.roles}), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.', '',
             '| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in table:
        m = r['mean']
        lines.append(f"| {r['arm']} | {r['group']} | {m[0]:.2f} | {m[1]:.2f} | "+' | '.join(f'{100*v:.2f}%' for v in m[2:])+' |')
    lines += ['', '| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |', '|---|---:|---:|']
    lines += [f"| {a} | {100*result['sampled_pixel_miou'][a]:.2f} | {100*result['pixel_accuracy'][a]:.2f}% |" for a in ARMS]
    lines += ['', 'Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.',
              '', f"Seconds per image on {result['gpu']}: "+', '.join(f'{k} {v:.2f}' for k, v in result['mean_seconds_per_image'].items())+f"; peak memory {result['peak_memory_gb']:.1f} GB.",
              '', 'Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.']
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
