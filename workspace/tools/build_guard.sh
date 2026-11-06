#!/bin/bash
# build_guard.sh <builds folder> <new build name>
# 6 Nov 2026 (owner 08:01 "analyse the effectiveness ... then adjust"; BUILD-ORDER item 5/6): a new build is refused while the
# newest build's check round is unfinished - the fast round must have STOPPED at a fault or PASSED, and if it passed, a
# separate review report (REVIEW.md, naming the package sha256) must exist. So every fault a round finds is fixed together in
# ONE new build, not one build per fix. Override only with the owner's words in <builds>/<new>.override.txt.
set -u; D=$1; N=$2
[ -s "$D/$N.override.txt" ] && { echo "build guard: override by the owner's words in $D/$N.override.txt"; exit 0; }
P=$(ls -d "$D"/b[0-9]* 2>/dev/null | sed 's/.*\/b//' | grep -E '^[0-9]+$' | sort -n | tail -1); [ -z "$P" ] && exit 0
B="$D/b$P"; S="$B/checks2/SUMMARY.txt"
[ -f "$S" ] || { echo "BUILD REFUSED: build b$P has no check round (run tools/check_round.sh ... fast on it first)"; exit 3; }
grep -q "^STOPPED at" "$S" && { echo "build guard: b$P's round stopped at a fault - fix every fault found, then build $N"; exit 0; }
grep -q "^FAST CHECKS PASSED" "$S" || { echo "BUILD REFUSED: build b$P's fast round has not finished"; exit 3; }
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1); SHA=$(sha256sum "$Z" | cut -c1-16)
[ -f "$B/REVIEW.md" ] && grep -q "$SHA" "$B/REVIEW.md" || { echo "BUILD REFUSED: build b$P passed its fast round but has no separate review report naming $SHA"; exit 3; }
echo "build guard: b$P checked and reviewed - build $N"
