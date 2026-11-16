"""SED probe exactness: (1) the chunked native forward reproduces the released Aggregator.forward; (2) a candidate's
anchored score equals its native score in the vocabulary bank+{candidate}; (3) anchored scores do not depend on which
other candidates are scored. Runs on CPU by default (python tests/check_sed_anchor.py [--cuda])."""
import json
import sys
from pathlib import Path

import torch
from PIL import Image
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from sed_probe_model import SEDProbe
from encode import ADE

device = 'cuda' if '--cuda' in sys.argv else 'cpu'
torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False   # as in exp_headroom_probe
torch.manual_seed(0)
model = SEDProbe().to(device)
names = ['wall', 'floor', 'ceiling', 'bed', 'window', 'cabinet', 'person', 'door', 'table', 'plant', 'curtain', 'chair', 'car', 'painting', 'sofa', 'shelf']
text = model.encode_text(names)
files = sorted(Path(ADE, 'images/validation').glob('*.jpg'))[:1] if Path(ADE).exists() else []
if files:
    img = torch.from_numpy(np.array(Image.open(files[0]).convert('RGB'))).permute(2, 0, 1).float().to(device)
else:
    img = torch.rand(3, 480, 640, device=device)*255
with torch.no_grad():
    feats = model.image_features(model.windows(img))
    ref = model.transformer(feats[0], text[None], feats[1], model.clip_model.logit_scale)[0]      # released, all labels at once
    mine = model.native(feats, text)
    print('released vs chunked native: max |diff| = %.2e' % (ref-mine).abs().max().item())
    assert torch.allclose(ref, mine, atol=1e-3), 'native mismatch'
    bank, cand = text[:12], text[12:]
    ctx = model.context(feats, bank)
    anch = model.anchored(feats, ctx, cand, chunk=2)
    # Diagnostic, not exact: natively the bank tokens also attend to the candidate at every stage (as for CAT-Seg).
    for j in range(cand.shape[0]):
        one = model.native(feats, torch.cat([bank, cand[j:j+1]]))[:, -1]
        d = (one-anch[:, j]).abs()
        same = (one.sigmoid().round() == anch[:, j].sigmoid().round()).float().mean().item()
        print(f'candidate {names[12+j]}: native bank+one vs anchored |diff| mean {d.mean().item():.3f} max {d.max().item():.3f}; same .5-decision {same:.4f}')
    alone = torch.cat([model.anchored(feats, ctx, cand[j:j+1]) for j in range(cand.shape[0])], 1)
    print('anchored alone vs together: max |diff| = %.2e' % (alone-anch).abs().max().item())
    assert torch.allclose(alone, anch, atol=1e-4)
    fast = model.native_fast(feats, text, topk=4)
    kept = (fast[0] > -100).flatten(1).any(1)
    print(f'fast mode kept {int(kept.sum())}/{len(names)} labels; kept labels vs non-fast max |diff| = %.2e' % (fast[:, kept]-mine[:, kept]).abs().max().item())
    if files:   # the paper cites these numbers (paper_numbers.py), so only a real ADE image counts
        out = Path(__file__).resolve().parents[1]/'results/headroom_probe_ade/sed_anchor_check.json'
        out.write_text(json.dumps({files[0].name: dict(reimplementation_max_abs=(ref-mine).abs().max().item(),
                                                       anchored_alone_vs_batch=(alone-anch).abs().max().item(),
                                                       logit_scale=anch.abs().mean().item(), device=device)}, indent=2))
print('ok')
