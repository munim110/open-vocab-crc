# Full-resolution mIoU, pc59 (59 classes), FC-CLIP ConvNeXt-L

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 54.96 | 76.03% | 0.03 |
| anchored_133 | 57.17 | 78.35% | 0.03 |
| anchored_bank683 | 55.65 | 76.68% | 0.04 |

Backbone, masks and logits 0.60 s/image on NVIDIA GH200 480GB; peak memory 4.1 GB. Development data; nothing fitted.