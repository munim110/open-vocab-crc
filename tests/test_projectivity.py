"""Stage A, item 4: is a score's membership actually independent of the vocabulary?

H1 in the plan says a candidate-independent score with a frozen threshold keeps
its image loss under carrier-preserving edits.  That is a claim about the code as
much as about the mathematics, so these checks edit the vocabulary underneath a
frozen threshold -- permute it, add labels, delete non-carrier labels, change the
chunk size -- and demand that the shared labels' scores, their membership and the
per-image loss all land in exactly the same place.

They also record which of the shipped scores are candidate-*dependent*.  That is
not a defect: softmax, margin and APS are the vocabulary-dependent comparators
the paper argues against, and a run in which they failed to move would mean the
intervention never happened.

Run: python3 tests/test_projectivity.py
"""
import os, sys
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'src'))
sys.path.insert(0, HERE)
import conformal as C

DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
PROJECTIVE = {'cosine'}                   # the only shipped score with no |V| coupling
# Widening the text matrix changes the GEMM shape, so a projective score comes
# back reassociated rather than bit-identical.  Anything above this is structure,
# not arithmetic; anything below is reported, never silently absorbed.
DRIFT_TOL = 1e-5
FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)
        print(f'    FAIL {msg}')
    return cond


def make_world(Cn=40, N=6, P=64, D=32, seed=0):
    """A canonical label universe, pixel features, and carriers drawn from V0."""
    g = torch.Generator().manual_seed(seed)
    Tall = torch.randn(Cn, D, generator=g)
    Tall = (Tall / Tall.norm(dim=-1, keepdim=True)).to(DEV)
    phi = torch.randn(N, P, D, generator=g)
    phi = (phi / phi.norm(dim=-1, keepdim=True)).to(DEV)
    v0 = list(range(24))                                   # source vocabulary V0
    carriers = list(range(20))                             # 20..23 are in V0 but unused,
    gt = torch.tensor(np.random.default_rng(seed)          # so they are legal to delete
                      .choice(carriers, size=(N, P))).long()
    return Tall, phi, gt, v0


def score_under(Tall, phi, gt, ids, chunk=64):
    """Score every pixel under vocabulary `ids` (a list of canonical label ids)."""
    Tm = Tall[torch.as_tensor(ids, device=DEV)]
    gmv = np.full(65536, -1, np.int64)
    for pos, cid in enumerate(ids):
        gmv[cid] = pos
    return C.true_class_scores(phi, gt, gmv, Tm, chunk=chunk)


def flips(u0, u1, val, t, score):
    """Membership changes at threshold t, split into structural vs near-threshold."""
    c0 = C.covered_mask(u0, [t], score).squeeze(-1) & val
    c1 = C.covered_mask(u1, [t], score).squeeze(-1) & val
    diff = c0 != c1
    near = (u0 - t).abs() <= DRIFT_TOL * max(1.0, abs(t))
    return int((diff & ~near).sum()), int((diff & near).sum())


def loss_at(u, val, t, score):
    """Per-image false-negative loss, the quantity CRC controls."""
    bad = ~C.covered_mask(u, [t], score).squeeze(-1)
    return ((bad & val).sum(1).float() / val.sum(1).clamp(min=1).float())


# ------------------------------------------------------------------ tests
def _edit_case(name, edit, seed):
    """Score under V0 and under an edited vocabulary; compare shared labels."""
    Tall, phi, gt, v0 = make_world(seed=seed)
    U0, VAL = score_under(Tall, phi, gt, v0)
    v1 = edit(v0, Tall.shape[0])
    U1, VAL1 = score_under(Tall, phi, gt, v1)
    check(bool((VAL == VAL1).all()), f'{name}: the valid-pixel mask moved')
    for s in C.SCORES:
        t = float(np.median(U0[s][VAL].cpu().numpy()))
        st, nr = flips(U0[s], U1[s], VAL, t, s)
        d = float((U0[s] - U1[s]).abs().max())
        l0, l1 = loss_at(U0[s], VAL, t, s), loss_at(U1[s], VAL1, t, s)
        dl = float((l0 - l1).abs().max())
        if s in PROJECTIVE:
            check(d <= DRIFT_TOL, f'{name}/{s}: shared-label score moved by {d:.3e}, '
                                  f'above the {DRIFT_TOL:.0e} float-noise bar')
            check(st == 0, f'{name}/{s}: {st} structural membership flips')
            print(f'      {name}/{s}: projective -- max |du|={d:.3e}, '
                  f'{st} structural flips, {nr} near-threshold flips, '
                  f'max loss move {dl:.3e}')
        else:
            print(f'      {name}/{s}: candidate-dependent as expected '
                  f'-- max |du|={d:.3e}, loss moves by {dl:.3f}')


def test_permutation():
    print('  test_permutation (relabel V0 in a different order)')
    _edit_case('permute', lambda v, C_: list(np.random.default_rng(1).permutation(v)), 1)


def test_addition():
    print('  test_addition (append distractors, carriers retained)')
    _edit_case('add', lambda v, C_: list(v) + list(range(len(v), C_)), 2)


def test_deletion():
    print('  test_deletion (drop non-carrier labels, carriers retained)')
    # carriers are ids 0..19, so only the unused 20..23 tail may go: deleting a
    # carrier is a different intervention and is out of the guaranteed setting.
    _edit_case('delete', lambda v, C_: [c for c in v if c < 20], 3)


def test_chunk_size():
    """Batching is an implementation detail and must not touch any score."""
    print('  test_chunk_size')
    Tall, phi, gt, v0 = make_world(seed=4)
    Ua, VALa = score_under(Tall, phi, gt, v0, chunk=64)
    Ub, VALb = score_under(Tall, phi, gt, v0, chunk=1)
    check(bool((VALa == VALb).all()), 'chunk: valid mask changed')
    for s in C.SCORES:
        d = float((Ua[s] - Ub[s]).abs().max())
        check(d == 0.0, f'chunk/{s}: score changed by {d:.3e} between chunk sizes')


def test_risk_transfer_over_a_sequence():
    """P3: a whole adaptive edit trace must leave the loss of a frozen score alone."""
    print('  test_risk_transfer_over_a_sequence')
    Tall, phi, gt, v0 = make_world(seed=5)
    U0, VAL = score_under(Tall, phi, gt, v0)
    rng = np.random.default_rng(7)
    for s in C.SCORES:
        t = float(np.quantile(U0[s][VAL].cpu().numpy(), 0.9))
        base = loss_at(U0[s], VAL, t, s)
        v = list(v0)
        moved = 0.0
        for step in range(5):                    # edits chosen as we go, per P3
            extra = [c for c in range(Tall.shape[0]) if c not in v]
            if extra:
                v = v + list(rng.choice(extra, size=min(4, len(extra)), replace=False))
            v = [c for c in v if c < 20 or rng.random() > 0.3]   # carriers kept
            U, VALs = score_under(Tall, phi, gt, v)
            moved = max(moved, float((loss_at(U[s], VALs, t, s) - base).abs().max()))
        if s in PROJECTIVE:
            check(moved <= DRIFT_TOL, f'sequence/{s}: loss moved by {moved:.3e} over 5 edits')
            print(f'      sequence/{s}: loss moves by at most {moved:.3e} over 5 edits')
        else:
            print(f'      sequence/{s}: loss moves by up to {moved:.3f} (expected)')


def test_nonprojective_scores_do_move():
    """If the vocabulary-dependent comparators did not move, nothing was edited."""
    print('  test_nonprojective_scores_do_move')
    Tall, phi, gt, v0 = make_world(seed=6)
    U0, VAL = score_under(Tall, phi, gt, v0)
    U1, _ = score_under(Tall, phi, gt, list(v0) + list(range(24, 40)))
    for s in C.SCORES:
        d = float((U0[s] - U1[s]).abs().max())
        if s in PROJECTIVE:
            check(d <= DRIFT_TOL, f'{s}: expected projective, moved by {d:.3e}')
        else:
            check(d > DRIFT_TOL, f'{s}: expected candidate-dependent, but moved only {d:.3e}')


def main():
    print(f'device={DEV}')
    for fn in [test_permutation, test_addition, test_deletion, test_chunk_size,
               test_risk_transfer_over_a_sequence, test_nonprojective_scores_do_move]:
        try:
            fn()
        except Exception as e:
            FAILURES.append(f'{fn.__name__} raised {type(e).__name__}: {e}')
            print(f'    ERROR {fn.__name__}: {type(e).__name__}: {e}')
    print()
    if FAILURES:
        print(f'{len(FAILURES)} FAILURE(S):')
        for f in FAILURES:
            print('  -', f)
        return 1
    print('all projectivity checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
