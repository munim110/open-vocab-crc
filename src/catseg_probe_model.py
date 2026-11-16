"""Standalone CAT-Seg (ViT-B) inference without detectron2, plus a reference-anchored forward.

Native CAT-Seg is candidate-dependent in two places: class-aggregation attention runs
across the deployed vocabulary, and vocabularies above pad_len=256 are truncated per crop
by initial CLIP similarity. The anchored forward removes both: a fixed reference bank R is
aggregated exactly as native CAT-Seg would aggregate the vocabulary R, and every candidate
attends to R's keys/values (plus the learned padding tokens and itself) only. A candidate's
score is then a function of (image, candidate text, R) and never of the other candidates.
Uses the released weights unchanged; nothing is fitted here.
"""
import sys
import types
from pathlib import Path

import torch
import torch.nn.functional as F
from einops import rearrange, repeat

CATSEG = Path(__file__).resolve().parents[2]/'third_party_probe'/'CAT-Seg'
CKPT = CATSEG.parent/'model_base.pth'
TEMPLATE = 'A photo of a {} in the scene'
CLIP_MEAN = torch.tensor([122.7709383, 116.7460125, 104.09373615]).view(1, 3, 1, 1)
CLIP_STD = torch.tensor([68.5005327, 66.6321579, 70.3231630]).view(1, 3, 1, 1)


def _import_catseg():
    """Import submodules without executing cat_seg/__init__.py (which needs detectron2)."""
    for name, sub in [('cat_seg', ''), ('cat_seg.modeling', 'modeling'),
                      ('cat_seg.modeling.transformer', 'modeling/transformer'),
                      ('cat_seg.third_party', 'third_party')]:
        if name not in sys.modules:
            module = types.ModuleType(name)
            module.__path__ = [str(CATSEG/'cat_seg'/sub)]
            sys.modules[name] = module
    from cat_seg.modeling.transformer.model import Aggregator
    from cat_seg.third_party import clip
    return Aggregator, clip


class CATSegProbe(torch.nn.Module):
    def __init__(self, aggregator=None, size='base'):
        super().__init__()
        Aggregator, clip = _import_catseg()
        self.clip = clip
        # vitb_384.yaml / vitl_336.yaml: CLIP model, its width, input side, tapped blocks, text and appearance guidance widths
        name, width, self.side, taps, dim = dict(base=('ViT-B/16', 768, 384, [3, 7], 512), large=('ViT-L/14@336px', 1024, 336, [7, 15], 768))[size]
        self.clip_model, _ = clip.load(name, device='cpu', jit=False, prompt_depth=0, prompt_length=0)
        self.clip_model = self.clip_model.float()
        # with the official eval override POOLING_SIZES [1,1]
        self.transformer = Aggregator(
            text_guidance_dim=dim, text_guidance_proj_dim=128, appearance_guidance_dim=dim,
            appearance_guidance_proj_dim=128, decoder_dims=[64, 32], decoder_guidance_dims=[256, 128],
            decoder_guidance_proj_dims=[32, 16], num_layers=2, nheads=4, hidden_dim=128,
            pooling_size=[1, 1], feature_resolution=[24, 24], window_size=12,
            attention_type='linear', prompt_channel=1)
        self.upsample1 = torch.nn.ConvTranspose2d(width, 256, kernel_size=2, stride=2)
        self.upsample2 = torch.nn.ConvTranspose2d(width, 128, kernel_size=4, stride=4)
        state = torch.load(CKPT if size == 'base' else CKPT.with_name('model_large.pth'), map_location='cpu', weights_only=False)['model']
        mapped = {}
        for key, value in state.items():
            key = key.replace('sem_seg_head.predictor.', '')
            mapped[key] = value
        missing, unexpected = self.load_state_dict(mapped, strict=False)
        assert not unexpected, unexpected
        assert all('attn_mask' in k or 'relative_position_index' in k for k in missing), missing
        if aggregator:                                               # fine-tuned cost aggregator from train_anchored_catseg.py
            self.transformer.load_state_dict(torch.load(aggregator, map_location='cpu')['aggregator'])
        self.hooked = []
        for index in taps:
            self.clip_model.visual.transformer.resblocks[index].register_forward_hook(
                lambda m, _, o: self.hooked.append(o))
        self.eval()

    @torch.no_grad()
    def encode_text(self, names):
        tokens = self.clip.tokenize([TEMPLATE.format(n) for n in names]).to(next(self.parameters()).device)
        out = torch.cat([self.clip_model.encode_text(tokens[i:i+128]) for i in range(0, len(tokens), 128)])
        return F.normalize(out.float(), dim=-1)                      # [T, 512]

    @torch.no_grad()
    def windows(self, image, kernel=384, overlap=.333, out_res=640):
        """image: float RGB 0..255 [3,h,w]. Official sliding-window crops plus the global view."""
        stride = int(kernel*(1-overlap))
        image = F.interpolate(image[None], size=(out_res, out_res), mode='bilinear', align_corners=False)
        crops = rearrange(F.unfold(image, kernel, stride=stride)[0], '(C H W) L -> L C H W', C=3, H=kernel)
        return torch.cat([crops, F.interpolate(image, size=(kernel, kernel), mode='bilinear', align_corners=False)])

    @torch.no_grad()
    def image_features(self, crops):
        self.hooked = []
        x = (crops-CLIP_MEAN.to(crops))/CLIP_STD.to(crops)
        x = F.interpolate(x, size=(self.side, self.side), mode='bilinear', align_corners=False)
        dense = self.clip_model.encode_image(x, dense=True)
        res3 = rearrange(dense[:, 1:], 'B (H W) C -> B C H W', H=24)
        res4 = self.upsample1(rearrange(self.hooked[0][1:], '(H W) B C -> B C H W', H=24))
        res5 = self.upsample2(rearrange(self.hooked[1][1:], '(H W) B C -> B C H W', H=24))
        return res3, [res3, res4, res5]

    @staticmethod
    def stitch(logits, kernel=384, overlap=.333, out_res=640):
        """Official merge: fold window probabilities, average with the upsampled global view."""
        stride = int(kernel*(1-overlap))
        prob = F.interpolate(logits, size=kernel, mode='bilinear', align_corners=False).sigmoid()
        glob = F.interpolate(prob[-1:], size=(out_res, out_res), mode='bilinear', align_corners=False)
        ones = torch.ones(1, 1, out_res, out_res, device=logits.device)
        count = F.fold(F.unfold(ones, kernel, stride=stride), (out_res, out_res), kernel, stride=stride)
        local = F.fold(prob[:-1].flatten(1).T[None], (out_res, out_res), kernel, stride=stride)/count
        return (local[0]+glob[0])/2                                # [T, out_res, out_res]

    def decode(self, x, g_dec, chunk=64):
        """conv_decoder is per-class; chunking over classes is exact and bounds memory."""
        return torch.cat([self.transformer.conv_decoder(x[:, :, i:i+chunk], g_dec) for i in range(0, x.shape[2], chunk)], 1)

    @torch.no_grad()
    def native(self, feats, text):
        """Released Aggregator.forward under the deployed vocabulary `text` [T,512], decoder chunked."""
        agg = self.transformer
        img, guidance = feats
        t = text[None, :, None].expand(img.shape[0], -1, -1, -1)
        corr = agg.correlation(img, t)
        classes = None
        if t.size(1) > agg.pad_len:                                  # native per-crop top-256 truncation
            top = corr.permute(0, 2, 1, 3, 4).flatten(-3).max(dim=-1)[0]
            classes = top.topk(agg.pad_len, dim=-1, sorted=False)[1]
            t = torch.gather(t, 1, classes[..., None, None].expand(-1, -1, 1, t.size(-1)))
            corr = agg.correlation(img, t)
        x = agg.corr_embed(corr)
        g_app = agg.guidance_projection(guidance[0])
        g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
        g_text = agg.text_guidance_projection(t.mean(-2))
        for layer in agg.layers:
            x = layer(x, g_app, g_text)
        logit = self.decode(x, g_dec)
        if classes is not None:
            out = torch.full((logit.size(0), text.size(0), logit.size(2), logit.size(3)), -100., device=logit.device)
            logit = out.scatter_(1, classes[..., None, None].expand(-1, -1, logit.size(-2), logit.size(-1)), logit)
        return logit

    @torch.no_grad()
    def released_forward(self, feats, text):
        """The untouched released forward, for equivalence checks only (memory hungry)."""
        return self.transformer(feats[0], text[None, :, None].expand(feats[0].shape[0], -1, -1, -1), feats[1])

    @torch.no_grad()
    def context(self, feats, ref_text, lean=False):
        """Run the reference bank natively, recording per-layer class-attention key/value sums.
        lean=True stops once the last layer's sums are recorded: no attention output for that layer and no bank logits
        (ref_logits=None). Candidates read only the sums, so their scores are unchanged; train_anchored_catseg.py needs
        ref_logits and keeps the default."""
        agg = self.transformer
        img, guidance = feats
        g_app = agg.guidance_projection(guidance[0])
        g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
        g_ref = agg.text_guidance_projection(ref_text)[None].expand(img.shape[0], -1, -1)
        x = agg.corr_embed(agg.correlation(img, ref_text[None, :, None].expand(img.shape[0], -1, -1, -1)))
        sums = []
        for layer in agg.layers:
            x = layer.swin_block(x, g_app)
            x, kv = class_attention(layer.attention, x, g_ref, None, sums_only=lean and layer is agg.layers[-1])
            sums.append(kv)
        return dict(g_app=g_app, g_dec=g_dec, sums=sums, ref_logits=None if lean else self.decode(x, g_dec))

    @torch.no_grad()
    def anchored(self, feats, ctx, cand_text, chunk=96):
        """Score candidates independently of each other against the frozen reference context."""
        agg = self.transformer
        img = feats[0]
        out = []
        for i in range(0, len(cand_text), chunk):
            text = cand_text[i:i+chunk]
            g = agg.text_guidance_projection(text)[None].expand(img.shape[0], -1, -1)
            x = agg.corr_embed(agg.correlation(img, text[None, :, None].expand(img.shape[0], -1, -1, -1)))
            for layer, kv in zip(agg.layers, ctx['sums']):
                x = layer.swin_block(x, ctx['g_app'])
                x, _ = class_attention(layer.attention, x, g, kv)
            out.append(self.decode(x, ctx['g_dec']))
        return torch.cat(out, 1)


def class_attention(layer, x, guidance, context, sums_only=False):
    """ClassTransformerLayer at pooling 1x1.

    context=None: native attention over the given tokens plus learned padding up to pad_len;
    returns the key/value sums so later candidates can reuse them.
    context=(KV, Ksum): each token attends to the recorded context plus itself only.
    sums_only (context=None): return (None, sums) once the key/value sums are recorded; the attention output is skipped.
    """
    B, C, T, H, W = x.shape
    att = layer.attention
    tok = rearrange(x, 'B C T H W -> (B H W) T C')
    gui = repeat(guidance, 'B T C -> (B H W) T C', H=H, W=W)

    qkv = lambda tokens, guide, which='qkv': _projections(layer, tokens, guide, which)
    q, k, v = qkv(tok, gui, 'kv' if (sums_only and context is None) else 'qkv')
    if context is None:
        pad = layer.pad_len-T
        if pad > 0:
            _, kp, vp = qkv(layer.padding_tokens.expand(tok.shape[0], pad, -1),
                            layer.padding_guidance.expand(tok.shape[0], pad, -1), 'kv')
            k_all, v_all = torch.cat([k, kp], 1), torch.cat([v, vp], 1)
        else:                                                        # a bank of pad_len labels or more: no padding (outside the released regime)
            k_all, v_all = k, v
        KV = torch.einsum('nshd,nshv->nhdv', k_all, v_all)
        Ks = k_all.sum(1)
        if sums_only:
            return None, (KV, Ks)
        num = torch.einsum('nlhd,nhdv->nlhv', q, KV)
        den = torch.einsum('nlhd,nhd->nlh', q, Ks)
    else:
        KV, Ks = context
        self_weight = (q*k).sum(-1)                                  # [N,T,heads]
        num = torch.einsum('nlhd,nhdv->nlhv', q, KV)+self_weight[..., None]*v
        den = torch.einsum('nlhd,nhd->nlh', q, Ks)+self_weight
    attended = rearrange(num/(den[..., None]+att.attention.eps), 'N T H D -> N T (H D)')
    pooled = tok+attended
    pooled = pooled+layer.MLP(layer.norm2(pooled))
    pooled = rearrange(pooled, '(B H W) T C -> B C T H W', B=B, H=H, W=W)
    return x+pooled, (KV, Ks)


def _projections(layer, tokens, guide, which='qkv'):
    """Query, key and value of a ClassTransformerLayer's linear attention, each computed only if named in `which` (they are
    separate linear maps, so leaving one out changes nothing else); the others are None."""
    att = layer.attention
    normed = layer.norm1(tokens)
    joint = torch.cat([normed, guide], -1) if ('q' in which or 'k' in which) else None
    split = lambda z: rearrange(z, 'N T (H D) -> N T H D', H=att.nheads)
    return (F.elu(split(att.q(joint)))+1 if 'q' in which else None,
            F.elu(split(att.k(joint)))+1 if 'k' in which else None,
            split(att.v(normed)) if 'v' in which else None)


def chunked_class_attention(layer, x, guidance, chunk=256, sums_only=False):
    """class_attention(context=None) for any number of tokens: linear attention only needs key/value sums, so those are
    accumulated over label chunks first, then every chunk attends to the recorded sums (which already include the token itself).
    sums_only: return (None, sums) once they are accumulated."""
    att = layer.attention; T = x.shape[2]
    qkv = lambda tokens, guide, which='qkv': _projections(layer, tokens, guide, which)

    B, C, _, H, W = x.shape
    tokens = lambda i: (rearrange(x[:, :, i:i+chunk], 'B C T H W -> (B H W) T C'), guidance[:, i:i+chunk].repeat_interleave(H*W, 0))
    KV = Ks = 0
    for i in range(0, T, chunk):
        _, k, v = qkv(*tokens(i), 'kv'); KV = KV+torch.einsum('nshd,nshv->nhdv', k, v); Ks = Ks+k.sum(1)
    if T < layer.pad_len:
        pad = layer.pad_len-T
        _, k, v = qkv(layer.padding_tokens.expand(B*H*W, pad, -1), layer.padding_guidance.expand(B*H*W, pad, -1), 'kv')
        KV = KV+torch.einsum('nshd,nshv->nhdv', k, v); Ks = Ks+k.sum(1)
    if sums_only:
        return None, (KV, Ks)
    out = []
    for i in range(0, T, chunk):
        tok, gui = tokens(i); q, _, _ = qkv(tok, gui, 'q')
        num = torch.einsum('nlhd,nhdv->nlhv', q, KV); den = torch.einsum('nlhd,nhd->nlh', q, Ks)
        pooled = tok+rearrange(num/(den[..., None]+att.attention.eps), 'N T H D -> N T (H D)')
        pooled = pooled+layer.MLP(layer.norm2(pooled))
        out.append(x[:, :, i:i+chunk]+rearrange(pooled, '(B H W) T C -> B C T H W', B=B, H=H, W=W))
    return torch.cat(out, 2), (KV, Ks)


@torch.no_grad()
def bank_context(model, feats, ref_text, lean=False):
    """CATSegProbe.context for one window and any bank size: swin_block is per label, so it is chunked.
    lean=True (inference only): stop once the last layer's key/value sums are recorded, so that layer's attention output and
    the bank logits are not computed (ref_logits=None); candidate scores are unchanged."""
    agg = model.transformer
    img, guidance = feats
    g_app = agg.guidance_projection(guidance[0])
    g_ref = agg.text_guidance_projection(ref_text)[None].expand(img.shape[0], -1, -1)
    x = torch.cat([agg.corr_embed(agg.correlation(img, ref_text[None, i:i+128, None].expand(img.shape[0], -1, -1, -1))) for i in range(0, len(ref_text), 128)], 2)
    sums = []
    for layer in agg.layers:
        x = torch.cat([layer.swin_block(x[:, :, i:i+128], g_app) for i in range(0, x.shape[2], 128)], 2)
        x, kv = chunked_class_attention(layer.attention, x, g_ref, sums_only=lean and layer is agg.layers[-1])
        sums.append(kv)
    g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
    return dict(g_app=g_app, g_dec=g_dec, sums=sums, ref_logits=None if lean else model.decode(x, g_dec))
