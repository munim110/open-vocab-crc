"""Qualitative figure: per-pixel CRC set size and missed source pixels on one ADE validation image.

Panels, with released CAT-Seg ViT-L:
  (0) native, threshold calibrated at the 150 source names, before growth     (native150 -> native150)
  (1) native, threshold calibrated at the 150 source names and reused        (native150 -> native845)
  (2) native, threshold recalibrated at the 845 names                          (native845 -> native845)
  (3) anchored (683-name bank), threshold calibrated once at the 150 names    (anchored845 -> anchored845)
The paper figure (problem, Sec. 4) shows (0)-(2); the supplement figure shows (1)-(3).
Set size counts all labels of the scored vocabulary with logit >= threshold; a source-labelled pixel is missed when
its true label's logit < threshold.

Thresholds: alpha = .10, image-level CRC (conformal.crc_lambda) on the paper's design (exp_headroom_splits.py,
tag vitl_bank683: 2,000 images, 1,000 calibration / 1,000 evaluation, 500 splits, rng 20261003). Per-split
thresholds were not stored, so they are recomputed here from the probe's sampled-pixel caches; the split whose
three thresholds sit closest to their medians across splits is used, and its mean evaluation risks are
checked against the stored results.json.

Dense scores repeat exp_headroom_probe.py exactly (resize_short, sliding windows + global view, official
stitch at 640x640, bilinear to the annotation grid, logit clamped to [-30, 30] and rounded to float16 like
the stores); the dense maps are checked against the stored scores at the probe's sampled pixels.

Stages (run from the repo root with .venv-probe):
  python src/fig_qualitative.py --stage select     # thresholds + cache-only scan of evaluation images
  python src/fig_qualitative.py --stage dense --image 1234 [--image ...]
  python src/fig_qualitative.py --stage plot --image 1234
  python src/fig_qualitative.py --image 1234      # all three for one image
  python src/fig_qualitative.py --stage panel     # supplement panel: PANEL_N random evaluation images of the median
                                                  # split (seed PANEL_SEED), dense maps computed where missing, writes
                                                  # paper/fig/fig_qualitative_panel.pdf and results/qualitative_ade/panel.json
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from conformal import crc_lambda
from exp_fixed_source import digest
from exp_headroom_sets import LOGIT_GRID
from exp_headroom_splits import curves

TAG = 'vitl_bank683'
RUNS = [f'results/headroom_probe_ade_{TAG}', f'results/headroom_probe_ade_{TAG}_rest']
CACHES = [f'cache/headroom_probe_{TAG}', f'cache/headroom_probe_{TAG}_rest']
SPLITS_RESULT = Path(f'results/headroom_splits_ade_{TAG}/results.json')
OUT = Path('results/qualitative_ade')
WORK = Path('cache/qualitative_ade')            # new folder; derived per-pixel true-label scores only
FIG = Path('paper/fig/fig_qualitative.pdf')
PROBLEM_FIG = Path('paper/fig/fig_problem.pdf')
PANEL_FIG = Path('paper/fig/fig_qualitative_panel.pdf')
PANEL_N, PANEL_SEED = 6, 20261019                # random (not selected) images for the supplement panel
ALPHA, NSPLITS, SEED, S = .10, 500, 20261003, 150
EVAL_ROLES = ['tune_eval', 'evaluation']        # evaluation roles of the probe's saved split
# panel -> (store the threshold is calibrated on, store the panel is evaluated on)
PANELS = dict(native_source=('native150', 'native150'), native_reused=('native150', 'native845'), native_recal=('native845', 'native845'),
              anchored=('anchored845', 'anchored845'))
LABELS = dict(native_source='native, at 150', native_reused='native, reused', native_recal='native, recal. at 845', anchored='anchored, once at 150')
SOLUTION_PANELS = ['native_reused', 'native_recal', 'anchored']
PROBLEM_PANELS = ['native_source', 'native_reused', 'native_recal']
PROBLEM_LABELS = dict(native_source='150 names, calibrated here', native_reused='845 names, same threshold', native_recal='845 names, recalibrated')
LEGIBLE = {'street', 'bedroom', 'living_room', 'bathroom', 'kitchen', 'dining_room', 'conference_room', 'hotel_room',
           'office', 'corridor', 'building_facade', 'alley', 'home_office', 'parlor', 'waiting_room', 'game_room',
           'skyscraper', 'highway', 'art_studio', 'poolroom_home', 'attic', 'closet', 'exterior', 'park'}


def probe_ids():
    return sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in RUNS], [])


def open_stores():
    return {k: [np.load(f'{c}/{k}.npy', mmap_mode='r') for c in CACHES] for k in ['native150', 'native845', 'anchored845']}


def store_row(parts, k):
    for part in parts:
        if k < len(part): return np.array(part[k])
        k -= len(part)
    raise IndexError(k)


def true_scores():
    """Per-pixel true-label logits [N,npix] for each store (source-labelled pixels; 255 elsewhere is clamped)."""
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK/'true_scores.npz'
    if path.exists(): return dict(np.load(path))
    ids = probe_ids(); gt = np.load('cache/sclip/gt150.npy')[ids]
    idx = np.minimum(gt, S-1).astype(np.int64)[..., None]
    stores, out = open_stores(), {}
    for name, parts in stores.items():
        rows = []
        for k in range(len(ids)):
            rows.append(np.take_along_axis(store_row(parts, k), idx[k], 1)[:, 0])
            if k % 250 == 0: print(name, k, flush=True)
        out[name] = np.stack(rows)
    np.savez(path, **out)
    return out


def thresholds():
    """Recompute the per-split CRC thresholds of the paper's design and pick the median split."""
    ids = probe_ids(); n = len(ids)
    gt = torch.from_numpy(np.load('cache/sclip/gt150.npy')[ids].astype(np.int64)).cuda()
    assert (gt < S).any(1).all(), 'exp_headroom_splits excludes images without source pixels; none expected here'
    grid = torch.from_numpy(LOGIT_GRID).cuda()
    ts = true_scores()
    loss = {}
    for name, t in ts.items():
        # curves() reads a score matrix; a one-column matrix holding the true score gives the identical loss curve
        loss[name] = np.stack([curves(torch.from_numpy(t[k].astype(np.float64)).cuda()[:, None], torch.zeros_like(gt[k]).masked_fill(gt[k] >= S, S),
                                      grid, 1, [1])[0] for k in range(n)])
    rng = np.random.default_rng(SEED)
    for n_cal in [200, n//2]:                                       # same draw order as exp_headroom_splits.py
        perms = [rng.permutation(n) for _ in range(NSPLITS)]
    n_cal = n//2
    thr = {store: np.array([crc_lambda(torch.from_numpy(loss[store][p[:n_cal]]), LOGIT_GRID, ALPHA, True) for p in perms]) for store in loss}
    # sanity: mean evaluation risk over splits reproduces the stored results.json
    stored = json.loads(SPLITS_RESULT.read_text())['designs'][f'cal{n_cal}_a{ALPHA}']
    arm_of = dict(native_source='catseg_native_source', native_reused='catseg_native_frozen_full', native_recal='catseg_native_replay_full', anchored='catseg_anchored')
    check = {}
    for panel, (cal, ev) in PANELS.items():
        risk = np.mean([loss[ev][p[n_cal:], thr[cal][s]].mean() for s, p in enumerate(perms)])
        check[panel] = dict(recomputed=float(risk), stored=stored[arm_of[panel]]['mean_risk'])
        # results.json (2026-09-23) was computed from the GH200 stores; the local stores were regenerated on 2026-09-26
        # (float noise up to ~5e-4 in re-runs), so agreement is to ~1e-6 rather than exact
        assert abs(risk-check[panel]['stored']) < 5e-4, check
    med = {k: np.median(v) for k, v in thr.items()}
    dev = sum(np.abs(thr[k]-med[k]) for k in thr)                    # grid steps from the per-arm median, summed
    split = int(np.argmin(dev))
    perm = perms[split]
    info = dict(design=f'cal{n_cal} (1,000 calibration / 1,000 evaluation images), alpha {ALPHA}, {NSPLITS} splits, rng {SEED}', split=split,
                split_rule='split minimising the summed distance (grid steps) of its three thresholds from their medians across splits',
                deviation_grid_steps=float(dev[split]), median_thresholds={k: float(LOGIT_GRID[int(round(v))]) if float(v).is_integer() else float(np.interp(v, np.arange(len(LOGIT_GRID)), LOGIT_GRID)) for k, v in med.items()},
                thresholds={k: float(LOGIT_GRID[v[split]]) for k, v in thr.items()},
                threshold_range_over_splits={k: [float(LOGIT_GRID[v.min()]), float(LOGIT_GRID[v.max()])] for k, v in thr.items()},
                calibration_risk_bound={k: float((loss[k][perm[:n_cal], thr[k][split]].sum()+1)/(n_cal+1)) for k in thr},
                evaluation_risk_this_split={p: float(loss[ev][perm[n_cal:], thr[cal][split]].mean()) for p, (cal, ev) in PANELS.items()},
                mean_risk_check=check, calibration_images=[ids[i] for i in perm[:n_cal]], evaluation_images=[ids[i] for i in perm[n_cal:]])
    return info, ts


def scenes():
    out = {}
    for line in Path('data/ADEChallengeData2016/sceneCategories.txt').read_text().split('\n'):
        if line.startswith('ADE_val_'): f, s = line.split(); out[int(f[8:])-1] = s
    return out


def select(args):
    OUT.mkdir(parents=True, exist_ok=True)
    info, ts = thresholds()
    ids = probe_ids(); pos = {i: k for k, i in enumerate(ids)}
    gt = np.load('cache/sclip/gt150.npy')
    split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
    roles = {r['index']: role for role in split['roles'] for r in split['roles'][role]}
    sc = scenes(); ev = set(info['evaluation_images'])
    pool = [i for i in ids if i in ev and roles[i] in EVAL_ROLES]
    rows = []
    for i in pool:
        k = pos[i]; valid = gt[i] < S
        miss = {p: float((ts[ev_][k][valid] < info['thresholds'][cal]).mean()) for p, (cal, ev_) in PANELS.items()}
        rows.append(dict(image=i, file=f'ADE_val_{i+1:08d}.jpg', scene=sc[i], role=roles[i], common_scene=sc[i] in LEGIBLE, source_pixel_fraction=float(valid.mean()), sampled_miss=miss))
    hit = lambda r: r['sampled_miss']['native_reused'] >= .2 and max(r['sampled_miss']['native_recal'], r['sampled_miss']['anchored']) <= .12 and r['source_pixel_fraction'] >= .5
    hits = [r for r in rows if hit(r)]
    hits.sort(key=lambda r: r['sampled_miss']['native_reused']-max(r['sampled_miss']['native_recal'], r['sampled_miss']['anchored']), reverse=True)
    stores = open_stores()
    for r in hits[:args.scan]:                                       # sampled-pixel set sizes for the top candidates only
        k = pos[r['image']]; valid = gt[r['image']] < S
        r['sampled_mean_size'] = {p: float((store_row(stores[ev_], k)[valid].astype(np.float32) >= info['thresholds'][cal]).sum(1).mean()) for p, (cal, ev_) in PANELS.items()}
    summary = dict(info={k: v for k, v in info.items() if k not in ('calibration_images', 'evaluation_images')},
                   pool=dict(evaluation_half_of_split=len(ev), also_in_probe_evaluation_roles=len(pool), meeting_criterion=len(hits), common_scene_meeting_criterion=sum(r['common_scene'] for r in hits),
                             criterion='sampled miss: reused >= 20%, recalibrated and anchored <= 12%; >= 50% of sampled pixels source-labelled; ranked by reused minus the larger of the other two',
                             mean_sampled_miss_over_pool={p: float(np.mean([r['sampled_miss'][p] for r in rows])) for p in PANELS},
                             reused_worse_than_both_others=float(np.mean([r['sampled_miss']['native_reused'] > max(r['sampled_miss']['native_recal'], r['sampled_miss']['anchored']) for r in rows]))),
                   top=hits[:args.scan])
    (OUT/'selection.json').write_text(json.dumps(summary, indent=2))
    (OUT/'split_images.json').write_text(json.dumps({k: info[k] for k in ('split', 'calibration_images', 'evaluation_images')}))
    print(json.dumps(summary['info'], indent=1)); print(json.dumps(summary['pool'], indent=1))
    for r in hits[:args.scan]:
        print(r['image'], r['scene'], r['role'], round(r['source_pixel_fraction'], 2), {k: round(v, 3) for k, v in r['sampled_miss'].items()}, {k: round(v, 2) for k, v in r['sampled_mean_size'].items()})
    return summary


@torch.no_grad()
def dense(image_ids):
    import torch.nn.functional as F
    from PIL import Image
    from catseg_probe_model import CATSegProbe, CKPT, bank_context
    from encode import ADE
    from exp_headroom_probe import resize_short
    from natural_vocab import load_manifest
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    sel = json.loads((OUT/'selection.json').read_text())['info']
    thr = sel['thresholds']
    protocol = json.loads((Path(RUNS[0])/'protocol.json').read_text())
    assert protocol['size'] == 'large' and protocol['bank'] == 'meta/bank_coco_oi683_v1.json' and protocol['model'] == 'catseg'
    names = [r['prompt'] for r in load_manifest()['rows']]
    reference = json.loads(Path(protocol['bank']).read_text())['names']
    model = CATSegProbe(None, 'large').cuda()
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    ids = probe_ids(); pos = {i: k for k, i in enumerate(ids)}
    stores = open_stores()
    for index in image_ids:
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        lab = np.array(Image.open(Path(ADE)/'annotations/validation'/info['file'].replace('.jpg', '.png')))
        gt = torch.from_numpy(np.where(lab > 0, lab.astype(np.int64)-1, 255)).cuda()
        valid = gt < S
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        feats = model.image_features(model.windows(tensor))
        maps = dict(native845=model.native(feats, text))
        maps['anchored845'] = model.anchored(feats, bank_context(model, feats, ref_text), text)
        maps['native150'] = model.native(feats, text[:S])
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        yy, xx = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        out, check = {}, {}
        for store, logits in maps.items():
            true = torch.full((H, W), -30., device='cuda'); counts = {}
            sampled = []
            for i in range(0, logits.shape[1], 128):
                prob = model.stitch(logits[:, i:i+128])                                  # [t,640,640] as in the probe
                prob = F.interpolate(prob[None], size=(H, W), mode='bilinear', align_corners=False)[0]   # == sample_phi at pixel centres
                z = torch.logit(prob.double().clamp(1e-12, 1-1e-12)).clamp(-30, 30).half().float()     # same rounding as the stores
                sampled.append(z[:, yy, xx].T)
                for p, (cal, ev) in PANELS.items():
                    if ev == store: counts[p] = counts.get(p, 0)+(z >= thr[cal]).sum(0)
                sel_ = (gt >= i) & (gt < i+z.shape[0]) & valid
                if sel_.any():
                    true[sel_] = z.gather(0, (gt.clamp(i, i+z.shape[0]-1)-i)[None])[0][sel_]
                del prob, z
            ref = torch.from_numpy(store_row(stores[store], pos[index]).astype(np.float32)).cuda()
            sampled = torch.cat(sampled, 1)
            check[store] = dict(max_abs_logit_diff=float((sampled-ref).abs().max()), entries_differing=int((sampled != ref).sum()), entries=int(ref.numel()),
                                membership_flips={p: int(((sampled >= thr[cal]) != (ref >= thr[cal])).sum()) for p, (cal, ev) in PANELS.items() if ev == store})
            for p, (cal, ev) in PANELS.items():
                if ev == store:
                    miss = valid & (true < thr[cal])
                    out[p] = dict(size=counts[p].cpu().numpy().astype(np.uint16), miss=miss.cpu().numpy())
        np.savez_compressed(OUT/f'dense_{index}.npz', valid=valid.cpu().numpy(), label=lab, **{f'{p}_{k}': v for p, d in out.items() for k, v in d.items()})
        v = valid.cpu().numpy()
        res = dict(image=index, file=info['file'], H=H, W=W, source_pixel_fraction=float(v.mean()),
                   max_abs_diff_vs_probe_store_at_sampled_pixels=check,
                   panels={p: dict(label=LABELS[p], calibrated_on=PANELS[p][0], evaluated_on=PANELS[p][1], threshold=thr[PANELS[p][0]],
                                   miss_fraction=float(d['miss'][v].mean()), mean_set_size_source_pixels=float(d['size'][v].mean()),
                                   mean_set_size_all_pixels=float(d['size'].mean()), median_set_size_source_pixels=float(np.median(d['size'][v])),
                                   empty_set_fraction_source_pixels=float((d['size'][v] == 0).mean()))
                           for p, d in out.items()})
        (OUT/f'dense_{index}.json').write_text(json.dumps(res, indent=2))
        print(json.dumps(res, indent=1), flush=True)
        del maps; torch.cuda.empty_cache()
    print('peak GB', torch.cuda.max_memory_allocated()/2**30)


def plot(index, vmax, fig_path=FIG, panels=SOLUTION_PANELS, labels=LABELS, png='fig_qualitative'):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from PIL import Image
    matplotlib.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.size': 6, 'font.family': 'DejaVu Sans'})
    d = np.load(OUT/f'dense_{index}.npz'); res = json.loads((OUT/f'dense_{index}.json').read_text())
    img = np.array(Image.open(Path('data/ADEChallengeData2016/images/validation')/res['file']).convert('RGB'))
    H, W = img.shape[:2]
    # sequential, one hue light -> dark; sizes >= vmax share the darkest bin
    base = plt.get_cmap('Blues')
    bounds = np.arange(0, vmax+2)-.5                                  # one bin per size 0..vmax (vmax = vmax or more)
    cmap = ListedColormap(base(np.linspace(.12, 1, vmax+1)))
    norm = BoundaryNorm(bounds, cmap.N)
    miss_rgba = np.array([.91, .30, .05, 1.])                        # orange: missed source pixel
    n = 1+len(panels)
    # layout in inches: one row of panels, colour bar + miss key at the right, two-line panel labels on top
    fig_w, left, gap, right, top, bottom = 3.25, .01, .035, .40, .21, .01
    pw = (fig_w-left-right-gap*(n-1))/n
    ph = pw*H/W
    fig_h = ph+top+bottom
    fig = plt.figure(figsize=(fig_w, fig_h))
    box = lambda x, y, w, h: fig.add_axes([x/fig_w, y/fig_h, w/fig_w, h/fig_h])
    axes = [box(left+j*(pw+gap), bottom, pw, ph) for j in range(n)]
    axes[0].imshow(img, interpolation='lanczos')
    axes[0].set_title('input', fontsize=6, pad=1.5, linespacing=.95)
    for ax, p in zip(axes[1:], panels):
        size = np.minimum(d[f'{p}_size'], vmax)
        rgba = cmap(norm(size))
        rgba[d[f'{p}_miss']] = miss_rgba
        rgba[~d['valid']] = rgba[~d['valid']]*.55+.45*np.array([1, 1, 1, 1.])   # unlabelled pixels faded
        ax.imshow(rgba, interpolation='nearest')
        ax.set_title(labels[p].replace(', ', ',\n'), fontsize=6, pad=1.5, linespacing=.95)
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_linewidth(.4)
    x_bar, w_bar, key = left+n*pw+(n-1)*gap+.05, .065, .065
    kax = box(x_bar, bottom+ph-key, w_bar, key)                       # orange key for missed source pixels
    kax.add_patch(matplotlib.patches.Rectangle((0, 0), 1, 1, color=miss_rgba)); kax.set_xlim(0, 1); kax.set_ylim(0, 1)
    kax.set_xticks([]); kax.set_yticks([])
    for s in kax.spines.values(): s.set_linewidth(.4)
    kax.text(1.3, .45, 'miss', fontsize=6, va='center', ha='left', transform=kax.transAxes)
    cax = box(x_bar, bottom, w_bar, ph-key-.06)
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, cax=cax, ticks=[0, vmax//2, vmax] if vmax > 2 else list(range(vmax+1)))
    cb.ax.set_yticklabels([str(t) if t < vmax else f'{t}+' for t in cb.get_ticks().astype(int)])
    cb.ax.tick_params(labelsize=6, width=.4, length=1.5, pad=1)
    cb.outline.set_linewidth(.4)
    cb.set_label('set size', fontsize=6, labelpad=1)
    fig_path = Path(fig_path); fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=600)
    fig.savefig(OUT/f'{png}_{index}.png', dpi=300)
    print('figure', fig_path, f'{fig_w:.2f} x {fig_h:.2f} in')
    return fig_h


def panel_images(n, seed):
    """n images drawn at random, without replacement, from the pool of the selection scan: the evaluation half of the
    median split restricted to the probe's evaluation roles. Returns the sorted indices and the pool size."""
    ev = set(json.loads((OUT/'split_images.json').read_text())['evaluation_images'])
    split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
    roles = {r['index']: role for role in split['roles'] for r in split['roles'][role]}
    pool = sorted(i for i in probe_ids() if i in ev and roles[i] in EVAL_ROLES)
    rng = np.random.default_rng(seed)
    return sorted(int(i) for i in rng.choice(pool, n, replace=False)), len(pool)


def panel(ids, vmax, fig_path=PANEL_FIG, seed=None, pool_size=None):
    """One row per image: input and the three panels of plot(), same colour scale; per-panel miss and mean set size above."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from PIL import Image
    matplotlib.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.size': 6, 'font.family': 'DejaVu Sans'})
    base = plt.get_cmap('Blues')
    bounds = np.arange(0, vmax+2)-.5
    cmap = ListedColormap(base(np.linspace(.12, 1, vmax+1)))
    norm = BoundaryNorm(bounds, cmap.N)
    miss_rgba = np.array([.91, .30, .05, 1.])
    panels = SOLUTION_PANELS
    n = 1+len(panels)
    rows = []
    for index in ids:
        d = np.load(OUT/f'dense_{index}.npz'); res = json.loads((OUT/f'dense_{index}.json').read_text())
        img = np.array(Image.open(Path('data/ADEChallengeData2016/images/validation')/res['file']).convert('RGB'))
        rows.append((index, d, res, img))
    fig_w, left, gap, right, top, bottom, vgap = 6.875, .01, .035, .40, .20, .01, .17
    pw = (fig_w-left-right-gap*(n-1))/n
    heights = [pw*img.shape[0]/img.shape[1] for _, _, _, img in rows]
    fig_h = sum(heights)+top+bottom+vgap*(len(rows)-1)
    fig = plt.figure(figsize=(fig_w, fig_h))
    box = lambda x, y, w, h: fig.add_axes([x/fig_w, y/fig_h, w/fig_w, h/fig_h])
    y = fig_h-top
    stats = {}
    for r, (index, d, res, img) in enumerate(rows):
        ph = heights[r]; y -= ph
        axes = [box(left+j*(pw+gap), y, pw, ph) for j in range(n)]
        axes[0].imshow(img, interpolation='lanczos')
        axes[0].set_title(('input\n' if r == 0 else '')+res['file'].replace('.jpg', ''), fontsize=6, pad=1.5, linespacing=.95)
        stats[index] = {}
        for ax, p in zip(axes[1:], panels):
            size = np.minimum(d[f'{p}_size'], vmax)
            rgba = cmap(norm(size))
            rgba[d[f'{p}_miss']] = miss_rgba
            rgba[~d['valid']] = rgba[~d['valid']]*.55+.45*np.array([1, 1, 1, 1.])
            ax.imshow(rgba, interpolation='nearest')
            pr = res['panels'][p]
            stats[index][p] = dict(miss_fraction=pr['miss_fraction'], mean_set_size_source_pixels=pr['mean_set_size_source_pixels'])
            line = f"miss {100*pr['miss_fraction']:.1f}%, {pr['mean_set_size_source_pixels']:.1f} labels"
            ax.set_title((LABELS[p]+'\n' if r == 0 else '')+line, fontsize=6, pad=1.5, linespacing=.95)
        for ax in axes:
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_linewidth(.4)
        if r == 0:
            x_bar, w_bar, key = left+n*pw+(n-1)*gap+.05, .065, .065
            kax = box(x_bar, y+ph-key, w_bar, key)
            kax.add_patch(matplotlib.patches.Rectangle((0, 0), 1, 1, color=miss_rgba)); kax.set_xlim(0, 1); kax.set_ylim(0, 1)
            kax.set_xticks([]); kax.set_yticks([])
            for s in kax.spines.values(): s.set_linewidth(.4)
            kax.text(1.3, .45, 'miss', fontsize=6, va='center', ha='left', transform=kax.transAxes)
            cax = box(x_bar, y, w_bar, ph-key-.06)
            sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
            cb = fig.colorbar(sm, cax=cax, ticks=[0, vmax//2, vmax] if vmax > 2 else list(range(vmax+1)))
            cb.ax.set_yticklabels([str(t) if t < vmax else f'{t}+' for t in cb.get_ticks().astype(int)])
            cb.ax.tick_params(labelsize=6, width=.4, length=1.5, pad=1)
            cb.outline.set_linewidth(.4)
            cb.set_label('set size', fontsize=6, labelpad=1)
        y -= vgap
    fig_path = Path(fig_path); fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=600)
    fig.savefig(OUT/'fig_qualitative_panel.png', dpi=200)
    sel = json.loads((OUT/'selection.json').read_text())['info']
    out = dict(images=[dict(image=i, file=rows[k][2]['file'], panels=stats[i]) for k, i in enumerate(ids)], n=len(ids), seed=seed, pool_size=pool_size,
               selection='random draw without replacement (numpy default_rng(seed)) from the pool of selection.json (evaluation half of the median split, probe evaluation roles)',
               split=sel['split'], thresholds=sel['thresholds'],
               mean_over_images={p: dict(miss_fraction=float(np.mean([stats[i][p]['miss_fraction'] for i in ids])),
                                         mean_set_size_source_pixels=float(np.mean([stats[i][p]['mean_set_size_source_pixels'] for i in ids]))) for p in panels},
               figure=str(fig_path), figure_size_in=[fig_w, round(fig_h, 3)], colour_scale=f'set size 0..{vmax}+ (shared with the paper figure), orange = missed source pixel, faded = unlabelled pixel',
               hashes={p: digest(Path(p)) for p in ['src/fig_qualitative.py', 'src/catseg_probe_model.py', 'src/exp_headroom_probe.py']})
    (OUT/'panel.json').write_text(json.dumps(out, indent=2))
    print('panel', fig_path, f'{fig_w:.3f} x {fig_h:.3f} in', ids)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', default='all', choices=['select', 'dense', 'plot', 'all', 'panel'])
    ap.add_argument('--panel-n', type=int, default=PANEL_N, help='images in the supplement panel (stage panel)')
    ap.add_argument('--panel-seed', type=int, default=PANEL_SEED, help='seed of the random draw (stage panel)')
    ap.add_argument('--image', type=int, action='append', default=[], help='ADE validation index (0-based; file ADE_val_{index+1:08d}.jpg)')
    ap.add_argument('--scan', type=int, default=40, help='candidates to keep from the cache-only scan')
    ap.add_argument('--fig', default=str(FIG), help='figure path (default: the paper figure); summary.json is written only for the default')
    ap.add_argument('--vmax', type=int, default=8, help='top of the shared set-size colour scale (larger sizes saturate)')
    a = ap.parse_args()
    if a.stage == 'panel':
        assert (OUT/'split_images.json').exists(), 'run the select stage first'
        ids, pool_size = panel_images(a.panel_n, a.panel_seed)
        missing = [i for i in ids if not (OUT/f'dense_{i}.npz').exists()]
        if missing: dense(missing)
        panel(ids, a.vmax, PANEL_FIG, a.panel_seed, pool_size)
        return
    if a.stage in ('select', 'all') and not (OUT/'selection.json').exists() or a.stage == 'select':
        select(a)
    if a.stage in ('dense', 'all'):
        dense(a.image)
    if a.stage in ('plot', 'all'):
        assert len(a.image) == 1
        fig_h = plot(a.image[0], a.vmax, a.fig)
        index = a.image[0]
        if Path(a.fig) != FIG: return
        problem_h = plot(index, a.vmax, PROBLEM_FIG, PROBLEM_PANELS, PROBLEM_LABELS, 'fig_problem')
        res = json.loads((OUT/f'dense_{index}.json').read_text())
        sel = json.loads((OUT/'selection.json').read_text())
        cand = next((r for r in sel['top'] if r['image'] == index), None)
        summary = dict(image=index, file=res['file'], scene=cand['scene'] if cand else None, probe_role=cand['role'] if cand else None,
                       selection='selected (not random): see selection.json for the pool, criterion and ranked candidates',
                       rank_in_cache_scan=(next(i for i, r in enumerate(sel['top']) if r['image'] == index)+1) if cand else None,
                       split=sel['info']['split'], design=sel['info']['design'], thresholds=sel['info']['thresholds'],
                       threshold_source=sel['info']['split_rule']+'; recomputed from the probe sampled-pixel caches with conformal.crc_lambda',
                       mean_risk_check=sel['info']['mean_risk_check'], panels=res['panels'], sampled_pixel_numbers=cand,
                       dense_vs_store_max_abs_diff=res['max_abs_diff_vs_probe_store_at_sampled_pixels'],
                       figure=str(FIG), figure_size_in=[3.25, round(fig_h, 3)], problem_figure=str(PROBLEM_FIG), problem_panels=PROBLEM_PANELS,
                       problem_figure_size_in=[3.25, round(problem_h, 3)], colour_scale=f'set size 0..{a.vmax}+ (shared), orange = missed source pixel, faded = unlabelled pixel',
                       hashes={p: digest(Path(p)) for p in ['src/fig_qualitative.py', 'src/catseg_probe_model.py', 'src/exp_headroom_probe.py']})
        (OUT/'summary.json').write_text(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
