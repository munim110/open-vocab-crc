# Ranking headroom probe

1600 development images (roles fit,calibration,evaluation), image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only; no calibrated set-size claim.

| Arm | Group | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 15.64 | 15.64 | 16.92% | 64.60% | 16.92% | 64.60% | 91.75% |
| sclip_cached | boundary | 20.97 | 20.97 | 15.36% | 54.02% | 15.36% | 54.02% | 87.25% |
| sclip_cached | interior | 14.88 | 14.88 | 17.18% | 66.10% | 17.18% | 66.10% | 92.38% |
| sclip_cached | small_class | 59.66 | 59.66 | 1.56% | 11.89% | 1.56% | 11.89% | 53.70% |
| sclip_cached | held_out | 30.00 | 30.00 | 0.00% | 33.65% | 0.00% | 33.65% | 79.51% |
| sclip_cached | seen | 16.29 | 16.29 | 18.90% | 65.97% | 18.90% | 65.97% | 90.48% |
| sclip_cached | name_in_coco | 22.53 | 22.53 | 0.00% | 37.03% | 0.00% | 37.03% | 88.16% |
| sclip_cached | name_not_in_coco | 14.29 | 14.29 | 22.57% | 72.88% | 22.57% | 72.88% | 91.34% |
| catseg_native | all | 2.37 | 6.29 | 71.66% | 96.67% | 66.03% | 92.22% | 97.93% |
| catseg_native | boundary | 3.33 | 8.93 | 52.32% | 94.52% | 47.84% | 87.46% | 96.73% |
| catseg_native | interior | 2.24 | 5.95 | 74.31% | 96.97% | 68.55% | 92.87% | 98.08% |
| catseg_native | small_class | 7.83 | 28.92 | 27.52% | 81.64% | 23.02% | 66.73% | 86.07% |
| catseg_native | held_out | 4.09 | 15.62 | 53.22% | 91.78% | 44.33% | 84.48% | 94.37% |
| catseg_native | seen | 2.03 | 4.27 | 75.15% | 97.58% | 70.00% | 93.63% | 98.51% |
| catseg_native | name_in_coco | 2.09 | 4.02 | 74.57% | 97.25% | 70.52% | 93.82% | 98.60% |
| catseg_native | name_not_in_coco | 2.66 | 7.68 | 67.72% | 95.80% | 61.82% | 90.48% | 97.35% |
| catseg_anchored | all | 2.42 | 5.91 | 71.01% | 96.55% | 64.85% | 91.41% | 97.86% |
| catseg_anchored | boundary | 3.48 | 9.16 | 51.14% | 94.07% | 45.48% | 85.37% | 96.35% |
| catseg_anchored | interior | 2.27 | 5.47 | 73.75% | 96.90% | 67.54% | 92.27% | 98.05% |
| catseg_anchored | small_class | 7.93 | 26.92 | 28.12% | 81.30% | 23.26% | 65.24% | 85.81% |
| catseg_anchored | held_out | 4.17 | 12.48 | 54.31% | 91.50% | 45.27% | 84.03% | 94.32% |
| catseg_anchored | seen | 2.10 | 4.68 | 74.13% | 97.36% | 68.15% | 92.64% | 98.33% |
| catseg_anchored | name_in_coco | 2.12 | 4.37 | 74.19% | 97.23% | 68.63% | 92.94% | 98.47% |
| catseg_anchored | name_not_in_coco | 2.72 | 7.02 | 66.89% | 95.61% | 60.88% | 89.60% | 97.28% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.11 | 16.68% |
| catseg_native | 30.99 | 71.87% |
| catseg_anchored | 30.27 | 71.21% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.07, native_150_plus_845 0.95, anchored_reference_plus_845 2.82; peak memory 8.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.