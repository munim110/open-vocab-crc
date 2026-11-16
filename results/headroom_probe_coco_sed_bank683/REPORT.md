# Ranking headroom probe, COCO-Stuff 171 -> 1283 with LVIS (sed_bank683)

2000 development images, image-averaged conditional metrics at the sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +1112 | Source top1 | Source top10 | +1112 top1 | +1112 top10 | +1112 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_native | all | 1.89 | 3.07 | 73.72% | 98.33% | 63.34% | 96.04% | 99.44% |
| catseg_native | boundary | 2.60 | 5.00 | 54.85% | 96.82% | 44.87% | 91.61% | 98.93% |
| catseg_native | interior | 1.79 | 2.82 | 76.09% | 98.54% | 65.66% | 96.62% | 99.51% |
| catseg_native | small_class | 4.99 | 14.75 | 31.39% | 90.32% | 23.73% | 73.70% | 94.82% |
| catseg_native | thing | 1.33 | 2.36 | 87.83% | 99.51% | 68.41% | 97.86% | 99.73% |
| catseg_native | stuff | 2.41 | 4.19 | 61.88% | 97.18% | 57.52% | 93.28% | 99.04% |
| catseg_anchored | all | 1.90 | 3.08 | 73.21% | 98.34% | 65.70% | 95.96% | 99.43% |
| catseg_anchored | boundary | 2.67 | 4.93 | 53.78% | 96.70% | 47.17% | 91.63% | 98.94% |
| catseg_anchored | interior | 1.79 | 2.84 | 75.64% | 98.57% | 68.02% | 96.52% | 99.50% |
| catseg_anchored | small_class | 5.21 | 14.52 | 30.71% | 89.43% | 23.35% | 74.32% | 94.85% |
| catseg_anchored | thing | 1.39 | 2.27 | 86.39% | 99.39% | 69.97% | 97.95% | 99.75% |
| catseg_anchored | stuff | 2.39 | 4.24 | 62.13% | 97.23% | 59.16% | 93.09% | 99.04% |

| Arm | Sampled-pixel mIoU (171) | Pixel accuracy |
|---|---:|---:|
| catseg_native | 49.35 | 73.84% |
| catseg_anchored | 49.05 | 73.34% |

Seconds per image on NVIDIA GH200 480GB: clip_features 0.09, native_source_plus_full 1.96, anchored_reference_plus_full 2.62; peak memory 11.6 GB.

Sampled-pixel mIoU is a fidelity ballpark, not a benchmark number.