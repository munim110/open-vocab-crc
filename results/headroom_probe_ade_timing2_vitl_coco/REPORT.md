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
| sclip_cached | 0.16 | 18.21% |
| catseg_native | 34.98 | 78.22% |
| catseg_anchored | 32.72 | 75.75% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.07, native_150_plus_845 0.43, anchored_reference_plus_845 0.88, native_150 0.15, native_845 0.28; peak memory 9.3 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.