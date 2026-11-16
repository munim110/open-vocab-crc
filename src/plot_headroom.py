"""Paper figures from the repeated-split results (results/headroom_splits_*/results.json).

Fig. 1: risk after growth for the frozen native threshold vs anchored vs replay, per configuration.
Fig. 3: set size vs added labels for the anchored arms, with the recalibrated native endpoint.
Usage: python src/plot_headroom.py [--design cal1000_a0.1] -> figures/*.pdf and a markdown table of the numbers used.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PDF_META = {'CreationDate': None, 'Creator': None}     # no timestamp: regenerating a figure gives the same bytes
PNG_META = {'Software': None}

# label -> splits directory (ADE unless noted)
CONFIGS = {
    'CAT-Seg ViT-B, COCO-171 bank': 'results/headroom_splits_ade',
    'CAT-Seg ViT-B, 683-name bank': 'results/headroom_splits_ade_bank683',
    'CAT-Seg ViT-L, COCO-171 bank': 'results/headroom_splits_ade_vitl',
    'CAT-Seg ViT-L, 683-name bank': 'results/headroom_splits_ade_vitl_bank683',
    'SED ConvNeXt-L, COCO-171 bank': 'results/headroom_splits_ade_sed',
    'SED ConvNeXt-L, 683-name bank': 'results/headroom_splits_ade_sed_bank683',
    'SED fast (top-8 rejection)': 'results/headroom_splits_ade_sed_fast8',
    'CAT-Seg ViT-B, Pascal 59 -> 458': 'results/headroom_splits_pascal',
}


# Fig. 1: the five models with the default bank (683 names; 701 for FC-CLIP) on the three benchmarks, as in Table 1
FIG1_MODELS = [('CAT-Seg ViT-B', {'ade': 'bank683', 'pascal': 'vitb_bank683', 'coco': 'vitb_bank683'}),
               ('CAT-Seg ViT-L', {'ade': 'vitl_bank683', 'pascal': 'vitl_bank683', 'coco': 'vitl_bank683'}),
               ('CAT-Seg + DeCLIP', {'ade': 'declip_bank683', 'pascal': 'declip_bank683', 'coco': 'declip_bank683'}),
               ('SED', {'ade': 'sed_bank683', 'pascal': 'sed_bank683', 'coco': 'sed_bank683'}),
               ('FC-CLIP', {'ade': 'fcclip_bank683', 'pascal': 'fcclip_bank683', 'coco': 'fcclip_bank683'})]
FIG1_DATASETS = [('ade', r'ADE20K 150$\to$845'), ('pascal', r'Pascal Context 59$\to$458'), ('coco', r'COCO-Stuff 171$\to$1,283')]


def load(design, configs=CONFIGS):
    out = {}
    for label, d in configs.items():
        p = Path(d)/'results.json'
        if not p.exists(): continue
        r = json.loads(p.read_text())
        key = design if design in r['designs'] else [k for k in r['designs'] if k.endswith(design.split('_')[-1])][-1]   # Pascal has other calibration sizes
        out[label] = dict(additions=r['additions'], design=key, **r['designs'][key])
    return out


def problem_figure(design, alpha, path):
    """Fig. 1, the failure only: per benchmark, risk and mean set size of the native threshold calibrated at the source
    vocabulary, before growth (open) and after growth (red), joined by a line (means over splits)."""
    fig, grid = plt.subplots(1, 8, figsize=(10, 1.85), sharey=True, gridspec_kw=dict(width_ratios=[1, 1, .18, 1, 1, .18, 1, 1]))
    for sp in (grid[2], grid[5]): sp.axis('off')
    axes = [grid[i] for i in (0, 1, 3, 4, 6, 7)]
    labels = [m for m, _ in FIG1_MODELS]
    for k, (ds, title) in enumerate(FIG1_DATASETS):
        panel = load(design, {m: f'results/headroom_splits_{ds}_{tags[ds]}' for m, tags in FIG1_MODELS})
        ax_r, ax_s = axes[2*k], axes[2*k+1]
        for i, label in enumerate(labels):
            b, a = panel[label]['catseg_native_source'], panel[label]['catseg_native_frozen_full']
            for ax, x0, x1 in [(ax_r, 100*b['mean_risk'], 100*a['mean_risk']), (ax_s, b['mean_size'][-1], a['mean_size'][-1])]:
                ax.plot([x0, x1], [i, i], color='#999999', linewidth=1.2, zorder=1)
                ax.plot(x0, i, 'o', color='#555555', mfc='white', mew=1.2, markersize=5, zorder=2, label='before growth' if i == 0 else None)
                ax.plot(x1, i, 'o', color='#c0392b', mew=1.2, markersize=5, zorder=3, label='after growth, same threshold' if i == 0 else None)
        ax_r.axvline(100*alpha, color='k', linestyle='--', linewidth=1, label='target risk', zorder=0)
        ax_r.set_xlim(2, 19); ax_r.set_xticks([5, 10, 15]); ax_r.set_xlabel('risk (%)', fontsize=10)
        ax_s.set_xscale('log'); ax_s.set_xlim(1.2, 14); ax_s.set_xticks([2, 5, 10]); ax_s.set_xticklabels(['2', '5', '10']); ax_s.minorticks_off()
        ax_s.set_xlabel('set size', fontsize=10)
        for ax in (ax_r, ax_s): ax.grid(axis='x', alpha=.3); ax.tick_params(labelsize=10)
    axes[0].set_yticks(range(len(labels))); axes[0].set_yticklabels(labels); axes[0].invert_yaxis()
    handles = dict((n, h) for h, n in zip(*axes[0].get_legend_handles_labels()))
    fig.legend(list(handles.values()), list(handles), loc='lower center', bbox_to_anchor=(.5, -.02), ncol=len(handles), fontsize=10, frameon=False,
               handlelength=1.6, columnspacing=1.4)
    fig.tight_layout(rect=(0, .09, 1, .91), w_pad=.4)
    for k, (_, title) in enumerate(FIG1_DATASETS):
        p, q = axes[2*k].get_position(), axes[2*k+1].get_position()
        fig.text((p.x0+q.x1)/2, p.y1+.03, title, ha='center', va='bottom', fontsize=11)
    fig.savefig(f'{path}.pdf', bbox_inches='tight', metadata=PDF_META); fig.savefig(f'{path}.png', dpi=150, bbox_inches='tight', metadata=PNG_META)


# native recalibration at the grown vocabulary: a grey bar, the per-row reference for the set size
RECAL = ('catseg_native_replay_full', '#7f7f7f', '|', 'none', 'native, recalibrated after growth')


def growth_figure(design, alpha, risk_arms, size_arms, path):
    """Per benchmark, two panels after growth, drawn like Fig. 1 (means over splits, no error bars): risk (dashed line
    at the target) and mean set size in labels per pixel (log axis shared by all benchmarks), with the size of native
    recalibration at the grown vocabulary, which meets the target, as a grey bar on each row."""
    # spacer columns between benchmarks, so that the two panels of a benchmark read as a pair
    fig, grid = plt.subplots(1, 8, figsize=(10, 1.85), sharey=True, gridspec_kw=dict(width_ratios=[1, 1, .18, 1, 1, .18, 1, 1]))
    for sp in (grid[2], grid[5]): sp.axis('off')
    axes = [grid[i] for i in (0, 1, 3, 4, 6, 7)]
    labels = [m for m, _ in FIG1_MODELS]
    for k, (ds, title) in enumerate(FIG1_DATASETS):
        panel = load(design, {m: f'results/headroom_splits_{ds}_{tags[ds]}' for m, tags in FIG1_MODELS})
        ax_r, ax_s = axes[2*k], axes[2*k+1]
        for i, label in enumerate(labels):
            d = panel[label]
            for j, (arm, color, mk, face, name) in enumerate(risk_arms):
                ax_r.plot(100*d[arm]['mean_risk'], i+(j-(len(risk_arms)-1)/2)*0.28, mk, color=color, mfc=face, mec=color, mew=1.2, label=name if i == 0 else None, markersize=5)
            ax_s.plot(d[RECAL[0]]['mean_size'][-1], i, RECAL[2], color=RECAL[1], mew=2, markersize=11, label=RECAL[4] if i == 0 else None)   # row reference
            for j, (arm, color, mk, face, name) in enumerate(size_arms):
                ax_s.plot(d[arm]['mean_size'][-1], i+(j-(len(size_arms)-1)/2)*0.28, mk, color=color, mfc=face, mec=color, mew=1.2, label=name if i == 0 else None, markersize=5)
        ax_r.axvline(100*alpha, color='k', linestyle='--', linewidth=1, label='target risk')
        ax_r.set_xlim(2, 19); ax_r.set_xticks([5, 10, 15]); ax_r.set_xlabel('risk (%)', fontsize=10)
        ax_s.set_xscale('log'); ax_s.set_xlim(1.2, 36); ax_s.set_xticks([2, 5, 10, 20]); ax_s.set_xticklabels(['2', '5', '10', '20']); ax_s.minorticks_off()
        ax_s.set_xlabel('set size', fontsize=10)
        for ax in (ax_r, ax_s): ax.grid(axis='x', alpha=.3); ax.tick_params(labelsize=10)
    axes[0].set_yticks(range(len(labels))); axes[0].set_yticklabels(labels); axes[0].invert_yaxis()
    handles = {}
    for ax in axes[:2]:
        for h, n in zip(*ax.get_legend_handles_labels()): handles.setdefault(n, h)
    handles['target risk'] = handles.pop('target risk')            # reference line last
    fig.legend(list(handles.values()), list(handles), loc='lower center', bbox_to_anchor=(.5, -.02), ncol=len(handles), fontsize=10, frameon=False,
               handlelength=1.6, columnspacing=1.4)
    fig.tight_layout(rect=(0, .09, 1, .91), w_pad=.4)
    for k, (_, title) in enumerate(FIG1_DATASETS):       # one title over the risk and set-size panels of each benchmark
        p, q = axes[2*k].get_position(), axes[2*k+1].get_position()
        fig.text((p.x0+q.x1)/2, p.y1+.03, title, ha='center', va='bottom', fontsize=11)
    fig.savefig(f'{path}.pdf', bbox_inches='tight', metadata=PDF_META); fig.savefig(f'{path}.png', dpi=150, bbox_inches='tight', metadata=PNG_META)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--design', default='cal1000_a0.1')
    a = ap.parse_args()
    data = load(a.design)
    Path('figures').mkdir(exist_ok=True)
    alpha = float(a.design.split('_a')[-1])

    # Fig. 1 shows only the failure (no anchored arm); Fig. 2 adds the anchored arm. Both: risk and set size per benchmark.
    # distinct marker shapes and fills, so that the arms stay apart in greyscale and where they overlap at the target
    before = ('catseg_native_source', '#555555', 'o', 'white', 'native, before growth')
    reused = ('catseg_native_frozen_full', '#c0392b', 'o', '#c0392b', 'native, same threshold')
    anch = ('catseg_anchored', '#1f5fa8', 'D', '#1f5fa8', 'anchored (ours), one calibration')
    problem_figure(a.design, alpha, 'figures/fig1_risk_after_growth')
    growth_figure(a.design, alpha, [reused, anch], [reused, anch], 'figures/fig2_anchored_after_growth')

    # Fig. 3: set size vs added labels
    fig, ax = plt.subplots(figsize=(6.4, 4))
    for label, d in data.items():
        if 'Pascal' in label: continue
        arm = d['catseg_anchored']
        ax.plot(arm['additions'], arm['mean_size'], marker='o', label=label)
        ax.fill_between(arm['additions'], arm['size_q025'], arm['size_q975'], alpha=.12)
        rep = d['catseg_native_replay_full']
        ax.plot(rep['additions'], rep['mean_size'], marker='x', linestyle='none', color=ax.lines[-1].get_color(), markersize=8)
    ax.set_xlabel('labels added to the 150 source labels'); ax.set_ylabel('mean prediction-set size (labels per pixel)')
    ax.set_title(f'anchored, calibrated once (lines); native recalibrated at +695 (x); target risk {100*alpha:.0f}%', fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig('figures/fig3_set_size_vs_additions.pdf', bbox_inches='tight', metadata=PDF_META); fig.savefig('figures/fig3_set_size_vs_additions.png', dpi=150, bbox_inches='tight', metadata=PNG_META)

    lines = ['| Configuration | Native frozen risk | Anchored risk | Anchored size (source -> full) | Native recalibrated size |', '|---|---:|---:|---:|---:|']
    for label, d in data.items():
        fr, an, rp = d['catseg_native_frozen_full'], d['catseg_anchored'], d['catseg_native_replay_full']
        lines.append(f"| {label} | {100*fr['mean_risk']:.1f}% | {100*an['mean_risk']:.2f}% | {an['mean_size'][0]:.2f} -> {an['mean_size'][-1]:.2f} | {rp['mean_size'][-1]:.2f} |")
    Path('figures/table1.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
