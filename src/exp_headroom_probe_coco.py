"""COCO-Stuff 171 -> + LVIS v1 (1,283 labels) replication of exp_headroom_probe_pascal.py (same arms, same protocol).

The third benchmark (docs/COCO_LVIS_BENCHMARK.md): the first 2,000 COCO val2017 images that LVIS v1 val annotates, and
their sampled pixels (cache/coco_pixels: meta.json, gt171.npy, gtlvis.npy from build_pixel_sample.py --dataset coco).
The source vocabulary is the models' COCO-Stuff training vocabulary; val2017 is not in their training data. There is no
SCLIP arm. Development data: no fitting, no calibration here. Run with .venv-probe:

    PYTHONPATH=src python src/exp_headroom_probe_coco.py --tag T --bank meta/bank_coco_oi683_v1.json [--size large | --model sed | --model declip]

Writes results/headroom_probe_coco_<tag> and cache/headroom_probe_coco_<tag> (stores native_source, native_full,
anchored_full; float16 logits clamped to [-30, 30]).
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, TEMPLATE, CKPT, bank_context
from coco_lvis_vocab import load_manifest
from diagnose_pixels import spatial_strata
from exp_fixed_source import digest
from probe_checkpoint import Checkpoint
from exp_headroom_probe import METRICS, pixel_metrics, resize_short, stitched_samples

PIX = Path('cache/coco_pixels')
IMAGES = Path('data/coco-stuff/images/val2017')
STUFF = Path('data/coco-stuff/annotations_detectron2/val2017')
ARMS = ['catseg_native', 'catseg_anchored']
GROUPS = ['all', 'boundary', 'interior', 'small_class', 'thing', 'stuff']
S, THINGS = 171, 80


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--size', default='base', choices=['base', 'large'], help='released CAT-Seg ViT-B or ViT-L')
    ap.add_argument('--bank', required=True, help='JSON with a "names" list: the reference bank')
    ap.add_argument('--tag', required=True, help='suffix for the output and store directories')
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed', 'declip'])
    a = ap.parse_args()
    OUT, STORE = Path(f'results/headroom_probe_coco_{a.tag}'), Path(f'cache/headroom_probe_coco_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]; T = len(names)
    assert [r['role'] for r in rows[:S]] == ['source']*S
    reference = json.loads(Path(a.bank).read_text())['names']
    meta = json.loads((PIX/'meta.json').read_text())
    ids = list(range(a.limit or len(meta['meta'])))
    code = ['src/exp_headroom_probe_coco.py', 'src/exp_headroom_probe.py', 'src/coco_lvis_vocab.py', 'src/build_pixel_sample.py', 'meta/coco_lvis_natural_vocab_v1.json', a.bank]
    protocol = dict(image_ids=ids, arms=ARMS, groups=GROUPS, metrics=METRICS, source_labels=S, labels=T,
        images='The first 2,000 COCO val2017 images annotated by LVIS v1 val, sorted by file name; no filtering. Images with no valid sampled pixel are reported as NaN.',
        wording=f'coco-lvis-natural-v1 prompts for every arm. CAT-Seg: its training template "{TEMPLATE}".',
        catseg=f'Released {"ViT-L" if a.size == "large" else "ViT-B"} checkpoint, official sliding-window inference (640 square, kernel 384, overlap .333, global view), sigmoid probabilities.',
        native=f'Source rank uses deployed V={S}; expanded rank uses deployed V={T} (includes the native per-crop top-256 truncation).',
        anchored=f'Reference bank = {len(reference)} names ({a.bank}); candidates attend to reference+padding+self only.',
        scope='Development data. No fitting, no calibration, no reserve access. The source vocabulary is the COCO-Stuff training vocabulary; val2017 images are not training images.',
        model=a.model, size=a.size, bank=a.bank, bank_size=len(reference),
        hashes={p: digest(Path(p)) for p in code+['src/catseg_probe_model.py', str(CKPT)]})
    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as SED_CKPT
        assert a.size == 'base', 'no resized SED'
        protocol.update(size='convnext_large', sed_fast_topk=0,
            catseg='Released SED ConvNeXt-L checkpoint (CVPR 2024), whole image at 768x768 as in the release (no sliding window), 80-template ensemble, sigmoid probabilities.',
            native='Released non-fast decoder (three stages of class attention across the deployed vocabulary; no truncation)',
            anchored='Reference bank run natively; candidates attend to the bank\'s per-stage keys/values plus themselves only (sed_probe_model.py).',
            hashes={p: digest(Path(p)) for p in code+['src/sed_probe_model.py', str(SED_CKPT)]})
    if a.model == 'declip':
        from declip_probe_model import DeCLIPProbe, CKPT as DECLIP_CKPT
        assert a.size == 'base', 'released DeCLIP EVA-L only; do not pass --size'
        protocol.update(size='eva02_large', catseg='Released CAT-Seg + DeCLIP EVA02-CLIP-L checkpoint (CVPR 2025, CATSeg_DeCLIP_EVA-L_DINOv2-L_csa_0.05_2.0), the same sliding-window inference and cost aggregator as CAT-Seg (declip_probe_model.py), sigmoid probabilities.',
            hashes={p: digest(Path(p)) for p in code+['src/catseg_probe_model.py', 'src/declip_probe_model.py', str(DECLIP_CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))

    if a.model == 'sed': model = SEDProbe().cuda()
    elif a.model == 'declip': model = DeCLIPProbe().cuda()
    else: model = CATSegProbe(None, a.size).cuda()
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    gt, gtl = np.load(PIX/'gt171.npy'), np.load(PIX/'gtlvis.npy')
    ckpt = Checkpoint(STORE, protocol)   # resumes an interrupted run of the same protocol (probe_checkpoint.py)
    stores = ckpt.open_stores({k: ((len(ids), meta['npix'], n), np.float16) for k, n in [('native_source', S), ('native_full', T), ('anchored_full', T)]})
    values = np.full((len(ARMS), len(ids), len(GROUPS), len(METRICS)), np.nan)
    counts = np.zeros((len(ids), len(GROUPS)), int)
    confusion = np.zeros((len(ARMS), S, S), np.int64)
    seconds = np.zeros(3)
    ckpt.restore(values=values, counts=counts, confusion=confusion, seconds=seconds)
    for k, index in enumerate(ids):
        if k < ckpt.start: continue
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(IMAGES/info['file']).convert('RGB')
        stuff = np.array(Image.open(STUFF/info['file'].replace('.jpg', '.png')))
        lab = np.where(stuff == 255, 0, stuff.astype(np.int64)+1)
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        np.testing.assert_array_equal(np.where(gtl[index] != 65535, 255, stuff.ravel()[flat]), gt[index])
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        feats = model.image_features(model.windows(tensor))
        torch.cuda.synchronize(); t1 = time.perf_counter()
        ns = stitched_samples(model, model.native(feats, text[:S]), y, x, H, W)
        nf = stitched_samples(model, model.native(feats, text), y, x, H, W)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        ctx = model.context(feats, ref_text) if a.model == 'sed' else bank_context(model, feats, ref_text)
        anch = stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W)
        torch.cuda.synchronize(); t3 = time.perf_counter()
        seconds += [t1-t0, t2-t1, t3-t2]
        for name, scores in [('native_source', ns), ('native_full', nf), ('anchored_full', anch)]:
            stores[name][k] = torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()
        near, area = spatial_strata(lab, flat, meta['short'])
        valid = gt[index] < S
        masks = [valid, valid & near, valid & ~near, valid & (area < .01), valid & (gt[index] < THINGS), valid & (gt[index] >= THINGS)]
        counts[k] = [m.sum() for m in masks]
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda().clamp(max=S-1)
        for ai, (source, expanded) in enumerate([(ns, nf), (anch[:, :S], anch)]):
            pix = pixel_metrics(source, expanded, target)
            for gi, m in enumerate(masks):
                if m.any(): values[ai, k, gi] = pix[m].mean(0)
            pred = source.argmax(-1).cpu().numpy()[valid]
            np.add.at(confusion[ai], (gt[index][valid].astype(int), pred), 1)
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} source top10 '+' '.join(f'{ARMS[i]}={values[i, k, 0, 3]:.3f}' for i in range(len(ARMS))), flush=True)
        ckpt.step(k, values=values, counts=counts, confusion=confusion, seconds=seconds)
    for s in stores.values(): s.flush()
    np.savez_compressed(OUT/'per_image.npz', values=values, counts=counts, image_ids=ids, confusion=confusion)

    table = [dict(arm=arm, group=group, images=int((counts[:, gi] > 0).sum()), mean=np.nanmean(values[ai, :, gi], axis=0).tolist())
             for ai, arm in enumerate(ARMS) for gi, group in enumerate(GROUPS)]
    iou = []
    for c in confusion:
        inter = np.diag(c); union = c.sum(0)+c.sum(1)-inter
        iou.append(float(np.mean(inter[union > 0]/union[union > 0])))
    result = dict(rows=table, sampled_pixel_miou=dict(zip(ARMS, iou)), pixel_accuracy={a_: float(np.diag(c).sum()/c.sum()) for a_, c in zip(ARMS, confusion)},
                  mean_seconds_per_image=dict(clip_features=seconds[0]/len(ids), native_source_plus_full=seconds[1]/len(ids), anchored_reference_plus_full=seconds[2]/len(ids)),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30,
                  model=protocol['model'], size=protocol['size'], bank=protocol['bank'], bank_size=protocol['bank_size'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    ckpt.finish()
    lines = [f'# Ranking headroom probe, COCO-Stuff 171 -> {T} with LVIS ({a.tag})', '',
             f'{len(ids)} development images, image-averaged conditional metrics at the sampled pixels. Ranking diagnostic only.', '',
             f'| Arm | Group | Source rank | Rank at +{T-S} | Source top1 | Source top10 | +{T-S} top1 | +{T-S} top10 | +{T-S} top50 |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in table:
        m = r['mean']
        lines.append(f"| {r['arm']} | {r['group']} | {m[0]:.2f} | {m[1]:.2f} | "+' | '.join(f'{100*v:.2f}%' for v in m[2:])+' |')
    lines += ['', f'| Arm | Sampled-pixel mIoU ({S}) | Pixel accuracy |', '|---|---:|---:|']
    lines += [f"| {a_} | {100*result['sampled_pixel_miou'][a_]:.2f} | {100*result['pixel_accuracy'][a_]:.2f}% |" for a_ in ARMS]
    lines += ['', f"Seconds per image on {result['gpu']}: "+', '.join(f'{k} {v:.2f}' for k, v in result['mean_seconds_per_image'].items())+f"; peak memory {result['peak_memory_gb']:.1f} GB.",
              '', 'Sampled-pixel mIoU is a fidelity ballpark, not a benchmark number.']
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
