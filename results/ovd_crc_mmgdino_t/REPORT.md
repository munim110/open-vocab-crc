# Detection, image-level CRC (mmgdino_t, 1989 images with a source box, 500 splits)

| alpha | arm | risk % | splits > alpha % | set size (vocabulary) |
|---|---|---:|---:|---|
| 0.1 | native, source | 9.88 | 43 | 1.20 (source) |
| 0.1 | native reused, one prompt | 9.33 | 16 | 1.71 (one prompt) |
| 0.1 | native reused, LVIS | 9.00 | 8 | 23.00 (LVIS) |
| 0.1 | native recal., one prompt | 9.88 | 39 | 1.63 (one prompt) |
| 0.1 | native recal., LVIS | 9.90 | 42 | 20.22 (LVIS) |
| 0.1 | anchored A | 9.88 | 43 | 1.20 (source), 1.22 (one prompt), 3.12 (LVIS) |
| 0.1 | anchored B | 9.88 | 47 | 6.60 (source), 8.50 (one prompt), 84.08 (LVIS) |
| 0.05 | native, source | 4.87 | 38 | 1.88 (source) |
| 0.05 | native reused, one prompt | 4.28 | 3 | 4.06 (one prompt) |
| 0.05 | native reused, LVIS | 4.49 | 11 | 63.76 (LVIS) |
| 0.05 | native recal., one prompt | 4.90 | 42 | 3.39 (one prompt) |
| 0.05 | native recal., LVIS | 4.88 | 37 | 55.82 (LVIS) |
| 0.05 | anchored A | 4.87 | 38 | 1.88 (source), 2.04 (one prompt), 9.49 (LVIS) |
| 0.05 | anchored B | 4.92 | 42 | 33.84 (source), 42.60 (one prompt), 474.14 (LVIS) |

# Label-level CRC (labels as units)

| alpha | design | store | loss | added, cal | added, held-out | trials > alpha (cal / held-out) | src at t | Delta(t) |
|---|---|---|---|---:|---:|---:|---:|---:|
| 0.1 | exchangeable | anch_a | pooled | 1.91 | 1.89 | 13 / 13 | 0.91 | 1.00 |
| 0.1 | exchangeable | anch_a | images | 3.21 | 3.23 | 25 / 24 | 1.71 | 1.50 |
| 0.05 | exchangeable | anch_a | pooled | 0.00 | 0.00 | 0 / 0 | 0.00 | 0.00 |
| 0.05 | exchangeable | anch_a | images | 0.02 | 0.02 | 0 / 0 | 0.00 | 0.02 |
| 0.1 | benchmark split | anch_a | pooled | 52.33 | 52.27 | 100 / 100 | 8.80 | 43.53 |
| 0.1 | benchmark split | anch_a | images | 55.96 | 55.92 | 100 / 100 | 8.80 | 47.17 |
| 0.05 | benchmark split | anch_a | pooled | 23.09 | 23.06 | 100 / 100 | 3.78 | 19.32 |
| 0.05 | benchmark split | anch_a | images | 30.62 | 30.68 | 100 / 100 | 3.73 | 26.89 |
| 0.1 | exchangeable | native_lvis | pooled | 7.68 | 7.70 | 26 / 26 | 5.95 | 1.73 |
| 0.1 | exchangeable | native_lvis | images | 7.90 | 7.90 | 25 / 27 | 6.27 | 1.64 |
| 0.05 | exchangeable | native_lvis | pooled | 0.55 | 0.57 | 7 / 8 | 0.19 | 0.36 |
| 0.05 | exchangeable | native_lvis | images | 1.19 | 1.20 | 10 / 10 | 0.44 | 0.75 |
| 0.1 | benchmark split | native_lvis | pooled | 21.68 | 21.63 | 100 / 100 | 8.79 | 12.89 |
| 0.1 | benchmark split | native_lvis | images | 22.58 | 22.53 | 100 / 100 | 8.80 | 13.78 |
| 0.05 | benchmark split | native_lvis | pooled | 9.21 | 9.23 | 100 / 100 | 3.78 | 5.43 |
| 0.05 | benchmark split | native_lvis | images | 11.11 | 11.10 | 100 / 100 | 3.75 | 7.36 |
