"""Native FC-CLIP scores under per-image vocabularies: exp_adaptive_vocab_probe.py for FC-CLIP (sec:adaptivesed).

Same images, sampled pixels, policies, column selection and store format as exp_adaptive_vocab_probe.py, so
exp_adaptive_vocab.py runs unchanged with --tag fcclip_bank683. FC-CLIP's per-query logits (in- and out-of-vocabulary)
and its masks do not depend on the other candidates (checked in exp_fcclip_probe.py --check); the candidate dependence
is in the softmaxes over the deployed vocabulary. One forward pass per image therefore gives the native scores at every
vocabulary: the released semantic inference (exp_fcclip_probe.native) applied to the vocabulary's columns. The text
classifier is built exactly as in the headroom probe run (candidates, the run's reference bank, void), so the logits are
those of the stored scores; --check compares native at 150 and 845 names with the stored native150 / native845.
Stores hold log(score + 1e-8) clamped to [-30, 30] in float16, as the FC-CLIP headroom stores do. Runs in .venv-fcclip
on the GH200. Development data (ADE validation); nothing is fitted; the confirmation reserve is not read.

    PYTHONPATH=src python src/exp_adaptive_vocab_probe_fcclip.py --tag fcclip_bank683 [--check] [--limit N]
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
from exp_adaptive_vocab_probe import IGN847, POLICIES, S, T, added_columns
from exp_fcclip_probe import CKPT, load_model, resize_shortest, text_classifier
from exp_fixed_source import digest
from natural_vocab import load_manifest


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='fcclip_bank683')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--check', action='store_true', help='compare native at 150 / 845 names with the stored scores on 3 images, then stop')
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    runs = [f'results/headroom_probe_ade_{a.tag}', f'results/headroom_probe_ade_{a.tag}_rest']
    caches = [f'cache/headroom_probe_{a.tag}', f'cache/headroom_probe_{a.tag}_rest']
    protos = [json.loads((Path(r)/'protocol.json').read_text()) for r in runs]
    assert all(p['model'] == 'fcclip' for p in protos) and len({p['extra_bank'] for p in protos}) == 1
    ids = sum([p['image_ids'] for p in protos], [])
    if a.limit: ids = ids[:a.limit]
    OUT = Path(f'results/adaptive_vocab_probe_{a.tag}'); STORE = Path(f'cache/adaptive_vocab_{a.tag}')
    OUT.mkdir(parents=True, exist_ok=True); STORE.mkdir(parents=True, exist_ok=True)

    rows = load_manifest()['rows']
    names = [r['prompt'] for r in rows]
    assert [r['role'] for r in rows[:S]] == ['source']*S and len(names) == T
    lut = np.full(IGN847+1, -1, np.int64)
    for i, r in enumerate(rows[S:]): lut[r['train_id']] = S+r.get('position', i)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt150_all, gt847_all = np.load('cache/sclip/gt150.npy'), np.load('cache/sclip/gt847.npy')
    native845 = [np.load(f'{c}/native845.npy', mmap_mode='r') for c in caches]
    native150 = [np.load(f'{c}/native150.npy', mmap_mode='r') for c in caches]

    def stored(parts, k):
        for part in parts:
            if k < len(part): return part[k]
            k -= len(part)

    def gt845(index):
        return np.where(gt150_all[index] < S, gt150_all[index].astype(np.int64), lut[gt847_all[index]])

    cols = {p: [added_columns(p, index, gt845(index), stored(native845, k)) for k, index in enumerate(ids)] for p in POLICIES}
    width = {p: max(len(c) for c in cols[p]) for p in POLICIES}

    # the headroom probe's text classifier: candidates, reference bank (training vocabulary + extra bank), void
    from detectron2.data import MetadataCatalog
    from detectron2.structures import ImageList
    model, cfg = load_model()
    from fcclip.modeling.transformer_decoder.fcclip_transformer_decoder import get_classification_logits
    model.set_metadata(MetadataCatalog.get(f'vscrc_ade_natural_{T}').set(stuff_classes=list(names)))
    bank_lists = [c.replace(', ', ',').split(',') for c in model.train_metadata.stuff_classes]
    B0, extra_bank = len(bank_lists), protos[0]['extra_bank']
    if extra_bank:
        known = {s.lower() for syns in bank_lists for s in syns}
        bank_lists = bank_lists+[[n] for n in json.loads(Path(extra_bank).read_text())['names'] if n.lower() not in known]
    assert len(bank_lists) == protos[0]['bank_size']
    text_cand, nt_cand = text_classifier(model, [[n] for n in names])
    text_bank, nt_bank = text_classifier(model, bank_lists)
    text = torch.cat([text_cand, text_bank, F.normalize(model.void_embedding.weight, dim=-1)], 0)
    nt = nt_cand+nt_bank
    overlap = model.category_overlapping_mask.to(model.device).bool()
    ens = torch.where(overlap, model.geometric_ensemble_alpha, model.geometric_ensemble_beta).double()
    mean, std = model.pixel_mean, model.pixel_std

    def native_at(in_l, out_l, m, vocab):
        """Released semantic inference over the deployed vocabulary `vocab` (exp_fcclip_probe.native on its columns)."""
        v = torch.from_numpy(vocab).cuda(); e = ens[v]
        in_p, out_p = in_l[:, v].softmax(-1), out_l[:, v].softmax(-1)
        cls = (in_p**(1-e)*out_p**e).log()
        void = torch.cat([in_l[:, v], in_l[:, -1:]], -1).softmax(-1)[:, -1:]
        return ((m@(cls.softmax(-1)*(1-void)))+1e-8).log().clamp(-30, 30).half().cpu().numpy()

    def image(index):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_shortest(img))).permute(2, 0, 1).float().cuda()
        images = ImageList.from_tensors([(tensor-mean)/std], model.size_divisibility)
        feats = model.backbone(images.tensor)
        feats['text_classifier'], feats['num_templates'] = text, nt
        out = model.sem_seg_head(feats)
        mask_cls, mask_pred = out['pred_logits'][0], out['pred_masks']
        pooled = model.mask_pooling(feats['clip_vis_dense'], F.interpolate(mask_pred, size=feats['clip_vis_dense'].shape[-2:], mode='bilinear', align_corners=False))
        out_cls = get_classification_logits(model.backbone.visual_prediction_forward(pooled), text, model.backbone.clip_model.logit_scale, nt)[0]
        up = F.interpolate(mask_pred, size=images.tensor.shape[-2:], mode='bilinear', align_corners=False)[0]
        ih, iw = images.image_sizes[0]
        m = sample_phi(up[None, :, :ih, :iw], y, x, H, W).double().sigmoid()
        return mask_cls.double(), out_cls.double(), m

    if a.check:
        report = {}
        for k, index in enumerate(ids[:3]):
            in_l, out_l, m = image(index)
            d150 = np.abs(native_at(in_l, out_l, m, np.arange(S)).astype(np.float32)-stored(native150, k).astype(np.float32))
            d845 = np.abs(native_at(in_l, out_l, m, np.arange(T)).astype(np.float32)-stored(native845, k).astype(np.float32))
            report[int(index)] = dict(native150_max_abs=float(d150.max()), native150_mean=float(d150.mean()),
                                      native845_max_abs=float(d845.max()), native845_mean=float(d845.mean()))
            print(index, report[int(index)], flush=True)
        (OUT/'check.json').write_text(json.dumps(report, indent=2))
        return

    protocol = dict(image_ids=ids, tag=a.tag, model='fcclip', size='convnext_large', policies={p: dict(kind=v[0], k=v[1]) for p, v in POLICIES.items()},
                    vocabulary='150 source names followed by the added names A(x) in manifest order; released semantic inference over exactly this list.',
                    stores='cache/adaptive_vocab_<tag>/<policy>.npy: float16 log(score + 1e-8) [image, pixel, 150+width] (source columns first, then '
                           'A(x); padding columns 0 with column index -1 in <policy>_cols.npy).',
                    scope='Development data (ADE validation). No fitting; no reserve access.',
                    added_names_per_image={p: dict(mean=float(np.mean([len(c) for c in cols[p]])), max=width[p]) for p in POLICIES},
                    hashes={str(p): digest(Path(p)) for p in ['src/exp_adaptive_vocab_probe_fcclip.py', 'src/exp_adaptive_vocab_probe.py', 'src/exp_fcclip_probe.py',
                                                              'meta/natural_vocab_v1.json', str(CKPT)] + ([extra_bank] if extra_bank else [])})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    stores = {}
    for p in POLICIES:
        stores[p] = np.lib.format.open_memmap(STORE/f'{p}.npy', mode='w+', dtype=np.float16, shape=(len(ids), meta['npix'], S+width[p]))
        c = np.full((len(ids), width[p]), -1, np.int16)
        for k, cc in enumerate(cols[p]): c[k, :len(cc)] = cc
        np.save(STORE/f'{p}_cols.npy', c)
    t_start = time.time()
    for k, index in enumerate(ids):
        in_l, out_l, m = image(index)
        for p in POLICIES:
            vocab = np.concatenate([np.arange(S), cols[p][k]])
            stores[p][k, :, :len(vocab)] = native_at(in_l, out_l, m, vocab)
            if len(vocab) < S+width[p]: stores[p][k, :, len(vocab):] = 0
        if k % 50 == 0:
            print(f'{k+1}/{len(ids)} {time.time()-t_start:.0f}s', flush=True)
    for s in stores.values(): s.flush()
    result = dict(images=len(ids), seconds_total=time.time()-t_start, gpu=torch.cuda.get_device_name(0),
                  peak_memory_gb=torch.cuda.max_memory_allocated()/2**30, added_names_per_image=protocol['added_names_per_image'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
