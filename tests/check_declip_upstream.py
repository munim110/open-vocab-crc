"""Reference outputs of the upstream DeCLIP CAT-Seg release (its own detectron2 model, config and sliding-window inference) on
two ADE validation images with the ADE-150 test vocabulary, at fixed sampled pixels. check_declip_anchor.py compares
DeCLIPProbe against them. Needs detectron2, so run with .venv-fcclip from the repo root:

    TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 .venv-fcclip/bin/python tests/check_declip_upstream.py   -> results/declip_check/upstream.pt

(the upstream torch.load calls predate the torch 2.6 weights_only default; both checkpoints are sha256-verified downloads)
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TP = REPO.parent/'third_party_probe'
DECLIP = TP/'DeCLIP_CATSeg'
sys.path.insert(0, str(DECLIP/'cat_seg'/'src')); sys.path.insert(0, str(DECLIP))

import numpy as np
import torch
from PIL import Image
import open_clip
assert Path(open_clip.__file__).resolve().is_relative_to(DECLIP.resolve()), open_clip.__file__
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.modeling import build_model
from detectron2.projects.deeplab import add_deeplab_config


def resize_short(img, short=640, long_max=2560):                     # = exp_headroom_probe.resize_short (not importable in this venv)
    w, h = img.size
    scale = min(short/min(h, w), long_max/max(h, w))
    return img.resize((int(w*scale+.5), int(h*scale+.5)), Image.BILINEAR)


FILES = sorted((REPO/'data/ADEChallengeData2016/images/validation').glob('*.jpg'))[:2]
NPIX = 4096


@torch.no_grad()
def main():
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    os.chdir(DECLIP)                                                  # class-name JSONs are read by relative path
    from cat_seg import add_cat_seg_config
    cfg = get_cfg(); add_deeplab_config(cfg); add_cat_seg_config(cfg)
    cfg.merge_from_file('configs/eva_vitl_336.yaml')
    cfg.merge_from_list(['MODEL.SEM_SEG_HEAD.TEST_CLASS_JSON', 'datasets/ade150.json', 'TEST.SLIDING_WINDOW', 'True',
                         'MODEL.SEM_SEG_HEAD.POOLING_SIZES', '[1,1]', 'MODEL.SEM_SEG_HEAD.CACHE_DIR', str(TP/'declip'/'declip_eva_l.pt'),
                         'MODEL.WEIGHTS', str(TP/'declip'/'catseg_declip_eva_l.pth')])
    model = build_model(cfg)
    for block in model.sem_seg_head.predictor.clip_model.visual.blocks:   # xformers is not installed here either
        block.attn.xattn = False
    DetectionCheckpointer(model).load(cfg.MODEL.WEIGHTS)
    model.eval()
    out = {}
    for path in FILES:
        img = Image.open(path).convert('RGB'); W, H = img.size
        image = torch.from_numpy(np.array(resize_short(img))).permute(2, 0, 1).float()
        prob = model([dict(image=image, height=H, width=W)])[0]['sem_seg']          # [150, H, W] probabilities
        flat = np.random.default_rng(0).choice(H*W, NPIX, replace=False)
        out[path.name] = dict(flat=flat, H=H, W=W, prob=prob.flatten(1)[:, torch.from_numpy(flat).cuda()].T.cpu())
        print(path.name, tuple(prob.shape), flush=True)
    (REPO/'results/declip_check').mkdir(parents=True, exist_ok=True)
    torch.save(out, REPO/'results/declip_check/upstream.pt')


if __name__ == '__main__':
    main()
