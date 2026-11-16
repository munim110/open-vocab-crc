"""CAT-Seg with the DeCLIP EVA02-CLIP-L backbone (DeCLIP, CVPR 2025) in the CATSegProbe interface.

DeCLIP's CAT-Seg branch (github.com/xiaomoguhz/DeCLIP, branch DeCLIP_CATSeg, commit bb2990c) changes only the backbone:
EVA02-CLIP-L-14-336 fine-tuned by DeCLIP, dense features from encode_dense(mode='csa'), guidance taps on visual.blocks[7, 15]
(configs/eva_vitl_336.yaml, eval.sh). Its cost aggregator (cat_seg/modeling/transformer/model.py) is byte-identical to
CAT-Seg's, so the native forward (class attention across the deployed vocabulary, per-crop top-256 truncation), the anchored
forward and bank_context are inherited unchanged. Released checkpoint CATSeg_DeCLIP_EVA-L_DINOv2-L_csa_0.05_2.0 (the authors'
retrain, which their README says replaces the lost original); it holds the whole fine-tuned EVA-CLIP, so no other weights are
read. xformers is not installed: the EVA blocks take the non-fused softmax-attention branch of the same file, which computes the
same attention. Nothing is fitted here.
"""
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from einops import rearrange

from catseg_probe_model import CATSegProbe, CATSEG, TEMPLATE, CLIP_MEAN, CLIP_STD, _import_catseg

DECLIP = CATSEG.parent/'DeCLIP_CATSeg'
CKPT = CATSEG.parent/'declip'/'catseg_declip_eva_l.pth'
CKPT_SHA256 = 'b57269da6d0590487986d1c2092737ba0604f234c5d4f80c7c7e32a5d15a59bc'   # = the Hugging Face LFS oid
CLIP_NAME = 'EVA02-CLIP-L-14-336'


def _import_eva():
    """DeCLIP ships its own open_clip (with eva_clip and encode_dense); it must shadow any installed open_clip."""
    sys.path.insert(0, str(DECLIP/'cat_seg'/'src'))
    import open_clip
    import open_clip.eva_clip as eva_clip
    assert Path(open_clip.__file__).resolve().is_relative_to(DECLIP.resolve()), open_clip.__file__
    return open_clip, eva_clip


class DeCLIPProbe(CATSegProbe):
    def __init__(self, aggregator=None, size='large'):
        torch.nn.Module.__init__(self)
        assert aggregator is None and size == 'large', 'released DeCLIP EVA-L only'
        Aggregator, _ = _import_catseg()
        open_clip, eva_clip = _import_eva()
        self.tokenizer = open_clip.get_tokenizer(CLIP_NAME)
        self.clip_model = eva_clip.create_model(model_name=CLIP_NAME, pretrained=None, force_custom_clip=True, device='cpu').float()
        for block in self.clip_model.visual.blocks:
            block.attn.xattn = False
        self.side = 336
        # eva_vitl_336.yaml with the eval.sh override POOLING_SIZES [1,1]
        self.transformer = Aggregator(
            text_guidance_dim=768, text_guidance_proj_dim=128, appearance_guidance_dim=768,
            appearance_guidance_proj_dim=128, decoder_dims=[64, 32], decoder_guidance_dims=[256, 128],
            decoder_guidance_proj_dims=[32, 16], num_layers=2, nheads=4, hidden_dim=128,
            pooling_size=[1, 1], feature_resolution=[24, 24], window_size=12,
            attention_type='linear', prompt_channel=1)
        self.upsample1 = torch.nn.ConvTranspose2d(1024, 256, kernel_size=2, stride=2)
        self.upsample2 = torch.nn.ConvTranspose2d(1024, 128, kernel_size=4, stride=4)
        state = torch.load(CKPT, map_location='cpu', weights_only=False)['model']
        missing, unexpected = self.load_state_dict({k.replace('sem_seg_head.predictor.', ''): v for k, v in state.items()}, strict=False)
        assert not unexpected, unexpected
        assert all('attn_mask' in k or 'rope' in k for k in missing), missing
        self.hooked = []
        for index in [7, 15]:
            self.clip_model.visual.blocks[index].register_forward_hook(lambda m, _, o: self.hooked.append(o))
        self.eval()

    @torch.no_grad()
    def encode_text(self, names):
        tokens = self.tokenizer([TEMPLATE.format(n) for n in names]).to(next(self.parameters()).device)
        out = torch.cat([self.clip_model.encode_text(tokens[i:i+128]) for i in range(0, len(tokens), 128)])
        return F.normalize(out.float(), dim=-1)                      # [T, 768]

    @torch.no_grad()
    def image_features(self, crops):
        self.hooked = []
        x = (crops-CLIP_MEAN.to(crops))/CLIP_STD.to(crops)
        x = F.interpolate(x, size=(self.side, self.side), mode='bilinear', align_corners=False)
        dense = self.clip_model.encode_dense(x, normalize=True, keep_shape=False, mode='csa')   # [B, 576, 768], no class token
        res3 = rearrange(dense, 'B (H W) C -> B C H W', H=24)
        res4 = self.upsample1(rearrange(self.hooked[0][:, 1:], 'B (H W) C -> B C H W', H=24))
        res5 = self.upsample2(rearrange(self.hooked[1][:, 1:], 'B (H W) C -> B C H W', H=24))
        return res3, [res3, res4, res5]
