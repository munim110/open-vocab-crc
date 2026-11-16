# Ranking headroom probe: FC-CLIP (mask-classification family)

1600 development images (roles fit,calibration,evaluation), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 3.14 | 9.57 | 66.12% | 95.17% | 52.13% | 90.14% | 96.38% |
| fcclip_anchored | 3.29 | 9.96 | 67.67% | 95.04% | 58.68% | 89.55% | 96.31% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 31.53 | 66.33% |
| fcclip_anchored | 28.26 | 67.93% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.951, native_150_plus_845 0.003, anchored_845 0.067; peak memory 11.3 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the training vocabulary instead and is candidate-independent by construction (its 150-label scores are the first 150 columns of its 845-label scores).