# Detection, image-level CRC (gdino_t, 1989 images with a source box, 500 splits)

| alpha | arm | risk % | splits > alpha % | set size (vocabulary) |
|---|---|---:|---:|---|
| 0.1 | native, source | 9.87 | 45 | 1.27 (source) |
| 0.1 | native reused, one prompt | 9.57 | 25 | 1.66 (one prompt) |
| 0.1 | native reused, LVIS | 9.57 | 22 | 94.69 (LVIS) |
| 0.1 | native recal., one prompt | 9.91 | 47 | 1.60 (one prompt) |
| 0.1 | native recal., LVIS | 9.91 | 45 | 88.29 (LVIS) |
| 0.1 | anchored A | 9.87 | 45 | 1.27 (source), 1.71 (one prompt), 34.20 (LVIS) |
| 0.1 | anchored B | 9.91 | 43 | 11.86 (source), 15.96 (one prompt), 295.39 (LVIS) |
| 0.05 | native, source | 4.90 | 38 | 2.19 (source) |
| 0.05 | native reused, one prompt | 4.63 | 19 | 3.81 (one prompt) |
| 0.05 | native reused, LVIS | 4.80 | 31 | 291.06 (LVIS) |
| 0.05 | native recal., one prompt | 4.91 | 46 | 3.51 (one prompt) |
| 0.05 | native recal., LVIS | 4.92 | 42 | 280.54 (LVIS) |
| 0.05 | anchored A | 4.90 | 38 | 2.19 (source), 4.01 (one prompt), 121.20 (LVIS) |
| 0.05 | anchored B | 1.68 | 31 | 74.71 (source), 93.93 (one prompt), 1158.49 (LVIS) |

# Label-level CRC (labels as units)

| alpha | design | store | loss | added, cal | added, held-out | trials > alpha (cal / held-out) | src at t | Delta(t) |
|---|---|---|---|---:|---:|---:|---:|---:|
| 0.1 | exchangeable | anch_a | pooled | 3.54 | 3.53 | 26 / 25 | 2.01 | 1.53 |
| 0.1 | exchangeable | anch_a | images | 4.78 | 4.78 | 26 / 26 | 2.98 | 1.80 |
| 0.05 | exchangeable | anch_a | pooled | 0.02 | 0.02 | 0 / 0 | 0.00 | 0.02 |
| 0.05 | exchangeable | anch_a | images | 0.08 | 0.07 | 1 / 1 | 0.02 | 0.06 |
| 0.1 | benchmark split | anch_a | pooled | 35.50 | 35.56 | 100 / 100 | 8.79 | 26.71 |
| 0.1 | benchmark split | anch_a | images | 38.04 | 38.07 | 100 / 100 | 8.79 | 29.26 |
| 0.05 | benchmark split | anch_a | pooled | 17.65 | 17.60 | 100 / 100 | 3.78 | 13.87 |
| 0.05 | benchmark split | anch_a | images | 20.75 | 20.74 | 100 / 100 | 3.75 | 16.99 |
| 0.1 | exchangeable | native_lvis | pooled | 6.10 | 6.12 | 24 / 24 | 4.41 | 1.70 |
| 0.1 | exchangeable | native_lvis | images | 7.29 | 7.29 | 23 / 24 | 5.67 | 1.62 |
| 0.05 | exchangeable | native_lvis | pooled | 0.10 | 0.10 | 1 / 1 | 0.02 | 0.07 |
| 0.05 | exchangeable | native_lvis | images | 0.53 | 0.55 | 8 / 8 | 0.18 | 0.35 |
| 0.1 | benchmark split | native_lvis | pooled | 19.07 | 19.14 | 100 / 100 | 8.79 | 10.28 |
| 0.1 | benchmark split | native_lvis | images | 18.96 | 19.03 | 100 / 100 | 8.78 | 10.17 |
| 0.05 | benchmark split | native_lvis | pooled | 9.88 | 9.88 | 100 / 100 | 3.77 | 6.11 |
| 0.05 | benchmark split | native_lvis | images | 10.26 | 10.28 | 100 / 100 | 3.76 | 6.50 |
