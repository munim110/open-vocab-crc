# Ranking headroom probe: FC-CLIP (mask-classification family), ADE 150 -> 845

100 development images (roles tune_cal,tune_eval), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 2.64 | 7.37 | 68.81% | 96.59% | 57.11% | 91.47% | 97.69% |
| fcclip_anchored | 2.70 | 8.06 | 72.08% | 96.52% | 64.29% | 90.64% | 97.45% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 30.94 | 69.39% |
| fcclip_anchored | 28.75 | 72.52% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.401, native_150_plus_845 0.001, anchored_845 0.008, native_150 0.000, native_845 0.000; peak memory 4.8 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the reference bank instead and is candidate-independent by construction (its 150-label scores are the first 150 columns of its 845-label scores).