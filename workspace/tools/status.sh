#!/bin/bash
# status.sh [bN] (7 Nov 2026): the page's state, printed only from the files - status messages to the owner are this printout,
# quoted, not written from memory. Each line names the file it comes from.
B=${1:-$(ls -d /home/claude/mm/build-35/b[0-9]* | sed 's/.*\/b//' | sort -n | tail -1 | sed 's/^/b/')}; D=/home/claude/mm/build-35/$B
echo "== $B, at $(date '+%d %b %H:%M') =="
for f in checks2/SUMMARY.txt checks/SUMMARY.txt; do [ -f $D/$f ] && { echo "-- $D/$f (last 6 lines):"; tail -6 $D/$f; }; done
[ -f $D/checks2/GATE-EARLY-PASSED ] && echo "-- early gate: PASSED ($D/checks2/GATE-EARLY-PASSED: $(cat $D/checks2/GATE-EARLY-PASSED))" || echo "-- early gate: not passed yet (no $D/checks2/GATE-EARLY-PASSED)"
[ -f $D/shots/READY ] && echo "-- screenshots: ready ($(ls $D/shots/*.png 2>/dev/null | wc -l) parts)" || echo "-- screenshots: not taken yet"
[ -f $D/REVIEW-BRIEF.md ] && echo "-- review brief: made" || echo "-- review brief: not made yet"
[ -f $D/REVIEW.md ] && echo "-- review: $(grep -E '^(NOT CHECKED|FAULTS):' $D/REVIEW.md | tr '\n' ' ')" || echo "-- review: not written yet"
[ -f $D/gate-full.txt ] && echo "-- gate: $(tail -1 $D/gate-full.txt)" || echo "-- gate: full run not done"
echo "-- free disk: $(df -h /home/claude | awk 'NR==2{print $4}')"
