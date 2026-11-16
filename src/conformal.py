"""Stage B: conformal risk control under vocabulary shift.

For every configuration we compute, per pixel, only the scalar that decides
coverage (the true class's score). Coverage of pixel p at threshold t is then a
one-dimensional comparison, so calibration and evaluation are O(N*P) regardless
of |V|.

Scores (set C_t(p) and the coverage-deciding scalar u):
  softmax  C = {c : softmax(s*logit)_c >= t}          u = prob of true class   (risk up in t)
  cosine   C = {c : logit_c >= t}                     u = logit of true class  (risk up in t)
  margin   C = {c : max_logit - logit_c <= t}         u = max - true           (risk down in t)
  aps      C = smallest top-prob set with mass >= t   u = mass strictly above  (risk down in t)

APS convention.  Labels are ranked by descending probability, ties broken by
ascending label index (a stable sort), and C is the smallest prefix of that
ranking whose mass reaches t -- so the crossing label, the one that carries the
running mass up to t, is INCLUDED.  Membership is then "the mass strictly
preceding this label is < t", which makes u the *exclusive* cumulative mass and
coverage a STRICT comparison; hence STRICT below.  No randomised tie-breaking is
used.  Including the crossing label keeps C non-empty, so a reported singleton or
empty-set rate describes the predictor rather than the bookkeeping.

Every score must satisfy one invariant: the u-vs-t rule that decides coverage and
the counting rule that reports |C| have to describe the same set.  Earlier
revisions scored APS coverage with the *inclusive* cumulative mass while sizing
the set with the crossing label included, which are two different sets.
"""
import os, sys, json, argparse
import numpy as np, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import ROOT
import vocab as V

LOGIT_SCALE = 40.0
INCREASING = {'softmax': True, 'cosine': True, 'margin': False, 'aps': False}
# Coverage needs a strict inequality for these; the rest compare with >= / <=.
STRICT = {'softmax': False, 'cosine': False, 'margin': False, 'aps': True}
SCORES = ['softmax', 'cosine', 'margin', 'aps']


def grid_bounds(lo, hi, score):
    """Widen the inclusive end of a threshold grid so its endpoint covers all.

    With a strict comparison (APS) a threshold sitting exactly on the largest
    observed score leaves that pixel uncovered, so the CRC fallback would land on
    an endpoint with nonzero loss.  One ulp outward fixes it, and CRC's promise of
    an all-label fallback survives.
    """
    if STRICT[score]:
        f32 = np.float32
        if INCREASING[score]:
            lo = float(np.nextafter(f32(lo), f32(-np.inf)))
        else:
            hi = float(np.nextafter(f32(hi), f32(np.inf)))
    return lo, hi


def covered_mask(u, grid, score):
    """[..., G] bool: is the true class in C_t, for every t in `grid`?

    The single place the coverage comparison is written down, so risk curves and
    the correctness tests cannot drift apart from each other.
    """
    uu = u.unsqueeze(-1)
    g = torch.as_tensor(grid, device=u.device, dtype=u.dtype).reshape(1, -1)
    while g.dim() < uu.dim():
        g = g.unsqueeze(0)
    if INCREASING[score]:
        return uu > g if STRICT[score] else uu >= g
    return uu < g if STRICT[score] else uu <= g


# ---------------------------------------------------------------- text encoding
@torch.no_grad()
def encode_names(net, names, templates, bs=256):
    import sclip_clip as clip
    out = []
    for n in names:
        toks = clip.tokenize([t(n) for t in templates]).cuda()
        f = net.encode_text(toks)
        f = f / f.norm(dim=-1, keepdim=True)
        f = f.mean(0)
        out.append(f / f.norm())
    return torch.stack(out).float()


def text_bank(net, all_names):
    from imagenet_template import openai_imagenet_template as T
    uniq = sorted(set(all_names))
    embs = encode_names(net, uniq, T)
    return {n: embs[i] for i, n in enumerate(uniq)}


# ---------------------------------------------------------------- per-pixel scores
@torch.no_grad()
def true_class_scores(phi, gt, gt_map, Tm, chunk=64):
    """Return dict score -> u[N,P] float32 and valid mask [N,P] bool."""
    N, P, D = phi.shape
    dev = Tm.device
    gm = torch.as_tensor(gt_map, device=dev)
    # APS keeps float64: its scores are cumulative masses that pack together
    # near 1, too tightly for float32 to order in the tail of the ranking.
    U = {s: torch.zeros(N, P, device=dev,
                        dtype=torch.float64 if s == 'aps' else torch.float32)
         for s in SCORES}
    VAL = torch.zeros(N, P, dtype=torch.bool, device=dev)
    for a in range(0, N, chunk):
        b = min(a + chunk, N)
        f = phi[a:b].to(dev).float()                       # [n,P,D]
        g = gt[a:b].to(dev).long()                         # [n,P]
        ig = g >= gm.numel()
        g = g.clamp(max=gm.numel() - 1)
        y = gm[g]
        y = torch.where(ig, torch.full_like(y, -1), y)
        val = y >= 0
        yc = y.clamp(min=0)
        lg = f @ Tm.t()                                    # [n,P,C]
        pr = torch.softmax(LOGIT_SCALE * lg, dim=-1)
        idx = yc.unsqueeze(-1)
        u_cos = lg.gather(-1, idx).squeeze(-1)
        u_sm = pr.gather(-1, idx).squeeze(-1)
        u_mar = lg.max(-1).values - u_cos
        py = u_sm.unsqueeze(-1)
        # Mass strictly preceding the true class in the ranking (descending prob,
        # ties by ascending label index) -- the exclusive cumulative mass.
        ci = torch.arange(pr.shape[-1], device=dev).view(1, 1, -1)
        prd = torch.softmax((LOGIT_SCALE * lg).double(), dim=-1)
        pyd = prd.gather(-1, idx)
        above = (prd > pyd) | ((prd == pyd) & (ci < yc.unsqueeze(-1)))
        u_aps = torch.where(above, prd, torch.zeros_like(prd)).sum(-1)
        del prd, pyd
        for s, u in zip(SCORES, [u_sm, u_cos, u_mar, u_aps]):
            U[s][a:b] = u
        VAL[a:b] = val
        del f, lg, pr
    return U, VAL


@torch.no_grad()
def set_size_curve(phi, Tm, grid, score, npix=256, chunk=32):
    """Mean |C_t| over a pixel subsample, evaluated on the whole grid at once.

    Sorting each pixel's score vector turns "how many classes pass threshold t"
    into a searchsorted, which is what makes sweeping 1024 thresholds cheap.
    """
    N, P, D = phi.shape
    dev = Tm.device
    C = Tm.shape[0]
    sel = torch.linspace(0, P - 1, npix).long().to(dev)
    g = torch.as_tensor(grid, device=dev, dtype=torch.float32)
    tot = torch.zeros(len(g), device=dev, dtype=torch.float64)
    cnt = 0
    for a in range(0, N, chunk):
        b = min(a + chunk, N)
        f = phi[a:b].to(dev).float()[:, sel]
        lg = f @ Tm.t()
        M = lg.reshape(-1, C)
        gg = g.unsqueeze(0).expand(M.shape[0], -1).contiguous()
        if score in ('softmax', 'cosine'):
            v = torch.softmax(LOGIT_SCALE * M, -1) if score == 'softmax' else M
            sv, _ = v.sort(-1)                       # ascending
            n_lt = torch.searchsorted(sv.contiguous(), gg, right=False).float()
            sz = C - n_lt                            # #{score >= t}
        elif score == 'margin':
            m = M.max(-1, keepdim=True).values - M
            sm, _ = m.sort(-1)
            sz = torch.searchsorted(sm.contiguous(), gg, right=True).float()   # #{margin <= t}
        else:                                        # aps -- float64, see above
            pr = torch.softmax((LOGIT_SCALE * M).double(), dim=-1)
            sp, _ = pr.sort(dim=-1, descending=True, stable=True)  # ties by label index
            cs = sp.cumsum(-1)
            gg = gg.double()
            # |C| = smallest prefix reaching t = #{cs < t} + 1, and 0 once t <= 0.
            sz = (torch.searchsorted(cs.contiguous(), gg, right=False).float() + 1).clamp(max=C)
            sz = torch.where(gg > 0, sz, torch.zeros_like(sz))
        tot += sz.sum(0).double()
        cnt += M.shape[0]
        del f, lg, M, gg
    return (tot / cnt).float().cpu().numpy()


# ---------------------------------------------------------------- CRC
def per_image_risk(u, val, grid, score):
    """R[i, g] = fraction of valid pixels of image i uncovered at grid[g]."""
    n = val.sum(1).clamp(min=1).float()
    R = torch.zeros(u.shape[0], len(grid), device=u.device)
    for g, t in enumerate(grid):
        bad = ~covered_mask(u, [t], score).squeeze(-1)
        R[:, g] = (bad & val).sum(1).float() / n
    return R


def crc_lambda(Rcal, grid, alpha, increasing, B=1.0):
    """Conformal risk control threshold on a grid (Angelopoulos et al. 2023)."""
    n, G = Rcal.shape
    bound = (n * Rcal.mean(0) + B) / (n + 1)
    ok = (bound <= alpha).cpu().numpy()
    if increasing:                       # risk grows with t -> take largest feasible t
        idx = np.where(ok)[0]
        return (int(idx.max()) if len(idx) else 0)
    else:                                # risk falls with t -> take smallest feasible t
        idx = np.where(ok)[0]
        return (int(idx.min()) if len(idx) else G - 1)


# ---------------------------------------------------------------- image pools
def pools(N, seed=11, nfit=1000):
    """Disjoint image pools: one to fit a score on, one to run conformal on.

    Experiment 1's scores are data-independent, so calibrating and testing on any
    exchangeable split of the 2000 images is valid.  A *learned* score is not: if
    it were fitted on the same images that later serve as calibration or test
    data, exchangeability between calibration and test would still hold but the
    score would no longer be independent of them, and the comparison against the
    analytic family would be contaminated.  So the learned score sees only `fit`,
    and every conformal number -- for the learned score and for the analytic
    family alike -- is computed inside `conf`.
    """
    p = np.random.default_rng(seed).permutation(N)
    return p[:nfit], p[nfit:]


def conf_splits(conf, nsplits=10, ncal=500, seed=7):
    """Resplits of the conformal pool into calibration and evaluation halves."""
    rng = np.random.default_rng(seed)
    return [conf[rng.permutation(len(conf))] for _ in range(nsplits)]
