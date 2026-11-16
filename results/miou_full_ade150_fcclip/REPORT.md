# Full-resolution mIoU, ade150 (150 classes), FC-CLIP ConvNeXt-L

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 32.03 | 67.68% | 0.03 |
| anchored_133 | 24.34 | 70.68% | 0.03 |
| anchored_bank683 | 28.03 | 69.93% | 0.04 |

Backbone, masks and logits 0.60 s/image on NVIDIA GH200 480GB; peak memory 9.8 GB. Development data; nothing fitted.