# Full-resolution mIoU, ade150 (150 classes), sed large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 34.90 | 73.82% | 0.27 |
| anchored_coco171 | 33.50 | 71.65% | 0.54 |
| anchored_bank683 | 34.01 | 73.15% | 1.36 |

Features 0.11 s/image on NVIDIA GH200 480GB; peak memory 6.8 GB. Development data; nothing fitted.