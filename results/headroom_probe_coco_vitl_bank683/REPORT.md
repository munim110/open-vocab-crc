# Ranking headroom probe, COCO-Stuff 171 -> 1283 with LVIS (vitl_bank683)

2000 development images, image-averaged conditional metrics at the sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +1112 | Source top1 | Source top10 | +1112 top1 | +1112 top10 | +1112 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_native | all | 1.85 | 2.99 | 73.93% | 98.40% | 69.54% | 96.57% | 99.48% |
| catseg_native | boundary | 2.52 | 4.53 | 55.28% | 97.14% | 51.34% | 93.39% | 99.13% |
| catseg_native | interior | 1.76 | 2.79 | 76.29% | 98.58% | 71.82% | 96.99% | 99.53% |
| catseg_native | small_class | 4.09 | 11.16 | 34.14% | 92.57% | 25.30% | 79.68% | 96.69% |
| catseg_native | thing | 1.30 | 1.91 | 87.89% | 99.54% | 78.07% | 98.45% | 99.82% |
| catseg_native | stuff | 2.31 | 4.24 | 63.12% | 97.47% | 60.88% | 94.39% | 99.14% |
| catseg_anchored | all | 1.86 | 2.90 | 73.50% | 98.41% | 68.52% | 96.37% | 99.46% |
| catseg_anchored | boundary | 2.57 | 4.53 | 54.59% | 97.03% | 49.58% | 92.57% | 99.06% |
| catseg_anchored | interior | 1.76 | 2.69 | 75.89% | 98.60% | 70.88% | 96.86% | 99.52% |
| catseg_anchored | small_class | 4.16 | 9.74 | 33.92% | 92.18% | 26.92% | 80.70% | 96.68% |
| catseg_anchored | thing | 1.34 | 2.01 | 86.94% | 99.45% | 76.39% | 98.25% | 99.80% |
| catseg_anchored | stuff | 2.30 | 3.93 | 63.14% | 97.51% | 60.89% | 94.14% | 99.10% |

| Arm | Sampled-pixel mIoU (171) | Pixel accuracy |
|---|---:|---:|
| catseg_native | 50.16 | 74.00% |
| catseg_anchored | 50.01 | 73.57% |

Seconds per image on NVIDIA GeForce RTX 5070 Ti: clip_features 0.23, native_source_plus_full 1.33, anchored_reference_plus_full 5.25; peak memory 9.4 GB.

Sampled-pixel mIoU is a fidelity ballpark, not a benchmark number.