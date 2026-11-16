# Ranking headroom probe: FC-CLIP (mask-classification family)

400 development images (roles tune_cal,tune_eval), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 3.19 | 9.68 | 66.68% | 94.85% | 52.92% | 89.51% | 96.38% |
| fcclip_anchored | 3.21 | 10.39 | 69.55% | 94.71% | 64.77% | 89.22% | 95.59% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 31.17 | 67.28% |
| fcclip_anchored | 23.81 | 70.06% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.388, native_150_plus_845 0.003, anchored_845 0.004; peak memory 3.8 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the training vocabulary instead and is candidate-independent by construction (its 150-label scores are the first 150 columns of its 845-label scores).