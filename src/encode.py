"""Stage A: cache vocabulary-independent per-pixel features Phi for ADE20K val.

Reproduces the SCLIP / NACLIP dense-inference pipeline exactly up to (but not
including) the text matmul. Everything after `feats @ T.t()` in those pipelines
(bilinear upsample, slide-window accumulation, /count_mat, final upsample) is
linear, so per-pixel logits factor as Phi(p) . T_c with Phi independent of the
vocabulary. We therefore cache Phi at a fixed random pixel subsample and every
vocabulary configuration later costs one matmul.
"""
import os, sys, json, argparse
import numpy as np, torch, torch.nn.functional as F, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import ROOT

ADE = os.path.join(ROOT, 'data/ADEChallengeData2016')
GT847 = os.path.join(ROOT, 'data/gt847')
MEAN = torch.tensor([122.771, 116.746, 104.094]).view(3, 1, 1)
STD = torch.tensor([68.501, 66.632, 70.323]).view(3, 1, 1)
IGN = 65535


def resize_keep_ratio(img, short=336, long_max=2048):
    h, w = img.shape[:2]
    scale = min(long_max / max(h, w), short / min(h, w))
    nh, nw = int(h * scale + 0.5), int(w * scale + 0.5)
    return cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)


@torch.no_grad()
def dense_feature_map(net, img_t, crop=224, stride=112, backbone='sclip'):
    """Stitched, count-normalised dense feature map at the resized resolution."""
    _, _, H, W = img_t.shape
    hg = max(H - crop + stride - 1, 0) // stride + 1
    wg = max(W - crop + stride - 1, 0) // stride + 1
    boxes, crops = [], []
    for hi in range(hg):
        for wi in range(wg):
            y1, x1 = hi * stride, wi * stride
            y2, x2 = min(y1 + crop, H), min(x1 + crop, W)
            y1, x1 = max(y2 - crop, 0), max(x2 - crop, 0)
            boxes.append((y1, y2, x1, x2)); crops.append(img_t[:, :, y1:y2, x1:x2])
    acc = None; cnt = torch.zeros(1, 1, H, W, device=img_t.device, dtype=torch.float32)
    # group crops by shape so we can batch
    from collections import defaultdict
    groups = defaultdict(list)
    for i, c in enumerate(crops): groups[tuple(c.shape[-2:])].append(i)
    for shp, idxs in groups.items():
        batch = torch.cat([crops[i] for i in idxs], 0)
        if backbone == 'sclip':
            f = net.encode_image(batch, return_all=True, csa=True)
        else:
            f = net.encode_image(batch, return_all=True)
        f = f / f.norm(dim=-1, keepdim=True)
        f = f[:, 1:]                                     # drop CLS
        ph, pw = shp[0] // net.visual.patch_size, shp[1] // net.visual.patch_size
        D = f.shape[-1]
        f = f.permute(0, 2, 1).reshape(-1, D, ph, pw).float()
        f = F.interpolate(f, size=shp, mode='bilinear', align_corners=False)
        if acc is None:
            acc = torch.zeros(1, D, H, W, device=img_t.device, dtype=torch.float32)
        for j, i in enumerate(idxs):
            y1, y2, x1, x2 = boxes[i]
            acc[:, :, y1:y2, x1:x2] += f[j]
            cnt[:, :, y1:y2, x1:x2] += 1
    assert (cnt == 0).sum() == 0
    return acc / cnt


@torch.no_grad()
def sample_phi(fmap, ys, xs, H, W):
    """Bilinear-sample fmap at target-grid pixels (ys,xs) of an HxW image.

    Equivalent to F.interpolate(fmap, (H,W), 'bilinear', align_corners=False)
    followed by a gather, but without materialising the full map.
    """
    gx = (2.0 * (xs.float() + 0.5) / W - 1.0)
    gy = (2.0 * (ys.float() + 0.5) / H - 1.0)
    grid = torch.stack([gx, gy], -1).view(1, 1, -1, 2)
    out = F.grid_sample(fmap, grid, mode='bilinear', padding_mode='border', align_corners=False)
    return out[0, :, 0, :].t().contiguous()            # [P, D]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--backbone', default='sclip', choices=['sclip', 'naclip'])
    ap.add_argument('--npix', type=int, default=4096)
    ap.add_argument('--short', type=int, default=336)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--pixseed', type=int, default=1234,
                    help='seed for the per-image pixel subsample; the sample is drawn once '
                         'here and reused for every lambda, score, vocabulary and backbone, '
                         'so the per-image risk is pathwise monotone in lambda')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(ROOT, f'cache/{a.backbone}')
    os.makedirs(out, exist_ok=True)

    import sclip_clip as clip
    if a.backbone == 'sclip':
        net, _ = clip.load('ViT-B/16', device='cuda', jit=False)
    else:
        import naclip_setup
        net = naclip_setup.load_naclip('ViT-B/16')
    net.eval()

    files = sorted(os.listdir(os.path.join(ADE, 'images/validation')))
    if a.limit: files = files[:a.limit]
    N, P = len(files), a.npix
    D = net.visual.proj.shape[-1]
    phi = np.lib.format.open_memmap(os.path.join(out, 'phi.npy'), mode='w+', dtype=np.float16, shape=(N, P, D))
    g150 = np.zeros((N, P), np.uint8)      # 0..149, 255 ignore
    g847 = np.zeros((N, P), np.uint16)
    meta = []
    for i, fn in enumerate(files):
        img = np.array(Image.open(os.path.join(ADE, 'images/validation', fn)).convert('RGB'))
        H, W = img.shape[:2]
        lab = np.array(Image.open(os.path.join(ADE, 'annotations/validation', fn.replace('.jpg', '.png'))))
        l847 = np.load(os.path.join(GT847, fn.replace('.jpg', '.npy')))
        rng = np.random.default_rng(a.pixseed + i)
        flat = rng.choice(H * W, size=P, replace=False)
        ys, xs = flat // W, flat % W
        g = lab[ys, xs].astype(np.int32) - 1                   # reduce_zero_label
        g150[i] = np.where(g < 0, 255, g).astype(np.uint8)
        g847[i] = l847[ys, xs]
        rz = resize_keep_ratio(img, a.short)
        t = torch.from_numpy(rz).permute(2, 0, 1).float()
        t = ((t - MEAN) / STD).unsqueeze(0).cuda().half()
        fmap = dense_feature_map(net, t, backbone=a.backbone)
        ysd = torch.from_numpy(ys).cuda(); xsd = torch.from_numpy(xs).cuda()
        phi[i] = sample_phi(fmap, ysd, xsd, H, W).cpu().numpy().astype(np.float16)
        meta.append(dict(file=fn, H=int(H), W=int(W)))
        if i % 100 == 0:
            print(f'{i}/{N} {fn} {H}x{W} -> {rz.shape[:2]}', flush=True)
    phi.flush()
    np.save(os.path.join(out, 'gt150.npy'), g150)
    np.save(os.path.join(out, 'gt847.npy'), g847)
    json.dump(dict(meta=meta, npix=P, dim=int(D), backbone=a.backbone, short=a.short,
                   pixseed=a.pixseed),
              open(os.path.join(out, 'meta.json'), 'w'))
    print('done', N, 'images ->', out, flush=True)


if __name__ == '__main__':
    main()
