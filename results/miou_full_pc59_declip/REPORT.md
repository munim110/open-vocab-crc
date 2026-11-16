# Full-resolution mIoU, pc59 (59 classes), declip large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 62.79 | 81.89% | 0.09 |
| anchored_coco171 | 60.12 | 80.42% | 0.21 |
| anchored_bank683 | 61.09 | 81.08% | 0.66 |

Features 0.07 s/image on NVIDIA GH200 480GB; peak memory 9.0 GB. Development data; nothing fitted.