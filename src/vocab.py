"""Vocabulary configurations: the four transfer regimes.

Calibration vocabulary V_cal is always ADE20K-150 (SCLIP's prompt names).
Each config supplies V_test plus a mapping from evaluation-space GT label to an
index in V_test (or -1 for "not representable", i.e. excluded from the risk).
"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import load_847, load_150, first_syn, ROOT

# SCLIP's ADE20K prompt names (one short name per class) -- this is V_cal.
CLS150 = [l.strip() for l in open('/tmp/SCLIP/configs/cls_ade20k.txt') if l.strip()] \
    if os.path.exists('/tmp/SCLIP/configs/cls_ade20k.txt') else None

# Genuine referential synonyms: same object, different string.
SYNONYMS = {
    'cushion': 'seat cushion', 'sofa': 'couch', 'bicycle': 'bike', 'car': 'automobile', 'airplane': 'aeroplane',
    'television receiver': 'tv set', 'refrigerator': 'fridge', 'stove': 'cooker',
    'ashcan': 'trash can', 'pillow': 'cushion pad', 'rug': 'carpet',
    'windowpane': 'window', 'streetlight': 'street lamp', 'skyscraper': 'high-rise',
    'sidewalk': 'pavement', 'truck': 'lorry', 'minibike': 'motorbike',
    'plaything': 'toy', 'countertop': 'worktop', 'stairway': 'staircase',
    'swivel chair': 'office chair', 'coffee table': 'low table', 'chest of drawers': 'dresser',
    'wardrobe': 'closet', 'bannister': 'handrail', 'signboard': 'sign',
    'pool table': 'billiard table', 'glass': 'drinking glass', 'screen door': 'screened door',
    'apparel': 'clothing', 'earth': 'ground', 'plant': 'vegetation',
    'painting': 'picture', 'sea': 'ocean', 'shelf': 'rack', 'house': 'home',
    'mountain': 'mount', 'path': 'trail', 'runway': 'airstrip', 'booth': 'kiosk',
    'hovel': 'shack', 'canopy': 'awning cover', 'washer': 'washing machine',
    'barrel': 'cask', 'basket': 'hamper', 'tent': 'marquee', 'bag': 'sack',
    'cradle': 'crib', 'oven': 'baking oven', 'tank': 'storage tank',
    'trade name': 'brand name', 'microwave': 'microwave oven', 'pot': 'flowerpot',
    'dishwasher': 'dish washer', 'blanket': 'throw', 'sculpture': 'statue',
    'sconce': 'wall light', 'vase': 'flower vase', 'traffic light': 'traffic signal',
    'tray': 'serving tray', 'fan': 'electric fan', 'pier': 'jetty',
    'crt screen': 'cathode ray tube screen', 'plate': 'dish', 'monitor': 'display',
    'bulletin board': 'notice board', 'radiator': 'heater', 'clock': 'timepiece',
    'flag': 'banner', 'lamp': 'light fixture', 'desk': 'writing desk',
    'armchair': 'easy chair', 'seat': 'bench seat', 'fence': 'fencing',
    'rock': 'stone', 'bathtub': 'bath', 'railing': 'balustrade', 'base': 'pedestal',
    'box': 'container box', 'column': 'pillar', 'counter': 'countertop surface',
    'sink': 'washbasin', 'fireplace': 'hearth', 'grandstand': 'bleachers',
    'case': 'display case', 'river': 'stream', 'bridge': 'overpass',
    'bookcase': 'bookshelf', 'blind': 'window blind', 'toilet': 'lavatory',
    'flower': 'blossom', 'book': 'volume', 'hill': 'hillside', 'bench': 'park bench',
    'palm': 'palm tree', 'kitchen island': 'island counter', 'computer': 'pc',
    'boat': 'vessel', 'bar': 'drinks bar', 'arcade machine': 'video arcade machine',
    'bus': 'coach', 'towel': 'bath towel', 'tower': 'spire', 'chandelier': 'ceiling light',
    'awning': 'sunshade', 'escalator': 'moving staircase', 'ottoman': 'footstool',
    'bottle': 'flask', 'buffet': 'sideboard', 'poster': 'placard', 'stage': 'platform',
    'van': 'minivan', 'ship': 'boat ship', 'fountain': 'water fountain',
    'conveyer belt': 'conveyor', 'swimming pool': 'pool', 'stool': 'bar stool',
    'waterfall': 'cascade', 'ball': 'sports ball', 'food': 'foodstuff', 'step': 'stair step',
    'animal': 'creature', 'lake': 'pond', 'screen': 'partition screen', 'hood': 'range hood',
    'shower': 'shower stall', 'curtain': 'drape', 'chair': 'seat chair', 'table': 'desk table',
    'door': 'doorway', 'mirror': 'looking glass', 'field': 'meadow', 'sand': 'sandy ground',
    'grass': 'lawn', 'cabinet': 'cupboard', 'person': 'human', 'water': 'water body',
    'light': 'lighting', 'pole': 'post', 'land': 'terrain', 'dirt track': 'dirt path',
    'stairs': 'steps', 'ceiling': 'roof interior', 'floor': 'flooring', 'wall': 'walling',
    'building': 'edifice', 'sky': 'skyline', 'tree': 'timber tree', 'road': 'roadway',
    'bed': 'bedstead',
}


def despace(n):
    """SCLIP's ADE convention: multiword class names are written without spaces."""
    return n.replace(' ', '').replace('-', '')


def v_cal():
    assert CLS150 is not None and len(CLS150) == 150
    return list(CLS150)


def names_847():
    """Short class names for A-847, disambiguated.

    Taking only the first synonym collapses distinct classes onto identical
    strings (three ADE classes begin 'bag', two begin 'pot', ...). Identical
    strings would give identical text embeddings and pin the minimum pairwise
    separation at 0 for a preprocessing reason rather than a semantic one, so we
    extend a colliding name with its next synonym until every name is unique.
    """
    cats = load_847()
    syns = [[despace(x.strip()) for x in c['name'].split(',') if x.strip()] for c in cats]
    counts = {}
    for s in syns: counts[s[0]] = counts.get(s[0], 0) + 1
    out, used = [], set()
    for s in syns:
        if counts[s[0]] == 1:
            out.append(s[0]); used.add(s[0]); continue
        nm = s[0]
        for j in range(1, len(s)):
            cand = s[0] + s[j]
            if cand not in used: nm = cand; break
        k = 2
        while nm in used:
            nm = s[0] + str(k); k += 1
        out.append(nm); used.add(nm)
    assert len(set(out)) == len(out) == 847
    return out


SYN_D = None
def syn_lookup(sclip_name):
    global SYN_D
    if SYN_D is None:
        SYN_D = {despace(k): despace(v) for k, v in SYNONYMS.items()}
    return SYN_D.get(sclip_name)


def build_configs(rng_seed=0):
    """Return list of dicts describing each (V_test, label-space) configuration."""
    base = v_cal()
    n847 = names_847()
    c847 = load_847()
    # A-150 class index -> A-847 trainId
    by_name = {c['name']: c for c in c847}
    manual = {'door, double door': 'door', 'crt screen': 'screen, crt screen'}
    long150 = load_150()
    map150_847 = np.array([(by_name.get(n) or by_name[manual[n]])['trainId'] for n in long150])
    # 847 ids that are NOT one of the 150 -> pool of genuinely novel classes.
    # Also drop any whose *string* already appears in V_cal: an exact duplicate
    # name is not a novel class, it is a collision, and it would pin the minimum
    # pairwise separation at 0 for a preprocessing reason.
    in150 = set(map150_847.tolist())
    base_set = set(base)
    novel_pool = [i for i in range(847) if i not in in150 and n847[i] not in base_set]

    cfgs = []
    rng = np.random.default_rng(rng_seed)

    cfgs.append(dict(name='identity', regime='control', space=150,
                     names=base, gt_map=np.arange(150)))

    for k in (120, 100, 75, 50):
        keep = np.sort(rng.choice(150, k, replace=False))
        gm = np.full(150, -1, np.int64); gm[keep] = np.arange(k)
        cfgs.append(dict(name=f'subset_{k}', regime='subset', space=150,
                         names=[base[i] for i in keep], gt_map=gm))

    for frac in (0.25, 0.5, 1.0):
        idx = rng.permutation(150)[:int(150 * frac)]
        nm = list(base)
        nsw = 0
        for i in idx:
            s = syn_lookup(base[i])
            if s: nm[i] = s; nsw += 1
        cfgs.append(dict(name=f'synonym_{int(frac*100)}', regime='synonym', space=150,
                         names=nm, gt_map=np.arange(150), n_swapped=nsw))

    for k in (50, 150, 350, 697):
        add = list(rng.choice(novel_pool, min(k, len(novel_pool)), replace=False))
        cfgs.append(dict(name=f'novel_{k}', regime='novel', space=150,
                         names=base + [n847[i] for i in add], gt_map=np.arange(150)))

    # granularity: evaluate in the 847 label space
    cfgs.append(dict(name='gran_847', regime='granularity', space=847,
                     names=n847, gt_map=np.arange(847)))
    for k in (300, 500):
        # 847-subsets that always retain the 150 anchors
        extra = [i for i in novel_pool]
        rng.shuffle(extra)
        keep = np.sort(np.array(sorted(set(in150) | set(extra[:max(0, k - len(in150))]))))
        gm = np.full(847, -1, np.int64); gm[keep] = np.arange(len(keep))
        cfgs.append(dict(name=f'gran_{len(keep)}', regime='granularity', space=847,
                         names=[n847[i] for i in keep], gt_map=gm))
    return cfgs, map150_847


def separation_sweep(bank, base, n847, novel_pool, ks=(50, 150, 350), device='cuda'):
    """Matched-cardinality probe of the separation axis.

    Injecting k novel classes changes two things at once: |V_test| grows and the
    vocabulary gets more crowded. To tell those apart we inject the *same* k
    classes-worth of vocabulary, drawn either from the classes closest to V_cal
    in text-embedding space ('near') or the furthest ('far'). Cardinality is
    matched by construction, so any gap difference is attributable to separation.
    """
    import torch
    Tb = torch.stack([bank[n] for n in base]).to(device)
    Tp = torch.stack([bank[n847[i]] for i in novel_pool]).to(device)
    sim = (Tp @ Tb.t()).max(1).values          # closeness of each candidate to V_cal
    order = torch.argsort(sim, descending=True).cpu().numpy()
    cfgs = []
    for k in ks:
        if 2 * k > len(order): continue
        for tag, idx in (('near', order[:k]), ('far', order[-k:])):
            add = [novel_pool[i] for i in idx]
            cfgs.append(dict(name=f'sep_{tag}_{k}', regime=f'novel_{tag}', space=150,
                             names=base + [n847[i] for i in add], gt_map=np.arange(150),
                             probe_sim=float(sim[idx].mean().item())))
    return cfgs


if __name__ == '__main__':
    cfgs, m = build_configs()
    print(f'{len(cfgs)} configs')
    for c in cfgs:
        print(f"  {c['name']:14s} regime={c['regime']:12s} space={c['space']:3d} "
              f"|V_test|={len(c['names']):4d} extra={c.get('n_swapped','')}")
    missing = [k for k in v_cal() if k not in SYNONYMS]
    print(f'classes without a synonym: {len(missing)} {missing[:10]}')
