#!/usr/bin/env bash
# .venv-fcclip without a CUDA toolkit (no nvcc): FC-CLIP's deformable attention runs on its PyTorch reference path
# (ms_deform_attn_core_pytorch, shipped in the FC-CLIP checkout) and detectron2 is imported from its checkout without
# building its C++ extension. Used for the local FC-CLIP runs of 2026-10-30 (Windows 11, Python 3.10, RTX 5070 Ti, Git Bash);
# on three ADE images every per-image ranking metric and the confusion matrix equal the GH200 run with the compiled kernel
# (results/lexicon_probe_fcclip_bank683/store_regeneration.json has the full comparison). scripts/setup_models.sh is the
# compiled route. Run from the repository root after scripts/setup_models.sh SKIP_VENV=1 (checkouts + checkpoints), or let
# this script clone the two checkouts at the pinned commits. Re-runnable.
#
#   PYTHON=/path/to/python3.10 scripts/setup_fcclip_nokernel.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TP="$(dirname "$ROOT")/third_party_probe"
PYTHON="${PYTHON:-python3}"
mkdir -p "$TP"; cd "$ROOT"

checkout() {  # dir url commit
  [ -d "$TP/$1/.git" ] || git clone -q "$2" "$TP/$1"
  git -C "$TP/$1" fetch -q origin "$3" 2>/dev/null || true
  git -C "$TP/$1" -c advice.detachedHead=false checkout -q "$3"
  echo "checkout $1 @ $(git -C "$TP/$1" rev-parse --short HEAD)"
}
checkout detectron2 https://github.com/facebookresearch/detectron2.git a2f4a8771ab77e8411c26b27f24f9489a28a2453
checkout fc-clip https://github.com/bytedance/fc-clip.git 2b0bbe213070d44da9182530fa2e826fef03f974
[ -f "$TP/fcclip_cocopan_convnext_large.pth" ] || { echo "missing $TP/fcclip_cocopan_convnext_large.pth (scripts/setup_models.sh fetches it)"; exit 1; }

# the two checkout edits (idempotent; CRLF-safe for checkouts cloned with core.autocrlf=true)
"$PYTHON" - "$TP" <<'EOF'
import sys
from pathlib import Path
tp = Path(sys.argv[1])

def patch(path, pairs):
    s = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    for old, new in pairs:
        old, new = old.replace('\n', nl), new.replace('\n', nl)
        if new in s: continue
        assert s.count(old) == 1, (path, old[:40])
        s = s.replace(old, new, 1)
    open(path, 'w', encoding='utf-8', newline='').write(s)

ops = tp/'fc-clip/fcclip/modeling/pixel_decoder/ops'
# 1. FC-CLIP: no import-time failure without the compiled kernel; MSDeformAttn.forward takes the reference path instead
patch(ops/'functions/ms_deform_attn_func.py', [(
    'except ModuleNotFoundError as e:\n    info_string = (\n'
    '        "\\n\\nPlease compile MultiScaleDeformableAttention CUDA op with the following commands:\\n"\n'
    '        "\\t`cd fcclip/modeling/pixel_decoder/ops`\\n"\n        "\\t`sh make.sh`\\n"\n    )\n    raise ModuleNotFoundError(info_string)\n',
    'except ModuleNotFoundError as e:\n    MSDA = None   # local patch: no CUDA toolkit here; MSDeformAttn.forward uses ms_deform_attn_core_pytorch instead\n'
    'MSDA_AVAILABLE = MSDA is not None\n')])
patch(ops/'modules/ms_deform_attn.py', [
    ('from ..functions.ms_deform_attn_func import ms_deform_attn_core_pytorch\n',
     'from ..functions.ms_deform_attn_func import ms_deform_attn_core_pytorch, MSDA_AVAILABLE\n'),
    ('        try:\n            output = MSDeformAttnFunction.apply(\n'
     '                value, input_spatial_shapes, input_level_start_index, sampling_locations, attention_weights, self.im2col_step)\n'
     '        except:\n            # CPU\n            output = ms_deform_attn_core_pytorch(value, input_spatial_shapes, sampling_locations, attention_weights)\n',
     '        if MSDA_AVAILABLE:\n            output = MSDeformAttnFunction.apply(\n'
     '                value, input_spatial_shapes, input_level_start_index, sampling_locations, attention_weights, self.im2col_step)\n'
     '        else:   # local patch: reference implementation (bilinear grid_sample), same math as the CUDA kernel\n'
     '            output = ms_deform_attn_core_pytorch(value, input_spatial_shapes, sampling_locations, attention_weights)\n')])
# 2. detectron2: the one module-level import of its extension (COCO fast evaluation, unused here)
patch(tp/'detectron2/detectron2/evaluation/fast_eval_api.py', [(
    'from detectron2 import _C\n',
    'try:\n    from detectron2 import _C\nexcept ImportError:   # local patch: extension not built; COCOeval_opt is not used here\n    _C = None\n')])
print('checkout patches ok')
EOF

# .venv-fcclip (Windows: Scripts/, elsewhere bin/)
[ -d .venv-fcclip ] || "$PYTHON" -m venv .venv-fcclip
VP=.venv-fcclip/bin/python; [ -x "$VP" ] || VP=.venv-fcclip/Scripts/python.exe
$VP -m pip -q install --upgrade pip wheel setuptools ninja
$VP -m pip -q install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
$VP -m pip -q install -r env/requirements-fcclip-local.txt
# detectron2 from its checkout, no build: a .pth file on sys.path
SITE="$($VP -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
$VP -c "import pathlib,sys; print(str(pathlib.Path(sys.argv[1]).resolve()))" "$TP/detectron2" > "$SITE/detectron2_checkout.pth"
( cd "$TP/fc-clip" && "$ROOT/$VP" -W ignore -c "import detectron2, fcclip; from fcclip.modeling.pixel_decoder.ops.functions.ms_deform_attn_func import MSDA_AVAILABLE; print('.venv-fcclip ok; compiled MSDeformAttn kernel:', MSDA_AVAILABLE)" )
