"""Mask-classification family demonstration: FC-CLIP (NeurIPS 2023, ConvNeXt-L, released COCO panoptic weights).

Same stored-score format as exp_headroom_probe.py (three stores at the cached sampled pixels, protocol.json with the
image ids), so exp_headroom_splits.py and exp_added_label_risk.py run unchanged with --tag fcclip.

FC-CLIP scores a pixel for label c as sum_q P(c|q) m_q(pixel): query masks m_q (vocabulary-independent) weighted by a
per-query class distribution. The released P(c|q) is candidate-dependent three times over: the in-vocabulary and
out-of-vocabulary (mask-pooled CLIP) logits are each softmaxed over the deployed vocabulary, geometrically ensembled,
softmaxed again, and scaled by a void probability from a softmax over the vocabulary plus void. The per-query per-label
logits and the masks never see the other candidates, so the conversion is the same recipe as for CAT-Seg: every label
is normalised against a fixed reference bank instead of the deployed candidates. The bank is FC-CLIP's own training
vocabulary (COCO panoptic, 133 classes with the released synonym lists); each softmax over the vocabulary becomes a
softmax over {label} + bank (the label's own bank entry, if any, removed from the bank side), the void term a softmax
over bank + void. For a label in the bank this is the released pipeline run on the training vocabulary (exactly so when
its bank entry has no extra synonyms; FC-CLIP takes the max over synonyms).
Stored under the 'anchored845' name; stores hold log(score + 1e-8) clamped to [-30, 30] in float16 (scores are
mask-weighted sums, not probabilities; the harness only needs a monotone transform).

Runs in .venv-fcclip on the GH200 (scripts/setup_models.sh; open_clip_torch 2.20.0, FC-CLIP's own text path
assumes the pre-batch-first transformer); the checkout and checkpoint live under ~/third_party_probe, outside the
repository (locally: ../third_party_probe, with MSDeformAttn on its PyTorch reference path, no CUDA toolkit). Development
data (ADE validation); no fitting, no reserve access.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from encode import ADE, sample_phi
from exp_fixed_source import digest
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

TP = Path(os.path.expanduser('~/third_party_probe'))                                     # GH200 layout ...
if not TP.exists(): TP = Path(__file__).resolve().parents[2]/'third_party_probe'          # ... or next to the repo, like CAT-Seg and SED
FCCLIP = TP/'fc-clip'
CKPT = TP/'fcclip_cocopan_convnext_large.pth'
CONFIG = 'configs/coco/panoptic-segmentation/fcclip/fcclip_convnext_large_eval_a847.yaml'
ARMS = ['fcclip_native', 'fcclip_anchored']
METRICS = ['source_rank', 'expanded_rank', 'source_top1', 'source_top10', 'expanded_top1', 'expanded_top10', 'expanded_top50']
S, T = 150, 845


def load_model():
    """Released FC-CLIP with the a847 evaluation config; datasets register from paths relative to the checkout."""
    sys.path.insert(0, str(FCCLIP)); cwd = os.getcwd(); os.chdir(FCCLIP)
    try:
        from detectron2.checkpoint import DetectionCheckpointer
        from detectron2.config import get_cfg
        from detectron2.modeling import build_model
        from detectron2.projects.deeplab import add_deeplab_config
        from fcclip import add_fcclip_config, add_maskformer2_config
        cfg = get_cfg(); add_deeplab_config(cfg); add_maskformer2_config(cfg); add_fcclip_config(cfg)
        cfg.merge_from_file(CONFIG); cfg.MODEL.WEIGHTS = str(CKPT); cfg.freeze()
        model = build_model(cfg); DetectionCheckpointer(model).load(cfg.MODEL.WEIGHTS); model.eval()
    finally:
        os.chdir(cwd)
    return model, cfg


def text_classifier(model, class_lists):
    """FC-CLIP's classifier for classes given as synonym lists: 14 templates averaged per synonym (get_text_classifier)."""
    from fcclip.fcclip import VILD_PROMPT
    texts = [t.format(s) for syns in class_lists for s in syns for t in VILD_PROMPT]
    emb = torch.cat([model.backbone.get_text_classifier(texts[i:i+128], model.device).detach() for i in range(0, len(texts), 128)])
    emb = F.normalize(emb, dim=-1).reshape(-1, len(VILD_PROMPT), emb.shape[-1]).mean(1)
    return F.normalize(emb, dim=-1), [len(syns) for syns in class_lists]


def resize_shortest(img, short=800, long_max=1333):
    """detectron2 ResizeShortestEdge at the config defaults (INPUT.MIN_SIZE_TEST 800, MAX_SIZE_TEST 1333)."""
    w, h = img.size
    scale = min(short/min(h, w), long_max/max(h, w))
    return img.resize((int(w*scale+.5), int(h*scale+.5)), Image.BILINEAR)


def pixel_metrics(source, expanded, target):
    r0, r1 = true_ranks(source, target), true_ranks(expanded, target)
    return torch.stack([r0, r1, r0 == 1, r0 <= 10, r1 == 1, r1 <= 10, r1 <= 50], -1).double().cpu().numpy()


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--roles', default='tune_cal,tune_eval')
    ap.add_argument('--tag', default='fcclip')
    ap.add_argument('--check', action='store_true', help='first image: verify the bank columns leave the native logits and masks unchanged')
    ap.add_argument('--extra-bank', default='', help='json with "names": reference names added to the training vocabulary (e.g. meta/bank_coco_oi683_v1.json)')
    ap.add_argument('--dataset', default='ade', choices=['ade', 'pascal', 'coco'], help='ADE 150 -> 845 (default), Pascal Context 59 -> 458 or COCO-Stuff 171 -> + LVIS (all 2,000 cached images; --roles ignored)')
    ap.add_argument('--time-native-only', action='store_true', help='also time the native deployment pass without bank columns (candidates + void), '
                    'the same steps as backbone_masks_and_logits; stored as native_only_features')
    a = ap.parse_args()
    global S, T
    pascal, coco = a.dataset == 'pascal', a.dataset == 'coco'
    OUT, STORE = Path(f'results/headroom_probe_{a.dataset}_{a.tag}'), Path(f'cache/headroom_probe_{"" if a.dataset == "ade" else a.dataset+"_"}{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    if pascal:
        import pascal_labels as PL
        import scipy.io as sio
        from pascal_natural_vocab import load_manifest as load_pascal_manifest
        S, T = 59, 458
        rows = load_pascal_manifest()['rows']
        sclip_dir, gt_file, store_names, manifest_path = 'cache/pascal_sclip', 'gt59.npy', ('native_source', 'native_full', 'anchored_full'), 'meta/pascal_natural_vocab_v1.json'
        coarse_lut, _ = PL.luts()
    elif coco:
        from coco_lvis_vocab import load_manifest as load_coco_manifest
        rows = load_coco_manifest()['rows']; S, T = 171, len(rows)
        sclip_dir, gt_file, store_names, manifest_path = 'cache/coco_pixels', 'gt171.npy', ('native_source', 'native_full', 'anchored_full'), 'meta/coco_lvis_natural_vocab_v1.json'
        gt_lvis = np.load('cache/coco_pixels/gtlvis.npy')
    else:
        rows = load_manifest()['rows']
        sclip_dir, gt_file, store_names, manifest_path = 'cache/sclip', 'gt150.npy', ('native150', 'native845', 'anchored845'), 'meta/natural_vocab_v1.json'
    meta = json.loads(Path(f'{sclip_dir}/meta.json').read_text())
    if pascal or coco:
        ids = list(range(a.limit or len(meta['meta'])))
    else:
        split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
        ids = [r['index'] for role in a.roles.split(',') for r in split['roles'][role]]
        if a.limit: ids = ids[:a.limit]
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(names) == T and not any(',' in n for n in names)

    from detectron2.data import MetadataCatalog
    from detectron2.structures import ImageList
    model, cfg = load_model()
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    model.set_metadata(MetadataCatalog.get(f'vscrc_{a.dataset}_natural_{T}').set(stuff_classes=list(names)))   # one name per label, no synonym lists
    bank_lists = [c.replace(', ', ',').split(',') for c in model.train_metadata.stuff_classes]        # COCO panoptic 133 with FC-CLIP's synonyms
    B0, extras = len(bank_lists), []
    if a.extra_bank:                                                                                    # larger reference bank: training vocabulary + extra names (one name each)
        known = {s.lower() for syns in bank_lists for s in syns}
        extras = [n for n in json.loads(Path(a.extra_bank).read_text())['names'] if n.lower() not in known]
        bank_lists = bank_lists+[[n] for n in extras]
    B = len(bank_lists)
    text_cand, nt_cand = text_classifier(model, [[n] for n in names])
    text_bank, nt_bank = text_classifier(model, bank_lists)
    text = torch.cat([text_cand, text_bank, F.normalize(model.void_embedding.weight, dim=-1)], 0)     # [845 + synonyms + 1, D], void last
    nt = nt_cand+nt_bank                                                                                # logits: [Q, 845 + B + 1]
    self_idx = torch.tensor([next((j for j, syns in enumerate(bank_lists) if n in syns), -1) for n in names], device=model.device)
    overlap = model.category_overlapping_mask.to(model.device).bool()
    assert torch.equal(overlap, (self_idx >= 0) & (self_idx < B0)) and B0 == 133 and not model.ensemble_on_valid_mask
    alpha, beta = model.geometric_ensemble_alpha, model.geometric_ensemble_beta
    ens = torch.where(overlap, alpha, beta).double()                                                    # out-of-vocab weight per label
    ens_bank = torch.where(torch.arange(B, device=model.device) < B0, alpha, beta).double()             # same rule for the bank entries (extras are out-of-vocab)
    bank_mask = torch.zeros(T, B, dtype=torch.double, device=model.device)                              # -inf removes a label's own bank entry
    bank_mask[self_idx >= 0, self_idx[self_idx >= 0]] = -float('inf')
    bank_name = 'fcclip_coco_panoptic_133'+(f'_plus_{len(extras)}_{Path(a.extra_bank).stem}' if extras else '')
    protocol = dict(image_ids=ids, arms=ARMS, metrics=METRICS, model='fcclip', size='convnext_large', bank=bank_name, bank_size=B, extra_bank=a.extra_bank,
        images='the 2,000 cached Pascal Context validation images (development data); no filtering.' if pascal else 'the first 2,000 COCO val2017 images annotated by LVIS v1 val, sorted by file name (development data); no filtering.' if coco else f'roles {a.roles} of the saved match-correction split (ADE validation, development data); no filtering.',
        wording=f'{a.dataset}-natural-v1 prompts for every arm, FC-CLIP\'s 14 ViLD templates averaged (its released prompt engineering).',
        catseg='Released FC-CLIP ConvNeXt-L (COCO panoptic weights), a847 evaluation config: shortest edge 800 (max 1333), 250 queries, geometric ensemble alpha .4 (COCO names) / beta .8 (other names).',
        native='Released semantic inference: in-/out-of-vocabulary logits softmaxed over the deployed vocabulary, ensembled, softmaxed, times one minus the void probability; masks weighted by the result. Source scores use the {S}-label softmaxes, expanded scores the {T}-label ones.'.replace('{S}', str(S)).replace('{T}', str(T)),
        anchored='Reference-anchored conversion (stored as anchored845): every softmax over the deployed vocabulary becomes a softmax over {label} + the reference bank (the training vocabulary, COCO panoptic 133 with released synonyms'+(f', plus {len(extras)} extra names from {a.extra_bank} not among those synonyms' if extras else '')+'; the label\'s own entry removed from the bank side), the void term a softmax over bank + void; same ensemble weights (alpha for training names, beta otherwise, on candidates and bank entries alike). Candidate-independent by construction; equals the released pipeline run on the bank vocabulary for bank labels (up to FC-CLIP\'s max over synonyms).',
        stores='log(score + 1e-8) clamped to [-30, 30]; scores are mask-weighted sums (not probabilities).',
        reference_overlap=f'{int(overlap[:S].sum())} of {S} source prompts and {int(overlap.sum())} of {T} prompts are COCO panoptic training names.',
        scope=f'Development images ({"Pascal Context" if pascal else "COCO val2017" if coco else "ADE"} validation); no fitting, no calibration, no reserve access. FC-CLIP was trained on COCO panoptic (train2017); these images are unseen by it.',
        hashes={str(p): digest(Path(p)) for p in ['src/exp_fcclip_probe.py', manifest_path, str(CKPT)]+([a.extra_bank] if a.extra_bank else [])})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))

    gt = np.load(f'{sclip_dir}/{gt_file}')
    stores = {k: np.lib.format.open_memmap(STORE/f'{k}.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], n))
              for k, n in zip(store_names, (S, T, T))}
    values = np.full((len(ARMS), len(ids), len(METRICS)), np.nan)
    confusion = np.zeros((len(ARMS), S, S), np.int64)
    seconds = np.zeros(5)
    native_only_seconds = 0.0
    text_native = torch.cat([text_cand, text[-1:]])                                                       # candidates + void, as in --check
    mean, std = model.pixel_mean, model.pixel_std

    def native(in_l, out_l, V, e=None):
        """Released per-query class probabilities over the first V labels [Q, V] (fcclip.py forward, eval branch)."""
        in_p, out_p = in_l[:, :V].softmax(-1), out_l[:, :V].softmax(-1)
        e = ens[:V] if e is None else e
        cls = (in_p**(1-e)*out_p**e).log()
        void = torch.cat([in_l[:, :V], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return cls.softmax(-1)*(1-void)

    def vs_bank(cand, bank):
        """log P(label | {label} + bank) per query for each candidate [Q, T]; bank entries of the label itself removed."""
        lse = torch.logsumexp(bank[:, None, :]+bank_mask, -1)                                        # [Q, T]
        return cand-torch.logaddexp(cand, lse)

    def log_softmax_out_bank(out_l):
        return out_l[:, T:T+B].log_softmax(-1)

    def anchored(in_l, out_l):
        """Reference-anchored per-query class probabilities for all 845 labels [Q, T]."""
        lp_in, lp_out = vs_bank(in_l[:, :T], in_l[:, T:T+B]), vs_bank(out_l[:, :T], out_l[:, T:T+B])
        g = (1-ens)*lp_in+ens*lp_out                                                                   # ensembled log-probability of each candidate
        g_bank = (1-ens_bank)*in_l[:, T:T+B].log_softmax(-1)+ens_bank*log_softmax_out_bank(out_l)      # released pipeline on the bank vocabulary
        void = torch.cat([in_l[:, T:T+B], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return vs_bank(g, g_bank).exp()*(1-void)

    def forward(images, text, nt):
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']                                  # [Q, N+1], [1, Q, h, w]
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        return mask_cls, out_cls, mask_pred

    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        if pascal:
            img = Image.open(Path(PL.VOC)/'JPEGImages'/(info['file']+'.jpg')).convert('RGB')
            coarse = coarse_lut[np.clip(sio.loadmat(str(Path(PL.PC)/'trainval'/(info['file']+'.mat')))['LabelMap'].astype(np.int64), 0, 511)]
            np.testing.assert_array_equal(coarse.ravel()[flat], gt[index])
        elif coco:
            img = Image.open(Path('data/coco-stuff/images/val2017')/info['file']).convert('RGB')
            stuff = np.array(Image.open(Path('data/coco-stuff/annotations_detectron2/val2017')/info['file'].replace('.jpg', '.png')))
            np.testing.assert_array_equal(np.where(gt_lvis[index] != 65535, 255, stuff.ravel()[flat]), gt[index])
        else:
            img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
            lab = np.array(Image.open(Path(ADE)/'annotations/validation'/info['file'].replace('.jpg', '.png')))
            np.testing.assert_array_equal(np.where(lab.ravel()[flat] > 0, lab.ravel()[flat].astype(int)-1, 255), gt[index])
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        torch.cuda.synchronize(); t0 = time.perf_counter()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        mask_cls, out_cls, mask_pred = forward(images, text, nt)
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
        ih, iw = images.image_sizes[0]
        m = sample_phi(up[None, :, :ih, :iw], y, x, H, W).double().sigmoid()                              # [P, Q] query masks at the sampled pixels
        in_l, out_l = mask_cls.double(), out_cls.double()
        torch.cuda.synchronize(); t1 = time.perf_counter()
        n150 = m@native(in_l, out_l, S)
        torch.cuda.synchronize(); t15 = time.perf_counter()     # the source pass is calibration-only; deployment runs the grown pass alone
        n845 = m@native(in_l, out_l, T)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        anch = m@anchored(in_l, out_l)
        torch.cuda.synchronize(); t3 = time.perf_counter()
        seconds += [t1-t0, t2-t1, t3-t2, t15-t1, t2-t15]
        if a.time_native_only:                                                                            # what native deployment runs: no bank columns
            torch.cuda.synchronize(); t4 = time.perf_counter()
            n_cls, n_out, n_pred = forward(images, text_native, nt_cand)
            n_up = F.interpolate(n_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
            sample_phi(n_up[None, :, :ih, :iw], y, x, H, W).double().sigmoid(); n_cls.double(); n_out.double()
            torch.cuda.synchronize(); native_only_seconds += time.perf_counter()-t4
        if a.check and k == 0:                                                                            # the bank columns must not touch the native quantities
            c_cls, c_out, c_pred = forward(images, torch.cat([text_cand, text[-1:]]), nt_cand)
            for u, v in [(c_cls[:, :T], mask_cls[:, :T]), (c_cls[:, -1], mask_cls[:, -1]), (c_out[:, :T], out_cls[:, :T]), (c_pred, mask_pred)]:
                assert torch.allclose(u, v, atol=1e-4), float((u-v).abs().max())
            single = torch.tensor([len(s) == 1 for s in bank_lists], device=model.device)                 # bank classes without extra synonyms (max over synonyms otherwise)
            j = torch.nonzero((self_idx >= 0) & single[self_idx.clamp(min=0)])[:, 0]                        # such labels: anchored == released pipeline on the bank
            ref = native(torch.cat([in_l[:, T:T+B], in_l[:, -1:]], -1), out_l[:, T:T+B], B, ens_bank)
            assert torch.allclose(anchored(in_l, out_l)[:, j], ref[:, self_idx[j]], atol=1e-6), 'anchored != native on the bank'
            print(f'check ok: bank columns leave native logits/masks unchanged; anchored equals native on the bank vocabulary ({len(j)} single-synonym bank labels, bank {B})', flush=True)
        for name, scores in zip(store_names, (n150, n845, anch)):
            stores[name][k] = (scores+1e-8).log().clamp(-30, 30).half().cpu().numpy()
        valid = gt[index] < S
        target = torch.from_numpy(gt[index].astype(np.int64)).cuda().clamp(max=S-1)
        for ai, (source, expanded) in enumerate([(n150, n845), (anch[:, :S], anch)]):
            pix = pixel_metrics(source, expanded, target)
            if valid.any(): values[ai, k] = pix[valid].mean(0)
            pred = source.argmax(-1).cpu().numpy()[valid]
            np.add.at(confusion[ai], (gt[index][valid].astype(int), pred), 1)
        if k % 20 == 0:
            print(f'{k+1}/{len(ids)} source top10 '+' '.join(f'{ARMS[i]}={values[i, k, 3]:.3f}' for i in range(2)), flush=True)
    for s in stores.values(): s.flush()
    np.savez_compressed(OUT/'per_image.npz', values=values, image_ids=ids, confusion=confusion)

    iou = []
    for c in confusion:
        inter = np.diag(c); union = c.sum(0)+c.sum(1)-inter
        iou.append(float(np.mean(inter[union > 0]/union[union > 0])))
    result = dict(rows=[dict(arm=arm, group='all', mean=np.nanmean(values[ai], 0).tolist()) for ai, arm in enumerate(ARMS)],
                  sampled_pixel_miou=dict(zip(ARMS, iou)), pixel_accuracy={a_: float(np.diag(c).sum()/c.sum()) for a_, c in zip(ARMS, confusion)},
                  mean_seconds_per_image=dict(backbone_masks_and_logits=seconds[0]/len(ids), native_150_plus_845=seconds[1]/len(ids), anchored_845=seconds[2]/len(ids),
                                             native_150=seconds[3]/len(ids), native_845=seconds[4]/len(ids),
                                             **({'native_only_features': native_only_seconds/len(ids)} if a.time_native_only else {})),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30)
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = [f'# Ranking headroom probe: FC-CLIP (mask-classification family), {"Pascal Context 59 -> 458" if pascal else f"COCO-Stuff 171 -> {T}" if coco else "ADE 150 -> 845"}', '', f'{len(ids)} development images ({"all cached images" if pascal or coco else "roles "+a.roles}), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.', '',
             f'| Arm | Source rank | Rank at +{T-S} | Source top1 | Source top10 | +{T-S} top1 | +{T-S} top10 | +{T-S} top50 |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        m_ = r['mean']; lines.append(f"| {r['arm']} | {m_[0]:.2f} | {m_[1]:.2f} | "+' | '.join(f'{100*v:.2f}%' for v in m_[2:])+' |')
    lines += ['', f'| Arm | Sampled-pixel mIoU ({S}, natural wording) | Pixel accuracy |', '|---|---:|---:|']
    lines += [f"| {a_} | {100*result['sampled_pixel_miou'][a_]:.2f} | {100*result['pixel_accuracy'][a_]:.2f}% |" for a_ in ARMS]
    lines += ['', f"Seconds per image on {result['gpu']}: "+', '.join(f'{k} {v:.3f}' for k, v in result['mean_seconds_per_image'].items())+f"; peak memory {result['peak_memory_gb']:.1f} GB.",
              '', f'Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the reference bank instead and is candidate-independent by construction (its {S}-label scores are the first {S} columns of its {T}-label scores).']
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
