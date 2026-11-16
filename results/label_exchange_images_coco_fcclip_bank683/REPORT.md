# Label-level CRC, pooled vs image-averaged label loss (coco, fcclip_bank683, 2000 images, 500 trials)

| alpha | loss | added, cal | added, held-out | % trials above alpha (cal / held-out) |
|---|---|---:|---:|---:|
| 0.1 | pooled | 8.98 | 8.99 | 32 / 33 |
| 0.1 | images | 8.98 | 8.96 | 33 / 31 |
| 0.05 | pooled | 4.02 | 4.02 | 26 / 28 |
| 0.05 | images | 3.96 | 3.94 | 25 / 25 |
