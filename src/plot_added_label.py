"""Fig. 4 / Table 6: miss risk on the added labels under thresholds calibrated at the source vocabulary.

Reads results/added_label_risk_ade*/results.json (exp_added_label_risk.py) and draws, per configuration, the added-label
risk of the frozen anchored threshold, native recalibrated on the grown vocabulary, native at the anchored set size, and
native frozen, with the 2.5-97.5% spread over splits. Usage: python src/plot_added_label.py [--alpha 0.1] ->
figures/fig4_added_label_risk.{pdf,png} and figures/table6.md.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PDF_META = {'CreationDate': None, 'Creator': None}     # no timestamp: regenerating a figure gives the same bytes
PNG_META = {'Software': None}

CONFIGS = {
    'CAT-Seg ViT-B, COCO-171 bank': 'results/added_label_risk_ade',
    'CAT-Seg ViT-B, 683-name bank': 'results/added_label_risk_ade_bank683',
    'CAT-Seg ViT-L, COCO-171 bank': 'results/added_label_risk_ade_vitl',
    'CAT-Seg ViT-L, 683-name bank': 'results/added_label_risk_ade_vitl_bank683',
    'SED ConvNeXt-L, COCO-171 bank': 'results/added_label_risk_ade_sed',
    'SED ConvNeXt-L, 683-name bank': 'results/added_label_risk_ade_sed_bank683',
    'SED fast (top-8 rejection)': 'results/added_label_risk_ade_sed_fast8',
    'FC-CLIP ConvNeXt-L, training-vocabulary bank (133)': 'results/added_label_risk_ade_fcclip',
    'FC-CLIP ConvNeXt-L, 701-name bank': 'results/added_label_risk_ade_fcclip_bank683',
    'FC-CLIP ConvNeXt-L, 1,366-name bank': 'results/added_label_risk_ade_fcclip_bank1366',
    'FC-CLIP ConvNeXt-L, 2,731-name bank': 'results/added_label_risk_ade_fcclip_bank2731',
    'ViT-B fine-tuned 10k': 'results/added_label_risk_ade_ft10k',
    'ViT-B fine-tuned, distractors': 'results/added_label_risk_ade_anchored_vitb_distract_near',
}
ARMS = [('anchored_frozen', 'anchored, calibrated once', 'C0', 'o'), ('native_replay', 'native, recalibrated at 845', 'C3', 's'),
        ('native_at_anchored_frozen_size', 'native at the anchored set size', 'C1', 'D'), ('native_frozen', 'native, reused threshold', '0.5', 'x')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alpha', default='0.1')
    a = ap.parse_args()
    rows = []
    for label, d in CONFIGS.items():
        p = Path(d)/'results.json'
        if p.exists(): rows.append((label, json.loads(p.read_text())['designs'][f'a{a.alpha}']))
    Path('figures').mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, .42*len(rows)+1.2))
    for i, (label, r) in enumerate(rows):
        for arm, name, c, m in ARMS:
            if arm not in r: continue
            v, (lo, hi) = 100*r[arm]['risk_added'], [100*q for q in r[arm]['risk_added_q025_q975']]
            ax.errorbar(v, i, xerr=[[v-lo], [hi-v]], fmt=m, color=c, ms=5, capsize=2, lw=1, label=name if i == 0 else None)
            if arm in ('anchored_frozen', 'native_replay'): ax.annotate(f'{r[arm]["size_845"]:.1f}', (v, i), (0, 5), textcoords='offset points', ha='center', fontsize=7.5, color=c)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([l for l, _ in rows], fontsize=9); ax.invert_yaxis()
    ax.set_xlabel(f'miss risk on the 695 added labels at 845 labels (%)\nthresholds calibrated at 150 labels, target {float(a.alpha):.0%} on source labels; numbers: set size at 845', fontsize=9)
    ax.grid(axis='x', lw=.3); ax.legend(fontsize=9, loc='upper center', bbox_to_anchor=(.5, -.13), ncol=2, frameon=False)
    fig.tight_layout()
    for ext in ('pdf', 'png'): fig.savefig(f'figures/fig4_added_label_risk.{ext}', dpi=200, bbox_inches='tight', metadata=PDF_META if ext == 'pdf' else PNG_META)
    lines = [f'| Configuration | '+' | '.join(n for _, n, _, _ in ARMS)+' |', '|---|'+'---:|'*len(ARMS)]
    for label, r in rows:
        lines.append(f'| {label} | '+' | '.join(f'{100*r[arm]["risk_added"]:.1f}% / {r[arm]["size_845"]:.1f}' if arm in r else '' for arm, _, _, _ in ARMS)+' |')
    lines += ['', f'Added-label miss risk / set size at 845, alpha {a.alpha}, 500 splits; source-label risk of the anchored frozen arm: '+', '.join(f'{100*r["anchored_frozen"]["risk_source"]:.2f}%' for _, r in rows)+'.']
    Path('figures/table6.md').write_text('\n'.join(lines)); print('\n'.join(lines))


if __name__ == '__main__':
    main()
