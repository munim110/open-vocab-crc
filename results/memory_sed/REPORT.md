# Peak GPU memory per arm, sed

3 development images, NVIDIA GeForce RTX 5070 Ti, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.

Weights 1.32 GiB; image features peak 1.82 GiB.

| Arm | V=150 | V=845 | V=1,690 | V=3,380 | V=6,760 |
|---|---:|---:|---:|---:|---:|
| native | 3.55 | 8.01 | 14.47 | 27.39 | OOM |
| anchored | 6.62 | 6.62 | 6.62 | 6.62 | 6.62 |
| anchored_lean | 4.65 | 4.65 | 4.65 | 4.68 | 5.91 |

Bank text embeddings: 160.1 MiB (683 names). Labelled calibration images: 43 KiB per image, 42 MiB for n_cal = 1000.
