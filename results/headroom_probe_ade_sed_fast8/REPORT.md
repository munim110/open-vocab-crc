# Ranking headroom probe

400 development images (roles tune_cal,tune_eval), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 9.63 | 37.25 | 38.17% | 76.56% | 26.25% | 58.44% | 80.94% |
| sclip_cached | boundary | 15.37 | 62.71 | 22.38% | 62.36% | 13.30% | 41.83% | 68.47% |
| sclip_cached | interior | 8.88 | 34.00 | 40.22% | 78.45% | 27.92% | 60.62% | 82.58% |
| sclip_cached | small_class | 22.38 | 94.38 | 14.06% | 48.73% | 8.17% | 31.99% | 55.81% |
| sclip_cached | held_out | 15.82 | 64.96 | 21.67% | 61.48% | 12.14% | 39.04% | 67.37% |
| sclip_cached | seen | 10.11 | 39.13 | 40.59% | 76.18% | 28.76% | 59.98% | 80.56% |
| sclip_cached | name_in_coco | 8.62 | 33.42 | 41.78% | 79.39% | 28.80% | 64.12% | 83.11% |
| sclip_cached | name_not_in_coco | 12.00 | 47.05 | 30.54% | 70.15% | 21.87% | 49.87% | 75.53% |
| catseg_native | all | 2.87 | 5.51 | 72.60% | 96.36% | 65.46% | 92.60% | 96.92% |
| catseg_native | boundary | 3.68 | 7.95 | 52.84% | 95.02% | 47.33% | 88.41% | 95.82% |
| catseg_native | interior | 2.76 | 5.20 | 75.31% | 96.51% | 68.03% | 93.16% | 97.03% |
| catseg_native | small_class | 12.32 | 30.53 | 29.26% | 84.74% | 22.72% | 69.89% | 79.05% |
| catseg_native | held_out | 6.14 | 15.21 | 48.29% | 87.70% | 40.98% | 81.40% | 88.82% |
| catseg_native | seen | 2.30 | 4.49 | 75.67% | 97.83% | 69.15% | 94.15% | 97.84% |
| catseg_native | name_in_coco | 2.55 | 5.17 | 75.39% | 98.07% | 68.00% | 94.06% | 97.25% |
| catseg_native | name_not_in_coco | 3.45 | 6.58 | 67.27% | 94.81% | 60.81% | 90.68% | 96.19% |
| catseg_anchored | all | 2.51 | 6.79 | 70.42% | 96.33% | 62.05% | 91.23% | 97.35% |
| catseg_anchored | boundary | 3.43 | 9.83 | 49.48% | 94.87% | 42.22% | 85.56% | 96.47% |
| catseg_anchored | interior | 2.39 | 6.40 | 73.32% | 96.52% | 64.86% | 92.00% | 97.45% |
| catseg_anchored | small_class | 5.35 | 16.93 | 36.76% | 88.35% | 29.40% | 75.83% | 91.32% |
| catseg_anchored | held_out | 5.00 | 16.93 | 51.95% | 88.38% | 41.89% | 81.96% | 91.02% |
| catseg_anchored | seen | 2.18 | 5.44 | 73.72% | 97.69% | 66.15% | 92.66% | 98.16% |
| catseg_anchored | name_in_coco | 1.96 | 4.47 | 75.89% | 98.40% | 67.21% | 94.01% | 98.82% |
| catseg_anchored | name_not_in_coco | 3.12 | 9.33 | 64.69% | 94.71% | 57.07% | 89.00% | 96.13% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 15.62 | 38.78% |
| catseg_native | 34.78 | 72.90% |
| catseg_anchored | 33.50 | 70.80% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.10, native_150_plus_845 0.15, anchored_reference_plus_845 0.75; peak memory 5.5 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.