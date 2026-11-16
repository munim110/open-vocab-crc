# Third benchmark: COCO-Stuff 171 grown with LVIS v1

Fixed 2026-09-25, before any model score on these images was computed. Development data: the analyses are the ones run
on ADE20K and Pascal Context, with the same settings; nothing is fitted or chosen from these results.

## Why this benchmark

ADE20K (150 -> 845) and Pascal Context (59 -> 458) grow a benchmark vocabulary that the models were not trained on.
Here the source vocabulary is the models' own training vocabulary (COCO-Stuff 171; FC-CLIP was trained on COCO
panoptic 133), and it grows by the LVIS long-tail vocabulary on the same images. Most deployed segmenters start from their training
vocabulary, so this is the most common way a vocabulary grows in practice. The images (COCO val2017) are not in the
training data of any of the five models.

## Data

- **Images:** the COCO val2017 images annotated by LVIS v1 val (4,809 of 5,000), sorted by file name; the first 2,000.
- **Source annotation:** COCO-Stuff 171, the detectron2 train-id maps in `data/coco-stuff/annotations_detectron2/val2017`
  (0-79 things, 80-170 stuff, 255 none).
- **Added annotation:** LVIS v1 val instance masks (`data/lvis/lvis_v1_val.json`, zip SHA-256
  `5cae9a3c79aadb667550c2b5dcf7f4d86e059a41ec91ef690225b667e28e9ba5`), decoded with pycocotools.
- **Pixels:** 4,096 per image, drawn with seed 1234 + image index (as on the other two benchmarks).
- **Label per sampled pixel** (`src/build_pixel_sample.py --dataset coco`):
  - The smallest LVIS instance covering the pixel decides.
  - If its category is an added label, and the COCO-Stuff label is a stuff class or none, the pixel takes the added
    label and has no source label. COCO-Stuff labels objects outside its 80 thing classes as the stuff around them.
  - COCO thing masks are never overridden. LVIS also annotates parts and worn items, such as wheels and shirts, and a
    pixel of a person's shirt stays "person".
  - LVIS categories that are source concepts change nothing.
- **Coverage** (recorded at build time, before any score):
  - 93.5% of sampled pixels carry a source label, and 3.1% an added label.
  - 489 of the added labels occur.
  - 1,300 images have an added-label pixel.
  - A further 4.1% of pixels lie under an added LVIS instance inside a COCO thing mask, and stay source.

## Vocabulary (`src/coco_lvis_vocab.py`, `meta/coco_lvis_natural_vocab_v1.json`)

- **Source:** the 171 names of CAT-Seg's released `datasets/coco.json`, verbatim. They are the training strings, in
  train-id order.
- **Added:** every LVIS v1 category that is not a source concept: 1,112 labels, for 1,283 in total.
  - A category counts as a source concept when its synset is the one the LVIS authors assign to a COCO thing class
    (`coco_to_synset.json`, 79 categories).
  - It also counts when one of its synonyms, without a parenthetical qualifier, equals a source name without the
    `-other` / `-stuff` / `-merged` suffix (12 categories: banner, blanket, cabinet, cupboard, curtain, desk, mirror,
    napkin, pillow, salad, table, towel).
- **Order of the added labels:** a seeded random permutation (seed 20260925). The nested additions +50, +150, +500 and
  +1,112 are prefixes of it.
- **Prompt of an added label:**
  - the first LVIS synonym without a parenthetical qualifier that no other label uses as its prompt or first synonym;
  - otherwise the name with its qualifier ("bat (animal)").
  - The rule is fixed and is not edited per name.

## Runs

Five configurations with the 683-name bank (`meta/bank_coco_oi683_v1.json`, a superset of the 171 source names):

- CAT-Seg ViT-B and ViT-L;
- SED;
- CAT-Seg+DeCLIP;
- FC-CLIP (133 training classes plus the bank, 701 entries).

The probes are `src/exp_headroom_probe_coco.py` and `src/exp_fcclip_probe.py --dataset coco`, each followed by:

- `exp_headroom_splits.py` (500 splits);
- `exp_conditional_risk.py`, `exp_alternative_losses.py`, `exp_set_constructions.py` and `exp_calibration_size.py`;
- the added-label risk. It runs through `src/coco_frozen_analyses.py`, because `exp_added_label_risk.py` is
  protocol-frozen and is run unchanged by a path-only substitution.

For CAT-Seg ViT-L, the label-level analyses of Sec. 5.2 are also run (`exp_label_exchange.py` through the same
wrapper):

- the exchangeable and dataset-split designs;
- the Δ decomposition (`--schemes all3 --suffix _delta`);
- the six prevalence schemes (`--suffix _schemes`).

The exchangeable native-frozen design is not run. It needs native passes at random source vocabularies, which were run
on ADE20K only.

## Reporting

Every number is reported as it comes out, in the same tables as the other two benchmarks. A result that goes against
the paper's claims is stated in the text and the limitations, as on the other benchmarks.
