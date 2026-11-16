"""Unrelated reference vocabularies for the bank ablation: names that are not visual categories at all.

abstract: single-word WordNet 3.0 nouns all of whose noun senses lie in abstract lexicographer files (acts, attributes,
    cognition, communication, feelings, ...; no artifact, object, animal, plant, body, food, substance, location or person
    sense), with a SemCor count of at least 1 so the words are in common use.
pseudo: pronounceable non-words (2-3 consonant-vowel syllables, optionally a final consonant), none a WordNet lemma.

Both drop any name equal (case, punctuation, final s ignored) to a label of COCO-Stuff, ADE, Pascal Context or VOC, a
natural wording in meta/, or an Open Images name, as in build_distractors.py. Draws are seeded; the output lists more
names than a bank needs, and a bank takes a prefix. Needs nltk with the wordnet corpus (not part of .venv-probe; run with
any Python that has it). Output: meta/bank_unrelated_v1.json.
"""
import hashlib, json, re
from pathlib import Path

import numpy as np
from nltk.corpus import wordnet as wn

CATSEG = Path(__file__).resolve().parents[2]/'third_party_probe'/'CAT-Seg'
norm = lambda s: re.sub(r's$', '', re.sub(r'[^a-z ]', ' ', s.lower()).strip())      # as in build_distractors.py
ABSTRACT = {'noun.act', 'noun.attribute', 'noun.cognition', 'noun.communication', 'noun.event', 'noun.feeling', 'noun.motive',
            'noun.phenomenon', 'noun.process', 'noun.quantity', 'noun.relation', 'noun.state', 'noun.time'}
N = 2000
SEED = 20260925


def used_names():
    used = set()
    for f in ['coco', 'ade150', 'ade847', 'pc59', 'pc459', 'voc20']:
        for entry in json.loads((CATSEG/f'datasets/{f}.json').read_text()):
            used |= {norm(part) for part in str(entry).split(',')}
    for f in ['meta/natural_vocab_v1.json', 'meta/pascal_natural_vocab_v1.json']:
        for row in json.loads(Path(f).read_text())['rows']:
            used |= {norm(str(row[k])) for k in ['canonical', 'prompt', 'historical_prompt'] if k in row}
    used |= {norm(n) for n in json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']}
    return used


def main():
    used = used_names()
    lemmas = {l.lower() for s in wn.all_synsets() for l in s.lemma_names()}
    abstract = []
    for w in sorted({l for l in wn.all_lemma_names(pos='n') if re.fullmatch(r'[a-z]{3,}', l)}):
        senses = wn.synsets(w, pos='n')
        if senses and all(s.lexname() in ABSTRACT for s in senses) and sum(l.count() for s in senses for l in s.lemmas() if l.name().lower() == w) >= 1 \
                and norm(w) not in used:
            abstract.append(w)
    rng = np.random.default_rng(SEED)
    abstract = [abstract[i] for i in rng.permutation(len(abstract))[:N]]

    cons, vows = list('bdfgklmnprstvz'), list('aeiou')
    pseudo = set()
    while len(pseudo) < N:
        w = ''.join(rng.choice(cons) + rng.choice(vows) for _ in range(rng.integers(2, 4))) + (rng.choice(cons) if rng.random() < .5 else '')
        if w not in lemmas and norm(w) not in used:
            pseudo.add(w)
    pseudo = sorted(pseudo)
    pseudo = [pseudo[i] for i in rng.permutation(len(pseudo))]

    src = wn.open('data.noun').read().encode()
    out = dict(wordnet=wn.get_version(), wordnet_data_noun_sha256=hashlib.sha256(src).hexdigest(), seed=SEED, abstract_lexnames=sorted(ABSTRACT),
               excluded_names=len(used), abstract=abstract, pseudo=pseudo,
               rule='abstract: single-word WordNet nouns, every noun sense abstract, SemCor count >= 1; pseudo: CV-syllable non-words not in WordNet; '
                    'both dropped if equal (case, punctuation, final s ignored) to any evaluated or trained label, natural wording or Open Images name')
    Path('meta/bank_unrelated_v1.json').write_text(json.dumps(out, indent=1))
    print(len(abstract), 'abstract, e.g.', abstract[:20]); print(len(pseudo), 'pseudo, e.g.', pseudo[:20])


if __name__ == '__main__':
    main()
