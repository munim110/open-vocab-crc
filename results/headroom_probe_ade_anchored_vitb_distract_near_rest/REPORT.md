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
| catseg_native | all | 2.61 | 6.52 | 69.73% | 96.13% | 64.36% | 92.09% | 97.80% |
| catseg_native | boundary | 3.66 | 9.09 | 49.20% | 93.79% | 45.16% | 87.45% | 96.73% |
| catseg_native | interior | 2.47 | 6.20 | 72.56% | 96.46% | 67.03% | 92.74% | 97.92% |
| catseg_native | small_class | 8.20 | 27.95 | 28.74% | 80.58% | 23.95% | 67.87% | 87.07% |
| catseg_native | held_out | 5.11 | 17.38 | 53.26% | 89.14% | 44.48% | 83.20% | 92.87% |
| catseg_native | seen | 2.08 | 4.09 | 73.08% | 97.60% | 67.97% | 93.85% | 98.74% |
| catseg_native | name_in_coco | 1.97 | 3.48 | 76.06% | 97.56% | 71.70% | 94.72% | 99.01% |
| catseg_native | name_not_in_coco | 3.04 | 8.18 | 64.41% | 94.85% | 59.13% | 90.05% | 97.01% |
| catseg_anchored | all | 2.67 | 6.20 | 69.14% | 95.99% | 66.03% | 91.50% | 97.77% |
| catseg_anchored | boundary | 3.76 | 9.12 | 48.24% | 93.48% | 45.58% | 86.52% | 96.60% |
| catseg_anchored | interior | 2.53 | 5.83 | 72.00% | 96.35% | 68.85% | 92.19% | 97.90% |
| catseg_anchored | small_class | 8.33 | 25.52 | 27.24% | 80.54% | 24.21% | 68.24% | 87.39% |
| catseg_anchored | held_out | 5.32 | 15.99 | 53.59% | 88.60% | 45.61% | 82.44% | 92.66% |
| catseg_anchored | seen | 2.13 | 4.09 | 72.04% | 97.48% | 69.08% | 93.34% | 98.75% |
| catseg_anchored | name_in_coco | 1.93 | 3.28 | 77.74% | 97.69% | 75.33% | 94.89% | 99.05% |
| catseg_anchored | name_not_in_coco | 3.15 | 7.80 | 62.79% | 94.57% | 59.70% | 89.06% | 96.93% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.11 | 16.68% |
| catseg_native | 28.78 | 69.87% |
| catseg_anchored | 26.12 | 69.28% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.03, native_150_plus_845 0.43, anchored_reference_plus_845 0.88; peak memory 8.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.