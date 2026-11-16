# Audit controls on released CAT-Seg (ADE development images)

## Frozen source threshold under the full vocabulary: attention versus pruning

400 images, mean over 200 random 200/200 splits. The threshold is calibrated by CRC under the 150-label deployment and reused after 695 labels are added; "replayed" recalibrates under the full vocabulary.

| alpha | Deployment at +695 | Risk with frozen threshold (%) | Frozen size | Risk replayed (%) | Replayed size |
|---:|---|---:|---:|---:|---:|
| 0.1 | released (top-256 pruning) | 15.92 | 2.83 | 9.46 | 5.49 |
| 0.1 | pruning removed | 7.71 | 7.77 | 9.52 | 6.11 |
| 0.05 | released (top-256 pruning) | 8.12 | 6.66 | 4.49 | 13.00 |
| 0.05 | pruning removed | 3.65 | 17.95 | 4.48 | 14.10 |

## Native CAT-Seg on COCO-171 + {c}, one run per candidate, versus the shared frozen reference context

16 images, all 845 labels, valid sampled pixels; logit differences over entries where either logit exceeds -12.

- mean |logit difference| 0.015, 99th percentile 0.189
- true label has the same rank at +695 on 92.64% of pixels; mean rank 3.62 (separate runs) vs 3.65 (shared context); same top-1 label 97.22%
- aggregation and decoding time per image: 349.6 s (separate runs) vs 2.6 s (shared context), CLIP image features excluded from both

Development data, previously inspected; released ViT-B weights; stored float16 logits.