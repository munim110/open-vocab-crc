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
| catseg_native | all | 1.61 | 3.01 | 79.81% | 98.93% | 73.86% | 96.34% | 99.35% |
| catseg_native | boundary | 2.40 | 5.26 | 57.55% | 97.41% | 54.86% | 92.33% | 98.49% |
| catseg_native | interior | 1.51 | 2.72 | 82.66% | 99.14% | 76.41% | 96.88% | 99.46% |
| catseg_native | small_class | 2.87 | 5.94 | 41.63% | 96.02% | 37.03% | 88.75% | 97.75% |
| catseg_native | held_out | 2.94 | 8.50 | 59.85% | 96.62% | 48.76% | 88.52% | 97.41% |
| catseg_native | seen | 1.52 | 2.40 | 81.62% | 99.14% | 76.17% | 97.01% | 99.46% |
| catseg_native | name_in_coco | 1.69 | 2.79 | 78.72% | 98.77% | 75.49% | 95.50% | 99.29% |
| catseg_native | name_not_in_coco | 1.89 | 5.26 | 75.70% | 98.17% | 69.25% | 95.32% | 98.69% |
| catseg_anchored | all | 1.65 | 2.98 | 79.40% | 98.83% | 72.69% | 95.54% | 99.30% |
| catseg_anchored | boundary | 2.52 | 5.64 | 56.12% | 97.36% | 50.79% | 90.57% | 98.26% |
| catseg_anchored | interior | 1.53 | 2.64 | 82.41% | 99.05% | 75.54% | 96.24% | 99.43% |
| catseg_anchored | small_class | 3.05 | 6.54 | 40.58% | 95.97% | 35.49% | 87.56% | 97.50% |
| catseg_anchored | held_out | 3.00 | 8.08 | 61.97% | 96.13% | 50.28% | 86.38% | 97.34% |
| catseg_anchored | seen | 1.56 | 2.67 | 80.64% | 99.13% | 74.29% | 96.24% | 99.42% |
| catseg_anchored | name_in_coco | 1.67 | 3.04 | 79.82% | 99.01% | 75.88% | 95.03% | 99.11% |
| catseg_anchored | name_not_in_coco | 1.94 | 4.02 | 74.74% | 98.06% | 67.95% | 94.40% | 98.77% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 13.26 | 39.77% |
| catseg_native | 38.82 | 79.79% |
| catseg_anchored | 38.07 | 79.41% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.24, native_150_plus_845 1.27, anchored_reference_plus_845 4.02, native_150 0.50, native_845 0.77; peak memory 9.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.