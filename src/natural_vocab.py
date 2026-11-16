"""Versioned, method-independent ADE wording policy. Historical loaders stay intact."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from labels import load_847
import vocab as V

POLICY = 'ade-natural-v1'


def build_manifest():
    cats = load_847()
    aliases = [[s.strip() for s in c['name'].split(',') if s.strip()] for c in cats]
    first_counts = Counter(a[0] for a in aliases)
    first_names = set(first_counts)
    # Resolve against the FULL registry, never the current candidate vocabulary.
    # Bare generic entries retain their name; ambiguous entries use an official alias.
    selected, used = [], set()
    for cat, names in zip(cats, aliases):
        if first_counts[names[0]] == 1 or len(names) == 1:
            name = names[0]
        else:
            options = [n for n in names[1:] if n not in first_names and n not in used]
            assert options, f'Explicit policy decision required: {cat["name"]}'
            name = options[0]
        assert name not in used, name
        used.add(name)
        selected.append(name)
    assert len(set(selected)) == 847
    _, mapping = V.build_configs()
    historical_source = V.v_cal()
    historical_all = V.names_847()
    source_ids = set(mapping.tolist())
    pool = [i for i, name in enumerate(historical_all)
            if i not in source_ids and name not in set(historical_source)]
    assert len(pool) == 695
    rows = []
    for role, indices, old_names in [('source', mapping.tolist(), historical_source),
                                      ('added', pool, [historical_all[i] for i in pool])]:
        for position, (idx, previous) in enumerate(zip(indices, old_names)):
            rows.append(dict(role=role, position=position, train_id=cats[idx]['trainId'],
                             canonical=cats[idx]['name'], historical_prompt=previous,
                             prompt=selected[idx]))
    manifest = dict(policy=POLICY, rows=rows, source_count=150, added_count=695,
                    selection='First official alias unless ambiguous in full ADE847 registry; bare names retained, other entries use first alternate alias not a primary registry name.',
                    template_file='src/imagenet_template.py',
                    template_sha256=hashlib.sha256(Path('src/imagenet_template.py').read_bytes()).hexdigest(),
                    encoding='Existing 80 templates; normalize each template embedding, average, normalize again. Same frozen text bank for every method using the same text encoder.',
                    threshold_policy='Re-encode source and added labels, then recalibrate every method. Never reuse historical source thresholds.')
    return manifest


def load_manifest(path='meta/natural_vocab_v1.json'):
    manifest = json.loads(Path(path).read_text())
    assert manifest['policy'] == POLICY
    assert hashlib.sha256(Path(manifest['template_file']).read_bytes()).hexdigest() == manifest['template_sha256']
    rows = manifest['rows']
    assert len(rows) == 845 and len({r['train_id'] for r in rows}) == 845
    assert len({r['prompt'] for r in rows}) == 845
    return manifest


if __name__ == '__main__':
    path = Path('meta/natural_vocab_v1.json')
    result = build_manifest()
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    assert load_manifest() == result
    import sclip_clip as clip
    from imagenet_template import openai_imagenet_template as templates
    for row in result['rows']:
        clip.tokenize([t(row['prompt']) for t in templates])
    for role in ['source', 'added']:
        rows = [r for r in result['rows'] if r['role'] == role]
        print(role, len(rows), 'changed:', sum(r['prompt'] != r['historical_prompt'] for r in rows))
    print('Validated immutable IDs, unique wording, template hash, and token capacity:', path)
