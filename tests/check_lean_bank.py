"""Check of the lean bank pass: with `lean=True` the CAT-Seg and SED bank passes stop
once the key/value sums are recorded. The sums, and therefore the anchored candidate logits, must equal the full pass.
Also reports the time and peak memory of both passes as a preview of the timing rows. Run with .venv-probe from the repo
root, e.g.  PYTHONPATH=src python tests/check_lean_bank.py --size large --bank meta/bank_coco_oi683_v1.json
             PYTHONPATH=src python tests/check_lean_bank.py --model sed --bank meta/bank_coco_oi683_v1.json"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, 'src')
from catseg_probe_model import CATSegProbe, CATSEG, bank_context
from exp_headroom_probe import resize_short
from natural_vocab import load_manifest


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='catseg', choices=['catseg', 'sed'])
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--bank', default='', help='JSON with a "names" list; default COCO-171')
    ap.add_argument('--images', type=int, default=20)
    a = ap.parse_args()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    if a.model == 'sed':
        from sed_probe_model import SEDProbe
        model = SEDProbe().cuda()
        passes = {'full': lambda f, r: model.context(f, r), 'lean': lambda f, r: model.context(f, r, lean=True)}
    else:
        model = CATSegProbe(None, a.size).cuda()
        fn = bank_context if a.bank else (lambda m, f, r, lean=False: m.context(f, r, lean=lean))
        passes = {'full': lambda f, r: fn(model, f, r), 'lean': lambda f, r: fn(model, f, r, lean=True)}
    names = [r['prompt'] for r in load_manifest()['rows']]
    reference = json.loads(Path(a.bank).read_text())['names'] if a.bank else json.loads((CATSEG/'datasets/coco.json').read_text())
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    files = sorted(Path('data/ADEChallengeData2016/images/validation').glob('*.jpg'))[:a.images]
    sums_diff = logit_diff = 0.; exact = True
    seconds = {'full': 0., 'lean': 0.}; peak = {'full': 0., 'lean': 0.}
    for path in files:
        tensor = torch.from_numpy(np.array(resize_short(Image.open(path).convert('RGB')))).permute(2, 0, 1).float().cuda()
        feats = model.image_features(model.windows(tensor))
        ctx = {}
        for name, run in passes.items():
            torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); t0 = time.perf_counter()
            ctx[name] = run(feats, ref_text)
            torch.cuda.synchronize(); seconds[name] += time.perf_counter()-t0
            peak[name] = max(peak[name], torch.cuda.max_memory_allocated()/2**30)
        assert ctx['lean']['ref_logits'] is None and ctx['full']['ref_logits'] is not None
        assert len(ctx['lean']['sums']) == len(ctx['full']['sums'])
        for (kv0, ks0), (kv1, ks1) in zip(ctx['full']['sums'], ctx['lean']['sums']):
            exact &= torch.equal(kv0, kv1) and torch.equal(ks0, ks1)
            sums_diff = max(sums_diff, float((kv0-kv1).abs().max()), float((ks0-ks1).abs().max()))
        full, lean = model.anchored(feats, ctx['full'], text), model.anchored(feats, ctx['lean'], text)
        logit_diff = max(logit_diff, float((full-lean).abs().max()))
    n = len(files)
    report = dict(model=a.model, size=a.size, bank=a.bank or 'coco171', bank_size=len(reference), images=n, gpu=torch.cuda.get_device_name(0),
                  sums_bitwise_equal=bool(exact), sums_max_abs_diff=sums_diff, anchored_logits_max_abs_diff=logit_diff,
                  bank_pass_seconds_per_image={k: v/n for k, v in seconds.items()}, bank_pass_peak_memory_gb=peak)
    out = Path('results/lean_bank_check'); out.mkdir(parents=True, exist_ok=True)
    tag = f"{a.model}_{a.size}_{'bank'+str(len(reference)) if a.bank else 'coco171'}"
    (out/f'{tag}.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    assert logit_diff == 0., logit_diff
    print(f'Lean bank pass: sums and anchored logits identical on {n} images; bank pass {seconds["full"]/n:.2f} -> {seconds["lean"]/n:.2f} s/image.')


if __name__ == '__main__':
    main()
