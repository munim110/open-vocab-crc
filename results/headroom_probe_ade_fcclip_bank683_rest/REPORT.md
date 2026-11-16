# Ranking headroom probe: FC-CLIP (mask-classification family)

1600 development images (roles fit,calibration,evaluation), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 3.14 | 9.57 | 66.12% | 95.17% | 52.13% | 90.14% | 96.38% |
| fcclip_anchored | 3.22 | 9.95 | 68.41% | 95.10% | 61.20% | 89.54% | 96.18% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 31.53 | 66.33% |
| fcclip_anchored | 26.63 | 68.67% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.506, native_150_plus_845 0.002, anchored_845 0.016; peak memory 4.8 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the training vocabulary instead and is candidate-independent by construction (its 150-label scores are the first 150 columns of its 845-label scores).