"""Natural-wording baseline reset and calibration-only top-k rank diagnostic."""
import json
import time
from pathlib import Path

import numpy as np
import torch

import conformal as C
from exp_fixed_source import calibrate, digest
from natural_vocab import load_manifest


def true_ranks(logits, y):
    """One-based descending rank, with ascending label index breaking ties."""
    true = logits.gather(-1, y[..., None])
    ids = torch.arange(logits.shape[-1], device=logits.device)
    return 1+((logits > true) | ((logits == true) & (ids < y[..., None]))).sum(-1)


def rank_losses(ranks, valid, nclasses):
    rows = []
    for rank, mask in zip(ranks, valid):
        counts = np.bincount(rank[mask], minlength=nclasses+1)[1:]
        rows.append(1-np.cumsum(counts)/counts.sum())
    return np.array(rows)


@torch.no_grad()
def main():
    start = time.perf_counter()
    out = Path('results/natural_ranks_sclip_ade')
    out.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    previous = Path('results/fixed_source_sclip_ade')
    old = json.loads((previous/'results.json').read_text())
    for path, expected in old['hashes'].items():
        assert digest(Path(path)) == expected, path
    image_manifest = json.loads((previous/'manifest.json').read_text())
    assert [r['historical_prompt'] for r in manifest['rows'][:150]] == image_manifest['source_names']
    assert [r['historical_prompt'] for r in manifest['rows'][150:]] == image_manifest['added_names_in_order']
    names = [r['prompt'] for r in manifest['rows']]
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    import sclip_clip as clip
    net, _ = clip.load('ViT-B/16', device='cuda', jit=False)
    net.eval()
    print('Encoding all natural-wording source and added labels...', flush=True)
    bank = C.text_bank(net, names)
    T = torch.stack([bank[n] for n in names]).cuda()
    np.save(out/'text_embeddings.npy', T.cpu().numpy())
    del net, bank
    torch.cuda.empty_cache()
    phi = np.load('cache/sclip/phi.npy', mmap_mode='r')
    gt = np.load('cache/sclip/gt150.npy')
    valid = gt < 150
    assert valid.any(1).all()
    ncal, neval = old['ncal'], old['neval']
    adds = [0, 50, 150, 500, 695]
    alpha = .1
    cal_scores = np.zeros((6, ncal, phi.shape[1]))
    cal_rank_losses = [np.zeros((ncal, 150+k)) for k in adds]

    def logits(lo, hi):
        f = torch.from_numpy(np.array(phi[lo:hi])).cuda().float()
        return torch.cat([f@T[j:j+64].T for j in range(0, len(T), 64)], -1)

    for lo in range(0, ncal, 8):
        hi = min(lo+8, ncal)
        lg = logits(lo, hi)
        z = C.LOGIT_SCALE*lg.double()
        y = torch.from_numpy(gt[lo:hi].astype(np.int64)).cuda().clamp(max=149)
        cal_scores[0, lo:hi] = lg.gather(-1, y[..., None]).squeeze(-1).cpu().numpy()
        for ki, k in enumerate(adds):
            lp = torch.log_softmax(z[..., :150+k], -1)
            cal_scores[ki+1, lo:hi] = lp.gather(-1, y[..., None]).squeeze(-1).cpu().numpy()
            rank = true_ranks(lg[..., :150+k], y).cpu().numpy()
            cal_rank_losses[ki][lo:hi] = rank_losses(rank, valid[lo:hi], 150+k)
        if lo % 200 == 0:
            print(f'Calibration {hi}/{ncal}', flush=True)
    thresholds, bounds = [], []
    for i, scores in enumerate(cal_scores):
        grid = np.r_[-np.inf, np.linspace(-2, 2, 32769)] if i == 0 else np.r_[-np.inf, np.linspace(-80, 0, 32769)]
        t, b = calibrate(scores, valid[:ncal], grid, alpha)
        thresholds.append(t)
        bounds.append(b)
    del cal_scores
    topks = []
    for losses in cal_rank_losses:
        bound = (losses.sum(0)+1)/(ncal+1)
        topks.append(int(np.flatnonzero(bound <= alpha)[0]+1))
    print('Calibrated top-k sizes:', topks, flush=True)
    methods = ['cosine', 'frozen_softmax', 'fixed_source', 'replay_softmax']
    per = np.zeros((4, 5, neval, 3))
    eval_rank_losses = [np.zeros((neval, 150+k)) for k in adds]
    source_disagreements = 0
    for lo in range(ncal, len(phi), 8):
        hi = min(lo+8, len(phi))
        lg = logits(lo, hi)
        z = C.LOGIT_SCALE*lg.double()
        ref = torch.logsumexp(z[..., :150], -1, keepdim=True)
        fixed = z-ref
        mask = torch.from_numpy(valid[lo:hi]).cuda()
        count = mask.sum(1).double()
        y = torch.from_numpy(gt[lo:hi].astype(np.int64)).cuda().clamp(max=149)
        src = torch.log_softmax(z[..., :150], -1) >= thresholds[1]
        source_disagreements += int((src != (fixed[..., :150] >= thresholds[1])).sum())
        for ki, k in enumerate(adds):
            n = 150+k
            lp = torch.log_softmax(z[..., :n], -1)
            memberships = [lg[..., :n] >= thresholds[0], lp >= thresholds[1],
                           fixed[..., :n] >= thresholds[1], lp >= thresholds[ki+1]]
            for mi, mem in enumerate(memberships):
                covered = mem.gather(-1, y[..., None]).squeeze(-1)
                values = torch.stack([((~covered)&mask).sum(1)/count,
                                      (mem[..., :150].sum(-1)*mask).sum(1)/count,
                                      (mem[..., 150:].sum(-1)*mask).sum(1)/count], -1)
                per[mi, ki, lo-ncal:hi-ncal] = values.cpu().numpy()
            rank = true_ranks(lg[..., :n], y).cpu().numpy()
            eval_rank_losses[ki][lo-ncal:hi-ncal] = rank_losses(rank, valid[lo:hi], n)
        if (lo-ncal) % 200 == 0:
            print(f'Evaluation {hi-ncal}/{neval}', flush=True)
    assert source_disagreements == 0
    assert np.array_equal(per[1, 0], per[2, 0]) and np.array_equal(per[2, 0], per[3, 0])
    assert np.array_equal(per[2, :, :, :2], np.broadcast_to(per[2, 0, :, :2], (5, neval, 2)))
    assert np.array_equal(per[0, :, :, :2], np.broadcast_to(per[0, 0, :, :2], (5, neval, 2)))
    boot = np.random.default_rng(20260921).integers(0, neval, (2000, neval))
    ci = lambda a: np.quantile(a[boot].mean(1), [.025, .975]).tolist()
    rows, ranks = [], []
    for ki, k in enumerate(adds):
        for mi, method in enumerate(methods):
            v = per[mi, ki]
            size = v[:, 1:].sum(1)
            rows.append(dict(method=method, added=k, risk=float(v[:, 0].mean()), risk_ci95=ci(v[:, 0]),
                             mean_size=float(size.mean()), size_ci95=ci(size),
                             original_size=float(v[:, 1].mean()), added_size=float(v[:, 2].mean())))
        topk = topks[ki]
        losses = eval_rank_losses[ki]
        curve = losses.mean(0)
        ranks.append(dict(added=k, calibrated_k=topk,
                          calibration_bound=float((cal_rank_losses[ki][:, topk-1].sum()+1)/(ncal+1)),
                          topk_risk=float(curve[topk-1]), topk_risk_ci95=ci(losses[:, topk-1]),
                          descriptive_eval_k90=int(np.flatnonzero(curve <= alpha)[0]+1),
                          risk_at_k={str(t):float(curve[t-1]) for t in [1, 5, 10, 20, 50, 100, 150] if t <= len(curve)},
                          mean_rank=float(1+curve.sum()), risk_curve=curve.tolist()))
    np.savez_compressed(out/'per_image.npz', values=per,
                        **{f'cal_rank_loss_{k}':v for k,v in zip(adds, cal_rank_losses)},
                        **{f'eval_rank_loss_{k}':v for k,v in zip(adds, eval_rank_losses)})
    result = dict(rows=rows, ranks=ranks, thresholds=thresholds, crc_bounds=bounds,
                  alpha=alpha, ncal=ncal, neval=neval, methods=methods,
                  checks=dict(source_membership_disagreements=source_disagreements,
                              source_softmax_fixed_replay_equal=True, cosine_and_fixed_source_risk_size_invariant=True),
                  protocol='ade-natural-v1 for every method; fresh calibration; same historical 1000/1000 images. Image-weighted valid sampled-pixel loss. Fixed-width float32 dot products, float64 log scores, TF32 off.',
                  rank_protocol='One-based rank; ties use ascending vocabulary index. Smallest fixed k with corrected calibration loss <=0.1, separately per vocabulary. Evaluation k90 is descriptive only.',
                  limitations='Fixed-k comparison cannot isolate causal training contributions or prove an irreducible minimum set size. Top-k is vocabulary-dependent and may flip old memberships. One inspected development split; no fitting or new-class guarantee. Cosine denotes historical cached dot-product convention; spatially averaged features are not renormalized.',
                  hashes={str(p):digest(p) for p in [Path(__file__), Path('meta/natural_vocab_v1.json'), previous/'results.json', out/'text_embeddings.npy']},
                  elapsed_seconds=time.perf_counter()-start)
    (out/'results.json').write_text(json.dumps(result, indent=2))
    (out/'vocabulary.json').write_text(json.dumps(manifest, indent=2))
    (out/'images.json').write_text(json.dumps(image_manifest, indent=2))
    report(out, result)
    print(json.dumps(dict(rows=rows, ranks=[{a:b for a,b in r.items() if a != 'risk_curve'} for r in ranks]), indent=2), flush=True)


def report(out, r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for rank in r['ranks']:
        x = np.arange(1, len(rank['risk_curve'])+1)
        axes[0].plot(x, np.array(rank['risk_curve'])*100, label=f"+{rank['added']}")
    axes[0].set_xscale('log')
    axes[0].axhline(10, color='gray', linestyle='--')
    axes[0].set_xlabel('Top-k size (log scale)')
    axes[0].set_ylabel('Image-averaged miss rate (%)')
    axes[0].legend(title='Added labels')
    for method in ['cosine', 'fixed_source', 'replay_softmax']:
        rows = [x for x in r['rows'] if x['method'] == method]
        axes[1].plot([x['added'] for x in rows], [x['mean_size'] for x in rows], marker='o', label=method)
    axes[1].plot([x['added'] for x in r['ranks']], [x['calibrated_k'] for x in r['ranks']], marker='s', label='Calibrated fixed k')
    axes[1].set_xlabel('Added labels')
    axes[1].set_ylabel('Labels per valid sampled pixel')
    axes[1].legend()
    fig.suptitle('Natural wording: ranking and calibrated set sizes, SCLIP / ADE20K')
    fig.tight_layout()
    fig.savefig(out/'ranks_sizes.png', dpi=180)
    fig.savefig(out/'ranks_sizes.pdf')
    lines = ['# Natural-wording baseline and rank diagnosis', '', r['protocol'], '',
             '| Method | Added | Miss rate (%) | Mean size | Original size | Added size |',
             '|---|---:|---:|---:|---:|---:|']
    for x in r['rows']:
        lines.append(f"| {x['method']} | {x['added']} | {100*x['risk']:.3f} | {x['mean_size']:.3f} | {x['original_size']:.3f} | {x['added_size']:.3f} |")
    lines += ['', '## Ranking diagnosis', '', r['rank_protocol'], '',
              '| Added | Calibrated k | Top-k miss rate (%) | Descriptive evaluation k for 90% coverage | Mean true-label rank |',
              '|---:|---:|---:|---:|---:|']
    for x in r['ranks']:
        lines.append(f"| {x['added']} | {x['calibrated_k']} | {100*x['topk_risk']:.3f} | {x['descriptive_eval_k90']} | {x['mean_rank']:.2f} |")
    lines += ['', '| Added | Top-1 coverage | Top-5 coverage | Top-10 coverage | Top-20 coverage | Top-50 coverage |',
              '|---:|---:|---:|---:|---:|---:|']
    for x in r['ranks']:
        vals = ' | '.join(f"{100*(1-x['risk_at_k'][str(k)]):.2f}%" for k in [1,5,10,20,50])
        lines.append(f"| {x['added']} | {vals} |")
    lines += ['', '## Interpretation constraints', '', r['limitations'], '',
              'The rank curves are common to all four scores because positive scaling and per-pixel scalar normalizers preserve ranking. '
              'A labelwise or spatial correction could change ranking. A small calibration-selected fixed-k set at comparable risk '
              'would demonstrate that another use of the same ranking can be competitive; it would not supply vocabulary stability. '
              'A large required fixed k indicates difficulty in the ranking tail, not a lower bound on adaptive-size predictors. '
              'Evaluation-selected k90 is never used to form the reported calibrated top-k predictor.', '',
              'Uncertainty in results.json uses 2000 image bootstrap draws conditional on this calibration split. '
              'No training/fit data or reserved images were accessed. Baselines are all recalibrated under the same wording; '
              'differences from historical numbers include source wording changes.', '',
              '## Reproduction', '', '```powershell', '.venv/Scripts/python.exe src/exp_natural_ranks.py', '```', '',
              'Per-image rank-loss curves and method metrics are in per_image.npz. Every image, label, threshold and artifact hash is recorded.']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
