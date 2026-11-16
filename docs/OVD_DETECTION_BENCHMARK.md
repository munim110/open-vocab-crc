# Second task: open-vocabulary detection, COCO 80 grown with LVIS v1

Fixed 2026-09-25, before any detector score on these images was computed. Development data (COCO val2017); the
confirmation reserve is not involved. The analyses are the image-level and label-level CRC of the segmentation
experiments, with a box-level loss in place of the pixel-level one. Nothing below is changed after scores exist; a
deviation is recorded in a dated section at the end, with its reason.

## Why this task

Candidate dependence is not specific to segmentation. In Grounding DINO each class phrase is masked so that its text
tokens attend only to themselves in the text encoder, but the names still interact through the image side:

- the image features attend to every text token (feature-enhancer fusion, softmax over the text tokens);
- the 900 queries are the encoder tokens with the highest similarity to any text token (language-guided query
  selection, a pruning step);
- the decoder queries attend to every text token (softmax);
- the text is capped at 256 tokens, so a vocabulary of LVIS size must be split into chunks, and which chunk a name
  falls in changes its score.

A threshold calibrated at the source vocabulary is therefore expected not to transfer, as for the segmenters.

## Models (Hugging Face transformers 5.17.0, released weights, no training)

- Grounding DINO Swin-T (`IDEA-Research/grounding-dino-tiny`) and Swin-B (`IDEA-Research/grounding-dino-base`).
- MM-Grounding-DINO Swin-T (`openmmlab-community/mm_grounding_dino_tiny_o365v1_goldg_v3det`), a later training of the
  same architecture.
- Control, candidate-independent by construction: OWLv2 B/16 (`google/owlv2-base-patch16-ensemble`); its query
  embeddings do not see the text and each class is scored by its own sigmoid.

Inference: the processor defaults of each model (shortest side 800, longest 1333 for Grounding DINO), fp32, TF32 off.

## Data

- **Images:** the 2,000 COCO val2017 images of the COCO-Stuff benchmark (`docs/COCO_LVIS_BENCHMARK.md`: the val2017
  images annotated by LVIS v1 val, sorted by file name, the first 2,000).
- **Source annotation:** COCO instances val2017 (`data/coco/annotations/instances_val2017.json`), boxes of the 80
  thing classes, `iscrowd = 0` only.
- **Added annotation:** LVIS v1 val boxes (`data/lvis/lvis_v1_val.json`, the file of the segmentation benchmark). LVIS
  is federated: a category takes part in an image only if the image carries at least one of its boxes, as in the
  segmentation label-level analysis ("only labels annotated in them take part").

## Vocabulary

- **Source:** the 80 COCO class names in COCO category order, as in the standard Grounding DINO COCO prompt
  ("person . bicycle . car . ...").
- **Added:** every LVIS v1 category that is not a COCO concept: the synset rule of the segmentation benchmark
  (`coco_to_synset.json`, 79 categories) plus an exact-name rule for the remaining COCO names. Prompt of an added
  label: the rule of `docs/COCO_LVIS_BENCHMARK.md` (first unqualified synonym not used by another label, else the
  qualified name).
- **Order of the added labels:** the seeded permutation of `meta/coco_lvis_natural_vocab_v1.json` restricted to these
  categories.
- **Two growth regimes:**
  1. *One prompt:* the source names followed by the first added names that fit in 256 tokens (the deployer extends
     the prompt).
  2. *LVIS scale:* all names, split into consecutive chunks of 40 names in the order source-then-added, the chunk
     size of the standard LVIS evaluation of GLIP and Grounding DINO. A box is scored for a label by the chunk that
     holds the label.

## Scores and loss

- **Detection score** of a query for a label: the maximum over the label's phrase tokens of the token logit (its
  sigmoid is the model's score). Stored as a logit clamped to [-30, 30] in float16, as the segmentation scores are.
- **Box-level score** of a ground-truth box g for a label c: the maximum of that score over the predicted boxes with
  IoU(d, g) >= 0.5; -30 (the lowest grid point) if no predicted box overlaps.
- **Prediction set** at threshold t: the labels whose box-level score is at least t. The lowest grid point includes
  every label, as in the segmentation experiments.
- **Loss** of an image (image-level CRC, Sec. 3.1): the fraction of its source-class ground-truth boxes whose true
  label is missing from the set. Images without a source box are excluded, as images without a source pixel are.
- **Label loss** (label-level CRC, Prop. 3): the fraction of a label's ground-truth boxes in the calibration images
  that are missed. The image-averaged variant (mean over the images containing the label of the per-image fraction)
  is reported alongside it, since it is the quantity of the new-image result.
- **Set size:** the mean number of labels in the set of a source ground-truth box.

## Conversion (anchored Grounding DINO)

The image side attends to a fixed reference bank only; each candidate is scored against the bank-conditioned
queries.

- One prompt holds the bank (at most 256 tokens). The image features, the query selection and the decoder see only
  the bank tokens.
- Each candidate phrase is passed through the text branch on its own (its tokens attend to themselves and to the
  bank-conditioned image features of each layer) and scored against the final queries by the model's contrastive
  head.
- A candidate's score is then a function of the image, the candidate and the bank. **Exactness test before any
  analysis:** on 20 images, the anchored score of every label is identical (maximum absolute logit difference below
  1e-4) when the candidates are split into different chunks or orders, and the anchored score of a bank name equals
  the native score of that name with the bank as the whole prompt.
- **Banks:** (A) the 80 COCO names, the standard prompt the model was tuned on (bank = source vocabulary); (B) the 80
  Objects365 names most frequent in Objects365 train that are not COCO concepts. Bank A is the main configuration and
  B the ablation; both are reported.

## Analyses (unchanged settings of the segmentation experiments)

- 500 random half/half calibration splits, alpha = 0.10 and 0.05.
- Arms: native reused (threshold calibrated at the source vocabulary, deployed at the grown one), native recalibrated
  at the grown vocabulary, anchored calibrated once at the source vocabulary; OWLv2 reused.
- Reported: risk after growth, fraction of splits above alpha, set size at the source and grown vocabulary, and
  added-label risk with the label-level threshold on random source vocabularies (calibration images and held-out
  images).
- Runtime per image for native and anchored at the grown vocabulary.

## Deviations

- 2026-09-25, before any score (clarification). The segmentation manifest's added labels exclude 12 LVIS categories
  that match COCO-*Stuff* names (banner, blanket, ...); they are not COCO-80 concepts, so here they are added labels.
  The added order is therefore a fresh seeded permutation (seed 20260925) of the added categories in LVIS id order,
  and prompts follow the rule above with the 80 COCO names as taken strings (`src/ovd_vocab.py`,
  `meta/ovd_coco_lvis_vocab_v1.json`).
- 2026-09-25, before any score (clarification). Bank B is taken from the Open Images part of the segmentation bank
  (`meta/bank_coco_oi683_v1.json`, entries 172 onwards, in bank order): the first 80 names that are neither a COCO name
  nor the prompt or a synonym of an LVIS category. Objects365 frequencies are not available offline.
- 2026-09-25, before any score (implementation). The anchored pass puts the bank and every candidate in one text
  sequence and marks the candidate tokens as padding for the image side (fusion, query selection and decoder); the
  256-token cap is lifted for this pass only, which changes nothing because every phrase attends only to itself and
  position ids restart at each phrase. Candidate logits come from the model's own contrastive head without the
  padding mask.
- 2026-09-25, exactness test (before any analysis). With queries taken from the joint pass, float rounding that
  depends on the sequence length (about 1e-6) flipped near-tied queries at the top-900 selection and moved box-level
  scores by up to 4.5e-3 (image 139). The queries and boxes are therefore taken from the native pass with the bank as
  the whole prompt, which the joint pass equals in exact arithmetic, and only the candidates' text features from the
  joint pass. Test on 5 images, Grounding DINO Swin-T: order invariance <= 3.9e-7, subset invariance <= 2.4e-7,
  anchored bank-A scores of the source names vs native with the source prompt <= 3.3e-7 (probabilities); the native
  source scores move by 0.026-0.118 when the prompt is extended to 256 tokens (`results/ovd_probe_gdino_t/check.json`).
- 2026-09-25, during the Grounding DINO Swin-T probe (runtime only). From 08:12 UTC for about 20 minutes (around
  images 500-800), an unrelated FC-CLIP run shared the GPU. Scores are unaffected, but the probe's seconds per image
  are not a clean timing. The runtime reported for detection is therefore measured in a separate timing run on a
  subset of images, with the GPU otherwise idle.
- 2026-09-25, after the Grounding DINO Swin-T analysis (post hoc diagnostic, no change to any reported analysis).
  - The label-level results with a random source vocabulary had a low mean added-label risk but many trials above alpha. `src/exp_ovd_floor.py` measures why, using the same draws.
  - A ground-truth box that no predicted box overlaps (IoU >= 0.5) scores -30 for every label, so only the lowest grid point, which includes every label, covers it.
  - With bank A, 2.5% of source boxes and 23.6% of added boxes are unlocalised; native at LVIS scale leaves 17.0% of added boxes unlocalised.
  - In 57% of the trials (image-averaged loss, alpha = .10; 71% with the pooled loss) the unlocalised boxes of the drawn labels alone exceed alpha, and the label-level threshold is trivial. At alpha = .05 it is trivial in almost every trial.
  - Both the diagnostic and this limitation are reported with the label-level results.
- 2026-09-25, after the MM-Grounding DINO Swin-T analysis (loading bug, rerun; no change to the protocol or the analyses).
  - Every MM-Grounding DINO T arm, native included, came out at the trivial threshold (all 1,204 labels), and 80% of source boxes had no predicted box at IoU >= 0.5 (Grounding DINO T: 2.5%).
  - Cause: transformers 5.17 does not load this checkpoint's decoder heads. Its per-layer box and class heads (`decoder_bbox_embed_share=False`) come out as layer 0's in layers 1-5; the model's own `post_process_grounded_object_detection` returns the same broken boxes. On 50 images (source classes, score >= .35, class-matched IoU >= .5) precision/recall is .06/.03 as loaded and .70/.70 with the checkpoint's heads (Grounding DINO T: .64/.70).
  - Grounding DINO B (shared head) also loads a box head that differs from the checkpoint's, with the same detection quality (.72/.72 either way). Grounding DINO T loads the checkpoint exactly.
  - Fix: `restore_heads` in `src/exp_ovd_probe.py` copies the decoder heads from the checkpoint file after loading (a shared head into every layer). With it, the stored Grounding DINO T scores are reproduced exactly (max abs difference 0 on the first 20 images, native and anchored), so Grounding DINO T is not rerun.
  - MM-Grounding DINO T (complete, analysed) and Grounding DINO B (stopped after 34 minutes) are rerun from the start with the fix. The tied-head outputs are kept on the GH200 as `*_tiedheads` and are not reported. OWLv2 is unaffected.
- 2026-09-26, clean timing run (runtime only; no score or analysis changes).
  - The probe timings are not clean: an unrelated job shared the GPU during the Grounding DINO T probe, and the head-fix queue ran next to the OWLv2 probe.
  - The timing runs time the four detectors one after another on the otherwise idle GH200, on the first 100 benchmark images, each arm separately (`src/exp_ovd_probe.py --limit 100 --tag _timing`, output `results/ovd_probe_<model>_timing`).
  - `--tag` only renames the output directories. The detection runtime reported in the paper comes from these runs.
- 2026-11-09, accuracy analysis (post hoc addition; no score or earlier analysis changes).
  - `src/exp_ovd_accuracy.py` reports box-level top-1/top-5 accuracy over all 1,204 names from the stored scores, for source and added boxes, the counterpart of the segmentation pixel accuracy. Unlocalised boxes and ties count as wrong.
  - Output `results/ovd_accuracy_<model>`, reported in the supplement (`tab:ovdacc`) and in one clause of `sec:detection`.
