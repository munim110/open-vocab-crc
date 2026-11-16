# Findings from the headroom probe (2026-09-21)

400 development tuning images (tune_cal + tune_eval of the match-correction split), ADE natural wording, the cached 4,096 sampled pixels per image. Nothing was fitted. Three arms: frozen SCLIP (cached features), released CAT-Seg ViT-B run natively, and the same released weights run with **reference-anchored class aggregation**.

## What the anchored arm is

CAT-Seg is already trained with a per-label sigmoid (BCE) loss. It is candidate-dependent only through (a) class-aggregation attention across the deployed vocabulary and (b) per-crop top-256 truncation above 256 labels. The anchored forward aggregates a fixed reference bank (the 171 COCO-Stuff training names) exactly as the released model would, records each layer's linear-attention key/value sums, and lets every candidate attend to that context plus itself only. Truncation is dropped. A candidate's score is a function of (image, candidate text, reference bank). No weights change.

`tests/check_catseg_anchor.py`: the re-implementation matches the released forward to 1.4e-5 (including the truncation path); anchored scores are unchanged by co-candidates, order and chunking up to 1.4e-5 float drift; native logits move by >1.0 under a 50-label addition.

## Ranking

| | source rank | rank at +695 | +695 top-10 | small-class +695 top-10 | sampled mIoU |
|---|---:|---:|---:|---:|---:|
| SCLIP | 9.63 | 37.25 | 58.44% | 31.99% | 15.62 |
| CAT-Seg native | 2.25 | 5.46 | 92.60% | 72.30% | 31.23 |
| CAT-Seg anchored | 2.40 | 5.70 | 90.80% | 71.78% | 29.74 |

The ranking bottleneck identified in `natural_ranks_sclip_ade` is a property of the frozen representation, not of the problem. Anchoring costs about 1.5 mIoU and 2 points of top-10 inclusion relative to native.

## Calibrated sets (200 cal / 200 eval, image-level CRC)

At alpha = 0.10: SCLIP fixed-source 28.21 labels at source and 111.87 at +695; anchored CAT-Seg **3.36 and 7.94**, threshold calibrated once. Native CAT-Seg with its source threshold frozen goes from 10.51% to **16.85%** risk at +695, so the failure this project studies is present in a trained state-of-the-art model. Native with replay recalibration needs 5.58 labels at +695; the measured price of projectivity here is 7.94 - 5.58 = 2.4 labels, against a 19-label price for cosine vs softmax on SCLIP. At alpha = 0.05 the anchored sets are 5.54 -> 15.85.

Anchored sets are under the plan's absolute ceiling (25% of |V0| = 37.5) at every addition count, by a wide margin.

## Limits

- One split, 200 calibration images, previously inspected development images, one dataset, one backbone size. Observed risks differ slightly across arms (8.68% vs 9.21%); this is not an exactly equal-risk comparison. Reserve untouched.
- CAT-Seg was trained on COCO-Stuff. ADE images are unseen but many ADE concepts are not; 'name_not_in_coco' rows are exact-string only and understate semantic overlap. The earlier SCLIP heads failed on label transfer; here held-out and not-in-COCO groups degrade but remain far above SCLIP.
- Invariance is up to 1e-5 logit drift from batch layout, not bit-exact. A deployment contract needs a fixed candidate batch layout or a near-threshold flip report.
- Cost: 2.7 s/image for reference + 845 candidates on an RTX 5070 Ti, versus 1.2 s for native 150 + 845. Anchored cost is linear in candidates and chunkable; native is capped by truncation.
- The reference bank was not selected or tuned; COCO-171 is simply the training vocabulary. Bank sensitivity is untested.
- The released model was trained with full class attention; anchoring is off-distribution for it. Training with anchored attention is the obvious next step and may close the remaining gap to native.
