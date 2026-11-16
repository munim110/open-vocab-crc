"""Vocabulary construction for ADE20K-150 / ADE20K-847."""
import ast, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_847():
    txt = open(os.path.join(ROOT, 'meta/register_ade20k_full.py')).read()
    start = txt.index('ADE20K_SEM_SEG_FULL_CATEGORIES = [')
    start = txt.index('[', start)
    depth, i = 0, start
    while True:
        if txt[i] == '[': depth += 1
        elif txt[i] == ']':
            depth -= 1
            if depth == 0: break
        i += 1
    cats = ast.literal_eval(txt[start:i+1])
    assert len(cats) == 847, len(cats)
    return cats

def load_150():
    rows = open(os.path.join(ROOT, 'data/ADEChallengeData2016/objectInfo150.txt')).read().strip().split('\n')[1:]
    names = [r.split('\t')[-1].strip() for r in rows]
    assert len(names) == 150
    return names

def first_syn(n):
    return n.split(',')[0].strip()

if __name__ == '__main__':
    c847 = load_847(); n150 = load_150()
    print('847:', len(c847), '| unique ids:', len({c['id'] for c in c847}))
    by_name = {c['name']: c for c in c847}
    by_first = {}
    for c in c847: by_first.setdefault(first_syn(c['name']), []).append(c)
    exact = [n for n in n150 if n in by_name]
    print(f'exact 150->847 name match: {len(exact)}/150')
    miss = [n for n in n150 if n not in by_name]
    print('misses:', len(miss))
    for n in miss:
        f = first_syn(n)
        cand = by_first.get(f, [])
        print(f'  {n[:55]!r:60s} -> first={f!r} cand={[c["name"][:40] for c in cand]}')
