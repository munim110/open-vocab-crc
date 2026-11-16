# Ranking headroom probe

100 development images (roles tune_cal,tune_eval), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 8.82 | 33.99 | 39.68% | 79.31% | 28.53% | 60.31% | 83.35% |
| sclip_cached | boundary | 15.08 | 62.16 | 21.79% | 64.29% | 13.91% | 42.53% | 70.03% |
| sclip_cached | interior | 8.01 | 30.46 | 41.98% | 81.34% | 30.40% | 62.56% | 85.17% |
| sclip_cached | small_class | 22.10 | 93.01 | 11.58% | 50.13% | 4.99% | 33.52% | 56.30% |
| sclip_cached | held_out | 16.57 | 69.32 | 22.86% | 60.98% | 13.55% | 39.89% | 65.05% |
| sclip_cached | seen | 9.49 | 36.60 | 40.11% | 77.11% | 28.86% | 59.23% | 81.60% |
| sclip_cached | name_in_coco | 9.05 | 34.96 | 41.88% | 78.55% | 31.63% | 64.44% | 82.68% |
| sclip_cached | name_not_in_coco | 10.54 | 41.44 | 33.34% | 74.76% | 24.08% | 53.11% | 79.45% |
| catseg_native | all | 2.14 | 6.28 | 76.58% | 97.48% | 71.05% | 94.54% | 98.17% |
| catseg_native | boundary | 3.53 | 10.23 | 53.76% | 95.03% | 50.87% | 88.48% | 96.78% |
| catseg_native | interior | 1.96 | 5.77 | 79.51% | 97.80% | 73.82% | 95.33% | 98.33% |
| catseg_native | small_class | 5.70 | 17.07 | 27.67% | 88.17% | 24.08% | 77.05% | 91.87% |
| catseg_native | held_out | 3.90 | 15.84 | 53.07% | 91.42% | 44.52% | 84.35% | 93.68% |
| catseg_native | seen | 2.07 | 4.97 | 76.92% | 97.84% | 71.83% | 94.88% | 98.47% |
| catseg_native | name_in_coco | 2.07 | 4.20 | 78.12% | 96.70% | 75.57% | 94.27% | 97.60% |
| catseg_native | name_not_in_coco | 2.66 | 9.44 | 71.19% | 96.89% | 64.36% | 93.11% | 97.58% |
| catseg_anchored | all | 2.27 | 5.50 | 73.27% | 97.27% | 67.12% | 93.24% | 98.06% |
| catseg_anchored | boundary | 3.93 | 11.11 | 49.03% | 93.48% | 44.18% | 84.41% | 96.31% |
| catseg_anchored | interior | 2.06 | 4.83 | 76.46% | 97.66% | 70.17% | 94.31% | 98.27% |
| catseg_anchored | small_class | 5.57 | 16.70 | 31.36% | 88.50% | 28.85% | 74.25% | 92.31% |
| catseg_anchored | held_out | 3.88 | 11.74 | 55.63% | 90.92% | 44.45% | 82.92% | 93.16% |
| catseg_anchored | seen | 2.20 | 5.13 | 74.19% | 97.60% | 68.53% | 93.07% | 98.32% |
| catseg_anchored | name_in_coco | 2.05 | 4.29 | 78.44% | 96.72% | 75.29% | 93.86% | 97.90% |
| catseg_anchored | name_not_in_coco | 2.87 | 8.01 | 66.86% | 96.59% | 59.41% | 91.44% | 97.42% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 13.26 | 39.77% |
| catseg_native | 30.79 | 76.39% |
| catseg_anchored | 28.85 | 73.34% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.07, native_150_plus_845 1.23, anchored_reference_plus_845 2.69, native_150 0.47, native_845 0.75; peak memory 8.3 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.