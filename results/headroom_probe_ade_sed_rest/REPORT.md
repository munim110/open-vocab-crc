# Ranking headroom probe

1600 development images (roles fit,calibration,evaluation), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 9.13 | 35.31 | 38.46% | 78.27% | 26.03% | 60.01% | 82.35% |
| sclip_cached | boundary | 15.23 | 62.18 | 22.12% | 62.80% | 13.11% | 41.97% | 68.86% |
| sclip_cached | interior | 8.35 | 31.91 | 40.52% | 80.27% | 27.65% | 62.27% | 84.07% |
| sclip_cached | small_class | 25.16 | 109.19 | 12.13% | 45.96% | 7.32% | 27.48% | 52.29% |
| sclip_cached | held_out | 16.14 | 66.48 | 22.39% | 62.22% | 12.50% | 41.08% | 67.03% |
| sclip_cached | seen | 9.44 | 36.45 | 41.43% | 77.93% | 29.70% | 61.72% | 82.09% |
| sclip_cached | name_in_coco | 8.62 | 33.80 | 43.30% | 81.00% | 30.92% | 65.99% | 84.78% |
| sclip_cached | name_not_in_coco | 11.23 | 44.01 | 31.72% | 72.78% | 21.46% | 52.61% | 77.68% |
| catseg_native | all | 2.48 | 6.50 | 72.24% | 96.15% | 66.31% | 92.19% | 97.07% |
| catseg_native | boundary | 3.35 | 9.32 | 53.24% | 94.58% | 47.53% | 87.79% | 95.88% |
| catseg_native | interior | 2.37 | 6.16 | 74.89% | 96.37% | 68.94% | 92.82% | 97.22% |
| catseg_native | small_class | 7.28 | 25.57 | 29.25% | 83.95% | 23.78% | 68.94% | 87.49% |
| catseg_native | held_out | 4.77 | 15.04 | 49.64% | 88.89% | 44.47% | 82.25% | 91.36% |
| catseg_native | seen | 1.92 | 4.29 | 75.86% | 98.18% | 69.93% | 93.94% | 98.67% |
| catseg_native | name_in_coco | 1.83 | 3.79 | 75.85% | 98.46% | 67.36% | 94.96% | 98.96% |
| catseg_native | name_not_in_coco | 2.98 | 8.41 | 67.73% | 94.59% | 63.54% | 90.05% | 95.77% |
| catseg_anchored | all | 2.58 | 7.11 | 70.17% | 95.99% | 63.35% | 91.24% | 96.91% |
| catseg_anchored | boundary | 3.56 | 10.28 | 49.64% | 94.18% | 43.18% | 85.90% | 95.66% |
| catseg_anchored | interior | 2.45 | 6.72 | 73.02% | 96.24% | 66.17% | 92.00% | 97.06% |
| catseg_anchored | small_class | 7.01 | 24.45 | 36.94% | 84.15% | 29.70% | 70.64% | 87.99% |
| catseg_anchored | held_out | 4.74 | 15.68 | 53.28% | 89.01% | 44.97% | 82.70% | 91.34% |
| catseg_anchored | seen | 2.00 | 4.61 | 74.28% | 97.98% | 67.76% | 92.99% | 98.55% |
| catseg_anchored | name_in_coco | 1.82 | 3.74 | 76.57% | 98.48% | 68.75% | 94.94% | 99.05% |
| catseg_anchored | name_not_in_coco | 3.11 | 9.26 | 65.31% | 94.35% | 59.33% | 88.87% | 95.54% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 16.38 | 38.78% |
| catseg_native | 33.83 | 72.46% |
| catseg_anchored | 32.41 | 70.38% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.09, native_150_plus_845 0.76, anchored_reference_plus_845 0.75; peak memory 8.0 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.