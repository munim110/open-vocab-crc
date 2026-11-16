# Ranking headroom probe, Pascal Context 59 -> 458 (vitl_bank683)

2000 development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 3.75 | 16.07 | 54.96% | 91.61% | 40.17% | 74.21% | 91.43% |
| sclip_cached | boundary | 6.33 | 31.98 | 35.53% | 82.33% | 24.45% | 57.14% | 81.38% |
| sclip_cached | interior | 3.49 | 14.43 | 56.86% | 92.58% | 41.70% | 75.96% | 92.47% |
| sclip_cached | small_class | 12.64 | 72.40 | 17.51% | 60.74% | 11.18% | 33.66% | 59.13% |
| sclip_cached | name_in_coco | 3.21 | 13.77 | 60.66% | 93.77% | 45.02% | 77.43% | 93.15% |
| sclip_cached | name_not_in_coco | 5.62 | 25.74 | 40.27% | 84.36% | 27.75% | 62.91% | 84.95% |
| catseg_native | all | 1.41 | 2.18 | 81.25% | 99.59% | 75.50% | 97.75% | 99.71% |
| catseg_native | boundary | 1.80 | 2.91 | 63.13% | 99.32% | 59.04% | 96.28% | 99.58% |
| catseg_native | interior | 1.37 | 2.09 | 83.14% | 99.63% | 77.22% | 97.92% | 99.73% |
| catseg_native | small_class | 3.00 | 8.47 | 42.44% | 95.58% | 37.45% | 85.59% | 96.60% |
| catseg_native | name_in_coco | 1.26 | 1.75 | 87.33% | 99.77% | 83.08% | 98.70% | 99.81% |
| catseg_native | name_not_in_coco | 1.69 | 2.87 | 69.81% | 99.28% | 61.95% | 96.16% | 99.57% |
| catseg_anchored | all | 1.43 | 2.24 | 80.40% | 99.59% | 74.74% | 97.57% | 99.70% |
| catseg_anchored | boundary | 1.84 | 3.02 | 61.23% | 99.30% | 57.74% | 95.88% | 99.56% |
| catseg_anchored | interior | 1.39 | 2.15 | 82.40% | 99.63% | 76.50% | 97.76% | 99.72% |
| catseg_anchored | small_class | 3.03 | 8.02 | 43.28% | 95.34% | 38.02% | 85.38% | 96.54% |
| catseg_anchored | name_in_coco | 1.26 | 1.79 | 87.19% | 99.77% | 82.81% | 98.58% | 99.80% |
| catseg_anchored | name_not_in_coco | 1.73 | 2.97 | 67.94% | 99.31% | 60.45% | 95.84% | 99.57% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 32.26 | 54.91% |
| catseg_native | 60.79 | 81.04% |
| catseg_anchored | 59.35 | 80.16% |

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.23, native_source_plus_full 1.01, anchored_reference_plus_full 3.08; peak memory 9.4 GB.

39 of 59 source prompts are exact COCO-Stuff names. Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number.