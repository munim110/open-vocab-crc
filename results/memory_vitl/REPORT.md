# Peak GPU memory per arm, vitl

3 development images, NVIDIA GeForce RTX 5070 Ti, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.

Weights 1.62 GiB; image features peak 1.90 GiB.

| Arm | V=150 | V=845 | V=1,690 | V=3,380 | V=6,760 |
|---|---:|---:|---:|---:|---:|
| native | 6.04 | 9.10 | 9.10 | 9.11 | 9.12 |
| anchored | 8.49 | 8.49 | 8.49 | 8.49 | 8.49 |
| anchored_lean | 8.44 | 8.44 | 8.44 | 8.44 | 8.44 |
| native_released | 6.05 | 9.11 | 9.11 | 9.12 | 9.13 |

Bank text embeddings: 2.0 MiB (683 names). Labelled calibration images: 43 KiB per image, 42 MiB for n_cal = 1000.
