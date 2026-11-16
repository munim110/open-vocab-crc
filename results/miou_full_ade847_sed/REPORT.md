# Full-resolution mIoU, ade847 (847 classes), sed large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 13.66 | 61.71% | 1.16 |
| anchored_coco171 | 13.64 | 59.10% | 1.37 |
| anchored_bank683 | 13.67 | 60.77% | 2.05 |

Features 0.09 s/image on NVIDIA GH200 480GB; peak memory 8.3 GB. Development data; nothing fitted.