"""Brute-force check of exp_set_constructions.per_image: enumerate the sets pixel by pixel at every grid point
and compare loss and size curves with the searchsorted/bincount version. Run: PYTHONPATH=src python tests/test_set_constructions.py"""
import numpy as np
import torch

from exp_set_constructions import CONSTRUCTIONS, K_REG, LAMBDA, grids, per_image

torch.manual_seed(0)
n, W = 37, 9
z = (torch.randn(n, W, dtype=torch.float64)*8).clamp(-30, 30)
z[3, :4] = z[3, 0]                                      # ties
y = torch.randint(0, W, (n,))
G = {c: g for c, g in grids(W).items()}
G['logit'] = G['logit'][::97]; G['softmax'] = G['softmax'][::13]; G['aps'] = G['aps'][::13]; G['raps'] = G['raps'][::11]
loss, size, ref = per_image(z, y, G)
p = z.softmax(-1)
for c in CONSTRUCTIONS:
    for gi, t in enumerate(G[c].tolist()):
        members = np.zeros((n, W), bool)
        for i in range(n):
            if c == 'logit': members[i] = (z[i] >= t).numpy()
            elif c == 'softmax': members[i] = (p[i] >= t).numpy()
            else:
                order = sorted(range(W), key=lambda j: (-p[i, j].item(), j))
                mass = 0.0
                for r, j in enumerate(order):
                    v = mass+(LAMBDA*max(0, r+1-K_REG) if c == 'raps' else 0)
                    members[i, j] = v < t
                    mass += p[i, j].item()
        miss = 1-members[np.arange(n), y.numpy()].mean()
        assert abs(miss-loss[c][gi]) < 1e-12, (c, t, miss, loss[c][gi])
        assert abs(members.sum(1).mean()-size[c][gi]) < 1e-9, (c, t, members.sum(1).mean(), size[c][gi])
rank = (z > z[torch.arange(n), y][:, None]).sum(1)
assert abs(ref['top1']-(rank >= 1).double().mean().item()) < 1e-12 and abs(ref['top5']-(rank >= 5).double().mean().item()) < 1e-12
print('set constructions: loss and size curves match brute-force enumeration for', CONSTRUCTIONS)
