"""Development sanity experiment: frozen source normalization under additions.

Run from repo root: .venv/Scripts/python.exe src/exp_fixed_source.py
Uses previously inspected ADE validation cache only. No fitting or reserve access.
"""
import argparse
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

import conformal as C
import vocab as V


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def calibrate(values, valid, grid, alpha):
    # Sorted true-label scores give exact image-weighted losses on a fixed grid.
    risks = np.zeros(len(grid), dtype=np.float64)
    for u, v in zip(values, valid):
        assert v.any(), 'Empty valid image requires an explicit exclusion policy'
        risks += np.searchsorted(np.sort(u[v]), grid, side='left') / v.sum()
    bound = (risks + 1) / (len(values) + 1)
    feasible = np.flatnonzero(bound <= alpha)
    assert len(feasible), 'No feasible threshold'
    idx = feasible[-1]
    return float(grid[idx]), float(bound[idx])


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default='cache/sclip')
    ap.add_argument('--out', default='results/fixed_source_sclip_ade')
    ap.add_argument('--ncal', type=int, default=1000)
    ap.add_argument('--batch', type=int, default=8)
    ap.add_argument('--alpha', type=float, default=.1)
    a = ap.parse_args()
    start = time.time()
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cache = Path(a.cache)
    phi = np.load(cache / 'phi.npy', mmap_mode='r')
    gt = np.load(cache / 'gt150.npy')
    valid = gt < 150
    assert valid.any(1).all()
    N, P, D = phi.shape
    assert 0 < a.ncal < N
    base = V.v_cal()
    _, mapping = V.build_configs()
    pool = [n for i, n in enumerate(V.names_847())
            if i not in set(mapping.tolist()) and n not in set(base)]
    # Existing ADE847 pool in its register order; fixed nested additions.
    names = base + pool
    adds = [0, 50, 150, 500, 695]
    assert len(pool) == 695
    meta = json.loads((cache / 'meta.json').read_text())
    manifest = dict(source_names=base, added_names_in_order=pool,
                    calibration_images=[m['file'] for m in meta['meta'][:a.ncal]],
                    evaluation_images=[m['file'] for m in meta['meta'][a.ncal:]],
                    pixel_seed=meta['pixseed'], pixels_per_image=P,
                    status='development; historically inspected validation images',
                    addition_order='ADE847 register order after existing exclusion rules')
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    text_path = out / 'text_embeddings.npy'
    if text_path.exists():
        T = torch.from_numpy(np.load(text_path)).cuda()
        assert T.shape == (len(names), D)
    else:
        import sclip_clip as clip
        net, _ = clip.load('ViT-B/16', device='cuda', jit=False)
        net.eval()
        print('Encoding source and distractor text with historical templates...', flush=True)
        bank = C.text_bank(net, names)
        T = torch.stack([bank[n] for n in names]).cuda()
        np.save(text_path, T.cpu().numpy())
        del net, bank
        torch.cuda.empty_cache()

    def logits(lo, hi):
        f = torch.from_numpy(np.array(phi[lo:hi])).cuda().float()
        # Fixed-width products avoid vocabulary-size-dependent GEMM changes.
        return torch.cat([f @ T[j:j+64].T for j in range(0, len(T), 64)], -1)

    ucos, ulog = [], []
    for lo in range(0, a.ncal, a.batch):
        hi = min(lo + a.batch, a.ncal)
        lg = logits(lo, hi)[..., :150]
        y = torch.from_numpy(gt[lo:hi].astype(np.int64)).cuda().clamp(max=149)
        ucos.append(lg.gather(-1, y[..., None]).squeeze(-1).cpu().numpy())
        lp = torch.log_softmax(C.LOGIT_SCALE * lg.double(), -1)
        ulog.append(lp.gather(-1, y[..., None]).squeeze(-1).cpu().numpy())
        if lo % 200 == 0:
            print(f'Calibration scores {hi}/{a.ncal}', flush=True)
    # Data-independent grids, with a literal all-label endpoint; no eval-derived bounds.
    tc, bc = calibrate(np.concatenate(ucos), valid[:a.ncal],
                       np.r_[-np.inf, np.linspace(-2, 2, 32769)], a.alpha)
    ts, bs = calibrate(np.concatenate(ulog), valid[:a.ncal],
                       np.r_[-np.inf, np.linspace(-80, 0, 32769)], a.alpha)
    del ucos, ulog
    print(f'Threshold cosine={tc}; log softmax={ts}; CRC bounds={bc}, {bs}', flush=True)
    methods = ['cosine', 'softmax', 'fixed_source']
    per = np.zeros((3, len(adds), N-a.ncal, 5), dtype=np.float64)
    source_disagreements = 0
    max_log_identity_error = 0.
    for lo in range(a.ncal, N, a.batch):
        hi = min(lo+a.batch, N)
        lg = logits(lo, hi)
        z = C.LOGIT_SCALE * lg.double()
        ref = torch.logsumexp(z[..., :150], -1, keepdim=True)
        source_lp = torch.log_softmax(z[..., :150], -1)
        fixed_lp = z - ref
        source_disagreements += int(((source_lp >= ts) != (fixed_lp[..., :150] >= ts)).sum())
        max_log_identity_error = max(max_log_identity_error,
            float((source_lp - fixed_lp[..., :150]).abs().max()))
        mask = torch.from_numpy(valid[lo:hi]).cuda()
        y = torch.from_numpy(gt[lo:hi].astype(np.int64)).cuda().clamp(max=149)
        count = mask.sum(1)
        original = [lg[..., :150] >= tc, source_lp >= ts, fixed_lp[..., :150] >= ts]
        for ki, k in enumerate(adds):
            n = 150+k
            memberships = [lg[..., :n] >= tc,
                           torch.log_softmax(z[..., :n], -1) >= ts,
                           fixed_lp[..., :n] >= ts]
            for mi, mem in enumerate(memberships):
                covered = mem.gather(-1, y[..., None]).squeeze(-1)
                loss = ((~covered) & mask).sum(1) / count.double()
                orig_size = (mem[..., :150].sum(-1) * mask).sum(1) / count.double()
                added_size = (mem[..., 150:].sum(-1) * mask).sum(1) / count.double()
                flips = ((mem[..., :150] != original[mi]) & mask[..., None]).sum((1, 2))
                true_flips = ((covered != original[mi].gather(-1, y[..., None]).squeeze(-1)) & mask).sum(1)
                vals = torch.stack([loss, orig_size, added_size, flips, true_flips], -1)
                per[mi, ki, lo-a.ncal:hi-a.ncal] = vals.cpu().numpy()
        if (lo-a.ncal) % 100 == 0:
            print(f'Evaluation {hi-a.ncal}/{N-a.ncal}', flush=True)
    np.savez_compressed(out / 'per_image.npz', values=per,
                        fields=['risk', 'original_size', 'added_size', 'membership_flips', 'true_label_flips'])
    rows = []
    rng = np.random.default_rng(20260921)
    boot = rng.integers(0, N-a.ncal, size=(2000, N-a.ncal))
    for mi, method in enumerate(methods):
        for ki, k in enumerate(adds):
            vals = per[mi, ki]
            size = vals[:, 1] + vals[:, 2]
            row = dict(method=method, added=k, risk=float(vals[:, 0].mean()),
                       risk_ci95=np.quantile(vals[boot, 0].mean(1), [.025, .975]).tolist(),
                       mean_size=float(size.mean()),
                       size_ci95=np.quantile(size[boot].mean(1), [.025, .975]).tolist(),
                       original_size=float(vals[:, 1].mean()), added_size=float(vals[:, 2].mean()),
                       p95_image_mean_size=float(np.quantile(size, .95)),
                       membership_flips=int(vals[:, 3].sum()), true_label_flips=int(vals[:, 4].sum()),
                       max_image_loss_change=float(abs(vals[:, 0]-per[mi, 0, :, 0]).max()))
            rows.append(row)
            print(row, flush=True)
    checks = dict(source_membership_disagreements_all_eval_pixels=source_disagreements,
                  max_source_log_score_roundoff=max_log_identity_error,
                  fixed_membership_flips=int(per[2, :, :, 3].sum()),
                  cosine_membership_flips=int(per[0, :, :, 3].sum()),
                  fixed_max_image_loss_change=float(abs(per[2, :, :, 0]-per[2, 0, :, 0]).max()))
    result = dict(rows=rows, checks=checks, thresholds=dict(cosine=tc, log_softmax=ts),
                  crc_bounds=dict(cosine=bc, softmax=bs), alpha=a.alpha,
                  ncal=a.ncal, neval=N-a.ncal, valid_eval_pixels=int(valid[a.ncal:].sum()),
                  protocol='Frozen thresholds; all methods use same valid cached pixels; image-weighted means.',
                  numerical='float32 fixed-width dot products; float64 log normalization; TF32 disabled',
                  uncertainty='2000 image bootstrap draws; conditional on this calibration split',
                  scope='cached feature scoring only; no full-pipeline independence or new-class guarantee',
                  grid='32769 fixed points: cosine [-2,2], log probability [-80,0], plus -inf',
                  versions=dict(torch=torch.__version__, numpy=np.__version__, python=platform.python_version()),
                  gpu=torch.cuda.get_device_name(), git=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
                  hashes={str(p):digest(p) for p in [cache/'phi.npy', cache/'gt150.npy', text_path, Path(__file__), out/'manifest.json']},
                  elapsed_seconds=time.time()-start)
    (out/'results.json').write_text(json.dumps(result, indent=2))
    assert source_disagreements == 0, checks
    assert checks['fixed_membership_flips'] == checks['cosine_membership_flips'] == 0, checks
    assert checks['fixed_max_image_loss_change'] == 0, checks
    print('All sanity checks passed. Results:', out, flush=True)


if __name__ == '__main__':
    main()
