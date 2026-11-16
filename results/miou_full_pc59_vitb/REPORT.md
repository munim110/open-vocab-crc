# Full-resolution mIoU, pc59 (59 classes), catseg base

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 56.41 | 79.44% | 0.20 |
| anchored_coco171 | 54.30 | 77.78% | 0.44 |
| anchored_bank683 | 55.04 | 78.62% | 1.32 |

Features 0.07 s/image on NVIDIA GH200 480GB; peak memory 8.0 GB. Development data; nothing fitted.