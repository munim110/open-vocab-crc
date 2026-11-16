# Ranking headroom probe: FC-CLIP (mask-classification family), COCO-Stuff 171 -> 1283

2000 development images (all cached images), image-averaged metrics at the cached sampled pixels. Ranking diagnostic only.

| Arm | Source rank | Rank at +1112 | Source top1 | Source top10 | +1112 top1 | +1112 top10 | +1112 top50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fcclip_native | 4.30 | 21.38 | 61.23% | 91.76% | 44.20% | 82.74% | 92.43% |
| fcclip_anchored | 4.31 | 20.97 | 62.37% | 91.70% | 56.73% | 83.41% | 92.37% |

| Arm | Sampled-pixel mIoU (171, natural wording) | Pixel accuracy |
|---|---:|---:|
| fcclip_native | 43.27 | 61.29% |
| fcclip_anchored | 43.45 | 62.41% |

Seconds per image on NVIDIA GH200 480GB: backbone_masks_and_logits 0.485, native_150_plus_845 0.001, anchored_845 0.011, native_150 0.000, native_845 0.000; peak memory 6.1 GB.

Native FC-CLIP is candidate-dependent through its softmaxes over the deployed vocabulary; the anchored arm normalises every label against the reference bank instead and is candidate-independent by construction (its 171-label scores are the first 171 columns of its 1283-label scores).