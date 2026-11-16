# Label-level CRC, pooled vs image-averaged label loss (coco, vitb_bank683, 2000 images, 500 trials)

| alpha | loss | added, cal | added, held-out | % trials above alpha (cal / held-out) |
|---|---|---:|---:|---:|
| 0.1 | pooled | 9.09 | 9.17 | 36 / 37 |
| 0.1 | images | 9.04 | 9.09 | 35 / 35 |
| 0.05 | pooled | 4.09 | 4.14 | 29 / 28 |
| 0.05 | images | 4.05 | 4.07 | 25 / 27 |
