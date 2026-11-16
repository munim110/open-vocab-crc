# Ranking headroom probe: FC-CLIP (mask-classification family)

400 development images (roles tune_cal,tune_eval), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +695 | Source top1 | Source top10 | +695 top1 | +695 top10 | +695 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 3.19 | 9.68 | 66.68% | 94.85% | 52.92% | 89.51% | 96.38% |
| fcclip_anchored | 3.31 | 10.08 | 67.74% | 94.76% | 57.87% | 88.23% | 96.12% |

| Arm | Sampled-pixel mIoU (150, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 31.17 | 67.28% |
| fcclip_anchored | 28.79 | 68.29% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.998, native_150_plus_845 0.003, anchored_845 0.067; peak memory 11.4 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the training vocabulary instead and is candidate-independent by construction (its 150-label scores are the first 150 columns of its 845-label scores).