"""Repeated calibration/evaluation splits over the stored headroom-probe scores.

Same arms, grids and CRC rule as exp_headroom_sets.py, but every image's loss and set-size
curves are tabulated once on the threshold grid, so many random splits are cheap. Development
data (ADE validation); nothing is fitted; the confirmation reserve is not read.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID, LOGP_GRID

# stores: (native at the source vocabulary, native at the full vocabulary, anchored at the full vocabulary)
DATASETS = dict(
    ade=dict(source=150, additions=[0, 50, 150, 500, 695], sclip='cache/sclip', gt='gt150.npy', stores=('native150', 'native845', 'anchored845'),
             text='results/natural_ranks_sclip_ade/text_embeddings.npy', runs=['results/headroom_probe_ade', 'results/headroom_probe_ade_rest'],
             caches=['cache/headroom_probe', 'cache/headroom_probe_rest'], name='ADE validation'),
    pascal=dict(source=59, additions=[0, 50, 150, 399], sclip='cache/pascal_sclip', gt='gt59.npy', stores=('native_source', 'native_full', 'anchored_full'),
                text='results/headroom_probe_pascal/sclip_text_embeddings.npy', runs=['results/headroom_probe_pascal'],
                caches=['cache/headroom_probe_pascal'], name='Pascal Context validation'),
    # third benchmark (docs/COCO_LVIS_BENCHMARK.md): tagged runs only (results/headroom_probe_coco_<tag>); no SCLIP arm
    coco=dict(source=171, additions=[0, 50, 150, 500, 1112], sclip='cache/coco_pixels', gt='gt171.npy', stores=('native_source', 'native_full', 'anchored_full'),
              text=None, runs=[], caches=[], name='COCO val2017 (LVIS-annotated)'))


def curves(scores, gt, grid, source, widths):
    """Image loss [G] and mean set size [len(widths),G] at every grid threshold (member: score >= threshold)."""
    valid = gt < source
    s = scores[valid]; n = len(s)
    true = s.gather(1, gt[valid].long()[:, None])[:, 0]
    loss = torch.searchsorted(true.sort().values, grid, right=False).double()/n
    size, below = [], torch.zeros(len(grid)+1, dtype=torch.float64, device=s.device)
    lo = 0
    for w in widths:
        if w > s.shape[1]: break
        idx = torch.searchsorted(grid, s[:, lo:w].reshape(-1), right=True)     # thresholds <= score
        below += torch.bincount(idx, minlength=len(grid)+1).double()
        size.append((w*n-below.cumsum(0)[:-1])/n)                               # count with idx > g
        lo = w
    return loss.cpu().numpy(), torch.stack(size).cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(DATASETS))
    ap.add_argument('--runs', type=int, default=0, help='use only the first N probe runs of the dataset (testing)')
    ap.add_argument('--splits', type=int, default=500)
    ap.add_argument('--tag', default='', help='read a tagged probe run: ADE <run>_<tag> and <run>_<tag>_rest; Pascal and COCO the single run results/headroom_probe_<dataset>_<tag>')
    ap.add_argument('--disjoint', action='store_true', help='ADE only: drop the first run, whose 400 images chose the reference bank (exp_anchor_bank.py); keep the other 1,600')
    a = ap.parse_args()
    d = dict(DATASETS[a.dataset])
    if a.tag and a.dataset == 'ade':
        d['runs'] = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
        d['caches'] = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    elif a.tag:
        d['runs'] = [f'results/headroom_probe_{a.dataset}_{a.tag}']
        d['caches'] = [f'cache/headroom_probe_{a.dataset}_{a.tag}']
    n_runs = a.runs or len(d['runs'])
    if a.disjoint:
        assert a.dataset == 'ade' and not a.runs
        bank_images = set(json.loads(Path('results/headroom_probe_ade/protocol.json').read_text())['image_ids'])
        d['runs'], d['caches'] = d['runs'][1:], d['caches'][1:]; n_runs = len(d['runs'])
    S, ADDITIONS = d['source'], d['additions']; T = S+ADDITIONS[-1]; widths = [S+x for x in ADDITIONS]
    OUT = Path(f'results/headroom_splits_{a.dataset}'+(f'_{a.tag}' if a.tag else '')+('_disjoint' if a.disjoint else '')); OUT.mkdir(parents=True, exist_ok=True)
    ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in d['runs'][:n_runs]], [])
    assert len(set(ids)) == len(ids)
    if a.disjoint: assert not bank_images & set(ids), 'images that chose the bank must be excluded'
    gt_all = np.load(f"{d['sclip']}/{d['gt']}")[ids]
    has_sclip = Path(f"{d['sclip']}/phi.npy").exists()      # absent on the training box; the SCLIP arm is then skipped
    phi = np.load(f"{d['sclip']}/phi.npy", mmap_mode='r') if has_sclip else None
    text = torch.from_numpy(np.load(d['text'])).cuda().float() if has_sclip else None
    assert text is None or len(text) == T
    names = dict(zip(['native150', 'native845', 'anchored845'], d['stores']))      # internal keys keep the ADE names
    stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in d['caches'][:n_runs]] for k, v in names.items()}
    # Exclusion fixed before any vocabulary is tested: images with no sampled pixel labelled in the source vocabulary.
    keep = np.flatnonzero((gt_all < S).any(1)); dropped = len(ids)-len(keep)

    def scores(store, k):
        if store == 'sclip':
            f = torch.from_numpy(np.array(phi[ids[k]])).cuda().float()
            z = 40*torch.cat([f@text[j:j+64].T for j in range(0, T, 64)], -1).double()
            return z-torch.logsumexp(z[:, :S], -1, keepdim=True)
        for part in stores[store]:
            if k < len(part): return torch.from_numpy(np.array(part[k])).cuda().double()
            k -= len(part)

    grids = dict(sclip=torch.from_numpy(LOGP_GRID).cuda(), native150=torch.from_numpy(LOGIT_GRID).cuda())
    grids['native845'] = grids['anchored845'] = grids['native150']
    if not has_sclip: del grids['sclip']
    loss, size = {}, {}
    for store, grid in grids.items():
        rows = [curves(scores(store, k), torch.from_numpy(gt_all[k].astype(np.int64)).cuda(), grid, S, widths) for k in keep]
        loss[store] = np.stack([r[0] for r in rows]); size[store] = np.stack([r[1] for r in rows]).astype(np.float32)
        print(store, loss[store].shape, size[store].shape, flush=True)

    def pick(store, cal, alpha):
        bound = (loss[store][cal].sum(0)+1)/(len(cal)+1)
        return np.flatnonzero(bound <= alpha)[-1]

    n_img = len(keep)
    if a.dataset == 'ade' and not a.tag and not a.disjoint:   # the original fixed 200/200 split must reproduce exp_headroom_sets.py
        ref = json.loads(Path('results/headroom_probe_ade/sets.json').read_text())['arms']['catseg_anchored_a0.1']
        g = pick('anchored845', np.arange(200), .1)
        np.testing.assert_allclose(size['anchored845'][200:400, :, g].mean(0), ref['mean_size'], rtol=1e-5)
        np.testing.assert_allclose(loss['anchored845'][200:400, g].mean(), ref['risk'], rtol=1e-9)

    # arm -> (store calibrated on, store evaluated on, reported additions)
    arms = dict(sclip_fixed_source=('sclip', 'sclip', ADDITIONS), catseg_anchored=('anchored845', 'anchored845', ADDITIONS),
                catseg_native_source=('native150', 'native150', [0]), catseg_native_frozen_full=('native150', 'native845', ADDITIONS[-1:]),
                catseg_native_replay_full=('native845', 'native845', ADDITIONS[-1:]))
    arms = {k: v for k, v in arms.items() if v[0] in grids}
    rng = np.random.default_rng(20261003)
    result = dict(dataset=a.dataset, disjoint_from_bank_choice=a.disjoint, images=n_img, excluded_images=dropped, splits=a.splits, alphas=ALPHAS, additions=ADDITIONS, designs={})
    lines = ['# Repeated-split calibrated sets from the headroom probe', '',
             f"{n_img} {d['name']} images (development data; {dropped} without a source-labelled sampled pixel excluded), {S} source labels, {a.splits} random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.", '']
    for n_cal in [200, n_img//2]:
        perms = [rng.permutation(n_img) for _ in range(a.splits)]
        for alpha in ALPHAS:
            key = f'cal{n_cal}_a{alpha}'; result['designs'][key] = {}
            lines += [f'## {n_cal} calibration / {n_img-n_cal} evaluation images, alpha = {alpha}', '',
                      '| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | '+' | '.join(f'+{x}' for x in ADDITIONS)+' |', '|---|---:|---:|---:|'+'---:|'*len(ADDITIONS)]
            for arm, (cal_store, ev_store, adds) in arms.items():
                risk, sizes = [], []
                cols = [ADDITIONS.index(x) if ev_store != 'native150' else 0 for x in adds]
                for perm in perms:
                    cal, ev = perm[:n_cal], perm[n_cal:]
                    g = pick(cal_store, cal, alpha)
                    risk.append(loss[ev_store][ev, g].mean())
                    sizes.append(size[ev_store][:, cols, g][ev].mean(0))
                risk, sizes = np.array(risk), np.array(sizes)
                lo, hi = np.quantile(sizes, [.025, .975], axis=0)
                result['designs'][key][arm] = dict(mean_risk=float(risk.mean()), risk_sd=float(risk.std(ddof=1)), frac_splits_above_alpha=float((risk > alpha).mean()),
                                                   additions=adds, mean_size=sizes.mean(0).tolist(), size_q025=lo.tolist(), size_q975=hi.tolist())
                cells = {x: f'{m:.2f} [{l:.2f}, {h:.2f}]' for x, m, l, h in zip(adds, sizes.mean(0), lo, hi)}
                lines.append(f'| {arm} | {100*risk.mean():.2f} | {100*risk.std(ddof=1):.2f} | {100*(risk > alpha).mean():.1f} | '+' | '.join(cells.get(x, '') for x in ADDITIONS)+' |')
            lines.append('')
    lines += ['Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_headroom_splits.py', 'src/exp_headroom_sets.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
