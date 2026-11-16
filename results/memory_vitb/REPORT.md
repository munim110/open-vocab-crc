# Peak GPU memory per arm, vitb

3 development images, NVIDIA GeForce RTX 5070 Ti, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.

Weights 0.58 GiB; image features peak 0.79 GiB.

| Arm | V=150 | V=845 | V=1,690 | V=3,380 | V=6,760 |
|---|---:|---:|---:|---:|---:|
| native | 4.99 | 8.05 | 8.05 | 8.05 | 8.06 |
| anchored | 7.44 | 7.44 | 7.44 | 7.44 | 7.44 |
| anchored_lean | 7.39 | 7.39 | 7.39 | 7.39 | 7.39 |
| native_released | 5.00 | 8.06 | 8.06 | 8.06 | 8.07 |

Bank text embeddings: 1.3 MiB (683 names). Labelled calibration images: 43 KiB per image, 42 MiB for n_cal = 1000.
