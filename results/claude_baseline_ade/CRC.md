# CRC on the marked pixels (1000 images, 15000 markers, alpha = 0.1, 500 half splits)

| Arm | Threshold | Risk at 845 names (%) | Splits above alpha (%) | Set size at 845 names |
|---|---|---:|---:|---:|
| claude | reused | 0.0 | 0 | 845.00 |
| claude | recalibrated | 0.0 | 0 | 845.00 |
| catseg_native | reused | 15.6 | 100 | 2.27 |
| catseg_native | recalibrated | 9.8 | 43 | 3.69 |
| catseg_anchored | reused | 9.8 | 41 | 4.56 |
| catseg_anchored | recalibrated | 9.8 | 41 | 4.56 |

Reused: calibrated with the 150 source names in the vocabulary, applied with 845. Claude sets include every unlisted label when the threshold is 0. CAT-Seg ViT-L (683-name bank) scores are the stored logits of the main protocol at the same pixels; the anchored source scores do not depend on the vocabulary.
