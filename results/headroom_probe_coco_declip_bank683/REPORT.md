# Ranking headroom probe, COCO-Stuff 171 -> 1283 with LVIS (declip_bank683)

2000 development images, image-averaged conditional metrics at the sampled pixels. Ranking diagnostic only.

| Arm | Group | Source rank | Rank at +1112 | Source top1 | Source top10 | +1112 top1 | +1112 top10 | +1112 top50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_native | all | 1.78 | 3.14 | 74.87% | 98.59% | 70.60% | 96.67% | 99.49% |
| catseg_native | boundary | 2.42 | 4.45 | 56.23% | 97.48% | 52.63% | 93.70% | 99.17% |
| catseg_native | interior | 1.70 | 2.97 | 77.23% | 98.74% | 72.88% | 97.06% | 99.52% |
| catseg_native | small_class | 3.73 | 10.06 | 36.44% | 94.06% | 29.21% | 82.12% | 97.38% |
| catseg_native | thing | 1.25 | 1.82 | 89.04% | 99.69% | 80.87% | 98.68% | 99.80% |
| catseg_native | stuff | 2.22 | 4.36 | 63.83% | 97.67% | 61.35% | 94.44% | 99.13% |
| catseg_anchored | all | 1.79 | 2.90 | 74.66% | 98.61% | 69.68% | 96.49% | 99.48% |
| catseg_anchored | boundary | 2.46 | 4.50 | 55.85% | 97.43% | 51.23% | 92.84% | 99.08% |
| catseg_anchored | interior | 1.70 | 2.69 | 77.05% | 98.77% | 72.02% | 96.97% | 99.53% |
| catseg_anchored | small_class | 3.79 | 9.84 | 36.60% | 93.77% | 30.01% | 82.07% | 97.03% |
| catseg_anchored | thing | 1.28 | 1.91 | 88.32% | 99.64% | 78.69% | 98.49% | 99.79% |
| catseg_anchored | stuff | 2.22 | 3.94 | 64.15% | 97.71% | 61.65% | 94.10% | 99.11% |

| Arm | Sampled-pixel mIoU (171) | Pixel accuracy |
|---|---:|---:|
| catseg_native | 51.73 | 74.94% |
| catseg_anchored | 51.68 | 74.74% |

Seconds per image on NVIDIA GH200 480GB: clip_features 0.21, native_source_plus_full 1.50, anchored_reference_plus_full 5.07; peak memory 9.4 GB.

Sampled-pixel mIoU is a fidelity ballpark, not a benchmark number.