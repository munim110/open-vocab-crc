"""Native FC-CLIP source-label scores with a large known lexicon deployed (FC-CLIP counterpart of exp_lexicon_probe.py and
exp_lexicon_probe_sed.py, read by exp_adaptive_vocab.py --tag fcclip_bank683).

Same lexicons as the CAT-Seg and SED runs: the 845 evaluated names followed by Open Images names (meta/distractors_openimages_v1.json,
seed-1 permutation, no evaluated label among them) up to 1,690, 3,380, 6,760 and 17,001 names. Same 2,000 ADE validation
images and pixel samples as the FC-CLIP headroom probe (results/headroom_probe_ade_fcclip_bank683 and _rest); calibration
needs only the source-label loss, so only the 150 source columns are stored, as log(score + 1e-8) clamped to [-30, 30] in
float16 like every FC-CLIP store.

FC-CLIP's per-query logits (in- and out-of-vocabulary) and its masks do not depend on the other candidates (checked in
exp_fcclip_probe.py --check for the bank columns; --check here repeats it for the lexicon columns), so one forward pass with
the text classifier of the whole 17,001-name lexicon gives the released semantic inference at every lexicon: the softmaxes
over the deployed vocabulary, the geometric ensemble (alpha for COCO training names, beta otherwise) and the void term are
taken over the first N names, exactly as exp_fcclip_probe.native does over the deployed vocabulary. Runs in .venv-fcclip.
Development data (ADE validation); nothing is fitted; the confirmation reserve is not read.

    PYTHONPATH=src python src/exp_lexicon_probe_fcclip.py [--check] [--limit N] [--lexicons 1690,3380,6760,17001]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from encode import ADE, sample_phi
from exp_adaptive_vocab_probe import S, T
from exp_fcclip_probe import CKPT, load_model, resize_shortest, text_classifier
from exp_fixed_source import digest
from natural_vocab import load_manifest
from probe_checkpoint import Checkpoint

LEXICONS = [1690, 3380, 6760, 17001]
TAG = 'fcclip_bank683'


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--lexicons', default=','.join(map(str, LEXICONS)))
    ap.add_argument('--check', action='store_true', help='first images: lexicon columns leave logits and masks unchanged; native at 150 / 845 names vs the stored scores')
    ap.add_argument('--check-images', type=int, default=3)
    a = ap.parse_args()
    lexicons = [int(v) for v in a.lexicons.split(',')]
    assert all(n in LEXICONS for n in lexicons) and lexicons == sorted(lexicons)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{TAG}', f'results/headroom_probe_ade_{TAG}_rest']
    caches = [f'cache/headroom_probe_{TAG}', f'cache/headroom_probe_{TAG}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p['model'] == 'fcclip' for p in protos)
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT = Path(f'results/lexicon_probe_{TAG}'); STORE = Path(f'cache/lexicon_{TAG}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(names) == T
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    oi = [oi[i] for i in np.random.default_rng(1).permutation(len(oi))]
    assert not set(oi) & set(names) and T+len(oi) == LEXICONS[-1]
    lexicon = (names+oi)[:max(lexicons)]
    meta = json.loads(Path('cache/sclip/meta.json').read_text())

    from detectron2.data import MetadataCatalog
    from detectron2.structures import ImageList
    model, cfg = load_model()                                                                                  # puts the FC-CLIP checkout on sys.path
    from fcclip.modeling.pixel_decoder.ops.functions.ms_deform_attn_func import MSDA_AVAILABLE
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    model.set_metadata(MetadataCatalog.get(f'vscrc_ade_natural_{T}').set(stuff_classes=list(names)))
    train_names = {s for c in model.train_metadata.stuff_classes for s in c.replace(', ', ',').split(',')}   # FC-CLIP's split_labels
    overlap = torch.tensor([n in train_names for n in lexicon], device=model.device)
    assert torch.equal(overlap[:T], model.category_overlapping_mask.to(model.device).bool()) and not model.ensemble_on_valid_mask
    ens = torch.where(overlap, model.geometric_ensemble_alpha, model.geometric_ensemble_beta).double()
    t0 = time.time()
    text_lex, nt_lex = text_classifier(model, [[n] for n in lexicon])
    void = F.normalize(model.void_embedding.weight, dim=-1)
    text = torch.cat([text_lex, void], 0)                                                                      # [max lexicon + 1, D], void last
    print(f'text {tuple(text.shape)} in {time.time()-t0:.0f}s', flush=True)
    mean, std = model.pixel_mean, model.pixel_std

    def forward(images, text, nt):
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']                                         # [Q, N+1], [1, Q, h, w]
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        return mask_cls, out_cls, mask_pred

    def image(index, text=text, nt=nt_lex):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        mask_cls, out_cls, mask_pred = forward(images, text, nt)
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
        ih, iw = images.image_sizes[0]
        m = sample_phi(up[None, :, :ih, :iw], y, x, H, W).double().sigmoid()                                   # [P, Q] query masks at the sampled pixels
        return mask_cls.double(), out_cls.double(), m, mask_pred

    def source_scores(in_l, out_l, m, n):
        """Released semantic inference with the first n lexicon names deployed (exp_fcclip_probe.native over that vocabulary), source columns [P, S]."""
        e = ens[:n]
        in_p, out_p = in_l[:, :n].softmax(-1), out_l[:, :n].softmax(-1)
        cls = (in_p**(1-e)*out_p**e).log()
        void = torch.cat([in_l[:, :n], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return ((m@(cls.softmax(-1)*(1-void))[:, :S])+1e-8).log().clamp(-30, 30).half().cpu().numpy()

    def stored(parts, k):
        for part in parts:
            if k < len(part): return part[k]
            k -= len(part)

    if a.check:
        native845 = [np.load(f'{c}/native845.npy', mmap_mode='r') for c in caches]
        native150 = [np.load(f'{c}/native150.npy', mmap_mode='r') for c in caches]
        report = []
        for k in range(min(a.check_images, len(ids))):
            in_l, out_l, m, pred = image(ids[k])
            c_in, c_out, c_m, c_pred = image(ids[k], torch.cat([text[:T], void]), nt_lex[:T])              # the 845 names + void alone
            d150 = np.abs(source_scores(in_l, out_l, m, S).astype(np.float32)-np.array(stored(native150, k))[:, :S].astype(np.float32))
            d845 = np.abs(source_scores(in_l, out_l, m, T).astype(np.float32)-np.array(stored(native845, k))[:, :S].astype(np.float32))
            report.append(dict(image=ids[k], lexicon_columns_in_logits_max_abs_diff=float((in_l[:, :T]-c_in[:, :T]).abs().max()),
                               lexicon_columns_void_logit_max_abs_diff=float((in_l[:, -1]-c_in[:, -1]).abs().max()),
                               lexicon_columns_out_logits_max_abs_diff=float((out_l[:, :T]-c_out[:, :T]).abs().max()),
                               lexicon_columns_masks_max_abs_diff=float((pred-c_pred).abs().max()),
                               native150_max_abs_diff=float(d150.max()), native150_mean_abs_diff=float(d150.mean()),
                               native845_max_abs_diff=float(d845.max()), native845_mean_abs_diff=float(d845.mean())))
            print(json.dumps(report[-1]), flush=True)
        (OUT/'check.json').write_text(json.dumps(dict(vocabulary=len(lexicon), source=S, msdeform_attn_cuda_kernel=MSDA_AVAILABLE, images=report), indent=2))
        return

    protocol = dict(image_ids=ids, tag=TAG, model='fcclip', size='convnext_large', lexicon_sizes=lexicons,
                    lexicon='845 evaluated names, then Open Images names (distractors_openimages_v1, seed-1 permutation) up to each size',
                    native='Released semantic inference over the first N lexicon names: in-/out-of-vocabulary logits softmaxed over them, geometric ensemble '
                           '(alpha for COCO panoptic training names, beta otherwise), softmaxed, times one minus the void probability; masks weighted by the result.',
                    stores=f'cache/lexicon_{TAG}/lex<N>.npy: float16 log(score + 1e-8) clamped to [-30, 30] of the 150 source names [image, pixel, 150] with the N-name lexicon deployed',
                    msdeform_attn='compiled CUDA kernel' if MSDA_AVAILABLE else 'PyTorch reference path (ms_deform_attn_core_pytorch; no CUDA toolkit on this machine)',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_lexicon_probe_fcclip.py', 'src/exp_fcclip_probe.py', 'meta/natural_vocab_v1.json',
                                                              'meta/distractors_openimages_v1.json', str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    ckpt = Checkpoint(STORE, protocol)
    stores = ckpt.open_stores({f'lex{n}': ((len(ids), meta['npix'], S), np.float16) for n in lexicons})
    seconds = np.zeros(len(lexicons)+1); ckpt.restore(seconds=seconds)                                        # forward pass, then one entry per lexicon
    t_start = time.time()
    for k, index in enumerate(ids):
        if k < ckpt.start: continue
        torch.cuda.synchronize(); t0 = time.perf_counter()
        in_l, out_l, m, _ = image(index)
        torch.cuda.synchronize(); seconds[0] += time.perf_counter()-t0
        for j, n in enumerate(lexicons):
            torch.cuda.synchronize(); t0 = time.perf_counter()
            stores[f'lex{n}'][k] = source_scores(in_l, out_l, m, n)
            torch.cuda.synchronize(); seconds[j+1] += time.perf_counter()-t0
        if k % 25 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
        ckpt.step(k, seconds=seconds)
    result = dict(images=len(ids), seconds_per_image=dict(forward=float(seconds[0]/len(ids)), **{str(n): float(v/len(ids)) for n, v in zip(lexicons, seconds[1:])}),
                  gpu=torch.cuda.get_device_name(0), peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, msdeform_attn=protocol['msdeform_attn'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    ckpt.finish()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
