# Full-resolution mIoU, pc459 (459 classes), catseg base

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 19.01 | 69.39% | 0.86 |
| anchored_coco171 | 18.37 | 67.64% | 1.84 |
| anchored_bank683 | 18.73 | 68.84% | 3.16 |

Features 0.11 s/image on NVIDIA GH200 480GB; peak memory 8.4 GB. Development data; nothing fitted.