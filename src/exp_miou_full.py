"""Full-resolution mIoU of the released and the reference-anchored models on the standard open-vocabulary benchmarks.

Answers "did the conversion break the segmenter?": the same forward passes as exp_headroom_probe.py (official CAT-Seg
sliding-window inference at 640, SED whole image at 768), but instead of sampling pixels the stitched probabilities are
resampled to the annotation resolution and arg-maxed, and the confusion matrix is accumulated over the whole validation
set as detectron2's SemSegEvaluator does (mIoU over the classes that have ground-truth pixels). Arms: native (deployed
vocabulary = benchmark vocabulary, released behaviour including CAT-Seg's per-crop top-256 truncation above 256 labels),
anchored on the COCO-171 bank, anchored on the 683-name bank. Class names are the benchmark files shipped with the
CAT-Seg checkout (datasets/*.json); names with several synonyms are embedded as the releases do, one prompt per synonym,
averaged. Benchmarks: ade150 (the 2,000 ADE validation images), ade847 (same images, ADE20K-full masks from build_gt.py
on the A-150 grid), pc459 / pc59 (Pascal Context validation, CAT-Seg's 5,105-image list; pc459 keeps 'unknown' as a
class as the released preparation does). Development data; nothing is fitted; the confirmation reserve is untouched.
Run with .venv-probe.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import scipy.io as sio
import torch
import torch.nn.functional as F
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, CKPT, bank_context
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short

PASCAL = Path('data/pascal')
ARMS = ['native', 'anchored_coco171', 'anchored_bank683']


def benchmark_names(dataset):
    return json.loads((CATSEG/'datasets'/f'{dataset}.json').read_text())


def encode_names(model, names):
    """CAT-Seg / SED class_embeddings: one prompt per comma-separated synonym, embeddings averaged and re-normalised."""
    syns = [n.split(', ') if ', ' in n else [n] for n in names]
    flat = [s for ss in syns for s in ss]
    E = model.encode_text(flat)
    idx = np.cumsum([0]+[len(s) for s in syns])
    return torch.stack([F.normalize(E[idx[i]:idx[i+1]].mean(0), dim=-1) for i in range(len(names))])


def ade_items(dataset, limit):
    meta = json.loads(Path('cache/sclip/meta.json').read_text())['meta']
    items = []
    for info in meta[:limit or None]:
        stem = info['file'].replace('.jpg', '')
        items.append((stem, Path(ADE)/'images/validation'/info['file'], (dataset, stem)))
    return items


def load_gt(dataset, key, K, pc_lut=None):
    """Annotation as int64 [H, W] with -1 for ignore."""
    kind, stem = key
    if kind == 'ade150':
        lab = np.array(Image.open(Path(ADE)/'annotations/validation'/f'{stem}.png')).astype(np.int64)
        return lab-1                                                          # 0 = ignore
    if kind == 'ade847':
        lab = np.load(f'data/gt847/{stem}.npy').astype(np.int64)
        return np.where(lab == 65535, -1, lab)
    raw = np.clip(sio.loadmat(str(PASCAL/'trainval'/f'{stem}.mat'))['LabelMap'].astype(np.int64), 0, 511)
    assert raw.min() >= 1, stem
    return pc_lut[raw]


def pascal_items(dataset, limit):
    ids = [l.strip() for l in (CATSEG/'datasets/pascalcontext_val.txt').read_text().splitlines() if l.strip()]
    return [(i, PASCAL/'VOCdevkit/VOC2010/JPEGImages'/f'{i}.jpg', (dataset, i)) for i in ids[:limit or None]]


PC59_IDS = sorted([2, 259, 260, 415, 324, 9, 258, 144, 18, 19, 22, 23, 397, 25, 284, 158, 159, 416, 33, 162, 420, 454, 295, 296, 427, 44, 45, 46, 308, 59,
                   440, 445, 31, 232, 65, 354, 424, 68, 326, 72, 458, 34, 207, 80, 355, 85, 347, 220, 349, 360, 98, 187, 104, 105, 366, 189, 368, 113, 115])   # released prepare_pascal_context_59.py (id 0 = ignore dropped)


def pascal_lut(dataset, names):
    """Raw .mat value (1..459) -> benchmark index. pc459 as the released preparation (value - 1, 'unknown' kept; the shipped
    pc459.json is labels.txt order with spaces removed from multi-word names, used verbatim as the released numbers were);
    pc59 through the released 59-id mapping (alphabetical, so pc59.json order)."""
    n459 = {}
    for line in (PASCAL/'labels.txt').read_text().splitlines():
        if ':' in line:
            i, n = line.split(':', 1); n459[int(i)] = n.strip()
    norm = lambda n: {'diningtable': 'table'}.get(n.replace(' ', ''), n.replace(' ', ''))   # pc59.json calls id 397 ('table') 'diningtable'
    lut = np.full(512, -1, np.int64)
    if dataset == 'pc459':
        assert [norm(n459[i]) for i in range(1, 460)] == [norm(n) for n in names], 'pc459.json is not labels.txt order'
        lut[1:460] = np.arange(459)
    else:
        assert [norm(n459[i]) for i in PC59_IDS] == [norm(n) for n in names], 'pc59.json is not the released 59-id order'
        lut[PC59_IDS] = np.arange(59)
    return lut


@torch.no_grad()
def argmax_full(model, logits, H, W, chunk=96):
    """Stitch label chunks to the model's output square, resample to the annotation grid, running arg-max."""
    best = arg = None
    for i in range(0, logits.shape[1], chunk):
        p = F.interpolate(model.stitch(logits[:, i:i+chunk])[None], size=(H, W), mode='bilinear', align_corners=False)[0]
        m, a = p.max(0)
        if best is None: best, arg = m, a+i
        else:
            upd = m > best; best = torch.where(upd, m, best); arg = torch.where(upd, a+i, arg)
    return arg


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed', 'declip'])
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--dataset', default='ade150', choices=['ade150', 'ade847', 'pc459', 'pc59'])
    ap.add_argument('--bank683', default='meta/bank_coco_oi683_v1.json')
    ap.add_argument('--arms', default=','.join(ARMS))
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--tag', default='', help='output suffix (default: model/size)')
    ap.add_argument('--global-view', default='square', choices=['square', 'original'],
                    help='CAT-Seg global view resized from the 640 square (default, every paper run) or from the input image as the upstream release does')
    ap.add_argument('--synonyms', default='mean', choices=['mean', 'first'],
                    help='average the synonym embeddings (default, every paper run) or take the first synonym as the upstream test-time forward does')
    a = ap.parse_args()
    tag = a.tag or (a.model if a.model in ('sed', 'declip') else {'base': 'vitb', 'large': 'vitl'}[a.size])
    OUT = Path(f'results/miou_full_{a.dataset}_{tag}'); OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    arms = a.arms.split(',')
    names = benchmark_names(a.dataset); K = len(names)
    coco = json.loads((CATSEG/'datasets/coco.json').read_text())
    bank683 = json.loads(Path(a.bank683).read_text())['names']
    if a.dataset.startswith('ade'):
        items, lut = ade_items(a.dataset, a.limit), None
    else:
        items, lut = pascal_items(a.dataset, a.limit), pascal_lut(a.dataset, names)
    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT as SED_CKPT
        assert a.size == 'large'; model = SEDProbe().cuda(); ckpt = SED_CKPT
    elif a.model == 'declip':
        from declip_probe_model import DeCLIPProbe, CKPT as DECLIP_CKPT
        assert a.size == 'large'; model = DeCLIPProbe().cuda(); ckpt = DECLIP_CKPT
    else:
        model = CATSegProbe(None, a.size).cuda(); ckpt = CKPT if a.size == 'base' else CKPT.with_name('model_large.pth')
    text = encode_names(model, names) if a.synonyms == 'mean' else model.encode_text([n.split(', ')[0] for n in names])
    ref = {'anchored_coco171': model.encode_text(coco), 'anchored_bank683': model.encode_text(bank683)}
    protocol = dict(model=a.model, size=a.size, dataset=a.dataset, global_view=a.global_view, synonyms=a.synonyms, classes=K, images=len(items), arms=arms, bank683=a.bank683,
        names='CAT-Seg checkout datasets/%s.json; synonyms embedded separately and averaged (released class_embeddings).' % a.dataset,
        inference='Official CAT-Seg sliding window (640 square, kernel 384, overlap .333, global view, pooling 1x1), sigmoid, fold, bilinear to the annotation grid, arg-max.' if a.model in ('catseg', 'declip')
                  else 'Released SED whole image at 768x768, sigmoid, bilinear to the annotation grid, arg-max.',
        native='Deployed vocabulary = benchmark vocabulary (released behaviour; per-crop top-256 truncation for CAT-Seg above 256 labels).',
        anchored='Reference-anchored forward (candidates attend to the bank plus themselves only), same class names; bank = COCO-171 or the 683-name bank.',
        metric='Confusion over all annotated pixels; mIoU over classes with ground-truth pixels (detectron2 SemSegEvaluator convention); pc459 keeps "unknown" as a class as in the released preparation.',
        scope='Development data (ADE validation, Pascal Context validation); nothing is fitted; no reserve access.',
        hashes={str(p): digest(Path(p)) for p in ['src/exp_miou_full.py', 'src/catseg_probe_model.py', 'src/sed_probe_model.py', 'src/declip_probe_model.py', str(ckpt)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    conf = {arm: torch.zeros(K*K, dtype=torch.long, device='cuda') for arm in arms}
    seconds = dict.fromkeys(arms, 0.); t_feat = 0.
    for k, (stem, path, key) in enumerate(items):
        gt = torch.from_numpy(load_gt(a.dataset, key, K, lut)).cuda(); H, W = gt.shape
        valid = gt >= 0
        img = Image.open(path).convert('RGB')
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        windows = model.windows(tensor)
        if a.global_view == 'original':
            assert a.model in ('catseg', 'declip')
            windows = torch.cat([windows[:-1], F.interpolate(tensor[None], size=(384, 384), mode='bilinear', align_corners=False)])
        feats = model.image_features(windows)
        torch.cuda.synchronize(); t_feat += time.perf_counter()-t0
        for arm in arms:
            torch.cuda.synchronize(); t0 = time.perf_counter()
            if arm == 'native':
                logits = model.native(feats, text)
            else:
                ctx = model.context(feats, ref[arm]) if (a.model == 'sed' or arm == 'anchored_coco171') else bank_context(model, feats, ref[arm])
                logits = model.anchored(feats, ctx, text)
            pred = argmax_full(model, logits, H, W)
            conf[arm] += torch.bincount((gt[valid]*K+pred[valid]), minlength=K*K)
            torch.cuda.synchronize(); seconds[arm] += time.perf_counter()-t0
        if k % 100 == 0:
            print(f'{k+1}/{len(items)} '+' '.join(f'{arm}={100*miou(conf[arm].view(K, K))[0]:.2f}' for arm in arms), flush=True)
    result = dict(images=len(items), classes=K, per_arm={}, seconds_per_image=dict(features=t_feat/len(items), **{arm: s/len(items) for arm, s in seconds.items()}),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    for arm in arms:
        c = conf[arm].view(K, K); m, iou, present = miou(c)
        result['per_arm'][arm] = dict(miou=m, pixel_accuracy=float(c.diag().sum()/c.sum()), classes_present=int(present.sum()), per_class_iou=iou.tolist())
    np.savez_compressed(OUT/'confusion.npz', **{arm: conf[arm].view(K, K).cpu().numpy() for arm in arms})
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = [f'# Full-resolution mIoU, {a.dataset} ({K} classes), {a.model} {a.size}', '', f'{len(items)} validation images; arg-max prediction; mIoU over classes with ground-truth pixels.', '',
             '| Arm | mIoU | Pixel accuracy | Seconds / image |', '|---|---:|---:|---:|']
    lines += [f"| {arm} | {100*result['per_arm'][arm]['miou']:.2f} | {100*result['per_arm'][arm]['pixel_accuracy']:.2f}% | {result['seconds_per_image'][arm]:.2f} |" for arm in arms]
    lines += ['', f"Features {result['seconds_per_image']['features']:.2f} s/image on {result['gpu']}; peak memory {result['peak_memory_gb']:.1f} GB. Development data; nothing fitted."]
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


def miou(c):
    inter = c.diag().double(); union = (c.sum(0)+c.sum(1)).double()-inter
    present = c.sum(1) > 0
    iou = torch.where(union > 0, inter/union.clamp(min=1), torch.zeros_like(inter))
    return float(iou[present].mean()) if present.any() else float('nan'), iou.cpu().numpy(), present.cpu().numpy()


if __name__ == '__main__':
    main()
