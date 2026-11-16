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
| catseg_native | all | 1.84 | 3.76 | 76.45% | 98.37% | 70.15% | 95.06% | 99.05% |
| catseg_native | boundary | 2.48 | 5.33 | 56.84% | 97.14% | 52.17% | 91.76% | 98.50% |
| catseg_native | interior | 1.75 | 3.55 | 79.13% | 98.53% | 72.67% | 95.52% | 99.12% |
| catseg_native | small_class | 3.84 | 10.84 | 39.82% | 93.75% | 34.56% | 85.51% | 95.56% |
| catseg_native | held_out | 3.16 | 8.49 | 58.59% | 95.82% | 48.10% | 89.03% | 97.01% |
| catseg_native | seen | 1.72 | 3.29 | 79.14% | 98.61% | 73.81% | 95.98% | 99.18% |
| catseg_native | name_in_coco | 1.68 | 2.85 | 77.92% | 98.97% | 72.79% | 96.06% | 99.42% |
| catseg_native | name_not_in_coco | 2.04 | 4.67 | 71.69% | 98.00% | 65.43% | 93.84% | 98.80% |
| catseg_anchored | all | 1.89 | 3.86 | 75.40% | 98.29% | 68.33% | 94.26% | 98.93% |
| catseg_anchored | boundary | 2.61 | 5.84 | 55.25% | 96.93% | 49.05% | 90.10% | 98.25% |
| catseg_anchored | interior | 1.80 | 3.60 | 78.18% | 98.47% | 71.01% | 94.87% | 99.02% |
| catseg_anchored | small_class | 3.98 | 11.25 | 39.93% | 93.68% | 34.51% | 84.43% | 95.44% |
| catseg_anchored | held_out | 3.23 | 8.83 | 60.46% | 95.56% | 49.17% | 87.77% | 96.86% |
| catseg_anchored | seen | 1.77 | 3.55 | 77.73% | 98.50% | 71.39% | 95.13% | 99.00% |
| catseg_anchored | name_in_coco | 1.69 | 3.15 | 77.80% | 98.95% | 71.10% | 95.81% | 99.30% |
| catseg_anchored | name_not_in_coco | 2.11 | 4.50 | 70.54% | 97.84% | 63.95% | 92.88% | 98.66% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.12 | 17.71% |
| catseg_native | 40.21 | 76.71% |
| catseg_anchored | 39.14 | 75.77% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.34, native_150_plus_845 2.10, anchored_reference_plus_845 6.18, native_150 0.75, native_845 1.35; peak memory 9.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.