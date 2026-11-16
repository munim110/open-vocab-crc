#!/usr/bin/env bash
# Stage A data acquisition for Pascal Context 59 subset 459.
# Label-free with respect to the experiment: this only puts files on disk.
. "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
set -x
mkdir -p "$ROOT/data/pascal"
cd "$ROOT/data/pascal"
wget -c -q --show-progress --progress=dot:giga \
  https://thor.robots.ox.ac.uk/pascal/VOC/voc2010/VOCtrainval_03-May-2010.tar
wget -c -q --show-progress --progress=dot:giga \
  https://cs.stanford.edu/~roozbeh/pascal-context/trainval.tar.gz
wget -c https://cs.stanford.edu/~roozbeh/pascal-context/labels.txt
wget -c https://cs.stanford.edu/~roozbeh/pascal-context/33_labels.txt
# The 59-class list is not published as a file at that URL. It is a strict
# name-subset of the 459 list; the copy used for the published results is
# committed at meta/pascal_59_labels.txt and installed here.
cp -n "$ROOT/meta/pascal_59_labels.txt" 59_labels.txt
ls -la
echo "--- extracting ---"
tar xf VOCtrainval_03-May-2010.tar
tar xzf trainval.tar.gz
echo "--- inventory ---"
ls VOCdevkit/VOC2010/ 2>/dev/null
ls trainval | head -3
ls trainval | wc -l
wc -l VOCdevkit/VOC2010/ImageSets/Segmentation/*.txt 2>/dev/null
echo "--- required files ---"
for f in labels.txt 59_labels.txt VOCdevkit/VOC2010/JPEGImages trainval; do
  [ -e "$f" ] && echo "ok       $f" || echo "MISSING  $f"
done
echo FETCH_PASCAL_DONE
