# Ranking headroom probe, COCO-Stuff 171 -> 1283 with LVIS (vitb_bank683)

2000 development images, image-averaged conditional metrics at the sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +1112 | Source top1 | Source top10 | +1112 top1 | +1112 top10 | +1112 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_native | all | 2.02 | 3.67 | 72.46% | 97.89% | 68.14% | 95.65% | 99.22% |
| catseg_native | boundary | 2.81 | 5.52 | 53.25% | 96.14% | 49.41% | 91.69% | 98.67% |
| catseg_native | interior | 1.92 | 3.42 | 74.87% | 98.13% | 70.47% | 96.17% | 99.29% |
| catseg_native | small_class | 5.06 | 15.90 | 29.36% | 88.75% | 22.71% | 74.12% | 94.05% |
| catseg_native | thing | 1.43 | 2.45 | 85.38% | 99.23% | 75.99% | 97.52% | 99.63% |
| catseg_native | stuff | 2.55 | 5.18 | 61.38% | 96.57% | 59.22% | 92.98% | 98.73% |
| catseg_anchored | all | 2.02 | 3.53 | 72.10% | 97.91% | 67.21% | 95.31% | 99.17% |
| catseg_anchored | boundary | 2.87 | 5.68 | 52.59% | 96.02% | 47.80% | 90.51% | 98.53% |
| catseg_anchored | interior | 1.91 | 3.25 | 74.56% | 98.18% | 69.63% | 95.94% | 99.25% |
| catseg_anchored | small_class | 5.26 | 14.50 | 29.04% | 88.19% | 23.71% | 73.81% | 94.01% |
| catseg_anchored | thing | 1.48 | 2.51 | 84.54% | 99.11% | 74.45% | 97.24% | 99.61% |
| catseg_anchored | stuff | 2.53 | 4.81 | 61.37% | 96.64% | 59.17% | 92.51% | 98.64% |

| Arm | Sampled-pixel mIoU (171) | Pixel accuracy |
|---|---:|---:|
| catseg_native | 47.11 | 72.58% |
| catseg_anchored | 47.02 | 72.22% |

Seconds per image on NVIDIA GH200 480GB: clip_features 0.04, native_source_plus_full 0.67, anchored_reference_plus_full 2.32; peak memory 8.4 GB.

Sampled-pixel mIoU is a fidelity ballpark, not a benchmark number.