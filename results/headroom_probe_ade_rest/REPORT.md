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
| catseg_native | all | 2.37 | 6.29 | 71.66% | 96.67% | 66.03% | 92.22% | 97.93% |
| catseg_native | boundary | 3.33 | 8.93 | 52.32% | 94.52% | 47.84% | 87.46% | 96.73% |
| catseg_native | interior | 2.24 | 5.95 | 74.31% | 96.97% | 68.55% | 92.87% | 98.08% |
| catseg_native | small_class | 7.83 | 28.92 | 27.52% | 81.64% | 23.02% | 66.73% | 86.07% |
| catseg_native | held_out | 4.09 | 15.62 | 53.22% | 91.78% | 44.33% | 84.48% | 94.37% |
| catseg_native | seen | 2.03 | 4.27 | 75.15% | 97.58% | 70.00% | 93.63% | 98.51% |
| catseg_native | name_in_coco | 2.09 | 4.02 | 74.57% | 97.25% | 70.52% | 93.82% | 98.60% |
| catseg_native | name_not_in_coco | 2.66 | 7.68 | 67.72% | 95.80% | 61.82% | 90.48% | 97.35% |
| catseg_anchored | all | 2.49 | 6.21 | 69.28% | 96.35% | 63.11% | 90.89% | 97.70% |
| catseg_anchored | boundary | 3.59 | 9.58 | 48.48% | 93.82% | 43.09% | 84.50% | 96.16% |
| catseg_anchored | interior | 2.34 | 5.76 | 72.16% | 96.72% | 65.89% | 91.80% | 97.89% |
| catseg_anchored | small_class | 7.60 | 25.80 | 31.66% | 81.87% | 25.65% | 66.74% | 86.34% |
| catseg_anchored | held_out | 4.16 | 12.58 | 55.49% | 91.44% | 43.70% | 84.13% | 94.22% |
| catseg_anchored | seen | 2.14 | 4.85 | 73.07% | 97.23% | 67.51% | 92.14% | 98.22% |
| catseg_anchored | name_in_coco | 2.08 | 4.27 | 74.72% | 97.31% | 70.04% | 93.07% | 98.56% |
| catseg_anchored | name_not_in_coco | 2.82 | 7.43 | 64.54% | 95.33% | 58.18% | 88.95% | 97.06% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 16.38 | 38.78% |
| catseg_native | 30.98 | 71.87% |
| catseg_anchored | 29.72 | 69.49% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.08, native_150_plus_845 1.36, anchored_reference_plus_845 2.93; peak memory 8.1 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.