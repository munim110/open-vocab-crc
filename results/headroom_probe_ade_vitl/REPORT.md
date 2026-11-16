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
| catseg_native | all | 1.85 | 3.48 | 75.26% | 98.20% | 67.90% | 95.02% | 99.01% |
| catseg_native | boundary | 2.53 | 5.05 | 55.84% | 97.07% | 49.94% | 91.87% | 98.50% |
| catseg_native | interior | 1.75 | 3.26 | 77.94% | 98.36% | 70.37% | 95.46% | 99.09% |
| catseg_native | small_class | 4.53 | 14.40 | 36.87% | 91.30% | 29.83% | 83.23% | 93.76% |
| catseg_native | held_out | 2.71 | 6.15 | 58.41% | 96.30% | 46.73% | 90.59% | 97.35% |
| catseg_native | seen | 1.78 | 3.28 | 77.62% | 98.28% | 71.22% | 95.59% | 99.18% |
| catseg_native | name_in_coco | 1.73 | 2.99 | 76.59% | 98.74% | 68.69% | 96.18% | 99.35% |
| catseg_native | name_not_in_coco | 2.03 | 3.91 | 70.36% | 97.83% | 63.50% | 93.82% | 98.82% |
| catseg_anchored | all | 1.95 | 3.89 | 72.41% | 98.08% | 63.71% | 93.88% | 98.85% |
| catseg_anchored | boundary | 2.74 | 5.95 | 51.43% | 96.75% | 44.61% | 89.70% | 98.13% |
| catseg_anchored | interior | 1.84 | 3.61 | 75.30% | 98.28% | 66.37% | 94.50% | 98.95% |
| catseg_anchored | small_class | 4.33 | 11.96 | 43.16% | 91.58% | 36.73% | 84.38% | 94.21% |
| catseg_anchored | held_out | 2.76 | 6.70 | 61.75% | 95.94% | 49.48% | 89.86% | 97.12% |
| catseg_anchored | seen | 1.86 | 3.69 | 75.54% | 98.14% | 67.62% | 94.34% | 98.93% |
| catseg_anchored | name_in_coco | 1.72 | 3.15 | 76.23% | 98.89% | 67.53% | 95.68% | 99.34% |
| catseg_anchored | name_not_in_coco | 2.17 | 4.47 | 67.03% | 97.62% | 59.07% | 92.38% | 98.59% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.12 | 17.71% |
| catseg_native | 35.25 | 75.47% |
| catseg_anchored | 33.89 | 72.66% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.15, native_150_plus_845 0.96, anchored_reference_plus_845 1.94; peak memory 9.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.