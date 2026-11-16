"""Natural wording manifest for Pascal Context 59 -> 459 (policy `pascal-natural-v1`).

Written before any Pascal headroom score was computed. The release names are used verbatim
except for the fused or dataset-specific spellings below; every arm receives the same prompt.
Rows: the 59 source labels in ground-truth order, then the other names of the 459 release in
release order. `unknown` marks unlabelled pixels and is not a label.
"""
import json
from pathlib import Path

import pascal_labels as PL

PATH = Path('meta/pascal_natural_vocab_v1.json')
WORDING = {'aeroplane': 'airplane', 'motorbike': 'motorcycle', 'pottedplant': 'potted plant', 'tvmonitor': 'tv monitor',
           'bedclothes': 'bedding', 'crabstick': 'crab stick', 'flagstaff': 'flagpole', 'hydrovalve': 'water valve',
           'snowmobiles': 'snowmobile', 'wineglass': 'wine glass'}


def build():
    source, fine = PL.load_59(), PL.load_459()
    added = [n for n in fine if n not in set(source) and n != 'unknown']
    rows = [dict(role=role, name=n, prompt=WORDING.get(n, n), fine_id=fine.index(n))
            for role, names in [('source', source), ('added', added)] for n in names]
    assert len(rows) == 458 and len({r['prompt'] for r in rows}) == 458, 'wording must not merge labels'
    assert set(WORDING) <= set(fine)
    return dict(policy='pascal-natural-v1', rows=rows)


def load_manifest():
    return json.loads(PATH.read_text())


if __name__ == '__main__':
    PATH.write_text(json.dumps(build(), indent=1))
    print(PATH, len(build()['rows']))
