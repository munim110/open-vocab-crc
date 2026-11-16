# Added-label excess risk against measured hardness (prop:shift)

vitl_bank683, 2000 ADE validation images, 845 names, 500 trials (design "exchangeable" of exp_label_exchange.py: 150 uniformly drawn names are the calibration labels). Q_k = uniform over the k-th fifth of the remaining names by hardness (pooled loss on the held-out images at the label-level threshold of the held-out images; Q1 easiest). All risks on the calibration images at the label-level threshold t_l (the proposition's quantity), in %, mean over trials: realised = l_Q(t_l); P = l_P(t_l), a further uniform draw; bound = alpha + Delta(t_l) and alpha + max_t Delta(t). Development data; nothing fitted.

## alpha = 0.1

| Added names | Names | Held-out hardness | Realised | P | alpha + Delta(t_l) | alpha + max Delta | Trials above alpha |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 72 | 0.0 | 1.71 | 9.44 | 2.27 | 10.03 | 0% |
| Q2 | 72 | 0.0 | 6.14 | 9.44 | 6.70 | 13.45 | 11% |
| Q3 | 72 | 0.3 | 4.44 | 9.44 | 5.00 | 10.73 | 5% |
| Q4 | 71 | 3.3 | 6.23 | 9.44 | 6.79 | 12.69 | 9% |
| Q5 | 71 | 39.6 | 24.86 | 9.44 | 25.43 | 36.12 | 100% |
| Q_all | 358 | 8.6 | 8.65 | 9.44 | 9.21 | 10.33 | 26% |

Contamination, Q = (1 - eps) P + eps Q5:

| eps | Realised | Bound alpha + eps | Excess over alpha |
|---:|---:|---:|---:|
| 0 | 9.44 | 10 | -0.56 |
| 0.05 | 10.21 | 15 | +0.21 |
| 0.1 | 10.98 | 20 | +0.98 |
| 0.25 | 13.29 | 35 | +3.29 |
| 0.5 | 17.15 | 60 | +7.15 |
| 1 | 24.86 | 110 | +14.86 |

## alpha = 0.05

| Added names | Names | Held-out hardness | Realised | P | alpha + Delta(t_l) | alpha + max Delta | Trials above alpha |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 72 | 0.0 | 0.33 | 4.42 | 0.92 | 5.01 | 0% |
| Q2 | 72 | 0.0 | 1.38 | 4.42 | 1.96 | 6.85 | 2% |
| Q3 | 72 | 0.0 | 2.69 | 4.42 | 3.27 | 10.26 | 14% |
| Q4 | 71 | 0.3 | 2.93 | 4.42 | 3.51 | 8.92 | 16% |
| Q5 | 71 | 19.3 | 12.48 | 4.42 | 13.06 | 23.38 | 96% |
| Q_all | 358 | 3.9 | 3.95 | 4.42 | 4.53 | 5.33 | 23% |

Contamination, Q = (1 - eps) P + eps Q5:

| eps | Realised | Bound alpha + eps | Excess over alpha |
|---:|---:|---:|---:|
| 0 | 4.42 | 5 | -0.58 |
| 0.05 | 4.82 | 10 | -0.18 |
| 0.1 | 5.22 | 15 | +0.22 |
| 0.25 | 6.43 | 30 | +1.43 |
| 0.5 | 8.45 | 55 | +3.45 |
| 1 | 12.48 | 105 | +7.48 |

