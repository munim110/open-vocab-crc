# CLIPSeg independent-query baseline

400 ADE development images (the headroom-probe 400), CIDAS/clipseg-rd64-refined, raw per-query logits, threshold calibrated once at the 150 source labels by image-level CRC; mean over 200 random 200/200 splits.

Source rank 5.04; rank at +695 20.58; source top-1 56.61%; +695 top-10 75.25%; sampled-pixel mIoU 15.33; 0.35 s/image for 845 queries.

| alpha | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 9.41 | 10.20 | 14.58 | 22.45 | 39.59 | 46.24 |
| 0.05 | 4.48 | 19.48 | 28.29 | 44.29 | 81.08 | 96.49 |

Compare with results/anchor_bank_ade/REPORT.md (same images and split seed). CLIPSeg was trained on PhraseCut, not COCO-Stuff, at lower resolution; this is a baseline for the independent-query construction, not a matched-training comparison. Development data.