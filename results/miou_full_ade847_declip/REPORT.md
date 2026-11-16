# Full-resolution mIoU, ade847 (847 classes), declip large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 17.87 | 66.34% | 0.29 |
| anchored_coco171 | 16.85 | 63.32% | 0.90 |
| anchored_bank683 | 16.86 | 65.40% | 1.31 |

Features 0.07 s/image on NVIDIA GH200 480GB; peak memory 9.5 GB. Development data; nothing fitted.