"""Zero-shot baseline with a general multimodal model: Claude Opus 5.5 labels marked pixels of ADE20K images.

A multimodal LLM gives no dense output, so it is asked about K numbered markers per image (Set-of-Mark visual prompting),
placed on the paper's own cached pixel samples (cache/sclip: 4,096 pixels per image) that carry a source label. For each
marker it returns up to ten class names from the given list, most likely first, each with a verbalised probability; the
API returns no token log-probabilities, so the verbalised probability is the score (unlisted labels score 0). Every image is
asked twice, with the 150 source names and with all 845 names (one fixed shuffled order, the 150-name list in the same
relative order), so the only change between the two calls is the list. Prompts, sampling settings and every raw response
are stored; the analysis stage reads only the stored responses (no API call).

Images: a fixed random subset (seed 20261101) of the 2,000 ADE validation images of the main protocol; markers: K of the
cached pixels with a source label, chosen at random at least 3 marker radii apart. Development data. The API keeps inputs
and outputs for up to 30 days and does not train on them; ADE20K images are for non-commercial research use.

Key: the ANTHROPIC_API_KEY environment variable; never printed or stored.

    PYTHONPATH=src .venv/Scripts/python.exe src/exp_claude_baseline.py --stage run --images 20      # pilot
    PYTHONPATH=src .venv/Scripts/python.exe src/exp_claude_baseline.py --stage analyze
"""
import argparse
import base64
import io
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from encode import ADE
from natural_vocab import load_manifest

OUT = Path('results/claude_baseline_ade')
MODEL = 'claude-opus-5-5'
EFFORT = 'low'
K = 15
TOP = 10                       # a 20-image pilot with 5 (results/claude_baseline_ade_pilot_top5) left the true label out at 17% of markers at 845 names
SEED = 20261101
PRICES = dict(input=4.00, output=20.00, cache_read=0.20, cache_write=5.00)      # $ per 1M tokens, claude-opus-5-5, 2026-10
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['markers'], 'properties': {'markers': {'type': 'array', 'items': {
    'type': 'object', 'additionalProperties': False, 'required': ['marker', 'labels'], 'properties': {
        'marker': {'type': 'integer'},
        'labels': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['name', 'probability'],
                                              'properties': {'name': {'type': 'string'}, 'probability': {'type': 'number'}}}}}}}}}
SYSTEM = 'You label regions of photographs. You are given a list of class names and an image with numbered markers.'
INSTRUCTION = ('For each numbered marker (1 to {K}), name the class of the object or surface at the centre of the marker. '
               'Give up to {TOP} candidate classes from the list, most likely first, each with your probability (0 to 1) that it is '
               'the correct class. Use the names exactly as they are written in the list. Answer for every marker.')


def api_key():
    if os.environ.get('ANTHROPIC_API_KEY'):
        return os.environ['ANTHROPIC_API_KEY']
    raise SystemExit('no key: set ANTHROPIC_API_KEY')


def evaluation_images():
    ids = sum([json.loads(Path(f'results/headroom_probe_ade_vitl_bank683{s}/protocol.json').read_text())['image_ids'] for s in ['', '_rest']], [])
    assert len(ids) == 2000
    return [ids[i] for i in np.random.default_rng(SEED).permutation(len(ids))]


def vocabularies():
    names = [r['prompt'] for r in load_manifest()['rows']]
    order = np.random.default_rng(SEED).permutation(len(names))
    return {845: [int(j) for j in order], 150: [int(j) for j in order if j < 150]}, names


def markers(index, meta, gt, img_size):
    """K cached pixels with a source label, at least 3 radii apart; returns (pixel slot, y, x) and the radius."""
    info = meta['meta'][index]; H, W = info['H'], info['W']
    flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
    radius = max(9, round(min(H, W)/45))
    chosen = []
    for slot in np.random.default_rng(SEED+index).permutation(meta['npix']):
        if gt[index][slot] >= 150: continue
        y, x = int(flat[slot]//W), int(flat[slot] % W)
        if not (radius <= y < H-radius and radius <= x < W-radius): continue
        if all((y-yy)**2+(x-xx)**2 >= (3*radius)**2 for _, yy, xx in chosen):
            chosen.append((int(slot), y, x))
        if len(chosen) == K: break
    return chosen, radius


def draw(img, chosen, radius):
    img = img.copy(); d = ImageDraw.Draw(img)
    try: font = ImageFont.truetype('arialbd.ttf', int(radius*1.2))
    except OSError: font = ImageFont.load_default()
    for m, (_, y, x) in enumerate(chosen, 1):
        d.ellipse([x-radius, y-radius, x+radius, y+radius], fill=(255, 230, 0), outline=(0, 0, 0), width=2)
        d.text((x, y), str(m), fill=(0, 0, 0), font=font, anchor='mm')
    buf = io.BytesIO(); img.save(buf, 'JPEG', quality=92)
    return buf.getvalue()


def request(client, names_text, jpeg, n):
    content = [{'type': 'text', 'text': names_text, 'cache_control': {'type': 'ephemeral'}},
               {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': base64.b64encode(jpeg).decode()}},
               {'type': 'text', 'text': INSTRUCTION.format(K=n, TOP=TOP)}]
    t0 = time.time()
    r = client.messages.create(model=MODEL, max_tokens=8000, system=SYSTEM, messages=[{'role': 'user', 'content': content}],
                               output_config={'effort': EFFORT, 'format': {'type': 'json_schema', 'schema': SCHEMA}})
    text = ''.join(b.text for b in r.content if b.type == 'text')
    return dict(text=text, stop_reason=r.stop_reason, model=r.model, seconds=time.time()-t0,
                usage=dict(input=r.usage.input_tokens, output=r.usage.output_tokens,
                           cache_read=r.usage.cache_read_input_tokens or 0, cache_write=r.usage.cache_creation_input_tokens or 0))


def run(a):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key(), max_retries=6)
    meta = json.loads(Path('cache/sclip/meta.json').read_text()); gt = np.load('cache/sclip/gt150.npy')
    vocab, names = vocabularies()
    lists = {V: f'Class names ({V}):\n'+'\n'.join(names[j] for j in vocab[V]) for V in vocab}
    images = evaluation_images()[:a.images]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'protocol.json').write_text(json.dumps(dict(model=MODEL, effort=EFFORT, thinking='adaptive (cannot be disabled on this model)', K=K, top=TOP, seed=SEED,
        max_tokens=8000, system=SYSTEM, instruction=INSTRUCTION, schema=SCHEMA, vocab_order=vocab, names=names, image_order=evaluation_images(),
        sampling='model default (claude-opus-5-5 rejects temperature)', fallbacks='none: a refusal is recorded, not answered by another model',
        note=__doc__.split('\n\n')[0]), indent=1))
    raw = OUT/'raw.jsonl'
    done = {(r['image'], r['V']) for r in map(json.loads, raw.read_text().splitlines())} if raw.exists() else set()
    jobs = []
    for index in images:
        info = meta['meta'][index]
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        chosen, radius = markers(index, meta, gt, img.size)
        jpeg = draw(img, chosen, radius)
        if a.save_marked: (OUT/'marked').mkdir(exist_ok=True); (OUT/'marked'/f'{index}.jpg').write_bytes(jpeg)
        for V in (150, 845):
            if (index, V) not in done: jobs.append((index, V, chosen, radius, jpeg))
    print(f'{len(jobs)} requests ({len(done)} already stored)', flush=True)
    with ThreadPoolExecutor(a.workers) as pool, raw.open('a') as f:
        futs = {pool.submit(request, client, lists[V], jpeg, len(chosen)): (index, V, chosen, radius) for index, V, chosen, radius, jpeg in jobs}
        for n, fut in enumerate(as_completed(futs), 1):
            index, V, chosen, radius = futs[fut]
            try: res = fut.result()
            except Exception as e: res = dict(error=f'{type(e).__name__}: {e}'[:500])
            f.write(json.dumps(dict(image=index, V=V, slots=[c[0] for c in chosen], points=[c[1:] for c in chosen], radius=radius,
                                    time=datetime.now(timezone.utc).isoformat(timespec='seconds'), **res))+'\n'); f.flush()
            if n % 10 == 0 or n == len(jobs): print(f'{n}/{len(jobs)}', flush=True)


def scores(row, names, vocab):
    """[markers, 845] verbalised probability of each label, manifest order (0 if not listed or not in the request's list);
    None if the response is unusable."""
    if 'error' in row or row.get('stop_reason') != 'end_turn': return None
    try: answer = json.loads(row['text'])['markers']
    except (json.JSONDecodeError, KeyError): return None
    lookup = {names[j].strip().lower(): j for j in vocab[row['V']]}
    out = np.zeros((len(row['slots']), len(names))); unmatched = 0
    for m in answer:
        i = m.get('marker', 0)-1
        if not 0 <= i < len(row['slots']): continue
        for lab in m['labels'][:TOP]:
            j = lookup.get(lab['name'].strip().lower())
            if j is None: unmatched += 1
            else: out[i, j] = max(out[i, j], float(np.clip(lab['probability'], 0, 1)))
    return out, unmatched


def analyze(a):
    proto = json.loads((OUT/'protocol.json').read_text()); names = proto['names']; vocab = {int(k): v for k, v in proto['vocab_order'].items()}
    gt = np.load('cache/sclip/gt150.npy')
    rows = [json.loads(l) for l in (OUT/'raw.jsonl').read_text().splitlines()]
    by = {(r['image'], r['V']): r for r in rows}
    cost = sum(r['usage']['input']*PRICES['input']+r['usage']['output']*PRICES['output']+r['usage']['cache_read']*PRICES['cache_read']
               +r['usage']['cache_write']*PRICES['cache_write'] for r in rows if 'usage' in r)/1e6
    stats = {}
    paired = []
    for V in (150, 845):
        good = [(r, s) for r in rows if r['V'] == V for s in [scores(r, names, vocab)] if s is not None]
        y = np.concatenate([gt[r['image']][r['slots']] for r, _ in good]); S = np.concatenate([s for _, (s, _) in good])
        true = S[np.arange(len(y)), y]
        rank = (S > true[:, None]).sum(1)+1
        stats[V] = dict(requests=sum(r['V'] == V for r in rows), usable=len(good), markers=int(len(y)), top1=float(np.mean((rank == 1) & (true > 0))),
                        listed=float(np.mean(true > 0)), mean_true_probability=float(true.mean()), unmatched_names=int(sum(u for _, (_, u) in good)),
                        output_tokens=float(np.mean([r['usage']['output'] for r, _ in good])), input_tokens=float(np.mean([r['usage']['input']+r['usage']['cache_read']+r['usage']['cache_write'] for r, _ in good])),
                        seconds=float(np.mean([r['seconds'] for r, _ in good])))
    for (index, V), r in by.items():
        if V != 150 or (index, 845) not in by: continue
        s0, s1 = scores(r, names, vocab), scores(by[(index, 845)], names, vocab)
        if s0 is None or s1 is None: continue
        y = gt[index][r['slots']]; t0, t1 = s0[0][np.arange(len(y)), y], s1[0][np.arange(len(y)), y]
        paired.append(np.stack([t0, t1, s0[0].argmax(1) == s1[0].argmax(1)], 1))
    p = np.concatenate(paired) if paired else np.zeros((0, 3))
    result = dict(model=MODEL, images=len({r['image'] for r in rows}), cost_usd=cost, cost_per_image_usd=cost/max(1, len({r['image'] for r in rows})), by_vocab={str(k): v for k, v in stats.items()},
                  paired=dict(markers=int(len(p)), true_prob_150=float(p[:, 0].mean()) if len(p) else None, true_prob_845=float(p[:, 1].mean()) if len(p) else None,
                              top1_unchanged=float(p[:, 2].mean()) if len(p) else None, true_prob_changed=float(np.mean(p[:, 0] != p[:, 1])) if len(p) else None))
    (OUT/'results.json').write_text(json.dumps(result, indent=2))
    lines = [f"# Claude Opus 5.5 zero-shot on marked ADE20K pixels ({result['images']} images, K = {K})", '',
             f"Cost ${cost:.2f} (${result['cost_per_image_usd']:.3f} per image, both vocabularies).", '',
             '| Names | Usable / requests | Markers | Top-1 | Listed (top-10) | Mean prob. of true label | Unmatched names | In tokens | Out tokens | Seconds |', '|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for V, s in stats.items():
        lines.append(f"| {V} | {s['usable']}/{s['requests']} | {s['markers']} | {100*s['top1']:.1f}% | {100*s['listed']:.1f}% | {s['mean_true_probability']:.3f} | {s['unmatched_names']} | {s['input_tokens']:.0f} | {s['output_tokens']:.0f} | {s['seconds']:.1f} |")
    pr = result['paired']
    lines += ['', f"Same markers at 150 and 845 names ({pr['markers']}): probability of the true label {pr['true_prob_150']} -> {pr['true_prob_845']}; "
              f"top-1 unchanged at {pr['top1_unchanged']}; true-label probability changed at {pr['true_prob_changed']} of markers."]
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n'); print('\n'.join(lines))


STORES = [('catseg_native', 'native150', 'native845'), ('catseg_anchored', 'anchored845', 'anchored845')]


def crc_threshold(t, alpha):
    """CRC on per-image losses L_i(lam) = share of image i's markers whose true-label score is below lam (sets: score >= lam).
    t: list of arrays of true-label scores per calibration image. Returns the largest lam with (sum_i L_i + 1)/(n + 1) <= alpha."""
    n = len(t)
    s = np.concatenate(t); w = np.concatenate([np.full(len(x), 1/len(x)) for x in t])
    order = np.argsort(s, kind='stable'); s, w = s[order], w[order]
    u, first = np.unique(s, return_index=True)
    below = np.concatenate([[0], np.cumsum(w)])[first]               # sum_i L_i(u_j): weight of scores strictly below u_j
    ok = (below+1)/(n+1) <= alpha
    return u[np.flatnonzero(ok)[-1]]


def crc_stage(a):
    """Reused (calibrated at 150 names, applied at 845) and recalibrated (845) thresholds for Claude, and for CAT-Seg ViT-L native
    and anchored on the same marked pixels (stored scores of the main protocol), over random half splits of the images."""
    proto = json.loads((OUT/'protocol.json').read_text()); names = proto['names']; vocab = {int(k): v for k, v in proto['vocab_order'].items()}
    gt = np.load('cache/sclip/gt150.npy')
    rows = {(r['image'], r['V']): r for r in map(json.loads, (OUT/'raw.jsonl').read_text().splitlines())}
    data = {}
    for (index, V), r in rows.items():
        if V != 150 or (index, 845) not in rows: continue
        s0, s1 = scores(r, names, vocab), scores(rows[(index, 845)], names, vocab)
        if s0 is not None and s1 is not None: data[index] = (np.array(r['slots']), s0[0], s1[0])
    images = sorted(data)
    ids = sum([json.loads(Path(f'results/headroom_probe_ade_vitl_bank683{s}/protocol.json').read_text())['image_ids'] for s in ['', '_rest']], [])
    parts = {k: [np.load(f'cache/headroom_probe_vitl_bank683{s}/{k}.npy', mmap_mode='r') for s in ['', '_rest']] for k in ['native150', 'native845', 'anchored845']}
    n0 = len(parts['native150'][0])
    row = lambda k, index: parts[k][0][ids.index(index)] if ids.index(index) < n0 else parts[k][1][ids.index(index)-n0]
    arms = {}
    y = {i: gt[i][data[i][0]].astype(int) for i in images}
    arms['claude'] = {i: (data[i][1], data[i][2]) for i in images}                     # (scores at 150, scores at 845), [markers, 845]
    for arm, src, grown in STORES:
        arms[arm] = {i: (np.asarray(row(src, i)[data[i][0]], dtype=np.float64), np.asarray(row(grown, i)[data[i][0]], dtype=np.float64)) for i in images}
    alpha, rng = .1, np.random.default_rng(SEED)
    splits = [rng.permutation(len(images)) for _ in range(a.splits)]
    result = dict(images=len(images), markers=int(sum(len(y[i]) for i in images)), alpha=alpha, splits=a.splits, arms={})
    for arm, sc in arms.items():
        true = {i: (sc[i][0][np.arange(len(y[i])), y[i]], sc[i][1][np.arange(len(y[i])), y[i]]) for i in images}
        res = {}
        for mode, (cal_v, eval_v) in dict(reused=(0, 1), recalibrated=(1, 1)).items():
            risk, size = [], []
            for perm in splits:
                cal, ev = [images[j] for j in perm[:len(perm)//2]], [images[j] for j in perm[len(perm)//2:]]
                lam = crc_threshold([true[i][cal_v] for i in cal], alpha)
                risk.append(np.mean([np.mean(true[i][eval_v] < lam) for i in ev]))
                size.append(np.mean([np.mean((sc[i][1] >= lam).sum(1)) for i in ev]))
            res[mode] = dict(mean_risk=float(np.mean(risk)), share_above_alpha=float(np.mean(np.array(risk) > alpha)), mean_size=float(np.mean(size)))
        result['arms'][arm] = res
    (OUT/'crc.json').write_text(json.dumps(result, indent=2))
    lines = [f"# CRC on the marked pixels ({result['images']} images, {result['markers']} markers, alpha = {alpha}, {a.splits} half splits)", '',
             '| Arm | Threshold | Risk at 845 names (%) | Splits above alpha (%) | Set size at 845 names |', '|---|---|---:|---:|---:|']
    for arm, res in result['arms'].items():
        for mode, v in res.items():
            lines.append(f"| {arm} | {mode} | {100*v['mean_risk']:.1f} | {100*v['share_above_alpha']:.0f} | {v['mean_size']:.2f} |")
    lines += ['', 'Reused: calibrated with the 150 source names in the vocabulary, applied with 845. Claude sets include every unlisted label when the threshold is 0. '
              'CAT-Seg ViT-L (683-name bank) scores are the stored logits of the main protocol at the same pixels; the anchored source scores do not depend on the vocabulary.']
    (OUT/'CRC.md').write_text('\n'.join(lines)+'\n'); print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', choices=['run', 'analyze', 'crc'], required=True)
    ap.add_argument('--splits', type=int, default=500)
    ap.add_argument('--images', type=int, default=20)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--save-marked', action='store_true')
    a = ap.parse_args()
    dict(run=run, analyze=analyze, crc=crc_stage)[a.stage](a)
