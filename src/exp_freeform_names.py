"""Free-form per-image names from a general multimodal model (docs/FREEFORM_NAMES_PROTOCOL.md).

Claude Opus 5.5 lists what it sees in each ADE20K image, with no list of names shown, so the names are not restricted to
ADE20K-847. Every raw response is stored; the analysis stage normalises the names, drops those already deployed (the 150
source prompts and their canonical ADE synonyms) and duplicates, and writes names.json, the per-image added names that
exp_freeform_vocab_probe.py deploys after the 150 source names. Images: the 2,000 ADE validation images of the main
protocol, in probe order. Development data. The API keeps inputs and outputs for up to 30 days and does not train on them;
ADE20K images are for non-commercial research use.

Key: the ANTHROPIC_API_KEY environment variable; never printed or stored.

    PYTHONPATH=src .venv/Scripts/python.exe src/exp_freeform_names.py --stage run --images 20      # pilot
    PYTHONPATH=src .venv/Scripts/python.exe src/exp_freeform_names.py --stage run --images 2000
    PYTHONPATH=src .venv/Scripts/python.exe src/exp_freeform_names.py --stage analyze
"""
import argparse
import base64
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from encode import ADE
from exp_claude_baseline import EFFORT, MODEL, PRICES, api_key
from natural_vocab import load_manifest

OUT = Path('results/freeform_names_ade')
MAX_NAMES = 30
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['names'],
          'properties': {'names': {'type': 'array', 'items': {'type': 'string'}}}}
SYSTEM = 'You name what is visible in photographs.'
INSTRUCTION = ('List what is visible in this image: objects, parts of the scene, and surfaces or materials. Use short common English '
               'nouns or noun phrases in the singular, as a person would type them to search for each thing. Give up to '
               f'{MAX_NAMES} names, the most prominent first, each once.')


def evaluation_images():
    ids = sum([json.loads(Path(f'results/headroom_probe_ade_vitl_bank683{s}/protocol.json').read_text())['image_ids'] for s in ['', '_rest']], [])
    assert len(ids) == 2000
    return ids


def normalise(name):
    return re.sub(r'\s+', ' ', name.lower()).strip(' \t\n.,;:!?"\'()[]{}-_*')


def request(client, jpeg):
    content = [{'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': base64.b64encode(jpeg).decode()}},
               {'type': 'text', 'text': INSTRUCTION}]
    t0 = time.time()
    r = client.messages.create(model=MODEL, max_tokens=4000, system=SYSTEM, messages=[{'role': 'user', 'content': content}],
                               output_config={'effort': EFFORT, 'format': {'type': 'json_schema', 'schema': SCHEMA}})
    text = ''.join(b.text for b in r.content if b.type == 'text')
    return dict(text=text, stop_reason=r.stop_reason, model=r.model, seconds=time.time()-t0,
                usage=dict(input=r.usage.input_tokens, output=r.usage.output_tokens,
                           cache_read=r.usage.cache_read_input_tokens or 0, cache_write=r.usage.cache_creation_input_tokens or 0))


def run(a):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key(), max_retries=6)
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    images = evaluation_images()[:a.images]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'protocol.json').write_text(json.dumps(dict(model=MODEL, effort=EFFORT, thinking='adaptive (cannot be disabled on this model)', max_tokens=4000,
        system=SYSTEM, instruction=INSTRUCTION, schema=SCHEMA, image_order=evaluation_images(), input='the original ADE20K validation JPEG',
        sampling='model default (claude-opus-5-5 rejects temperature)', fallbacks='none: a refusal or empty answer is recorded, the image gets no added names',
        note=__doc__.split('\n\n')[0]), indent=1))
    raw = OUT/'raw.jsonl'
    done = {r['image'] for r in map(json.loads, raw.read_text().splitlines()) if 'error' not in r} if raw.exists() else set()
    jobs = [i for i in images if i not in done]
    print(f'{len(jobs)} requests ({len(done)} already stored)', flush=True)
    with ThreadPoolExecutor(a.workers) as pool, raw.open('a') as f:
        futs = {pool.submit(request, client, (Path(ADE)/'images/validation'/meta['meta'][i]['file']).read_bytes()): i for i in jobs}
        for n, fut in enumerate(as_completed(futs), 1):
            index = futs[fut]
            try: res = fut.result()
            except Exception as e: res = dict(error=f'{type(e).__name__}: {e}'[:500])
            f.write(json.dumps(dict(image=index, time=datetime.now(timezone.utc).isoformat(timespec='seconds'), **res))+'\n'); f.flush()
            if n % 25 == 0 or n == len(jobs): print(f'{n}/{len(jobs)}', flush=True)


def analyze(a):
    rows = {}
    for r in map(json.loads, (OUT/'raw.jsonl').read_text().splitlines()):
        if r['image'] not in rows or 'error' in rows[r['image']]: rows[r['image']] = r      # a retried request replaces an error
    manifest = load_manifest()['rows']
    synonyms = lambda r: {normalise(r['prompt'])} | {normalise(s) for s in r['canonical'].split(',')}
    source = set().union(*[synonyms(r) for r in manifest[:150]])
    ade = set().union(*[synonyms(r) for r in manifest])
    oi = json.loads(Path('meta/distractors_openimages_v1.json').read_text())['names']
    lexicon = ade | {normalise(n) for n in oi}       # the 17,001-name lexicon of exp_lexicon_probe.py (845 names + Open Images), with ADE synonyms
    images = [i for i in evaluation_images() if i in rows]
    added, raw_counts, failed = {}, [], []
    for i in images:
        r = rows[i]
        try: names = json.loads(r['text'])['names'] if 'error' not in r and r.get('stop_reason') == 'end_turn' else None
        except (json.JSONDecodeError, KeyError): names = None
        if names is None: failed.append(i); added[i] = []; continue
        raw_counts.append(len(names)); seen, keep = set(source), []
        for n in map(normalise, names):
            if n and n not in seen: seen.add(n); keep.append(n)
        added[i] = keep
    flat = [n for i in images for n in added[i]]; unique = sorted(set(flat))
    cost = sum(r['usage']['input']*PRICES['input']+r['usage']['output']*PRICES['output']+r['usage']['cache_read']*PRICES['cache_read']
               +r['usage']['cache_write']*PRICES['cache_write'] for r in rows.values() if 'usage' in r)/1e6
    stats = dict(images=len(images), failed=failed, cost_usd=cost, cost_per_image_usd=cost/max(1, len(images)),
                 answered_names_per_image=float(np.mean(raw_counts)), added_names_per_image=float(np.mean([len(added[i]) for i in images])),
                 max_added=max(len(added[i]) for i in images), unique_added=len(unique),
                 share_outside_ade847=float(np.mean([n not in ade for n in flat])), unique_share_outside_ade847=float(np.mean([n not in ade for n in unique])),
                 share_outside_lexicon=float(np.mean([n not in lexicon for n in flat])), unique_share_outside_lexicon=float(np.mean([n not in lexicon for n in unique])),
                 seconds=float(np.mean([r['seconds'] for r in rows.values() if 'seconds' in r])),
                 output_tokens=float(np.mean([r['usage']['output'] for r in rows.values() if 'usage' in r])),
                 input_tokens=float(np.mean([r['usage']['input'] for r in rows.values() if 'usage' in r])))
    common = [n for n, _ in sorted(((n, flat.count(n)) for n in unique), key=lambda t: -t[1])[:40]]
    outside = [n for n in common if n not in ade]
    (OUT/'names.json').write_text(json.dumps(dict(image_ids=images, added={str(i): added[i] for i in images}, normalisation=normalise.__name__ +
        ': lower case, inner whitespace collapsed, outer whitespace and punctuation stripped; source prompts and their canonical ADE synonyms and repeats dropped'), indent=1))
    (OUT/'results.json').write_text(json.dumps(dict(**stats, most_common=common), indent=2))
    lines = [f"# Free-form names from {MODEL} ({stats['images']} ADE20K images)", '',
             f"Cost ${cost:.2f} (${stats['cost_per_image_usd']:.4f} per image); {len(failed)} images without a usable answer.", '',
             f"Names answered per image {stats['answered_names_per_image']:.1f}; added after dropping deployed source names and repeats "
             f"{stats['added_names_per_image']:.1f} (max {stats['max_added']}); {stats['unique_added']} unique added names.",
             f"Outside the 845 ADE20K-847 names and their synonyms: {100*stats['share_outside_ade847']:.1f}% of added names "
             f"({100*stats['unique_share_outside_ade847']:.1f}% of unique ones). Outside the 17,001-name lexicon: "
             f"{100*stats['share_outside_lexicon']:.1f}% ({100*stats['unique_share_outside_lexicon']:.1f}% of unique ones).", '',
             'Most common added names: '+', '.join(common), '', 'Of these, outside ADE20K-847: '+', '.join(outside)]
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n'); print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', choices=['run', 'analyze'], required=True)
    ap.add_argument('--images', type=int, default=20)
    ap.add_argument('--workers', type=int, default=6)
    a = ap.parse_args()
    dict(run=run, analyze=analyze)[a.stage](a)
