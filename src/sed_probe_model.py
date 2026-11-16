"""Standalone SED (ConvNeXt-L, CVPR 2024) inference without detectron2, plus the same reference-anchored forward as CAT-Seg.

SED keeps CAT-Seg's cost-aggregation design but decodes with three gradual-fusion stages, each of which runs linear class
attention across the deployed vocabulary (Up.attention), so its scores are candidate-dependent; in the fast mode the
category early rejection (per-pixel top-K at every stage) is a second candidate-dependent mechanism. The anchored forward
aggregates a fixed reference bank natively and lets every candidate attend to the bank's keys/values plus itself only,
exactly as catseg_probe_model does, so a candidate's score depends on (image, candidate, bank) and not on the other
candidates. Released weights unchanged; nothing is fitted here. Whole-image inference at 768x768 as in the release
(no sliding window, no truncation).
"""
import hashlib
import json
import sys
import types
from pathlib import Path

import torch
import torch.nn.functional as F
from einops import rearrange, repeat

SED = Path(__file__).resolve().parents[2]/'third_party_probe'/'SED'
CKPT = SED.parent/'sed_model_large.pth'
CLIP_MEAN = torch.tensor([122.7709383, 116.7460125, 104.09373615]).view(1, 3, 1, 1)
CLIP_STD = torch.tensor([68.5005327, 66.6321579, 70.3231630]).view(1, 3, 1, 1)


def _import_sed():
    """Import SED's aggregator, templates and its modified open_clip (dense ConvNeXt features) without detectron2."""
    if str(SED/'open_clip'/'src') not in sys.path:
        sys.path.insert(0, str(SED/'open_clip'/'src'))
    for name, sub in [('sed', ''), ('sed.modeling', 'modeling'), ('sed.modeling.transformer', 'modeling/transformer'),
                      ('sed.third_party', 'third_party')]:
        if name not in sys.modules:
            module = types.ModuleType(name)
            module.__path__ = [str(SED/'sed'/sub)]
            sys.modules[name] = module
    from sed.modeling.transformer.model import Aggregator
    from sed.third_party.imagenet_templates import IMAGENET_TEMPLATES
    import open_clip
    return Aggregator, IMAGENET_TEMPLATES, open_clip


class SEDProbe(torch.nn.Module):
    def __init__(self, size='large'):
        super().__init__()
        assert size == 'large', 'only the ConvNeXt-L release is wired up'
        Aggregator, self.templates, open_clip = _import_sed()
        self.clip_model = open_clip.create_model('convnext_large_d_320', pretrained=None, device='cpu').float()
        self.tokenizer = open_clip.get_tokenizer('convnext_large_d_320')
        # configs/convnextL_768.yaml (text guidance off, imagenet 80-template ensemble)
        self.transformer = Aggregator(
            text_guidance_dim=0, text_guidance_proj_dim=0, appearance_guidance_dim=1536, appearance_guidance_proj_dim=128,
            decoder_dims=[64, 32, 16], decoder_guidance_dims=[768, 384, 192], decoder_guidance_proj_dims=[32, 16, 8],
            num_layers=2, nheads=4, hidden_dim=128, pooling_size=[2, 2], feature_resolution=[24, 24], window_size=12,
            attention_type='linear', prompt_channel=len(self.templates), cnext_type='V1', kernel_size=[9, 9, 9])
        state = torch.load(CKPT, map_location='cpu', weights_only=False)['model']
        mapped = {k.replace('sem_seg_head.predictor.', ''): v for k, v in state.items() if k.startswith('sem_seg_head.predictor.')}
        missing, unexpected = self.load_state_dict(mapped, strict=False)
        assert not unexpected, unexpected
        assert all('attn_mask' in k or 'relative_position_index' in k for k in missing), missing
        self.side = 768
        self.eval()

    @torch.no_grad()
    def encode_text(self, names, batch=256):
        """SED's class_embeddings: 80 ImageNet templates per name, each template embedding unit-normalised. [T,80,768]
        Cached on disk per (names, templates) since 845 names are 67,600 prompts through the text tower."""
        device = next(self.parameters()).device
        key = hashlib.sha256(json.dumps([list(names), list(self.templates)]).encode()).hexdigest()[:16]
        path = Path('cache')/f'sed_text_{key}.pt'
        if path.exists():
            return torch.load(path, map_location=device)
        prompts = [t.format(n) for n in names for t in self.templates]
        tokens = self.tokenizer(prompts).to(device)
        out = torch.cat([self.clip_model.encode_text(tokens[i:i+batch]) for i in range(0, len(tokens), batch)]).float()
        out = F.normalize(out, dim=-1).view(len(names), len(self.templates), -1)
        path.parent.mkdir(exist_ok=True); torch.save(out.cpu(), path)
        return out

    def windows(self, image, out_res=768):
        """image: float RGB 0..255 [3,h,w]. SED scores the whole image squashed to 768x768 (one 'window')."""
        return F.interpolate(image[None], size=(out_res, out_res), mode='bilinear', align_corners=False)

    @torch.no_grad()
    def image_features(self, crops):
        x = (crops-CLIP_MEAN.to(crops))/CLIP_STD.to(crops)
        dense = self.clip_model.encode_image(x, dense=True)
        return dense['clip_vis_dense'], [dense[k] for k in ['res5', 'res4', 'res3', 'res2']]

    @staticmethod
    def stitch(logits, out_res=640):
        """Whole-image probabilities resampled to the 640 square used by the samplers (one window, nothing to merge)."""
        return F.interpolate(logits.sigmoid(), size=(out_res, out_res), mode='bilinear', align_corners=False)[0]

    def _prepare(self, feats, text, chunk, stages=3):
        """Cost volume embedding and the per-label correlation guidance (both per label, so chunked), decoder guidance.
        stages: how many stages' correlation guidance to compute (the lean bank pass needs only the first two)."""
        agg = self.transformer
        img, guidance = feats
        projections = list(agg.decoder_corr_guidance_projection)[:stages]
        embed, corr_g = [], [[] for _ in projections]
        for i in range(0, len(text), chunk):
            t = text[None, i:i+chunk].expand(img.shape[0], -1, -1, -1)
            corr = agg.correlation(img, t, self.clip_model.logit_scale)
            embed.append(agg.corr_embed(corr))
            c = rearrange(corr, 'B P T H W -> (B T) P H W')
            for j, proj in enumerate(projections):
                c = proj(c); corr_g[j].append(c)
        g_dec = [p(g) for p, g in zip(agg.decoder_guidance_projection, guidance[1:])]
        return torch.cat(embed, 2), [torch.cat(c) for c in corr_g], g_dec

    @torch.no_grad()
    def forward_bank(self, feats, text, chunk=128, lean=False):
        """Run a vocabulary natively through the three stages, recording each stage's class-attention key/value sums.
        Chunked over labels wherever the computation is per label, so any vocabulary size fits.
        lean=True (inference only): stop once the stage-3 sums are recorded; that stage's attention output, the third fuse,
        its correlation guidance and the head are skipped (ref_logits=None). Candidates read only the sums, so their scores
        are unchanged; `native` keeps the full path."""
        agg = self.transformer
        x, corr_g, g_dec = self._prepare(feats, text, chunk, stages=2 if lean else 3)
        B, T = x.shape[0], x.shape[2]
        x = rearrange(x, 'B C T H W -> (B T) C H W')
        sums = []
        for stage, (up, g) in enumerate(zip([agg.decoder1, agg.decoder2, agg.decoder3], g_dec)):
            last = lean and stage == 2
            x = torch.cat([up.cnext(x[i:i+chunk]) for i in range(0, x.shape[0], chunk)])
            x, kv = sed_class_attention(up.attention, rearrange(x, '(B T) C H W -> B C T H W', B=B), None, chunk, sums_only=last)
            sums.append(kv)
            if last:
                return dict(g_dec=g_dec, sums=sums, ref_logits=None)
            x = rearrange(x, 'B C T H W -> (B T) C H W')
            x = torch.cat([_fuse(up, x[i:i+chunk], g, corr_g[stage][i:i+chunk]) for i in range(0, x.shape[0], chunk)])
        logits = rearrange(torch.cat([agg.head(x[i:i+chunk]) for i in range(0, x.shape[0], chunk)]), '(B T) () H W -> B T H W', B=B)
        return dict(g_dec=g_dec, sums=sums, ref_logits=logits)

    def native(self, feats, text):
        """Released (non-fast) SED under the deployed vocabulary `text` [T,80,768]: [1,T,192,192] logits."""
        return self.forward_bank(feats, text)['ref_logits']

    @torch.no_grad()
    def native_fast(self, feats, text, topk=8, chunk=128):
        """Released fast mode: category early rejection keeps, at each stage, the labels in some pixel's top-K of the
        auxiliary head; rejected labels get probability 0 (logit -100)."""
        agg = self.transformer
        x, corr_g, g_dec = self._prepare(feats, text, chunk)
        B, T = x.shape[0], x.shape[2]
        x = rearrange(x, 'B C T H W -> (B T) C H W')
        keep = torch.arange(T, device=x.device)
        for up, g, cg, head in zip([agg.decoder1, agg.decoder2, agg.decoder3], g_dec, corr_g, [agg.head0, agg.head1, agg.head2]):
            aux = rearrange(head(x), '(B T) () H W -> B T H W', B=B)
            valid = agg.get_valid_idx_from_mask(aux, topk)
            x, keep = x[valid], keep[valid]
            cg = cg[keep]                                            # guidance rows are indexed by original label id
            x = torch.cat([up.cnext(x[i:i+chunk]) for i in range(0, x.shape[0], chunk)])
            x, _ = sed_class_attention(up.attention, rearrange(x, '(B T) C H W -> B C T H W', B=B), None, chunk)
            x = rearrange(x, 'B C T H W -> (B T) C H W')
            x = torch.cat([_fuse(up, x[i:i+chunk], g, cg[i:i+chunk]) for i in range(0, x.shape[0], chunk)])
        logits = agg.head(x)
        out = torch.full((B, T, logits.shape[-2], logits.shape[-1]), -100., device=x.device)
        out[:, keep] = rearrange(logits, '(B T) () H W -> B T H W', B=B)
        return out

    @torch.no_grad()
    def context(self, feats, ref_text, lean=False):
        """Reference bank run natively; per-stage key/value sums for the anchored forward (lean: see forward_bank)."""
        return self.forward_bank(feats, ref_text, lean=lean)

    @torch.no_grad()
    def anchored(self, feats, ctx, cand_text, chunk=128):
        """Score candidates independently of each other against the frozen reference context."""
        agg = self.transformer
        out = []
        for i in range(0, len(cand_text), chunk):
            x, corr_g, _ = self._prepare(feats, cand_text[i:i+chunk], chunk)
            B = x.shape[0]
            x = rearrange(x, 'B C T H W -> (B T) C H W')
            for up, g, cg, kv in zip([agg.decoder1, agg.decoder2, agg.decoder3], ctx['g_dec'], corr_g, ctx['sums']):
                x = up.cnext(x)
                x, _ = sed_class_attention(up.attention, rearrange(x, '(B T) C H W -> B C T H W', B=B), kv, chunk)
                x = _fuse(up, rearrange(x, 'B C T H W -> (B T) C H W'), g, cg)
            out.append(rearrange(agg.head(x), '(B T) () H W -> B T H W', B=B))
        return torch.cat(out, 1)


def _fuse(up, x, guidance, corr_guidance):
    """The rest of Up.forward after the class attention: upsample, concatenate guidance, double conv (per label)."""
    x = up.up(x)
    x = torch.cat([x, repeat(guidance, 'B C H W -> (B T) C H W', T=x.shape[0]//guidance.shape[0]), corr_guidance], 1)
    return up.conv(x)


def sed_class_attention(layer, x, context, chunk=128, sums_only=False):
    """SED's ClassTransformerLayer (pooled tokens, no text guidance) with linear attention over labels.

    context=None: native attention over all given labels; key/value sums are accumulated over label chunks first, then
    every chunk attends to them (which already include the token itself), so any vocabulary size fits. Returns the sums.
    context=(KV, Ks): every label attends to the recorded context plus itself only.
    sums_only (context=None): return (None, sums) once they are accumulated; the attention output is skipped.
    The released `values / v_length ... * v_length` scaling cancels exactly and is omitted.
    """
    att = layer.attention
    B, C, T, H, W = x.shape
    pooled = layer.pool_features(x)
    *_, Hp, Wp = pooled.shape

    def qkv(i, which='qkv'):                                         # query, key, value are separate linear maps: only the named ones are computed
        tok = rearrange(pooled[:, :, i:i+chunk], 'B C T H W -> (B H W) T C')
        normed = layer.norm1(tok)
        split = lambda z: rearrange(z, 'N T (H D) -> N T H D', H=att.nheads)
        return (tok, F.elu(split(att.q(normed)))+1 if 'q' in which else None,
                F.elu(split(att.k(normed)))+1 if 'k' in which else None, split(att.v(normed)) if 'v' in which else None)

    if context is None:
        KV = Ks = 0
        for i in range(0, T, chunk):
            _, _, k, v = qkv(i, 'kv'); KV = KV+torch.einsum('nshd,nshv->nhdv', k, v); Ks = Ks+k.sum(1)
        if sums_only:
            return None, (KV, Ks)
    else:
        KV, Ks = context
    out = []
    for i in range(0, T, chunk):
        tok, q, k, v = qkv(i, 'q' if context is None else 'qkv')
        num = torch.einsum('nlhd,nhdv->nlhv', q, KV); den = torch.einsum('nlhd,nhd->nlh', q, Ks)
        if context is not None:                                      # plus the candidate itself
            self_weight = (q*k).sum(-1)
            num = num+self_weight[..., None]*v; den = den+self_weight
        tok = tok+rearrange(num/(den[..., None]+att.attention.eps), 'N T H D -> N T (H D)')
        tok = tok+layer.MLP(layer.norm2(tok))
        tok = rearrange(tok, '(B H W) T C -> (B T) C H W', B=B, H=Hp, W=Wp)
        tok = F.interpolate(tok, size=(H, W), mode='bilinear', align_corners=True)
        out.append(x[:, :, i:i+chunk]+rearrange(tok, '(B T) C H W -> B C T H W', B=B))
    return torch.cat(out, 2), (KV, Ks)
