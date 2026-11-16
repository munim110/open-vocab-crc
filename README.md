# Calibrate Once, Grow the Vocabulary

Code and results for *Calibrate Once, Grow the Vocabulary: Candidate-Independent Scores for Conformal Risk Control in Open-Vocabulary Segmentation*.

Md Tanveer Hossain Munim, Bijoy Ahmed Saiem, Muhammad Abdullah Adnan
Bangladesh University of Engineering and Technology

Paper: arXiv link to be added.

Open-vocabulary segmenters accept class names at inference time. A conformal risk control (CRC) threshold calibrated
for one vocabulary stops holding when names are added later, because each label's score in released models depends on
which other labels were requested. This repository contains a training-free conversion that scores each candidate
against a fixed reference bank of names, so a label's score does not change when names are added and one calibration
keeps its guarantee as the vocabulary grows. It covers CAT-Seg (ViT-B, ViT-L, DeCLIP EVA02-L), SED and FC-CLIP on
ADE20K, Pascal Context and COCO-Stuff, and three Grounding DINO detectors on COCO grown to LVIS.

## Contents

- `src/catseg_probe_model.py`: the anchored conversion of CAT-Seg. `CATSegProbe` computes the bank context once per
  image (`context`) and scores any list of candidate names against it (`anchored`); `native` is the released forward
  pass. `tests/check_catseg_anchor.py` shows the calls and checks that the anchored scores do not depend on the other
  candidates and agree with the released model on the bank vocabulary.
- `src/declip_probe_model.py`: the same interface for CAT-Seg with the DeCLIP EVA02-L backbone.
- `src/sed_probe_model.py`: SED inference without detectron2, with the same anchored forward
  (`tests/check_sed_anchor.py`).
- `src/exp_fcclip_probe.py`: the conversion for FC-CLIP. `src/exp_ovd_probe.py`: the conversion for Grounding DINO.
- `src/conformal.py`: CRC thresholds and prediction sets.
- `src/exp_*.py`: the experiments. `src/paper_numbers.py` turns `results/` into every number and table of the paper.
- `meta/`: reference banks (`bank_coco_oi683_v1.json`, 171 COCO-Stuff names and 512 Open Images names, is the default),
  the grown vocabularies of each benchmark, the Open Images distractor list and the confirmation-reserve manifest.
- `results/`: one directory per registered result, with `results.json`, `REPORT.md` and, for probe runs,
  `protocol.json` (image ids, settings).
- `paper/`: the generated macros (`numbers.tex`), tables (`tables/`) and figures (`fig/`) of the paper. The LaTeX
  source of the paper is on arXiv.
- `docs/`: protocols for the COCO-Stuff/LVIS benchmark, detection, free-form names and the second read of the
  confirmation reserve.

## Reproducing the paper

`src/reproduce.py` registers 347 result directories, each with the command that wrote it, the Python
environment it runs in and the inputs it needs:

```bash
python src/reproduce.py list                  # level, environment, and whether the inputs are present
python src/reproduce.py show results/headroom_splits_ade_vitl_bank683
```

There are four levels. Each produces the inputs of the one above it:

| Level | Starts from | Produces | Needs | Entries |
|---|---|---|---|---|
| **paper** | `results/` (included) | `numbers.tex`, 55 tables, 4 figures | Python only | |
| **cpu** | stored per-pixel (per-box) scores + datasets | the analyses in `results/` | CPU; a GPU speeds it up | 220 |
| **gpu** | datasets + released checkpoints | stored scores, full-resolution mIoU, timings, bank sweeps, controls | one CUDA GPU, at most 12 GB | 123 |
| **train** | COCO-Stuff | the two fine-tuned aggregators of the supplement | about 64 GB of GPU memory | 2 |

### Level paper

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/reproduce.py paper
# all 60 generated files (numbers.tex, 55 tables, 4 figures) are identical to paper/
```

This regenerates the macros, tables and figures from `results/` and compares them byte for byte with `paper/`.
Figures are written without timestamps, so a correct regeneration is identical. If a file differs, the command names it
and restores the committed version; `--write` keeps the regenerated files instead.

### Level cpu

The analyses read stored float16 scores at 4,096 sampled pixels per image (`cache/headroom_probe*`): the native score at
the source vocabulary, the native score at the grown vocabulary and the anchored score. They are too large to host
(15 to 45 GB per configuration) and are regenerated at the gpu level. Detection stores box-level scores instead
(`cache/ovd_probe_<model>/`, about 200 MB per detector).

1. Datasets: `scripts/fetch_ade.sh` (ADE20K A-150 and A-847, checksum-pinned), `scripts/fetch_pascal.sh` (Pascal
   Context) and `scripts/fetch_coco_val.sh` (COCO-Stuff val2017, the LVIS v1 val annotations, checksum-pinned, and the
   COCO val2017 boxes for detection). None needs a login. `python src/build_gt.py` decodes the A-847 masks.
   `scripts/check_data.sh` lists what is missing.
2. Ground truth at the sampled pixels (the sample depends only on the image size and a seed):
   ```bash
   PYTHONPATH=src python src/build_pixel_sample.py --dataset ade      # also: pascal, coco
   ```
3. Run or verify an analysis. `verify` re-runs it, compares the new `results.json` with the committed one and restores
   the committed directory:
   ```bash
   python src/reproduce.py list --level cpu
   python src/reproduce.py verify results/headroom_splits_pascal results/added_label_risk_pascal
   ```

All analyses use the same 500 random half/half calibration/test splits (seed 20261003). No analysis fits anything, and none reads
the confirmation reserve.

### Level gpu

```bash
scripts/setup_models.sh
```

clones CAT-Seg, SED, FC-CLIP and detectron2 at the commits that produced our scores into `../third_party_probe/`,
downloads the released checkpoints with their sha256 checks, and builds the model environments:

- `.venv-probe` for CAT-Seg and SED (`env/requirements-probe.txt`);
- `.venv-fcclip` for FC-CLIP (`env/requirements-fcclip.txt`; detectron2 and the deformable-attention kernel are
  compiled). Without a CUDA toolkit, `scripts/setup_fcclip_nokernel.sh` builds the same environment
  (`env/requirements-fcclip-local.txt`) with detectron2 imported from its checkout and FC-CLIP's deformable attention on
  the PyTorch reference path shipped in its checkout (its edits to the checkouts are marked `# local patch`);
- `.venv-ovd` for the detectors (`env/requirements-ovd.txt`, Hugging Face `transformers==5.17.0`). transformers 5.17
  loads the per-layer decoder heads of MM-Grounding DINO and Grounding DINO B incorrectly; `restore_heads` in
  `src/exp_ovd_probe.py` copies them from the checkpoint (`docs/OVD_DETECTION_BENCHMARK.md`).

Otherwise the only change to any checkout is a one-line fix to FC-CLIP's CUDA kernel for torch 2.x (`value.type()` becomes
`value.scalar_type()`). Then run a registered configuration, for example

```bash
python src/reproduce.py run results/headroom_probe_ade_vitl_bank683 results/headroom_probe_ade_vitl_bank683_rest
```

Each probe run writes its stored scores to `cache/` and a record to `results/headroom_probe_*`, and checks exactness
itself: candidate independence and agreement with the released forward pass on the bank vocabulary for CAT-Seg and SED,
unchanged native logits and masks for FC-CLIP (`--check`), and order and subset invariance for the detectors
(`src/exp_ovd_probe.py --model <m> --check`).

Our scores were produced on an NVIDIA GH200 (Linux, aarch64, CUDA 12.8) and, for some configurations, on an RTX 5070 Ti
(Windows); on 20 images the two machines gave identical probe metrics. On other GPUs float16 scores can differ in the
last bit.

### Level train

The fine-tuned aggregators of the supplement (`runs/anchored_vitb`, `runs/anchored_vitb_distract_near`) are not
included; `src/train_anchored_catseg.py` trains each in 10,000 iterations on COCO-Stuff
(`python src/reproduce.py show runs/anchored_vitb`). The main method uses no training.

## Confirmation reserve

`meta/ade_confirmation_reserve_v1.json` lists 2,000 ADE20K training images that were not used during development. They
were scored once, with CAT-Seg ViT-L and the 683-name bank (`results/confirmation_ade_vitl_bank683`, Tab. S41),
and the stored scores were analysed a second time for the added-label guarantee under a protocol fixed in advance
(`docs/PROTOCOL_ADDED_LABEL_RESERVE.md`). The registry lists both runs but refuses to execute them. All ADE20K, Pascal
Context and COCO validation images are development data.

## Tables and figures

Numbering follows the arXiv version (S: supplementary material). `NOT_INCLUDED.txt` lists files left out for size.

| Paper | File |
|---|---|
| Fig. 1 | `paper/fig/fig1_risk_after_growth.pdf` |
| Fig. 2 | `paper/fig/fig_problem.pdf` |
| Fig. 3 | (drawn in LaTeX; source on arXiv) |
| Fig. 4 | `paper/fig/fig2_anchored_after_growth.pdf` |
| Tab. 1 | `paper/tables/adaptive_main.tex` |
| Tab. 2 | `paper/tables/labelexch.tex` |
| Tab. S1 | `paper/tables/labelexch_images.tex` |
| Tab. S2 | `paper/tables/nativerefs.tex` |
| Tab. S3 | (typed in the LaTeX source; no numbers) |
| Tab. S4 | `paper/tables/overview.tex` |
| Tab. S5 | `paper/tables/overview_b.tex` |
| Tab. S6 | `paper/tables/ade_main.tex` |
| Tab. S7 | `paper/tables/pascal_main.tex` |
| Tab. S8 | `paper/tables/coco_main.tex` |
| Tab. S9 | `paper/tables/curve.tex` |
| Fig. S1 | `paper/fig/fig3_set_size_vs_additions.pdf` |
| Fig. S2 | `paper/fig/fig_qualitative.pdf` |
| Fig. S3 | `paper/fig/fig_qualitative_panel.pdf` |
| Tab. S10 | `paper/tables/setsize.tex` |
| Tab. S11 | `paper/tables/setsize_b.tex` |
| Tab. S12 | `paper/tables/setsize_label.tex` |
| Tab. S13 | `paper/tables/adaptive.tex` |
| Tab. S14 | `paper/tables/adaptive_sed.tex` |
| Tab. S15 | `paper/tables/adaptive_fcclip.tex` |
| Tab. S16 | `paper/tables/adaptive_pascal.tex` |
| Tab. S17 | `paper/tables/freeform.tex` |
| Tab. S18 | `paper/tables/labelexch_models.tex` |
| Tab. S19 | `paper/tables/labelexch_heldout.tex` |
| Tab. S20 | `paper/tables/hardness.tex` |
| Tab. S21 | `paper/tables/labelsample_a.tex`, `paper/tables/labelsample_b.tex` |
| Tab. S22 | `paper/tables/labelexch_weights.tex` |
| Tab. S23 | `paper/tables/labelexch_weights_coco.tex` |
| Tab. S24 | `paper/tables/added.tex` |
| Tab. S25 | `paper/tables/added_pascal.tex` |
| Tab. S26 | `paper/tables/added_coco.tex` |
| Fig. S4 | `paper/fig/fig4_added_label_risk.pdf` |
| Tab. S27 | `paper/tables/bank.tex` |
| Tab. S28 | `paper/tables/fcclip_banks.tex` |
| Tab. S29 | `paper/tables/bank_seeds.tex` |
| Tab. S30 | `paper/tables/miou.tex` |
| Tab. S31 | `paper/tables/miou_pixacc.tex` |
| Tab. S32 | `paper/tables/pixacc_added.tex` |
| Tab. S33 | `paper/tables/runtime.tex` |
| Tab. S34 | `paper/tables/runtime_lean.tex` |
| Tab. S35 | `paper/tables/memory.tex` |
| Tab. S36 | (typed in the LaTeX source; no numbers) |
| Tab. S37 | `paper/tables/finetune.tex` |
| Tab. S38 | `paper/tables/ovd.tex` |
| Tab. S39 | `paper/tables/ovd_full.tex` |
| Tab. S40 | `paper/tables/ovd_acc.tex` |
| Tab. S41 | `paper/tables/confirm.tex` |
| Tab. S42 | `paper/tables/strata.tex` |
| Tab. S43 | `paper/tables/strata_pascal.tex` |
| Tab. S44 | `paper/tables/strata_coco.tex` |
| Tab. S45 | `paper/tables/pername.tex` |
| Tab. S46 | `paper/tables/calsize.tex` |
| Tab. S47 | `paper/tables/losses_a.tex` |
| Tab. S48 | `paper/tables/losses_b.tex` |
| Tab. S49 | `paper/tables/constructions_a.tex` |
| Tab. S50 | `paper/tables/constructions_b.tex` |

`bank_main.tex`, `constructions.tex`, `labelsample.tex`, `losses.tex` are one-table layouts of tables the paper prints in two parts (or not at all); they are generated and checked with the others.

## Citation

```bibtex
@misc{munim2026calibrate,
  title         = {Calibrate Once, Grow the Vocabulary: Candidate-Independent Scores for Conformal Risk Control in Open-Vocabulary Segmentation},
  author        = {Md Tanveer Hossain Munim and Bijoy Ahmed Saiem and Muhammad Abdullah Adnan},
  year          = {2026},
  eprint        = {XXXX.XXXXX},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV}
}
```

## License

The code is under the MIT license (`LICENSE`). Vendored components and dataset terms are listed in `THIRD_PARTY.md`.
