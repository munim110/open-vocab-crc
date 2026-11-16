"""Shared loader for the stored headroom-probe scores (development data; the confirmation reserve is never read).

Resolves a dataset/tag pair to the probe runs and score stores exactly as exp_headroom_splits.py and
exp_added_label_risk.py do, applies the same image exclusion (no sampled pixel labelled in the source
vocabulary) and the same 500 random half/half splits (seed 20261003, first 500 draws, as in
exp_added_label_risk.py), and returns per-pixel scores as torch tensors.
"""
import json
from pathlib import Path

import numpy as np
import torch

from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS

SPLIT_SEED = 20261003
STORES = ('native_source', 'native_full', 'anchored_full')      # internal names; ADE stores are native150/native845/anchored845


class Probe:
    def __init__(self, dataset='ade', tag='', runs=0, device=None):
        d = dict(DATASETS[dataset])
        if tag and dataset == 'ade':
            d['runs'] = [f'results/headroom_probe_ade_{tag}', f'results/headroom_probe_ade_{tag}_rest']
            d['caches'] = [f'cache/headroom_probe_{tag}', f'cache/headroom_probe_{tag}_rest']
        elif tag:                                                                # Pascal, COCO: one probe run over all images (exp_headroom_probe_{pascal,coco}.py --tag)
            d['runs'] = [f'results/headroom_probe_{dataset}_{tag}']
            d['caches'] = [f'cache/headroom_probe_{dataset}_{tag}']
        n_runs = runs or len(d['runs'])
        self.dataset, self.tag, self.name = dataset, tag, d['name']
        self.S, self.additions = d['source'], d['additions']; self.T = self.S+self.additions[-1]
        self.dev = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.ids = sum([json.loads((Path(r)/'protocol.json').read_text())['image_ids'] for r in d['runs'][:n_runs]], [])
        assert len(set(self.ids)) == len(self.ids)
        self.gt_all = np.load(f"{d['sclip']}/{d['gt']}")[self.ids]                 # [N, P] uint8; >= S means ignore
        self.meta = json.loads(Path(f"{d['sclip']}/meta.json").read_text())['meta']
        self.files = [self.meta[i]['file'] for i in self.ids]
        self._stores = {k: [np.load(f'{c}/{v}.npy', mmap_mode='r') for c in d['caches'][:n_runs]] for k, v in zip(STORES, d['stores'])}
        self.keep = np.flatnonzero((self.gt_all < self.S).any(1)); self.dropped = len(self.ids)-len(self.keep)
        self.gt = self.gt_all[self.keep]
        self.n_img = len(self.keep); self.n_cal = self.n_img//2
        self.suffix = f'_{tag}' if tag else ''
        self.config = (tag or 'vitb_coco171') if dataset == 'ade' else f'{dataset}_{tag or "vitb_coco171"}'
        self.class_names = self._class_names(d)

    def _class_names(self, d):
        if self.dataset == 'ade':
            from natural_vocab import load_manifest
            rows = load_manifest()['rows']; return [r['canonical'] for r in rows[:self.S]]
        if self.dataset == 'coco':
            from coco_lvis_vocab import load_manifest
            return [r['name'] for r in load_manifest()['rows'][:self.S]]
        lines = [l.split(':', 1)[1].strip() for l in Path('meta/pascal_59_labels.txt').read_text().splitlines() if ':' in l]
        assert len(lines) >= self.S
        return lines[:self.S]

    def scores(self, store, j):
        """Stored scores of kept image j (index into self.keep) as a double tensor [P, W]."""
        k = int(self.keep[j])
        for part in self._stores[store]:
            if k < len(part): return torch.from_numpy(np.array(part[k])).to(self.dev).double()
            k -= len(part)
        raise IndexError(k)

    def splits(self, n_splits=500):
        rng = np.random.default_rng(SPLIT_SEED)
        return [rng.permutation(self.n_img) for _ in range(n_splits)]

    def scenes(self):
        """ADE scene category per kept image (None for other datasets)."""
        if self.dataset != 'ade': return None
        cat = dict(l.split() for l in Path('data/ADEChallengeData2016/sceneCategories.txt').read_text().splitlines() if l.strip())
        return [cat[Path(f).stem] for f in (self.files[k] for k in self.keep)]

    def describe(self, n_splits):
        return (f'{self.n_img} {self.name} images ({self.dropped} without a source-labelled sampled pixel excluded), {self.S} source labels, '
                f'{self.T} after growth, {n_splits} random {self.n_cal}/{self.n_img-self.n_cal} calibration/evaluation splits; configuration {self.config}. '
                'Development data; nothing is fitted; the confirmation reserve is untouched.')


def crc_pick(L, cal, alpha, increasing=True):
    """CRC grid index on calibration images: (sum of losses + 1)/(n + 1) <= alpha, at the last feasible index when the loss grows with the index, the first otherwise."""
    bound = (L[cal].sum(0)+1)/(len(cal)+1)
    ok = np.flatnonzero(bound <= alpha)
    if len(ok) == 0: return 0 if increasing else L.shape[1]-1
    return int(ok[-1] if increasing else ok[0])


__all__ = ['Probe', 'crc_pick', 'ALPHAS', 'LOGIT_GRID', 'STORES']
