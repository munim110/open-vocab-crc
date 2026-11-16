# Free-form per-image names: protocol (fixed 2026-11-01, before any score was computed)

Question: with per-image
names from a language model, including names outside ADE20K-847, what are the source-label risk and the set size of each
calibration option, and what happens to the added names?

## Names

- Namer: Claude Opus 5.5 (`claude-opus-5-5`), effort low (adaptive thinking cannot be disabled on this model), default
  sampling, structured output `{"names": [string]}`. No list of names is shown. One request per image, the original
  ADE20K JPEG, prompt fixed in `src/exp_freeform_names.py` (SYSTEM, INSTRUCTION). A refusal or an empty answer is
  recorded and the image gets no added names; no other model is asked.
- Images: the 2,000 ADE20K validation images of the main protocol (headroom-probe runs `*_bank683` and `_rest`).
- Normalisation: lower case, outer whitespace and punctuation stripped, inner whitespace collapsed. A name equal to one of
  the 150 source prompts or to a synonym in their canonical ADE names is dropped (it is already deployed); duplicates
  within an image are dropped; the order of the answer is kept. Nothing else is filtered: near-synonyms of source names
  ("brick wall", "couch") stay, as they would in a deployment.
- Reported about the names: names per image; unique names; share not among the 845 evaluated names or their canonical
  synonyms ("outside ADE20K-847"); share not in the 17,001-name lexicon of exp_lexicon_probe.py.

## Scores

Deployed vocabulary per image: the 150 source names followed by its added names A(x). Same sampled pixels, inference and
float16 logit storage as exp_adaptive_vocab_probe.py.
- CAT-Seg ViT-L and SED (683-name bank): one native pass at exactly that list; one anchored pass of the A(x) candidates
  against the bank (lean bank pass, candidate scores identical). Anchored source columns are the stored anchored845
  source columns; the run recomputes them on the first images as a check (must equal the store).
- FC-CLIP (701-name bank): one forward pass with the source names, A(x), the bank and void in the text classifier; native =
  released semantic inference over the deployed columns, anchored = the conversion of exp_fcclip_probe.py per candidate.
  The per-query logits do not depend on the other candidates, so adding A(x) to the classifier leaves the source columns
  unchanged; checked on the first images against the stored native150 / anchored scores.

## Analysis (src/exp_freeform_vocab.py)

Image-level CRC on the source-label miss rate, 500 random half/half splits (seed 20260924, as exp_adaptive_vocab.py),
alpha 10% and 5%. Arms:
- anchored, calibrated once (the threshold of exp_adaptive_vocab.py; its source-label loss does not depend on A(x));
- native, reused at 150; native, recalibrated at 845;
- native, recalibrated at a lexicon of 1,690 / 17,001 names (SED and FC-CLIP, whose lexicon stores are on this machine);
- native, matched: calibrated on the calibration half under the free-form names (needs the namer at calibration time).
Risk, share of splits above alpha, set size (deployed labels per source-labelled pixel), and how many added names are in
the set per source-labelled pixel. No ground truth exists for names outside ADE20K-847, so no added-label risk is claimed.

Expected from Prop. 1: the anchored risk equals its value under every other rule (9.9% at alpha 10%). The open questions
are the native arms and the set sizes. Whatever the result, it is reported.

## Run record (2026-11-01)

- Naming: 2,000 requests, none failed or refused, $9.48 ($0.0047 per image; 20-image pilot $0.10 included in raw.jsonl).
  25.1 names answered and 16.1 added per image (max 29), 5,797 unique added names; 77.2% of added names (91.1% of unique
  ones) outside ADE20K-847 with its synonyms, 51.2% (73.6%) outside the 17,001-name lexicon. Most common added names:
  shadow, shrub, cloud, roof, asphalt, balcony, picture frame (results/freeform_names_ade/REPORT.md).
- Store checks (--check, first 3 images): native at 150 names and the anchored source columns equal the stored scores to
  one float16 step (max 0.0078 logit; mean below 1e-6) for CAT-Seg ViT-L, SED and FC-CLIP (check.json per run).
- Scoring and analyses: one GPU job at a time on the RTX 5070 Ti.
