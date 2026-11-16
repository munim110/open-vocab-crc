# Ranking headroom probe

1600 development images (roles fit,calibration,evaluation), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 15.64 | 15.64 | 16.92% | 64.60% | 16.92% | 64.60% | 91.75% |
| sclip_cached | boundary | 20.97 | 20.97 | 15.36% | 54.02% | 15.36% | 54.02% | 87.25% |
| sclip_cached | interior | 14.88 | 14.88 | 17.18% | 66.10% | 17.18% | 66.10% | 92.38% |
| sclip_cached | small_class | 59.66 | 59.66 | 1.56% | 11.89% | 1.56% | 11.89% | 53.70% |
| sclip_cached | held_out | 30.00 | 30.00 | 0.00% | 33.65% | 0.00% | 33.65% | 79.51% |
| sclip_cached | seen | 16.29 | 16.29 | 18.90% | 65.97% | 18.90% | 65.97% | 90.48% |
| sclip_cached | name_in_coco | 22.53 | 22.53 | 0.00% | 37.03% | 0.00% | 37.03% | 88.16% |
| sclip_cached | name_not_in_coco | 14.29 | 14.29 | 22.57% | 72.88% | 22.57% | 72.88% | 91.34% |
| catseg_native | all | 2.48 | 6.47 | 69.66% | 96.43% | 64.25% | 91.89% | 97.87% |
| catseg_native | boundary | 3.52 | 9.22 | 49.12% | 94.07% | 45.10% | 86.89% | 96.68% |
| catseg_native | interior | 2.34 | 6.12 | 72.52% | 96.76% | 66.93% | 92.58% | 98.01% |
| catseg_native | small_class | 7.94 | 29.06 | 28.88% | 81.14% | 23.46% | 65.98% | 86.21% |
| catseg_native | held_out | 4.31 | 16.07 | 55.01% | 90.90% | 44.46% | 84.06% | 94.01% |
| catseg_native | seen | 2.11 | 4.37 | 72.99% | 97.43% | 68.04% | 93.33% | 98.55% |
| catseg_native | name_in_coco | 2.05 | 3.93 | 75.52% | 97.36% | 70.62% | 93.99% | 98.70% |
| catseg_native | name_not_in_coco | 2.82 | 7.96 | 64.57% | 95.37% | 59.34% | 90.01% | 97.21% |
| catseg_anchored | all | 2.51 | 6.13 | 69.29% | 96.31% | 63.90% | 91.19% | 97.74% |
| catseg_anchored | boundary | 3.60 | 9.34 | 48.27% | 93.77% | 43.88% | 85.32% | 96.31% |
| catseg_anchored | interior | 2.36 | 5.72 | 72.21% | 96.67% | 66.70% | 92.03% | 97.92% |
| catseg_anchored | small_class | 7.90 | 26.11 | 28.78% | 81.06% | 24.17% | 66.00% | 86.19% |
| catseg_anchored | held_out | 4.34 | 12.99 | 55.02% | 90.80% | 44.79% | 84.00% | 94.03% |
| catseg_anchored | seen | 2.14 | 4.66 | 72.43% | 97.29% | 67.41% | 92.52% | 98.38% |
| catseg_anchored | name_in_coco | 2.04 | 4.01 | 75.89% | 97.38% | 71.66% | 93.67% | 98.72% |
| catseg_anchored | name_not_in_coco | 2.88 | 7.43 | 63.75% | 95.20% | 58.31% | 89.17% | 97.06% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.11 | 16.68% |
| catseg_native | 30.17 | 69.83% |
| catseg_anchored | 29.52 | 69.47% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.07, native_150_plus_845 0.96, anchored_reference_plus_845 1.95; peak memory 8.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.