# Ranking headroom probe, Pascal Context 59 -> 458 (declip_bank683)

2000 development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only. SCLIP rows are uninformative (no cached SCLIP features on this machine).

| Arm | Group | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 31.34 | 31.34 | 1.03% | 12.46% | 1.03% | 12.46% | 79.42% |
| sclip_cached | boundary | 30.05 | 30.05 | 1.72% | 14.25% | 1.72% | 14.25% | 80.11% |
| sclip_cached | interior | 31.51 | 31.51 | 0.99% | 12.22% | 0.99% | 12.22% | 79.30% |
| sclip_cached | small_class | 30.47 | 30.47 | 1.07% | 15.14% | 1.07% | 15.14% | 88.62% |
| sclip_cached | name_in_coco | 21.81 | 21.81 | 3.17% | 24.66% | 3.17% | 24.66% | 88.43% |
| sclip_cached | name_not_in_coco | 41.84 | 41.84 | 0.00% | 0.00% | 0.00% | 0.00% | 70.91% |
| catseg_native | all | 1.41 | 2.19 | 81.30% | 99.64% | 75.68% | 97.59% | 99.75% |
| catseg_native | boundary | 1.80 | 2.97 | 63.48% | 99.31% | 59.27% | 96.04% | 99.59% |
| catseg_native | interior | 1.37 | 2.10 | 83.15% | 99.68% | 77.38% | 97.76% | 99.77% |
| catseg_native | small_class | 2.73 | 7.16 | 46.83% | 96.49% | 43.24% | 87.87% | 97.33% |
| catseg_native | name_in_coco | 1.24 | 1.68 | 88.29% | 99.80% | 83.68% | 98.81% | 99.84% |
| catseg_native | name_not_in_coco | 1.73 | 3.05 | 69.30% | 99.20% | 62.06% | 95.68% | 99.52% |
| catseg_anchored | all | 1.43 | 2.27 | 80.49% | 99.63% | 74.87% | 97.40% | 99.73% |
| catseg_anchored | boundary | 1.85 | 3.14 | 61.58% | 99.29% | 57.85% | 95.58% | 99.55% |
| catseg_anchored | interior | 1.39 | 2.17 | 82.44% | 99.67% | 76.62% | 97.60% | 99.76% |
| catseg_anchored | small_class | 2.72 | 7.10 | 48.35% | 96.39% | 42.62% | 87.60% | 97.09% |
| catseg_anchored | name_in_coco | 1.24 | 1.71 | 88.21% | 99.81% | 83.47% | 98.72% | 99.83% |
| catseg_anchored | name_not_in_coco | 1.78 | 3.23 | 67.41% | 99.20% | 60.21% | 95.37% | 99.50% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.02 | 1.09% |
| catseg_native | 61.22 | 81.12% |
| catseg_anchored | 59.63 | 80.28% |

Seconds per image on NVIDIA GH200 480GB: clip_features 0.16, native_source_plus_full 0.74, anchored_reference_plus_full 2.10; peak memory 9.4 GB.

39 of 59 source prompts are exact COCO-Stuff names. Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number.