# Full-resolution mIoU, pc59 (59 classes), sed large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 59.14 | 80.14% | 0.10 |
| anchored_coco171 | 57.49 | 78.98% | 0.33 |
| anchored_bank683 | 57.81 | 79.29% | 1.01 |

Features 0.09 s/image on NVIDIA GH200 480GB; peak memory 6.7 GB. Development data; nothing fitted.