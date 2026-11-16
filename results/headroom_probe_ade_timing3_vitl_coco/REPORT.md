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
| catseg_native | all | 1.63 | 2.70 | 78.40% | 98.65% | 71.08% | 96.81% | 99.36% |
| catseg_native | boundary | 2.34 | 4.34 | 58.14% | 97.53% | 52.81% | 93.18% | 98.64% |
| catseg_native | interior | 1.53 | 2.46 | 81.16% | 98.84% | 73.54% | 97.34% | 99.48% |
| catseg_native | small_class | 3.54 | 11.78 | 36.57% | 93.51% | 29.48% | 85.28% | 96.06% |
| catseg_native | held_out | 2.59 | 5.79 | 57.66% | 95.71% | 44.52% | 89.92% | 97.00% |
| catseg_native | seen | 1.59 | 2.77 | 79.59% | 98.80% | 72.94% | 97.10% | 99.44% |
| catseg_native | name_in_coco | 1.66 | 2.88 | 77.44% | 98.85% | 70.34% | 96.42% | 99.44% |
| catseg_native | name_not_in_coco | 1.89 | 3.24 | 73.48% | 97.97% | 66.11% | 95.52% | 98.86% |
| catseg_anchored | all | 1.74 | 3.19 | 75.90% | 98.57% | 67.37% | 95.71% | 99.23% |
| catseg_anchored | boundary | 2.60 | 5.47 | 53.08% | 97.15% | 46.16% | 90.91% | 98.35% |
| catseg_anchored | interior | 1.61 | 2.87 | 78.98% | 98.81% | 70.19% | 96.41% | 99.38% |
| catseg_anchored | small_class | 3.39 | 7.74 | 43.83% | 93.08% | 38.72% | 85.27% | 96.25% |
| catseg_anchored | held_out | 2.67 | 6.43 | 62.57% | 95.61% | 47.99% | 89.15% | 96.76% |
| catseg_anchored | seen | 1.69 | 3.00 | 77.62% | 98.67% | 69.87% | 95.83% | 99.35% |
| catseg_anchored | name_in_coco | 1.65 | 2.81 | 77.65% | 98.91% | 69.97% | 96.07% | 99.46% |
| catseg_anchored | name_not_in_coco | 2.05 | 4.12 | 70.06% | 97.82% | 61.53% | 94.11% | 98.67% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 13.26 | 39.77% |
| catseg_native | 34.98 | 78.22% |
| catseg_anchored | 32.72 | 75.75% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.22, native_150_plus_845 1.23, anchored_reference_plus_845 2.70, native_150 0.47, native_845 0.75; peak memory 9.3 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.