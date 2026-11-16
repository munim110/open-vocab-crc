"""Pixel evidence and verified spatial strata for fixed-source softmax."""
import csv
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exp_fixed_source import digest
from exp_natural_ranks import true_ranks

OUT = Path('results/pixel_diagnosis_sclip_ade')
PRIOR = Path('results/match_correction_sclip_ade')
FEATURES = ['feature_norm', 'source_entropy', 'top_two_gap', 'max_dot_product']
METRICS = ['miss', 'source_size', 'expanded_size', 'source_rank', 'expanded_rank', 'source_top1_wrong']


def spatial_strata(lab, sampled, short):
    valid = lab > 0
    edge = np.zeros_like(valid)
    vertical = valid[1:] & valid[:-1] & (lab[1:] != lab[:-1])
    horizontal = valid[:, 1:] & valid[:, :-1] & (lab[:, 1:] != lab[:, :-1])
    edge[1:] |= vertical; edge[:-1] |= vertical
    edge[:, 1:] |= horizontal; edge[:, :-1] |= horizontal
    scale = min(2048/max(lab.shape), short/min(lab.shape))
    if edge.any():
        distance = cv2.distanceTransform((~edge).astype(np.uint8), cv2.DIST_L2, cv2.DIST_MASK_PRECISE)*scale
    else:
        distance = np.full(lab.shape, np.inf)
    near = distance.ravel()[sampled] <= 3
    frequency = np.bincount(lab[valid], minlength=151)/max(valid.sum(), 1)
    area = frequency[lab.ravel()[sampled]]
    return near, area


def feature_values(f, z):
    g = z-torch.logsumexp(z, -1, keepdim=True)
    tops = z.topk(2, dim=-1).values
    return torch.stack([f.norm(dim=-1).double(), -(g.exp()*g).sum(-1),
                        tops[..., 0]-tops[..., 1], tops[..., 0]/40], -1)


@torch.no_grad()
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    split = json.loads((PRIOR/'split.json').read_text())
    fit = np.array([x['index'] for x in split['roles']['fit']])
    ids = np.array([x['index'] for x in split['roles']['evaluation']])
    assert not set(fit)&set(ids)
    result = json.loads((PRIOR/'results.json').read_text())
    threshold = result['thresholds'][0][0]
    protocol = dict(
        purpose='Descriptive pixel audit of frozen fixed-source baseline; no fitting or correction selection.',
        roles='800 fit images set feature quintile edges; existing 400 evaluation images supply outcomes. All historically inspected development data.',
        threshold=threshold, additions=[0, 695], temperature=40,
        features=FEATURES, metrics=METRICS,
        spatial='Reconstruct sample coordinates with pixseed+image_index; require exact mask/cache label agreement in every evaluation image. Boundary endpoints are 4-neighbor differing valid labels; near means within3 resized-image pixels, using encoder resize scale. Ignore transitions and image borders are not semantic boundaries.',
        area='Ground-truth semantic class area / valid image area: <1%, 1-10%, >=10%. All disconnected regions of one class combined; not instance size.',
        aggregation='Equal-image conditional group metrics; occupancy and miss/size contributions use all valid pixels per image. Conditional means do not sum; contributions do.',
        features_scope='Computed against fixed source150; entropy/gap are evidence summaries, not calibrated correctness probabilities. Feature norm is affected by interpolation and crop averaging.',
        limits='Observational, class composition confounded. Spatial strata use ground truth and are diagnostic only. Sampled pixels cannot validate a dense spatial operator.',
        hashes={str(p): digest(p) for p in [Path(__file__), Path('src/encode.py'), PRIOR/'split.json', PRIOR/'results.json', Path('cache/sclip/meta.json')]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    phi = np.load('cache/sclip/phi.npy', mmap_mode='r')
    gt = np.load('cache/sclip/gt150.npy')
    text = torch.from_numpy(np.load('results/natural_ranks_sclip_ade/text_embeddings.npy')).cuda()
    def batches(indices, expanded):
        end = 845 if expanded else 150
        for lo in range(0, len(indices), 8):
            ix = indices[lo:lo+8]
            f = torch.from_numpy(np.array(phi[ix])).cuda().float()
            z = 40*torch.cat([f@text[j:min(j+64,end)].T for j in range(0,end,64)], -1).double()
            yield lo, ix, f, z
    fitting_features = []
    for lo, ix, f, z in batches(fit, False):
        values = feature_values(f, z).cpu().numpy()
        fitting_features.append(values[gt[ix] < 150])
        if lo%160 == 0:
            print(f'Feature bins: {lo+len(ix)}/{len(fit)}', flush=True)
    edges = np.quantile(np.concatenate(fitting_features), [.2,.4,.6,.8], axis=0).T
    del fitting_features
    (OUT/'bin_edges.json').write_text(json.dumps(dict(zip(FEATURES, edges.tolist())), indent=2))
    n, pixels = len(ids), meta['npix']
    values = np.zeros((n, pixels, 6), np.float32)
    features = np.zeros((n, pixels, 4), np.float32)
    boundaries = np.zeros((n, pixels), bool)
    area = np.zeros((n, pixels), np.float32)
    coords = np.zeros((n, pixels, 2), np.int32)
    for lo, ix, f, z in batches(ids, True):
        base = z-torch.logsumexp(z[...,:150], -1, keepdim=True)
        y = torch.from_numpy(gt[ix].astype(np.int64)).cuda().clamp(max=149)
        true = z.gather(-1, y[...,None])
        true_score = base.gather(-1, y[...,None]).squeeze(-1)
        # Match historical stable ranking, including label-index tie breaking.
        rank0 = true_ranks(base[...,:150], y)
        rank1 = true_ranks(base, y)
        fields = [true_score < threshold, (base[...,:150] >= threshold).sum(-1),
                  (base >= threshold).sum(-1), rank0, rank1, z[...,:150].argmax(-1) != y]
        values[lo:lo+len(ix)] = torch.stack(fields, -1).cpu().numpy()
        features[lo:lo+len(ix)] = feature_values(f, z[...,:150]).cpu().numpy()
        for j, image_id in enumerate(ix):
            m = meta['meta'][image_id]
            lab = np.array(Image.open(Path('data/ADEChallengeData2016/annotations/validation')/m['file'].replace('.jpg','.png')))
            assert lab.shape == (m['H'],m['W'])
            flat = np.random.default_rng(meta['pixseed']+int(image_id)).choice(lab.size, pixels, replace=False)
            recovered = lab.ravel()[flat].astype(int)-1
            recovered[recovered < 0] = 255
            assert np.array_equal(recovered, gt[image_id]), 'Pixel-coordinate reconstruction mismatch'
            coords[lo+j] = np.stack(np.unravel_index(flat, lab.shape), -1)
            boundaries[lo+j], area[lo+j] = spatial_strata(lab, flat, meta['short'])
        if lo%80 == 0:
            print(f'Pixel audit: {lo+len(ix)}/{n}', flush=True)
    valid = gt[ids] < 150
    all_image = (values*valid[...,None]).sum(1)/valid.sum(1)[:,None]
    saved = np.load(PRIOR/'per_image.npz')['evaluation']
    np.testing.assert_allclose(all_image[:,0], saved[0,0,:,0], atol=1e-7)
    np.testing.assert_allclose(all_image[:,1], saved[0,0,:,1], atol=1e-5)
    np.testing.assert_allclose(all_image[:,2], saved[0,-1,:,1]+saved[0,-1,:,2], atol=1e-5)
    np.testing.assert_allclose(all_image[:,3], saved[0,0,:,3], atol=1e-5)
    np.testing.assert_allclose(all_image[:,4], saved[0,-1,:,3], atol=1e-5)
    groups = [('all', 'all', valid), ('boundary', 'near', valid&boundaries), ('boundary', 'interior', valid&~boundaries)]
    for k, name in enumerate(['small_<1%', 'medium_1-10%', 'large_>=10%']):
        code = np.digitize(area, [.01,.1])
        groups.append(('class_area', name, valid&(code==k)))
    for k, feature in enumerate(FEATURES):
        codes = np.digitize(features[...,k], edges[k])
        groups += [(feature, f'Q{b+1}', valid&(codes==b)) for b in range(5)]
    rows, per_groups = [], []
    for family, name, mask in groups:
        count = mask.sum(1)
        sums = (values*mask[...,None]).sum(1)
        per = np.divide(sums, count[:,None], out=np.full_like(sums,np.nan,dtype=float), where=count[:,None]>0)
        occupancy = count/valid.sum(1)
        contributions = sums/valid.sum(1)[:,None]
        row = dict(family=family, group=name, images=int((count>0).sum()),
                   pixel_fraction=float(occupancy.mean()))
        row.update({m:float(np.nanmean(per[:,k])) for k,m in enumerate(METRICS)})
        row.update({m+'_contribution':float(contributions[:,k].mean()) for k,m in enumerate(METRICS)})
        rows.append(row)
        per_groups.append(np.c_[count, per, contributions])
    for family in ['boundary','class_area']+FEATURES:
        selected = [r for r in rows if r['family']==family]
        assert np.isclose(sum(r['pixel_fraction'] for r in selected),1)
        for metric in METRICS:
            assert np.isclose(sum(r[metric+'_contribution'] for r in selected),rows[0][metric],atol=1e-6)
    with (OUT/'groups.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    np.savez_compressed(OUT/'pixels.npz', image_ids=ids, coordinates=coords, valid=valid, gt=gt[ids],
                        metrics=values, features=features, boundary=boundaries, class_area=area)
    np.savez_compressed(OUT/'per_image.npz', groups=np.array(per_groups), baseline=all_image)
    # Paired image bootstrap for boundary/interior conditional mean differences.
    rng = np.random.default_rng(20260927)
    arr = np.array(per_groups)
    diffs = []
    for _ in range(1000):
        draw = rng.integers(0,n,n)
        diffs.append(np.nanmean(arr[1,draw,1:7],0)-np.nanmean(arr[2,draw,1:7],0))
    ci = np.quantile(diffs,[.025,.975],axis=0).T
    (OUT/'checks.json').write_text(json.dumps(dict(
        coordinate_label_matches=n, baseline_risk_size_rank_reproduced=True, partition_accounting=True,
        boundary_minus_interior_conditional_bootstrap95=dict(zip(METRICS,ci.tolist()))),indent=2))
    fig, axes = plt.subplots(2, 3, figsize=(13,7))
    for ax, family in zip(axes.flat, ['boundary','class_area']+FEATURES):
        rr = [r for r in rows if r['family']==family]
        xx = np.arange(len(rr))
        ax.bar(xx,[r['source_size'] for r in rr], color='steelblue', alpha=.8)
        ax.set_xticks(xx,[r['group'] for r in rr], rotation=15); ax.set_title(family)
        ax.set_ylabel('Source labels per pixel')
        right = ax.twinx(); right.plot(xx,[100*r['miss'] for r in rr], 'o-', color='darkred')
        right.set_ylabel('Miss rate (%)', color='darkred')
    fig.suptitle('Frozen baseline: image-averaged conditional metrics; associations, not effects')
    fig.tight_layout(); fig.savefig(OUT/'pixel_strata.png',dpi=180); plt.close(fig)
    # First three evaluation images in saved split order, not selected by outcome.
    fig, axes = plt.subplots(3,3,figsize=(12,10))
    for i in range(3):
        m = meta['meta'][ids[i]]
        img = np.array(Image.open(Path('data/ADEChallengeData2016/images/validation')/m['file']))
        for ax in axes[i]: ax.imshow(img); ax.axis('off')
        axes[i,0].set_title(m['file'])
        v = valid[i]
        sc = axes[i,1].scatter(coords[i,v,1],coords[i,v,0],c=values[i,v,1],s=2,vmin=0,vmax=100,cmap='viridis')
        axes[i,1].set_title('Sampled source set sizes (0-100)')
        miss = v&(values[i,:,0]>0)
        axes[i,2].scatter(coords[i,miss,1],coords[i,miss,0],c='red',s=4)
        axes[i,2].set_title('Missed true labels at sampled pixels')
    fig.tight_layout(); fig.savefig(OUT/'sampled_examples.png',dpi=160); plt.close(fig)
    lines = ['# Pixel-level diagnosis of fixed-source softmax', '',
        'Frozen baseline on 400 previously inspected development evaluation images; no score, calibration or model changed. Feature quintiles are determined on the separate 800 fitting images.', '',
        '| Group | Pixel share | Miss % | Source size | +695 size | Source rank |', '|---|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['family']}: {r['group']} | {100*r['pixel_fraction']:.1f}% | {100*r['miss']:.2f} | {r['source_size']:.2f} | {r['expanded_size']:.2f} | {r['source_rank']:.2f} |")
    lines += ['', 'Each row averages pixels within an image, then images with pixels in that stratum. Pixel shares use all valid pixels and average images. Group rates do not add to the overall rate; additive contributions are saved in groups.csv.', '',
        '## Spatial definitions and verification', '',
        'Every sampled evaluation label was exactly reproduced from its original mask using the original seed and dimensions. A boundary is a change between valid 4-neighbor semantic labels. Near-boundary pixels are within 3 pixels at the encoder resize scale; ignore transitions and image borders are not counted. Class area is semantic-class area, not object-instance size.', '',
        'Feature norm describes interpolated/crop-averaged features. Entropy, top-two gap (scaled-logit units), and maximum dot product use only the fixed150 reference labels. No active-vocabulary statistic is introduced. Groupings based on ground truth are diagnostic only.', '',
        'Baseline image-level risks, source/expanded set sizes and ranks reproduce the saved experiment; all grouping contributions sum back to the baseline. Paired image-bootstrap boundary/interior intervals are in checks.json, conditional on the frozen model and calibration.', '',
        'These associations are confounded by class identity, image content and region size. They do not demonstrate that smoothing, feature renormalization or adaptive temperature will improve results. Any intervention needs independent tuning, recalibration and vocabulary-invariance checks. No reserved confirmation data accessed.', '',
        'pixel_strata.png summarizes group metrics. sampled_examples.png shows the first three evaluation images in saved split order, with sparse sampled-pixel overlays rather than dense predictions. pixels.npz stores coordinates, features and outcomes for reproducibility.', '',
        'Run: `.venv/Scripts/python.exe src/diagnose_pixels.py`', '']
    (OUT/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print('\n'.join(lines[:13]),flush=True)


if __name__ == '__main__':
    main()
