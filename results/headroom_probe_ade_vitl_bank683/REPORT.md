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
| catseg_native | all | 1.85 | 3.48 | 75.26% | 98.20% | 67.90% | 95.02% | 99.01% |
| catseg_native | boundary | 2.53 | 5.05 | 55.84% | 97.07% | 49.94% | 91.87% | 98.50% |
| catseg_native | interior | 1.75 | 3.26 | 77.94% | 98.36% | 70.37% | 95.46% | 99.09% |
| catseg_native | small_class | 4.53 | 14.40 | 36.87% | 91.30% | 29.83% | 83.23% | 93.76% |
| catseg_native | held_out | 2.71 | 6.15 | 58.41% | 96.30% | 46.73% | 90.59% | 97.35% |
| catseg_native | seen | 1.78 | 3.28 | 77.62% | 98.28% | 71.22% | 95.59% | 99.18% |
| catseg_native | name_in_coco | 1.73 | 2.99 | 76.59% | 98.74% | 68.69% | 96.18% | 99.35% |
| catseg_native | name_not_in_coco | 2.03 | 3.91 | 70.36% | 97.83% | 63.50% | 93.82% | 98.82% |
| catseg_anchored | all | 1.89 | 3.69 | 74.18% | 98.19% | 66.03% | 94.31% | 98.90% |
| catseg_anchored | boundary | 2.64 | 5.65 | 54.56% | 96.94% | 47.25% | 90.33% | 98.24% |
| catseg_anchored | interior | 1.79 | 3.43 | 76.89% | 98.37% | 68.60% | 94.88% | 99.00% |
| catseg_anchored | small_class | 4.62 | 12.94 | 37.33% | 91.28% | 31.49% | 83.54% | 94.07% |
| catseg_anchored | held_out | 2.81 | 6.82 | 59.49% | 96.07% | 48.99% | 89.89% | 97.16% |
| catseg_anchored | seen | 1.82 | 3.51 | 76.45% | 98.27% | 68.73% | 94.80% | 99.02% |
| catseg_anchored | name_in_coco | 1.74 | 3.21 | 76.03% | 98.84% | 66.12% | 95.79% | 99.33% |
| catseg_anchored | name_not_in_coco | 2.10 | 4.22 | 69.20% | 97.77% | 62.20% | 92.86% | 98.66% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 15.62 | 38.78% |
| catseg_native | 35.25 | 75.47% |
| catseg_anchored | 34.32 | 74.42% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.22, native_150_plus_845 1.23, anchored_reference_plus_845 4.12, native_150 0.47, native_845 0.76; peak memory 9.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.