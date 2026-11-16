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
| catseg_native | all | 2.18 | 5.58 | 76.93% | 97.47% | 69.88% | 94.44% | 98.23% |
| catseg_native | boundary | 3.50 | 10.43 | 54.94% | 95.36% | 48.87% | 89.14% | 96.61% |
| catseg_native | interior | 2.00 | 4.90 | 79.78% | 97.77% | 72.59% | 95.17% | 98.46% |
| catseg_native | small_class | 5.44 | 16.69 | 27.87% | 90.54% | 22.57% | 77.97% | 91.94% |
| catseg_native | held_out | 5.31 | 18.29 | 46.52% | 88.35% | 43.23% | 80.59% | 90.24% |
| catseg_native | seen | 1.83 | 4.10 | 78.69% | 98.48% | 71.24% | 95.24% | 98.90% |
| catseg_native | name_in_coco | 1.63 | 2.91 | 78.50% | 99.07% | 72.35% | 95.10% | 99.59% |
| catseg_native | name_not_in_coco | 3.09 | 9.79 | 72.02% | 95.97% | 65.75% | 92.82% | 97.12% |
| catseg_anchored | all | 2.23 | 5.95 | 76.15% | 97.36% | 69.12% | 93.68% | 98.18% |
| catseg_anchored | boundary | 3.65 | 11.32 | 53.51% | 95.26% | 47.64% | 86.53% | 96.59% |
| catseg_anchored | interior | 2.03 | 5.18 | 79.10% | 97.69% | 71.90% | 94.52% | 98.42% |
| catseg_anchored | small_class | 5.57 | 17.02 | 27.49% | 90.28% | 23.42% | 75.36% | 92.21% |
| catseg_anchored | held_out | 5.39 | 18.96 | 48.38% | 88.33% | 43.52% | 81.04% | 90.55% |
| catseg_anchored | seen | 1.89 | 4.35 | 77.44% | 98.33% | 70.18% | 94.34% | 98.83% |
| catseg_anchored | name_in_coco | 1.63 | 2.95 | 79.48% | 98.99% | 72.20% | 94.94% | 99.54% |
| catseg_anchored | name_not_in_coco | 3.17 | 10.41 | 70.71% | 95.83% | 64.35% | 91.81% | 97.08% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 13.26 | 39.77% |
| catseg_native | 36.62 | 76.92% |
| catseg_anchored | 34.44 | 76.20% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.13, native_150_plus_845 0.80, anchored_reference_plus_845 0.95, native_150 0.16, native_845 0.63; peak memory 8.1 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.