# Full-resolution mIoU, ade150 (150 classes), declip large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 40.59 | 76.95% | 0.55 |
| anchored_coco171 | 38.48 | 74.37% | 0.96 |
| anchored_bank683 | 39.72 | 76.25% | 2.34 |

Features 0.24 s/image on NVIDIA GH200 480GB; peak memory 9.1 GB. Development data; nothing fitted.