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
| catseg_native | all | 1.96 | 4.31 | 74.79% | 98.04% | 68.18% | 94.71% | 98.76% |
| catseg_native | boundary | 2.65 | 5.83 | 55.55% | 96.66% | 50.32% | 91.34% | 98.19% |
| catseg_native | interior | 1.87 | 4.12 | 77.42% | 98.22% | 70.63% | 95.16% | 98.83% |
| catseg_native | small_class | 5.57 | 16.26 | 33.81% | 88.29% | 27.89% | 77.98% | 92.11% |
| catseg_native | held_out | 2.84 | 7.64 | 59.88% | 95.69% | 48.75% | 90.14% | 97.16% |
| catseg_native | seen | 1.76 | 3.43 | 77.74% | 98.59% | 72.00% | 95.56% | 99.16% |
| catseg_native | name_in_coco | 1.73 | 2.92 | 77.01% | 98.65% | 70.70% | 96.15% | 99.38% |
| catseg_native | name_not_in_coco | 2.16 | 5.07 | 70.94% | 97.59% | 64.61% | 93.61% | 98.47% |
| catseg_anchored | all | 2.05 | 4.36 | 72.24% | 97.86% | 64.75% | 93.71% | 98.66% |
| catseg_anchored | boundary | 2.85 | 6.43 | 51.82% | 96.20% | 45.51% | 89.29% | 97.88% |
| catseg_anchored | interior | 1.94 | 4.10 | 75.06% | 98.09% | 67.40% | 94.31% | 98.75% |
| catseg_anchored | small_class | 5.35 | 15.85 | 40.99% | 88.21% | 34.24% | 78.49% | 92.44% |
| catseg_anchored | held_out | 2.85 | 7.08 | 61.90% | 95.43% | 50.75% | 89.76% | 97.11% |
| catseg_anchored | seen | 1.84 | 3.68 | 75.82% | 98.41% | 69.25% | 94.53% | 99.04% |
| catseg_anchored | name_in_coco | 1.72 | 3.03 | 77.25% | 98.65% | 70.22% | 95.78% | 99.33% |
| catseg_anchored | name_not_in_coco | 2.28 | 5.09 | 67.78% | 97.33% | 60.60% | 92.44% | 98.32% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.11 | 16.68% |
| catseg_native | 36.82 | 75.00% |
| catseg_anchored | 35.35 | 72.45% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.15, native_150_plus_845 0.95, anchored_reference_plus_845 1.93; peak memory 9.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.