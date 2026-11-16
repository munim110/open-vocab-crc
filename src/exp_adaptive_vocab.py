"""Calibrate once, deploy under per-image vocabularies (stored scores of exp_adaptive_vocab_probe.py).

A deployed vocabulary is the 150 source names plus a per-image set A(x) of added names chosen by a policy (random k,
the names present in the image, the names a tagger proposes; see exp_adaptive_vocab_probe.py). Image-level CRC on the
source-label miss rate, random half/half splits as in exp_headroom_splits.py. Arms, each evaluated under every policy:
  anchored, calibrated once   threshold from the anchored scores of the calibration images (source names only); the
                              source-label loss does not depend on A(x), so one threshold serves every policy;
  native, frozen              threshold calibrated at the 150 source names;
  native, recalibrated at 845 threshold calibrated on the full grown vocabulary;
  native, matched             threshold calibrated on the calibration images under the SAME policy (needs the policy at
                              calibration time; valid by exchangeability);
  native, calibrated under q  threshold calibrated under another policy q (the policy changed after calibration);
  native, worst case          CRC on the per-image maximum loss over the listed policies: one threshold valid for any
                              per-image choice among them, adaptive included; needs every policy's native pass on every
                              calibration image (for all vocabularies, exponentially many).
  native, recalibrated at an N-name lexicon   threshold calibrated with a large known lexicon deployed (the 845 names plus
                              Open Images names, exp_lexicon_probe.py), then used for any per-image subset of it.
A sixth deployment, "adversarial", picks per image the listed policy with the highest loss under each arm's threshold.
Set size = mean number of deployed labels per source-labelled pixel. Development data; nothing is fitted; the confirmation
reserve is not read.

    PYTHONPATH=src python src/exp_adaptive_vocab.py --tag vitl_bank683
    PYTHONPATH=src python src/exp_adaptive_vocab.py --dataset pascal --tag vitl_bank683     (59 -> 458; arms named with 59 / 458)
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_added_label_risk import DATASETS
from exp_adaptive_vocab_probe import POLICY_SETS, probe_paths


def curves(scores, true_col, member, grid):
    """Image loss [G] and mean set size [G] over source-labelled pixels; member [P,C] marks deployed columns."""
    true = scores.gather(1, true_col[:, None])[:, 0]
    loss = torch.searchsorted(true.sort().values, grid, right=False).double()/len(true)
    s = scores[member]
    idx = torch.searchsorted(grid, s, right=True)
    below = torch.bincount(idx, minlength=len(grid)+1).double().cumsum(0)[:-1]
    size = (member.sum()-below)/len(true)
    return loss.cpu().numpy(), size.cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', default='ade', choices=list(POLICY_SETS))
    ap.add_argument('--tag', default='vitl_bank683')
    ap.add_argument('--splits', type=int, default=500)
    ap.add_argument('--limit', type=int, default=0, help='first N images only (testing while the probe runs; output tagged _limit)')
    a = ap.parse_args()
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    d = DATASETS[a.dataset]; S, T = d['S'], d['T']
    runs, caches, PROBE, STORE = probe_paths(a.dataset, a.tag)
    proto = json.loads((PROBE/'protocol.json').read_text())
    ids = proto['image_ids'][:a.limit or None]; pols = list(POLICY_SETS[a.dataset])
    assert list(proto['policies']) == pols
    assert sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in runs], [])[:len(ids)] == ids
    stored = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in caches] for k, v in zip(['native150', 'native845', 'anchored845'], d['stores'])}
    pol_scores = {p: np.load(STORE/f'{p}.npy', mmap_mode='r') for p in pols}
    pol_cols = {p: np.load(STORE/f'{p}_cols.npy') for p in pols}
    LEX = Path(f'cache/lexicon_{a.tag}')          # exp_lexicon_probe.py: native source scores with a large known lexicon deployed
    lexicons = json.loads(Path(f'results/lexicon_probe_{a.tag}/protocol.json').read_text())['lexicon_sizes'] if a.dataset == 'ade' and (LEX/'lex1690.npy').exists() else []
    if lexicons: assert json.loads(Path(f'results/lexicon_probe_{a.tag}/protocol.json').read_text())['image_ids'][:len(ids)] == ids
    lex_scores = {m: np.load(LEX/f'lex{m}.npy', mmap_mode='r') for m in lexicons}
    gt = np.load(f"{d['sclip']}/{d['gt_source']}")[ids]
    keep = np.flatnonzero((gt < S).any(1)); dropped = len(ids)-len(keep)
    grid = torch.from_numpy(LOGIT_GRID).to(dev)
    OUT = Path(f"results/adaptive_vocab_{'' if a.dataset == 'ade' else a.dataset+'_'}{a.tag}" + ('_limit' if a.limit else '')); OUT.mkdir(parents=True, exist_ok=True)

    def part(parts, k):
        for p in parts:
            if k < len(p): return p[k]
            k -= len(p)

    # per image: loss and size curves of every (calibration store, deployment) view
    L = {k: [] for k in ['anchored', 'native150', 'native845'] + [f'native_{p}' for p in pols] + [f'lex{m}' for m in lexicons]}
    Z = {k: [] for k in [f'anchored_{p}' for p in pols] + ['anchored_845', 'native150', 'native845'] + [f'native_{p}' for p in pols]}
    for k in keep:
        valid = torch.from_numpy(gt[k] < S).to(dev)
        tc = torch.from_numpy(gt[k].astype(np.int64)).to(dev)[valid]
        anch = torch.from_numpy(np.array(part(stored['anchored845'], k))).to(dev).double()[valid]
        full = torch.ones(anch.shape, dtype=torch.bool, device=dev)
        l, z = curves(anch, tc, full, grid); L['anchored'].append(l); Z['anchored_845'].append(z)
        for p in pols:
            cols = pol_cols[p][k]; cols = cols[cols >= 0]
            m = torch.zeros(anch.shape, dtype=torch.bool, device=dev); m[:, :S] = True; m[:, torch.from_numpy(cols.astype(np.int64)).to(dev)] = True
            Z[f'anchored_{p}'].append(curves(anch, tc, m, grid)[1])
            nat = torch.from_numpy(np.array(pol_scores[p][k])).to(dev).double()[valid]
            m = torch.zeros(nat.shape, dtype=torch.bool, device=dev); m[:, :S+len(cols)] = True
            l, z = curves(nat, tc, m, grid); L[f'native_{p}'].append(l); Z[f'native_{p}'].append(z)
        for name in ['native150', 'native845']:
            nat = torch.from_numpy(np.array(part(stored[name], k))).to(dev).double()[valid]
            l, z = curves(nat, tc, torch.ones(nat.shape, dtype=torch.bool, device=dev), grid); L[name].append(l); Z[name].append(z)
        for m in lexicons:                  # calibration only: the loss needs the source columns alone
            nat = torch.from_numpy(np.array(lex_scores[m][k])).to(dev).double()[valid]
            L[f'lex{m}'].append(curves(nat, tc, torch.ones(nat.shape, dtype=torch.bool, device=dev), grid)[0])
    L = {k: np.stack(v) for k, v in L.items()}; Z = {k: np.stack(v) for k, v in Z.items()}
    L['native_worst'] = np.max([L[f'native_{p}'] for p in pols], 0)      # per-image worst case over the listed policies
    n = len(keep)

    def pick(key, cal, alpha):
        bound = (L[key][cal].sum(0)+1)/(len(cal)+1)
        return np.flatnonzero(bound <= alpha)[-1]

    rng = np.random.default_rng(20260924)
    perms = [rng.permutation(n) for _ in range(a.splits)]
    FROZEN, RECAL = f'native, frozen at {S}', f'native, recalibrated at {T}'     # ADE: 150 / 845
    result = dict(dataset=a.dataset, tag=a.tag, images=n, excluded_images=dropped, splits=a.splits, policies=pols,
                  added_names_per_image=proto['added_names_per_image'], alphas={})
    lines = ['# Calibrate once, deploy under per-image vocabularies', '',
             f"{ {'sed': 'SED', 'fcclip': 'FC-CLIP'}.get(proto.get('model'), 'CAT-Seg')} ({a.tag})" f", {n} {d['name']} images ({dropped} without a source-labelled sampled pixel excluded), {a.splits} random half/half splits, "
             f'image-level CRC on the source-label miss rate. Deployed vocabulary = {S} source names + per-image added names A(x): '
             + ', '.join(f"{p} ({proto['added_names_per_image'][p]['mean']:.1f} on average)" for p in pols)
             + '. Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.', '']
    for alpha in ALPHAS:
        res = {}
        acc = {}
        for perm in perms:
            cal, ev = perm[:n//2], perm[n//2:]
            g = dict(anchored=pick('anchored', cal, alpha), frozen=pick('native150', cal, alpha), recal845=pick('native845', cal, alpha))
            g.update({f'cal_{q}': pick(f'native_{q}', cal, alpha) for q in pols})
            g['worst'] = pick('native_worst', cal, alpha)
            g.update({f'lex{m}': pick(f'lex{m}', cal, alpha) for m in lexicons})
            for p in pols:
                rows = {'anchored, calibrated once': (L['anchored'], Z[f'anchored_{p}'], g['anchored']),
                        FROZEN: (L[f'native_{p}'], Z[f'native_{p}'], g['frozen']),
                        RECAL: (L[f'native_{p}'], Z[f'native_{p}'], g['recal845']),
                        'native, matched to the policy': (L[f'native_{p}'], Z[f'native_{p}'], g[f'cal_{p}']),
                        'native, worst case over the policies': (L[f'native_{p}'], Z[f'native_{p}'], g['worst'])}
                rows.update({f'native, calibrated under {q}': (L[f'native_{p}'], Z[f'native_{p}'], g[f'cal_{q}']) for q in pols if q != p})
                rows.update({f'native, recalibrated at a {m:,}-name lexicon': (L[f'native_{p}'], Z[f'native_{p}'], g[f'lex{m}']) for m in lexicons})
                for arm, (loss, size, gi) in rows.items():
                    acc.setdefault((p, arm), []).append((loss[ev, gi].mean(), size[ev, gi].mean()))
            # adversarial deployment: per image, the listed policy with the highest loss under the arm's threshold
            # (ties -> the policy with the larger set; for the anchored arm every policy ties, its loss does not depend on A(x))
            for arm, key, gi in [('anchored, calibrated once', 'anchored', g['anchored']), (FROZEN, 'native', g['frozen']),
                                 (RECAL, 'native', g['recal845']), ('native, worst case over the policies', 'native', g['worst'])] + \
                                [(f'native, calibrated under {q}', 'native', g[f'cal_{q}']) for q in pols] + \
                                [(f'native, recalibrated at a {m:,}-name lexicon', 'native', g[f'lex{m}']) for m in lexicons]:
                lp = np.stack([L['anchored'] if key == 'anchored' else L[f'native_{q}'] for q in pols])[:, ev, gi]
                zp = np.stack([Z[f'{key}_{q}'] for q in pols])[:, ev, gi]
                j = (lp*1e8+zp).argmax(0)      # highest loss, ties to the larger set (losses on one image share a denominator <= 4096)
                acc.setdefault(('adversarial', arm), []).append((lp[j, np.arange(len(ev))].mean(), zp[j, np.arange(len(ev))].mean()))
        for (p, arm), v in acc.items():
            v = np.array(v)
            res.setdefault(p, {})[arm] = dict(mean_risk=float(v[:, 0].mean()), frac_splits_above_alpha=float((v[:, 0] > alpha).mean()), mean_size=float(v[:, 1].mean()))
        result['alphas'][str(alpha)] = res
        for p in pols + ['adversarial']:
            lines += [f'## alpha = {alpha}, policy {p}', '', '| Arm | Risk (%) | Above (%) | Size |', '|---|---:|---:|---:|']
            lines += [f"| {arm} | {100*r['mean_risk']:.2f} | {100*r['frac_splits_above_alpha']:.1f} | {r['mean_size']:.2f} |" for arm, r in res[p].items()]
            lines.append('')
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_adaptive_vocab.py', 'src/exp_adaptive_vocab_probe.py']}
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
