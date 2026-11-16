#!/usr/bin/env bash
# Validate that data/ holds everything the experiments read, and nothing is
# silently half-extracted. Exits non-zero if anything required is missing.
#
# Checks paths only -- it does not re-hash the multi-gigabyte archives.
. "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
cd "$ROOT"

fail=0
need() {  # need <path> <what reads it>
  if [ -e "$1" ]; then printf '  ok       %-46s %s\n' "$1" "$2"
  else printf '  MISSING  %-46s %s\n' "$1" "$2"; fail=1; fi
}
count() {  # count <dir> <expected> <what reads it>
  if [ -d "$1" ]; then
    n=$(ls "$1" 2>/dev/null | wc -l)
    if [ "$n" -eq "$2" ]; then printf '  ok       %-46s %s (%s files)\n' "$1" "$3" "$n"
    else printf '  WRONG N  %-46s %s (%s files, expected %s)\n' "$1" "$3" "$n" "$2"; fail=1; fi
  else printf '  MISSING  %-46s %s\n' "$1" "$3"; fail=1; fi
}

echo "ADE20K -- A-150 label space          (scripts/fetch_ade.sh)"
need data/ADEChallengeData2016/objectInfo150.txt        "src/labels.py"
count data/ADEChallengeData2016/images/validation 2000  "src/encode.py"
count data/ADEChallengeData2016/annotations/validation 2000 "src/build_gt.py"

echo "ADE20K -- A-847 label space          (scripts/fetch_ade.sh, HF mirror)"
need data/ade_full_val.parquet                          "src/build_gt.py"
need meta/register_ade20k_full.py                       "src/labels.py (committed)"

echo "ADE20K -- derived by src/build_gt.py"
count data/gt847 2000                                   "src/encode.py"

echo "Pascal Context                       (scripts/fetch_pascal.sh)"
need data/pascal/labels.txt                             "src/pascal_labels.py (459 names)"
need data/pascal/59_labels.txt                          "src/pascal_labels.py (59 names)"
need data/pascal/VOCdevkit/VOC2010/JPEGImages           "src/encode_pascal.py"
need data/pascal/trainval                               "src/encode_pascal.py (.mat LabelMap)"

echo "COCO-Stuff, LVIS, COCO instances     (scripts/fetch_coco_val.sh)"
count data/coco-stuff/images/val2017 5000               "src/exp_headroom_probe_coco.py, src/exp_ovd_probe.py"
need data/coco-stuff/annotations_detectron2/val2017     "src/build_pixel_sample.py --dataset coco"
need data/lvis/lvis_v1_val.json                         "src/coco_lvis_vocab.py, src/ovd_vocab.py"
need data/lvis/coco_to_synset.json                      "src/coco_lvis_vocab.py, src/ovd_vocab.py"
need data/coco/annotations/instances_val2017.json       "src/ovd_vocab.py (detection)"

echo "Ground truth at the sampled pixels   (src/build_pixel_sample.py)"
for c in sclip pascal_sclip coco_pixels; do
  need "cache/$c/meta.json"                             "the CRC analyses"
done

if [ "$fail" -eq 0 ]; then
  echo "all present"
else
  echo "SOMETHING IS MISSING -- see README.md, level cpu"
fi
exit $fail
