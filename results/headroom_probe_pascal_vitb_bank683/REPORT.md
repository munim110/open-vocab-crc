# Ranking headroom probe, Pascal Context 59 -> 458 (vitb_bank683)

2000 development images, image-averaged conditional metrics at the cached sampled pixels. Ranking diagnostic only. SCLIP rows are uninformative (no cached SCLIP features on this machine).

| Arm | Group | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_cached | all | 31.34 | 31.34 | 1.03% | 12.46% | 1.03% | 12.46% | 79.42% |
| sclip_cached | boundary | 30.05 | 30.05 | 1.72% | 14.25% | 1.72% | 14.25% | 80.11% |
| sclip_cached | interior | 31.51 | 31.51 | 0.99% | 12.22% | 0.99% | 12.22% | 79.30% |
| sclip_cached | small_class | 30.47 | 30.47 | 1.07% | 15.14% | 1.07% | 15.14% | 88.62% |
| sclip_cached | name_in_coco | 21.81 | 21.81 | 3.17% | 24.66% | 3.17% | 24.66% | 88.43% |
| sclip_cached | name_not_in_coco | 41.84 | 41.84 | 0.00% | 0.00% | 0.00% | 0.00% | 70.91% |
| catseg_native | all | 1.53 | 2.69 | 79.45% | 99.29% | 73.74% | 96.64% | 99.48% |
| catseg_native | boundary | 1.98 | 3.71 | 60.85% | 98.76% | 56.43% | 94.33% | 99.19% |
| catseg_native | interior | 1.48 | 2.57 | 81.39% | 99.34% | 75.53% | 96.89% | 99.51% |
| catseg_native | small_class | 3.57 | 11.58 | 36.40% | 93.98% | 32.08% | 78.87% | 94.96% |
| catseg_native | name_in_coco | 1.33 | 2.06 | 85.60% | 99.67% | 81.49% | 98.07% | 99.70% |
| catseg_native | name_not_in_coco | 1.87 | 3.66 | 67.41% | 98.73% | 59.42% | 94.15% | 99.25% |
| catseg_anchored | all | 1.55 | 2.80 | 78.63% | 99.22% | 72.96% | 96.31% | 99.42% |
| catseg_anchored | boundary | 2.03 | 3.92 | 58.67% | 98.68% | 54.98% | 93.74% | 99.12% |
| catseg_anchored | interior | 1.50 | 2.68 | 80.69% | 99.28% | 74.80% | 96.60% | 99.46% |
| catseg_anchored | small_class | 3.62 | 11.49 | 37.29% | 93.65% | 32.54% | 78.30% | 94.94% |
| catseg_anchored | name_in_coco | 1.33 | 2.12 | 85.68% | 99.65% | 81.43% | 97.88% | 99.69% |
| catseg_anchored | name_not_in_coco | 1.92 | 3.84 | 65.34% | 98.64% | 57.74% | 93.64% | 99.13% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| sclip_cached | 0.02 | 1.09% |
| catseg_native | 56.17 | 79.28% |
| catseg_anchored | 55.04 | 78.45% |

Seconds per image on NVIDIA GH200 480GB: clip_features 0.06, native_source_plus_full 0.57, anchored_reference_plus_full 1.63; peak memory 8.3 GB.

39 of 59 source prompts are exact COCO-Stuff names. Sampled-pixel mIoU is a fidelity ballpark, not the published benchmark number.