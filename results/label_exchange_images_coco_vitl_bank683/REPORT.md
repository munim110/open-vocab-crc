# Label-level CRC, pooled vs image-averaged label loss (coco, vitl_bank683, 2000 images, 500 trials)

| alpha | loss | added, cal | added, held-out | % trials above alpha (cal / held-out) |
|---|---|---:|---:|---:|
| 0.1 | pooled | 8.93 | 9.02 | 33 / 34 |
| 0.1 | images | 8.90 | 8.95 | 32 / 34 |
| 0.05 | pooled | 4.01 | 4.06 | 27 / 28 |
| 0.05 | images | 3.93 | 3.98 | 24 / 27 |
