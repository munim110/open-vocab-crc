# Conditional risk under source-calibrated thresholds: fcclip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.89 | 18.05 | 100.0 | 41.7 | 8.90 | 15.38 | 23.45 | 12.2 | 0 | 10.9 | 3.3 | 26.9 | 13.48 | 11.98 | 9.02 | 7.48 |
| native_frozen | 13.81 | 24.07 | 100.0 | 56.8 | 12.39 | 21.98 | 30.41 | 15.8 | 0 | 17.5 | 5.8 | 37.8 | 20.32 | 17.10 | 12.23 | 10.02 |
| native_replay | 9.89 | 18.71 | 100.0 | 43.9 | 8.71 | 17.13 | 23.12 | 10.9 | 0 | 11.1 | 3.9 | 27.2 | 14.49 | 12.84 | 8.57 | 6.77 |
| anchored_frozen | 9.89 | 16.56 | 100.0 | 38.8 | 9.06 | 15.32 | 19.15 | 13.5 | 0 | 11.6 | 3.2 | 27.4 | 13.41 | 12.04 | 8.46 | 8.14 |

Worst classes (pixel-pooled miss rate, %):

- native_source: earth, ground 100, case, display case, showcase, vitrine 100, buffet, counter, sideboard 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 91, base, pedestal, stand 88, canopy 75, step, stair 74, glass, drinking glass 72, screen door, screen 66, tank, storage tank 61
- native_frozen: case, display case, showcase, vitrine 100, earth, ground 100, base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, buffet, counter, sideboard 99, tank, storage tank 88, step, stair 84, screen door, screen 83, booth, cubicle, stall, kiosk 79, canopy 79
- native_replay: earth, ground 100, case, display case, showcase, vitrine 99, buffet, counter, sideboard 98, base, pedestal, stand 98, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 98, screen door, screen 74, booth, cubicle, stall, kiosk 69, box 66, canopy 65, glass, drinking glass 64
- anchored_frozen: earth, ground 100, case, display case, showcase, vitrine 99, buffet, counter, sideboard 96, animal, animate being, beast, brute, creature, fauna 88, base, pedestal, stand 87, tank, storage tank 73, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 70, plant, flora, plant life 66, step, stair 63, blind, screen 58

Worst scenes (image-level risk, %):

- native_source: bathroom 12, dining_room 11, misc 10, kitchen 6, living_room 6
- native_frozen: bathroom 16, dining_room 14, misc 13, kitchen 8, living_room 8
- native_replay: bathroom 11, dining_room 11, misc 9, kitchen 5, living_room 5
- anchored_frozen: bathroom 14, dining_room 13, living_room 10, misc 9, kitchen 8

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 9.10 | 96.7 | 33.4 | 4.47 | 7.71 | 10.13 | 6.0 | 0 | 5.7 | 1.5 | 13.6 | 6.60 | 6.79 | 4.22 | 3.09 |
| native_frozen | 6.78 | 13.64 | 99.4 | 48.4 | 5.94 | 12.27 | 15.47 | 7.3 | 0 | 7.7 | 2.4 | 19.1 | 10.93 | 9.13 | 5.59 | 4.31 |
| native_replay | 4.90 | 9.61 | 97.6 | 36.6 | 4.38 | 7.93 | 10.64 | 5.5 | 0 | 6.1 | 1.8 | 13.6 | 8.01 | 7.06 | 3.89 | 2.74 |
| anchored_frozen | 4.91 | 8.59 | 97.9 | 31.0 | 4.50 | 7.12 | 9.51 | 5.6 | 0 | 5.8 | 1.7 | 13.3 | 8.03 | 6.96 | 3.73 | 3.07 |

Worst classes (pixel-pooled miss rate, %):

- native_source: earth, ground 94, buffet, counter, sideboard 92, case, display case, showcase, vitrine 91, base, pedestal, stand 75, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 56, screen door, screen 45, traffic light, traffic signal, stoplight 43, box 40, ship 39, canopy 39
- native_frozen: earth, ground 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 95, base, pedestal, stand 95, case, display case, showcase, vitrine 95, buffet, counter, sideboard 91, box 57, tank, storage tank 56, screen door, screen 51, booth, cubicle, stall, kiosk 49, step, stair 47
- native_replay: earth, ground 97, base, pedestal, stand 89, case, display case, showcase, vitrine 86, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 85, buffet, counter, sideboard 84, screen door, screen 45, box 44, tank, storage tank 43, traffic light, traffic signal, stoplight 40, ship 39
- anchored_frozen: earth, ground 97, buffet, counter, sideboard 84, animal, animate being, beast, brute, creature, fauna 82, case, display case, showcase, vitrine 79, base, pedestal, stand 59, tank, storage tank 43, glass, drinking glass 41, ship 40, traffic light, traffic signal, stoplight 36, tray 34

Worst scenes (image-level risk, %):

- native_source: dining_room 6, misc 5, bathroom 4, kitchen 3, living_room 2
- native_frozen: dining_room 7, misc 7, bathroom 4, kitchen 3, living_room 3
- native_replay: misc 6, dining_room 5, bathroom 3, kitchen 2, living_room 2
- anchored_frozen: dining_room 6, misc 5, living_room 3, kitchen 3, bathroom 2

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].