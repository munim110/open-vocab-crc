"""Calibrate, then deploy with free-form per-image names (stored scores of exp_freeform_vocab_probe*.py).

The deployed vocabulary of each image is the 150 source names plus the names a language model gave for it
(docs/FREEFORM_NAMES_PROTOCOL.md); most are outside ADE20K-847 and outside any list known at calibration. Image-level CRC
on the source-label miss rate, random half/half splits as in exp_adaptive_vocab.py (same seed). Thresholds:
  anchored, calibrated once     the anchored threshold of exp_adaptive_vocab.py (source names only);
  native, reused at 150         calibrated at the 150 source names;
  native, recalibrated at 845   calibrated with all 845 evaluated names deployed;
  native, recalibrated at an N-name lexicon   calibrated with the 845 names plus Open Images names deployed (exp_lexicon_probe*.py;
                                SED and FC-CLIP, whose lexicon stores are on this machine);
  native, matched               calibrated on the calibration half under the free-form names themselves (needs the namer
                                at calibration time; valid by exchangeability).
Risk on the evaluation half under the free-form deployment; size = deployed labels per source-labelled pixel; "added in
set" = how many of those are added names. Development data; nothing is fitted; the reserve is not read.

    PYTHONPATH=src .venv-probe/Scripts/python.exe src/exp_freeform_vocab.py --tag vitl_bank683
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_adaptive_vocab import curves
from exp_adaptive_vocab_probe import probe_paths
from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID

S = 150
LEXICONS = [1690, 17001]


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--splits', type=int, default=500)
    a = ap.parse_args()
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    runs, caches, _, _ = probe_paths('ade', a.tag)
    PROBE, STORE = Path(f'results/freeform_vocab_probe_{a.tag}'), Path(f'cache/freeform_vocab_{a.tag}')
    proto = json.loads((PROBE/'protocol.json').read_text())
    ids = proto['image_ids']
    assert sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], []) == ids
    stored = {k: [np.load(f'{c}/{k}.npy', mmap_mode='r') for c in caches] for k in ['native150', 'native845', 'anchored845']}
    native_free, anch_added = np.load(STORE/'native.npy', mmap_mode='r'), np.load(STORE/'anchored_added.npy', mmap_mode='r')
    n_added = np.load(STORE/'n_added.npy')
    LEX = Path(f'cache/lexicon_{a.tag}')
    lexicons = [m for m in LEXICONS if (LEX/f'lex{m}.npy').exists()]
    if lexicons: assert json.loads(Path(f'results/lexicon_probe_{a.tag}/protocol.json').read_text())['image_ids'] == ids
    lex_scores = {m: np.load(LEX/f'lex{m}.npy', mmap_mode='r') for m in lexicons}
    gt = np.load('cache/sclip/gt150.npy')[ids]
    keep = np.flatnonzero((gt < S).any(1)); dropped = len(ids)-len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev)

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    L = {k: [] for k in ['anchored', 'native150', 'native845', 'free'] + [f'lex{m}' for m in lexicons]}
    Z = {k: [] for k in ['anchored', 'anchored_added', 'free', 'free_added']}
    for k in keep:
        valid = torch.from_numpy(gt[k] < S).to(dev); n = int(n_added[k])
        tc = torch.from_numpy(gt[k].astype(np.int64)).to(dev)[valid]
        anch = torch.cat([torch.from_numpy(np.array(part(stored['anchored845'], k)[:, :S])), torch.from_numpy(np.array(anch_added[k, :, :n]))], 1).to(dev).double()[valid]
        nat = torch.from_numpy(np.array(native_free[k, :, :S+n])).to(dev).double()[valid]
        full = torch.ones(anch.shape, dtype=torch.bool, device=dev)
        only_added = full.clone(); only_added[:, :S] = False
        for key, sc in [('anchored', anch), ('free', nat)]:
            l, z = curves(sc, tc, full, grid); L[key].append(l); Z[key].append(z)
            Z[f'{key}_added'].append(curves(sc, tc, only_added, grid)[1])
        for name in ['native150', 'native845']:
            s = torch.from_numpy(np.array(part(stored[name], k))).to(dev).double()[valid]
            L[name].append(curves(s, tc, torch.ones(s.shape, dtype=torch.bool, device=dev), grid)[0])
        for m in lexicons:
            s = torch.from_numpy(np.array(lex_scores[m][k])).to(dev).double()[valid]
            L[f'lex{m}'].append(curves(s, tc, torch.ones(s.shape, dtype=torch.bool, device=dev), grid)[0])
    L = {k: np.stack(v) for k, v in L.items()}; Z = {k: np.stack(v) for k, v in Z.items()}
    n = len(keep)

    def pick(key, cal, alpha):
        bound = (L[key][cal].sum(0)+1)/(len(cal)+1)
        return np.flatnonzero(bound <= alpha)[-1]

    rng = np.random.default_rng(20260924)
    perms = [rng.permutation(n) for _ in range(a.splits)]
    ARMS = [('anchored, calibrated once', 'anchored', 'anchored'), ('native, reused at 150', 'native150', 'free'),
            ('native, recalibrated at 845', 'native845', 'free')] + \
           [(f'native, recalibrated at a {m:,}-name lexicon', f'lex{m}', 'free') for m in lexicons] + [('native, matched to the names', 'free', 'free')]
    result = dict(tag=a.tag, model=proto['model'], images=n, excluded_images=dropped, splits=a.splits, added_names_per_image=proto['added_names_per_image'],
                  unique_added_names=proto['unique_added_names'], alphas={})
    model_name = {'sed': 'SED', 'fcclip': 'FC-CLIP'}.get(proto['model'], 'CAT-Seg')
    lines = ['# Calibrate, then deploy with free-form per-image names', '',
             f"{model_name} ({a.tag}), {n} ADE20K images ({dropped} without a source-labelled sampled pixel excluded), {a.splits} random half/half splits, "
             f"image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + the image's free-form names "
             f"({proto['added_names_per_image']['mean']:.1f} on average, {proto['unique_added_names']} unique). Risk in %, above = % of splits above alpha, "
             'size = deployed labels per source-labelled pixel, added = added names among them.', '']
    for alpha in ALPHAS:
        acc = {arm: [] for arm, _, _ in ARMS}
        for perm in perms:
            cal, ev = perm[:n//2], perm[n//2:]
            for arm, cal_key, dep in ARMS:
                g = pick(cal_key, cal, alpha)
                acc[arm].append((L[dep][ev, g].mean(), Z[dep][ev, g].mean(), Z[f'{dep}_added'][ev, g].mean()))
        res = {}
        for arm, v in acc.items():
            v = np.array(v)
            res[arm] = dict(mean_risk=float(v[:, 0].mean()), frac_splits_above_alpha=float((v[:, 0] > alpha).mean()),
                            mean_size=float(v[:, 1].mean()), mean_added_in_set=float(v[:, 2].mean()))
        result['alphas'][str(alpha)] = res
        lines += [f'## alpha = {alpha}', '', '| Arm | Risk (%) | Above (%) | Size | Added in set |', '|---|---:|---:|---:|---:|']
        lines += [f"| {arm} | {100*r['mean_risk']:.2f} | {100*r['frac_splits_above_alpha']:.1f} | {r['mean_size']:.2f} | {r['mean_added_in_set']:.2f} |" for arm, r in res.items()]
        lines.append('')
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_freeform_vocab.py', 'results/freeform_names_ade/names.json']}
    OUT = Path(f'results/freeform_vocab_{a.tag}'); OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
