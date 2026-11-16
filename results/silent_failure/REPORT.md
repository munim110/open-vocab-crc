# Silent failure: set size of the reused native threshold against the size needed

cal1000_a0.1. Source: native threshold calibrated and applied at the source vocabulary. Reused: the same threshold at the grown vocabulary. Needed: native recalibrated at the grown vocabulary (risk at the target). Share = (reused - source)/(needed - source): the part of the needed growth that the reused sets show. Anchored growth: anchored size at the grown vocabulary over its size at the source vocabulary.

| Benchmark | Model | risk source -> reused (%) | size source | reused | needed | share | reused growth | anchored growth |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ade | CAT-Seg ViT-B | 9.9 -> 15.4 | 2.31 | 2.73 | 4.99 | 0.16 | 1.18x | 2.17x |
| ade | CAT-Seg ViT-L | 9.9 -> 15.2 | 1.91 | 2.16 | 3.47 | 0.16 | 1.13x | 1.90x |
| ade | CAT-Seg + DeCLIP | 9.9 -> 14.7 | 1.84 | 2.17 | 3.39 | 0.21 | 1.18x | 2.01x |
| ade | SED | 9.9 -> 7.1 | 2.22 | 8.80 | 5.28 | 2.15 | 3.96x | 2.19x |
| ade | FC-CLIP | 9.8 -> 13.8 | 3.22 | 5.19 | 8.18 | 0.40 | 1.61x | 2.94x |
| pascal | CAT-Seg ViT-B | 9.9 -> 15.2 | 1.49 | 1.63 | 2.52 | 0.14 | 1.10x | 1.69x |
| pascal | CAT-Seg ViT-L | 9.8 -> 15.0 | 1.37 | 1.49 | 2.07 | 0.17 | 1.09x | 1.54x |
| pascal | CAT-Seg + DeCLIP | 9.9 -> 14.7 | 1.37 | 1.50 | 2.09 | 0.18 | 1.09x | 1.60x |
| pascal | SED | 9.8 -> 4.6 | 1.53 | 4.80 | 2.68 | 2.85 | 3.14x | 1.68x |
| pascal | FC-CLIP | 9.9 -> 16.2 | 1.95 | 2.82 | 5.30 | 0.26 | 1.45x | 2.88x |
| coco | CAT-Seg ViT-B | 9.9 -> 12.9 | 2.15 | 2.39 | 3.11 | 0.25 | 1.11x | 1.65x |
| coco | CAT-Seg ViT-L | 9.8 -> 12.8 | 1.95 | 2.13 | 2.66 | 0.26 | 1.09x | 1.56x |
| coco | CAT-Seg + DeCLIP | 9.8 -> 12.9 | 1.85 | 2.08 | 2.64 | 0.29 | 1.12x | 1.64x |
| coco | SED | 9.9 -> 3.6 | 2.01 | 8.21 | 3.74 | 3.58 | 4.09x | 1.62x |
| coco | FC-CLIP | 9.9 -> 17.1 | 5.98 | 9.71 | 26.50 | 0.18 | 1.62x | 4.58x |

Reused threshold above the target in 12 of 15 combinations. There the reused sets show 0.14-0.40 of the needed growth (sizes x1.09-x1.62), while the valid anchored sets grow x1.54-x4.58; anchored grows more in every one: True. Where the reused threshold is over-conservative (SED), its sets grow 2.15-3.58 times the needed growth.
