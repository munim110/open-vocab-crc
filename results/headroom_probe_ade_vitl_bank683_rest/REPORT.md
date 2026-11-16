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
| catseg_native | all | 1.96 | 4.31 | 74.79% | 98.04% | 68.18% | 94.71% | 98.76% |
| catseg_native | boundary | 2.65 | 5.83 | 55.55% | 96.66% | 50.32% | 91.34% | 98.19% |
| catseg_native | interior | 1.87 | 4.12 | 77.42% | 98.22% | 70.63% | 95.16% | 98.83% |
| catseg_native | small_class | 5.57 | 16.26 | 33.81% | 88.29% | 27.89% | 77.98% | 92.11% |
| catseg_native | held_out | 2.84 | 7.64 | 59.88% | 95.69% | 48.75% | 90.14% | 97.16% |
| catseg_native | seen | 1.76 | 3.43 | 77.74% | 98.59% | 72.00% | 95.56% | 99.16% |
| catseg_native | name_in_coco | 1.73 | 2.92 | 77.01% | 98.65% | 70.70% | 96.15% | 99.38% |
| catseg_native | name_not_in_coco | 2.16 | 5.07 | 70.94% | 97.59% | 64.61% | 93.61% | 98.47% |
| catseg_anchored | all | 2.00 | 4.19 | 74.09% | 97.94% | 66.73% | 94.10% | 98.71% |
| catseg_anchored | boundary | 2.77 | 6.18 | 54.39% | 96.37% | 47.74% | 89.92% | 97.99% |
| catseg_anchored | interior | 1.89 | 3.93 | 76.78% | 98.15% | 69.33% | 94.68% | 98.80% |
| catseg_anchored | small_class | 5.60 | 16.57 | 34.54% | 87.87% | 28.99% | 77.58% | 91.97% |
| catseg_anchored | held_out | 2.89 | 7.16 | 60.66% | 95.30% | 51.22% | 89.74% | 96.98% |
| catseg_anchored | seen | 1.81 | 3.55 | 76.73% | 98.49% | 69.80% | 94.89% | 99.09% |
| catseg_anchored | name_in_coco | 1.74 | 3.09 | 76.65% | 98.66% | 68.45% | 95.80% | 99.31% |
| catseg_anchored | name_not_in_coco | 2.21 | 4.86 | 70.15% | 97.44% | 63.71% | 92.95% | 98.40% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 16.38 | 38.78% |
| catseg_native | 36.82 | 75.00% |
| catseg_anchored | 35.85 | 74.30% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.23, native_150_plus_845 1.25, anchored_reference_plus_845 4.19, native_150 0.48, native_845 0.77; peak memory 9.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.