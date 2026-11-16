# Full-resolution mIoU, pc459 (459 classes), sed large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 22.25 | 69.99% | 0.68 |
| anchored_coco171 | 22.06 | 69.08% | 0.91 |
| anchored_bank683 | 21.85 | 69.70% | 1.64 |

Features 0.10 s/image on NVIDIA GH200 480GB; peak memory 6.9 GB. Development data; nothing fitted.