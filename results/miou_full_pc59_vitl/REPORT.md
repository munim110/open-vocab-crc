# Full-resolution mIoU, pc59 (59 classes), catseg large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 61.96 | 81.83% | 0.19 |
| anchored_coco171 | 60.07 | 80.45% | 0.41 |
| anchored_bank683 | 60.41 | 80.95% | 1.25 |

Features 0.14 s/image on NVIDIA GH200 480GB; peak memory 9.0 GB. Development data; nothing fitted.