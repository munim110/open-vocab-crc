# Claude Opus 5.5 zero-shot on marked ADE20K pixels (1000 images, K = 15)

Cost $34.15 ($0.034 per image, both vocabularies).

| Names | Usable / requests | Markers | Top-1 | Listed (top-10) | Mean prob. of true label | Unmatched names | In tokens | Out tokens | Seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 150 | 1000/1000 | 15000 | 67.5% | 88.4% | 0.582 | 21 | 1412 | 744 | 7.2 |
| 845 | 1000/1000 | 15000 | 62.8% | 82.9% | 0.542 | 81 | 4390 | 738 | 6.2 |

Same markers at 150 and 845 names (15000): probability of the true label 0.5819639999999999 -> 0.5421633333333333; top-1 unchanged at 0.8164666666666667; true-label probability changed at 0.5726 of markers.
