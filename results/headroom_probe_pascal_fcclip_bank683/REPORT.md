# Ranking headroom probe: FC-CLIP (mask-classification family), Pascal Context 59 -> 458

2000 development images (all cached images), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +399 | Source top1 | Source top10 | +399 top1 | +399 top10 | +399 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 1.77 | 4.61 | 76.36% | 98.56% | 63.15% | 93.00% | 98.55% |
| fcclip_anchored | 1.76 | 4.72 | 76.49% | 98.63% | 69.18% | 93.00% | 98.39% |

| Arm | Sampled-pixel mIoU (59, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 54.73 | 76.18% |
| fcclip_anchored | 54.30 | 76.35% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.375, native_150_plus_845 0.001, anchored_845 0.007; peak memory 4.0 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the reference bank instead and is candidate-independent by construction (its 59-label scores are the first 59 columns of its 458-label scores).