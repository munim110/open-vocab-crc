"""Run the two protocol-frozen analyses on the COCO-Stuff + LVIS benchmark without editing them.

src/exp_added_label_risk.py and src/exp_label_exchange.py are named, with their SHA-256, in
docs/PROTOCOL_ADDED_LABEL_RESERVE.md and must stay bit-identical. Both know two datasets (ADE and Pascal Context); for
any dataset other than ADE they read the probe run results/headroom_probe_pascal_<tag>. This wrapper
  1. checks the frozen file's hash,
  2. registers the `coco` dataset in its DATASETS table (manifest meta/coco_lvis_natural_vocab_v1.json, LVIS category
     id as the fine label, cache/coco_pixels/{gt171,gtlvis}.npy),
  3. reads the frozen source and replaces the literal `headroom_probe_pascal` by `headroom_probe_{a.dataset}` (inside the
     same f-strings; identical behaviour for Pascal), and nothing else,
  4. runs its main() with the remaining arguments, and writes wrapper.json (this file's hash, the substitution) next to
     the analysis output.

    PYTHONPATH=src python src/coco_frozen_analyses.py added_label_risk --dataset coco --tag vitl_bank683
    PYTHONPATH=src python src/coco_frozen_analyses.py label_exchange --dataset coco --tag vitl_bank683 --schemes all3 --suffix _delta
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

# file, SHA-256, occurrences of the literal (exp_added_label_risk.py also names it once in a comment)
FROZEN = {'added_label_risk': ('src/exp_added_label_risk.py', 'b12a1deb30db4d3c7ce0dfbc3023630bc322ef8bfa095f33515bbd920be17c50', 3),
          'label_exchange': ('src/exp_label_exchange.py', 'b8b31e68eb3747ce67bf944dda1d8d50c01d731043df4e3377498cf52e5985e1', 2)}
OLD, NEW = 'headroom_probe_pascal', 'headroom_probe_{a.dataset}'


def coco_manifest():
    from coco_lvis_vocab import load_manifest
    return load_manifest()


def coco_entry():
    rows = coco_manifest()['rows']
    return dict(S=171, T=len(rows), sclip='cache/coco_pixels', gt_source='gt171.npy', gt_fine='gtlvis.npy', stores=('native_source', 'native_full', 'anchored_full'),
                manifest=coco_manifest, fine_key='lvis_id', fine='LVIS v1', name='COCO val2017 (LVIS-annotated)')


def main():
    which, argv = sys.argv[1], sys.argv[2:]
    path, digest, count = FROZEN[which]
    raw = Path(path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest, f'{path} is not the frozen version'
    src = raw.decode('utf-8')
    assert src.count(OLD) == count, src.count(OLD)
    import exp_added_label_risk
    exp_added_label_risk.DATASETS.setdefault('coco', coco_entry())         # exp_label_exchange builds its table from this one
    ns = dict(__name__='frozen_'+which, __file__=path)
    exec(compile(src.replace(OLD, NEW), path, 'exec'), ns)
    ns['DATASETS'].setdefault('coco', coco_entry())
    sys.argv = [path]+argv
    ns['main']()
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--dataset'); ap.add_argument('--tag', default='' if which == 'added_label_risk' else 'vitl_bank683'); ap.add_argument('--suffix', default='')
    k, _ = ap.parse_known_args(argv)
    out = Path(f"results/added_label_risk_{k.dataset}{'_'+k.tag if k.tag else ''}") if which == 'added_label_risk' else \
        Path(f'results/label_exchange_{k.dataset}_{k.tag}{k.suffix}')
    (out/'wrapper.json').write_text(json.dumps(dict(wrapper='src/coco_frozen_analyses.py', wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                                   frozen=path, frozen_sha256=digest, substitution=[OLD, NEW], argv=argv), indent=2))


if __name__ == '__main__':
    main()
