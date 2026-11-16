#!/bin/bash
# ADE20K acquisition. Two separate releases are needed; they share the same
# 2000 validation filenames (ADE_val_%08d) but are distributed independently.
#
#   1. ADEChallengeData2016  -- the A-150 label space. Public, no registration.
#   2. ADE20K_2021_17_01     -- the full release, from which the A-847 label
#                               space is decoded. Behind a registration wall at
#                               MIT, so we use the public HF parquet mirror.
#
# Both are fetched automatically and checksum-verified.
. "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
set -x
mkdir -p "$ROOT/data"
cd "$ROOT/data"

# --- 1. ADEChallengeData2016 (SceneParse150), 967382037 bytes ----------------
wget -c -q --show-progress --progress=dot:giga \
  "http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip"
echo "7ff1be44964418441f542a7cc1e1a650e7dc0fc275f5d23252bc9bbdbc977b29  ADEChallengeData2016.zip" \
  | sha256sum -c - || { echo "CHECKSUM MISMATCH"; exit 1; }
unzip -q -n ADEChallengeData2016.zip
ls ADEChallengeData2016/

# --- 2. ADE20K full (ADE20K_2021_17_01), validation split -------------------
# The MIT full release is behind a registration wall, but the 2021_17_01 export
# is mirrored on the Hugging Face Hub as parquet by 1aurent/ADE20K -- public,
# ungated, BSD, and byte-stable. data/ade_full_val.parquet is that repository's
# data/validation-00000-of-00001.parquet, renamed. 2000 rows, 473665979 bytes.
#
# The mirror is a convenience, not a relicensing: the underlying terms are still
# MIT CSAIL's. See THIRD_PARTY.md.
URL="https://huggingface.co/datasets/1aurent/ADE20K/resolve/main/data/validation-00000-of-00001.parquet"
SHA="3da40ee1eb5d7988f62f58abbe10f69fb1684a95bed613332833e6a4fe08b50a"
if [ ! -f ade_full_val.parquet ]; then
  wget -c -q --show-progress --progress=dot:giga "$URL" -O ade_full_val.parquet.part
  echo "$SHA  ade_full_val.parquet.part" | sha256sum -c - \
    || { echo "CHECKSUM MISMATCH -- not renaming"; exit 1; }
  mv ade_full_val.parquet.part ade_full_val.parquet
else
  echo "$SHA  ade_full_val.parquet" | sha256sum -c -
fi

echo FETCH_ADE_DONE
