"""Generate paper/numbers.tex (macros) and paper/tables/*.tex from results/*.json. No number in the paper is
typed by hand: every figure in the text is a macro defined here, every table is an \\input. Pure bookkeeping; no scores
are touched. Run from the repository root: PYTHONPATH=src python src/paper_numbers.py"""
import json
import math
import re
from pathlib import Path

OUT = Path('paper'); TAB = OUT/'tables'
ALPHA, ALPHA2 = 'a0.1', 'a0.05'

# key -> (dataset, headroom tag, extended-analysis (dataset, config), added-label dir suffix, display name, macro stem)
CONFIGS = {
    'vitb':       ('ade', '',              ('ade', 'vitb_coco171'),        'ade',                 'CAT-Seg ViT-B, COCO-171 bank',       'VitB'),
    'vitb683':    ('ade', 'bank683',       None,                           'ade_bank683',         'CAT-Seg ViT-B, 683-name bank',       'VitBBank'),
    'vitl':       ('ade', 'vitl',          ('ade', 'vitl'),                'ade_vitl',            'CAT-Seg ViT-L, COCO-171 bank',       'VitL'),
    'vitl683':    ('ade', 'vitl_bank683',  ('ade', 'vitl_bank683'),        'ade_vitl_bank683',    'CAT-Seg ViT-L, 683-name bank',       'VitLBank'),
    'sed':        ('ade', 'sed',           ('ade', 'sed'),                 'ade_sed',             'SED ConvNeXt-L, COCO-171 bank',      'Sed'),
    'sedfast':    ('ade', 'sed_fast8',     ('ade', 'sed_fast8'),           'ade_sed_fast8',       'SED ConvNeXt-L, fast mode (top-8 rejection)', 'SedFast'),
    'sed683':     ('ade', 'sed_bank683',   ('ade', 'sed_bank683'),         'ade_sed_bank683',     'SED ConvNeXt-L, 683-name bank',      'SedBank'),
    'fcclip':     ('ade', 'fcclip',        ('ade', 'fcclip'),              'ade_fcclip',          'FC-CLIP ConvNeXt-L, 133-name bank',  'Fcclip'),
    'fcclip683':  ('ade', 'fcclip_bank683', ('ade', 'fcclip_bank683'),     'ade_fcclip_bank683',  'FC-CLIP ConvNeXt-L, 701-name bank',  'FcclipBank'),
    'fcclip1366': ('ade', 'fcclip_bank1366', None,                         'ade_fcclip_bank1366', 'FC-CLIP ConvNeXt-L, 1,366-name bank', 'FcclipBankM'),
    'fcclip2731': ('ade', 'fcclip_bank2731', None,                         'ade_fcclip_bank2731', 'FC-CLIP ConvNeXt-L, 2,731-name bank', 'FcclipBankL'),
    'pascal':     ('pascal', '',           ('pascal', 'pascal_vitb_coco171'), 'pascal',           'CAT-Seg ViT-B, COCO-171 bank, Pascal 59$\\to$458',  'Pascal'),
    # Pascal Context for the other configurations (2026-09-23): one probe run per tag, all 2,000 cached images
    'pascal683':       ('pascal', 'vitb_bank683',   ('pascal', 'pascal_vitb_bank683'),   'pascal_vitb_bank683',   'CAT-Seg ViT-B, 683-name bank, Pascal 59$\\to$458',      'PascalBank'),
    'pascalvitl683':   ('pascal', 'vitl_bank683',   ('pascal', 'pascal_vitl_bank683'),   'pascal_vitl_bank683',   'CAT-Seg ViT-L, 683-name bank, Pascal 59$\\to$458',      'PascalVitLBank'),
    'pascalsed683':    ('pascal', 'sed_bank683',    ('pascal', 'pascal_sed_bank683'),    'pascal_sed_bank683',    'SED ConvNeXt-L, 683-name bank, Pascal 59$\\to$458',     'PascalSedBank'),
    'pascalfcclip683': ('pascal', 'fcclip_bank683', ('pascal', 'pascal_fcclip_bank683'), 'pascal_fcclip_bank683', 'FC-CLIP ConvNeXt-L, 701-name bank, Pascal 59$\\to$458', 'PascalFcclipBank'),
    # newer segmenter (2026-09-24): CAT-Seg + DeCLIP EVA02-CLIP-L (CVPR 2025)
    'declip683':       ('ade', 'declip_bank683',    ('ade', 'declip_bank683'),           'ade_declip_bank683',    'CAT-Seg + DeCLIP EVA-L, 683-name bank',  'DeclipBank'),
    'pascaldeclip683': ('pascal', 'declip_bank683', ('pascal', 'pascal_declip_bank683'), 'pascal_declip_bank683', 'CAT-Seg + DeCLIP EVA-L, 683-name bank, Pascal 59$\\to$458', 'PascalDeclipBank'),
    # third benchmark (2026-09-25, docs/COCO_LVIS_BENCHMARK.md): COCO-Stuff 171 -> 1,283 with LVIS
    'coco683':       ('coco', 'vitb_bank683',   ('coco', 'coco_vitb_bank683'),   'coco_vitb_bank683',   'CAT-Seg ViT-B, 683-name bank, COCO 171$\\to$1,283',          'CocoBank'),
    'cocovitl683':   ('coco', 'vitl_bank683',   ('coco', 'coco_vitl_bank683'),   'coco_vitl_bank683',   'CAT-Seg ViT-L, 683-name bank, COCO 171$\\to$1,283',          'CocoVitLBank'),
    'cocodeclip683': ('coco', 'declip_bank683', ('coco', 'coco_declip_bank683'), 'coco_declip_bank683', 'CAT-Seg + DeCLIP EVA-L, 683-name bank, COCO 171$\\to$1,283', 'CocoDeclipBank'),
    'cocosed683':    ('coco', 'sed_bank683',    ('coco', 'coco_sed_bank683'),    'coco_sed_bank683',    'SED ConvNeXt-L, 683-name bank, COCO 171$\\to$1,283',         'CocoSedBank'),
    'cocofcclip683': ('coco', 'fcclip_bank683', ('coco', 'coco_fcclip_bank683'), 'coco_fcclip_bank683', 'FC-CLIP ConvNeXt-L, 701-name bank, COCO 171$\\to$1,283',     'CocoFcclipBank'),
    'ft10k':      ('ade', 'ft10k',        None,                           'ade_ft10k',           'ViT-B, aggregator fine-tuned 10k',   'FtTenK'),
    'distract':   ('ade', 'anchored_vitb_distract_near', None,             'ade_anchored_vitb_distract_near', 'ViT-B, fine-tuned with distractors', 'FtDistract'),
}
MAIN = ['vitb', 'vitb683', 'vitl', 'vitl683', 'declip683', 'sed', 'sedfast', 'sed683', 'fcclip', 'fcclip683']
PASCAL = ['pascal', 'pascal683', 'pascalvitl683', 'pascaldeclip683', 'pascalsed683', 'pascalfcclip683']     # supplement tables; rows appear as the runs land
COCO = ['coco683', 'cocovitl683', 'cocodeclip683', 'cocosed683', 'cocofcclip683']                         # supplement tables, third benchmark
FAMILY = {'vitb': 'CAT-Seg', 'vitl': 'CAT-Seg', 'sed': 'SED', 'fcclip': 'FC-CLIP'}
macros = {}


def load(path):
    p = Path(path)/'results.json'
    return json.loads(p.read_text()) if p.exists() else None


def pc(x, d=1): return f'{100*x:.{d}f}'
def f2(x): return f'{x:.2f}'
def f1(x): return f'{x:.1f}'
def num(x): return f'{x:,}'


def macro(name, value):
    assert re.fullmatch(r'[A-Za-z]+', name), name
    macros[name] = str(value)


def headroom(key):
    ds, tag, *_ = CONFIGS[key]
    return load(f'results/headroom_splits_{ds}' + (f'_{tag}' if tag else ''))


def arms(j, alpha=ALPHA, design='cal1000'):
    return j['designs'][f'{design}_{alpha}']


def headline_row(key, alpha=ALPHA):
    j = headroom(key); d = arms(j, alpha)
    a, f, r, s = d['catseg_anchored'], d['catseg_native_frozen_full'], d['catseg_native_replay_full'], d['catseg_native_source']
    return dict(frozen_risk=f['mean_risk'], frozen_frac=f['frac_splits_above_alpha'], frozen_size=f['mean_size'][0],
                anch_risk=a['mean_risk'], anch_frac=a['frac_splits_above_alpha'], anch_src=a['mean_size'][0], anch_full=a['mean_size'][-1],
                anch_full_lo=a['size_q025'][-1], anch_full_hi=a['size_q975'][-1],
                replay_size=r['mean_size'][0], replay_risk=r['mean_risk'], replay_frac=r['frac_splits_above_alpha'], src_size=s['mean_size'][0], src_risk=s['mean_risk'],
                price=a['mean_size'][-1]-r['mean_size'][0], sclip=d.get('sclip_fixed_source'), splits=j['splits'], images=j['images'])


def table_headline(keys, filename):
    rows = [r'\begin{tabular}{@{}llrrrrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{native, reused} & \multicolumn{3}{c}{native, recalibrated} & \multicolumn{4}{c}{anchored (ours)} \\',
            r'\cmidrule(lr){3-4}\cmidrule(lr){5-7}\cmidrule(lr){8-11}',
            r'Model & bank & risk & splits $>\alpha$ & risk & splits $>\alpha$ & size & risk & splits $>\alpha$ & size & overhead \\', r'\midrule']
    for key in keys:
        if headroom(key) is None: continue
        ds, tag, _, _, name, stem = CONFIGS[key]; h = headline_row(key)
        model, bank = name.split(', ', 1)
        rows.append(f'{model} & {bank} & {pc(h["frozen_risk"])} & {pc(h["frozen_frac"], 0)}\\% & {pc(h["replay_risk"])} & {pc(h["replay_frac"], 0)}\\% & {f2(h["replay_size"])} & '
                    f'{pc(h["anch_risk"])} & {pc(h["anch_frac"], 0)}\\% & {f2(h["anch_src"])}$\\to${f2(h["anch_full"])} & {h["price"]:+.2f} \\\\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')


OVERVIEW = [('CAT-Seg ViT-B', ['vitb683', 'pascal683', 'coco683']), ('CAT-Seg ViT-L', ['vitl683', 'pascalvitl683', 'cocovitl683']),
            ('CAT-Seg + DeCLIP', ['declip683', 'pascaldeclip683', 'cocodeclip683']), ('SED', ['sed683', 'pascalsed683', 'cocosed683']),
            ('FC-CLIP', ['fcclip683', 'pascalfcclip683', 'cocofcclip683'])]


def table_overview(alpha=ALPHA, filename='overview.tex'):
    """Main-text Table 1 (and its alpha = .05 version in the supplement): every model with the default bank on the three
    benchmarks (reused native risk, anchored risk, sizes)."""
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}l' + 'rrrr'*3 + '@{}}', r'\toprule',
            r'& \multicolumn{4}{c}{ADE20K $150\!\to\!845$} & \multicolumn{4}{c}{Pascal Context $59\!\to\!458$} & \multicolumn{4}{c}{COCO-Stuff $171\!\to\!1{,}283$} \\',
            r'\cmidrule(lr){2-5}\cmidrule(lr){6-9}\cmidrule(l){10-13}',
            r'& \multicolumn{2}{c}{risk (\%)} & \multicolumn{2}{c}{set size} ' * 3 + r'\\',
            r'\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}\cmidrule(lr){10-11}\cmidrule(l){12-13}',
            r'Model' + r' & reused & ours & recal. & ours' * 3 + r' \\', r'\midrule']
    for name, keys in OVERVIEW:
        cells = []
        for key in keys:
            h = headline_row(key, alpha)
            cells += [pc(h['frozen_risk']), pc(h['anch_risk']), f2(h['replay_size']), f2(h['anch_full'])]
        rows.append(name + ' & ' + ' & '.join(cells) + r' \\')
    hs = [headline_row(k, alpha) for _, keys in OVERVIEW for k in keys]; sfx = '' if alpha == ALPHA else 'B'
    macro('OverviewAnchFracMin'+sfx, pc(min(h['anch_frac'] for h in hs), 0)); macro('OverviewAnchFracMax'+sfx, pc(max(h['anch_frac'] for h in hs), 0))
    macro('OverviewReplayFracMin'+sfx, pc(min(h['replay_frac'] for h in hs), 0)); macro('OverviewReplayFracMax'+sfx, pc(max(h['replay_frac'] for h in hs), 0))
    cs = [headline_row(k, alpha) for name, keys in OVERVIEW if name != 'FC-CLIP' for k in keys]      # cost-aggregation models
    macro('OverviewCostAggPriceMax'+sfx, f2(max(h['price'] for h in cs)))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')


def table_main():
    table_overview(); table_overview(ALPHA2, 'overview_b.tex')
    table_headline(MAIN, 'ade_main.tex')              # supplement: every ADE20K configuration (both banks, SED fast mode)
    table_headline(PASCAL, 'pascal_main.tex')        # supplement: every model on Pascal Context 59 -> 458
    macro('NumSplits', headline_row('vitb')['splits']); macro('NumAdeImages', num(headline_row('vitb')['images']))
    macro('NumPascalImages', num(headline_row('pascal')['images']))
    macro('NumPascalConfigs', str(sum(headroom(k) is not None for k in PASCAL)))
    table_headline(COCO, 'coco_main.tex')            # supplement: every model on COCO-Stuff 171 -> 1,283 (LVIS)
    macro('NumCocoConfigs', str(sum(headroom(k) is not None for k in COCO)))
    got = [k for k in COCO if headroom(k) is not None]
    if got: macro('NumCocoImages', num(headline_row(got[0])['images']))


def headline_macros(key):
    """Headline macros for every configuration, including those outside the main table (bank sweep, fine-tuning)."""
    stem = CONFIGS[key][5]
    if headroom(key) is None: return
    h = headline_row(key); h2 = headline_row(key, ALPHA2)
    if True:
        for k, v in dict(NativeFrozenRisk=pc(h['frozen_risk']), NativeFrozenFrac=pc(h['frozen_frac'], 0), NativeFrozenSize=f2(h['frozen_size']),
                         AnchRisk=pc(h['anch_risk'], 2), AnchRiskOne=pc(h['anch_risk']), AnchFrac=pc(h['anch_frac'], 0), AnchSrc=f2(h['anch_src']), AnchFull=f2(h['anch_full']),
                         AnchFullLo=f2(h['anch_full_lo']), AnchFullHi=f2(h['anch_full_hi']),
                         ReplaySize=f2(h['replay_size']), ReplayRisk=pc(h['replay_risk'], 2), SrcSize=f2(h['src_size']), Price=f2(abs(h['price'])),
                         PriceSigned=f'{h["price"]:+.2f}', PriceRatio=f2(h['anch_full']/h['replay_size']), NativeFrozenRatio=f1(h['frozen_size']/h['replay_size']),
                         NativeFrozenRiskB=pc(h2['frozen_risk']), AnchRiskB=pc(h2['anch_risk'], 2), AnchSrcB=f2(h2['anch_src']), AnchFullB=f2(h2['anch_full']),
                         ReplaySizeB=f2(h2['replay_size']), PriceB=f2(abs(h2['price'])), PriceSignedB=f'{h2["price"]:+.2f}').items():
            macro(stem+k, v)
        if h['sclip']:
            macro(stem+'SclipSrc', f1(h['sclip']['mean_size'][0])); macro(stem+'SclipFull', f1(h['sclip']['mean_size'][-1])); macro(stem+'SclipRisk', pc(h['sclip']['mean_risk']))


def silent_failure():
    """Set size of the reused native threshold against the size needed, 15 combinations (results/silent_failure,
    src/exp_silent_failure.py): the label-free signal of the failure."""
    s = load('results/silent_failure')['summary']
    macro('SilentNUnder', str(s['n_under'])); macro('SilentN', str(s['n']))
    macro('SilentShareLo', pc(s['share_lo'], 0)); macro('SilentShareHi', pc(s['share_hi'], 0))
    macro('SilentGrowthReusedLo', f2(s['growth_reused_lo'])); macro('SilentGrowthReusedHi', f2(s['growth_reused_hi']))
    macro('SilentGrowthAnchLo', f2(s['growth_anchored_lo'])); macro('SilentGrowthAnchHi', f2(s['growth_anchored_hi']))
    assert s['anchored_grows_more']


def claude_baseline():
    """General multimodal model on marked ADE20K pixels (results/claude_baseline_ade, src/exp_claude_baseline.py):
    verbalised probabilities of Claude Opus 5.5 at 150 and 845 names, CRC on them, and CAT-Seg ViT-L on the same pixels."""
    j = load('results/claude_baseline_ade'); c = json.loads(Path('results/claude_baseline_ade/crc.json').read_text())
    b = j['by_vocab']; arms = c['arms']
    macro('ClaudeImages', num(j['images'])); macro('ClaudeMarkers', num(c['markers'])); macro('ClaudeSplits', num(c['splits']))
    macro('ClaudeCostImage', f'{j["cost_per_image_usd"]:.3f}')
    macro('ClaudeTopOneSrc', pc(b['150']['top1'])); macro('ClaudeTopOneFull', pc(b['845']['top1']))
    macro('ClaudeUnlistedSrc', pc(1-b['150']['listed'])); macro('ClaudeUnlistedFull', pc(1-b['845']['listed']))
    macro('ClaudeProbChanged', pc(j['paired']['true_prob_changed'], 0)); macro('ClaudeTopChanged', pc(1-j['paired']['top1_unchanged'], 0))
    assert 1-b['150']['listed'] > c['alpha'] and 1-b['845']['listed'] > c['alpha']      # why CRC falls to the all-label endpoint
    for mode in ('reused', 'recalibrated'):
        assert arms['claude'][mode]['mean_size'] == 845 and arms['claude'][mode]['mean_risk'] == 0
    macro('ClaudeCrcSize', num(round(arms['claude']['reused']['mean_size'])))
    macro('ClaudeCatReusedRisk', pc(arms['catseg_native']['reused']['mean_risk'])); macro('ClaudeCatRecalSize', f2(arms['catseg_native']['recalibrated']['mean_size']))
    macro('ClaudeCatAnchRisk', pc(arms['catseg_anchored']['reused']['mean_risk'])); macro('ClaudeCatAnchSize', f2(arms['catseg_anchored']['reused']['mean_size']))


def repeated_recal():
    """Simultaneous calibration-conditional guarantee over K recalibrations (results/repeated_recal, src/exp_repeated_recal.py):
    native at delta/K against anchored at delta, RCPS Hoeffding-Bentkus; Rr<model><dataset>{Cross,AnchSize,NatOne,NatHundred}."""
    j = load('results/repeated_recal')
    stems = {'vitl_bank683': 'VitL', 'sed_bank683': 'Sed', 'fcclip_bank683': 'Fc'}; dss = {'ade': 'Ade', 'pascal': 'Pas', 'coco': 'Coc'}
    macro('RrDelta', pc(j['delta'], 0)); macro('RrKMax', num(max(j['ks'])))
    for r in j['configs'].values():
        p = 'Rr' + stems[r['tag']] + dss[r['dataset']]
        macro(p+'Cross', num(r['crossover_k']) if r['crossover_k'] else '--')
        macro(p+'AnchSize', f2(r['anchored_rcps']['mean_size'])); macro(p+'AnchRisk', pc(r['anchored_rcps']['mean_risk']))
        macro(p+'NatOne', f2(r['native_rcps']['1']['mean_size'])); macro(p+'NatHundred', f2(r['native_rcps']['100']['mean_size']))
        macro(p+'NatThousand', f2(r['native_rcps']['1000']['mean_size'])); macro(p+'CrcNat', f2(r['crc']['native_recal']['mean_size']))


def table_curve():
    """Set size at every nested addition (Fig. 3 companion) for the headline configurations."""
    rows = [r'\begin{tabular}{@{}lrrrrr@{}}', r'\toprule', r'Configuration & +0 & +50 & +150 & +500 & +695 \\', r'\midrule']
    for key in ['vitb', 'vitb683', 'vitl', 'vitl683', 'declip683', 'sed', 'sed683', 'fcclip', 'fcclip683']:
        a = arms(headroom(key))['catseg_anchored']
        rows.append(f'{CONFIGS[key][4]} & ' + ' & '.join(f2(s) for s in a['mean_size']) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'curve.tex').write_text('\n'.join(rows)+'\n')


def table_bank():
    """Bank ablation on two datasets: ADE20K 150->845 (400 validation images, ViT-B) and COCO-Stuff 171->866 (500 val2017 images,
    ViT-B and ViT-L; exp_bank_select_coco.py, exp_bank_unrelated_coco.py). The unrelated banks (abstract WordNet nouns,
    pronounceable non-words) were run on COCO-Stuff only; the Pascal banks on ADE20K only."""
    NAMES = {'candidate_only': 'none (candidate only)', 'coco20': 'COCO-20', 'coco85': 'COCO-85', 'coco171': 'COCO-171', 'pascal171': 'Pascal-171',
             'coco_pascal255': 'COCO + Pascal 255', 'coco_oi255': 'COCO + OI 255', 'coco_pascal342': 'COCO + Pascal 342', 'coco_oi342': 'COCO + OI 342',
             'coco_oi683': 'COCO + OI 683', 'coco_oi1366': 'COCO + OI 1,366', 'coco_oi2731': 'COCO + OI 2,731', 'coco_oi5462': 'COCO + OI 5,462', 'oi683': 'OI 683, no COCO names',
             'abstract683': 'abstract nouns 683', 'pseudo683': 'non-words 683', 'coco_abstract683': 'COCO + abstract 683', 'coco_pseudo683': 'COCO + non-words 683'}
    UNRELATED = ['abstract683', 'pseudo683', 'coco_abstract683', 'coco_pseudo683']
    entries = {}
    for d in ['results/anchor_bank_ade', 'results/anchor_bank_large_ade', 'results/anchor_bank_huge_ade']:
        j = load(d) or {}
        for k, v in j.items():
            if k.endswith('_'+ALPHA): entries[k[:-len(ALPHA)-1]] = v
    coco_b, coco_u, coco_l = (load(d)['alphas']['0.1'] for d in ['results/bank_select_coco', 'results/bank_unrelated_coco', 'results/bank_select_coco_vitl'])
    for k in ['native_grown', 'coco171', 'coco_oi683', 'oi683']:      # the unrelated run (local GPU) repeats these arms of the GH200 run: same images and splits, float drift only
        assert abs(coco_u['rows'][k]['size_grown']-coco_b['rows'][k]['size_grown']) < 1e-4, k
    cb = {**coco_b['rows'], **coco_u['rows']}; cl = coco_l['rows']
    dash = '--'
    rows = [r'\begin{tabular}{@{}lrrrrrrr@{}}', r'\toprule',
            r' & & \multicolumn{3}{c}{ADE20K, ViT-B} & \multicolumn{3}{c}{COCO-Stuff} \\',
            r'\cmidrule(lr){3-5}\cmidrule(l){6-8}',
            r'Reference bank & names & size & risk & top-10 & ViT-B size & ViT-B risk & ViT-L size \\', r'\midrule']
    def row(k, n):
        a, b, l = entries.get(k), cb.get(k), cl.get(k)
        return (f'{NAMES.get(k, k)} & {num(n)} & ' + (f'{f2(a["mean_size"][-1])} & {pc(a["mean_risk"])} & {pc(a["expanded_top10"])}' if a else f'{dash} & {dash} & {dash}')
                + ' & ' + (f'{f2(b["size_grown"])} & {pc(b["risk"])}' if b else f'{dash} & {dash}') + ' & ' + (f2(l['size_grown']) if l else dash) + r' \\')
    nb, nl = cb['native_grown'], cl['native_grown']
    rows.append(f'native, recalibrated & {dash} & {dash} & {dash} & {dash} & {f2(nb["size_grown"])} & {pc(nb["risk"])} & {f2(nl["size_grown"])} \\\\')
    rows.append(r'\midrule')
    related = {**{k: v['bank_size'] for k, v in entries.items()}, **{k: v['bank_size'] for k, v in cb.items() if k != 'native_grown' and k not in UNRELATED}}
    head = rows[:]
    for k in sorted(related, key=lambda k: (related[k], k)):
        rows.append(row(k, related[k]))
    rows.append(r'\midrule')
    for k in UNRELATED:
        rows.append(row(k, cb[k]['bank_size']))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'bank.tex').write_text('\n'.join(rows)+'\n')      # supplement: the full sweep
    # main text: the bank sizes and compositions the text discusses
    # sizes only, so that it fits one column at full type size; the risk of every row is one range in the caption
    SHORT = {'candidate_only': 'none', 'oi683': 'OI 683, no COCO'}
    MAIN_BANKS = ['candidate_only', 'coco20', 'coco171', 'coco_oi683', 'coco_oi5462', 'oi683', 'pseudo683']
    rows = [r'\begin{tabular}{@{}lrrrr@{}}', r'\toprule',
            r' & \multicolumn{2}{c}{ADE20K, ViT-B} & \multicolumn{2}{c}{COCO-Stuff size} \\',
            r'\cmidrule(lr){2-3}\cmidrule(l){4-5}',
            r'Reference bank & size & top-10 & ViT-B & ViT-L \\', r'\midrule',
            f'native, recalibrated & {dash} & {dash} & {f2(nb["size_grown"])} & {f2(nl["size_grown"])} \\\\', r'\midrule']
    main_risks = [nb['risk'], nl['risk']]
    for k in MAIN_BANKS:
        a, b, l = entries.get(k), cb.get(k), cl.get(k)
        main_risks += [x['risk'] for x in (b, l) if x] + ([a['mean_risk']] if a else [])
        rows.append(f'{SHORT.get(k, NAMES.get(k, k))} & ' + (f'{f2(a["mean_size"][-1])} & {pc(a["expanded_top10"])}' if a else f'{dash} & {dash}')
                    + ' & ' + (f2(b['size_grown']) if b else dash) + ' & ' + (f2(l['size_grown']) if l else dash) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'bank_main.tex').write_text('\n'.join(rows)+'\n')
    macro('BankMainRiskMin', pc(min(main_risks))); macro('BankMainRiskMax', pc(max(main_risks)))
    for k, v in entries.items():
        macro('Bank'+re.sub(r'[^A-Za-z]', '', k.title())+size_word(v['bank_size'])+'Size', f2(v['mean_size'][-1]))
    macro('BankSweepImages', num(load('results/anchor_bank_ade')['coco171_'+ALPHA].get('images', 400)) if 'images' in load('results/anchor_bank_ade')['coco171_'+ALPHA] else '400')
    # COCO-Stuff: the bank chosen there, and what that choice would cost on ADE20K
    macro('BankCocoImages', num(load('results/bank_select_coco')['images']))
    selb, sell = coco_b['smallest_grown_set'], coco_l['smallest_grown_set']
    macro('BankCocoSelB', num(cb[selb]['bank_size'])); macro('BankCocoSelL', num(cl[sell]['bank_size']))
    macro('BankCocoSelBSize', f2(cb[selb]['size_grown'])); macro('BankCocoSelLSize', f2(cl[sell]['size_grown']))
    macro('BankCocoNativeB', f2(nb['size_grown'])); macro('BankCocoNativeL', f2(nl['size_grown']))
    macro('BankCocoDefaultB', f2(cb['coco_oi683']['size_grown'])); macro('BankCocoDefaultL', f2(cl['coco_oi683']['size_grown']))
    macro('BankCocoRegretB', f2(cb['coco_oi683']['size_grown']-cb[selb]['size_grown'])); macro('BankCocoRegretL', f2(cl['coco_oi683']['size_grown']-cl[sell]['size_grown']))
    macro('BankAdeCostOfCocoSel', f1(entries[selb]['mean_size'][-1]-entries['coco_oi683']['mean_size'][-1]))
    risks = [cb[k]['risk'] for k in cb] + [cl[k]['risk'] for k in cl]
    macro('BankCocoRiskMin', pc(min(risks), 2)); macro('BankCocoRiskMax', pc(max(risks), 2))
    for k, stem in [('abstract683', 'Abstract'), ('pseudo683', 'Pseudo'), ('coco_abstract683', 'CoreAbstract'), ('coco_pseudo683', 'CorePseudo'),
                    ('oi683', 'OiOnly'), ('coco171', 'Core')]:
        macro('BankUnrel'+stem+'Size', f2(cb[k]['size_grown']))


BANK_SEEDS = [('sed', 'SED', 'Sed'), ('vitl', 'CAT-Seg ViT-L', 'VitL')]


def table_bank_seeds():
    """Supplement: the 512 Open Images names of the 683-name bank redrawn five times, COCO-171 kept (exp_bank_seeds.py), on
    the images and splits of the bank sweep: tables/bank_seeds.tex and \\BankSeeds* macros. The text says "five" redraws,
    "every draw meets the target at both levels" and "less than its standard deviation over splits"; each is asserted here."""
    J = {m: load(f'results/bank_seeds_ade_{m}') for m, _, _ in BANK_SEEDS}
    if any(v is None for v in J.values()): return
    seeds = J['sed']['seeds']; draws = ['published'] + [f'seed{s}' for s in seeds]
    assert len(seeds) == 5 and all(j['seeds'] == seeds for j in J.values())
    assert all(num(j['images']) == macros['BankSweepImages'] and j['splits'] == J['sed']['splits'] for j in J.values())
    A = lambda m, al: J[m]['alphas'][al]
    def line(name, risk, size, size_b, d=2):
        return name + ' & ' + ' & '.join(f'{pc(risk(m), d)} & {f2(size(m))} & {f2(size_b(m))}' for m, _, _ in BANK_SEEDS) + r' \\'
    rows = [r'\begin{tabular}{@{}l' + 'rrr'*len(BANK_SEEDS) + '@{}}', r'\toprule',
            '& ' + ' & '.join(rf'\multicolumn{{3}}{{c}}{{{n}}}' for _, n, _ in BANK_SEEDS) + r' \\', r'\cmidrule(lr){2-4}\cmidrule(l){5-7}',
            'Open Images names' + r' & risk & size & size, $5\%$' * len(BANK_SEEDS) + r' \\', r'\midrule',
            line('native, recalibrated', lambda m: A(m, '0.1')['native']['recalibrated_risk'], lambda m: A(m, '0.1')['native']['recalibrated_size'],
                 lambda m: A(m, '0.05')['native']['recalibrated_size']), r'\midrule']
    for i, k in enumerate(draws):
        rows.append(line('draw of the paper' if k == 'published' else f'redraw {i}', lambda m: A(m, '0.1')['rows'][k]['risk'],
                         lambda m: A(m, '0.1')['rows'][k]['size'][-1], lambda m: A(m, '0.05')['rows'][k]['size'][-1]))
    rows.append(r'\midrule')
    for stat, name in [('mean', 'mean of the redraws'), ('sd', 's.d.\\ of the redraws')]:
        rows.append(line(name, lambda m: A(m, '0.1')['redraw_summary']['risk'][stat], lambda m: A(m, '0.1')['redraw_summary']['size_grown'][stat],
                         lambda m: A(m, '0.05')['redraw_summary']['size_grown'][stat]))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'bank_seeds.tex').write_text('\n'.join(rows)+'\n')
    macro('BankSeedsSplits', num(J['sed']['splits']))
    spread, overhead, top1, shared = [], [], [], []
    for al, suf in [('0.1', ''), ('0.05', 'B')]:
        risks = [A(m, al)['rows'][k]['risk'] for m, _, _ in BANK_SEEDS for k in draws]
        assert max(risks) < float(al), al                                                   # every draw meets the target
        macro('BankSeedsRiskLo'+suf, pc(min(risks), 2)); macro('BankSeedsRiskHi'+suf, pc(max(risks), 2))
    for m, _, stem in BANK_SEEDS:
        a = A(m, '0.1'); r = a['rows']; sizes = [r[k]['size'][-1] for k in draws]
        sd, split_sd = a['redraw_summary']['size_grown']['sd'], r['published']['size_split_sd']
        assert sd < split_sd, m
        macro('BankSeedsSizeSd'+stem, f2(sd)); macro('BankSeedsSplitSd'+stem, f2(split_sd))
        spread.append(max(sizes)-min(sizes)); overhead += [r[k]['overhead'] for k in draws]
        top1 += [abs(r[k]['top1_at_845']-r['published']['top1_at_845']) for k in draws]
        shared += [r[k]['open_images_names_shared_with_published'] for k in draws[1:]]
        gap = J[m]['published_draw_against_stored_scores']
        assert gap['max_abs_logit_difference'] == 0 and gap['fraction_of_entries_that_differ'] == 0, m   # the paper's draw rescored equals the stored scores
    macro('BankSeedsSizeSpread', f2(max(spread)))                 # largest difference between two of the six draws, either model
    macro('BankSeedsOverheadLo', f2(min(overhead))); macro('BankSeedsOverheadHi', f2(max(overhead)))
    macro('BankSeedsTopOneMaxChange', pc(max(top1)))
    macro('BankSeedsSharedLo', str(min(shared))); macro('BankSeedsSharedHi', str(max(shared)))


def table_added():
    table_added_keys(['vitb', 'vitb683', 'vitl', 'vitl683', 'declip683', 'sed', 'sedfast', 'sed683', 'fcclip', 'fcclip683', 'fcclip1366', 'fcclip2731', 'ft10k', 'distract'], 'added.tex')
    table_added_keys(PASCAL, 'added_pascal.tex')     # supplement: added-label risk on Pascal Context (459-label annotations)
    table_added_keys(COCO, 'added_coco.tex')         # supplement: added-label risk on COCO (LVIS annotations)
    # oracle (calibrated on all 845 labels' annotations) added-label risk, range over every ADE20K configuration and both arms
    oracle = [d[arm]['risk_added'] for k in ['vitb', 'vitb683', 'vitl', 'vitl683', 'declip683', 'sed', 'sedfast', 'sed683', 'fcclip', 'fcclip683', 'fcclip1366', 'fcclip2731', 'ft10k', 'distract']
              for j in [load(f'results/added_label_risk_{CONFIGS[k][3]}')] if j is not None for d in [j['designs'][ALPHA]]
              for arm in ['anchored_calibrated_on_all845', 'native_calibrated_on_all845']]
    if oracle: macro('AddedOracleMin', pc(min(oracle))); macro('AddedOracleMax', pc(max(oracle)))


def table_added_keys(keys, filename):
    rows = [r'\begin{tabular}{@{}lrrrr@{}}', r'\toprule',
            r'Configuration & anchored & native, recalibrated & native at anchored size & native, reused \\', r'\midrule']
    for key in keys:
        j = load(f'results/added_label_risk_{CONFIGS[key][3]}') if CONFIGS[key][3] else None
        if j is None: continue
        d = j['designs'][ALPHA]; a, r, m, f = d['anchored_frozen'], d['native_replay'], d['native_at_anchored_frozen_size'], d['native_frozen']
        rows.append(f'{CONFIGS[key][4]} & {pc(a["risk_added"])} / {f1(a["size_845"])} & {pc(r["risk_added"])} / {f1(r["size_845"])} & '
                    f'{pc(m["risk_added"])} / {f1(m["size_845"])} & {pc(f["risk_added"])} / {f1(f["size_845"])} \\\\')
        stem = CONFIGS[key][5]
        for k, v in dict(AddedAnch=pc(a['risk_added']), AddedReplay=pc(r['risk_added']), AddedMatched=pc(m['risk_added']), AddedFrozen=pc(f['risk_added']),
                         AddedGapMatched=f1(100*(m['risk_added']-a['risk_added'])), MatchedSourceRisk=pc(m['risk_source']), AnchSourceRisk=pc(a['risk_source'], 2)).items():
            macro(stem+k, v)
        if key == 'vitb':
            macro('AddedPixelFraction', pc(j['pixel_fraction']['added'])); macro('AddedImages', num(j['images_with_added_pixels']))
            b = d['anchored_calibrated_on_all845']; n = d['native_calibrated_on_all845']
            macro('AddedOracleAnch', pc(b['risk_added'])); macro('AddedOracleNative', pc(n['risk_added']))
        if key == 'pascal':
            macro('PascalAddedPixelFraction', pc(j['pixel_fraction']['added'])); macro('PascalAddedImages', num(j['images_with_added_pixels']))
        if key in COCO:                               # same images and annotations for every COCO configuration
            macro('CocoAddedPixelFraction', pc(j['pixel_fraction']['added'])); macro('CocoAddedImages', num(j['images_with_added_pixels']))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')


def table_confirm():
    j = load('results/confirmation_ade_vitl_bank683'); rows = [r'\begin{tabular}{@{}lrrrrr@{}}', r'\toprule',
                                                               r'& & \multicolumn{2}{c}{risk} & \multicolumn{2}{c}{size} \\', r'\cmidrule(lr){3-4}\cmidrule(lr){5-6}',
                                                               r'Design & $\alpha$ & native reused & anchored & anchored & native recal. \\', r'\midrule']
    for design, dname in [('primary', 'pre-declared split'), ('secondary', f'{500} random splits')]:
        for alpha, an in [(ALPHA, '.10'), (ALPHA2, '.05')]:
            d = j['designs'][f'{design}_{alpha}']; a, f, r = d['anchored'], d['native_frozen_full'], d['native_replay_full']
            rows.append(f'{dname} & {an} & {pc(f["mean_risk"])} & {pc(a["mean_risk"])} & {f2(a["mean_size"][0])}$\\to${f2(a["mean_size"][-1])} & {f2(r["mean_size"][0])} \\\\')
            stem = 'Conf'+design.title()+('B' if alpha == ALPHA2 else '')
            for k, v in dict(NativeFrozenRisk=pc(f['mean_risk']), AnchRisk=pc(a['mean_risk']), AnchSrc=f2(a['mean_size'][0]), AnchFull=f2(a['mean_size'][-1]),
                             ReplaySize=f2(r['mean_size'][0]), ReplayRisk=pc(r['mean_risk']), Price=f2(a['mean_size'][-1]-r['mean_size'][0]), AnchFrac=pc(a['frac_above'], 0)).items():
                macro(stem+k, v)
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'confirm.tex').write_text('\n'.join(rows)+'\n'); macro('ConfImages', num(j['images']))


def rb(prefix, key):
    c = CONFIGS[key][2]
    if c is None: return None
    for p in sorted(Path('results').glob(f'{prefix}_*/results.json')):
        j = json.loads(p.read_text())
        if (j['dataset'], j['config']) == c and j['splits'] >= 100: return j
    return None


def table_strata():
    table_strata_keys(MAIN, 'strata.tex')
    table_strata_keys(PASCAL, 'strata_pascal.tex', scenes=False)   # supplement (no scene labels on Pascal Context)
    table_strata_keys(COCO, 'strata_coco.tex', scenes=False)       # supplement (no scene labels on COCO-Stuff)


def table_strata_keys(keys, filename, scenes=True):
    """scenes=False (Pascal Context, COCO-Stuff: no scene labels) drops the worst-scene columns."""
    rows = [r'\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
            r'& \multicolumn{3}{c}{class-averaged risk} & \multicolumn{3}{c}{worst ADE scene} \\', r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}',
            r'Configuration & native reused & native recal. & anchored & native reused & native recal. & anchored \\', r'\midrule'] if scenes else \
           [r'\begin{tabular}{@{}lrrr@{}}', r'\toprule', r'& \multicolumn{3}{c}{class-averaged risk} \\', r'\cmidrule(l){2-4}',
            r'Configuration & native reused & native recal. & anchored \\', r'\midrule']
    for key in keys:
        j = rb('conditional_risk', key)
        if j is None: continue
        d = j['designs'][ALPHA]; f, r, a = d['native_frozen'], d['native_replay'], d['anchored_frozen']
        ws = lambda x: ('--' if x.get('worst_scene') is None or x['worst_scene'] != x['worst_scene'] else pc(x['worst_scene']))
        rows.append(f'{CONFIGS[key][4]} & {pc(f["macro"])} & {pc(r["macro"])} & {pc(a["macro"])}' + (f' & {ws(f)} & {ws(r)} & {ws(a)}' if scenes else '') + r' \\')
        stem = CONFIGS[key][5]
        for k, v in dict(MacroFrozen=pc(f['macro']), MacroReplay=pc(r['macro']), MacroAnch=pc(a['macro']), RareReplay=pc(r['thirds'][2]), RareAnch=pc(a['thirds'][2]),
                         RareFrozen=pc(f['thirds'][2]), TailReplay=pc(r['images_over_25']), TailAnch=pc(a['images_over_25']), QninetyReplay=pc(r['image_loss_q90']), QninetyAnch=pc(a['image_loss_q90'])).items():
            macro(stem+k, v)
        if a.get('worst_scene') is not None and a['worst_scene'] == a['worst_scene']:
            macro(stem+'WorstSceneAnch', pc(a['worst_scene'])); macro(stem+'WorstSceneReplay', pc(r['worst_scene'])); macro(stem+'WorstSceneName', a['worst_scenes'][0][0].replace('_', ' '))
            macro(stem+'ScenesOverTwoAlpha', a['scenes_over_2alpha'])
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')


LOSS_NAMES = {'fnr': 'pixel miss (headline)', 'fnr_gt_0.25': r'$\ind[\text{miss} > 25\%]$', 'fnr_gt_0.10': r'$\ind[\text{miss} > 10\%]$', 'class_balanced': 'class-balanced', 'worst_class': 'worst class in image'}


def table_losses():
    rows = [r'\begin{tabular}{@{}llrrrr@{}}', r'\toprule',
            r'Configuration & loss & native reused risk & native recal.\ size & anchored risk & anchored size \\', r'\midrule']
    lo_a, hi_a = 1, 0
    for key in MAIN+PASCAL+[k for k in COCO if k not in MAIN]:
        j = rb('alternative_losses', key)
        if j is None: continue
        first = True
        for loss in j['losses']:
            d = j['designs'][ALPHA][loss]; f, r, a = d['native_frozen'], d['native_replay'], d['anchored_frozen']
            rows.append(f'{CONFIGS[key][4] if first else ""} & {LOSS_NAMES[loss]} & {pc(f["mean_risk"])} & {f1(r["mean_size"])} & {pc(a["mean_risk"])} & {f1(a["mean_size"])} \\\\'); first = False
            lo_a, hi_a = min(lo_a, a['mean_risk']), max(hi_a, a['mean_risk'])
            stem = CONFIGS[key][5]+'Loss'+re.sub(r'[^A-Za-z]', '', loss.title())
            macro(stem+'AnchSize', f1(a['mean_size'])); macro(stem+'ReplaySize', f1(r['mean_size'])); macro(stem+'AnchRisk', pc(a['mean_risk'], 2)); macro(stem+'FrozenRisk', pc(f['mean_risk']))
        rows.append(r'\midrule')
    rows[-1] = r'\bottomrule'; rows.append(r'\end{tabular}')
    (TAB/'losses.tex').write_text('\n'.join(rows)+'\n'); write_parts('losses', rows, 4, 2); macro('LossAnchRiskLo', pc(lo_a, 2)); macro('LossAnchRiskHi', pc(hi_a, 2))


def write_parts(name, rows, head, k=2):
    """A long supplement table also as k parts (name_a, name_b, ...), split at the group boundaries nearest the k-quantiles
    of its rows, each with the header, so that every part prints at full size instead of being shrunk to one page."""
    body = rows[head:-2]; mids = [i for i, r in enumerate(body) if r == r'\midrule']
    cuts = [min(mids, key=lambda i: abs(i - q*len(body)/k)) for q in range(1, k)]
    for part, (lo, hi) in zip('abcdef', zip([0]+[c+1 for c in cuts], cuts+[len(body)])):
        (TAB/f'{name}_{part}.tex').write_text('\n'.join(rows[:head] + body[lo:hi] + rows[-2:])+'\n')


CONS_NAMES = dict(logit='per-label threshold (ours)', softmax='softmax cutoff', aps='APS', raps='RAPS')


def table_constructions():
    rows = [r'\begin{tabular}{@{}llrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{native} & \multicolumn{3}{c}{anchored} \\', r'\cmidrule(lr){3-4}\cmidrule(lr){5-7}',
            r'Configuration & construction & reused risk & recal.\ size & reused risk & reused size & recal.\ size \\', r'\midrule']
    soft_lo, soft_hi, raps_lo, raps_hi, aps_lo, aps_hi = 1, 0, 1, 0, 1, 0
    for key in MAIN+PASCAL+[k for k in COCO if k not in MAIN]:
        j = rb('set_constructions', key)
        if j is None: continue
        first = True
        for c in j['constructions']:
            d = j['designs'][ALPHA][c]; f, r, a, b = d['native_frozen'], d['native_replay'], d['anchored_frozen'], d['anchored_replay']
            rows.append(f'{CONFIGS[key][4] if first else ""} & {CONS_NAMES[c]} & {pc(f["mean_risk"])} & {f2(r["mean_size"])} & {pc(a["mean_risk"])} & {f2(a["mean_size"])} & {f2(b["mean_size"])} \\\\'); first = False
            stem = CONFIGS[key][5]+'Cons'+c.title()
            macro(stem+'AnchRisk', pc(a['mean_risk'])); macro(stem+'AnchSize', f2(a['mean_size'])); macro(stem+'AnchReplaySize', f2(b['mean_size'])); macro(stem+'AnchFrac', pc(a['frac_splits_above_alpha'], 0))
            if c == 'softmax': soft_lo, soft_hi = min(soft_lo, a['mean_risk']), max(soft_hi, a['mean_risk'])
            if c == 'raps': raps_lo, raps_hi = min(raps_lo, a['mean_risk']), max(raps_hi, a['mean_risk'])
            if c == 'aps': aps_lo, aps_hi = min(aps_lo, a['mean_risk']), max(aps_hi, a['mean_risk'])
            d5 = j['designs'][ALPHA2][c]['anchored_frozen']; macro(stem+'AnchRiskB', pc(d5['mean_risk']))
        u = j.get('uncalibrated', {}).get(ALPHA) or j.get('uncalibrated') or {}
        rows.append(r'\midrule')
    rows[-1] = r'\bottomrule'; rows.append(r'\end{tabular}')
    (TAB/'constructions.tex').write_text('\n'.join(rows)+'\n'); write_parts('constructions', rows, 6, 2)
    macro('SoftmaxAnchRiskLo', pc(soft_lo)); macro('SoftmaxAnchRiskHi', pc(soft_hi)); macro('RapsAnchRiskLo', pc(raps_lo)); macro('RapsAnchRiskHi', pc(raps_hi))
    macro('ApsAnchRiskLo', pc(aps_lo)); macro('ApsAnchRiskHi', pc(aps_hi))


def table_calsize():
    keys = ['vitb', 'vitl683', 'declip683', 'sed683', 'fcclip683'] + PASCAL + COCO
    js = {k: rb('calibration_size', k) for k in keys}; js = {k: v for k, v in js.items() if v}
    ns = next(iter(js.values()))['n_cal']
    rows = [r'\begin{tabular}{@{}l' + 'r'*len(ns) + '@{}}', r'\toprule', r'Configuration / arm & ' + ' & '.join(f'$n={n}$' for n in ns) + r' \\', r'\midrule']
    for k, j in js.items():
        for arm, an in [('native_replay', 'native recal.'), ('anchored_frozen', 'anchored')]:
            cells = [j['designs'][ALPHA][str(n)][arm] for n in ns]
            rows.append(f'{CONFIGS[k][4]}, {an} & ' + ' & '.join(f'{pc(c["mean_risk"])} / {f1(c["mean_size"])}' for c in cells) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'calsize.tex').write_text('\n'.join(rows)+'\n')
    for n in ns:
        for k in js:
            d = js[k]['designs'][ALPHA][str(n)]
            macro(f'{CONFIGS[k][5]}Cal{n_word(n)}AnchRisk', pc(d['anchored_frozen']['mean_risk'])); macro(f'{CONFIGS[k][5]}Cal{n_word(n)}ReplayRisk', pc(d['native_replay']['mean_risk']))
            macro(f'{CONFIGS[k][5]}Cal{n_word(n)}AnchSize', f1(d['anchored_frozen']['mean_size'])); macro(f'{CONFIGS[k][5]}Cal{n_word(n)}ReplaySize', f1(d['native_replay']['mean_size']))
            macro(f'{CONFIGS[k][5]}Cal{n_word(n)}AnchSd', pc(d['anchored_frozen']['risk_sd'])); macro(f'{CONFIGS[k][5]}Cal{n_word(n)}ReplaySd', pc(d['native_replay']['risk_sd']))
    macro('CalSizeMaxN', num(ns[-1]))
    # smallest n from which the overhead (anchored minus recalibrated native size) stays within 0.2 labels of its value at the largest n
    for k in js:
        d = js[k]['designs'][ALPHA]; ov = [d[str(n)]['anchored_frozen']['mean_size']-d[str(n)]['native_replay']['mean_size'] for n in ns]
        settle = next(n for i, n in enumerate(ns) if all(abs(o-ov[-1]) <= 0.2 for o in ov[i:]))
        macro(f'{CONFIGS[k][5]}CalSettleN', num(settle))


def n_word(n): return {10: 'Ten', 20: 'Twenty', 50: 'Fifty', 100: 'Hundred', 200: 'TwoHundred', 400: 'FourHundred'}.get(n, 'Max')


def size_word(n):
    """Bank sizes as macro-safe words (macro names must be letters only)."""
    return ''.join({'0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'}[c] for c in str(n))


def table_fcclip_banks():
    rows = [r'\begin{tabular}{@{}rrrrr@{}}', r'\toprule', r'bank names & anchored & native recal. & overhead & added risk \\', r'\midrule']
    for key, n in [('fcclip', 133), ('fcclip683', 701), ('fcclip1366', 1366), ('fcclip2731', 2731)]:
        h = headline_row(key); j = load(f'results/added_label_risk_{CONFIGS[key][3]}'); d = j['designs'][ALPHA]
        rows.append(f'{num(n)} & {f2(h["anch_full"])} & {f2(h["replay_size"])} & {f2(h["price"])} & {pc(d["anchored_frozen"]["risk_added"])} / {pc(d["native_at_anchored_frozen_size"]["risk_added"])} \\\\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'fcclip_banks.tex').write_text('\n'.join(rows)+'\n')


def table_finetune():
    rows = [r'\begin{tabular}{@{}lrrrr@{}}', r'\toprule', r'Aggregator & anchored size at +695 & native recal.\ size & held-out top-10 & added-label risk at matched size (anchored / native) \\', r'\midrule']
    for key, ho in [('vitb', None), ('ft10k', None), ('distract', None)]:
        h = headline_row(key); j = load(f'results/added_label_risk_{CONFIGS[key][3]}'); d = j['designs'][ALPHA]
        rows.append(f'{CONFIGS[key][4]} & {f2(h["anch_full"])} & {f2(h["replay_size"])} & \\heldout{key} & {pc(d["anchored_frozen"]["risk_added"])} / {pc(d["native_at_anchored_frozen_size"]["risk_added"])} \\\\')
    rows += [r'\bottomrule', r'\end{tabular}']
    # held-out top-10 at +695: 'held_out' group (30 ADE20K source labels held out in the SCLIP pilot; 7 are COCO-Stuff names) of the
    # 400-image headroom probe, column 5 of 'mean' ('+695 top10' in the REPORT.md)
    ho = {}
    for key, run in [('vitb', 'results/headroom_probe_ade'), ('ft10k', 'results/headroom_probe_ade_ft10k'), ('distract', 'results/headroom_probe_ade_anchored_vitb_distract_near')]:
        jr = load(run)
        if jr is None: continue
        r = next(x for x in jr['rows'] if x['arm'] == 'catseg_anchored' and x['group'] == 'held_out')
        ho[key] = pc(r['mean'][5]); macro(CONFIGS[key][5]+'HeldTopTen', ho[key])
    pp = Path('results/headroom_probe_ade/protocol.json')
    if pp.exists(): macro('FtProbeImages', num(len(json.loads(pp.read_text())['image_ids'])))
    ph = Path('results/match_correction_sclip_ade/protocol.json')
    if ph.exists(): macro('FtHeldLabels', num(len(json.loads(ph.read_text())['held_out_ids'])))
    (TAB/'finetune.tex').write_text('\n'.join(rows).replace('\\heldoutvitb', ho.get('vitb', '--')).replace('\\heldoutft10k', ho.get('ft10k', '--')).replace('\\heldoutdistract', ho.get('distract', '--'))+'\n')


def bank_overlap():
    """Exact-name overlap between the evaluated ADE20K vocabulary and the 683-name bank (the COCO core is not filtered)."""
    names = [r['prompt'] for r in json.loads(Path('meta/natural_vocab_v1.json').read_text())['rows']]
    bank = set(json.loads(Path('meta/bank_coco_oi683_v1.json').read_text())['names'])
    macro('BankOverlapSource', sum(n in bank for n in names[:150])); macro('BankOverlapAll', sum(n in bank for n in names))
    # the Open Images part was filtered against ADE20K and Pascal Context only; count its exact matches with COCO-Stuff->LVIS added labels
    oi = json.loads(Path('meta/bank_coco_oi683_v1.json').read_text())['names'][171:]
    added = {r['prompt'] for r in json.loads(Path('meta/coco_lvis_natural_vocab_v1.json').read_text())['rows'] if r['role'] == 'added'}
    macro('BankOverlapOiCocoAdded', sum(n in added for n in oi))


def qualitative():
    """Figs. problem and qualitative (src/fig_qualitative.py): one selected ADE20K image, CAT-Seg ViT-L, thresholds of the median split."""
    p, q = Path('results/qualitative_ade/summary.json'), Path('results/qualitative_ade/selection.json')
    if not (p.exists() and q.exists()): return
    s, pool = json.loads(p.read_text()), json.loads(q.read_text())['pool']
    for key, name in [('native_source', 'Source'), ('native_reused', 'Reused'), ('native_recal', 'Recal'), ('anchored', 'Anch')]:
        macro(f'Qual{name}Miss', pc(s['panels'][key]['miss_fraction']))
        macro(f'Qual{name}Size', f1(s['panels'][key]['mean_set_size_source_pixels']))
        macro(f'QualPool{name}Miss', pc(pool['mean_sampled_miss_over_pool'][key]))
    macro('QualPoolImages', num(pool['also_in_probe_evaluation_roles'])); macro('QualPoolWorse', pc(pool['reused_worse_than_both_others'], 0))
    r = Path('results/qualitative_ade/panel.json')
    if r.exists():
        pn = json.loads(r.read_text())
        macro('QualPanelImages', num(pn['n'])); macro('QualPanelPool', num(pn['pool_size']))
        for key, name in [('native_reused', 'Reused'), ('native_recal', 'Recal'), ('anchored', 'Anch')]:
            macro(f'QualPanel{name}Miss', pc(pn['mean_over_images'][key]['miss_fraction']))
            macro(f'QualPanel{name}Size', f1(pn['mean_over_images'][key]['mean_set_size_source_pixels']))


def audit():
    bank_overlap()
    j = load('results/audit_controls_ade')
    if j is None: return
    macro('AuditImages', num(j['images'])); macro('AuditUntruncatedFrozenRisk', pc(j['splits']['untruncated845_'+ALPHA][0]))
    macro('AuditNativeFrozenRisk', pc(j['splits']['native845_'+ALPHA][0])); macro('AuditUntruncatedReplaySize', f2(j['splits']['untruncated845_'+ALPHA][1]))
    macro('AuditNativeReplaySize', f2(j['splits']['native845_'+ALPHA][1])); macro('AuditBankPlusOneDiff', f'{j["bank_plus_one"]["mean_abs_logit_diff"]:.3f}')
    macro('AuditBankPlusOneImages', j['bank_plus_one']['images'])
    macro('AuditBankPlusOneCostRatio', num(int(float(f"{j['bank_plus_one']['seconds_separate']/j['bank_plus_one']['seconds_shared']:.2g}"))))
    # exactness of the reimplemented forwards (tests/check_catseg_anchor.py, tests/check_sed_anchor.py): max over images
    # of |released - reimplemented| logits, and of the anchored drift under co-candidate / order changes
    def sci(x):
        m, e = f'{x:.1e}'.split('e')
        return f'{m}\\times10^{{{int(e)}}}'
    for key, f in [('Catseg', 'anchor_check'), ('Sed', 'sed_anchor_check')]:
        p = Path(f'results/headroom_probe_ade/{f}.json')
        if not p.exists(): continue
        rows = json.loads(p.read_text()).values()
        macro(f'Check{key}Reimpl', sci(max(r['reimplementation_max_abs'] for r in rows)))
        macro(f'Check{key}Drift', sci(max(max(v for k, v in r.items() if k.startswith('anchored_')) for r in rows)))
    for k in ['same_top1', 'seconds_per_image_native_bank_plus_one', 'seconds_per_image_anchored']:
        if k in j['bank_plus_one']: macro('AuditBankPlusOne'+re.sub(r'[^A-Za-z]', '', k.title()), j['bank_plus_one'][k])
    c = load('results/clipseg_baseline_ade')
    if c: macro('ClipsegSrc', f1(c['sets']['0.1']['mean_size'][0])); macro('ClipsegFull', f1(c['sets']['0.1']['mean_size'][-1])); macro('ClipsegRisk', pc(c['sets']['0.1']['risk']))
    if c:                                             # images from results.json; split count only in the REPORT.md written by exp_clipseg_baseline.py
        macro('ClipsegImages', num(c['images']))
        ms = re.search(r'mean over (\d+) random', Path('results/clipseg_baseline_ade/REPORT.md').read_text())
        if ms: macro('ClipsegSplits', num(int(ms.group(1))))


def probe_miou():
    """Sampled-pixel mIoU from the probe reports (fidelity check) until the full-resolution row lands."""
    for key, run in [('vitb', 'results/headroom_probe_ade'), ('vitl683', 'results/headroom_probe_ade_vitl_bank683'), ('sed', 'results/headroom_probe_ade_sed'),
                     ('sed683', 'results/headroom_probe_ade_sed_bank683'), ('fcclip', 'results/headroom_probe_ade_fcclip'), ('fcclip683', 'results/headroom_probe_ade_fcclip_bank683')]:
        j = load(run+'_rest') or load(run)                              # the 1,600-image run when it exists, else the 400-image run
        if j is None: continue
        m = j['sampled_pixel_miou']; nat = m.get('catseg_native', m.get('fcclip_native')); anc = m.get('catseg_anchored', m.get('fcclip_anchored'))
        macro(CONFIGS[key][5]+'PixMiouNative', pc(nat)); macro(CONFIGS[key][5]+'PixMiouAnch', pc(anc))


def table_miou():
    """Full-resolution mIoU (results/miou_full_<dataset>_<lane>); written only when at least one lane has finished.
    Also writes tables/miou_pixacc.tex (pixel accuracy, supplement) and macros \Miou<Lane><Arm><Dataset>,
    \PixAcc<Lane><Arm><Dataset>, \MiouGap<Lane><Arm><Dataset> (native minus anchored, signed)."""
    DS = [('ade150', 'A-150', 'AdeOneFifty'), ('pc459', 'PC-459', 'PcFourFiftyNine'), ('ade847', 'A-847', 'AdeEightFortySeven'), ('pc59', 'PC-59', 'PcFiftyNine')]
    LANES = [('vitb', 'CAT-Seg ViT-B'), ('vitl', 'CAT-Seg ViT-L'), ('declip', 'CAT-Seg + DeCLIP EVA-L'), ('sed', 'SED ConvNeXt-L'), ('fcclip', 'FC-CLIP ConvNeXt-L')]
    ARM_NAMES = {'native': 'native (released)', 'anchored_coco171': 'anchored, COCO-171 bank', 'anchored_bank683': 'anchored, 683-name bank',
                 'anchored_133': 'anchored, 133-name bank'}
    found = {}
    for lane, _ in LANES:
        for ds, _, _ in DS:
            j = load(f'results/miou_full_{ds}_{lane}')
            if j: found[(lane, ds)] = j
    if not found: return
    def build(key, macro_stem):
        rows = [r'\begin{tabular}{@{}ll' + 'r'*len(DS) + '@{}}', r'\toprule', r'Model & scoring & ' + ' & '.join(n for _, n, _ in DS) + r' \\', r'\midrule']
        for lane, lname in LANES:
            arms_here = []
            for ds, _, _ in DS:
                j = found.get((lane, ds))
                if j: arms_here = list(j['per_arm'].keys()); break
            if not arms_here: continue
            for arm in arms_here:
                cells = []
                for ds, _, dsname in DS:
                    j = found.get((lane, ds)); v = j['per_arm'][arm][key] if j and arm in j['per_arm'] else None
                    cells.append('--' if v is None else pc(v))
                    if v is not None:
                        armname = re.sub(r'[^A-Za-z]', '', arm.title())
                        macro(macro_stem + lane.title() + armname + dsname, pc(v))
                        if arm != 'native' and macro_stem == 'Miou':
                            gap = j['per_arm']['native'][key] - v
                            macro('MiouGap' + lane.title() + armname + dsname, f'{100*gap:.1f}'.replace('-0.0', '0.0'))
                name = ARM_NAMES.get(arm, arm.replace('_', ' '))
                if lane == 'fcclip' and arm == 'anchored_bank683': name = 'anchored, 701-name bank'
                rows.append(f'{lname if arm == arms_here[0] else ""} & {name} & ' + ' & '.join(cells) + r' \\')
            rows.append(r'\midrule')
        rows[-1] = r'\bottomrule'; rows.append(r'\end{tabular}')
        return '\n'.join(rows) + '\n'
    (TAB/'miou.tex').write_text(build('miou', 'Miou'))
    (TAB/'miou_pixacc.tex').write_text(build('pixel_accuracy', 'PixAcc'))
    # conversion cost (683-name bank) across the cost-aggregation models, per benchmark: \MiouGapLo<Dataset>, \MiouGapHi<Dataset>
    for ds, _, dsname in DS:
        gaps = [found[(l, ds)]['per_arm']['native']['miou']-found[(l, ds)]['per_arm']['anchored_bank683']['miou']
                for l in ['vitb', 'vitl', 'declip', 'sed'] if (l, ds) in found and 'anchored_bank683' in found[(l, ds)]['per_arm']]
        if gaps:
            macro('MiouGapLo'+dsname, f'{100*min(gaps):.1f}'.replace('-0.0', '0.0')); macro('MiouGapHi'+dsname, f'{100*max(gaps):.1f}'.replace('-0.0', '0.0'))
    # protocol check (2026-09-24): ViT-B native on PC-59 with the released global view and/or first-synonym text (exp_miou_full.py --global-view/--synonyms)
    base = found[('vitb', 'pc59')]['per_arm']['native']['miou']
    variants = [load(f'results/miou_full_pc59_vitb_{v}')['per_arm']['native']['miou'] for v in ['gvoriginal_synfirst', 'gvoriginal_synmean', 'gvsquare_synfirst']]
    macro('MiouProtocolMaxChange', f'{100*max(abs(v-base) for v in variants):.2f}')


def table_runtime():
    """Seconds per image and peak memory at 845 labels (tables/runtime.tex and the Rt* macros of the cost paragraphs).
    Every configuration was timed back to back on one idle GH200 over the same 100 development images.
    The native column is the single grown-vocabulary pass that deployment runs; the
    source-vocabulary pass is needed only once, for calibration, and is not counted. The ratio is end to end
    (features included). The one-label-at-a-time row is the audit control, timed on the RTX 5070 Ti."""
    rows_spec = [  # (label, timing tag, anchored column shown, macro prefix)
        ('CAT-Seg ViT-B, COCO-171 bank, sliding window 640', 'vitb_coco', True, 'VitB'),
        ('CAT-Seg ViT-B, 683-name bank', 'vitb_bank683', True, 'VitBBank'),
        ('CAT-Seg ViT-L, COCO-171 bank', 'vitl_coco', True, 'VitL'),
        ('CAT-Seg ViT-L, 683-name bank', 'vitl_bank683', True, 'VitLBank'),
        ('SED ConvNeXt-L, COCO-171 bank, whole image 768', 'sed_coco', True, 'Sed'),
        ('SED ConvNeXt-L, fast mode (top-8), native only', 'sed_fast8', False, 'SedFast'),
        ('SED ConvNeXt-L, 683-name bank', 'sed_bank683', True, 'SedBank'),
        ('FC-CLIP ConvNeXt-L, 133-name bank, shortest edge 800', 'fcclip', True, 'Fcclip'),
        ('FC-CLIP ConvNeXt-L, 701-name bank', 'fcclip_bank683', True, 'FcclipBank')]
    rows = ['% generated by src/paper_numbers.py from results/headroom_probe_ade_timing2_*/results.json, results/audit_controls_ade and results/ovd_probe_*_timing; do not edit',
            r'\begin{tabular}{@{}lrrrrr@{}}', r'\toprule', r'Model & features & native & anchored & ratio & peak memory \\', r'\midrule']
    ratios = {}
    n_cal = headline_row('vitl683')['images']//2
    sig2 = lambda x: int(float(f'{x:.2g}'))
    # FC-CLIP's timed features (backbone_masks_and_logits) include the per-query logits of the bank columns, which only the
    # anchored arm computes; no native pass without them was timed. The logits are the only vocabulary-dependent part of
    # that span (text embeddings are precomputed), so the 133-name-bank pass bounds a native pass from above, and the
    # 701-name-bank row gets a lower bound on its ratio and upper bounds on its break-even and recalibration time. The
    # 133-name-bank row has no smaller pass to bound it and shows no ratio.
    fc_native_feat_ub = load('results/headroom_probe_ade_timing2_fcclip')['mean_seconds_per_image']['backbone_masks_and_logits']
    for label, tag, show_anch, key in rows_spec:
        j = load(f'results/headroom_probe_ade_timing2_{tag}'); t = j['mean_seconds_per_image']
        assert j['gpu'] == 'NVIDIA GH200 480GB', (tag, j['gpu'])
        fc = 'backbone_masks_and_logits' in t
        feat = t['backbone_masks_and_logits'] if fc else t['clip_features']
        anch = t['anchored_845'] if fc else t['anchored_reference_plus_845']
        prec = 4 if fc else 2      # FC-CLIP's per-query softmax takes well under a millisecond
        if fc:
            bounded = feat > fc_native_feat_ub
            ratio = (feat+anch)/(fc_native_feat_ub+t['native_845'])
            ratio_cell = f'$\\geq${ratio:.1f}$\\times$' if bounded else '--'
        else:
            ratio = (feat+anch)/(feat+t['native_845']); ratio_cell = f'{ratio:.1f}$\\times$'
        cells = [f'{feat:.2f}' + ('$^\\dagger$' if fc else ''), f'{t["native_845"]:.{prec}f}'] + \
                ([f'{anch:.{prec}f}', ratio_cell] if show_anch else ['--', '--'])
        rows.append(f'{label} & ' + ' & '.join(cells) + f' & {j["peak_memory_gb"]:.1f} GB \\\\')
        macro(f'Rt{key}Feat', f2(feat)); macro(f'Rt{key}Native', f'{t["native_845"]:.{prec}f}'); macro(f'Rt{key}Mem', f1(j['peak_memory_gb']))
        if show_anch:
            macro(f'Rt{key}Anch', f'{anch:.{prec}f}')
        if fc:
            if bounded:     # ratio >= this, break-even <= this, recalibration pass <= this
                macro(f'Rt{key}RatioMin', f1(ratio)); macro(f'Rt{key}BreakEvenMax', num(sig2(n_cal/(ratio-1))))
                macro(f'Rt{key}RecalMinMax', f1(n_cal*(fc_native_feat_ub+t['native_845'])/60))
            continue
        if show_anch:
            macro(f'Rt{key}Ratio', f1(ratio)); ratios[key] = ratio
            # recalibration costs one native pass per calibration image per vocabulary; the conversion (ratio - 1) extra per test image
            macro(f'Rt{key}BreakEven', num(sig2(n_cal/(ratio-1)))); macro(f'Rt{key}RecalMin', f1(n_cal*(feat+t['native_845'])/60))
            # with the vocabulary-independent features of the calibration images cached, recalibration costs n_cal native passes only
            macro(f'Rt{key}BreakEvenCached', num(sig2(n_cal*t['native_845']/(anch-t['native_845']))))
    macro('RtCalImages', num(n_cal))
    agg = [ratios[k] for k in ratios if not k.startswith('Fcclip')]
    macro('RtRatioLo', f1(min(agg))); macro('RtRatioHi', f1(max(agg)))
    b = load('results/audit_controls_ade')['bank_plus_one']
    macro('RtOneAtATime', f'{b["seconds_separate"]:.0f}')
    rows += [f'native, one label at a time against the bank (ViT-B, RTX 5070 Ti) & -- & {b["seconds_separate"]:.0f} & -- & -- & -- \\\\']
    # detection at 1,204 names (first 100 benchmark images, idle GH200): native = the
    # chunked LVIS-scale pass (31 prompts of 40 names), anchored = bank A; no separate feature column, so the ratio is anchored/native
    det = [(m, name, pre) for m, name, pre in OVD if load(f'results/ovd_probe_{m}_timing') is not None]
    speedups = []
    if det:
        rows += [r'\midrule', r'\multicolumn{6}{l}{\emph{Detection, $1{,}204$ names}} \\']
    for m, name, pre in det:
        j = load(f'results/ovd_probe_{m}_timing'); t = j['seconds_per_image']
        assert j['gpu'] == 'NVIDIA GH200 480GB', (m, j['gpu'])
        if m == 'owlv2':
            rows.append(f'{name} & -- & {t["owl"]:.2f} & -- & -- & {j["peak_memory_gb"]:.1f} GB \\\\'); macro(pre+'RtNative', f2(t['owl']))
            continue
        ratio = t['anch_a']/t['native_lvis']
        rows.append(f'{name}, 80-name bank & -- & {t["native_lvis"]:.2f} & {t["anch_a"]:.2f} & {ratio:.2f}$\\times$ ({1/ratio:.1f}$\\times$ faster) & {j["peak_memory_gb"]:.1f} GB \\\\')
        macro(pre+'RtNative', f2(t['native_lvis'])); macro(pre+'RtAnch', f2(t['anch_a'])); macro(pre+'RtSpeedup', f1(1/ratio)); speedups.append(1/ratio)
    if speedups:
        macro('OvdRtSpeedupLo', f1(min(speedups))); macro('OvdRtSpeedupHi', f1(max(speedups)))
    rows += [r'\bottomrule',
             r'\multicolumn{6}{l}{\footnotesize $^\dagger$backbone, mask proposals and per-query logits, including the bank columns, which only the anchored arm needs.}\\',
             r'\multicolumn{6}{l}{\footnotesize No FC-CLIP pass without bank columns was timed; the $133$-name-bank pass bounds it from above, so the $701$-name-bank ratio is a lower bound.}', r'\end{tabular}']
    (TAB/'runtime.tex').write_text('\n'.join(rows)+'\n')


def table_memory():
    """Peak GPU memory per arm as the vocabulary grows (tables/memory.tex, Mem* macros; results/memory_*, src/exp_memory.py and
    src/exp_memory_fcclip.py). The peak is reset before each arm, unlike the peak column of tab:runtime, which is
    the maximum over all passes of a timing run. GB = 2**30 bytes, as in tab:runtime. Measured on the local RTX 5070 Ti."""
    sizes = ['150', '845', '1690', '3380', '6760']
    card = 16303/1024                     # nvidia-smi memory.total of the RTX 5070 Ti (MiB), in GB
    spec = [('CAT-Seg ViT-B', 'vitb', 'VitB', [('native', 'native'), ('anchored', 'anchored'), ('anchored, lean', 'anchored_lean')]),
            ('CAT-Seg ViT-L', 'vitl', 'VitL', [('native', 'native'), ('anchored', 'anchored'), ('anchored, lean', 'anchored_lean')]),
            ('SED', 'sed', 'Sed', [('native', 'native'), ('anchored', 'anchored'), ('anchored, lean', 'anchored_lean')]),
            ('FC-CLIP', 'fcclip', 'Fc', [('native', 'native'), ('anchored', 'anchored')]),
            ('CAT-Seg + DeCLIP', 'declip', 'Declip', [('native', 'native'), ('anchored', 'anchored'), ('anchored, lean', 'anchored_lean')])]
    rows = ['% generated by src/paper_numbers.py from results/memory_{vitb,vitl,sed,fcclip,declip}/results.json; do not edit',
            r'\begin{tabular}{@{}llrrrrr@{}}', r'\toprule',
            r'Model & arm & \multicolumn{5}{c}{vocabulary size} \\', r'\cmidrule(l){3-7}',
            '& & '+' & '.join(f'${num(int(V))}$'.replace(',', '{,}') for V in sizes)+r' \\', r'\midrule']
    J = {}
    for name, tag, key, arms in spec:
        j = J[tag] = load(f'results/memory_{tag}')
        assert j['gpu'] == 'NVIDIA GeForce RTX 5070 Ti' and j['vocab_sizes'] == [int(V) for V in sizes], tag
        assert j['images'] == J['vitb']['images'], tag
        if 'native_released' in j['peak_gb']:         # the chunked decoder of the probe changes no peak: same as released code
            assert all(abs(j['peak_gb']['native'][V]-j['peak_gb']['native_released'][V]) < .02 for V in sizes), tag
        for k, (label, arm) in enumerate(arms):
            cells = []
            for V in sizes:
                v = j['peak_gb'][arm][V]
                cells.append(r'\emph{OOM}' if int(V) in j['out_of_memory'][arm] else f'{v:.2f}'+(r'$^\ddagger$' if v > card else ''))
            rows.append(f'{name if k == 0 else ""} & {label} & '+' & '.join(cells)+r' \\')
        rows.append(r'\addlinespace')
        nat, anc = j['peak_gb']['native'], j['peak_gb']['anchored_lean' if 'anchored_lean' in j['peak_gb'] else 'anchored']
        macro(f'Mem{key}NatSrc', f2(nat['150'])); macro(f'Mem{key}NatFull', f2(nat['845']))
        macro(f'Mem{key}AnchMin', f2(min(anc.values()))); macro(f'Mem{key}AnchMax', f2(max(anc.values())))
    rows = rows[:-1]+[r'\bottomrule', r'\end{tabular}']     # the dagger is explained in the caption (MemCard)
    (TAB/'memory.tex').write_text('\n'.join(rows)+'\n')
    sed, vitl, fc = J['sed'], J['vitl'], J['fcclip']
    assert sed['out_of_memory']['native'] == [6760] and not any(sed['out_of_memory'][a] for a in ('anchored', 'anchored_lean'))
    assert sed['peak_gb']['native']['3380'] > card > sed['peak_gb']['native']['1690']
    for tag in ('vitb', 'vitl', 'declip'):             # anchored above native at the source names, below it from 845 on
        p = J[tag]['peak_gb']
        assert p['anchored_lean']['150'] > p['native']['150'] and all(p['anchored'][V] < p['native'][V] for V in sizes[1:]), tag
    macro('MemImages', num(sed['images'])); macro('MemCard', f1(card))
    macro('MemSedNatTwo', f1(sed['peak_gb']['native']['1690'])); macro('MemSedNatFour', f1(sed['peak_gb']['native']['3380']))
    macro('MemVitLSrcExtra', f1(vitl['peak_gb']['anchored_lean']['150']-vitl['peak_gb']['native']['150']))
    macro('MemVitLFullSaving', f1(vitl['peak_gb']['native']['845']-vitl['peak_gb']['anchored_lean']['845']))
    macro('MemFcMax', f1(max(max(fc['peak_gb'][a].values()) for a in ('native', 'anchored'))))
    macro('MemBankVitLMB', f1(vitl['bank_text_bytes']/2**20)); macro('MemBankSedMB', f'{sed["bank_text_bytes"]/2**20:.0f}')
    cal = vitl['calibration']; assert cal == sed['calibration']
    macro('MemCalMB', f'{cal["n_cal_bytes"]/2**20:.0f}'); macro('MemCalImages', num(cal['n_cal']))


def table_runtime_lean():
    """Full against lean bank pass (tables/runtime_lean.tex, RtLocal*/RtLean* macros): the lean pass stops once the key/value
    sums are recorded (bank_context / forward_bank lean=True; tests/check_lean_bank.py shows the candidate scores unchanged).
    Timed on the local RTX 5070 Ti (the GH200 is gone) over the same 100 development images as tab:runtime, each pair back
    to back on an otherwise idle card. Ratios are end to end, as in table_runtime."""
    rows_spec = [('CAT-Seg ViT-B, COCO-171 bank, sliding window 640', 'vitb_coco', 'VitB'), ('CAT-Seg ViT-B, 683-name bank', 'vitb_bank683', 'VitBBank'),
                 ('CAT-Seg ViT-L, COCO-171 bank', 'vitl_coco', 'VitL'), ('CAT-Seg ViT-L, 683-name bank', 'vitl_bank683', 'VitLBank'),
                 ('SED ConvNeXt-L, COCO-171 bank, whole image 768', 'sed_coco', 'Sed'), ('SED ConvNeXt-L, 683-name bank', 'sed_bank683', 'SedBank'),
                 # DeCLIP was not timed on the GH200; timed here on 2026-11-01
                 ('CAT-Seg + DeCLIP EVA-L, 683-name bank', 'declip_bank683', 'DeclipBank')]
    rows = ['% generated by src/paper_numbers.py from results/headroom_probe_ade_timing3_*/results.json; do not edit',
            r'\begin{tabular}{@{}lrrrrrrr@{}}', r'\toprule',
            r'& & & \multicolumn{2}{c}{full bank pass} & \multicolumn{2}{c}{lean bank pass} & \\',
            r'\cmidrule(lr){4-5}\cmidrule(lr){6-7}',
            r'Model & features & native & anchored & ratio & anchored & ratio & peak memory \\', r'\midrule']
    n_cal = headline_row('vitl683')['images']//2
    sig2 = lambda x: int(float(f'{x:.2g}'))
    for label, tag, key in rows_spec:
        full = load(f'results/headroom_probe_ade_timing3_{tag}'); lean = load(f'results/headroom_probe_ade_timing3_{tag}_lean')
        for j in (full, lean): assert j['gpu'] == 'NVIDIA GeForce RTX 5070 Ti', (tag, j['gpu'])
        tf, tl = full['mean_seconds_per_image'], lean['mean_seconds_per_image']
        # features and the native pass are the same computation in both runs; the full run's values are shown
        feat, nat, anch, anch_lean = tf['clip_features'], tf['native_845'], tf['anchored_reference_plus_845'], tl['anchored_reference_plus_845']
        assert abs(tl['native_845']-nat) < .05*nat, (tag, nat, tl['native_845'])     # same card, same load: the pair is comparable
        ratio, ratio_lean = (feat+anch)/(feat+nat), (feat+anch_lean)/(feat+nat)
        rows.append(f'{label} & {feat:.2f} & {nat:.2f} & {anch:.2f} & {ratio:.1f}$\\times$ & {anch_lean:.2f} & {ratio_lean:.1f}$\\times$ & {lean["peak_memory_gb"]:.1f} GB \\\\')
        macro(f'RtLocal{key}Feat', f2(feat)); macro(f'RtLocal{key}Native', f2(nat)); macro(f'RtLocal{key}Anch', f2(anch)); macro(f'RtLocal{key}Ratio', f1(ratio))
        macro(f'RtLocal{key}RecalMin', f1(n_cal*(feat+nat)/60))       # one native pass per calibration image, on this card
        macro(f'RtLean{key}Anch', f2(anch_lean)); macro(f'RtLean{key}Ratio', f1(ratio_lean)); macro(f'RtLean{key}Mem', f1(lean['peak_memory_gb']))
        macro(f'RtLean{key}Saving', f'{100*(anch-anch_lean)/anch:.0f}')              # share of the anchored time removed
        if 'Bank' in key:
            macro(f'RtLean{key}BreakEven', num(sig2(n_cal/(ratio_lean-1))))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'runtime_lean.tex').write_text('\n'.join(rows)+'\n')
    # tests/check_lean_bank.py: sums and anchored logits of the lean pass equal the full pass, per model
    checks = [json.loads(p.read_text()) for p in sorted(Path('results/lean_bank_check').glob('*_*_*.json')) if p.name != 'timing3_repeats.json']
    assert len(checks) == 3 and all(c['sums_bitwise_equal'] and c['anchored_logits_max_abs_diff'] == 0 for c in checks), checks
    assert len({c['images'] for c in checks}) == 1
    macro('LeanCheckImages', num(checks[0]['images']))


FREEFORM = [('CAT-Seg ViT-L', 'vitl_bank683', 'VitL'), ('SED', 'sed_bank683', 'Sed'), ('FC-CLIP', 'fcclip_bank683', 'Fc')]


def table_freeform():
    """Free-form per-image names from a language model (docs/FREEFORM_NAMES_PROTOCOL.md; exp_freeform_names.py,
    exp_freeform_vocab_probe*.py, exp_freeform_vocab.py): tables/freeform.tex and the Ff* macros. Each image deploys the 150
    source names plus the names Claude Opus 5.5 gave for it, most outside ADE20K-847. Written once every model's run exists."""
    nm = load('results/freeform_names_ade')
    js = [(name, load(f'results/freeform_vocab_{tag}'), key) for name, tag, key in FREEFORM]
    if nm is None or any(j is None for _, j, _ in js): return
    assert not nm['failed'] and all(j['images'] == nm['images'] for _, j, _ in js)
    macro('FfImages', num(nm['images'])); macro('FfAnswered', f1(nm['answered_names_per_image'])); macro('FfAdded', f1(nm['added_names_per_image']))
    macro('FfUnique', num(nm['unique_added'])); macro('FfOutsideAde', pc(nm['share_outside_ade847'], 0)); macro('FfOutsideLex', pc(nm['share_outside_lexicon'], 0))
    macro('FfCost', f'{nm["cost_usd"]:.2f}')
    ARMS = [('anchored, calibrated once', 'Anch'), ('native, reused at 150', 'Reused'), ('native, recalibrated at 845', 'Recal'),
            ('native, recalibrated at a 1,690-name lexicon', 'LexSmall'), ('native, recalibrated at a 17,001-name lexicon', 'Lex'),
            ('native, matched to the names', 'Matched')]
    cell = lambda d: f'{pc(d["mean_risk"])}/{f1(d["mean_size"])}' if d else '--'
    rows = ['% generated by src/paper_numbers.py from results/freeform_vocab_*/results.json; do not edit',
            r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
            r'& \multicolumn{1}{c}{anchored} & \multicolumn{5}{c}{native} \\ \cmidrule(lr){2-2}\cmidrule(l){3-7}'
            r'Model & \multicolumn{1}{c}{once} & \multicolumn{1}{c}{reused} & \multicolumn{1}{c}{recal.\ 845} & \multicolumn{1}{c}{recal.\ 1.7k}'
            r' & \multicolumn{1}{c}{recal.\ 17k} & \multicolumn{1}{c}{matched} \\']
    for alpha, pre in [('0.1', 'Ff'), ('0.05', 'FfB')]:
        rows += [r'\midrule', r'\multicolumn{7}{@{}l}{$\alpha=' + str(int(round(100*float(alpha)))) + r'\%$} \\']
        for name, j, key in js:
            r = j['alphas'][alpha]
            rows.append(f'{name} & ' + ' & '.join(cell(r.get(a)) for a, _ in ARMS) + r' \\')
            for a, stem in ARMS:
                if a in r:
                    macro(f'{pre}{key}{stem}Risk', pc(r[a]['mean_risk'])); macro(f'{pre}{key}{stem}Size', f2(r[a]['mean_size']))
                    macro(f'{pre}{key}{stem}Above', pc(r[a]['frac_splits_above_alpha'], 0)); macro(f'{pre}{key}{stem}Added', f2(r[a]['mean_added_in_set']))
        for a, stem in ARMS[:3]:
            v = [j['alphas'][alpha][a]['mean_risk'] for _, j, _ in js]
            macro(f'{pre}{stem}RiskLo', pc(min(v))); macro(f'{pre}{stem}RiskHi', pc(max(v)))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'freeform.tex').write_text('\n'.join(rows)+'\n')
    r = {key: j['alphas']['0.1'] for _, j, key in js}
    # what the text states: the reused and the 845-name thresholds exceed the target for every model, the anchored one never does
    assert all(r[k]['native, reused at 150']['frac_splits_above_alpha'] == 1 and r[k]['native, recalibrated at 845']['frac_splits_above_alpha'] == 1 for k in r)
    assert all(r[k]['anchored, calibrated once']['mean_risk'] <= .1 for k in r)
    # Prop. 1: the anchored source-label risk under the free-form names is the one under every fixed rule (same splits);
    # equal for SED and FC-CLIP, 3e-8 apart for CAT-Seg ViT-L (one sampled pixel's worth; far below the printed precision)
    for _, tag, key in FREEFORM:
        a = load(f'results/adaptive_vocab_{tag}')['alphas']['0.1']['adversarial']['anchored, calibrated once']['mean_risk']
        assert abs(r[key]['anchored, calibrated once']['mean_risk']-a) < 1e-6, (tag, a)
    assert all(r[k]['anchored, calibrated once']['mean_size'] < r[k]['native, matched to the names']['mean_size'] for k in r)
    lex = r['Fc']['native, recalibrated at a 17,001-name lexicon']
    assert lex['mean_risk'] <= .1 and r['Sed']['native, recalibrated at a 17,001-name lexicon']['mean_risk'] > .1
    macro('FfFcLexRatio', f1(lex['mean_size']/r['Fc']['anchored, calibrated once']['mean_size']))


def disjoint_bank_check():
    """The 683-name bank was chosen on the first 400 of the 2,000 ADE20K development images (exp_anchor_bank.py); the
    repeated-split analysis on the other 1,600 alone (exp_headroom_splits.py --disjoint) gives the Disj* macros."""
    keys = [('vitl683', 'vitl_bank683'), ('sed683', 'sed_bank683'), ('fcclip683', 'fcclip_bank683')]
    js = [(k, load(f'results/headroom_splits_ade_{t}_disjoint')) for k, t in keys]
    if any(j is None for _, j in js): return
    risk, gap = [], []
    for k, j in js:
        assert j['disjoint_from_bank_choice']
        a = j['designs'][f'cal{j["images"]//2}_{ALPHA}']['catseg_anchored']
        risk.append(a['mean_risk']); gap.append(abs(a['mean_size'][-1]-headline_row(k)['anch_full']))
    macro('DisjImages', num(js[0][1]['images'])); macro('DisjBankImages', num(2000-js[0][1]['images']))
    macro('DisjAnchRiskLo', pc(min(risk))); macro('DisjAnchRiskHi', pc(max(risk))); macro('DisjSizeGapMax', f1(max(gap)))


def table_adaptive(tag='vitl_bank683', out='adaptive', pre='Adapt'):
    """Per-image vocabularies (exp_adaptive_vocab.py; 683-name bank): tables/{out}.tex and \\{pre}* macros; CAT-Seg ViT-L in the
    main text, SED (tag sed_bank683) in the supplement. Written only once results/adaptive_vocab_{tag} exists."""
    j = load(f'results/adaptive_vocab_{tag}')
    if j is None: return
    r = j['alphas']['0.1']
    lex = max(int(k.split('a ')[1].split('-name')[0].replace(',', '')) for k in r['rand50'] if 'lexicon' in k) if any('lexicon' in k for k in r['rand50']) else None
    LEX = f'native, recalibrated at a {lex:,}-name lexicon' if lex else None
    POL = [('present', 'present in image'), ('rand50', '50 random'), ('rand200', '200 random'),
           ('rand500', '500 random'), ('tagger50', 'tagger, top 50'), ('adversarial', 'worst, per image')]
    ARMS = [('anchored, calibrated once', 'Anch'), ('native, frozen at 150', 'Frozen'), ('native, recalibrated at 845', 'Recal'),
            ('native, calibrated under rand500', 'RandCal'), ('native, matched to the policy', 'Matched')] + ([(LEX, 'Lex')] if LEX else [])
    cells = lambda d: f'{pc(d["mean_risk"])}/{f1(d["mean_size"])}'
    head = r'& \multicolumn{1}{c}{anchored} & \multicolumn{' + str(len(ARMS)-1) + r'}{c}{native} \\ \cmidrule(lr){2-2}\cmidrule(l){3-' + str(len(ARMS)+1) + '}' + \
           r'Added names & \multicolumn{1}{c}{once} & \multicolumn{1}{c}{reused} & \multicolumn{1}{c}{recal.\ 845} & \multicolumn{1}{c}{random}' + \
           (r' & \multicolumn{1}{c}{recal.\ ' + f'{lex//1000}k' + '}' if LEX else '') + r' & \multicolumn{1}{c}{matched} \\'
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}l' + 'r'*(len(ARMS)) + '@{}}', r'\toprule', head, r'\midrule']
    for p, pname in POL:
        # last column: native calibrated under the deployed policy itself (for the per-image worst case, CRC on the worst case)
        d = {**r[p]}; d.setdefault('native, matched to the policy', r[p].get('native, worst case over the policies'))
        if p == 'rand500': d.setdefault('native, calibrated under rand500', r[p].get('native, matched to the policy'))  # the random calibration is the matched one here
        order = [a for a, _ in ARMS if a != 'native, matched to the policy'] + ['native, matched to the policy']
        rows.append(f'{pname} & ' + ' & '.join(cells(d[a]) if d.get(a) else '--' for a in order) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/f'{out}.tex').write_text('\n'.join(rows)+'\n')
    stems = {'present': 'Present', 'rand50': 'RandFifty', 'rand200': 'RandTwoHundred', 'rand500': 'RandFiveHundred', 'tagger50': 'Tagger', 'adversarial': 'Adv'}
    for p, ps in stems.items():
        for arm, stem in ARMS + [(f'native, calibrated under {q}', 'CalUnder'+stems[q]) for q in stems if q != 'adversarial']:
            if arm in r[p]:
                d = r[p][arm]
                macro(f'{pre}{ps}{stem}Risk', pc(d['mean_risk'])); macro(f'{pre}{ps}{stem}Size', f2(d['mean_size'])); macro(f'{pre}{ps}{stem}Above', pc(d['frac_splits_above_alpha'], 0))
    w = r['adversarial']['native, worst case over the policies']
    macro(pre+'AdvWorstRisk', pc(w['mean_risk'])); macro(pre+'AdvWorstSize', f2(w['mean_size']))
    b = j['alphas']['0.05']
    macro(pre+'BAdvAnchSize', f2(b['adversarial']['anchored, calibrated once']['mean_size']))
    if lex:
        macro(pre+'LexSize', num(lex))
        macro(pre+'BAdvLexSize', f2(b['adversarial'][LEX]['mean_size']))
        sizes = [b[p][LEX]['mean_size'] for p, _ in POL]; asz = [b[p]['anchored, calibrated once']['mean_size'] for p, _ in POL]
        macro(pre+'BLexSizeLo', f1(min(sizes))); macro(pre+'BLexSizeHi', f1(max(sizes)))
        macro(pre+'BAnchSizeLo', f1(min(asz))); macro(pre+'BAnchSizeHi', f1(max(asz)))
        lx = sorted(int(k.split('a ')[1].split('-name')[0].replace(',', '')) for k in r['rand50'] if 'lexicon' in k)
        macro(pre+'LexSmall', num(lx[0]))
        for n, word in zip(lx, ['One', 'Two', 'Three', 'Four']):
            d = r['adversarial'][f'native, recalibrated at a {n:,}-name lexicon']
            macro(f'{pre}AdvLex{word}Risk', pc(d['mean_risk'])); macro(f'{pre}AdvLex{word}Size', f2(d['mean_size'])); macro(f'{pre}Lex{word}Names', num(n))
    macro(pre+'Images', num(j['images'])); macro(pre+'PresentNames', f1(j['added_names_per_image']['present']['mean']))


PAS_ADAPT = [('CAT-Seg ViT-L', 'vitl_bank683', 'AdaptPas'), ('SED', 'sed_bank683', 'AdaptPasSed')]


def table_adaptive_pascal():
    """Per-image vocabularies on Pascal Context, 59 -> 458: tables/adaptive_pascal.tex,
    both models in one supplement table, and \\AdaptPas* (ViT-L) and \\AdaptPasSed* macros. Written only once both runs exist."""
    js = [(name, load(f'results/adaptive_vocab_pascal_{tag}'), pre) for name, tag, pre in PAS_ADAPT]
    if any(j is None for _, j, _ in js): return
    POL = [('present', 'present in image'), ('rand50', '50 random'), ('rand100', '100 random'),
           ('rand300', '300 random'), ('tagger50', 'tagger, top 50'), ('adversarial', 'worst, per image')]
    ARMS = [('anchored, calibrated once', 'Anch'), ('native, frozen at 59', 'Frozen'), ('native, recalibrated at 458', 'Recal'),
            ('native, calibrated under rand300', 'RandCal'), ('native, matched to the policy', 'Matched')]
    cells = lambda d: f'{pc(d["mean_risk"])}/{f1(d["mean_size"])}'
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lrrrrr@{}}', r'\toprule',
            r'& \multicolumn{1}{c}{anchored} & \multicolumn{4}{c}{native} \\ \cmidrule(lr){2-2}\cmidrule(l){3-6}'
            r'Added names & \multicolumn{1}{c}{once} & \multicolumn{1}{c}{reused} & \multicolumn{1}{c}{recal.\ 458} & \multicolumn{1}{c}{random} & \multicolumn{1}{c}{matched} \\']
    stems = {'present': 'Present', 'rand50': 'RandFifty', 'rand100': 'RandHundred', 'rand300': 'RandThreeHundred', 'tagger50': 'Tagger', 'adversarial': 'Adv'}
    for name, j, pre in js:
        r = j['alphas']['0.1']
        rows += [r'\midrule', r'\multicolumn{6}{@{}l}{\emph{' + name + r'}} \\']
        for p, pname in POL:
            # as in table_adaptive: the last column is calibrated under the row's own rule (the worst case over the rules for the last row)
            d = {**r[p]}; d.setdefault('native, matched to the policy', r[p].get('native, worst case over the policies'))
            if p == 'rand300': d.setdefault('native, calibrated under rand300', r[p].get('native, matched to the policy'))
            rows.append(f'{pname} & ' + ' & '.join(cells(d[a]) for a, _ in ARMS) + r' \\')
        for p, ps in stems.items():
            for arm, stem in ARMS + [('native, worst case over the policies', 'Worst')]:
                if arm in r[p]:
                    d = r[p][arm]
                    macro(f'{pre}{ps}{stem}Risk', pc(d['mean_risk'])); macro(f'{pre}{ps}{stem}Size', f2(d['mean_size'])); macro(f'{pre}{ps}{stem}Above', pc(d['frac_splits_above_alpha'], 0))
        b = j['alphas']['0.05']['adversarial']
        for arm, stem in ARMS[:4] + [('native, worst case over the policies', 'Worst')]:
            macro(f'{pre}BAdv{stem}Risk', pc(b[arm]['mean_risk'])); macro(f'{pre}BAdv{stem}Size', f2(b[arm]['mean_size']))
        macro(pre+'Images', num(j['images'])); macro(pre+'PresentNames', f1(j['added_names_per_image']['present']['mean']))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'adaptive_pascal.tex').write_text('\n'.join(rows)+'\n')


def table_adaptive_main():
    """Main-text summary of the per-image tables (tables/adaptive_main.tex): one row per model and benchmark, the worst-case rule
    ('worst, per image') of tables/adaptive*.tex, with what each threshold needs to know at calibration time."""
    runs = [('CAT-Seg ViT-L', 'vitl_bank683'), ('SED', 'sed_bank683'), ('FC-CLIP', 'fcclip_bank683')]
    js = [(name, load(f'results/adaptive_vocab_{tag}')) for name, tag in runs]
    if any(j is None for _, j in js): return
    lex = max(int(k.split('a ')[1].split('-name')[0].replace(',', '')) for k in js[0][1]['alphas']['0.1']['rand50'] if 'lexicon' in k)
    # 'random': native calibrated on per-image vocabularies of random names from the grown vocabulary (rule-agnostic baseline):
    # 500 of the 845 on ADE20K, 300 of the 458 on Pascal Context (the largest random rule of each protocol)
    ARMS = ['anchored, calibrated once', 'native, frozen at 150', 'native, recalibrated at 845', 'native, calibrated under rand500',
            f'native, recalibrated at a {lex:,}-name lexicon', 'native, worst case over the policies']
    PARMS = ['anchored, calibrated once', 'native, frozen at 59', 'native, recalibrated at 458', 'native, calibrated under rand300',
             None, 'native, worst case over the policies']
    cell = lambda d: f'{pc(d["mean_risk"])}/{f1(d["mean_size"])}' if d else '--'
    rows = [r'\setlength{\tabcolsep}{3pt}\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
            r'& \multicolumn{1}{c}{anchored} & \multicolumn{5}{c}{native} \\ \cmidrule(lr){2-2}\cmidrule(l){3-7}',
            r'& \multicolumn{1}{c}{once} & \multicolumn{1}{c}{reused} & \multicolumn{1}{c}{recal.} & \multicolumn{1}{c}{random} & \multicolumn{1}{c}{recal.} & \multicolumn{1}{c}{rules} \\',
            r'\emph{calibration needs} & \multicolumn{1}{c}{$\Vsrc$} & \multicolumn{1}{c}{$\Vsrc$} & \multicolumn{1}{c}{all} & \multicolumn{1}{c}{all} & \multicolumn{1}{c}{' + f'{lex//1000}k' + r'} & \multicolumn{1}{c}{all rules} \\',
            r'\midrule', r'\multicolumn{7}{@{}l}{\emph{ADE20K, $150\to845$}} \\']
    for name, j in js:
        r = j['alphas']['0.1']['adversarial']
        rows.append(f'{name} & ' + ' & '.join(cell(r.get(a)) for a in ARMS) + r' \\')
    pjs = [(name, load(f'results/adaptive_vocab_pascal_{tag}')) for name, tag, _ in PAS_ADAPT]
    if all(j is not None for _, j in pjs):
        rows += [r'\midrule', r'\multicolumn{7}{@{}l}{\emph{Pascal Context, $59\to458$}} \\']
        for name, j in pjs:
            r = j['alphas']['0.1']['adversarial']
            rows.append(f'{name} & ' + ' & '.join(cell(r.get(a)) if a else '--' for a in PARMS) + r' \\')
    # names a language model lists for each image (table_freeform): no random-names arm; 'rules' is native CRC on those names
    fjs = [(name, load(f'results/freeform_vocab_{tag}')) for name, tag, _ in FREEFORM]
    if all(j is not None for _, j in fjs):
        FARMS = ['anchored, calibrated once', 'native, reused at 150', 'native, recalibrated at 845', None,
                 f'native, recalibrated at a {lex:,}-name lexicon', 'native, matched to the names']
        assert all(FARMS[4] in j['alphas']['0.1'] for name, j in fjs if name != 'CAT-Seg ViT-L'), FARMS[4]
        rows += [r'\midrule', r'\multicolumn{7}{@{}l}{\emph{ADE20K, names from a language model}} \\']
        for name, j in fjs:
            r = j['alphas']['0.1']
            rows.append(f'{name} & ' + ' & '.join(cell(r.get(a)) if a else '--' for a in FARMS) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'adaptive_main.tex').write_text('\n'.join(rows)+'\n')


LX_ARMS = [('anchored, image-level (paper)', 'Img'), ('anchored, label-level', 'Lab'), ('native, full known, label-level', 'Recal'),
           ('native, frozen at source, label-level', 'Frozen'), ('native, frozen at source, image-level', 'FrozenImg')]
LX_DIRS = {'Ade': 'results/label_exchange_ade_vitl_bank683', 'Pas': 'results/label_exchange_pascal_vitl_bank683_schemes',
           'Coc': 'results/label_exchange_coco_vitl_bank683_schemes'}
LX_ORACLE = {'Ade': 'results/label_exchange_ade_vitl_bank683_oracle', 'Pas': 'results/label_exchange_pascal_vitl_bank683_oracle',
             'Coc': 'results/label_exchange_coco_vitl_bank683_oracle'}


def table_label_exchange():
    """Label-level CRC for the added labels (exp_label_exchange.py; CAT-Seg ViT-L, 683-name bank): tables/labelexch.tex (main),
    tables/labelexch_weights.tex (supplement: prevalence-weighted CRC on the dataset split, predicted vs true prevalence) and
    the \\Lx* macros. ADE: the random-source design with a native pass at each of the 10 source sets; Pascal: a fresh random
    source set per trial (no native pass at random sets). Added risk = mean over the added labels present in the calibration
    images (the quantity Proposition 3 bounds)."""
    js = {k: load(v) for k, v in LX_DIRS.items()}
    if any(j is None for j in js.values()): return
    design = {'Ade': 'exchangeable, native frozen', 'Pas': 'exchangeable', 'Coc': 'exchangeable'}
    cell = lambda r: f'{pc(r["added_cal"])} / {f1(r["size"])}' if r else '--'
    dash = '--'
    rows = [r'\begin{tabular}{@{}lcrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{anchored} & \multicolumn{2}{c}{native, label-level} \\', r'\cmidrule(lr){3-4}\cmidrule(l){5-6}',
            r'& & \multicolumn{1}{c}{image-level} & \multicolumn{1}{c}{label-level (ours)} & \multicolumn{1}{c}{recal.\ at grown} & \multicolumn{1}{c}{reused from source} \\',
            r'Source vocabulary & $\alpha$ & \multicolumn{4}{c}{added-label risk (\%) / set size} \\']
    gaps = []
    for part, pname in [('exch', 'random draw'), ('split', "benchmark's own")]:
        rows += [r'\midrule', r'\multicolumn{6}{@{}l}{\emph{' + pname + r'}} \\']
        for ds, dname in [('Ade', r'ADE20K $150\!\to\!845$'), ('Pas', r'Pascal Context $59\!\to\!458$'), ('Coc', r'COCO $171\!\to\!1{,}283$')]:
            for alpha, an, astem in [('0.1', '.10', ''), ('0.05', '.05', 'B')]:
                if part == 'split' and alpha == '0.05': continue
                d = js[ds]['designs'][f'a{alpha}, ' + (design[ds] if part == 'exch' else 'dataset split')]
                rows.append(f'{dname} & {an} & ' + ' & '.join(cell(d.get(a)) for a, _ in LX_ARMS[:4]) + r' \\')
                stem = 'Lx' + ds + ('Split' if part == 'split' else '') + astem
                for a, s in LX_ARMS:
                    if a not in d: continue
                    r = d[a]
                    for k, v in dict(Risk=pc(r['added_cal']), Held=pc(r['added_heldout']), Size=f1(r['size']), Above=pc(r['above_added_cal'], 0),
                                     SrcImg=pc(r['source_image']), SrcClass=pc(r['source_class'])).items():
                        macro(stem + s + k, v)
                    if part == 'exch': gaps.append(abs(r['added_cal']-r['added_heldout']))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch.tex').write_text('\n'.join(rows)+'\n')
    macro('LxHeldGap', f1(100*max(gaps)))
    ade = js['Ade']
    macro('LxAdeSets', num(ade['frozen_sets'])); macro('LxTrials', num(ade['trials'])); macro('LxAdeImages', num(ade['images'])); macro('LxPasImages', num(js['Pas']['images'])); macro('LxCocImages', num(js['Coc']['images']))
    # a fresh random source set per trial on ADE too (anchored and native recalibrated need no native pass at the source set)
    for alpha, astem in [('0.1', ''), ('0.05', 'B')]:
        d = ade['designs'][f'a{alpha}, exchangeable']
        for a, s in LX_ARMS[:3]:
            macro('LxAdeFresh' + astem + s + 'Risk', pc(d[a]['added_cal'])); macro('LxAdeFresh' + astem + s + 'Size', f1(d[a]['size']))
    # Proposition 4 decomposition: source mean loss at the calibrated threshold plus Delta(t) = added minus source mean loss
    dl = {k: load(v + '_delta' if k == 'Ade' else v.replace('_schemes', '_delta')) for k, v in LX_DIRS.items()}
    if all(j is not None for j in dl.values()):
        exch_gaps = []
        for ds, j in dl.items():
            for alpha, astem in [('0.1', ''), ('0.05', 'B')]:
                for a, s in LX_ARMS:
                    r = j['designs'][f'a{alpha}, dataset split'].get(a)
                    if r is None: continue
                    stem = f'LxD{ds}Split{astem}{s}'
                    macro(stem + 'Src', pc(r['source_cal_at_t'])); macro(stem + 'Delta', pc(r['delta_at_t'])); macro(stem + 'DeltaMax', pc(r['delta_max']))
                    if s == 'Lab' and r['delta_at_t'] > 0: macro(stem + 'DeltaRatio', f1(r['delta_max']/r['delta_at_t']))   # worst-case bound over realised excess
                d = j['designs'][f'a{alpha}, ' + design[ds]]
                exch_gaps += [abs(d[a]['delta_at_t']) for a, _ in LX_ARMS[1:3]]
                if 'native, frozen at source, label-level' in d:
                    macro(f'LxD{ds}Exch{astem}FrozenDelta', pc(d['native, frozen at source, label-level']['delta_at_t']))
        macro('LxDExchDeltaMax', pc(max(exch_gaps)))
    # second read of the reserve (docs/PROTOCOL_ADDED_LABEL_RESERVE.md): P1 (exchangeable, anchored label-level) and S1-S6
    rsv = load('results/label_exchange_ade_reserve_vitl_bank683')
    if rsv is not None:
        for alpha, astem in [('0.1', ''), ('0.05', 'B')]:
            for part, pstem in [('exchangeable', ''), ('dataset split', 'Split')]:
                d = rsv['designs'][f'a{alpha}, {part}']
                for a, s in LX_ARMS + [('anchored, weighted, all3', 'WAllThree')]:
                    if a not in d: continue
                    r = d[a]; stem = f'LxRsv{pstem}{astem}{s}'
                    macro(stem + 'Risk', pc(r['added_cal'])); macro(stem + 'Held', pc(r['added_heldout'])); macro(stem + 'Size', f1(r['size']))
                    macro(stem + 'Above', pc(r['above_added_cal'], 0)); macro(stem + 'Src', pc(r['source_cal_at_t'])); macro(stem + 'Delta', pc(r['delta_at_t']))
        chk = Path('results/label_exchange_ade_reserve_vitl_bank683/gt_checks.json')
        if chk.exists(): macro('LxRsvAgree', pc(json.loads(chk.read_text())['C3_agreement']))
    # prevalence-weighted CRC on the dataset split: predicted vs true (annotated) prevalence, every binning scheme
    orc ={k: load(v) for k, v in LX_ORACLE.items()}
    if any(j is None for j in orc.values()): return
    SCH = [('all2', 'all names, 2 bins'), ('all3', 'all names, 3 bins'), ('all5', 'all names, 5 bins'),
           ('src2', 'source names, 2 bins'), ('src3', 'source names, 3 bins'), ('src5', 'source names, 5 bins')]
    wcell = lambda r: f'{pc(r["added_cal"])} / {f1(r["size"])}' + (f' ({pc(r["floor"], 0)})' if r['floor'] > 0 else '')
    rows = [r'\begin{tabular}{@{}llrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{ADE20K $150\!\to\!845$} & \multicolumn{2}{c}{Pascal Context $59\!\to\!458$} \\', r'\cmidrule(lr){3-4}\cmidrule(l){5-6}',
            r'Prevalence bins & weights from & $\alpha=.10$ & $\alpha=.05$ & $\alpha=.10$ & $\alpha=.05$ \\', r'\midrule']
    rows.append(r'unweighted (label-level CRC) & -- & ' + ' & '.join(wcell(orc[ds]['designs'][f'a{al}, dataset split']['anchored, label-level'])
                                                                  for ds in ['Ade', 'Pas'] for al in ['0.1', '0.05']) + r' \\')
    rows.append(r'\midrule')
    for sc, sname in SCH:
        for src, wname, s in [('weighted', 'predicted', 'P'), ('weighted by true prevalence', 'true', 'T')]:
            rows.append(f'{sname} & {wname} & ' + ' & '.join(wcell(orc[ds]['designs'][f'a{al}, dataset split'][f'anchored, {src}, {sc}'])
                                                           for ds in ['Ade', 'Pas'] for al in ['0.1', '0.05']) + r' \\')
            for ds in ['Ade', 'Pas', 'Coc']:
                for al, astem in [('0.1', ''), ('0.05', 'B')]:
                    r = orc[ds]['designs'][f'a{al}, dataset split'][f'anchored, {src}, {sc}']
                    stem = f'LxW{ds}{astem}{s}' + {'all2': 'AllTwo', 'all3': 'AllThree', 'all5': 'AllFive', 'src2': 'SrcTwo', 'src3': 'SrcThree', 'src5': 'SrcFive'}[sc]
                    macro(stem+'Risk', pc(r['added_cal'])); macro(stem+'Size', f1(r['size'])); macro(stem+'Floor', pc(r['floor'], 0))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch_weights.tex').write_text('\n'.join(rows)+'\n')
    rows = [r'\begin{tabular}{@{}llrr@{}}', r'\toprule', r'Prevalence bins & weights from & $\alpha=.10$ & $\alpha=.05$ \\', r'\midrule',
            r'unweighted (label-level CRC) & -- & ' + ' & '.join(wcell(orc['Coc']['designs'][f'a{al}, dataset split']['anchored, label-level'])
                                                                for al in ['0.1', '0.05']) + r' \\', r'\midrule']
    for sc, sname in SCH:
        for src, wname in [('weighted', 'predicted'), ('weighted by true prevalence', 'true')]:
            rows.append(f'{sname} & {wname} & ' + ' & '.join(wcell(orc['Coc']['designs'][f'a{al}, dataset split'][f'anchored, {src}, {sc}'])
                                                           for al in ['0.1', '0.05']) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch_weights_coco.tex').write_text('\n'.join(rows)+'\n')


LX_MODELS = [('CAT-Seg ViT-B', {'ade': 'bank683', 'pascal': 'vitb_bank683', 'coco': 'vitb_bank683'}),
             ('CAT-Seg ViT-L', {'ade': 'vitl_bank683', 'pascal': 'vitl_bank683', 'coco': 'vitl_bank683'}),
             ('CAT-Seg + DeCLIP', {'ade': 'declip_bank683', 'pascal': 'declip_bank683', 'coco': 'declip_bank683'}),
             ('SED', {'ade': 'sed_bank683', 'pascal': 'sed_bank683', 'coco': 'sed_bank683'}),
             ('FC-CLIP', {'ade': 'fcclip_bank683', 'pascal': 'fcclip_bank683', 'coco': 'fcclip_bank683'})]


def table_label_models():
    """Supplement: label-level CRC for the added labels for every model (exp_label_exchange.py on each model's stored scores;
    ViT-L from the runs of table_label_exchange). Random source vocabulary drawn
    afresh per trial; the benchmark's own split at alpha = .10 with the decomposition of Proposition 4."""
    DS = [('ade', 'ADE20K'), ('pascal', 'Pascal Context'), ('coco', 'COCO-Stuff')]
    cell = lambda r: f'{pc(r["added_cal"])} / {f1(r["size"])}'
    rows = [r'\begin{tabular}{@{}llrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{4}{c}{random source vocabulary} & \multicolumn{2}{c}{benchmark\rq{}s own, $\alpha=.10$} \\',
            r'\cmidrule(lr){3-6}\cmidrule(l){7-8}',
            r'& & \multicolumn{2}{c}{$\alpha=.10$} & \multicolumn{2}{c}{$\alpha=.05$} & & \\',
            r'\cmidrule(lr){3-4}\cmidrule(lr){5-6}',
            r'Model & benchmark & anchored & native recal. & anchored & native recal. & anchored & $\Delta(\hat t)$ \\', r'\midrule']
    risks = {'0.1': [], '0.05': []}; held = {'0.1': [], '0.05': []}; above = {'0.1': [], '0.05': []}; n = 0
    heldabove = {'0.1': [], '0.05': []}
    hrows = [r'\begin{tabular}{@{}llrrrrrrrr@{}}', r'\toprule',
             r'& & \multicolumn{4}{c}{$\alpha=.10$} & \multicolumn{4}{c}{$\alpha=.05$} \\', r'\cmidrule(lr){3-6}\cmidrule(l){7-10}',
             r'& & \multicolumn{2}{c}{risk} & \multicolumn{2}{c}{draws $>\alpha$} & \multicolumn{2}{c}{risk} & \multicolumn{2}{c}{draws $>\alpha$} \\',
             r'\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}\cmidrule(l){9-10}',
             r'Model & benchmark & cal. & held-out & cal. & held-out & cal. & held-out & cal. & held-out \\', r'\midrule']
    for name, tags in LX_MODELS:
        for ds, dname in DS:
            if name == 'CAT-Seg ViT-L': j = load({'ade': 'results/label_exchange_ade_vitl_bank683'}.get(ds, f'results/label_exchange_{ds}_vitl_bank683_schemes'))
            else: j = load(f'results/label_exchange_{ds}_{tags[ds]}_schemes')
            if j is None: continue
            d = j['designs']; ex = {al: d[f'a{al}, exchangeable'] for al in ['0.1', '0.05']}; sp = d['a0.1, dataset split']['anchored, label-level']
            if 'delta_at_t' not in sp:                  # ViT-L: the decomposition comes from the later all3-only run (same trials)
                sp = load(f'results/label_exchange_{ds}_vitl_bank683_delta')['designs']['a0.1, dataset split']['anchored, label-level']
            for al in risks:
                risks[al].append(ex[al]['anchored, label-level']['added_cal']); held[al].append(ex[al]['anchored, label-level']['added_heldout'])
                above[al].append(ex[al]['anchored, label-level']['above_added_cal']); heldabove[al].append(ex[al]['anchored, label-level']['above_added_heldout'])
            lab = {al: ex[al]['anchored, label-level'] for al in ['0.1', '0.05']}
            hrows.append(f'{name} & {dname} & ' + ' & '.join(f"{pc(lab[al]['added_cal'])} & {pc(lab[al]['added_heldout'])} & {pc(lab[al]['above_added_cal'], 0)} & "
                                                             f"{pc(lab[al]['above_added_heldout'], 0)}" for al in ['0.1', '0.05']) + r' \\')
            rows.append(f'{name} & {dname} & ' + ' & '.join(cell(ex[al][arm]) for al in ['0.1', '0.05'] for arm in ['anchored, label-level', 'native, full known, label-level'])
                        + f' & {pc(sp["added_cal"])} & {100*sp["delta_at_t"]:.1f} \\\\')
            n += 1
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch_models.tex').write_text('\n'.join(rows)+'\n')
    hrows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch_heldout.tex').write_text('\n'.join(hrows)+'\n')   # supplement: calibration vs held-out images, spread over the draws
    total = len(LX_MODELS)*len(DS)
    macros['LxModelsPending'] = '' if n == total else rf'\textbf{{[Pending: {n} of {total} model--benchmark pairs are complete; the table and ranges are regenerated as the runs finish.]}}'
    if n:
        macro('LxModelsRows', str(n)); macro('LxModelsMaxRisk', pc(max(risks['0.1']))); macro('LxModelsBMaxRisk', pc(max(risks['0.05'])))
        macro('LxModelsMinRisk', pc(min(risks['0.1']))); macro('LxModelsBMinRisk', pc(min(risks['0.05'])))
        macro('LxModelsMaxHeld', pc(max(held['0.1']))); macro('LxModelsBMaxHeld', pc(max(held['0.05'])))         # the same risk on the held-out images
        macro('LxModelsMinAbove', pc(min(above['0.1']), 0)); macro('LxModelsMaxAbove', pc(max(above['0.1']), 0))  # % of trials above alpha
        macro('LxModelsBMinAbove', pc(min(above['0.05']), 0)); macro('LxModelsBMaxAbove', pc(max(above['0.05']), 0))
        macro('LxModelsHeldMinAbove', pc(min(heldabove['0.1']), 0)); macro('LxModelsHeldMaxAbove', pc(max(heldabove['0.1']), 0))
        macro('LxModelsHeldMaxGap', f"{100*max(abs(c-h) for al in risks for c, h in zip(risks[al], held[al])):.2f}")  # calibration vs held-out risk, points


def table_label_images():
    """Supplement: label-level CRC with the image-averaged label loss, the quantity of prop:newimages
    (exp_label_exchange_images.py: the exchangeable design of exp_label_exchange.py replayed, same draws). The pooled
    columns of each run are checked against the frozen runs of table_label_models (\\LxImgReplayDiff, points)."""
    DS = [('ade', 'ADE20K'), ('pascal', 'Pascal Context'), ('coco', 'COCO-Stuff')]
    rows = [r'\begin{tabular}{@{}llrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{3}{c}{$\alpha=.10$} & \multicolumn{3}{c}{$\alpha=.05$} \\', r'\cmidrule(lr){3-5}\cmidrule(l){6-8}',
            r'Model & benchmark & cal. & held-out & draws $>\alpha$ & cal. & held-out & draws $>\alpha$ \\', r'\midrule']
    held = {'0.1': [], '0.05': []}; above = {'0.1': [], '0.05': []}; gap, diff, n = [], [], 0
    for name, tags in LX_MODELS:
        for ds, dname in DS:
            j = load(f'results/label_exchange_images_{ds}_{tags[ds]}')
            if j is None: continue
            ref = load({'ade': 'results/label_exchange_ade_vitl_bank683'}.get(ds, f'results/label_exchange_{ds}_vitl_bank683_schemes')
                       if name == 'CAT-Seg ViT-L' else f'results/label_exchange_{ds}_{tags[ds]}_schemes')
            cells = []
            for al in ['0.1', '0.05']:
                r = j['alphas'][al]['images']; p = j['alphas'][al]['pooled']
                held[al].append(r['added_heldout']); above[al].append(r['above_added_heldout']); gap.append(abs(r['added_cal']-r['added_heldout']))
                if ref is not None:
                    f = ref['designs'][f'a{al}, exchangeable']['anchored, label-level']
                    diff.append(max(abs(p['added_cal']-f['added_cal']), abs(p['added_heldout']-f['added_heldout'])))
                cells.append(f"{pc(r['added_cal'])} & {pc(r['added_heldout'])} & {pc(r['above_added_heldout'], 0)}")
            rows.append(f'{name} & {dname} & ' + ' & '.join(cells) + r' \\')
            n += 1
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelexch_images.tex').write_text('\n'.join(rows)+'\n')
    total = len(LX_MODELS)*len(DS)
    macros['LxImgPending'] = '' if n == total else rf'\textbf{{[Pending: {n} of {total} model--benchmark pairs are complete.]}}'
    if n:
        macro('LxImgMinHeld', pc(min(held['0.1']))); macro('LxImgMaxHeld', pc(max(held['0.1'])))
        macro('LxImgBMinHeld', pc(min(held['0.05']))); macro('LxImgBMaxHeld', pc(max(held['0.05'])))
        macro('LxImgMinAbove', pc(min(above['0.1']), 0)); macro('LxImgMaxAbove', pc(max(above['0.1']), 0))
        macro('LxImgBMinAbove', pc(min(above['0.05']), 0)); macro('LxImgBMaxAbove', pc(max(above['0.05']), 0))
        macro('LxImgMaxGap', f'{100*max(gap):.2f}'); macro('LxImgReplayDiff', f'{100*max(diff):.0e}' if diff else '--')


LS_WORD = {10: 'Ten', 20: 'Twenty', 30: 'Thirty', 50: 'Fifty', 75: 'SeventyFive', 100: 'Hundred', 150: 'OneFifty', 200: 'TwoHundred'}
LS_MODEL = {'CAT-Seg ViT-B': 'VitB', 'CAT-Seg ViT-L': 'VitL', 'CAT-Seg + DeCLIP': 'Declip', 'SED': 'Sed', 'FC-CLIP': 'Fcclip'}


def table_label_sample():
    """Supplement: the added-label guarantee from m randomly drawn, annotated added names, with the benchmark's own source
    classes (exp_label_sample.py): tables/labelsample.tex and \\Ls<benchmark><model>... macros for every run present. The
    replay arms of each run are checked against exp_label_exchange.py's results (\\LsReplayDiff, points)."""
    DS = [('ade', 'ADE20K', 'Ade'), ('pascal', 'Pascal Context', 'Pas'), ('coco', 'COCO-Stuff', 'Coc')]
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lrrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{4}{c}{$\alpha=.10$} & \multicolumn{2}{c}{$\alpha=.05$} \\ \cmidrule(lr){3-6}\cmidrule(l){7-8}',
            r"Calibration labels & $m'$ & risk & draws $>\alpha$ & size & native & risk & size \\"]
    diff, n = [], 0
    for name, tags in LX_MODELS:
        for ds, dname, dpre in DS:
            j = load(f'results/label_sample_{ds}_{tags[ds]}')
            if j is None: continue
            n += 1; pre = f'Ls{dpre}{LS_MODEL[name]}'
            diff += [v for c in j.get('checks', {}).values() for k, v in c.items() if k != 'size']
            r = lambda al, key: j['arms'][f'a{al}, {key}']
            rows += [r'\midrule', rf'\multicolumn{{8}}{{@{{}}l}}{{\emph{{{name}, {dname}}}}} \\']
            ref = [('benchmark source classes', 'source classes (benchmark split), per-label'), ('random source vocabulary', 'check: random S of T')]
            for label, key in ref:
                a, b = r(0.1, key), r(0.05, key)
                rows.append(rf"{label} & {a['m_present']:.0f} & {pc(a['added_cal'])} & {pc(a['above_added_cal'], 0)} & {f1(a['size'])} & -- & {pc(b['added_cal'])} & {f1(b['size'])} \\")
            s = r(0.1, 'source classes (benchmark split), per-label')
            macro(f'{pre}SplitRisk', pc(s['added_cal'])); macro(f'{pre}SplitSize', f1(s['size']))
            s = r(0.1, 'check: random S of T')
            macro(f'{pre}RandRisk', pc(s['added_cal'])); macro(f'{pre}RandSize', f1(s['size']))
            macro(f'{pre}MaxRisk', pc(max(r(0.1, f'anchored, m={m}')['added_cal'] for m in j['ms'])))
            macro(f'{pre}BMaxRisk', pc(max(r(0.05, f'anchored, m={m}')['added_cal'] for m in j['ms'])))
            for m in j['ms']:
                a, b, na = r(0.1, f'anchored, m={m}'), r(0.05, f'anchored, m={m}'), r(0.1, f'native at grown vocabulary, m={m}')
                rows.append(rf"$m={m}$ random added names & {a['m_present']:.0f} & {pc(a['added_cal'])} & {pc(a['above_added_cal'], 0)} & "
                            rf"{f1(a['size'])} & {f1(na['size'])} & {pc(b['added_cal'])} & {f1(b['size'])} \\")
                w = LS_WORD[m]
                macro(f'{pre}M{w}Risk', pc(a['added_cal'])); macro(f'{pre}M{w}Held', pc(a['added_heldout'])); macro(f'{pre}M{w}Size', f1(a['size']))
                macro(f'{pre}M{w}NatSize', f1(na['size'])); macro(f'{pre}M{w}Floor', pc(a['floor'], 0)); macro(f'{pre}M{w}Present', f"{a['m_present']:.0f}")
                macro(f'{pre}M{w}Above', pc(a['above_added_cal'], 0)); macro(f'{pre}M{w}SrcRisk', pc(a['source_image']))
                macro(f'{pre}BM{w}Risk', pc(b['added_cal'])); macro(f'{pre}BM{w}Size', f1(b['size'])); macro(f'{pre}BM{w}Floor', pc(b['floor'], 0))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'labelsample.tex').write_text('\n'.join(rows)+'\n'); write_parts('labelsample', rows, 4, 2)
    macros['LsPending'] = '' if n else r'\textbf{[Pending: no run of exp\_label\_sample.py.]}'
    macro('LsReplayDiff', ('0' if max(diff) == 0 else f'{100*max(diff):.0e}') if diff else '--')


NR_MODELS = [('CAT-Seg ViT-L', 'vitl_bank683', 'VitL'), ('SED', 'sed_bank683', 'Sed')]


def table_native_refs():
    """Supplement: native references for calibration reuse on ADE20K (exp_native_baselines.py): the native model's own
    set size at the source vocabulary, native reuse with the alpha' that meets alpha at the grown vocabulary (chosen on
    the evaluation images, an oracle), and how often the native top-1 label falls outside the anchored set.
    tables/nativerefs.tex and \\Nr<model>... macros (B: alpha = .05)."""
    rows = [r'\setlength{\tabcolsep}{3pt}\begin{tabular}{@{}llrrrrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{size at $150$} & reused & \multicolumn{3}{c}{reused at $\alpha^\prime$} & recal. & anchored & top-1 \\'
            r' \cmidrule(lr){3-4}\cmidrule(lr){6-8}',
            r'Model & $\alpha$ & native & anch. & risk & $\alpha^\prime$ & risk & size & size & size & outside \\', r'\midrule']
    n = 0
    for name, tag, pre in NR_MODELS:
        j = load(f'results/native_baselines_ade_{tag}')
        if j is None: continue
        n += 1
        for al in [.1, .05]:
            arm = lambda k: j['arms'][f'a{al}, {k}']
            an, ns, nr, nc = arm('anchored, calibrated at V0'), arm('native at V0 (calibrated and deployed at V0)'), \
                arm('native reused (V0 threshold at the grown vocabulary)'), arm('native recalibrated at the grown vocabulary')
            tp, n5 = j['tightened'][f'a{al}'], j['n5'][f'a{al}']
            rows.append(rf"{name if al == .1 else ''} & ${al:.2f}$ & {f2(ns['size_v0'])} & {f2(an['size_v0'])} & {pc(nr['risk'])} & "
                        rf"{pc(tp['alpha_prime'], 2)} & {pc(tp['risk'])} & {f2(tp['size_full'])} & {f2(nc['size_full'])} & {f2(an['size_full'])} & "
                        rf"{pc(n5['outside_all'], 2)} \\")
            b = '' if al == .1 else 'B'
            macro(f'Nr{pre}{b}NatSrcSize', f2(ns['size_v0'])); macro(f'Nr{pre}{b}AnchSrcSize', f2(an['size_v0']))
            macro(f'Nr{pre}{b}AlphaPrime', pc(tp['alpha_prime'], 2)); macro(f'Nr{pre}{b}TightSize', f2(tp['size_full']))
            macro(f'Nr{pre}{b}TightRisk', pc(tp['risk'])); macro(f'Nr{pre}{b}RecalSize', f2(nc['size_full']))
            macro(f'Nr{pre}{b}AnchSize', f2(an['size_full'])); macro(f'Nr{pre}{b}ReusedRisk', pc(nr['risk']))
            macro(f'Nr{pre}{b}Outside', pc(n5['outside_all'], 2)); macro(f'Nr{pre}{b}OutsideCorrect', pc(n5['outside_when_native_correct'], 2))
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'nativerefs.tex').write_text('\n'.join(rows)+'\n')
    macros['NrPending'] = '' if n else r'\textbf{[Pending: no run of exp\_native\_baselines.py.]}'


EPS_WORD = {0: 'Zero', 0.05: 'Five', 0.1: 'Ten', 0.25: 'TwentyFive', 0.5: 'Fifty', 1: 'Hundred'}


def table_label_hardness():
    """Supplement: added-label risk at the label-level threshold when the added names are the easiest ... hardest fifth by
    held-out loss, and under contamination with the hardest fifth (exp_label_hardness.py; prop:shift). ADE20K, alpha = .10
    in tables/hardness.tex; \\Hd<model>... macros (B: alpha = .05)."""
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lrrrrrrrr@{}}', r'\toprule',
            r'& \multicolumn{4}{c}{CAT-Seg ViT-L} & \multicolumn{4}{c}{SED} \\ \cmidrule(lr){2-5}\cmidrule(l){6-9}',
            r'Added names & held-out & risk & $\alpha+\Delta(\hat t_\ell)$ & $\alpha+\max\Delta$ & held-out & risk & $\alpha+\Delta(\hat t_\ell)$ & $\alpha+\max\Delta$ \\', r'\midrule']
    js = [load(f'results/label_hardness_ade_{tag}') for _, tag, _ in NR_MODELS]
    if not all(js):
        macros['HdPending'] = r'\textbf{[Pending: no run of exp\_label\_hardness.py.]}'
        return
    macros['HdPending'] = ''
    for (_, _, pre), j in zip(NR_MODELS, js):
        macro('HdTrials', num(j['trials']))
        for al in [.1, .05]:
            b = '' if al == .1 else 'B'; f = lambda k: j['fifths'][f'a{al}, {k}']
            macro(f'Hd{pre}{b}PRisk', pc(f('Q_all')['p_risk']))
            for k, w in [('Q_all', 'All'), ('Q4', 'Four'), ('Q5', 'Five')]:
                macro(f'Hd{pre}{b}Q{w}Risk', pc(f(k)['realised'])); macro(f'Hd{pre}{b}Q{w}Hard', pc(f(k)['hardness']))
                macro(f'Hd{pre}{b}Q{w}Bound', pc(al+f(k)['max_delta'])); macro(f'Hd{pre}{b}Q{w}Above', pc(f(k)['frac_trials_above_alpha'], 0))
            for e, w in EPS_WORD.items():
                macro(f'Hd{pre}{b}Eps{w}Risk', pc(j['contamination'][f'a{al}, eps={e}']['realised']))
    # largest held-out loss of the three easiest fifths over both models, rounded up to 0.01 points (caption bound)
    macro('HdFirstThreeMaxHard', f'{math.ceil(10000*max(j["fifths"][f"a0.1, Q{k}"]["hardness"] for j in js for k in (1, 2, 3))-1e-9)/100:.2f}')
    labels = [(f'Q{k}', f'fifth {k}' + (' (easiest)' if k == 1 else ' (hardest)' if k == 5 else '')) for k in range(1, 6)] + [('Q_all', 'all remaining')]
    for k, lab in labels:
        cells = []
        for j in js:
            v = j['fifths'][f'a0.1, {k}']
            cells += [pc(v['hardness']), pc(v['realised']), pc(.1+v['delta_at_t']), pc(.1+v['max_delta'])]
        rows.append((r'\midrule ' if k == 'Q_all' else '') + f'{lab} & ' + ' & '.join(cells) + r' \\')
    rows += [r'\midrule', r'\multicolumn{9}{@{}l}{\emph{$(1-\varepsilon)$ uniform draw $+\ \varepsilon$ hardest fifth: risk, and the bound $\alpha+\varepsilon$}} \\']
    for e in [0.05, 0.1, 0.25, 0.5]:
        cells = []
        for j in js:
            cells += ['', pc(j['contamination'][f'a0.1, eps={e}']['realised']), pc(.1+e, 0), '']
        rows.append(rf'$\varepsilon={e:g}$ & ' + ' & '.join(cells) + r' \\')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/'hardness.tex').write_text('\n'.join(rows)+'\n')


OVD = [('gdino_t', 'Grounding DINO T', 'OvdGdT'), ('mmgdino_t', 'MM-Grounding DINO T', 'OvdMmT'),
       ('gdino_b', 'Grounding DINO B', 'OvdGdB'), ('owlv2', 'OWLv2 B (control)', 'OvdOwl')]


def table_ovd():
    """Detection, COCO 80 -> LVIS 1,204 (exp_ovd_crc.py; docs/OVD_DETECTION_BENCHMARK.md): tables/ovd.tex (main text,
    alpha = .10, LVIS scale), tables/ovd_full.tex (supplement: both growth regimes, bank B, both alphas, label level) and
    \\Ovd* macros. Rows appear as the runs land."""
    cell = lambda d, v: f'{pc(d["risk"])}/{f1(d["size"][v])}'
    main = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lrrr@{}}', r'\toprule',
            r'& \multicolumn{2}{c}{native} & \multicolumn{1}{c}{anchored} \\ \cmidrule(lr){2-3}\cmidrule(l){4-4}',
            r'Detector & \multicolumn{1}{c}{reused} & \multicolumn{1}{c}{recal.} & \multicolumn{1}{c}{once} \\', r'\midrule']
    full = [r'\setlength{\tabcolsep}{3pt}\begin{tabular}{@{}llrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{3}{c}{$\alpha=.10$} & \multicolumn{3}{c}{$\alpha=.05$} \\ \cmidrule(lr){3-5}\cmidrule(l){6-8}',
            r'Detector & arm & risk & size, one prompt & size, LVIS & risk & size, one prompt & size, LVIS \\', r'\midrule']
    n = 0
    for m, name, pre in OVD:
        j = load(f'results/ovd_crc_{m}')
        if j is None: continue
        n += 1
        a, b = j['image_level']['0.1'], j['image_level']['0.05']
        if m == 'owlv2':
            o = a['OWLv2']; lx = j['label_level']['owl']['exchangeable']['0.1']['images']
            main.append(f'{name} & {cell(o, "LVIS")} & -- & -- \\\\')
            macro(pre+'Risk', pc(o['risk'])); macro(pre+'Size', f1(o['size']['LVIS'])); macro(pre+'AddedHeld', pc(lx['added_heldout']))
            fl = load(f'results/ovd_floor_{m}')
            if fl is not None:
                f = fl['stores']['owl']; tv = f['trivial_threshold']
                macro(pre+'UnlocSrc', pc(f['unlocalised_source'])); macro(pre+'UnlocAdded', pc(f['unlocalised_added']))
                macro(pre+'TrivialImages', pc(tv['exchangeable, 0.1, images'], 0)); macro(pre+'BTrivialImages', pc(tv['exchangeable, 0.05, images'], 0))
            full.append(f'{name} & reused & {pc(o["risk"])} & -- & {f1(o["size"]["LVIS"])} & {pc(b["OWLv2"]["risk"])} & -- & {f1(b["OWLv2"]["size"]["LVIS"])} \\\\')
            continue
        lx = j['label_level']['anch_a']['exchangeable']['0.1']['images']
        main.append(f'{name} & {cell(a["native reused, LVIS"], "LVIS")} & {cell(a["native recal., LVIS"], "LVIS")} & '
                    f'{cell(a["anchored A"], "LVIS")} \\\\')
        ARMS = [('native, source', 'native, source', 'Src'), ('native reused', 'native reused, {}', 'Reuse'), ('native recal.', 'native recal., {}', 'Recal'),
                ('anchored, bank A', 'anchored A', 'AnchA'), ('anchored, bank B', 'anchored B', 'AnchB')]
        for k, (label, arm, stem) in enumerate(ARMS):
            cells = []
            for al, r in [('', a), ('B', b)]:
                if '{}' in arm:
                    one, lv = r[arm.format('one prompt')], r[arm.format('LVIS')]
                    cells.append(f'{pc(one["risk"])}, {pc(lv["risk"])} & {f1(one["size"]["one prompt"])} & {f1(lv["size"]["LVIS"])}')
                    macro(pre+al+stem+'OneRisk', pc(one['risk'])); macro(pre+al+stem+'Risk', pc(lv['risk']))
                    macro(pre+al+stem+'Above', pc(lv['above'], 0)); macro(pre+al+stem+'Size', f1(lv['size']['LVIS'])); macro(pre+al+stem+'OneSize', f1(one['size']['one prompt']))
                else:
                    d = r[arm]; sz = d['size']
                    cells.append(f'{pc(d["risk"])} & {f1(sz["one prompt"]) if "one prompt" in sz else "--"} & {f1(sz["LVIS"]) if "LVIS" in sz else "--"}')
                    macro(pre+al+stem+'Risk', pc(d['risk'])); macro(pre+al+stem+'Above', pc(d['above'], 0)); macro(pre+al+stem+'SrcSize', f1(sz['source']))
                    if 'LVIS' in sz: macro(pre+al+stem+'Size', f1(sz['LVIS'])); macro(pre+al+stem+'OneSize', f1(sz['one prompt']))
            full.append(f'{name if k == 0 else ""} & {label} & ' + ' & '.join(cells) + r' \\')
        full.append(r'\midrule')
        for store, sst in [('anch_a', 'Anch'), ('native_lvis', 'Native')]:
            for design, dst in [('exchangeable', 'Exch'), ('benchmark split', 'Bench')]:
                for al, ast in [('0.1', ''), ('0.05', 'B')]:
                    d = j['label_level'][store][design][al]['images']
                    macro(f'{pre}{ast}Lx{sst}{dst}Cal', pc(d['added_cal'])); macro(f'{pre}{ast}Lx{sst}{dst}Held', pc(d['added_heldout']))
                    macro(f'{pre}{ast}Lx{sst}{dst}Above', pc(d['above_heldout'], 0)); macro(f'{pre}{ast}Lx{sst}{dst}Delta', pc(d['delta_at_t']))
        fl = load(f'results/ovd_floor_{m}')
        if fl is not None:
            for store, sst in [('anch_a', 'Anch'), ('native_lvis', 'Native')]:
                f = fl['stores'][store]; tv = f['trivial_threshold']
                macro(pre+sst+'UnlocSrc', pc(f['unlocalised_source'])); macro(pre+sst+'UnlocAdded', pc(f['unlocalised_added']))
                macro(pre+sst+'TrivialImages', pc(tv['exchangeable, 0.1, images'], 0)); macro(pre+sst+'TrivialPooled', pc(tv['exchangeable, 0.1, pooled'], 0))
                macro(pre+'B'+sst+'TrivialImages', pc(tv['exchangeable, 0.05, images'], 0))
            macro(pre+'LabelsPresent', num(fl['labels_present']))
        macro(pre+'Images', num(j['images'])); macro(pre+'Boxes', num(j['source_boxes'])); macro(pre+'OneLabels', num(j['one_prompt_labels']))
        # exactness check of the anchored detector (exp_ovd_probe.py --check, 5 images): largest box-logit change under candidate order and subset
        ck = Path(f'results/ovd_probe_{m}/check.json')
        if ck.exists():
            mx = max(max(r['anchored_order_invariance_max_abs'], r['anchored_subset_invariance_max_abs']) for r in json.loads(ck.read_text()).values())
            mant, ex = f'{mx:.1e}'.split('e'); macro(pre+'CheckMax', f'{mant}\\times10^{{{int(ex)}}}')
    main += [r'\bottomrule', r'\end{tabular}']; full[-1:] = [r'\bottomrule', r'\end{tabular}'] if n and full[-1] == r'\midrule' else full[-1:] + [r'\bottomrule', r'\end{tabular}']
    (TAB/'ovd.tex').write_text('\n'.join(main)+'\n'); (TAB/'ovd_full.tex').write_text('\n'.join(full)+'\n')
    macros['OvdPending'] = '' if n == len(OVD) else rf'\textbf{{[Pending: {n} of {len(OVD)} detectors are complete.]}}'


def table_ovd_accuracy():
    """Supplement: box-level accuracy at 1,204 names (exp_ovd_accuracy.py), the detection counterpart of tab:pixacc:
    tables/ovd_acc.tex and \\OvdAcc* macros (top-1 %, ties against the true label, unlocalised boxes wrong)."""
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}llrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{2}{c}{COCO boxes} & \multicolumn{4}{c}{LVIS (added) boxes} \\ \cmidrule(lr){3-4}\cmidrule(l){5-8}',
            r'Detector & scoring & top-1 & class mean & localised & top-1 & top-1 $\mid$ loc. & class mean \\', r'\midrule']
    ARMS = [('native_lvis', 'native, chunks of 40', 'Native'), ('anch_a', 'anchored, bank A', 'AnchA'), ('anch_b', 'anchored, bank B', 'AnchB'),
            ('owl', 'native', 'Owl')]
    gd = {'Native': [], 'AnchA': [], 'NativeLoc': [], 'AnchALoc': [], 'NativeSrc': [], 'AnchASrc': [], 'AnchBSrc': [],
          'NativeAll': [], 'AnchAAll': []}
    n, rise = 0, []
    for m, name, pre in OVD:
        j = load(f'results/ovd_accuracy_{m}')
        if j is None: continue
        n += 1; first = True
        for store, label, stem in ARMS:
            if store not in j['stores']: continue
            s, d = j['stores'][store]['source'], j['stores'][store]['added']
            rows.append(f'{name if first else ""} & {label} & {pc(s["top1"])} & {pc(s["class_mean_top1"])} & {pc(d["localised"])} & '
                        f'{pc(d["top1"])} & {pc(d["top1_given_localised"])} & {pc(d["class_mean_top1"])} \\\\')
            first = False
            p = pre+'Acc'+stem
            macro(p+'SrcTop', pc(s['top1'])); macro(p+'AddTop', pc(d['top1'])); macro(p+'AddLocTop', pc(d['top1_given_localised']))
            macro(p+'AddClassTop', pc(d['class_mean_top1'])); macro(p+'SrcClassTop', pc(s['class_mean_top1']))
            if stem == 'AnchB': gd['AnchBSrc'].append(s['top1'])
            if stem in ('Native', 'AnchA'):
                gd[stem].append(d['top1']); gd[stem+'Loc'].append(d['top1_given_localised']); gd[stem+'Src'].append(s['top1'])
                # all boxes (COCO + added), pooled over boxes
                gd[stem+'All'].append((s['top1']*s['boxes']+d['top1']*d['boxes'])/(s['boxes']+d['boxes']))
        if 'native_lvis' in j['stores'] and 'anch_a' in j['stores']:
            rise.append(gd['AnchAAll'][-1] > gd['NativeAll'][-1])
        rows.append(r'\midrule')
        macro('OvdAccAddedBoxes', num(j['stores'][next(iter(j['stores']))]['added']['boxes']))
        macro('OvdAccAddedLabels', num(j['stores'][next(iter(j['stores']))]['added']['labels']))
    rows[-1:] = [r'\bottomrule', r'\end{tabular}'] if n and rows[-1] == r'\midrule' else rows[-1:] + [r'\bottomrule', r'\end{tabular}']
    (TAB/'ovd_acc.tex').write_text('\n'.join(rows)+'\n')
    for k, v in gd.items():
        if v: macro(f'OvdAcc{k}Lo', pc(min(v))); macro(f'OvdAcc{k}Hi', pc(max(v)))
    if rise:
        words = {0: 'none', 1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        macro('OvdAccAllRiseCount', words[sum(rise)]); macro('OvdAccAllDetectors', words[len(rise)])


def table_seg_added():
    """Supplement: pixel accuracy split into source and added classes (exp_seg_added_accuracy.py, from the stored
    full-resolution confusion matrices): tables/pixacc_added.tex and \SegAdd* macros. Changes are computed before rounding."""
    j = load('results/seg_added_accuracy')
    if j is None: return
    DS = [('ade847', 'A-847', 'AdeEightFortySeven'), ('pc459', 'PC-459', 'PcFourFiftyNine')]
    LANES = [('vitb', 'CAT-Seg ViT-B'), ('vitl', 'CAT-Seg ViT-L'), ('declip', 'CAT-Seg + DeCLIP EVA-L'), ('sed', 'SED ConvNeXt-L'), ('fcclip', 'FC-CLIP ConvNeXt-L')]
    ARM_NAMES = {'native': 'native (released)', 'anchored_coco171': 'anchored, COCO-171 bank', 'anchored_bank683': 'anchored, 683-name bank',
                 'anchored_133': 'anchored, 133-name bank'}
    head = ' & '.join(rf'\multicolumn{{4}}{{c}}{{{n} (${j["datasets"][d]["source_classes"]}$ source, ${j["datasets"][d]["added_classes"]}$ added)}}' for d, n, _ in DS)
    rows = [r'\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}ll' + 'r'*8 + '@{}}', r'\toprule', '& & ' + head + r' \\ \cmidrule(lr){3-6}\cmidrule(l){7-10}',
            r'Model & scoring & ' + ' & '.join(['source & added & class mean & mIoU']*2) + r' \\', r'\midrule']
    for lane, lname in LANES:
        arms = list(j['datasets']['ade847']['lanes'][lane])
        for arm in arms:
            cells = []; armname = re.sub(r'[^A-Za-z]', '', arm.title())
            for ds, _, dsname in DS:
                v = j['datasets'][ds]['lanes'][lane][arm]; s, a = v['source'], v['added']
                vals = [s['pixel_accuracy'], a['pixel_accuracy'], a['class_mean_accuracy'], a['miou']]
                cells += [pc(x) for x in vals]
                for suf, x in zip(['Src', 'Add', 'AddCls', 'AddMiou'], vals): macro('SegAdd'+lane.title()+armname+dsname+suf, pc(x))
            name = ARM_NAMES.get(arm, arm.replace('_', ' '))
            if lane == 'fcclip' and arm == 'anchored_bank683': name = 'anchored, 701-name bank'
            rows.append(f'{lname if arm == arms[0] else ""} & {name} & ' + ' & '.join(cells) + r' \\')
        rows.append(r'\midrule')
    rows[-1] = r'\bottomrule'; rows.append(r'\end{tabular}')
    (TAB/'pixacc_added.tex').write_text('\n'.join(rows)+'\n')
    for ds, _, dsname in DS:
        d = j['datasets'][ds]; a0 = d['lanes']['vitb']['native']['added']
        macro('SegAddClasses'+dsname, num(d['added_classes'])); macro('SegAddPresent'+dsname, num(a0['classes_present']))
        macro('SegAddShare'+dsname, pc(a0['pixel_share']))
    # cost-volume models (CAT-Seg, SED): change of added-class pixel accuracy, anchored minus native, over both benchmarks
    def change(arm):
        return [j['datasets'][ds]['lanes'][l][arm]['added']['pixel_accuracy']-j['datasets'][ds]['lanes'][l]['native']['added']['pixel_accuracy']
                for ds, _, _ in DS for l in ['vitb', 'vitl', 'declip', 'sed']]
    macro('SegAddPixMaxAbsChange', pc(max(abs(x) for x in change('anchored_bank683'))))
    g = change('anchored_coco171'); macro('SegAddPixCocoGainLo', pc(min(g))); macro('SegAddPixCocoGainHi', pc(max(g)))


PN = [('ade', 'vitl', 'ADE20K', 'CAT-Seg ViT-L', 'AdeVitL'), ('ade', 'sed', 'ADE20K', 'SED', 'AdeSed'), ('ade', 'fcclip', 'ADE20K', 'FC-CLIP', 'AdeFc'),
      ('pascal', 'vitl', 'Pascal Context', 'CAT-Seg ViT-L', 'PasVitL'), ('pascal', 'sed', 'Pascal Context', 'SED', 'PasSed'),
      ('coco', 'sed', 'COCO-Stuff', 'SED', 'CocSed')]


def table_per_name():
    """Supplement: per-name thresholds on the anchored scores against the image-level one, and the hybrid that keeps both
    guarantees (exp_per_name.py): tables/pername.tex and \\Pn* macros (suffix B: alpha = 5%)."""
    J = {st: load(f'results/per_name_{ds}_{m}_bank683') for ds, m, _, _, st in PN}
    if any(v is None for v in J.values()): return
    rows = [r'\begin{tabular}{@{}lll' + 'r'*9 + '@{}}', r'\toprule',
            r'& & & & \multicolumn{2}{c}{image-level} & \multicolumn{2}{c}{per-name} & \multicolumn{3}{c}{lower of both} & native, reused \\',
            r'\cmidrule(lr){5-6}\cmidrule(lr){7-8}\cmidrule(lr){9-11}\cmidrule(l){12-12}',
            r'$\alpha$ & Benchmark & Model & calibrated & over $\alpha$ & size & over $\alpha$ & size & image risk & over $\alpha$ & size & over $\alpha$ \\',
            r'\midrule']
    ratio, ratio_h, hyb_risk = {}, {}, {}
    for ai, (al, suf) in enumerate([('0.1', ''), ('0.05', 'B')]):
        for i, (ds, m, bench, model, st) in enumerate(PN):
            j = J[st]; A = lambda arm: j['arms'][f'a{al}, {arm}']
            pn, il, ila, hy, hyc, nat = (A('anchored, per-name'), A('anchored, image-level, per-name names'), A('anchored, image-level, all names'),
                                         A('hybrid, lower of both'), A('hybrid, lower of both (calibrated names)'), A('native, per-name, source->grown'))
            nat_cell = f'{nat["over"]} of {nat["estimated"]}'
            first = r'\multirow{6}{*}{$' + ('10' if al == '0.1' else '5') + r'\%$}' if i == 0 else ''
            rows.append(f'{first} & {bench} & {model} & {pn["calibrated"]:.0f} of {num(j["names_present"])} & {il["over"]} & {f2(ila["size"])} & '
                        f'{pn["over"]} & {f2(pn["size"])} & {pc(hy["image_risk"])} & {hyc["over"]} & {f2(hy["size"])} & {nat_cell}' + r' \\')
            macro('PnCal'+st+suf, f'{pn["calibrated"]:.0f}'); macro('PnImgOver'+st+suf, str(il['over'])); macro('PnNatOver'+st+suf, str(nat['over']))
            macro('PnNatEst'+st+suf, str(nat['estimated'])); macro('PnHybRisk'+st+suf, pc(hy['image_risk']))
            macro('PnSize'+st+suf, f2(pn['size'])); macro('PnHybSize'+st+suf, f2(hy['size'])); macro('PnImgSize'+st+suf, f2(ila['size']))
            assert pn['over'] == 0 and hyc['over'] == 0, (st, al)
            ratio[st, al] = pn['size']/ila['size']; ratio_h[st, al] = hy['size']/ila['size']; hyb_risk[st, al] = hy['image_risk']
            assert A('anchored, per-name, 20 images')['over'] == 0, (st, al)
            if al == '0.1': macro('PnPresent'+st, num(j['names_present']))
        rows.append(r'\midrule' if ai == 0 else r'\bottomrule')
    rows.append(r'\end{tabular}')
    (TAB/'pername.tex').write_text('\n'.join(rows)+'\n')
    for al, suf in [('0.1', ''), ('0.05', 'B')]:
        r = [v for (s, a), v in ratio.items() if a == al]; rh = [v for (s, a), v in ratio_h.items() if a == al]
        macro('PnSizeRatioLo'+suf, f1(min(r))); macro('PnSizeRatioHi'+suf, f1(max(r)))
        macro('PnHybRatioLo'+suf, f1(min(rh))); macro('PnHybRatioHi'+suf, f1(max(rh)))
        macro('PnHybRiskHi'+suf, pc(max(v for (s, a), v in hyb_risk.items() if a == al)))


SSD = [('vitl683', 'ADE20K', 'CAT-Seg ViT-L'), ('sed683', 'ADE20K', 'SED'), ('pascalvitl683', 'Pascal Context', 'CAT-Seg ViT-L'),
       ('pascalsed683', 'Pascal Context', 'SED'), ('cocosed683', 'COCO-Stuff', 'SED')]
SSD_ARMS = [('catseg_native_source', 'native at source'), ('catseg_native_frozen_full', 'native, reused'),
            ('catseg_native_replay_full', 'native, recalibrated'), ('catseg_anchored', 'anchored')]


def table_setsize(alpha=ALPHA, filename='setsize.tex'):
    """Supplement: distribution of the per-pixel set size at the grown vocabulary (exp_set_size_dist.py), on the splits and
    thresholds of Tab. 1, for the configurations whose stored scores were available locally. Macros \\Ssd<stem><Arm><stat>."""
    rows = [r'\begin{tabular}{@{}llrrrrrrrr@{}}', r'\toprule',
            r'& & & \multicolumn{5}{c}{pixels with $|C|$ (\%)} & \multicolumn{2}{c}{labels per pixel} \\', r'\cmidrule(lr){4-8}\cmidrule(l){9-10}',
            r'Configuration & threshold & names & $=0$ & $=1$ & $\le 3$ & $\le 10$ & $>10$ & median & mean \\', r'\midrule']
    n = 0
    for key, ds, model in SSD:
        dset, tag, *_ = CONFIGS[key]; stem = CONFIGS[key][5]
        j = load(f'results/set_size_dist_{dset}_{tag}')
        if j is None: continue
        n += 1
        d = j['designs'][f"cal{j['n_cal']}_{alpha}"]
        for i, (arm, label) in enumerate(SSD_ARMS):
            s = d[arm]; names = j['source'] if arm == 'catseg_native_source' else j['total']
            rows.append((f'{ds}, {model}' if i == 0 else '') + f' & {label} & {num(names)} & {pc(s["frac_empty"])} & {pc(s["frac_one"])} & {pc(s["frac_le3"])} & '
                        f'{pc(s["frac_le10"])} & {pc(s["frac_gt10"])} & {s["median_of_mean_dist"]} & {f2(s["mean"])} \\\\')
            if alpha == ALPHA:
                a = {'catseg_native_source': 'Src', 'catseg_native_frozen_full': 'Reused', 'catseg_native_replay_full': 'Recal', 'catseg_anchored': 'Anch'}[arm]
                macro(f'Ssd{stem}{a}One', pc(s['frac_one'])); macro(f'Ssd{stem}{a}LeThree', pc(s['frac_le3'])); macro(f'Ssd{stem}{a}LeTen', pc(s['frac_le10']))
                macro(f'Ssd{stem}{a}GtTen', pc(s['frac_gt10'])); macro(f'Ssd{stem}{a}Median', str(s['median_of_mean_dist'])); macro(f'Ssd{stem}{a}Empty', pc(s['frac_empty']))
        if key != SSD[-1][0]: rows.append(r'\addlinespace')
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')
    if alpha == ALPHA: macro('SsdConfigs', str(n))


SSDL_DESIGN = {'vitl683': 'exchangeable, native frozen'}        # Tab. 2's ADE20K row draws one of the K frozen sets; every other row a fresh random set
SSDL_ARMS = [('anchored, image-level (paper)', 'anchored, image-level', 'Img'), ('anchored, label-level', 'anchored, label-level', 'Lab'),
             ('native, full known, label-level', 'native recal., label-level', 'NatLab')]


def table_setsize_label(filename='setsize_label.tex'):
    """Supplement: distribution of the per-pixel set size under the label-level threshold (exp_set_size_dist_label.py), on
    the trials of Tab. 2 / Tab. S-labelmodels, over labelled held-out pixels. Macros \\SsdL<stem><Arm><stat> (alpha = .1,
    random source vocabulary) and \\SsdLSplit<stem><Arm><stat> (alpha = .1, the dataset's own split)."""
    rows = [r'\begin{tabular}{@{}llrrrrrr@{}}', r'\toprule',
            r'& & \multicolumn{4}{c}{pixels with $|C|$ (\%)} & \multicolumn{2}{c}{labels per pixel} \\', r'\cmidrule(lr){3-6}\cmidrule(l){7-8}',
            r'Configuration & threshold & $=1$ & $\le 3$ & $\le 10$ & $>10$ & median & mean \\']
    n = 0
    for alpha in ['0.1', '0.05']:
        if rows[-1] == r'\addlinespace': rows.pop()
        rows += [r'\midrule', r'\multicolumn{8}{@{}l}{\emph{$\alpha=' + ('10' if alpha == '0.1' else '5') + r'\%$}} \\']
        for key, ds, model in SSD:
            dset, tag, *_ = CONFIGS[key]; stem = CONFIGS[key][5]
            j = load(f'results/set_size_dist_label_{dset}_{tag}')
            if j is None: continue
            n += alpha == '0.1'
            for design, pre in [(SSDL_DESIGN.get(key, 'exchangeable'), 'SsdL'), ('dataset split', 'SsdLSplit')]:
                d = j['designs'][f'a{alpha}, {design}']
                for i, (arm, label, a) in enumerate(SSDL_ARMS):
                    s = d[arm]
                    if pre == 'SsdL':
                        rows.append((f'{ds}, {model}' if i == 0 else '') + f' & {label} & {pc(s["frac_one"])} & {pc(s["frac_le3"])} & {pc(s["frac_le10"])} & '
                                    f'{pc(s["frac_gt10"])} & {s["median_of_mean_dist"]} & {f2(s["mean"])} \\\\')
                    if alpha == '0.1':
                        macro(f'{pre}{stem}{a}One', pc(s['frac_one'])); macro(f'{pre}{stem}{a}LeThree', pc(s['frac_le3'])); macro(f'{pre}{stem}{a}LeTen', pc(s['frac_le10']))
                        macro(f'{pre}{stem}{a}GtTen', pc(s['frac_gt10'])); macro(f'{pre}{stem}{a}Median', str(s['median_of_mean_dist'])); macro(f'{pre}{stem}{a}Mean', f2(s['mean']))
            if key != SSD[-1][0]: rows.append(r'\addlinespace')
    if rows[-1] == r'\addlinespace': rows.pop()
    rows += [r'\bottomrule', r'\end{tabular}']
    (TAB/filename).write_text('\n'.join(rows)+'\n')
    macro('SsdLConfigs', str(n))


def main():
    TAB.mkdir(parents=True, exist_ok=True)
    table_main()
    for key in CONFIGS: headline_macros(key)
    silent_failure(); repeated_recal(); claude_baseline(); table_curve(); table_bank(); table_bank_seeds(); table_added(); table_confirm(); table_strata(); table_losses(); table_constructions(); table_calsize()
    table_fcclip_banks(); table_finetune(); audit(); qualitative(); probe_miou(); table_miou(); table_seg_added(); table_per_name();table_runtime(); table_runtime_lean(); table_memory(); table_adaptive(); table_adaptive('sed_bank683', 'adaptive_sed', 'AdaptSed'); table_adaptive('fcclip_bank683', 'adaptive_fcclip', 'AdaptFc'); table_adaptive_pascal(); table_adaptive_main(); table_freeform(); disjoint_bank_check();table_label_exchange(); table_label_models(); table_label_images(); table_label_sample(); table_native_refs(); table_label_hardness(); table_ovd(); table_ovd_accuracy(); table_setsize(); table_setsize(ALPHA2, 'setsize_b.tex'); table_setsize_label()
    lines = ['% generated by src/paper_numbers.py; do not edit'] + [f'\\newcommand{{\\{k}}}{{{v}}}' for k, v in sorted(macros.items())]
    (OUT/'numbers.tex').write_text('\n'.join(lines)+'\n'); print(f'{len(macros)} macros, tables: {sorted(p.name for p in TAB.glob("*.tex"))}')


if __name__ == '__main__':
    main()
