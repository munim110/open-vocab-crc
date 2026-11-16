# Protocol: the added-label guarantee on the reserved images

Status: **frozen 2026-09-24 (code and hashes below), not yet run.** Running it requires the user's explicit approval. It is the second read of
the reserve (`meta/ade_confirmation_reserve_v1.json`, 2,000 ADE20K *training* images). The first read,
`results/confirmation_ade_vitl_bank683`, confirmed the source-label results. Everything below is fixed before any
added-label annotation of a reserved image is decoded. After the run, nothing in this document or in the code it names
changes.

## What is tested

Proposition 3 (`prop:labels`) says the following for candidate-independent scores whose source labels are exchangeable
with the added labels. Label-level CRC at the source vocabulary bounds the expected risk of an added label by α.

Proposition 4 (`prop:shift`) covers the case where the labels are not exchangeable. The excess is then Δ(t̂): the added
labels' mean loss minus the source labels' mean loss, both taken at the calibrated threshold.

On development data (ADE20K val, Pascal Context val; `results/label_exchange_*_vitl_bank683*`) both hold. This run
checks them once on images that played no part in any choice.

## Fixed inputs

- **Model:** CAT-Seg ViT-L, released weights, with the anchored conversion and the 683-name bank
  (`meta/bank_coco_oi683_v1.json`).
- **Scores:** the stores already written by the first read, in `cache/confirmation_vitl_bank683/{native150,native845,anchored845}.npy`
  on the GH200. The 4,096 sampled pixels per image were drawn with seed = reserve seed + image index. **No new model pass.**
- **Vocabulary:** `meta/natural_vocab_v1.json`, with 150 source names followed by 695 added names, 845 in total.
- **Added-label annotation:** ADE20K full (2021_17_01), training split, from the Hugging Face mirror `1aurent/ADE20K`
  (`data/train-0000{0..9}-of-00010.parquet`, pinned by SHA-256 at download).
  - It is decoded exactly as `src/build_gt.py` decodes the validation split: the class index is R/10·256 + G, mapped to
    A-847 train ids, then resized by nearest neighbour to the A-150 grid when the sizes differ.
  - It is then read at the stored sampled pixels.
  - It is mapped to the 845 names through the same manifest lookup as `exp_label_exchange.gt_all`. Fine labels outside
    the manifest are dropped from the added-label losses.
- **Analysis code:** `src/exp_label_exchange.py`, run as it produced the development numbers, with a new dataset key
  `ade_reserve` that changes only where the stores and the ground truth are read from. Settings:
  - seed 20260926;
  - 500 trials, each a random half/half image split;
  - grid `LOGIT_GRID`;
  - α ∈ {.10, .05};
  - weighting scheme `all3` only.
- **Designs:**
  - *exchangeable:* the source vocabulary is a fresh uniformly random 150 of the 845 names in each trial;
  - *dataset split:* the source vocabulary is the benchmark's 150 source names.

The design "exchangeable, native frozen" is **not** run. It needs native passes at random source vocabularies, which
means reading the reserved images through the model again, and the reserve rule is one model pass per configuration.

## Integrity checks (run first; any failure stops the run before any risk is computed)

1. **C1, filenames (can run before approval):** all 2,000 reserve filenames are present in the mirror's `filename`
   column. Only that column is read.
2. **C2, sampling:** re-sampling the A-150 annotation at the regenerated pixel indices reproduces the stored
   `gt150.npy` exactly.
3. **C3, alignment:** on sampled pixels labelled in both annotations, the A-150 label mapped into A-847 agrees with
   the decoded A-847 label at a rate of at least 0.98. On validation the rate is 0.995 (`meta/gt847_stats.json`).
4. **C4, coverage (reported, no threshold):** the share of sampled pixels with an added-label annotation, and the
   number of added labels present per calibration half.

The ground-truth builder is first run on the validation images, where it must reproduce the development ground truth
at the development pixels. That smoke test touches no reserved image.

## Primary outcome (a pass/fail claim, reported whichever way it goes)

- **P1:** in the *exchangeable* design, the anchored label-level arm's mean over 500 trials of the added-label risk on
  the calibration images is ≤ α, at both α = .10 and α = .05.
- On development data the values were 9.50 and 4.48 on ADE20K, and 7.55 and 2.76 on Pascal Context.
- This is the quantity Proposition 3 bounds: an expectation over the label draw, conditional on the images, because
  the loss is measured on the calibration images.

## Secondary outcomes (reported with the prediction stated here; no pass/fail claim)

- **S1, held-out images:** the same arm on the held-out images. Prediction: within 1 point of P1.
- **S2, native recalibration at 845, label-level, exchangeable:** prediction ≤ α, with larger sets than the anchored
  arm. On development data the sizes were 34.2 against 27.6 at α = .10.
- **S3, image-level threshold on the added labels, exchangeable:** prediction above α at both levels.
- **S4, dataset split, anchored label-level:**
  - Prediction: added-label risk above α.
  - Prediction: the source labels' mean loss at t̂ is within 2 points of α or below.
  - Prediction: Δ(t̂) accounts for the excess.
  - Reported: the source mean at t̂, Δ(t̂) and max_t Δ(t).
- **S5, dataset split, native frozen at the source vocabulary, label-level:** prediction above the anchored arm (S4).
- **S6, dataset split, prevalence-weighted `all3`:** reported only. No guarantee is claimed for it in the paper, and
  nothing is chosen from it.

## Reporting rule

- The paper reports P1 and S4 on the reserve as they come out, in the sentence of Sec. 5.2 that names the reserve.
- If P1 fails at either level, the paper says so there and in the limitations. The development result stays, labelled
  as development.
- Nothing is re-run to change an outcome. A re-run is allowed only after a crash, and only with bit-identical code and
  inputs (same hashes).
- The run writes `results/label_exchange_ade_reserve_vitl_bank683/` containing `REPORT.md`, `results.json` and a
  `protocol.json` with the SHA-256 of:
  - this document;
  - `src/exp_label_exchange.py`;
  - the ground-truth builder;
  - the vocabulary manifest;
  - the reserve list;
  - the mirror shards.

## Code to write before the run (smoke-tested on validation images only)

- `src/build_gt_reserve.py`: fetches the shards, runs C1, decodes A-847 for the 2,000 reserve files at the stored
  pixels, runs C2 and C3, and writes `cache/confirmation_vitl_bank683/gt847.npy` and `gt_checks.json`. Its `--smoke`
  mode runs on the validation parquet.
- `src/exp_label_exchange.py`: the `ade_reserve` dataset entry.
- `src/reproduce.py`: registry entries with stage `reserve`.

Once the code is written, its hashes are recorded in the "Frozen hashes" section below. The run starts only after that
and after approval.

## Pre-run checks done (2026-09-24, validation images only, plus C1)

- **`build_gt_reserve.py --dev`:** on all 2,000 validation images, the A-847 labels rebuilt at the development pixels
  equal `cache/sclip/gt847.npy` exactly. Agreement between the two annotations: 0.9959.
- **`build_gt_reserve.py --smoke`:** on the first 40 validation images, sampled with the reserve seed, C1–C3 pass
  (agreement 0.9963).
- **End to end on the smoke images:** `exp_label_exchange.py --dataset ade_reserve --reserve-dir
  cache/confirmation_vitl_bank683_smoke` runs through both designs. With 40 images the numbers carry no information,
  and they are not used.
- **Guard:** without `--reserve-read` the script refuses to read the reserve.
- **C1 on the reserve:** all 2,000 filenames are present in the training shards
  (`results/reserve_filenames_check.json`). Only the filename column was read.

## Frozen hashes (SHA-256)

Code and metadata:

| File | SHA-256 |
|---|---|
| `src/build_gt_reserve.py` | `630229d4d2be7f1e6aa24e89e3c652773c68eaa8bf98496b33407c5cbb3debe7` |
| `src/build_gt.py` | `7a70e894b4d40ee2324dd9ab5d7fef2c47ff999f0b9dafee7dcb3311d9c7df6b` |
| `src/exp_label_exchange.py` | `b8b31e68eb3747ce67bf944dda1d8d50c01d731043df4e3377498cf52e5985e1` |
| `src/exp_headroom_sets.py` | `76f897675a2aa155fbda18e3a687676820f1684b398dbdcbdef373f05cff5cb8` |
| `src/exp_added_label_risk.py` | `b12a1deb30db4d3c7ce0dfbc3023630bc322ef8bfa095f33515bbd920be17c50` |
| `meta/natural_vocab_v1.json` | `7c0fae275a79055dc5ac71741aaa1318a5b137b263c340acdba1abc8fb43b313` |
| `meta/ade_confirmation_reserve_v1.json` | `5897961e562963d1425b27974707207eff8ce04cc36a6f94c004d9154dda31f4` |

Training shards (`data/ade_full_train/`, from `1aurent/ADE20K`):

| Shard | SHA-256 |
|---|---|
| `train-00000-of-00010.parquet` | `20ab4443522379f08a0f6ae27f35374d98b6f4854f92067882c79188e5307671` |
| `train-00001-of-00010.parquet` | `72110d0636d700e64a16f587deb7c900eab199a0a24ad3a17405644465c2f9c8` |
| `train-00002-of-00010.parquet` | `ef3dbd70ab4d6ae6ce3d24f74a012203b9fe5062d0f09aed6c650bb3ad304f73` |
| `train-00003-of-00010.parquet` | `a7bbfc479c48fe36bda67437949c5c3d478befaba94dccef5aa3eeb916666fe1` |
| `train-00004-of-00010.parquet` | `bba48e38693f910877e5a02e14eb1b949923bbcafc4103aade9a120179df0a85` |
| `train-00005-of-00010.parquet` | `2ad42ce28d8c1808c9d5ffe0a62e83a8d84f7d27101107b2b8b6ac70157b8c61` |
| `train-00006-of-00010.parquet` | `64a6634a9f45b9ba964679f192f68b2499909eb30074e48ad2d1563d442c26b5` |
| `train-00007-of-00010.parquet` | `2ae8306de3a08b3621b93f7080e93949a1b6fae7966d1f82aa717fb62074b454` |
| `train-00008-of-00010.parquet` | `e3028ae600df8b8a2a5367c0d8e930fe4d4cffe3348c77e0eaf5a40d96ad9fe2` |
| `train-00009-of-00010.parquet` | `fc4681c7c692fda8453fe7546514b126ef4938471f438fb4a90030e3d66c14e2` |

## The run (after approval)

    PYTHONPATH=src python src/build_gt_reserve.py --reserve-read
    PYTHONPATH=src python src/exp_label_exchange.py --dataset ade_reserve --tag vitl_bank683 --schemes all3 --reserve-read

Both run on CPU. The first command stops without writing `gt847.npy` if C1, C2
or C3 fails.
