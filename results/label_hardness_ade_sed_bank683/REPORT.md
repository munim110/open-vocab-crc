# Added-label excess risk against measured hardness (prop:shift)

sed_bank683, 2000 ADE validation images, 845 names, 500 trials (design "exchangeable" of exp_label_exchange.py: 150 uniformly drawn names are the calibration labels). Q_k = uniform over the k-th fifth of the remaining names by hardness (pooled loss on the held-out images at the label-level threshold of the held-out images; Q1 easiest). All risks on the calibration images at the label-level threshold t_l (the proposition's quantity), in %, mean over trials: realised = l_Q(t_l); P = l_P(t_l), a further uniform draw; bound = alpha + Delta(t_l) and alpha + max_t Delta(t). Development data; nothing fitted.

## alpha = 0.1

| Added names | Names | Held-out hardness | Realised | P | alpha + Delta(t_l) | alpha + max Delta | Trials above alpha |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 72 | 0.0 | 1.26 | 9.44 | 1.82 | 10.01 | 0% |
| Q2 | 72 | 0.0 | 6.35 | 9.44 | 6.90 | 12.91 | 12% |
| Q3 | 72 | 0.2 | 5.18 | 9.44 | 5.74 | 11.37 | 5% |
| Q4 | 71 | 3.3 | 6.10 | 9.44 | 6.66 | 15.12 | 11% |
| Q5 | 71 | 41.9 | 25.63 | 9.44 | 26.19 | 38.51 | 100% |
| Q_all | 358 | 9.0 | 8.88 | 9.44 | 9.44 | 10.56 | 31% |

Contamination, Q = (1 - eps) P + eps Q5:

| eps | Realised | Bound alpha + eps | Excess over alpha |
|---:|---:|---:|---:|
| 0 | 9.44 | 10 | -0.56 |
| 0.05 | 10.25 | 15 | +0.25 |
| 0.1 | 11.06 | 20 | +1.06 |
| 0.25 | 13.49 | 35 | +3.49 |
| 0.5 | 17.53 | 60 | +7.53 |
| 1 | 25.63 | 110 | +15.63 |

## alpha = 0.05

| Added names | Names | Held-out hardness | Realised | P | alpha + Delta(t_l) | alpha + max Delta | Trials above alpha |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 72 | 0.0 | 0.19 | 4.47 | 0.72 | 5.00 | 0% |
| Q2 | 72 | 0.0 | 1.46 | 4.47 | 1.99 | 6.07 | 2% |
| Q3 | 72 | 0.0 | 3.47 | 4.47 | 3.99 | 11.41 | 24% |
| Q4 | 71 | 0.3 | 2.75 | 4.47 | 3.27 | 8.42 | 12% |
| Q5 | 71 | 21.0 | 13.20 | 4.47 | 13.73 | 27.50 | 96% |
| Q_all | 358 | 4.3 | 4.20 | 4.47 | 4.73 | 5.56 | 28% |

Contamination, Q = (1 - eps) P + eps Q5:

| eps | Realised | Bound alpha + eps | Excess over alpha |
|---:|---:|---:|---:|
| 0 | 4.47 | 5 | -0.53 |
| 0.05 | 4.91 | 10 | -0.09 |
| 0.1 | 5.35 | 15 | +0.35 |
| 0.25 | 6.66 | 30 | +1.66 |
| 0.5 | 8.84 | 55 | +3.84 |
| 1 | 13.20 | 105 | +8.20 |

