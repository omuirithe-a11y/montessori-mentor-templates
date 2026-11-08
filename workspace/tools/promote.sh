#!/bin/bash
# promote.sh <builds folder> <bN>   (8 Nov 2026, owner "built the three", items 1 and 2)
# A numbered build is made only from a trial build (<builds>/try) whose fast round PASSED - every fast check ran to the end with no
# fault (checks2/FAST-PASSED names the trial's own zip). The build guard runs as for any numbered build (the previous build's round
# and review, the gate plan, the fingerprints, a stated cause), then the trial folder becomes <builds>/<bN>.
set -u; D=$1; N=$2; T="$D/try"
case "$N" in b[0-9]*) ;; *) echo "PROMOTE REFUSED: $N is not a build number (b<N>)"; exit 3;; esac
[ -d "$T" ] || { echo "PROMOTE REFUSED: no trial build $T"; exit 3; }
[ -e "$D/$N" ] && { echo "PROMOTE REFUSED: $D/$N already exists"; exit 3; }
Z=$(ls "$T"/*.zip 2>/dev/null | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1)
[ -n "$Z" ] || { echo "PROMOTE REFUSED: the trial has no upload zip"; exit 3; }
SHA=$(sha256sum "$Z" | cut -c1-16)
grep -q "package sha256 $SHA" "$T/checks2/FAST-PASSED" 2>/dev/null || { echo "PROMOTE REFUSED: the trial's fast round has not passed for its zip ($SHA) - see $T/checks2/SUMMARY.txt and FAULTS.txt"; exit 3; }
PROMOTING=1 bash /home/claude/mm/tools/build_guard.sh "$D" "$N" || { echo "PROMOTE REFUSED by the build guard (above)"; exit 3; }
mv "$T" "$D/$N" && echo "promoted: $T -> $D/$N (zip $SHA, fast round passed)"
