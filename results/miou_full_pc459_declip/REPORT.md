# Full-resolution mIoU, pc459 (459 classes), declip large

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 25.82 | 72.18% | 0.44 |
| anchored_coco171 | 25.06 | 70.63% | 0.96 |
| anchored_bank683 | 25.19 | 71.56% | 1.65 |

Features 0.12 s/image on NVIDIA GH200 480GB; peak memory 9.4 GB. Development data; nothing fitted.