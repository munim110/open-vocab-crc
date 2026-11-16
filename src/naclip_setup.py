"""NACLIP backbone (neighbourhood attention + Gaussian spatial prior).

PAMR is deliberately not used: it is a nonlinear, colour-affinity mask
refinement applied *after* the text matmul, which would break the
vocabulary-independence of the cached features. SCLIP's ADE20K config also runs
without it, so both backbones are compared on the same footing.
"""
import naclip_clip as nclip

def load_naclip(path='ViT-B/16', arch='reduced', attn_strategy='naclip', gaussian_std=5.0, device='cuda'):
    net, _ = nclip.load(path, device=device, jit=False)
    net.visual.set_params(arch, attn_strategy, gaussian_std)
    return net
