# Ranking headroom probe, Pascal Context 59 -> 458 (sed_bank683)

2000 development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 3.75 | 16.07 | 54.96% | 91.61% | 40.17% | 74.21% | 91.43% |
| sclip_cached | boundary | 6.33 | 31.98 | 35.53% | 82.33% | 24.45% | 57.14% | 81.38% |
| sclip_cached | interior | 3.49 | 14.43 | 56.86% | 92.58% | 41.70% | 75.96% | 92.47% |
| sclip_cached | small_class | 12.64 | 72.40 | 17.51% | 60.74% | 11.18% | 33.66% | 59.13% |
| sclip_cached | name_in_coco | 3.21 | 13.77 | 60.66% | 93.77% | 45.02% | 77.43% | 93.15% |
| sclip_cached | name_not_in_coco | 5.62 | 25.74 | 40.27% | 84.36% | 27.75% | 62.91% | 84.95% |
| catseg_native | all | 1.51 | 2.33 | 79.72% | 99.40% | 73.88% | 97.16% | 99.67% |
| catseg_native | boundary | 1.95 | 3.35 | 61.32% | 98.94% | 56.82% | 94.69% | 99.45% |
| catseg_native | interior | 1.47 | 2.22 | 81.64% | 99.46% | 75.67% | 97.43% | 99.70% |
| catseg_native | small_class | 3.88 | 11.36 | 39.67% | 92.56% | 33.80% | 79.16% | 95.09% |
| catseg_native | name_in_coco | 1.30 | 1.85 | 86.84% | 99.72% | 81.61% | 98.23% | 99.82% |
| catseg_native | name_not_in_coco | 1.91 | 3.29 | 66.78% | 98.85% | 59.53% | 94.87% | 99.44% |
| catseg_anchored | all | 1.52 | 2.39 | 79.01% | 99.42% | 73.34% | 97.00% | 99.65% |
| catseg_anchored | boundary | 1.97 | 3.43 | 59.84% | 98.95% | 55.88% | 94.49% | 99.44% |
| catseg_anchored | interior | 1.47 | 2.27 | 81.01% | 99.48% | 75.18% | 97.26% | 99.68% |
| catseg_anchored | small_class | 3.87 | 11.62 | 38.45% | 92.56% | 34.09% | 78.90% | 94.95% |
| catseg_anchored | name_in_coco | 1.31 | 1.87 | 86.09% | 99.71% | 81.82% | 98.16% | 99.81% |
| catseg_anchored | name_not_in_coco | 1.91 | 3.40 | 65.70% | 98.89% | 58.11% | 94.57% | 99.40% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 32.26 | 54.91% |
| catseg_native | 58.20 | 79.55% |
| catseg_anchored | 56.89 | 78.83% |

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.09, native_source_plus_full 0.40, anchored_reference_plus_full 0.85; peak memory 6.9 GB.

39 of 59 source prompts are exact COCO-Stuff names. Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number.