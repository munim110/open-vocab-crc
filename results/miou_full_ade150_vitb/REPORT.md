# Full-resolution mIoU, ade150 (150 classes), catseg base

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 31.71 | 72.86% | 0.63 |
| anchored_coco171 | 30.42 | 70.38% | 1.11 |
| anchored_bank683 | 31.01 | 72.13% | 2.69 |

Features 0.14 s/image on NVIDIA GH200 480GB; peak memory 8.0 GB. Development data; nothing fitted.