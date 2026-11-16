# Full-resolution mIoU, ade150 (150 classes), catseg large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 37.81 | 76.09% | 0.63 |
| anchored_coco171 | 36.06 | 73.37% | 1.11 |
| anchored_bank683 | 36.84 | 75.33% | 2.70 |

Features 0.27 s/image on NVIDIA GH200 480GB; peak memory 9.1 GB. Development data; nothing fitted.