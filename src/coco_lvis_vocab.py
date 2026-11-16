"""Natural wording manifest for COCO-Stuff 171 -> + LVIS v1 (policy `coco-lvis-natural-v1`), the third benchmark.

Written before any COCO score was computed (docs/COCO_LVIS_BENCHMARK.md). Source labels: the 171 COCO-Stuff names
exactly as CAT-Seg's released `datasets/coco.json` lists them (the models' training vocabulary, in ground-truth train-id
order). Added labels: every LVIS v1 category that is not a source concept, in a seeded random order (nested additions
are prefixes of this order).

An LVIS category is a source concept when
  * its WordNet synset is the one the LVIS authors assign to a COCO thing class (lvis-api data/coco_to_synset.json), or
  * one of its synonyms, with underscores read as spaces and no parenthetical qualifier, equals a source name after
    dropping COCO-Stuff's `-other` / `-stuff` / `-merged` suffix (so `straw_(for_drinking)` is not COCO-Stuff `straw`).
Such categories are dropped from the added list; their pixels keep the COCO-Stuff label.

Prompt of an added label: the first LVIS synonym, underscores read as spaces, without a parenthetical qualifier, that
is not the prompt of a source label or the qualifier-free first synonym of another LVIS category; if none exists, the
LVIS name with its qualifier in parentheses ("bat (animal)"). Prompts are unique and contain no comma.

    PYTHONPATH=src python src/coco_lvis_vocab.py           # on a machine with data/lvis and the CAT-Seg checkout
"""
import hashlib
import json
import re
from pathlib import Path

PATH = Path('meta/coco_lvis_natural_vocab_v1.json')
LVIS = Path('data/lvis/lvis_v1_val.json')
C2S = Path('data/lvis/coco_to_synset.json')
ORDER_SEED = 20260925


def spaced(s):
    return s.replace('_', ' ').strip().lower()


def plain(s):
    """Synonym as words, or None if it carries a parenthetical qualifier."""
    return None if '(' in s else re.sub(r'\s+', ' ', spaced(s))


def base(n):
    return re.sub(r'-(other|stuff|merged)$', '', n).replace('-', ' ')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build():
    import numpy as np
    from catseg_probe_model import CATSEG
    source = json.loads((CATSEG/'datasets/coco.json').read_text())
    assert len(source) == 171 and len(set(source)) == 171
    cats = sorted(json.loads(LVIS.read_text())['categories'], key=lambda c: c['id'])
    assert len(cats) == 1203
    c2s = json.loads(C2S.read_text())
    thing_synsets = {v['synset']: k for k, v in c2s.items()}
    by_word = {}
    for i, n in enumerate(source):
        by_word.setdefault(n.lower(), i); by_word.setdefault(base(n).lower(), i)
    dup, added = {}, []
    for c in cats:
        hit = source.index(thing_synsets[c['synset']]) if c['synset'] in thing_synsets else \
            next((by_word[p] for p in map(plain, c['synonyms']) if p is not None and p in by_word), None)
        if hit is None: added.append(c)
        else: dup[c['id']] = dict(lvis_name=c['name'], source=source[hit], source_id=hit, rule='synset' if c['synset'] in thing_synsets else 'synonym')
    taken = {n.lower() for n in source}
    primary = {}                                                # qualifier-free first synonym of each LVIS category
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
        assert prompt not in used and ',' not in prompt, (c['name'], prompt)
        used.add(prompt)
        rows.append(dict(role='added', name=c['name'], prompt=prompt, lvis_id=c['id'], synset=c['synset'], frequency=c['frequency']))
    order = np.random.default_rng(ORDER_SEED).permutation(len(rows))
    rows = [dict(role='source', name=n, prompt=n, source_id=i) for i, n in enumerate(source)]+[rows[j] for j in order]
    assert len({r['prompt'] for r in rows}) == len(rows)
    return dict(policy='coco-lvis-natural-v1', source_labels=171, labels=len(rows), order_seed=ORDER_SEED, rows=rows,
                source_concepts_in_lvis=dup, inputs={str(LVIS): sha(LVIS), str(C2S): sha(C2S), 'CAT-Seg datasets/coco.json': sha(CATSEG/'datasets/coco.json')})


def load_manifest():
    return json.loads(PATH.read_text())


if __name__ == '__main__':
    m = build()
    PATH.write_text(json.dumps(m, indent=1))
    rules = [v['rule'] for v in m['source_concepts_in_lvis'].values()]
    print(PATH, m['labels'], 'labels;', len(rules), 'LVIS categories are source concepts', {r: rules.count(r) for r in set(rules)})
