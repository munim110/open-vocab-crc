# Detection, image-level CRC (gdino_b, 1989 images with a source box, 500 splits)

| alpha | arm | risk % | splits > alpha % | set size (vocabulary) |
|---|---|---:|---:|---|
| 0.1 | native, source | 9.87 | 36 | 1.01 (source) |
| 0.1 | native reused, one prompt | 18.33 | 100 | 0.90 (one prompt) |
| 0.1 | native reused, LVIS | 9.80 | 34 | 3.69 (LVIS) |
| 0.1 | native recal., one prompt | 9.88 | 42 | 1.18 (one prompt) |
| 0.1 | native recal., LVIS | 9.86 | 36 | 3.67 (LVIS) |
| 0.1 | anchored A | 9.87 | 36 | 1.01 (source), 1.03 (one prompt), 3.63 (LVIS) |
| 0.1 | anchored B | 9.91 | 45 | 4.05 (source), 7.74 (one prompt), 243.02 (LVIS) |
| 0.05 | native, source | 4.89 | 39 | 1.20 (source) |
| 0.05 | native reused, one prompt | 9.87 | 100 | 1.19 (one prompt) |
| 0.05 | native reused, LVIS | 4.89 | 41 | 9.68 (LVIS) |
| 0.05 | native recal., one prompt | 4.89 | 43 | 2.18 (one prompt) |
| 0.05 | native recal., LVIS | 4.89 | 38 | 9.68 (LVIS) |
| 0.05 | anchored A | 4.89 | 39 | 1.20 (source), 1.40 (one prompt), 12.21 (LVIS) |
| 0.05 | anchored B | 4.34 | 42 | 54.57 (source), 71.47 (one prompt), 1026.70 (LVIS) |

# Label-level CRC (labels as units)

| alpha | design | store | loss | added, cal | added, held-out | trials > alpha (cal / held-out) | src at t | Delta(t) |
|---|---|---|---|---:|---:|---:|---:|---:|
| 0.1 | exchangeable | anch_a | pooled | 2.96 | 2.96 | 21 / 22 | 1.55 | 1.41 |
| 0.1 | exchangeable | anch_a | images | 4.27 | 4.23 | 26 / 23 | 2.48 | 1.79 |
| 0.05 | exchangeable | anch_a | pooled | 0.03 | 0.03 | 0 / 0 | 0.00 | 0.02 |
| 0.05 | exchangeable | anch_a | images | 0.06 | 0.06 | 1 / 1 | 0.01 | 0.05 |
| 0.1 | benchmark split | anch_a | pooled | 64.50 | 64.56 | 100 / 100 | 8.80 | 55.71 |
| 0.1 | benchmark split | anch_a | images | 66.08 | 66.13 | 100 / 100 | 8.79 | 57.29 |
| 0.05 | benchmark split | anch_a | pooled | 40.07 | 40.11 | 100 / 100 | 3.70 | 36.36 |
| 0.05 | benchmark split | anch_a | images | 41.66 | 41.78 | 100 / 100 | 3.70 | 37.96 |
| 0.1 | exchangeable | native_lvis | pooled | 6.64 | 6.66 | 25 / 25 | 4.57 | 2.07 |
| 0.1 | exchangeable | native_lvis | images | 7.52 | 7.51 | 26 / 25 | 5.64 | 1.88 |
| 0.05 | exchangeable | native_lvis | pooled | 0.21 | 0.22 | 3 / 3 | 0.05 | 0.16 |
| 0.05 | exchangeable | native_lvis | images | 0.46 | 0.47 | 7 / 7 | 0.13 | 0.33 |
| 0.1 | benchmark split | native_lvis | pooled | 62.64 | 62.53 | 100 / 100 | 8.79 | 53.85 |
| 0.1 | benchmark split | native_lvis | images | 63.71 | 63.56 | 100 / 100 | 8.77 | 54.94 |
| 0.05 | benchmark split | native_lvis | pooled | 43.35 | 43.26 | 100 / 100 | 3.70 | 39.65 |
| 0.05 | benchmark split | native_lvis | images | 43.24 | 43.15 | 100 / 100 | 3.71 | 39.53 |
