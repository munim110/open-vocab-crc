"""Pascal Context 59 -> 458 replication of exp_headroom_probe.py (same arms, same protocol per model).

Uses the 2,000 cached Pascal Context validation images and their cached sampled pixels (cache/pascal_sclip:
meta.json and gt59.npy; phi.npy is optional, without it the SCLIP arm is uninformative). Development data: no
fitting, no calibration here. Run with .venv-probe after pascal_natural_vocab.py and encode_pascal_natural_text.py.
Without --tag this is the released CAT-Seg ViT-B with the COCO-171 bank (results/headroom_probe_pascal); with
--tag the run goes to results/headroom_probe_pascal_<tag> and cache/headroom_probe_pascal_<tag>, and --size,
--bank, --model and --sed-fast select the configuration exactly as in exp_headroom_probe.py.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import scipy.io as sio
import torch
from PIL import Image

import pascal_labels as PL
from catseg_probe_model import CATSegProbe, CATSEG, CKPT, TEMPLATE, bank_context
from diagnose_pixels import spatial_strata
from exp_fixed_source import digest
from probe_checkpoint import Checkpoint
from exp_headroom_probe import ARMS, METRICS, pixel_metrics, resize_short, stitched_samples
from pascal_natural_vocab import load_manifest

BASE = Path('results/headroom_probe_pascal')          # the ViT-B + COCO-171 run; also holds the SCLIP text embeddings
OUT = BASE
STORE = Path('cache/headroom_probe_pascal')
GROUPS = ['all', 'boundary', 'interior', 'small_class', 'name_in_coco', 'name_not_in_coco']
S = 59


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--size', default='base', choices=['base', 'large'], help='released CAT-Seg ViT-B or ViT-L; use with --tag')
    ap.add_argument('--bank', default='', help='JSON with a "names" list replacing the COCO-171 reference bank (any size; chunked context)')
    ap.add_argument('--tag', default='', help='suffix for the output and store directories, so earlier runs are kept')
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed', 'declip'], help='CAT-Seg (default), SED ConvNeXt-L (sed_probe_model.py) or CAT-Seg + DeCLIP EVA-L (declip_probe_model.py); use with --tag')
    ap.add_argument('--sed-fast', type=int, default=0, help='SED only: native arm uses the released fast mode with category early rejection at this top-K (0 = off)')
    a = ap.parse_args()
    global OUT, STORE
    if a.tag: OUT, STORE = Path(f'{OUT}_{a.tag}'), Path(f'{STORE}_{a.tag}')
    else: assert a.size == 'base' and not a.bank and a.model == 'catseg', 'use --tag for any configuration other than ViT-B + COCO-171'
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]; T = len(names)
    assert [r['role'] for r in rows[:S]] == ['source']*S and [r['name'] for r in rows[:S]] == PL.load_59()
    coco_names = json.loads((CATSEG/'datasets/coco.json').read_text())
    reference = json.loads(Path(a.bank).read_text())['names'] if a.bank else coco_names
    in_coco = np.array([n in set(coco_names) for n in names[:S]])
    meta = json.loads(Path('cache/pascal_sclip/meta.json').read_text())
    ids = list(range(a.limit or len(meta['meta'])))
    extra = [a.bank] if a.bank else []
    protocol = dict(image_ids=ids, arms=ARMS, groups=GROUPS, metrics=METRICS, source_labels=S, labels=T,
        images='The cached Pascal Context validation images (first 2,000 of the sorted list), no filtering. Images with no valid sampled pixel are reported as NaN.',
        wording='pascal-natural-v1 prompts for every arm. SCLIP: 80-template bank. CAT-Seg: its training template "%s".' % TEMPLATE,
        catseg=f'Released {"ViT-L" if a.size == "large" else "ViT-B"} checkpoint, official sliding-window inference (640 square, kernel 384, overlap .333, global view), sigmoid probabilities.',
        native=f'Source rank uses deployed V={S}; expanded rank uses deployed V={T} (includes the native per-crop top-256 truncation).',
        anchored=f'Reference bank = {len(reference)} names ({a.bank or "171 COCO-Stuff training names in released order"}); candidates attend to reference+padding+self only.',
        reference_overlap=f'{int(in_coco.sum())} of {S} source prompts are exact COCO-Stuff names.',
        scope='Development data. No fitting, no calibration, no reserve access. CAT-Seg was trained on COCO-Stuff, whose concepts cover much of Pascal Context 59.',
        model=a.model, size=a.size, bank=a.bank or 'coco171', bank_size=len(reference),
        hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe_pascal.py', 'src/exp_headroom_probe.py', 'src/catseg_probe_model.py', 'meta/pascal_natural_vocab_v1.json', str(CKPT)]+extra})
    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as SED_CKPT
        assert a.size == 'base', 'no resized SED'
        protocol.update(size='convnext_large', sed_fast_topk=a.sed_fast,
            catseg='Released SED ConvNeXt-L checkpoint (CVPR 2024), whole image at 768x768 as in the release (no sliding window), 80-template ensemble, sigmoid probabilities.',
            native='Released non-fast decoder (three stages of class attention across the deployed vocabulary; no truncation)' if not a.sed_fast else
                   f'Released fast mode: category early rejection keeps labels in some pixel\'s top-{a.sed_fast} at each stage; rejected labels get probability 0.',
            anchored='Reference bank run natively; candidates attend to the bank\'s per-stage keys/values plus themselves only (sed_probe_model.py).',
            hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe_pascal.py', 'src/exp_headroom_probe.py', 'src/sed_probe_model.py', 'meta/pascal_natural_vocab_v1.json', str(SED_CKPT)]+extra})
    if a.model == 'declip':
        from declip_probe_model import DeCLIPProbe, CKPT as DECLIP_CKPT
        assert a.size == 'base', 'released DeCLIP EVA-L only; do not pass --size'
        protocol.update(size='eva02_large', catseg='Released CAT-Seg + DeCLIP EVA02-CLIP-L checkpoint (CVPR 2025, CATSeg_DeCLIP_EVA-L_DINOv2-L_csa_0.05_2.0), the same sliding-window inference and cost aggregator as CAT-Seg (declip_probe_model.py), sigmoid probabilities.',
            hashes={str(p): digest(Path(p)) for p in ['src/exp_headroom_probe_pascal.py', 'src/exp_headroom_probe.py', 'src/catseg_probe_model.py', 'src/declip_probe_model.py', 'meta/pascal_natural_vocab_v1.json', str(DECLIP_CKPT)]+extra})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))

    if a.model == 'sed':
        model = SEDProbe().cuda()
        if a.sed_fast: model.native = lambda feats, text: model.native_fast(feats, text, a.sed_fast)
    elif a.model == 'declip':
        model = DeCLIPProbe().cuda()
    else:
        model = CATSegProbe(None, a.size).cuda()
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    cache = np.load('cache/pascal_sclip/phi.npy', mmap_mode='r') if Path('cache/pascal_sclip/phi.npy').exists() else None   # absent on the GH200: SCLIP rows are then uninformative
    gt = np.load('cache/pascal_sclip/gt59.npy')
    coarse_lut, _ = PL.luts()
    sclip_text = torch.from_numpy(np.load(BASE/'sclip_text_embeddings.npy')).cuda().float()
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
        img = Image.open(Path(PL.VOC)/'JPEGImages'/(info['file']+'.jpg')).convert('RGB')
        raw = np.clip(sio.loadmat(str(Path(PL.PC)/'trainval'/(info['file']+'.mat')))['LabelMap'].astype(np.int64), 0, 511)
        coarse = coarse_lut[raw]
        lab = np.where(coarse == PL.IGN, 0, coarse.astype(np.int64)+1)
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        np.testing.assert_array_equal(coarse.ravel()[flat], gt[index])
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        feats = model.image_features(model.windows(tensor))
        torch.cuda.synchronize(); t1 = time.perf_counter()
        ns = stitched_samples(model, model.native(feats, text[:S]), y, x, H, W)
        nf = stitched_samples(model, model.native(feats, text), y, x, H, W)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        ctx = model.context(feats, ref_text) if (not a.bank or a.model == 'sed') else bank_context(model, feats, ref_text)
        anch = stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W)
        torch.cuda.synchronize(); t3 = time.perf_counter()
        seconds += [t1-t0, t2-t1, t3-t2]
        f = torch.from_numpy(np.array(cache[index])).cuda().float() if cache is not None else torch.zeros(meta['npix'], sclip_text.shape[1], device='cuda')
        z = 40*torch.cat([f@sclip_text[j:j+64].T for j in range(0, T, 64)], -1).double()
        for name, scores in [('native_source', ns), ('native_full', nf), ('anchored_full', anch)]:
            stores[name][k] = torch.logit(scores.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()
        near, area = spatial_strata(lab, flat, meta['short'])
        valid = gt[index] < S
        coco = np.zeros_like(valid); coco[valid] = in_coco[gt[index][valid]]
        masks = [valid, valid & near, valid & ~near, valid & (area < .01), valid & coco, valid & ~coco]
        counts[k] = [m.sum() for m in masks]
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda().clamp(max=S-1)
        for ai, (source, expanded) in enumerate([(z[:, :S], z), (ns, nf), (anch[:, :S], anch)]):
            pix = pixel_metrics(source, expanded, target)
            for gi, m in enumerate(masks):
                if m.any(): values[ai, k, gi] = pix[m].mean(0)
            pred = source.argmax(-1).cpu().numpy()[valid]
            np.add.at(confusion[ai], (gt[index][valid].astype(int), pred), 1)
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} source top10 '+' '.join(f'{ARMS[i]}={values[i, k, 0, 3]:.3f}' for i in range(3)), flush=True)
        ckpt.step(k, values=values, counts=counts, confusion=confusion, seconds=seconds)
    for s in stores.values(): s.flush()
    np.savez_compressed(OUT/'per_image.npz', values=values, counts=counts, image_ids=ids, confusion=confusion)

    table = [dict(arm=arm, group=group, images=int((counts[:, gi] > 0).sum()), mean=np.nanmean(values[ai, :, gi], axis=0).tolist())
             for ai, arm in enumerate(ARMS) for gi, group in enumerate(GROUPS)]
    iou = []
    for c in confusion:
        inter = np.diag(c); union = c.sum(0)+c.sum(1)-inter
        iou.append(float(np.mean(inter[union > 0]/union[union > 0])))
    result = dict(rows=table, sampled_pixel_miou=dict(zip(ARMS, iou)), pixel_accuracy={a: float(np.diag(c).sum()/c.sum()) for a, c in zip(ARMS, confusion)},
                  mean_seconds_per_image=dict(clip_features=seconds[0]/len(ids), native_source_plus_full=seconds[1]/len(ids), anchored_reference_plus_full=seconds[2]/len(ids)),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30,
                  model=protocol['model'], size=protocol['size'], bank=protocol['bank'], bank_size=protocol['bank_size'], sclip_arm_informative=cache is not None)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    ckpt.finish()
    lines = [f'# Ranking headroom probe, Pascal Context 59 -> 458 ({a.tag or "ViT-B, COCO-171 bank"})', '',
             f'{len(ids)} development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only.'+('' if cache is not None else ' SCLIP rows are uninformative (no cached SCLIP features on this machine).'), '',
             f'| Arm | Group | Source rank | Rank at +{T-S} | Source top1 | Source top10 | +{T-S} top1 | +{T-S} top10 | +{T-S} top50 |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in table:
        m = r['mean']
        lines.append(f"| {r['arm']} | {r['group']} | {m[0]:.2f} | {m[1]:.2f} | "+' | '.join(f'{100*v:.2f}%' for v in m[2:])+' |')
    lines += ['', '| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |', '|---|---:|---:|']
    lines += [f"| {a} | {100*result['sampled_pixel_miou'][a]:.2f} | {100*result['pixel_accuracy'][a]:.2f}% |" for a in ARMS]
    lines += ['', f"Seconds per image on {result['gpu']}: "+', '.join(f'{k} {v:.2f}' for k, v in result['mean_seconds_per_image'].items())+f"; peak memory {result['peak_memory_gb']:.1f} GB.",
              '', f"{protocol['reference_overlap']} Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number."]
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
