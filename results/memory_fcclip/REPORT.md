# Peak GPU memory per arm, fcclip

3 development images, NVIDIA GeForce RTX 5070 Ti, fp32. Peak = max over images of max_memory_allocated (GiB), reset before each arm.

Weights 1.39 GiB; bank 701 classes.

| Arm | V=150 | V=845 | V=1,690 | V=3,380 | V=6,760 |
|---|---:|---:|---:|---:|---:|
| native | 2.59 | 2.60 | 2.61 | 2.63 | 2.67 |
| anchored | 2.60 | 2.61 | 2.62 | 2.64 | 2.67 |
