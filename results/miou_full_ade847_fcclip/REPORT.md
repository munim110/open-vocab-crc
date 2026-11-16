# Full-resolution mIoU, ade847 (847 classes), FC-CLIP ConvNeXt-L

2000 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 13.53 | 51.64% | 0.05 |
| anchored_133 | 6.98 | 62.61% | 0.06 |
| anchored_bank683 | 10.68 | 59.05% | 0.08 |

Backbone, masks and logits 0.74 s/image on NVIDIA GH200 480GB; peak memory 11.9 GB. Development data; nothing fitted.