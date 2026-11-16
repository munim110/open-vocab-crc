# Ranking headroom probe

100 development images (roles tune_cal,tune_eval), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 15.98 | 15.98 | 18.52% | 64.20% | 18.52% | 64.20% | 90.72% |
| sclip_cached | boundary | 21.48 | 21.48 | 17.28% | 54.11% | 17.28% | 54.11% | 86.47% |
| sclip_cached | interior | 15.18 | 15.18 | 18.72% | 65.71% | 18.72% | 65.71% | 91.36% |
| sclip_cached | small_class | 55.25 | 55.25 | 0.78% | 7.96% | 0.78% | 7.96% | 62.07% |
| sclip_cached | held_out | 32.27 | 32.27 | 0.00% | 29.66% | 0.00% | 29.66% | 75.93% |
| sclip_cached | seen | 15.67 | 15.67 | 20.28% | 66.63% | 20.28% | 66.63% | 90.21% |
| sclip_cached | name_in_coco | 24.44 | 24.44 | 0.00% | 30.37% | 0.00% | 30.37% | 86.13% |
| sclip_cached | name_not_in_coco | 13.27 | 13.27 | 24.98% | 74.39% | 24.98% | 74.39% | 92.27% |
| catseg_native | all | 2.18 | 5.58 | 76.93% | 97.47% | 69.88% | 94.44% | 98.23% |
| catseg_native | boundary | 3.50 | 10.43 | 54.94% | 95.36% | 48.87% | 89.14% | 96.61% |
| catseg_native | interior | 2.00 | 4.90 | 79.78% | 97.77% | 72.59% | 95.17% | 98.46% |
| catseg_native | small_class | 5.44 | 16.69 | 27.87% | 90.54% | 22.57% | 77.97% | 91.94% |
| catseg_native | held_out | 5.31 | 18.29 | 46.52% | 88.35% | 43.23% | 80.59% | 90.24% |
| catseg_native | seen | 1.83 | 4.10 | 78.69% | 98.48% | 71.24% | 95.24% | 98.90% |
| catseg_native | name_in_coco | 1.63 | 2.91 | 78.50% | 99.07% | 72.35% | 95.10% | 99.59% |
| catseg_native | name_not_in_coco | 3.09 | 9.79 | 72.02% | 95.97% | 65.75% | 92.82% | 97.12% |
| catseg_anchored | all | 2.29 | 6.23 | 74.41% | 97.31% | 67.01% | 93.29% | 98.11% |
| catseg_anchored | boundary | 3.80 | 12.00 | 50.19% | 95.03% | 44.23% | 85.79% | 96.45% |
| catseg_anchored | interior | 2.08 | 5.44 | 77.56% | 97.66% | 69.97% | 94.17% | 98.36% |
| catseg_anchored | small_class | 5.20 | 16.06 | 36.65% | 90.94% | 31.99% | 77.32% | 92.29% |
| catseg_anchored | held_out | 5.20 | 18.24 | 51.78% | 88.41% | 44.02% | 79.89% | 90.48% |
| catseg_anchored | seen | 1.95 | 4.68 | 76.24% | 98.27% | 68.91% | 93.94% | 98.74% |
| catseg_anchored | name_in_coco | 1.62 | 2.92 | 78.87% | 99.09% | 73.23% | 94.88% | 99.51% |
| catseg_anchored | name_not_in_coco | 3.25 | 10.83 | 68.80% | 95.77% | 61.09% | 91.26% | 97.02% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.16 | 18.21% |
| catseg_native | 36.62 | 76.92% |
| catseg_anchored | 34.11 | 74.53% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.03, native_150_plus_845 0.40, anchored_reference_plus_845 0.40, native_150 0.06, native_845 0.34; peak memory 8.0 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.