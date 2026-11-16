#!/usr/bin/env bash
# Model checkouts, released checkpoints and the two model environments for the GPU level
# (README.md). Run from the repository root on a Linux CUDA 12.x machine. Re-runnable: finished steps are skipped.
# Every checkout is pinned to the commit that produced the stored scores and every checkpoint is checked against its sha256.
#
#   scripts/setup_models.sh            # checkouts + checkpoints + .venv-probe + .venv-ovd + .venv-fcclip
#   SKIP_VENV=1 scripts/setup_models.sh    # checkouts + checkpoints only (e.g. to verify files already on disk)
#   SKIP_FCCLIP=1 scripts/setup_models.sh  # no FC-CLIP (it needs nvcc to build detectron2 and its kernel)
#   SKIP_OVD=1 scripts/setup_models.sh     # no detectors
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TP="$(dirname "$ROOT")/third_party_probe"          # where src/catseg_probe_model.py, sed_probe_model.py and the FC-CLIP scripts look
mkdir -p "$TP"; cd "$ROOT"

checkout() {  # dir url commit
  [ -d "$TP/$1/.git" ] || git clone -q "$2" "$TP/$1"
  git -C "$TP/$1" fetch -q origin "$3" 2>/dev/null || true
  git -C "$TP/$1" -c advice.detachedHead=false checkout -q "$3"
  echo "checkout $1 @ $(git -C "$TP/$1" rev-parse --short HEAD)"
}
fetch() {  # file sha256 command...
  local name="$1" f="$TP/$1" sum="$2"; shift 2
  [ -f "$f" ] || "$@"
  local got; got="$(sha256sum "$f" | cut -d' ' -f1)"
  [ "$got" = "$sum" ] || { echo "sha256 mismatch for $f: $got (expected $sum)"; exit 1; }
  echo "checkpoint $name sha256 ok"
}

# 1. checkouts (commits used for every stored score in results/)
checkout CAT-Seg https://github.com/KU-CVLAB/CAT-Seg 6d3a188af95165147fe2f34a8237fa7d2633e784
checkout SED https://github.com/xb534/SED.git db20d93c0ec8b0ce7fae267a10f826dfc7da15f5
[ -n "${SKIP_FCCLIP:-}" ] || {
  checkout detectron2 https://github.com/facebookresearch/detectron2.git a2f4a8771ab77e8411c26b27f24f9489a28a2453
  checkout fc-clip https://github.com/bytedance/fc-clip.git 2b0bbe213070d44da9182530fa2e826fef03f974
  # the only change to any checkout: Tensor.type() was removed from AT_DISPATCH in torch 2.x
  sed -i 's/AT_DISPATCH_FLOATING_TYPES(value\.type()/AT_DISPATCH_FLOATING_TYPES(value.scalar_type()/g' \
    "$TP/fc-clip/fcclip/modeling/pixel_decoder/ops/src/cuda/ms_deform_attn_cuda.cu"
}

# 2. released checkpoints
HF=https://huggingface.co/spaces/hamacojr/CAT-Seg-weights/resolve/main
fetch model_base.pth a201a50f94f4c04196e3083773832b736c2b8b81d27ea2c59cc13af3aff05760 wget -q -O "$TP/model_base.pth" $HF/model_base.pth
fetch model_large.pth 80722f4b328161aa15d25d278e832a824b72af4486b013f664757ae7cc020f61 wget -q -O "$TP/model_large.pth" $HF/model_large.pth
if [ -z "${SKIP_VENV:-}" ] && [ ! -d .venv-probe ]; then python3 -m venv .venv-probe; .venv-probe/bin/pip -q install gdown==6.4.0; fi
GDOWN="${GDOWN:-.venv-probe/bin/gdown}"
fetch sed_model_large.pth 25c2a29837d141459a324883280a9bd0f7e3804cda9c8c1c398f9a25bb32ee0f $GDOWN 1zAXE0QXy47n0cVn7j_2cSR85eqxdDGg8 -O "$TP/sed_model_large.pth"
[ -n "${SKIP_FCCLIP:-}" ] || \
  fetch fcclip_cocopan_convnext_large.pth 241c141e0fec7f3be7e06915daee60807502de3b7ae8b8cbef2560d6df346257 $GDOWN 1-91PIns86vyNaL3CzMmDD39zKGnPMtvj -O "$TP/fcclip_cocopan_convnext_large.pth"
[ -n "${SKIP_VENV:-}" ] && exit 0

# 3. .venv-probe: CAT-Seg, SED, fine-tuning (no detectron2: the probe imports the aggregators through stub packages)
TORCH="torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128"
.venv-probe/bin/pip -q install $TORCH
.venv-probe/bin/pip -q install -r env/requirements-probe.txt
.venv-probe/bin/python -c "import torch; assert torch.cuda.is_available(), 'CPU-only torch'; print('.venv-probe ok', torch.__version__)"

# 3b. .venv-ovd: the four detectors of the detection benchmark (docs/OVD_DETECTION_BENCHMARK.md), Hugging Face transformers
#     only. The checkpoints are fetched at the commits that wrote the stored scores (listed in env/requirements-ovd.txt).
if [ -z "${SKIP_OVD:-}" ]; then
  [ -d .venv-ovd ] || python3 -m venv .venv-ovd
  .venv-ovd/bin/pip -q install $TORCH
  .venv-ovd/bin/pip -q install -r env/requirements-ovd.txt
  grep -E '^#   [a-z]' env/requirements-ovd.txt | while read -r _ repo rev; do
    .venv-ovd/bin/python -c "import sys; from huggingface_hub import snapshot_download as s; s(sys.argv[1], revision=sys.argv[2])" "$repo" "$rev"
    echo "checkpoint $repo @ ${rev:0:7}"
  done
  .venv-ovd/bin/python -c "import torch, transformers; assert torch.cuda.is_available(), 'CPU-only torch'; print('.venv-ovd ok', transformers.__version__)"
fi

# 4. .venv-fcclip: detectron2 and the deformable-attention kernel are compiled here (needs nvcc; set TORCH_CUDA_ARCH_LIST for your GPU)
[ -n "${SKIP_FCCLIP:-}" ] && exit 0
[ -d .venv-fcclip ] || python3 -m venv .venv-fcclip
.venv-fcclip/bin/pip -q install --upgrade pip wheel setuptools ninja
.venv-fcclip/bin/pip -q install $TORCH
.venv-fcclip/bin/pip -q install -r env/requirements-fcclip.txt
.venv-fcclip/bin/python -c "import detectron2" 2>/dev/null || .venv-fcclip/bin/pip -q install --no-build-isolation -e "$TP/detectron2"
.venv-fcclip/bin/python -c "import panopticapi" 2>/dev/null || \
  .venv-fcclip/bin/pip -q install --no-build-isolation git+https://github.com/cocodataset/panopticapi.git@7bb4655548f98f3fedc07bf37e9040a992b054b0
.venv-fcclip/bin/python -c "import MultiScaleDeformableAttention" 2>/dev/null || \
  ( cd "$TP/fc-clip/fcclip/modeling/pixel_decoder/ops" && rm -rf build && "$ROOT/.venv-fcclip/bin/python" setup.py build install )
( cd "$TP/fc-clip" && "$ROOT/.venv-fcclip/bin/python" -c "import detectron2; from fcclip.modeling.pixel_decoder.ops.modules import MSDeformAttn; print('.venv-fcclip ok')" )
