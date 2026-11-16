# Full-resolution mIoU, pc459 (459 classes), FC-CLIP ConvNeXt-L

5104 validation images; arg-max prediction; mIoU over classes with ground-truth pixels.

| Arm | mIoU | Pixel accuracy | Seconds / image |
|---|---:|---:|---:|
| native | 16.55 | 61.53% | 0.04 |
| anchored_133 | 15.12 | 68.80% | 0.04 |
| anchored_bank683 | 16.78 | 65.54% | 0.05 |

Backbone, masks and logits 0.64 s/image on NVIDIA GH200 480GB; peak memory 4.1 GB. Development data; nothing fitted.