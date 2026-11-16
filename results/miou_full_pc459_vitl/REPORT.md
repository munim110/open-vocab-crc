# Full-resolution mIoU, pc459 (459 classes), catseg large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 23.74 | 72.12% | 0.85 |
| anchored_coco171 | 23.10 | 70.57% | 1.82 |
| anchored_bank683 | 23.17 | 71.41% | 3.13 |

Features 0.23 s/image on NVIDIA GH200 480GB; peak memory 9.4 GB. Development data; nothing fitted.