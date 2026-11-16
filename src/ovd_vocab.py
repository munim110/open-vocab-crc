"""Vocabulary of the detection benchmark (docs/OVD_DETECTION_BENCHMARK.md): the 80 COCO class names grown by every LVIS v1
category that is not a COCO concept, and the two reference banks.

  Source: the COCO instances category names in category-id order (the standard Grounding DINO COCO prompt).
  Added:  LVIS v1 categories whose synset is not the one LVIS assigns to a COCO thing class (coco_to_synset.json) and
          none of whose qualifier-free synonyms equals a COCO name; prompts by the rule of coco_lvis_vocab.py with the
          COCO names as taken strings; order: seeded permutation (20260925) of the added categories in LVIS id order.
  Bank A: the 80 COCO names. Bank B: the first 80 Open Images names of meta/bank_coco_oi683_v1.json (entries 172 on,
          in bank order) that are neither a COCO name nor an LVIS prompt or synonym.

    PYTHONPATH=src python src/ovd_vocab.py      # writes meta/ovd_coco_lvis_vocab_v1.json, meta/bank_ovd_{a,b}_v1.json
"""
import json
import re
from pathlib import Path

import numpy as np

from coco_lvis_vocab import C2S, LVIS, ORDER_SEED, plain, sha, spaced

COCO = Path('data/coco/annotations/instances_val2017.json')
BANK683 = Path('meta/bank_coco_oi683_v1.json')
PATH = Path('meta/ovd_coco_lvis_vocab_v1.json')


def build():
    coco = sorted(json.loads(COCO.read_text())['categories'], key=lambda c: c['id'])
    source = [c['name'] for c in coco]
    assert len(source) == 80 and len(set(source)) == 80
    cats = sorted(json.loads(LVIS.read_text())['categories'], key=lambda c: c['id'])
    thing_synsets = {v['synset']: k for k, v in json.loads(C2S.read_text()).items()}
    taken = {n.lower() for n in source}
    added, dup = [], {}
    for c in cats:
        if c['synset'] in thing_synsets: dup[c['id']] = dict(lvis_name=c['name'], rule='synset'); continue
        hit = next((p for p in map(plain, c['synonyms']) if p is not None and p in taken), None)
        if hit is not None: dup[c['id']] = dict(lvis_name=c['name'], rule='name', coco=hit); continue
        added.append(c)
    primary = {}
    for c in added:
        p = plain(c['synonyms'][0])
        if p is not None: primary.setdefault(p, []).append(c['id'])
    rows, used = [], set(taken)
    for c in added:
        prompt = None
        for s in c['synonyms']:
            p = plain(s)
            if p is None or p in used: continue
            if p in primary and primary[p] != [c['id']]: continue
            prompt = p; break
        if prompt is None:
            m = re.match(r'^(.*?)_\((.*)\)$', c['name'])
            prompt = f"{spaced(m.group(1))} ({spaced(m.group(2))})" if m else spaced(c['name'])
        assert prompt not in used and ',' not in prompt and '.' not in prompt, (c['name'], prompt)
        used.add(prompt)
        rows.append(dict(role='added', name=c['name'], prompt=prompt, lvis_id=c['id'], synset=c['synset'], frequency=c['frequency']))
    order = np.random.default_rng(ORDER_SEED).permutation(len(rows))
    rows = [dict(role='source', name=n, prompt=n, coco_id=c['id']) for n, c in zip(source, coco)] + [rows[j] for j in order]
    assert len({r['prompt'] for r in rows}) == len(rows)
    lvis_words = {p for c in cats for p in map(plain, c['synonyms']) if p is not None} | {r['prompt'] for r in rows}
    oi = json.loads(BANK683.read_text())['names'][171:]
    bank_b = [n for n in oi if n.lower() not in taken and n.lower() not in lvis_words][:80]
    assert len(bank_b) == 80
    return dict(policy='ovd-coco-lvis-v1', source_labels=80, labels=len(rows), order_seed=ORDER_SEED, rows=rows,
                coco_concepts_in_lvis=dup, inputs={str(p): sha(p) for p in [COCO, LVIS, C2S, BANK683]}), \
        dict(names=source, note='bank A: the 80 COCO names (the standard Grounding DINO COCO prompt)'), \
        dict(names=bank_b, note='bank B: first 80 Open Images names of bank_coco_oi683_v1 that are not COCO or LVIS names')


def load_manifest():
    return json.loads(PATH.read_text())


if __name__ == '__main__':
    m, a, b = build()
    PATH.write_text(json.dumps(m, indent=1))
    Path('meta/bank_ovd_a_v1.json').write_text(json.dumps(a, indent=1))
    Path('meta/bank_ovd_b_v1.json').write_text(json.dumps(b, indent=1))
    rules = [v['rule'] for v in m['coco_concepts_in_lvis'].values()]
    print(PATH, m['labels'], 'labels;', len(rules), 'LVIS categories are COCO concepts', {r: rules.count(r) for r in set(rules)})
    print('bank B:', b['names'][:10], '...')
