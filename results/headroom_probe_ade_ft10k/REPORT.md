# Ranking headroom probe

400 development images (roles tune_cal,tune_eval), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 16.20 | 16.20 | 18.10% | 64.41% | 18.10% | 64.41% | 90.65% |
| sclip_cached | boundary | 21.94 | 21.94 | 15.84% | 53.88% | 15.84% | 53.88% | 85.84% |
| sclip_cached | interior | 15.35 | 15.35 | 18.36% | 65.90% | 18.36% | 65.90% | 91.35% |
| sclip_cached | small_class | 59.65 | 59.65 | 0.55% | 10.57% | 0.55% | 10.57% | 55.27% |
| sclip_cached | held_out | 33.02 | 33.02 | 0.00% | 30.79% | 0.00% | 30.79% | 75.48% |
| sclip_cached | seen | 16.34 | 16.34 | 19.75% | 66.25% | 19.75% | 66.25% | 89.96% |
| sclip_cached | name_in_coco | 23.36 | 23.36 | 0.00% | 34.72% | 0.00% | 34.72% | 86.84% |
| sclip_cached | name_not_in_coco | 14.52 | 14.52 | 24.10% | 72.95% | 24.10% | 72.95% | 90.89% |
| catseg_native | all | 2.38 | 5.69 | 70.05% | 96.69% | 63.99% | 92.16% | 98.11% |
| catseg_native | boundary | 3.42 | 8.53 | 49.24% | 94.60% | 44.20% | 87.34% | 97.04% |
| catseg_native | interior | 2.24 | 5.32 | 72.93% | 96.95% | 66.75% | 92.83% | 98.23% |
| catseg_native | small_class | 7.19 | 26.15 | 29.73% | 84.23% | 24.33% | 72.31% | 89.42% |
| catseg_native | held_out | 3.89 | 12.52 | 54.66% | 92.10% | 41.79% | 83.27% | 95.10% |
| catseg_native | seen | 2.20 | 4.69 | 72.71% | 97.23% | 67.28% | 93.33% | 98.46% |
| catseg_native | name_in_coco | 2.04 | 4.01 | 75.77% | 97.66% | 70.66% | 93.63% | 98.57% |
| catseg_native | name_not_in_coco | 2.80 | 7.34 | 63.28% | 95.72% | 57.33% | 90.28% | 97.51% |
| catseg_anchored | all | 2.43 | 5.66 | 69.66% | 96.57% | 63.62% | 91.16% | 97.97% |
| catseg_anchored | boundary | 3.53 | 8.94 | 48.30% | 94.32% | 43.13% | 85.31% | 96.64% |
| catseg_anchored | interior | 2.28 | 5.22 | 72.63% | 96.86% | 66.51% | 91.97% | 98.13% |
| catseg_anchored | small_class | 7.22 | 23.43 | 28.73% | 84.64% | 24.69% | 71.70% | 89.09% |
| catseg_anchored | held_out | 3.95 | 11.03 | 54.17% | 91.84% | 41.81% | 82.84% | 94.87% |
| catseg_anchored | seen | 2.25 | 5.01 | 72.16% | 97.07% | 66.71% | 92.21% | 98.21% |
| catseg_anchored | name_in_coco | 2.03 | 4.12 | 76.03% | 97.71% | 71.39% | 93.17% | 98.46% |
| catseg_anchored | name_not_in_coco | 2.88 | 7.21 | 62.57% | 95.52% | 56.44% | 89.03% | 97.37% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.12 | 17.71% |
| catseg_native | 30.11 | 70.44% |
| catseg_anchored | 29.40 | 70.09% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.03, native_150_plus_845 0.43, anchored_reference_plus_845 0.88; peak memory 8.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.