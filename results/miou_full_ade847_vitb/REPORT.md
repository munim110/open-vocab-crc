# Full-resolution mIoU, ade847 (847 classes), catseg base

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 12.17 | 62.11% | 0.67 |
| anchored_coco171 | 11.57 | 59.02% | 2.00 |
| anchored_bank683 | 11.90 | 60.81% | 2.90 |

Features 0.07 s/image on NVIDIA GH200 480GB; peak memory 8.5 GB. Development data; nothing fitted.