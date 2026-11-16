"""Calibrated set sizes from the headroom-probe scores. Development data; no fitting.

tune_cal (200 images) selects every threshold by image-level CRC; tune_eval (200) reports.
Projective arms (SCLIP fixed-source, anchored CAT-Seg) calibrate once at the 150 source
labels and keep that threshold under nested additions. Native CAT-Seg is shown both frozen
(source threshold reused at +695) and replayed (recalibrated under the deployed vocabulary).
"""
import json
from pathlib import Path

import numpy as np
import torch

from exp_fixed_source import calibrate, digest

OUT = Path('results/headroom_probe_ade')
STORE = Path('cache/headroom_probe')
ADDITIONS = [0, 50, 150, 500, 695]
ALPHAS = [.1, .05]
LOGIT_GRID = np.arange(-30, 30+1e-9, 1/64)
LOGP_GRID = np.arange(-40, 1e-9, 1/128)


def evaluate(scores, gt, valid, threshold, widths):
    """Image loss and mean set size at each nested vocabulary width."""
    true = np.take_along_axis(scores, np.minimum(gt, 149)[:, None].astype(np.int64), 1)[:, 0]
    member = scores[valid] >= threshold
    sizes = [member[:, :w].sum(1).mean() for w in widths]
    return float((true[valid] < threshold).mean()), sizes


def main():
    protocol = json.loads((OUT/'protocol.json').read_text())
    ids = protocol['image_ids']; assert len(ids) == 400
    cal, ev = np.arange(200), np.arange(200, 400)
    gt_all = np.load('cache/sclip/gt150.npy')[ids]
    valid_all = gt_all < 150
    phi = np.load('cache/sclip/phi.npy', mmap_mode='r')
    text = torch.from_numpy(np.load('results/natural_ranks_sclip_ade/text_embeddings.npy')).cuda().float()
    stores = {k: np.load(STORE/f'{k}.npy', mmap_mode='r') for k in ['native150', 'native845', 'anchored845']}

    def scores(arm, k):
        if arm == 'sclip_fixed_source':
            f = torch.from_numpy(np.array(phi[ids[k]])).cuda().float()
            z = 40*torch.cat([f@text[j:j+64].T for j in range(0, 845, 64)], -1).double()
            return (z-torch.logsumexp(z[:, :150], -1, keepdim=True)).cpu().numpy()
        return np.array(stores[arm][k]).astype(np.float64)

    arms = [('sclip_fixed_source', 'sclip_fixed_source', LOGP_GRID, ADDITIONS),
            ('catseg_anchored', 'anchored845', LOGIT_GRID, ADDITIONS),
            ('catseg_native_V150', 'native150', LOGIT_GRID, [0]),
            ('catseg_native_replay_V845', 'native845', LOGIT_GRID, [695])]
    true_scores = {}
    for name, store, _, _ in arms:
        true_scores[name] = [np.take_along_axis(scores(store, k), np.minimum(gt_all[k], 149)[:, None].astype(np.int64), 1)[:, 0] for k in cal]
    result = dict(alphas=ALPHAS, additions=ADDITIONS, arms={})
    per_image = {}
    for alpha in ALPHAS:
        for name, store, grid, adds in arms:
            threshold, bound = calibrate(true_scores[name], valid_all[cal], grid, alpha)
            widths = [150+a for a in adds] if store != 'native150' else [150]
            rows = [evaluate(scores(store, k), gt_all[k], valid_all[k], threshold, widths) for k in ev]
            risk = np.array([r[0] for r in rows]); size = np.array([r[1] for r in rows])
            per_image[f'{name}_a{alpha}'] = np.concatenate([risk[:, None], size], 1)
            result['arms'][f'{name}_a{alpha}'] = dict(threshold=threshold, crc_bound=bound, risk=float(risk.mean()),
                                                      additions=adds, mean_size=size.mean(0).tolist(),
                                                      p90_image_size=np.quantile(size, .9, axis=0).tolist())
        # frozen native: the V=150 threshold reused under the deployed 845-label vocabulary
        threshold = result['arms'][f'catseg_native_V150_a{alpha}']['threshold']
        rows = [evaluate(scores('native845', k), gt_all[k], valid_all[k], threshold, [845]) for k in ev]
        result['arms'][f'catseg_native_frozen_V845_a{alpha}'] = dict(threshold=threshold, risk=float(np.mean([r[0] for r in rows])),
                                                                     additions=[695], mean_size=[float(np.mean([r[1][0] for r in rows]))])
    rng = np.random.default_rng(20261002); draws = rng.integers(0, 200, (2000, 200))
    for alpha in ALPHAS:
        delta = per_image[f'catseg_anchored_a{alpha}']-per_image[f'sclip_fixed_source_a{alpha}']
        ci = np.quantile(delta[draws].mean(1), [.025, .975], axis=0).T
        result[f'anchored_minus_sclip_a{alpha}'] = dict(columns=['risk']+[f'size_plus_{a}' for a in ADDITIONS], mean=delta.mean(0).tolist(), ci95=ci.tolist())
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_headroom_sets.py', str(OUT/'protocol.json')]}
    (OUT/'sets.json').write_text(json.dumps(result, indent=2))
    np.savez_compressed(OUT/'sets_per_image.npz', **per_image)
    lines = ['# Calibrated set sizes from the headroom probe', '',
             '200 tuning-calibration images select thresholds (image-level CRC); 200 tuning-evaluation images report. Image-averaged sampled-pixel risk and mean labels per pixel. Development data; one split; no fitting.', '']
    for alpha in ALPHAS:
        lines += [f'## alpha = {alpha}', '', '| Arm | Calibrated once? | Risk (%) | '+' | '.join(f'+{a}' for a in ADDITIONS)+' |', '|---|---|---:|'+'---:|'*len(ADDITIONS)]
        for name, once in [('sclip_fixed_source', 'yes'), ('catseg_anchored', 'yes'), ('catseg_native_V150', 'n/a'),
                           ('catseg_native_frozen_V845', 'yes (invalid)'), ('catseg_native_replay_V845', 'no, replayed')]:
            r = result['arms'][f'{name}_a{alpha}']
            cells = {a: f'{s:.2f}' for a, s in zip(r['additions'], r['mean_size'])}
            lines.append(f"| {name} | {once} | {100*r['risk']:.2f} | "+' | '.join(cells.get(a, '') for a in ADDITIONS)+' |')
        d = result[f'anchored_minus_sclip_a{alpha}']
        lines += ['', 'Anchored minus SCLIP fixed-source, paired image bootstrap 95%: '+'; '.join(f"{c} {m:+.2f} [{lo:+.2f}, {hi:+.2f}]" for c, m, (lo, hi) in zip(d['columns'], d['mean'], d['ci95'])), '']
    lines += ['Intervals are conditional on this calibration split. Risk columns are in fraction units in the delta line. Native CAT-Seg scores at +695 include its per-crop top-256 truncation. Stored scores are float16 logits clamped to [-30, 30].']
    (OUT/'SETS.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
