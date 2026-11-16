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
| catseg_native | all | 2.14 | 6.28 | 76.58% | 97.48% | 71.05% | 94.54% | 98.17% |
| catseg_native | boundary | 3.53 | 10.23 | 53.76% | 95.03% | 50.87% | 88.48% | 96.78% |
| catseg_native | interior | 1.96 | 5.77 | 79.51% | 97.80% | 73.82% | 95.33% | 98.33% |
| catseg_native | small_class | 5.70 | 17.07 | 27.67% | 88.17% | 24.08% | 77.05% | 91.87% |
| catseg_native | held_out | 3.90 | 15.84 | 53.07% | 91.42% | 44.52% | 84.35% | 93.68% |
| catseg_native | seen | 2.07 | 4.97 | 76.92% | 97.84% | 71.83% | 94.88% | 98.47% |
| catseg_native | name_in_coco | 2.07 | 4.20 | 78.12% | 96.70% | 75.57% | 94.27% | 97.60% |
| catseg_native | name_not_in_coco | 2.66 | 9.44 | 71.19% | 96.89% | 64.36% | 93.11% | 97.58% |
| catseg_anchored | all | 2.18 | 5.16 | 75.55% | 97.34% | 68.89% | 93.64% | 98.15% |
| catseg_anchored | boundary | 3.72 | 10.42 | 52.17% | 94.61% | 47.09% | 85.30% | 96.42% |
| catseg_anchored | interior | 1.98 | 4.49 | 78.55% | 97.71% | 71.70% | 94.65% | 98.36% |
| catseg_anchored | small_class | 5.78 | 17.57 | 28.91% | 88.08% | 25.00% | 73.21% | 91.19% |
| catseg_anchored | held_out | 4.02 | 12.06 | 53.27% | 90.77% | 45.79% | 83.59% | 93.33% |
| catseg_anchored | seen | 2.11 | 4.77 | 75.74% | 97.73% | 69.25% | 93.72% | 98.42% |
| catseg_anchored | name_in_coco | 2.11 | 4.48 | 78.36% | 96.58% | 74.36% | 93.68% | 97.78% |
| catseg_anchored | name_not_in_coco | 2.72 | 7.39 | 69.63% | 96.72% | 62.16% | 91.92% | 97.61% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.16 | 18.21% |
| catseg_native | 30.79 | 76.39% |
| catseg_anchored | 30.43 | 75.51% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.03, native_150_plus_845 0.43, anchored_reference_plus_845 1.29, native_150 0.15, native_845 0.27; peak memory 8.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.