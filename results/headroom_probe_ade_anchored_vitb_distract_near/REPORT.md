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
| catseg_native | all | 2.45 | 5.70 | 70.15% | 96.51% | 64.23% | 92.32% | 98.07% |
| catseg_native | boundary | 3.48 | 8.33 | 49.28% | 94.35% | 44.61% | 87.76% | 97.21% |
| catseg_native | interior | 2.32 | 5.36 | 73.05% | 96.77% | 66.99% | 92.93% | 98.16% |
| catseg_native | small_class | 7.44 | 25.39 | 29.30% | 83.99% | 25.03% | 73.72% | 89.84% |
| catseg_native | held_out | 4.49 | 13.58 | 53.17% | 90.24% | 41.56% | 81.77% | 93.94% |
| catseg_native | seen | 2.15 | 4.41 | 72.61% | 97.41% | 67.34% | 93.80% | 98.68% |
| catseg_native | name_in_coco | 1.97 | 3.54 | 75.78% | 98.04% | 71.58% | 94.46% | 99.06% |
| catseg_native | name_not_in_coco | 2.93 | 7.45 | 63.39% | 95.39% | 57.41% | 90.24% | 97.35% |
| catseg_anchored | all | 2.55 | 5.52 | 69.56% | 96.27% | 66.08% | 91.66% | 98.00% |
| catseg_anchored | boundary | 3.60 | 8.33 | 48.16% | 93.96% | 45.26% | 86.80% | 96.96% |
| catseg_anchored | interior | 2.41 | 5.16 | 72.52% | 96.56% | 69.00% | 92.30% | 98.11% |
| catseg_anchored | small_class | 7.59 | 22.77 | 26.78% | 84.15% | 24.17% | 72.53% | 89.89% |
| catseg_anchored | held_out | 4.71 | 12.90 | 52.62% | 89.35% | 42.19% | 80.15% | 93.69% |
| catseg_anchored | seen | 2.24 | 4.37 | 71.65% | 97.26% | 68.62% | 93.26% | 98.64% |
| catseg_anchored | name_in_coco | 1.91 | 3.36 | 76.89% | 98.17% | 74.51% | 94.57% | 99.23% |
| catseg_anchored | name_not_in_coco | 3.08 | 7.23 | 62.07% | 95.03% | 58.55% | 89.29% | 97.24% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.12 | 17.71% |
| catseg_native | 28.92 | 70.58% |
| catseg_anchored | 25.72 | 69.96% |

Sampled-pixel mIoU over a 400-image subset is a fidelity ballpark, not a reproduction of published full-validation mIoU.

Seconds per image on NVIDIA GH200 480GB: clip_features 0.03, native_150_plus_845 0.43, anchored_reference_plus_845 0.88; peak memory 8.2 GB.

Native CAT-Seg is candidate-dependent (class attention across the deployed vocabulary; per-crop top-256 truncation above 256 labels). The anchored arm is candidate-independent by construction; tests/check_catseg_anchor.py verifies it.