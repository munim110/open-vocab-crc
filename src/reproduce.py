"""Reproduce the paper (paper/) from any of three starting points.

Every result directory the paper reads is registered below with the command that wrote it, the Python environment
it runs in and the stored inputs it needs. Levels:

  paper  results/ -> numbers.tex, tables/*.tex, figures (no GPU, no dataset; seconds)
  cpu    stored per-pixel scores (cache/headroom_probe*) -> results/ analyses (no model; a GPU only speeds it up)
  gpu    images + released weights -> stored scores, full-resolution mIoU, timings, bank sweeps, controls
  train  COCO-Stuff -> the two fine-tuned aggregators of the supplement

Usage (repository root):
  python src/reproduce.py paper                  # regenerate everything under paper/ and compare byte for byte
  python src/reproduce.py list [--level cpu]     # every registered result, its level and whether its inputs are here
  python src/reproduce.py show results/headroom_splits_ade_vitl_bank683
  python src/reproduce.py verify <result dir>... # re-run cpu-level analyses, compare with the committed results.json
  python src/reproduce.py run <result dir>... [--dry-run]

`verify` restores the committed directory afterwards, so it never changes results/; `run` overwrites it.
The confirmation reserve (meta/ade_confirmation_reserve_v1.json) was read once; its entry is listed but refuses to run.
"""
import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK683, BANK1366, BANK2731 = 'meta/bank_coco_oi683_v1.json', 'meta/bank_coco_oi1366_v1.json', 'meta/bank_coco_oi2731_v1.json'
ENVS = {  # environment -> (python, what it is for); see README.md for how each is built
    'repo': ('.venv', 'analyses, tables, figures (requirements.txt)'),
    'probe': ('.venv-probe', 'CAT-Seg and SED forward passes (CAT-Seg / SED checkouts outside the repo)'),
    'fcclip': ('.venv-fcclip', 'FC-CLIP forward passes (detectron2 + FC-CLIP checkouts, open_clip_torch==2.20.0)'),
    'ovd': ('.venv-ovd', 'Grounding DINO / MM-Grounding DINO / OWLv2 forward passes (transformers==5.17.0)'),
}
GT = {'ade': ['cache/sclip/gt150.npy', 'cache/sclip/gt847.npy', 'cache/sclip/meta.json'],
      'pascal': ['cache/pascal_sclip/gt59.npy', 'cache/pascal_sclip/gt459.npy', 'cache/pascal_sclip/meta.json'],
      'coco': ['cache/coco_pixels/gt171.npy', 'cache/coco_pixels/gtlvis.npy', 'cache/coco_pixels/meta.json']}   # build_pixel_sample.py --dataset coco

# ---------------------------------------------------------------------------------------------------------------------
# Stored-score configurations: (dataset, tag, model, probe arguments). The tag names results/headroom_probe_<ds>_<tag>
# and cache/headroom_probe[_pascal|_coco]_<tag>; ADE has two probe runs per configuration (400 + 1,600 images, "<tag>_rest").
SCORES = [
    ('ade', '', 'catseg', []),                                       # CAT-Seg ViT-B, COCO-171 bank
    ('ade', 'bank683', 'catseg', ['--bank', BANK683]),
    ('ade', 'vitl', 'catseg', ['--size', 'large']),
    ('ade', 'vitl_bank683', 'catseg', ['--size', 'large', '--bank', BANK683]),
    ('ade', 'sed', 'sed', ['--model', 'sed']),
    ('ade', 'sed_fast8', 'sed', ['--model', 'sed', '--sed-fast', '8']),
    ('ade', 'sed_bank683', 'sed', ['--model', 'sed', '--bank', BANK683]),
    ('ade', 'fcclip', 'fcclip', []),                                 # FC-CLIP, training vocabulary (133 names) as the bank
    ('ade', 'fcclip_bank683', 'fcclip', ['--extra-bank', BANK683]),  # 133 + 683 names, 701 after merging duplicates
    ('ade', 'fcclip_bank1366', 'fcclip', ['--extra-bank', BANK1366]),
    ('ade', 'fcclip_bank2731', 'fcclip', ['--extra-bank', BANK2731]),
    ('ade', 'ft10k', 'catseg', ['--aggregator', 'runs/anchored_vitb/step10000.pt']),
    ('ade', 'anchored_vitb_distract_near', 'catseg', ['--aggregator', 'runs/anchored_vitb_distract_near/step10000.pt']),
    ('pascal', '', 'catseg', []),
    ('pascal', 'vitb_bank683', 'catseg', ['--bank', BANK683]),
    ('pascal', 'vitl_bank683', 'catseg', ['--size', 'large', '--bank', BANK683]),
    ('pascal', 'sed_bank683', 'sed', ['--model', 'sed', '--bank', BANK683]),
    ('pascal', 'fcclip_bank683', 'fcclip', ['--extra-bank', BANK683]),
    ('ade', 'declip_bank683', 'catseg', ['--model', 'declip', '--bank', BANK683]),     # CAT-Seg + DeCLIP EVA02-L (declip_probe_model.py)
    ('pascal', 'declip_bank683', 'catseg', ['--model', 'declip', '--bank', BANK683]),
    # third benchmark, COCO-Stuff 171 -> 1,283 with LVIS v1 (docs/COCO_LVIS_BENCHMARK.md; exp_headroom_probe_coco.py)
    ('coco', 'vitb_bank683', 'catseg', ['--bank', BANK683]),
    ('coco', 'vitl_bank683', 'catseg', ['--size', 'large', '--bank', BANK683]),
    ('coco', 'sed_bank683', 'catseg', ['--model', 'sed', '--bank', BANK683]),
    ('coco', 'declip_bank683', 'catseg', ['--model', 'declip', '--bank', BANK683]),
    ('coco', 'fcclip_bank683', 'fcclip', ['--extra-bank', BANK683]),
]
# configurations with the four "beyond the marginal guarantee" analyses (strata, losses, constructions, calibration size)
EXTENDED = {('ade', t) for t in ['', 'vitl', 'vitl_bank683', 'declip_bank683', 'sed', 'sed_fast8', 'sed_bank683', 'fcclip', 'fcclip_bank683']} | \
               {('pascal', t) for t in ['', 'vitb_bank683', 'vitl_bank683', 'declip_bank683', 'sed_bank683', 'fcclip_bank683']} | \
               {('coco', t) for t in ['vitb_bank683', 'vitl_bank683', 'declip_bank683', 'sed_bank683', 'fcclip_bank683']}
ANALYSES = [('exp_headroom_splits', 'headroom_splits'), ('exp_added_label_risk', 'added_label_risk')]
# the runtime table: 100 development images per configuration, timed on one idle GPU
TIMING = [('vitb_coco', []), ('vitb_bank683', ['--bank', BANK683]), ('vitl_coco', ['--size', 'large']),
          ('vitl_bank683', ['--bank', BANK683, '--size', 'large']), ('sed_coco', ['--model', 'sed']),
          ('sed_fast8', ['--model', 'sed', '--sed-fast', '8']), ('sed_bank683', ['--model', 'sed', '--bank', BANK683]),
          ('fcclip', []), ('fcclip_bank683', ['--extra-bank', BANK683])]
# local timing of the full against the lean bank pass (--lean), 2026-10-26: the segmentation rows .venv-probe can run
TIMING3 = [(tag, extra) for tag, extra in TIMING if not tag.startswith('fcclip') and tag != 'sed_fast8']
TIMING3 += [('declip_bank683', ['--model', 'declip', '--bank', BANK683])]    # 2026-11-01 (not timed on the GH200)
RB_ANALYSES = [('exp_conditional_risk', 'conditional_risk'), ('exp_alternative_losses', 'alternative_losses'),
               ('exp_set_constructions', 'set_constructions'), ('exp_calibration_size', 'calibration_size')]
# the set-size distributions of the supplement (exp_set_size_dist.py, exp_set_size_dist_label.py): the configurations whose stored scores were on the writing machine
SET_SIZE_DIST = {('ade', 'vitl_bank683'), ('ade', 'sed_bank683'), ('pascal', 'vitl_bank683'), ('pascal', 'sed_bank683'), ('coco', 'sed_bank683')}


def sfx(tag): return f'_{tag}' if tag else ''


def score_stores(ds, tag):
    if ds == 'ade':
        base = 'cache/headroom_probe' + sfx(tag)
        return [base, (base + '_rest') if tag else 'cache/headroom_probe_rest']
    return [f'cache/headroom_probe_{ds}' + sfx(tag)]


def probe_records(ds, tag):
    if ds == 'ade':
        return [f'results/headroom_probe_ade{sfx(tag)}', f'results/headroom_probe_ade{sfx(tag)}_rest' if tag else 'results/headroom_probe_ade_rest']
    return [f'results/headroom_probe_{ds}{sfx(tag)}']


def registry():
    R = {}

    def add(out, level, env, cmds, needs=(), note=''):
        R[out] = dict(level=level, env=env, cmds=cmds, needs=list(needs), note=note)

    rest = ['--roles', 'fit,calibration,evaluation']
    for ds, tag, model, args in SCORES:
        rec, stores = probe_records(ds, tag), score_stores(ds, tag)
        if model == 'fcclip':
            base = ['src/exp_fcclip_probe.py'] + (['--dataset', ds] if ds != 'ade' else []) + args
            cmds = [base + ['--check', '--tag', tag]] + ([base + rest + ['--tag', tag + '_rest']] if ds == 'ade' else [])
        elif ds == 'ade':
            tags = ['--tag', tag] if tag else []
            cmds = [['src/exp_headroom_probe.py'] + args + tags, ['src/exp_headroom_probe.py'] + args + rest + ['--tag', (tag + '_rest') if tag else 'rest']]
        else:
            cmds = [[f'src/exp_headroom_probe_{ds}.py'] + args + (['--tag', tag] if tag else [])]
        needs = GT[ds] + [a for a in args if a.startswith('runs/')]
        for r, s in zip(rec, stores):
            add(r, 'gpu', 'fcclip' if model == 'fcclip' else 'probe', [cmds[rec.index(r)]], needs,
                note=f'writes the stored scores {s}/ (float16, per sampled pixel and label) next to this record')
        todo = ANALYSES + (RB_ANALYSES if (ds, tag) in EXTENDED else []) + ([('exp_set_size_dist', 'set_size_dist'), ('exp_set_size_dist_label', 'set_size_dist_label')] if (ds, tag) in SET_SIZE_DIST else [])
        for script, stem in todo:
            # COCO runs the protocol-frozen added-label script through its path-substitution wrapper
            cmd = ['src/coco_frozen_analyses.py', 'added_label_risk'] if (ds, script) == ('coco', 'exp_added_label_risk') else [f'src/{script}.py']
            add(f'results/{stem}_{ds}{sfx(tag)}', 'cpu', 'repo', [cmd + ['--dataset', ds] + (['--tag', tag] if tag else [])],
                GT[ds] + stores + [f'{r}/protocol.json' for r in rec])

    for name, extra in [('anchor_bank_ade', []), ('anchor_bank_large_ade', ['--large']), ('anchor_bank_huge_ade', ['--huge'])]:
        add(f'results/{name}', 'gpu', 'probe', [['src/exp_anchor_bank.py'] + extra], GT['ade'] + ['results/headroom_probe_ade/protocol.json'],
            note='bank sweep on the 400 images of the first ViT-B probe run')
    # the 512 Open Images names of the 683-name bank redrawn five times, COCO-171 kept (tab:bankseeds)
    for m in ['sed', 'vitl']:
        add(f'results/bank_seeds_ade_{m}', 'gpu', 'probe', [['src/exp_bank_seeds.py', '--model', m]],
            GT['ade'] + ['results/headroom_probe_ade/protocol.json', BANK683, 'meta/distractors_openimages_v1.json'] + score_stores('ade', f'{m}_bank683')[:1],
            note='images and splits of the bank sweep; the bank of the paper is scored again and compared with the stored scores')
    for tag, extra in [('', []), ('vitl', ['--size', 'large', '--tag', 'vitl'])]:
        add(f'results/bank_select_coco{sfx(tag)}', 'gpu', 'probe', [['src/exp_bank_select_coco.py'] + extra],
            ['data/coco-stuff/images/val2017', 'data/coco-stuff/annotations_detectron2/val2017'],
            note='bank size chosen on COCO-Stuff val2017, no evaluation dataset read (scripts/fetch_coco_val.sh)')
    add('results/bank_unrelated_coco', 'gpu', 'probe', [['src/exp_bank_unrelated_coco.py']],
        ['data/coco-stuff/images/val2017', 'data/coco-stuff/annotations_detectron2/val2017', 'meta/bank_unrelated_v1.json'],
        note='banks of abstract nouns and non-words on the images and splits of bank_select_coco (meta/bank_unrelated_v1.json from src/build_unrelated_banks.py)')
    add('results/audit_controls_ade', 'gpu', 'probe', [['src/exp_audit_controls.py']], GT['ade'] + score_stores('ade', '')[:1],
        note='pruning removed; one label at a time against the bank')
    add('results/qualitative_ade', 'gpu', 'probe', [['src/fig_qualitative.py', '--image', '897', '--vmax', '10'], ['src/fig_qualitative.py', '--stage', 'panel', '--vmax', '10']],
        GT['ade'] + score_stores('ade', 'vitl_bank683') + ['results/headroom_splits_ade_vitl_bank683/results.json'],
        note='selected image for the problem figure (Sec. 4, paper/fig/fig_problem.pdf) and the qualitative figure (supplement, fig_qualitative.pdf) and the supplement panel of random images (fig_qualitative_panel.pdf, panel.json); thresholds of the median cal1000 split')
    add('results/clipseg_baseline_ade', 'gpu', 'probe', [['src/exp_clipseg_baseline.py']], GT['ade'], note='CLIPSeg (Hugging Face transformers)')
    for tag, extra in TIMING:
        fc = tag.startswith('fcclip')
        add(f'results/headroom_probe_ade_timing2_{tag}', 'gpu', 'fcclip' if fc else 'probe',
            [['src/exp_fcclip_probe.py' if fc else 'src/exp_headroom_probe.py'] + extra + ['--limit', '100', '--tag', f'timing2_{tag}']],
            GT['ade'], note='run all nine back to back on an otherwise idle GPU')
    for tag, extra in TIMING3:
        for lean in ['', '_lean']:
            add(f'results/headroom_probe_ade_timing3_{tag}{lean}', 'gpu', 'probe',
                [['src/exp_headroom_probe.py'] + extra + (['--lean'] if lean else []) + ['--limit', '100', '--tag', f'timing3_{tag}{lean}']],
                GT['ade'], note='full and lean bank pass timed back to back on an otherwise idle RTX 5070 Ti; candidate scores identical (tests/check_lean_bank.py)')
    add('results/lean_bank_check', 'gpu', 'probe',
        [['tests/check_lean_bank.py', '--size', 'large', '--bank', BANK683], ['tests/check_lean_bank.py', '--model', 'sed', '--bank', BANK683], ['tests/check_lean_bank.py', '--size', 'base']],
        GT['ade'], note='lean bank pass: key/value sums and anchored logits bitwise equal to the full pass on 20 ADE images per model; timing3_repeats.json records the repeat timing runs')
    # peak memory per arm as the vocabulary grows, local RTX 5070 Ti; peaks depend on the GPU and driver
    for tag, args in [('vitb', ['--model', 'catseg', '--size', 'base']), ('vitl', ['--model', 'catseg', '--size', 'large']), ('sed', ['--model', 'sed'])]:
        add(f'results/memory_{tag}', 'gpu', 'probe', [['src/exp_memory.py'] + args + ['--limit', '3']], GT['ade'],
            note='peak reset before each arm; the three run back to back on an otherwise idle GPU')
    add('results/memory_declip', 'gpu', 'probe', [['src/exp_memory.py', '--model', 'declip', '--limit', '3']], GT['ade'],
        note='run after the DeCLIP timing pair')
    add('results/memory_fcclip', 'gpu', 'fcclip', [['src/exp_memory_fcclip.py', '--limit', '3']], GT['ade'],
        note='FC-CLIP counterpart of exp_memory.py')
    for ds in ['ade150', 'ade847', 'pc459', 'pc59']:
        for lane, env, cmd in [('vitb', 'probe', ['src/exp_miou_full.py', '--model', 'catseg', '--size', 'base']),
                               ('vitl', 'probe', ['src/exp_miou_full.py', '--model', 'catseg', '--size', 'large']),
                               ('declip', 'probe', ['src/exp_miou_full.py', '--model', 'declip', '--size', 'large']),
                               ('sed', 'probe', ['src/exp_miou_full.py', '--model', 'sed', '--size', 'large']),
                               ('fcclip', 'fcclip', ['src/exp_fcclip_miou.py'])]:
            add(f'results/miou_full_{ds}_{lane}', 'gpu', env, [cmd + ['--dataset', ds]], note='full-resolution mIoU, whole validation set')
    add('results/seg_added_accuracy', 'cpu', 'repo', [['src/exp_seg_added_accuracy.py']],
        [f'results/miou_full_{ds}_{lane}' for ds in ['ade847', 'pc459'] for lane in ['vitb', 'vitl', 'declip', 'sed', 'fcclip']]
        + ['meta/register_ade20k_full.py', 'data/ADEChallengeData2016/objectInfo150.txt', 'data/pascal/labels.txt', 'data/pascal/59_labels.txt'],
        note='post hoc addition: pixel accuracy on source and added classes from the stored confusion matrices (tab:pixaccadded)')
    for gv, syn in [('original', 'first'), ('original', 'mean'), ('square', 'first')]:
        add(f'results/miou_full_pc59_vitb_gv{gv}_syn{syn}', 'gpu', 'probe',
            [['src/exp_miou_full.py', '--model', 'catseg', '--size', 'base', '--dataset', 'pc59', '--arms', 'native',
              '--global-view', gv, '--synonyms', syn, '--tag', f'vitb_gv{gv}_syn{syn}']],
            note='protocol check: native ViT-B with the released global view and/or first-synonym text')
    add('results/declip_check', 'gpu', 'probe', [['tests/check_declip_anchor.py']], ['results/declip_check/upstream.pt'],
        note='DeCLIPProbe against the upstream release; upstream.pt comes from TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 .venv-fcclip/bin/python tests/check_declip_upstream.py')
    # per-image vocabularies (sec:adaptive) and label-level calibration for the added labels (sec:labelguarantee, sec:weights):
    # CAT-Seg ViT-L with the 683-name bank, all 2,000 ADE validation images; development data, run after the reserve read
    vl = ['--tag', 'vitl_bank683', '--size', 'large']
    vl_records = [f'{r}/protocol.json' for r in probe_records('ade', 'vitl_bank683')]
    add('results/adaptive_vocab_probe_vitl_bank683', 'gpu', 'probe', [['src/exp_adaptive_vocab_probe.py'] + vl], GT['ade'] + vl_records,
        note='native CAT-Seg at each per-image vocabulary; writes cache/adaptive_vocab_vitl_bank683/')
    add('results/lexicon_probe_vitl_bank683', 'gpu', 'probe', [['src/exp_lexicon_probe.py'] + vl], GT['ade'] + vl_records + ['meta/distractors_openimages_v1.json'],
        note='native source-label scores at lexicons of 1,690-17,001 names; writes cache/lexicon_vitl_bank683/')
    add('results/adaptive_vocab_vitl_bank683', 'cpu', 'probe', [['src/exp_adaptive_vocab.py', '--tag', 'vitl_bank683']],
        GT['ade'] + score_stores('ade', 'vitl_bank683') + ['cache/adaptive_vocab_vitl_bank683', 'cache/lexicon_vitl_bank683'])
    add('results/label_exchange_probe_vitl_bank683', 'gpu', 'probe', [['src/exp_label_exchange_probe.py'] + vl], GT['ade'] + vl_records,
        note='native CAT-Seg at 10 random 150-name source vocabularies; writes cache/label_exchange_vitl_bank683/native_sets.npy')
    lx = ['src/exp_label_exchange.py', '--tag', 'vitl_bank683']
    add('results/label_exchange_ade_vitl_bank683', 'cpu', 'repo', [lx + ['--dataset', 'ade', '--schemes', 'all3,all5']],
        GT['ade'] + score_stores('ade', 'vitl_bank683') + ['cache/label_exchange_vitl_bank683/native_sets.npy', 'results/label_exchange_probe_vitl_bank683/protocol.json'])
    add('results/label_exchange_pascal_vitl_bank683_schemes', 'cpu', 'repo', [lx + ['--dataset', 'pascal', '--suffix', '_schemes']],
        GT['pascal'] + score_stores('pascal', 'vitl_bank683'),
        note='the recorded run wrote results/label_exchange_pascal_vitl_bank683 and was copied to this name; its hashes predate the --oracle option')
    for ds in ['ade', 'pascal']:
        add(f'results/label_exchange_{ds}_vitl_bank683_oracle', 'cpu', 'repo', [lx + ['--dataset', ds, '--designs', 'dataset split', '--oracle', '--suffix', '_oracle']],
            GT[ds] + score_stores(ds, 'vitl_bank683'), note='prevalence weights from predicted vs true prevalence (supplement)')
        add(f'results/label_exchange_{ds}_vitl_bank683_delta', 'cpu', 'repo', [lx + ['--dataset', ds, '--schemes', 'all3', '--suffix', '_delta']],
            GT[ds] + score_stores(ds, 'vitl_bank683') + (['cache/label_exchange_vitl_bank683/native_sets.npy', 'results/label_exchange_probe_vitl_bank683/protocol.json'] if ds == 'ade' else []),
            note='source loss and Delta(t) = added minus source mean loss at the calibrated threshold (Proposition 4)')
    clx = ['src/coco_frozen_analyses.py', 'label_exchange', '--dataset', 'coco', '--tag', 'vitl_bank683']
    for suffix, extra in [('_delta', ['--schemes', 'all3']), ('_schemes', []), ('_oracle', ['--designs', 'dataset split', '--oracle'])]:
        add(f'results/label_exchange_coco_vitl_bank683{suffix}', 'cpu', 'repo', [clx + extra + ['--suffix', suffix]],
            GT['coco'] + score_stores('coco', 'vitl_bank683') + ['results/headroom_probe_coco_vitl_bank683/protocol.json'],
            note='third benchmark; exp_label_exchange.py run unchanged through src/coco_frozen_analyses.py')
    # per-image vocabularies with SED (sec:adaptivesed)
    sd_records = [f'{r}/protocol.json' for r in probe_records('ade', 'sed_bank683')]
    add('results/adaptive_vocab_probe_sed_bank683', 'gpu', 'probe', [['src/exp_adaptive_vocab_probe.py', '--tag', 'sed_bank683', '--model', 'sed']],
        GT['ade'] + sd_records, note='native SED at each per-image vocabulary; writes cache/adaptive_vocab_sed_bank683/')
    add('results/lexicon_probe_sed_bank683', 'gpu', 'probe', [['src/exp_lexicon_probe_sed.py']], GT['ade'] + sd_records + ['meta/distractors_openimages_v1.json'],
        note='native SED source-label scores at lexicons of 1,690-17,001 names (streamed class-attention sums; --check records the equality with the native pass); writes cache/lexicon_sed_bank683/')
    add('results/adaptive_vocab_sed_bank683', 'cpu', 'probe', [['src/exp_adaptive_vocab.py', '--tag', 'sed_bank683']],
        GT['ade'] + score_stores('ade', 'sed_bank683') + ['cache/adaptive_vocab_sed_bank683', 'cache/lexicon_sed_bank683'])
    fc_records = [f'{r}/protocol.json' for r in probe_records('ade', 'fcclip_bank683')]
    add('results/adaptive_vocab_probe_fcclip_bank683', 'gpu', 'fcclip', [['src/exp_adaptive_vocab_probe_fcclip.py', '--tag', 'fcclip_bank683']],
        GT['ade'] + fc_records, note='native FC-CLIP at each per-image vocabulary (one forward pass per image); writes cache/adaptive_vocab_fcclip_bank683/')
    add('results/lexicon_probe_fcclip_bank683', 'gpu', 'fcclip', [['src/exp_lexicon_probe_fcclip.py']], GT['ade'] + fc_records + ['meta/distractors_openimages_v1.json'],
        note='native FC-CLIP source-label scores at lexicons of 1,690-17,001 names (one forward pass per image with the whole lexicon as text classifier; --check records '
             'that the lexicon columns leave the per-query logits and masks unchanged); writes cache/lexicon_fcclip_bank683/')
    add('results/adaptive_vocab_fcclip_bank683', 'cpu', 'probe', [['src/exp_adaptive_vocab.py', '--tag', 'fcclip_bank683']],
        GT['ade'] + score_stores('ade', 'fcclip_bank683') + ['cache/adaptive_vocab_fcclip_bank683', 'cache/lexicon_fcclip_bank683'])
    # per-image vocabularies on Pascal Context, 59 -> 458 (sec:adaptivepascal); run locally 2026-09-27
    for tag, extra in [('vitl_bank683', ['--size', 'large']), ('sed_bank683', ['--model', 'sed'])]:
        pa = ['--dataset', 'pascal', '--tag', tag] + extra
        pa_records = [f'{r}/protocol.json' for r in probe_records('pascal', tag)]
        add(f'results/adaptive_vocab_probe_pascal_{tag}', 'gpu', 'probe', [['src/exp_adaptive_vocab_probe.py'] + pa + ['--check'], ['src/exp_adaptive_vocab_probe.py'] + pa],
            GT['pascal'] + pa_records, note=f'the --check exactness test first; writes cache/adaptive_vocab_pascal_{tag}/')
        add(f'results/adaptive_vocab_pascal_{tag}', 'cpu', 'probe', [['src/exp_adaptive_vocab.py', '--dataset', 'pascal', '--tag', tag]],
            GT['pascal'] + score_stores('pascal', tag) + [f'cache/adaptive_vocab_pascal_{tag}'])
    # detection, COCO 80 -> LVIS 1,204 (sec:detection; docs/OVD_DETECTION_BENCHMARK.md): box-level scores, then CRC
    ovd_meta = ['meta/ovd_coco_lvis_vocab_v1.json', 'meta/bank_ovd_a_v1.json', 'meta/bank_ovd_b_v1.json']
    for m in ['gdino_t', 'mmgdino_t', 'gdino_b', 'owlv2']:
        add(f'results/ovd_probe_{m}', 'gpu', 'ovd', ([['src/exp_ovd_probe.py', '--model', m, '--check']] if m != 'owlv2' else []) + [['src/exp_ovd_probe.py', '--model', m]],
            ovd_meta, note='2,000 COCO val2017 images; the --check exactness test first; writes cache/ovd_probe_' + m + '/'
            + ('; the recorded run predates restore_heads, which reproduces it exactly for this checkpoint' if m == 'gdino_t' else ''))
        add(f'results/ovd_crc_{m}', 'cpu', 'repo', [['src/exp_ovd_crc.py', '--model', m]], [f'cache/ovd_probe_{m}', f'results/ovd_probe_{m}/protocol.json'])
        add(f'results/ovd_floor_{m}', 'cpu', 'repo', [['src/exp_ovd_floor.py', '--model', m]], [f'cache/ovd_probe_{m}', f'results/ovd_probe_{m}/protocol.json'],
            note='post hoc diagnostic: unlocalised boxes and label-level trials whose threshold is the lowest grid point')
        add(f'results/ovd_accuracy_{m}', 'cpu', 'repo', [['src/exp_ovd_accuracy.py', '--model', m]], [f'cache/ovd_probe_{m}', f'results/ovd_probe_{m}/protocol.json'],
            note='post hoc addition: box-level top-1 accuracy at 1,204 names (tab:ovdacc)')
        add(f'results/ovd_probe_{m}_timing', 'gpu', 'ovd', [['src/exp_ovd_probe.py', '--model', m, '--limit', '100', '--tag', '_timing']], ovd_meta,
            note='clean timing: first 100 images, every arm timed separately, on an otherwise idle GPU (the four run back to back)')
    # label-level CRC for the added labels, the four models other than CAT-Seg ViT-L (tab:labelmodels;
    # ViT-L is registered above)
    for ds in ['ade', 'pascal', 'coco']:
        for t in ['declip_bank683', 'sed_bank683', 'fcclip_bank683'] + (['bank683'] if ds == 'ade' else ['vitb_bank683']):
            cmd = (['src/coco_frozen_analyses.py', 'label_exchange', '--dataset', 'coco'] if ds == 'coco' else ['src/exp_label_exchange.py', '--dataset', ds])
            add(f'results/label_exchange_{ds}_{t}_schemes', 'cpu', 'repo', [cmd + ['--tag', t, '--suffix', '_schemes']],
                GT[ds] + score_stores(ds, t), note='all designs, default schemes')
    # image-averaged label loss, the quantity of prop:newimages (tab:labelimages): the exchangeable trials replayed, every model
    for ds in ['ade', 'pascal', 'coco']:
        for t in ['vitl_bank683', 'declip_bank683', 'sed_bank683', 'fcclip_bank683'] + (['bank683'] if ds == 'ade' else ['vitb_bank683']):
            add(f'results/label_exchange_images_{ds}_{t}', 'cpu', 'repo', [['src/exp_label_exchange_images.py', '--dataset', ds, '--tag', t]],
                GT[ds] + score_stores(ds, t), note='same seed and draws as exp_label_exchange.py; the pooled columns reproduce it')
    # added-label guarantee from m randomly drawn, annotated added names, benchmark's own source classes (tab:labelsample)
    for ds in ['ade', 'pascal', 'coco']:
        for t in ['vitl_bank683', 'sed_bank683']:
            add(f'results/label_sample_{ds}_{t}', 'cpu', 'repo', [['src/exp_label_sample.py', '--dataset', ds, '--tag', t, '--ms', '10,20,30,50,75,100,150,200']],
                GT[ds] + score_stores(ds, t), note=f'its replay arms reproduce label_exchange_{ds}_{t}_schemes')
    # per-name (class-conditional) thresholds on the anchored scores, and the hybrid with the image-level one (tab:pername)
    for ds, t in [('ade', 'vitl_bank683'), ('ade', 'sed_bank683'), ('ade', 'fcclip_bank683'), ('pascal', 'vitl_bank683'),
                  ('pascal', 'sed_bank683'), ('coco', 'sed_bank683')]:
        add(f'results/per_name_{ds}_{t}', 'cpu', 'repo', [['src/exp_per_name.py', '--dataset', ds, '--tag', t, '--splits', '500']],
            GT[ds] + score_stores(ds, t), note='post hoc addition; same image splits as exp_label_sample.py')
    # native references for calibration reuse (native size at V0, tightened alpha, native arg-max outside the anchored set) and
    # added-label risk against measured added-label hardness (prop:shift); ADE20K development data
    for t in ['vitl_bank683', 'sed_bank683']:
        add(f'results/native_baselines_ade_{t}', 'cpu', 'repo', [['src/exp_native_baselines.py', '--dataset', 'ade', '--tag', t]],
            GT['ade'] + score_stores('ade', t), note='same images, splits and grid as headroom_splits_ade_' + t)
        add(f'results/label_hardness_ade_{t}', 'cpu', 'repo', [['src/exp_label_hardness.py', '--dataset', 'ade', '--tag', t]],
            GT['ade'] + score_stores('ade', t), note="same trials as label_exchange_ade_" + t + "'s exchangeable design")
    # recalibration in deployment (sec:problem)
    fig1 = [('ade', 'bank683'), ('ade', 'vitl_bank683'), ('ade', 'declip_bank683'), ('ade', 'sed_bank683'), ('ade', 'fcclip_bank683')] + \
           [(ds, t) for ds in ['pascal', 'coco'] for t in ['vitb_bank683', 'vitl_bank683', 'declip_bank683', 'sed_bank683', 'fcclip_bank683']]
    add('results/silent_failure', 'cpu', 'repo', [['src/exp_silent_failure.py']], [f'results/headroom_splits_{ds}_{t}/results.json' for ds, t in fig1],
        note='set size of the reused native threshold against the size needed, the 15 combinations of Fig. 1; stored results only')
    rr = [('ade', 'vitl_bank683'), ('ade', 'sed_bank683'), ('ade', 'fcclip_bank683'), ('pascal', 'vitl_bank683'), ('pascal', 'sed_bank683'), ('coco', 'sed_bank683')]
    add('results/repeated_recal', 'cpu', 'repo', [['src/exp_repeated_recal.py']],
        sorted({g for ds, _ in rr for g in GT[ds]}) + [s for ds, t in rr for s in score_stores(ds, t)] + [f'results/headroom_splits_{ds}_{t}/results.json' for ds, t in rr],
        note='delta/K calibration-conditional (RCPS, Hoeffding-Bentkus) thresholds for K recalibrations; the configurations whose stored scores are on the writing machine')
    # general multimodal model: the stored API responses are re-analysed; the run stage calls the Anthropic API
    # (claude-opus-5-5, about $34 for 1,000 images) and is not part of verify
    add('results/claude_baseline_ade', 'cpu', 'repo', [['src/exp_claude_baseline.py', '--stage', 'analyze'], ['src/exp_claude_baseline.py', '--stage', 'crc']],
        ['results/claude_baseline_ade/raw.jsonl', 'results/claude_baseline_ade/protocol.json'] + GT['ade'] + score_stores('ade', 'vitl_bank683'),
        note='raw.jsonl holds every prompt response; to re-query: --stage run --images 1000 --workers 8 with ANTHROPIC_API_KEY set')
    # free-form per-image names (docs/FREEFORM_NAMES_PROTOCOL.md): the namer's stored responses are re-analysed; the run stage
    # calls the Anthropic API (claude-opus-5-5, about $9.50 for 2,000 images) and is not part of verify
    add('results/freeform_names_ade', 'cpu', 'repo', [['src/exp_freeform_names.py', '--stage', 'analyze']],
        ['results/freeform_names_ade/raw.jsonl', 'results/freeform_names_ade/protocol.json', 'meta/natural_vocab_v1.json', 'meta/distractors_openimages_v1.json'],
        note='writes names.json; to re-query: --stage run --images 2000 --workers 8 with ANTHROPIC_API_KEY set')
    for t, env, cmd in [('vitl_bank683', 'probe', ['src/exp_freeform_vocab_probe.py', '--tag', 'vitl_bank683', '--size', 'large']),
                        ('sed_bank683', 'probe', ['src/exp_freeform_vocab_probe.py', '--tag', 'sed_bank683', '--model', 'sed']),
                        ('fcclip_bank683', 'fcclip', ['src/exp_freeform_vocab_probe_fcclip.py', '--tag', 'fcclip_bank683'])]:
        records = [f'{r}/protocol.json' for r in probe_records('ade', t)]
        add(f'results/freeform_vocab_probe_{t}', 'gpu', env, [cmd + ['--check'], cmd], GT['ade'] + records + score_stores('ade', t) + ['results/freeform_names_ade/names.json'],
            note=f'--check compares the source columns with the stored scores; writes cache/freeform_vocab_{t}/')
        lex = ['cache/lexicon_' + t] if t != 'vitl_bank683' else []      # the ViT-L lexicon stores are not on the writing machine
        add(f'results/freeform_vocab_{t}', 'cpu', 'probe', [['src/exp_freeform_vocab.py', '--tag', t]],
            GT['ade'] + score_stores('ade', t) + [f'cache/freeform_vocab_{t}'] + lex)
        # W1 of the 2026-11-01 review: the 683-name bank was chosen on the first 400 ADE images; the other 1,600 are disjoint from that choice
        add(f'results/headroom_splits_ade_{t}_disjoint', 'cpu', 'probe', [['src/exp_headroom_splits.py', '--tag', t, '--disjoint']],
            GT['ade'] + score_stores('ade', t)[1:] + ['results/headroom_probe_ade/protocol.json'])
    add('results/confirmation_ade_vitl_bank683', 'reserve', 'probe',
        [['src/exp_confirm_reserve.py', '--tag', 'vitl_bank683', '--size', 'large', '--bank', BANK683]],
        ['meta/ade_confirmation_reserve_v1.json'],
        note='the 2,000 reserved ADE training images, read once for this configuration; do not re-run for model selection')
    add('results/label_exchange_ade_reserve_vitl_bank683', 'reserve', 'probe',
        [['src/build_gt_reserve.py', '--filenames'], ['src/build_gt_reserve.py', '--reserve-read'],
         lx + ['--dataset', 'ade_reserve', '--schemes', 'all3', '--reserve-read']],
        ['meta/ade_confirmation_reserve_v1.json', 'data/ade_full_train', 'results/confirmation_ade_vitl_bank683'],
        note='second reserve read, added-label guarantee, under docs/PROTOCOL_ADDED_LABEL_RESERVE.md; reuses the stored reserve scores; run once')
    coco = ['--images', 'data/coco-stuff/images/train2017', '--labels', 'data/coco-stuff/annotations_detectron2/train2017', '--iters', '10000', '--batch', '4', '--tf32']
    add('runs/anchored_vitb', 'train', 'probe', [['src/train_anchored_catseg.py'] + coco + ['--out', 'runs/anchored_vitb']],
        note='aggregator fine-tuning, ~1.1 h on a GH200, 64 GB peak; feeds the ft10k scores')
    add('runs/anchored_vitb_distract_near', 'train', 'probe',
        [['src/train_anchored_catseg.py'] + coco + ['--seed', '0', '--distractors', 'meta/distractors_openimages_v1.json', '--distractor-near', '1.0',
                                                    '--out', 'runs/anchored_vitb_distract_near']],
        note='as above with near Open Images distractors; feeds the anchored_vitb_distract_near scores')
    return R


def python_for(env):
    root = ROOT/ENVS[env][0]
    for p in (root/'Scripts'/'python.exe', root/'bin'/'python'):
        if p.exists(): return str(p)
    return sys.executable if env == 'repo' else f'{ENVS[env][0]}/bin/python'    # analyses run in whatever Python runs this script


def missing(entry):
    return [n for n in entry['needs'] if not (ROOT/n).exists()]


def run_entry(out, entry, dry=False):
    if entry['level'] == 'reserve':
        raise SystemExit(f'{out}: the confirmation reserve is not re-read by this script (see its note).')
    env = dict(os.environ, PYTHONPATH='src')
    for cmd in entry['cmds']:
        line = [python_for(entry['env'])] + cmd
        print('  $ PYTHONPATH=src ' + ' '.join(line), flush=True)
        if not dry:
            subprocess.run(line, cwd=ROOT, env=env, check=True)


def compare_json(a, b, path='', tol=1e-9):
    """Largest absolute difference between two JSON trees (a committed, b fresh); raises on a structural difference.
    Keys only in the fresh tree are descriptive fields the code gained after the committed run (e.g. 'dataset') and are
    reported, not compared."""
    if isinstance(a, dict):
        if set(a) - set(b): raise ValueError(f'{path}: keys missing from the fresh run ({sorted(set(a) - set(b))[:5]})')
        if set(b) - set(a): print(f'  note: {path or "/"} has new keys {sorted(set(b) - set(a))[:5]} (not in the committed file)')
        return max([compare_json(a[k], b[k], f'{path}/{k}', tol) for k in a] or [0.0])
    if isinstance(a, list):
        if len(a) != len(b): raise ValueError(f'{path}: lengths {len(a)} vs {len(b)}')
        return max([compare_json(x, y, f'{path}[{i}]', tol) for i, (x, y) in enumerate(zip(a, b))] or [0.0])
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(float(a) - float(b))
    if a != b and path.split('/')[-1] not in ('hashes',):
        raise ValueError(f'{path}: {str(a)[:60]!r} vs {str(b)[:60]!r}')
    return 0.0


def verify(out, entry, tol):
    if entry['level'] != 'cpu':
        raise SystemExit(f'{out}: only cpu-level results are verified by re-running (level {entry["level"]}).')
    committed = json.loads((ROOT/out/'results.json').read_text())
    backup = Path(tempfile.mkdtemp(prefix='verify_'))/'committed'
    shutil.copytree(ROOT/out, backup)
    try:
        run_entry(out, entry)
        fresh = json.loads((ROOT/out/'results.json').read_text())
        fresh.pop('hashes', None); committed.pop('hashes', None)
        d = compare_json(committed, fresh)
        print(f'{out}: {"REPRODUCED" if d <= tol else "DIFFERS"} (largest absolute difference {d:.2e}, tolerance {tol:.0e})')
        return d <= tol
    finally:
        shutil.rmtree(ROOT/out); shutil.copytree(backup, ROOT/out); shutil.rmtree(backup.parent)


PAPER_FILES = ['paper/numbers.tex'] + [f'paper/tables/{t}.tex' for t in
               ['adaptive', 'adaptive_fcclip', 'adaptive_main', 'adaptive_pascal', 'adaptive_sed', 'added', 'added_coco', 'added_pascal', 'ade_main', 'bank', 'bank_main', 'bank_seeds', 'calsize', 'coco_main', 'confirm',
                'constructions', 'curve', 'fcclip_banks', 'finetune', 'hardness', 'labelexch', 'labelexch_models', 'labelexch_heldout', 'labelexch_images', 'labelexch_weights', 'labelexch_weights_coco', 'labelsample', 'losses',
                'miou', 'miou_pixacc', 'pixacc_added', 'nativerefs', 'overview', 'overview_b', 'ovd', 'ovd_acc', 'ovd_full', 'pascal_main', 'runtime', 'strata', 'strata_coco', 'strata_pascal', 'losses_a', 'losses_b', 'constructions_a', 'constructions_b', 'setsize', 'setsize_b', 'setsize_label', 'labelsample_a', 'labelsample_b', 'runtime_lean', 'pername', 'freeform', 'memory']]
FIGURES = ['fig1_risk_after_growth', 'fig2_anchored_after_growth', 'fig3_set_size_vs_additions', 'fig4_added_label_risk']


def paper(write):
    """Regenerate numbers, tables and figures from results/ and compare with what paper/ holds."""
    tmp = Path(tempfile.mkdtemp(prefix='paper_'))
    for f in PAPER_FILES: (tmp/f).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT/f, tmp/f)
    env = dict(os.environ, PYTHONPATH='src', MPLBACKEND='Agg')
    py = python_for('repo')
    for script in ['src/paper_numbers.py', 'src/plot_headroom.py', 'src/plot_added_label.py']:
        subprocess.run([py, script], cwd=ROOT, env=env, check=True, stdout=subprocess.DEVNULL)
    norm = lambda p: p.read_bytes().replace(b'\r\n', b'\n')
    diff = [f for f in PAPER_FILES if norm(ROOT/f) != norm(tmp/f)]
    diff += [f'paper/fig/{g}.pdf' for g in FIGURES if not filecmp.cmp(ROOT/f'figures/{g}.pdf', ROOT/f'paper/fig/{g}.pdf', shallow=False)]
    if write:
        for g in FIGURES: shutil.copy2(ROOT/f'figures/{g}.pdf', ROOT/f'paper/fig/{g}.pdf')
    else:
        for f in PAPER_FILES: shutil.copy2(tmp/f, ROOT/f)
    shutil.rmtree(tmp)
    n = len(PAPER_FILES) + len(FIGURES)
    if diff:
        print(f'{len(diff)} of {n} generated files differ from paper/' + (' (now overwritten)' if write else ' (left unchanged; --write to accept):'))
        for f in diff: print('  ' + f)
        return write
    print(f'all {n} generated files (numbers.tex, {len(PAPER_FILES)-1} tables, {len(FIGURES)} figures) are identical to paper/')
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('paper'); p.add_argument('--write', action='store_true', help='keep regenerated files (and copy figures into paper/fig)')
    p = sub.add_parser('list'); p.add_argument('--level', choices=['cpu', 'gpu', 'train', 'reserve'])
    p = sub.add_parser('show'); p.add_argument('outs', nargs='+')
    p = sub.add_parser('run'); p.add_argument('outs', nargs='+'); p.add_argument('--dry-run', action='store_true')
    p = sub.add_parser('verify'); p.add_argument('outs', nargs='+'); p.add_argument('--tol', type=float, default=1e-9)
    a = ap.parse_args()
    R = registry()
    if a.cmd == 'paper':
        raise SystemExit(0 if paper(a.write) else 1)
    if a.cmd == 'list':
        for out, e in R.items():
            if a.level and e['level'] != a.level: continue
            m = missing(e)
            print(f'{e["level"]:8s} {e["env"]:7s} {"inputs here" if not m else f"{len(m)} inputs missing":18s} {out}')
        return
    outs = [o.rstrip('/').replace('\\', '/') for o in a.outs]
    unknown = [o for o in outs if o not in R]
    if unknown: raise SystemExit(f'not registered: {unknown}; see `list`')
    if a.cmd == 'show':
        for o in outs:
            e = R[o]; print(f'{o}\n  level {e["level"]}, environment {e["env"]} ({ENVS[e["env"]][1]})')
            if e['note']: print(f'  {e["note"]}')
            for n in e['needs']: print(f'  needs {n}{"" if (ROOT/n).exists() else "  (MISSING)"}')
            run_entry(o, e, dry=True)
    elif a.cmd == 'run':
        for o in outs:
            m = missing(R[o])
            if m and not a.dry_run: raise SystemExit(f'{o}: missing inputs {m}')
            run_entry(o, R[o], dry=a.dry_run)
    else:
        ok = [verify(o, R[o], a.tol) for o in outs]
        raise SystemExit(0 if all(ok) else 1)


if __name__ == '__main__':
    main()
