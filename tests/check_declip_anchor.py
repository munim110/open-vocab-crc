"""Checks for DeCLIPProbe (CAT-Seg + DeCLIP EVA02-L). Run with .venv-probe from the repo root, after
tests/check_declip_upstream.py (.venv-fcclip) has written results/declip_check/upstream.pt:
(1) the probe's native forward reproduces the upstream release end to end (its detectron2 model, sliding window, ADE-150) when
the global view is taken as upstream takes it (the original image resized to 384); the shared CATSegProbe.windows resizes the
640 square instead, as in every CAT-Seg run of the paper, and that deviation is reported, not asserted;
(2) the re-implemented class attention reproduces the released Aggregator.forward, with and without top-256 truncation;
(3) anchored scores do not depend on co-candidates, order or chunking; (4) native scores do move with the vocabulary.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

sys.path.insert(0, 'src')
from declip_probe_model import DeCLIPProbe, DECLIP
from catseg_probe_model import CATSEG
from exp_headroom_probe import resize_short, stitched_samples
from natural_vocab import load_manifest


@torch.no_grad()
def main():
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    assert (DECLIP/'cat_seg/modeling/transformer/model.py').read_bytes() == (CATSEG/'cat_seg/modeling/transformer/model.py').read_bytes()
    model = DeCLIPProbe().cuda()
    names = [r['prompt'] for r in load_manifest()['rows']]
    reference = json.loads((CATSEG/'datasets/coco.json').read_text())
    ade150 = [n.split(', ')[0] for n in json.loads((DECLIP/'datasets/ade150.json').read_text())]   # upstream test-time text: first synonym
    text, ref_text, up_text = model.encode_text(names), model.encode_text(reference), model.encode_text(ade150)
    upstream = torch.load('results/declip_check/upstream.pt', weights_only=False)
    report = {}
    for fn, up in upstream.items():
        img = Image.open(Path('data/ADEChallengeData2016/images/validation')/fn).convert('RGB')
        tensor = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float().cuda()
        windows = model.windows(tensor)
        upstream_global = torch.cat([windows[:-1], F.interpolate(tensor[None], size=(384, 384), mode='bilinear', align_corners=False)])
        flat = up['flat']; W = up['W']
        y, x = torch.from_numpy(flat//W).cuda(), torch.from_numpy(flat % W).cuda()
        compare = lambda p: dict(max_abs_prob=float((p-up['prob']).abs().max()), mean_abs_prob=float((p-up['prob']).abs().mean()),
                                 argmax_agreement=float((p.argmax(1) == up['prob'].argmax(1)).float().mean()))
        release = compare(stitched_samples(model, model.native(model.image_features(upstream_global), up_text), y, x, up['H'], W).float().cpu())
        feats = model.image_features(windows)
        shared = compare(stitched_samples(model, model.native(feats, up_text), y, x, up['H'], W).float().cpu())
        ctx = model.context(feats, ref_text)
        released = model.released_forward(feats, ref_text)
        reimplementation = max(float((released-ctx['ref_logits']).abs().max()), float((released-model.native(feats, ref_text)).abs().max()))
        truncated = float((model.released_forward(feats, text[:300])-model.native(feats, text[:300])).abs().max())
        full = model.anchored(feats, ctx, text)
        alone = model.anchored(feats, ctx, text[:7], chunk=1)
        perm = torch.randperm(845, generator=torch.Generator().manual_seed(0)).cuda()
        shuffled = model.anchored(feats, ctx, text[perm], chunk=64)
        drift_alone, drift_perm = float((full[:, :7]-alone).abs().max()), float((full[:, perm]-shuffled).abs().max())
        native_shift = float((model.native(feats, text[:150])-model.native(feats, text[:200])[:, :150]).abs().max())
        report[fn] = dict(upstream=release, shared_pipeline_vs_upstream=shared, reimplementation_max_abs=reimplementation, truncated_max_abs=truncated,
                          anchored_alone_vs_batch=drift_alone, anchored_permutation=drift_perm, native_vocabulary_shift=native_shift)
        print(fn, json.dumps(report[fn]), flush=True)
        assert release['max_abs_prob'] < 1e-3, release
        assert reimplementation < 1e-3 and truncated < 1e-3, (reimplementation, truncated)
        assert drift_alone < 1e-3 and drift_perm < 1e-3, (drift_alone, drift_perm)
        assert native_shift > 1e-2, native_shift
    Path('results/declip_check/anchor_check.json').write_text(json.dumps(report, indent=2))
    print('DeCLIPProbe matches the upstream release; anchored scores independent of co-candidates up to float drift.')


if __name__ == '__main__':
    main()
