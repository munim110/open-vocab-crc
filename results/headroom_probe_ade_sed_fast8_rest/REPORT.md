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
| catseg_native | all | 2.89 | 5.78 | 72.01% | 96.04% | 66.66% | 92.25% | 96.76% |
| catseg_native | boundary | 3.82 | 8.31 | 52.77% | 94.45% | 48.03% | 88.09% | 95.39% |
| catseg_native | interior | 2.76 | 5.43 | 74.68% | 96.27% | 69.26% | 92.83% | 96.94% |
| catseg_native | small_class | 12.22 | 35.16 | 29.13% | 81.35% | 22.13% | 64.56% | 75.34% |
| catseg_native | held_out | 6.21 | 14.68 | 49.89% | 88.27% | 43.79% | 82.45% | 90.12% |
| catseg_native | seen | 2.12 | 4.53 | 75.94% | 98.14% | 70.51% | 94.03% | 98.07% |
| catseg_native | name_in_coco | 2.03 | 4.49 | 76.09% | 98.37% | 68.67% | 94.71% | 97.73% |
| catseg_native | name_not_in_coco | 3.55 | 7.32 | 67.53% | 94.37% | 63.04% | 90.04% | 95.43% |
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
| catseg_native | 33.73 | 72.20% |
| catseg_anchored | 32.41 | 70.38% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.09, native_150_plus_845 0.15, anchored_reference_plus_845 0.75; peak memory 5.5 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.