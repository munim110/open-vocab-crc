# Detection, image-level CRC (owlv2, 1989 images with a source box, 500 splits)

| alpha | arm | risk % | splits > alpha % | set size (vocabulary) |
|---|---|---:|---:|---|
| 0.1 | OWLv2 | 9.89 | 43 | 1.40 (source), 8.28 (LVIS) |
| 0.05 | OWLv2 | 4.93 | 44 | 2.72 (source), 28.53 (LVIS) |

# Label-level CRC (labels as units)

| alpha | design | store | loss | added, cal | added, held-out | trials > alpha (cal / held-out) | src at t | Delta(t) |
|---|---|---|---|---:|---:|---:|---:|---:|
| 0.1 | exchangeable | owl | pooled | 7.55 | 7.57 | 21 / 21 | 6.20 | 1.35 |
| 0.1 | exchangeable | owl | images | 7.82 | 7.86 | 22 / 22 | 6.55 | 1.27 |
| 0.05 | exchangeable | owl | pooled | 0.59 | 0.63 | 7 / 8 | 0.23 | 0.36 |
| 0.05 | exchangeable | owl | images | 1.25 | 1.29 | 7 / 8 | 0.56 | 0.70 |
| 0.1 | benchmark split | owl | pooled | 12.71 | 12.78 | 100 / 100 | 8.81 | 3.89 |
| 0.1 | benchmark split | owl | images | 13.32 | 13.41 | 100 / 100 | 8.81 | 4.51 |
| 0.05 | benchmark split | owl | pooled | 5.61 | 5.64 | 83 / 81 | 3.78 | 1.83 |
| 0.05 | benchmark split | owl | images | 6.09 | 6.14 | 95 / 95 | 3.76 | 2.33 |
