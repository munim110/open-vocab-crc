# Ranking headroom probe

400 development tuning images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

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
| catseg_native | all | 2.25 | 5.46 | 72.56% | 96.82% | 66.07% | 92.60% | 98.18% |
| catseg_native | boundary | 3.24 | 8.29 | 52.61% | 94.77% | 47.59% | 88.03% | 97.07% |
| catseg_native | interior | 2.12 | 5.09 | 75.28% | 97.07% | 68.66% | 93.22% | 98.31% |
| catseg_native | small_class | 7.21 | 26.00 | 28.57% | 84.39% | 23.63% | 72.30% | 88.79% |
| catseg_native | held_out | 3.71 | 11.92 | 53.17% | 92.64% | 41.37% | 83.97% | 95.44% |
| catseg_native | seen | 2.10 | 4.51 | 75.03% | 97.36% | 69.53% | 93.76% | 98.46% |
| catseg_native | name_in_coco | 2.07 | 4.09 | 74.97% | 97.48% | 70.89% | 93.43% | 98.39% |
| catseg_native | name_not_in_coco | 2.60 | 6.99 | 67.01% | 95.98% | 60.12% | 91.09% | 97.69% |
| catseg_anchored | all | 2.40 | 5.70 | 69.70% | 96.58% | 62.81% | 90.80% | 97.97% |
| catseg_anchored | boundary | 3.55 | 9.24 | 48.24% | 93.96% | 42.27% | 84.49% | 96.53% |
| catseg_anchored | interior | 2.24 | 5.24 | 72.65% | 96.89% | 65.66% | 91.67% | 98.15% |
| catseg_anchored | small_class | 7.01 | 23.15 | 31.85% | 85.34% | 26.46% | 71.78% | 88.89% |
| catseg_anchored | held_out | 3.81 | 10.78 | 55.04% | 92.13% | 40.47% | 82.70% | 95.19% |
| catseg_anchored | seen | 2.24 | 5.12 | 72.90% | 97.07% | 66.83% | 91.80% | 98.20% |
| catseg_anchored | name_in_coco | 2.06 | 4.36 | 75.09% | 97.49% | 70.01% | 92.44% | 98.50% |
| catseg_anchored | name_not_in_coco | 2.81 | 7.15 | 63.40% | 95.63% | 56.31% | 88.91% | 97.38% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 15.62 | 38.78% |
| catseg_native | 31.23 | 72.80% |
| catseg_anchored | 29.74 | 70.12% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.07, native_150_plus_845 1.24, anchored_reference_plus_845 2.70; peak memory 8.1 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.