"""Is the failure of a reused native threshold visible without labels? Tabulated from the repeated-split results.

At deployment the only label-free signal of a calibrated segmenter is its output; the simplest is the set size. For each
of the 15 model x benchmark combinations (Fig. 1), compare the set size of the reused native threshold before and after
growth with the size the grown vocabulary needs (native recalibrated there), and with the growth of the anchored sets,
which stay valid. Stored results only (results/headroom_splits_*/results.json, cal1000_a0.1); nothing is recomputed.
Usage: python src/exp_silent_failure.py -> results/silent_failure/{results.json,REPORT.md}
"""
import json
from pathlib import Path

from exp_fixed_source import digest
from plot_headroom import FIG1_DATASETS, FIG1_MODELS

DESIGN = 'cal1000_a0.1'
OUT = Path('results/silent_failure')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    alpha = float(DESIGN.split('_a')[-1])
    rows, lines = {}, ['# Silent failure: set size of the reused native threshold against the size needed', '',
                       f'{DESIGN}. Source: native threshold calibrated and applied at the source vocabulary. Reused: the same threshold at the grown vocabulary. '
                       'Needed: native recalibrated at the grown vocabulary (risk at the target). Share = (reused - source)/(needed - source): the part of the needed '
                       'growth that the reused sets show. Anchored growth: anchored size at the grown vocabulary over its size at the source vocabulary.', '',
                       '| Benchmark | Model | risk source -> reused (%) | size source | reused | needed | share | reused growth | anchored growth |',
                       '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for ds, _ in FIG1_DATASETS:
        for model, tags in FIG1_MODELS:
            d = json.loads(Path(f'results/headroom_splits_{ds}_{tags[ds]}/results.json').read_text())['designs'][DESIGN]
            src, reu, need, anc = d['catseg_native_source'], d['catseg_native_frozen_full'], d['catseg_native_replay_full'], d['catseg_anchored']
            s0, s1, sn = src['mean_size'][0], reu['mean_size'][-1], need['mean_size'][-1]
            r = dict(risk_source=src['mean_risk'], risk_reused=reu['mean_risk'], frac_reused_above_alpha=reu['frac_splits_above_alpha'],
                     size_source=s0, size_reused=s1, size_needed=sn, share=(s1-s0)/(sn-s0), growth_reused=s1/s0,
                     size_anchored_source=anc['mean_size'][0], size_anchored=anc['mean_size'][-1], growth_anchored=anc['mean_size'][-1]/anc['mean_size'][0],
                     under=reu['mean_risk'] > alpha)
            rows[f'{ds}/{model}'] = r
            lines.append(f"| {ds} | {model} | {100*r['risk_source']:.1f} -> {100*r['risk_reused']:.1f} | {s0:.2f} | {s1:.2f} | {sn:.2f} | {r['share']:.2f} | "
                         f"{r['growth_reused']:.2f}x | {r['growth_anchored']:.2f}x |")
    under = [r for r in rows.values() if r['under']]
    summary = dict(n_under=len(under), n=len(rows), share_lo=min(r['share'] for r in under), share_hi=max(r['share'] for r in under),
                   growth_reused_lo=min(r['growth_reused'] for r in under), growth_reused_hi=max(r['growth_reused'] for r in under),
                   growth_anchored_lo=min(r['growth_anchored'] for r in under), growth_anchored_hi=max(r['growth_anchored'] for r in under),
                   anchored_grows_more=all(r['growth_anchored'] > r['growth_reused'] for r in under),
                   over_share_lo=min(r['share'] for r in rows.values() if not r['under']), over_share_hi=max(r['share'] for r in rows.values() if not r['under']))
    lines += ['', f"Reused threshold above the target in {summary['n_under']} of {summary['n']} combinations. There the reused sets show "
              f"{summary['share_lo']:.2f}-{summary['share_hi']:.2f} of the needed growth (sizes x{summary['growth_reused_lo']:.2f}-x{summary['growth_reused_hi']:.2f}), "
              f"while the valid anchored sets grow x{summary['growth_anchored_lo']:.2f}-x{summary['growth_anchored_hi']:.2f}; anchored grows more in every one: "
              f"{summary['anchored_grows_more']}. Where the reused threshold is over-conservative (SED), its sets grow "
              f"{summary['over_share_lo']:.2f}-{summary['over_share_hi']:.2f} times the needed growth."]
    result = dict(design=DESIGN, combinations=rows, summary=summary,
                  hashes={p: digest(Path(p)) for p in ['src/exp_silent_failure.py', 'src/plot_headroom.py']})
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
