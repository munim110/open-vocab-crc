# Full-resolution mIoU, ade847 (847 classes), catseg large

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 15.93 | 64.27% | 0.67 |
| anchored_coco171 | 15.37 | 60.89% | 2.00 |
| anchored_bank683 | 15.18 | 62.96% | 2.90 |

Features 0.15 s/image on NVIDIA GH200 480GB; peak memory 9.5 GB. Development data; nothing fitted.