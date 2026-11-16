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
| catseg_native | all | 2.41 | 6.22 | 72.69% | 96.49% | 64.62% | 92.55% | 97.60% |
| catseg_native | boundary | 3.21 | 8.85 | 53.36% | 95.18% | 45.94% | 88.09% | 96.75% |
| catseg_native | interior | 2.30 | 5.87 | 75.36% | 96.64% | 67.23% | 93.17% | 97.71% |
| catseg_native | small_class | 5.62 | 17.91 | 29.59% | 88.20% | 23.93% | 74.72% | 91.01% |
| catseg_native | held_out | 5.00 | 16.57 | 48.15% | 88.29% | 41.68% | 81.99% | 91.02% |
| catseg_native | seen | 2.08 | 4.98 | 75.53% | 97.91% | 67.85% | 94.13% | 98.35% |
| catseg_native | name_in_coco | 1.98 | 4.51 | 75.28% | 98.36% | 66.19% | 94.13% | 98.81% |
| catseg_native | name_not_in_coco | 2.98 | 8.50 | 67.40% | 94.92% | 61.03% | 90.63% | 96.49% |
| catseg_anchored | all | 2.46 | 6.58 | 71.96% | 96.43% | 63.89% | 91.65% | 97.42% |
| catseg_anchored | boundary | 3.34 | 9.43 | 52.03% | 95.06% | 45.05% | 86.33% | 96.57% |
| catseg_anchored | interior | 2.34 | 6.20 | 74.70% | 96.60% | 66.54% | 92.38% | 97.52% |
| catseg_anchored | small_class | 5.75 | 18.07 | 30.00% | 87.79% | 24.21% | 73.42% | 91.05% |
| catseg_anchored | held_out | 5.10 | 17.25 | 48.49% | 88.53% | 41.47% | 81.95% | 90.92% |
| catseg_anchored | seen | 2.13 | 5.22 | 74.50% | 97.78% | 66.99% | 93.10% | 98.23% |
| catseg_anchored | name_in_coco | 1.99 | 4.55 | 75.07% | 98.37% | 66.23% | 93.87% | 98.78% |
| catseg_anchored | name_not_in_coco | 3.06 | 9.08 | 66.60% | 94.84% | 59.72% | 89.55% | 96.22% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 15.62 | 38.78% |
| catseg_native | 35.27 | 73.03% |
| catseg_anchored | 33.85 | 72.33% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.09, native_150_plus_845 0.77, anchored_reference_plus_845 1.15; peak memory 8.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.