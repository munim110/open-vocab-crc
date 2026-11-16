"""Confirmation run on the untouched reserve (2,000 ADE *training* images, meta/ade_confirmation_reserve_v1.json).

Pre-registered protocol, to be run ONCE per frozen configuration after development on the validation images is over:
  * images: the reserve files in their stored (seeded) order; 4,096 sampled pixels per image (seed = reserve seed + index);
  * scores: the same three stores as the headroom probe (native at 150, native at 845, anchored at 845), released weights,
    the configuration given on the command line (backbone, bank) and nothing else;
  * primary: ONE split, calibration = first 1,000 reserve images, evaluation = the other 1,000, image-level CRC at
    alpha .10 and .05; anchored arm calibrated at the 150 source labels only, native frozen (calibrated at 150, applied at
    845) and native replay (calibrated at 845) as comparators; reported: risk and set size at +0/+50/+150/+500/+695;
  * secondary: 500 random 1,000/1,000 splits, as exp_headroom_splits.py.
Nothing is tuned here. Scores are cached so the CRC part can be re-run, but the reserve images are read once.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import curves
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

ADDITIONS = [0, 50, 150, 500, 695]
NPIX = 4096


@torch.no_grad()
def score(a, tag, out, store_dir):
    reserve = json.loads(Path('meta/ade_confirmation_reserve_v1.json').read_text())
    files = [Path(f.replace('\\', '/')) for f in reserve['files']]
    if a.smoke:                                                       # validation images only: the reserve stays untouched
        files = sorted(Path('data/ADEChallengeData2016/images/validation').glob('*.jpg'))[:a.smoke]
    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:150]] == ['source']*150 and len(names) == 845
    reference = json.loads(Path(a.bank).read_text())['names'] if a.bank else json.loads((CATSEG/'datasets/coco.json').read_text())
    if a.model == 'sed':
        from sed_probe_model import SEDProbe
        model = SEDProbe().cuda()
    else:
        model = CATSegProbe(None, a.size).cuda()
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    stores = {k: np.lib.format.open_memmap(store_dir/f'{k}.npy', mode='w+', dtype=np.float16, shape=(len(files), NPIX, n))
              for k, n in [('native150', 150), ('native845', 845), ('anchored845', 845)]}
    gt = np.full((len(files), NPIX), 255, np.uint8)
    ranks = np.zeros((len(files), 2, 4))                                # (native, anchored) x (src rank, src top10, exp rank, exp top10)
    seconds = np.zeros(3)
    for k, f in enumerate(files):
        img = Image.open(f).convert('RGB')
        lab = np.array(Image.open(str(f).replace('images', 'annotations').replace('.jpg', '.png')))
        H, W = lab.shape
        flat = np.random.default_rng(reserve['seed']+k).choice(H*W, NPIX, replace=False)
        gt[k] = np.where(lab.ravel()[flat] > 0, lab.ravel()[flat].astype(int)-1, 255)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        feats = model.image_features(model.windows(tensor))
        torch.cuda.synchronize(); t1 = time.perf_counter()
        n150 = stitched_samples(model, model.native(feats, text[:150]), y, x, H, W)
        n845 = stitched_samples(model, model.native(feats, text), y, x, H, W)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        ctx = model.context(feats, ref_text) if (not a.bank or a.model == 'sed') else bank_context(model, feats, ref_text)
        anch = stitched_samples(model, model.anchored(feats, ctx, text), y, x, H, W)
        torch.cuda.synchronize(); t3 = time.perf_counter()
        seconds += [t1-t0, t2-t1, t3-t2]
        for name, s in [('native150', n150), ('native845', n845), ('anchored845', anch)]:
            stores[name][k] = torch.logit(s.clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().cpu().numpy()
        valid = torch.from_numpy(gt[k] < 150).cuda(); target = torch.from_numpy(gt[k].astype(np.int64)).cuda().clamp(max=149)
        if valid.any():
            for i, (src, exp) in enumerate([(n150, n845), (anch[:, :150], anch)]):
                r0, r1 = true_ranks(src[valid], target[valid]), true_ranks(exp[valid], target[valid])
                ranks[k, i] = [r0.double().mean().item(), (r0 <= 10).double().mean().item(), r1.double().mean().item(), (r1 <= 10).double().mean().item()]
        if k % 50 == 0: print(f'{k+1}/{len(files)} src top10 native={ranks[k, 0, 1]:.3f} anchored={ranks[k, 1, 1]:.3f}', flush=True)
    for s in stores.values(): s.flush()
    np.save(store_dir/'gt150.npy', gt)
    protocol = dict(tag=tag, model=a.model, size=a.size, bank=a.bank or 'coco171', bank_size=len(reference), images=len(files), npix=NPIX,
                    seconds_per_image=dict(zip(['features', 'native_150_plus_845', 'anchored_reference_plus_845'], (seconds/len(files)).round(3).tolist())),
                    peak_gb=round(torch.cuda.max_memory_allocated()/2**30, 2), ranking=dict(native=ranks[:, 0].mean(0).tolist(), anchored=ranks[:, 1].mean(0).tolist(),
                    columns=['source_rank', 'source_top10', 'expanded_rank', 'expanded_top10']),
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_confirm_reserve.py', 'src/catseg_probe_model.py', 'src/sed_probe_model.py',
                                                              'meta/natural_vocab_v1.json', 'meta/ade_confirmation_reserve_v1.json'] + ([a.bank] if a.bank else [])})
    (out/'protocol.json').write_text(json.dumps(protocol, indent=2))


@torch.no_grad()
def crc(a, tag, out, store_dir):
    S = 150; widths = [S+x for x in ADDITIONS]
    gt = np.load(store_dir/'gt150.npy')
    stores = {k: np.load(store_dir/f'{k}.npy', mmap_mode='r') for k in ['native150', 'native845', 'anchored845']}
    n = len(gt)
    keep = np.flatnonzero((gt < S).any(1)); dropped = n-len(keep)
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    loss, size = {}, {}
    for k, st in stores.items():
        rows = [curves(torch.from_numpy(np.array(st[i])).cuda().double(), torch.from_numpy(gt[i].astype(np.int64)).cuda(), grid, S, widths) for i in keep]
        loss[k] = np.stack([r[0] for r in rows]); size[k] = np.stack([r[1] for r in rows]).astype(np.float32)

    def pick(store, cal, alpha):
        ok = np.flatnonzero((loss[store][cal].sum(0)+1)/(len(cal)+1) <= alpha)
        return ok[-1] if len(ok) else 0                                  # nothing qualifies (tiny calibration set): most conservative grid point

    arms = dict(anchored=('anchored845', 'anchored845', ADDITIONS), native_source=('native150', 'native150', [0]),
                native_frozen_full=('native150', 'native845', ADDITIONS[-1:]), native_replay_full=('native845', 'native845', ADDITIONS[-1:]))
    half = len(keep)//2
    designs = dict(primary=[np.arange(len(keep))], secondary=[np.random.default_rng(20261004).permutation(len(keep)) for _ in range(a.splits)])
    result = dict(tag=tag, images=int(len(keep)), excluded=int(dropped), alphas=ALPHAS, additions=ADDITIONS, designs={})
    lines = [f'# Confirmation run on the reserve: {tag}', '',
             f'{len(keep)} reserved ADE training images ({dropped} without a source-labelled sampled pixel excluded), read once. Primary: calibration = first {half} reserve images, evaluation = the rest. Secondary: {a.splits} random {half}/{len(keep)-half} splits. Image-level CRC; anchored calibrated at the 150 source labels only.', '']
    for design, perms in designs.items():
        for alpha in ALPHAS:
            key = f'{design}_a{alpha}'; result['designs'][key] = {}
            lines += [f'## {design}, alpha = {alpha}', '', '| Arm | Mean risk (%) | Splits above alpha (%) | '+' | '.join(f'+{x}' for x in ADDITIONS)+' |', '|---|---:|---:|'+'---:|'*len(ADDITIONS)]
            for arm, (cal_store, ev_store, adds) in arms.items():
                cols = [ADDITIONS.index(x) if ev_store != 'native150' else 0 for x in adds]
                risk, sizes = [], []
                for perm in perms:
                    cal, ev = perm[:half], perm[half:]
                    g = pick(cal_store, cal, alpha)
                    risk.append(loss[ev_store][ev, g].mean()); sizes.append(size[ev_store][:, cols, g][ev].mean(0))
                risk, sizes = np.array(risk), np.array(sizes)
                result['designs'][key][arm] = dict(mean_risk=float(risk.mean()), frac_above=float((risk > alpha).mean()), additions=adds, mean_size=sizes.mean(0).tolist(),
                                                   size_q025=np.quantile(sizes, .025, axis=0).tolist(), size_q975=np.quantile(sizes, .975, axis=0).tolist())
                cells = {x: f'{m:.2f}' for x, m in zip(adds, sizes.mean(0))}
                lines.append(f'| {arm} | {100*risk.mean():.2f} | {100*(risk > alpha).mean():.1f} | '+' | '.join(cells.get(x, '') for x in ADDITIONS)+' |')
            lines.append('')
    protocol = json.loads((out/'protocol.json').read_text())
    lines += ['Ranking on the reserve (source rank, source top-10, expanded rank, expanded top-10): native %s, anchored %s.' % (
        [round(v, 3) for v in protocol['ranking']['native']], [round(v, 3) for v in protocol['ranking']['anchored']]),
        'Seconds per image: %s; peak memory %s GB.' % (protocol['seconds_per_image'], protocol['peak_gb'])]
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_confirm_reserve.py', 'src/exp_headroom_splits.py', 'src/exp_headroom_sets.py']}
    (out/'results.json').write_text(json.dumps(result, indent=2))
    (out/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True, help='frozen configuration name, e.g. vitl_bank683')
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed'])
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--bank', default='', help='JSON with a "names" list; default COCO-171')
    ap.add_argument('--splits', type=int, default=500)
    ap.add_argument('--smoke', type=int, default=0, help='smoke test on N validation images instead of the reserve (tag gets _smoke)')
    ap.add_argument('--crc-only', action='store_true', help='re-run the CRC part on cached scores')
    a = ap.parse_args()
    if a.smoke: a.tag += '_smoke'
    torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
    out = Path(f'results/confirmation_ade_{a.tag}'); store_dir = Path(f'cache/confirmation_{a.tag}')
    out.mkdir(parents=True, exist_ok=True); store_dir.mkdir(parents=True, exist_ok=True)
    if not a.crc_only:
        assert a.smoke or not (out/'protocol.json').exists(), f'{out} already scored: the reserve is read once per configuration'
        score(a, a.tag, out, store_dir)
    crc(a, a.tag, out, store_dir)


if __name__ == '__main__':
    main()
