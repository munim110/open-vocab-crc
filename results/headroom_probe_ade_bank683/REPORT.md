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
| catseg_native | all | 2.25 | 5.46 | 72.56% | 96.82% | 66.07% | 92.60% | 98.18% |
| catseg_native | boundary | 3.24 | 8.29 | 52.61% | 94.77% | 47.59% | 88.03% | 97.07% |
| catseg_native | interior | 2.12 | 5.09 | 75.28% | 97.07% | 68.66% | 93.22% | 98.31% |
| catseg_native | small_class | 7.21 | 26.00 | 28.57% | 84.39% | 23.63% | 72.30% | 88.79% |
| catseg_native | held_out | 3.71 | 11.92 | 53.17% | 92.64% | 41.37% | 83.97% | 95.44% |
| catseg_native | seen | 2.10 | 4.51 | 75.03% | 97.36% | 69.53% | 93.76% | 98.46% |
| catseg_native | name_in_coco | 2.07 | 4.09 | 74.97% | 97.48% | 70.89% | 93.43% | 98.39% |
| catseg_native | name_not_in_coco | 2.60 | 6.99 | 67.01% | 95.98% | 60.12% | 91.09% | 97.69% |
| catseg_anchored | all | 2.31 | 5.35 | 71.74% | 96.74% | 64.57% | 91.52% | 98.09% |
| catseg_anchored | boundary | 3.39 | 8.71 | 51.07% | 94.61% | 44.72% | 85.48% | 96.71% |
| catseg_anchored | interior | 2.16 | 4.91 | 74.57% | 97.02% | 67.32% | 92.35% | 98.26% |
| catseg_anchored | small_class | 7.37 | 24.58 | 29.40% | 84.90% | 24.57% | 69.77% | 88.24% |
| catseg_anchored | held_out | 3.84 | 10.82 | 53.70% | 92.34% | 42.63% | 82.63% | 95.05% |
| catseg_anchored | seen | 2.15 | 4.79 | 74.09% | 97.25% | 67.38% | 92.59% | 98.37% |
| catseg_anchored | name_in_coco | 2.10 | 4.50 | 74.31% | 97.34% | 68.01% | 92.33% | 98.47% |
| catseg_anchored | name_not_in_coco | 2.69 | 6.69 | 66.09% | 95.82% | 59.14% | 89.72% | 97.53% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.12 | 17.71% |
| catseg_native | 31.23 | 72.80% |
| catseg_anchored | 30.58 | 72.15% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.05, native_150_plus_845 0.65, anchored_reference_plus_845 1.65; peak memory 8.3 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.