# Ranking headroom probe, Pascal Context 59 -> 458

2000 development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 3.75 | 16.07 | 54.96% | 91.61% | 40.17% | 74.21% | 91.43% |
| sclip_cached | boundary | 6.33 | 31.98 | 35.53% | 82.33% | 24.45% | 57.14% | 81.38% |
| sclip_cached | interior | 3.49 | 14.43 | 56.86% | 92.58% | 41.70% | 75.96% | 92.47% |
| sclip_cached | small_class | 12.64 | 72.40 | 17.51% | 60.74% | 11.18% | 33.66% | 59.13% |
| sclip_cached | name_in_coco | 3.21 | 13.77 | 60.66% | 93.77% | 45.02% | 77.43% | 93.15% |
| sclip_cached | name_not_in_coco | 5.62 | 25.74 | 40.27% | 84.36% | 27.75% | 62.91% | 84.95% |
| catseg_native | all | 1.53 | 2.69 | 79.45% | 99.29% | 73.74% | 96.64% | 99.48% |
| catseg_native | boundary | 1.98 | 3.71 | 60.85% | 98.76% | 56.43% | 94.33% | 99.19% |
| catseg_native | interior | 1.48 | 2.57 | 81.39% | 99.34% | 75.53% | 96.89% | 99.51% |
| catseg_native | small_class | 3.57 | 11.58 | 36.40% | 93.98% | 32.08% | 78.87% | 94.96% |
| catseg_native | name_in_coco | 1.33 | 2.06 | 85.60% | 99.67% | 81.49% | 98.07% | 99.70% |
| catseg_native | name_not_in_coco | 1.87 | 3.66 | 67.41% | 98.73% | 59.42% | 94.15% | 99.25% |
| catseg_anchored | all | 1.58 | 2.94 | 77.82% | 99.18% | 71.59% | 95.99% | 99.35% |
| catseg_anchored | boundary | 2.09 | 4.22 | 57.08% | 98.57% | 52.66% | 92.99% | 98.98% |
| catseg_anchored | interior | 1.53 | 2.80 | 79.96% | 99.25% | 73.53% | 96.32% | 99.39% |
| catseg_anchored | small_class | 3.48 | 11.16 | 40.14% | 94.23% | 33.94% | 78.85% | 94.98% |
| catseg_anchored | name_in_coco | 1.32 | 2.13 | 86.04% | 99.66% | 80.99% | 97.88% | 99.68% |
| catseg_anchored | name_not_in_coco | 1.99 | 4.15 | 63.63% | 98.54% | 55.78% | 92.93% | 98.98% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 32.26 | 54.91% |
| catseg_native | 56.17 | 79.28% |
| catseg_anchored | 54.09 | 77.64% |

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.07, native_source_plus_full 1.01, anchored_reference_plus_full 1.69; peak memory 8.1 GB.

39 of 59 source prompts are exact COCO-Stuff names. Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number.