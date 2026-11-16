# Conditional risk under source-calibrated thresholds: declip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.90 | 17.59 | 100.0 | 39.8 | 8.86 | 19.33 | 18.29 | 11.0 | 0 | 11.4 | 3.0 | 27.8 | 12.21 | 12.63 | 9.16 | 7.05 |
| native_frozen | 14.72 | 25.16 | 100.0 | 60.4 | 13.12 | 27.69 | 28.39 | 15.3 | 0 | 19.3 | 6.3 | 39.8 | 21.14 | 18.56 | 13.32 | 10.11 |
| native_replay | 9.92 | 17.58 | 100.0 | 39.9 | 8.75 | 19.21 | 18.82 | 9.9 | 0 | 12.1 | 3.6 | 29.2 | 14.58 | 13.18 | 8.74 | 6.24 |
| anchored_frozen | 9.89 | 13.78 | 100.0 | 29.7 | 9.23 | 12.51 | 14.60 | 13.5 | 0 | 12.5 | 3.9 | 29.8 | 14.82 | 13.34 | 8.68 | 5.97 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 100, base, pedestal, stand 100, buffet, counter, sideboard 99, trade name, brand name, brand, marque 99, pillow 91, earth, ground 89, canopy 84, tank, storage tank 72, hovel, hut, hutch, shack, shanty 72, blanket, cover 68
- native_frozen: base, pedestal, stand 100, case, display case, showcase, vitrine 100, trade name, brand name, brand, marque 100, buffet, counter, sideboard 100, hovel, hut, hutch, shack, shanty 98, earth, ground 96, pillow 94, canopy 94, tank, storage tank 89, screen door, screen 82
- native_replay: case, display case, showcase, vitrine 100, base, pedestal, stand 100, buffet, counter, sideboard 88, canopy 88, trade name, brand name, brand, marque 88, earth, ground 88, tank, storage tank 85, hovel, hut, hutch, shack, shanty 79, pillow 78, bulletin board, notice board 72
- anchored_frozen: case, display case, showcase, vitrine 100, base, pedestal, stand 100, earth, ground 96, buffet, counter, sideboard 88, tank, storage tank 78, canopy 69, step, stair 58, hovel, hut, hutch, shack, shanty 55, plaything, toy 54, traffic light, traffic signal, stoplight 52

Worst scenes (image-level risk, %):

- native_source: misc 11, dining_room 9, bedroom 7, living_room 6, bathroom 6
- native_frozen: misc 15, dining_room 13, bathroom 11, living_room 9, bedroom 9
- native_replay: misc 10, dining_room 9, bedroom 6, bathroom 6, living_room 5
- anchored_frozen: bathroom 14, misc 10, dining_room 9, kitchen 7, living_room 5

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 8.69 | 99.8 | 30.7 | 4.47 | 8.00 | 7.80 | 4.8 | 0 | 5.0 | 1.4 | 12.8 | 6.86 | 6.55 | 4.41 | 3.06 |
| native_frozen | 7.96 | 14.23 | 100.0 | 53.2 | 7.02 | 14.96 | 14.85 | 7.9 | 0 | 9.4 | 2.7 | 23.6 | 12.08 | 10.92 | 6.82 | 4.76 |
| native_replay | 4.91 | 8.58 | 99.9 | 32.3 | 4.43 | 7.49 | 8.03 | 4.8 | 0 | 5.7 | 1.5 | 13.8 | 8.10 | 7.06 | 4.06 | 2.55 |
| anchored_frozen | 4.89 | 7.29 | 98.5 | 23.6 | 4.59 | 5.42 | 6.39 | 5.2 | 0 | 5.6 | 1.4 | 14.1 | 7.61 | 7.28 | 4.06 | 2.40 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 100, base, pedestal, stand 98, earth, ground 68, buffet, counter, sideboard 67, canopy 57, pillow 47, traffic light, traffic signal, stoplight 46, box 41, step, stair 37, blanket, cover 37
- native_frozen: base, pedestal, stand 100, case, display case, showcase, vitrine 100, earth, ground 81, canopy 77, buffet, counter, sideboard 77, tank, storage tank 75, hovel, hut, hutch, shack, shanty 74, trade name, brand name, brand, marque 64, plaything, toy 64, pillow 62
- native_replay: case, display case, showcase, vitrine 100, base, pedestal, stand 100, earth, ground 66, canopy 59, buffet, counter, sideboard 55, box 44, traffic light, traffic signal, stoplight 41, hovel, hut, hutch, shack, shanty 39, step, stair 37, tank, storage tank 36
- anchored_frozen: case, display case, showcase, vitrine 97, base, pedestal, stand 96, earth, ground 78, buffet, counter, sideboard 57, traffic light, traffic signal, stoplight 42, tank, storage tank 41, box 40, canopy 40, plaything, toy 34, step, stair 31

Worst scenes (image-level risk, %):

- native_source: misc 5, dining_room 4, bedroom 4, living_room 2, kitchen 2
- native_frozen: misc 8, dining_room 7, bedroom 5, bathroom 4, living_room 4
- native_replay: misc 5, dining_room 3, bedroom 2, living_room 2, bathroom 2
- anchored_frozen: misc 5, dining_room 4, bathroom 2, kitchen 2, living_room 2

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].