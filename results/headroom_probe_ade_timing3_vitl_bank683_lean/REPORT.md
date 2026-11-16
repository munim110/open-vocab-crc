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
| catseg_anchored | all | 1.69 | 3.00 | 77.25% | 98.63% | 69.62% | 96.08% | 99.23% |
| catseg_anchored | boundary | 2.49 | 5.11 | 56.65% | 97.26% | 49.33% | 91.58% | 98.35% |
| catseg_anchored | interior | 1.57 | 2.71 | 80.05% | 98.85% | 72.26% | 96.73% | 99.37% |
| catseg_anchored | small_class | 3.56 | 8.19 | 36.81% | 93.00% | 32.89% | 85.36% | 96.52% |
| catseg_anchored | held_out | 2.74 | 6.53 | 59.70% | 95.69% | 48.34% | 88.89% | 96.51% |
| catseg_anchored | seen | 1.64 | 2.84 | 78.39% | 98.77% | 71.06% | 96.35% | 99.32% |
| catseg_anchored | name_in_coco | 1.66 | 2.85 | 77.35% | 98.81% | 69.01% | 95.89% | 99.39% |
| catseg_anchored | name_not_in_coco | 1.98 | 3.83 | 71.86% | 97.95% | 64.97% | 94.63% | 98.68% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 13.26 | 39.77% |
| catseg_native | 34.98 | 78.22% |
| catseg_anchored | 33.82 | 77.06% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.23, native_150_plus_845 1.24, anchored_reference_plus_845 3.38, native_150 0.48, native_845 0.76; peak memory 9.3 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.