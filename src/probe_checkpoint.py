"""Resumable per-image probe loops (power-outage safety).

A probe writes one row per image into float16 memmap stores and accumulates small per-image arrays in memory. Every
`every` images the stores are flushed and fsynced, then the in-memory arrays and the next image index are written
atomically to <STORE>/_checkpoint.npz. A rerun with the same protocol (image ids, settings and code hashes) reopens the
stores and continues from that index; a different protocol starts afresh. Rows are independent across images (each
image's pixel sample is seeded by its index), so a resumed run writes the same rows as an uninterrupted one. The
checkpoint is removed when the loop completes, so a finished run leaves nothing to resume from.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np

NAME = '_checkpoint.npz'


def fingerprint(protocol):
    return hashlib.sha256(json.dumps(protocol, sort_keys=True, default=str).encode()).hexdigest()


class Checkpoint:
    def __init__(self, store, protocol, every=25):
        self.store, self.every, self.key = Path(store), every, fingerprint(protocol)
        self.path = self.store/NAME
        self.start, self.state = 0, {}
        if self.path.exists():
            with np.load(self.path, allow_pickle=False) as z:
                if str(z['fingerprint']) == self.key:
                    self.start = int(z['next'])
                    self.state = {k[6:]: z[k] for k in z.files if k.startswith('state_')}
                else:
                    print(f'checkpoint {self.path} is for a different protocol; starting afresh', flush=True)
        if self.start: print(f'resuming from image {self.start} ({self.path})', flush=True)

    def open_stores(self, specs):
        """specs: {name: (shape, dtype)}. Reopens existing stores when resuming, creates them otherwise."""
        stores = {}
        for name, (shape, dtype) in specs.items():
            f = self.store/f'{name}.npy'
            if self.start:
                s = np.lib.format.open_memmap(f, mode='r+')
                assert s.shape == tuple(shape) and s.dtype == np.dtype(dtype), f'{f}: store does not match the checkpoint'
                assert np.any(s[self.start-1] != 0), f'{f}: last checkpointed row is empty; delete {self.path} and rerun'
            else:
                s = np.lib.format.open_memmap(f, mode='w+', dtype=dtype, shape=tuple(shape))
            stores[name] = s
        self.stores = stores
        return stores

    def restore(self, **arrays):
        """Copies saved values into the given in-memory arrays (in place) when resuming."""
        for k, a in arrays.items():
            if k in self.state: a[...] = self.state[k]

    def step(self, k, **arrays):
        """Call after image k is complete; saves every `every` images."""
        if (k+1) % self.every == 0: self.save(k+1, **arrays)

    def save(self, nxt, **arrays):
        for s in self.stores.values():
            s.flush()
            with open(s.filename, 'rb+') as fh: os.fsync(fh.fileno())
        tmp = self.path.with_name(NAME + '.tmp.npz')
        with open(tmp, 'wb') as fh:
            np.savez(fh, fingerprint=np.array(self.key), next=np.array(nxt), **{f'state_{k}': np.asarray(v) for k, v in arrays.items()})
            fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, self.path)

    def finish(self):
        for s in self.stores.values(): s.flush()
        if self.path.exists(): self.path.unlink()
