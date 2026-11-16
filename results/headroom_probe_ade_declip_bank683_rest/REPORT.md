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
| catseg_native | all | 1.97 | 4.52 | 75.50% | 98.02% | 69.96% | 94.61% | 98.75% |
| catseg_native | boundary | 2.60 | 5.91 | 56.81% | 96.70% | 52.22% | 91.58% | 98.15% |
| catseg_native | interior | 1.89 | 4.36 | 78.09% | 98.17% | 72.43% | 95.00% | 98.81% |
| catseg_native | small_class | 4.43 | 13.11 | 38.10% | 91.32% | 33.62% | 82.17% | 93.88% |
| catseg_native | held_out | 3.09 | 9.48 | 58.85% | 95.08% | 48.67% | 88.98% | 96.70% |
| catseg_native | seen | 1.66 | 2.97 | 79.57% | 98.79% | 74.61% | 96.10% | 99.30% |
| catseg_native | name_in_coco | 1.59 | 2.58 | 78.99% | 99.06% | 74.03% | 96.74% | 99.49% |
| catseg_native | name_not_in_coco | 2.21 | 5.33 | 71.45% | 97.40% | 66.13% | 93.24% | 98.43% |
| catseg_anchored | all | 2.00 | 4.44 | 74.87% | 97.93% | 68.73% | 94.01% | 98.63% |
| catseg_anchored | boundary | 2.72 | 6.41 | 55.48% | 96.42% | 49.54% | 90.09% | 97.83% |
| catseg_anchored | interior | 1.91 | 4.19 | 77.56% | 98.11% | 71.41% | 94.56% | 98.72% |
| catseg_anchored | small_class | 4.53 | 13.09 | 38.71% | 90.78% | 33.34% | 80.72% | 93.68% |
| catseg_anchored | held_out | 3.14 | 8.46 | 60.04% | 94.72% | 49.96% | 88.46% | 96.58% |
| catseg_anchored | seen | 1.71 | 3.34 | 78.42% | 98.71% | 72.52% | 95.40% | 99.15% |
| catseg_anchored | name_in_coco | 1.60 | 2.75 | 78.96% | 99.10% | 72.71% | 96.39% | 99.44% |
| catseg_anchored | name_not_in_coco | 2.26 | 5.31 | 70.66% | 97.23% | 65.13% | 92.47% | 98.25% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.11 | 16.68% |
| catseg_native | 39.64 | 75.64% |
| catseg_anchored | 38.94 | 75.00% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.21, native_150_plus_845 1.32, anchored_reference_plus_845 3.87, native_150 0.47, native_845 0.85; peak memory 9.4 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.