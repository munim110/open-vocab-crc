"""Checks for the reference-anchored CAT-Seg forward. Run with .venv-probe from the repo root."""
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, 'src')
from catseg_probe_model import CATSegProbe, CATSEG
from exp_headroom_probe import resize_short
from natural_vocab import load_manifest


@torch.no_grad()
def main():
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = CATSegProbe().cuda()
    names = [r['prompt'] for r in load_manifest()['rows']]
    reference = json.loads((CATSEG/'datasets/coco.json').read_text())
    text, ref_text = model.encode_text(names), model.encode_text(reference)
    files = sorted(Path('data/ADEChallengeData2016/images/validation').glob('*.jpg'))[:2]
    report = {}
    for path in files:
        tensor = torch.from_numpy(np.array(resize_short(Image.open(path).convert('RGB')))).permute(2, 0, 1).float().cuda()
        feats = model.image_features(model.windows(tensor))
        ctx = model.context(feats, ref_text)
        # 1. The re-implemented class attention reproduces the released forward on the reference vocabulary.
        released = model.released_forward(feats, ref_text)
        reimplementation = max(float((released-ctx['ref_logits']).abs().max()), float((released-model.native(feats, ref_text)).abs().max()))
        truncated = float((model.released_forward(feats, text[:300])-model.native(feats, text[:300])).abs().max())
        assert truncated < 1e-3, truncated
        # 2. Candidate scores do not depend on co-candidates, order, or chunking.
        full = model.anchored(feats, ctx, text)
        alone = model.anchored(feats, ctx, text[:7], chunk=1)
        perm = torch.randperm(845, generator=torch.Generator().manual_seed(0)).cuda()
        shuffled = model.anchored(feats, ctx, text[perm], chunk=64)
        drift_alone = float((full[:, :7]-alone).abs().max())
        drift_perm = float((full[:, perm]-shuffled).abs().max())
        # 3. The native model does move when the vocabulary changes (the intervention is real).
        native_shift = float((model.native(feats, text[:150])-model.native(feats, text[:200])[:, :150]).abs().max())
        report[path.name] = dict(reimplementation_max_abs=reimplementation, anchored_alone_vs_batch=drift_alone,
                                 anchored_permutation=drift_perm, native_vocabulary_shift=native_shift,
                                 logit_scale=float(full.abs().mean()))
        assert reimplementation < 1e-3, reimplementation
        assert drift_alone < 1e-3 and drift_perm < 1e-3, (drift_alone, drift_perm)
        assert native_shift > 1e-2, native_shift
    Path('results/headroom_probe_ade').mkdir(parents=True, exist_ok=True)
    Path('results/headroom_probe_ade/anchor_check.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print('Anchored forward: reimplementation matches release; candidate scores independent of co-candidates up to reported float drift.')


if __name__ == '__main__':
    main()
