"""Peak GPU memory per arm, native against anchored, as the vocabulary grows (CAT-Seg ViT-B/ViT-L, CAT-Seg + DeCLIP, SED).

The peak-memory column of tab:runtime is torch.cuda.max_memory_allocated() over a whole timing run, the maximum over the
features, native and anchored passes. Here the peak is reset before each arm, so each arm is measured on its own:
  features         CLIP (CAT-Seg) or ConvNeXt (SED) image features, shared by every arm;
  native           the released aggregator at V names (exp_headroom_probe.py; CAT-Seg decoder chunked, SED stages chunked);
  native_released  CAT-Seg (and DeCLIP, the same aggregator) only: the untouched released Aggregator.forward (decoder not chunked);
  anchored         bank pass (683-name bank) + all V candidates against its key/value sums;
  anchored_lean    the same with the lean bank pass (--lean in exp_headroom_probe.py; identical candidate scores).
Each arm includes the official stitching and the sampling of the cached pixels, as in the probe. "peak" is the maximum of
torch.cuda.max_memory_allocated() over the images (weights, text embeddings and image features included); "working" is
that peak minus the memory held when the arm starts. Vocabularies: the 845 evaluated names, then Open Images names in the
order of exp_lexicon_probe.py, cut at each size. CUDA out-of-memory is recorded as such. Development images (the first N
of the timing runs); nothing fitted, no scores stored.

Persistent state is also recorded: bytes of the bank's text embeddings (what anchoring keeps besides the weights) and the
bytes of the labelled ADE20K calibration images a recalibration needs (mean over the 2,000 evaluation images, times n_cal).

    PYTHONPATH=src .venv-probe/Scripts/python.exe src/exp_memory.py --model catseg --size large [--limit 3]
    PYTHONPATH=src .venv-probe/Scripts/python.exe src/exp_memory.py --model declip [--limit 3]
"""
import argparse
import gc
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from catseg_probe_model import CATSegProbe, bank_context
from encode import ADE
from exp_fixed_source import digest
from exp_headroom_probe import resize_short, stitched_samples
from natural_vocab import load_manifest

SIZES = [150, 845, 1690, 3380, 6760]
BANK = 'meta/bank_coco_oi683_v1.json'
N_CAL = 1000
GiB = 2**30


def calibration_bytes():
    """Bytes of the labelled images behind the 2,000-image evaluation (images + label maps), mean per image."""
    ids = sum([json.loads(Path(f'results/headroom_probe_ade_vitl_bank683{s}/protocol.json').read_text())['image_ids'] for s in ['', '_rest']], [])
    meta = json.loads(Path('cache/sclip/meta.json').read_text())['meta']
    sizes = [(Path(ADE)/'images/validation'/meta[i]['file']).stat().st_size+(Path(ADE)/'annotations/validation'/meta[i]['file'].replace('.jpg', '.png')).stat().st_size for i in ids]
    return len(ids), float(np.mean(sizes))


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed', 'declip'])
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--limit', type=int, default=20)
    ap.add_argument('--sizes', default=','.join(map(str, SIZES)))
    a = ap.parse_args()
    tag = a.model if a.model in ('sed', 'declip') else {'base': 'vitb', 'large': 'vitl'}[a.size]
    OUT = Path(f'results/memory_{tag}'); OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    sizes = [int(s) for s in a.sizes.split(',')]
    split = json.loads(Path('results/match_correction_sclip_ade/split.json').read_text())
    ids = [r['index'] for role in ['tune_cal', 'tune_eval'] for r in split['roles'][role]][:a.limit]
    names = [r['prompt'] for r in load_manifest()['rows']]
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    lexicon = names+[oi[i] for i in np.random.default_rng(1).permutation(len(oi))]
    assert max(sizes) <= len(lexicon)
    bank = json.loads(Path(BANK).read_text())['names']

    if a.model == 'sed':
        from sed_probe_model import SEDProbe, CKPT
        model = SEDProbe().cuda()
        context = lambda feats, lean: model.context(feats, ref_text, lean=lean)
        src = 'src/sed_probe_model.py'
    elif a.model == 'declip':
        from declip_probe_model import DeCLIPProbe, CKPT
        model = DeCLIPProbe().cuda()
        context = lambda feats, lean: bank_context(model, feats, ref_text, lean=lean)
        src = 'src/declip_probe_model.py'
    else:
        from catseg_probe_model import CKPT
        model = CATSegProbe(None, a.size).cuda()
        context = lambda feats, lean: bank_context(model, feats, ref_text, lean=lean)
        src = 'src/catseg_probe_model.py'
    torch.cuda.synchronize(); weights = torch.cuda.memory_allocated()
    text = model.encode_text(lexicon[:max(sizes)]).cpu()      # moved to the device per arm, so each arm holds the text of its own V names only
    ref_text = model.encode_text(bank)
    text_bytes_per_name = text[0].numel()*text.element_size()
    meta = json.loads(Path('cache/sclip/meta.json').read_text())

    t = lambda V: text[:V].cuda()
    arms = {'native': lambda feats, V: model.native(feats, t(V)),
            'anchored': lambda feats, V: model.anchored(feats, context(feats, False), t(V)),
            'anchored_lean': lambda feats, V: model.anchored(feats, context(feats, True), t(V))}
    if a.model != 'sed':
        arms['native_released'] = lambda feats, V: model.released_forward(feats, t(V))
    peak = {k: {V: 0. for V in sizes} for k in arms}; working = {k: {V: 0. for V in sizes} for k in arms}
    oom = {k: [] for k in arms}
    feat_peak = feat_working = 0.

    def measure(fn):
        gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats(); m0 = torch.cuda.memory_allocated()
        out = fn(); torch.cuda.synchronize()
        return out, torch.cuda.max_memory_allocated(), torch.cuda.max_memory_allocated()-m0

    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        feats, p, w = measure(lambda: model.image_features(model.windows(tensor)))
        feat_peak, feat_working = max(feat_peak, p), max(feat_working, w)
        for arm, fn in arms.items():
            for V in sizes:
                if V in oom[arm]: continue
                try:
                    out, p, w = measure(lambda: stitched_samples(model, fn(feats, V), y, x, H, W))
                    peak[arm][V], working[arm][V] = max(peak[arm][V], p), max(working[arm][V], w)
                    del out
                except torch.cuda.OutOfMemoryError:
                    oom[arm].append(V); print(f'{arm} V={V}: out of memory', flush=True)
        del feats
        print(f'{k+1}/{len(ids)} '+' '.join(f'{arm}@{sizes[-1]}={peak[arm][sizes[-1]]/GiB:.2f}' for arm in arms), flush=True)

    n_images, per_image = calibration_bytes()
    result = dict(model=a.model, size=a.size, tag=tag, gpu=torch.cuda.get_device_name(0), images=len(ids), vocab_sizes=sizes,
                  weights_gb=weights/GiB, features_peak_gb=feat_peak/GiB, features_working_gb=feat_working/GiB,
                  peak_gb={arm: {str(V): v/GiB for V, v in d.items()} for arm, d in peak.items()},
                  working_gb={arm: {str(V): v/GiB for V, v in d.items()} for arm, d in working.items()},
                  out_of_memory={arm: v for arm, v in oom.items()},
                  bank_size=len(bank), bank_text_bytes=len(bank)*text_bytes_per_name, text_bytes_per_name=text_bytes_per_name,
                  calibration=dict(n_cal=N_CAL, images_counted=n_images, mean_bytes_per_labelled_image=per_image, n_cal_bytes=N_CAL*per_image))
    protocol = dict(image_ids=ids, bank=BANK, lexicon='845 evaluated names, then Open Images names (distractors_openimages_v1, seed-1 permutation), as exp_lexicon_probe.py',
                    note=__doc__.split('\n\n')[0], hashes={p: digest(Path(p)) for p in ['src/exp_memory.py', src, 'meta/natural_vocab_v1.json', BANK, str(CKPT)]})
    (OUT/'protocol.json').write_text(json.dumps(protocol, indent=2))
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = [f'# Peak GPU memory per arm, {tag}', '', f"{len(ids)} development images, {result['gpu']}, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.", '',
             f"Weights {result['weights_gb']:.2f} GiB; image features peak {result['features_peak_gb']:.2f} GiB.", '',
             '| Arm | '+' | '.join(f'V={V:,}' for V in sizes)+' |', '|---|'+'---:|'*len(sizes)]
    for arm in arms:
        lines.append(f'| {arm} | '+' | '.join('OOM' if V in oom[arm] else f'{peak[arm][V]/GiB:.2f}' for V in sizes)+' |')
    lines += ['', f"Bank text embeddings: {result['bank_text_bytes']/2**20:.1f} MiB ({len(bank)} names). Labelled calibration images: "
              f"{per_image/2**10:.0f} KiB per image, {N_CAL*per_image/2**20:.0f} MiB for n_cal = {N_CAL}."]
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
