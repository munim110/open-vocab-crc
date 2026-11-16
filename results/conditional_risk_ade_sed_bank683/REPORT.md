# Conditional risk under source-calibrated thresholds: sed_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.90 | 19.92 | 100.0 | 43.3 | 8.66 | 19.29 | 25.68 | 11.0 | 0 | 10.9 | 3.2 | 26.9 | 13.37 | 12.58 | 8.78 | 7.19 |
| native_frozen | 7.12 | 14.22 | 100.0 | 31.2 | 6.19 | 12.16 | 18.64 | 7.5 | 0 | 8.6 | 2.6 | 20.8 | 12.26 | 10.18 | 5.56 | 3.98 |
| native_replay | 9.90 | 20.45 | 100.0 | 43.4 | 8.47 | 18.83 | 27.88 | 11.3 | 0 | 11.8 | 4.0 | 28.2 | 15.47 | 13.31 | 8.19 | 6.44 |
| anchored_frozen | 9.89 | 17.28 | 100.0 | 38.4 | 8.89 | 14.65 | 22.89 | 10.7 | 0 | 11.9 | 3.5 | 28.8 | 15.66 | 13.25 | 8.26 | 6.30 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 100, earth, ground 100, base, pedestal, stand 100, buffet, counter, sideboard 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 98, pillow 95, screen door, screen 90, step, stair 82, tray 77, bannister, banister, balustrade, balusters, handrail 76
- native_frozen: case, display case, showcase, vitrine 100, earth, ground 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, base, pedestal, stand 100, screen door, screen 86, tank, storage tank 69, tray 66, box 66, buffet, counter, sideboard 63, bannister, banister, balustrade, balusters, handrail 59
- native_replay: case, display case, showcase, vitrine 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, earth, ground 100, base, pedestal, stand 100, screen door, screen 93, tank, storage tank 88, screen, crt screen 87, tray 83, buffet, counter, sideboard 80, box 74
- anchored_frozen: case, display case, showcase, vitrine 100, earth, ground 100, base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 99, tank, storage tank 80, screen, crt screen 79, buffet, counter, sideboard 78, tray 76, land, ground, soil 69, box 67

Worst scenes (image-level risk, %):

- native_source: bathroom 11, misc 10, dining_room 10, bedroom 7, living_room 6
- native_frozen: bathroom 8, misc 7, dining_room 5, bedroom 3, living_room 3
- native_replay: bathroom 11, misc 9, dining_room 9, bedroom 6, living_room 5
- anchored_frozen: bathroom 11, misc 10, dining_room 10, kitchen 6, living_room 6

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 9.49 | 98.8 | 32.0 | 4.37 | 7.93 | 11.47 | 5.0 | 0 | 6.1 | 1.6 | 13.5 | 8.43 | 6.91 | 3.96 | 2.70 |
| native_frozen | 3.79 | 6.96 | 95.7 | 23.5 | 3.46 | 4.59 | 8.52 | 4.2 | 0 | 5.3 | 1.3 | 9.9 | 6.96 | 6.20 | 2.58 | 1.58 |
| native_replay | 4.90 | 9.25 | 98.9 | 29.9 | 4.38 | 6.79 | 11.86 | 5.1 | 0 | 6.3 | 1.7 | 13.9 | 9.27 | 7.54 | 3.51 | 2.26 |
| anchored_frozen | 4.89 | 8.47 | 99.9 | 29.3 | 4.50 | 5.61 | 10.61 | 5.3 | 0 | 6.1 | 1.9 | 13.3 | 9.52 | 7.37 | 3.65 | 2.18 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 98, earth, ground 96, base, pedestal, stand 94, buffet, counter, sideboard 64, screen door, screen 58, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 54, pillow 48, box 47, bannister, banister, balustrade, balusters, handrail 46, tank, storage tank 46
- native_frozen: earth, ground 91, case, display case, showcase, vitrine 91, base, pedestal, stand 87, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 78, box 47, tank, storage tank 46, screen door, screen 40, ship 36, bannister, banister, balustrade, balusters, handrail 35, tray 29
- native_replay: earth, ground 97, case, display case, showcase, vitrine 97, base, pedestal, stand 95, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 94, screen door, screen 59, box 55, tank, storage tank 47, screen, crt screen 47, bannister, banister, balustrade, balusters, handrail 46, ship 45
- anchored_frozen: earth, ground 100, case, display case, showcase, vitrine 98, base, pedestal, stand 91, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 76, box 48, tank, storage tank 46, buffet, counter, sideboard 44, ship 43, tray 42, bannister, banister, balustrade, balusters, handrail 38

Worst scenes (image-level risk, %):

- native_source: misc 5, bathroom 4, dining_room 4, bedroom 3, building_facade 2
- native_frozen: misc 4, bathroom 2, dining_room 1, highway 1, kitchen 1
- native_replay: misc 5, bathroom 4, dining_room 3, highway 2, kitchen 1
- anchored_frozen: misc 5, dining_room 3, bathroom 3, highway 2, kitchen 2

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].