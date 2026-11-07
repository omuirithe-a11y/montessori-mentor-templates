#!/bin/bash
# check_round.sh <build dir> <settings.py> <Word.docx> <PDF> <template.html> <menu reference index.html> <122-width checks dir> <page slug> [fast|long]
# 6 Nov 2026 (owner 07:16 "implement all 6 immediately", item 1; her 07:19 and 07:28 messages): one check round in the agreed order.
#  fast: 1. more_checks.sh fast (code check, static code, Word format, columns, text, style, tablet, spacing - stops at the
#           first fault);
#        2. the gate, early run (gate_list.py, review NONE): the round STOPS if the gate shows integrity faults or a FAULT row
#           whose result is one of the fast results (the rows that wait for the long checks or the review are expected to be
#           open here, and are listed, not judged);
#        then it says: run the separate review now (an agent that has not seen the work writes <build>/REVIEW.md).
#  long: refuses without the fast pass and a review report for the package (the runners check this themselves), then
#        run_checks.sh (122 widths, height, lines, placement, speed) and more_checks.sh long (images, wrap), each stopping
#        at the first fault; then the gate's full run.
set -u
B=$(cd "$1" && pwd); SET=$2; DOCX=$3; PDF=$4; TPL=$5; MENU=$6; C=$7; PAGE=$8; STAGE=${9:-fast}; M=/home/claude/mm
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$')
bash $M/tools/roundlock.sh check || exit 3; export MM_ROUND_LOCK=$$; bash $M/tools/roundlock.sh take $$; trap 'bash $M/tools/roundlock.sh release $$' EXIT   # 7 Nov 2026 (S7)
if [ "$STAGE" = fast ]; then
  # 6 Nov (owner 10:53 "yes", lessons list item 1): after a fast pass, the bulky files of builds older than the one before are cleared (records kept)
  bash $M/tools/more_checks.sh "$B" "$B/checks2" "$SET" "$DOCX" "$PDF" "$TPL" "$MENU" fast > "$B/fast.log" 2>&1 && bash $M/tools/clear_old_builds.sh "$(dirname "$B")" "$(basename "$B")" >> "$B/fast.log" 2>&1 || { echo "ROUND STOPPED in the fast checks:"; tail -3 "$B/checks2/SUMMARY.txt"; exit 1; }
  python3 $M/tools/gate_list.py "$Z" "$B" NONE "$B/checks2/gate-early.txt" --page "$PAGE" > /dev/null 2>&1
  # 7 Nov 2026 (owner "implement all of these changes", S1 refined): the early run used to stop on every build (the order
  # lines for the review and long checks, and rows met only by the gate itself) and nothing obeyed it; gate_early_judge.py
  # leaves those out, and only a pass writes checks2/GATE-EARLY-PASSED, which the review chain and the long runners require
  rm -f "$B/checks2/GATE-EARLY-PASSED"
  { echo "gate, early run $(date +%H:%M:%S): $(tail -2 "$B/checks2/gate-early.txt" | head -1)"; } >> "$B/checks2/SUMMARY.txt"
  EJ=$(python3 $M/tools/gate_early_judge.py "$B/checks2/gate-early.txt") || { echo "STOPPED at the gate's early run $(date +%H:%M:%S)" >> "$B/checks2/SUMMARY.txt"; echo "ROUND STOPPED at the gate's early run:"; echo "$EJ" | head -20; exit 1; }
  echo "package sha256 $(sha256sum "$Z" | cut -c1-16) $(date +%H:%M:%S)" > "$B/checks2/GATE-EARLY-PASSED"
  echo "gate, early run PASSED (gate_early_judge.py) $(date +%H:%M:%S)" >> "$B/checks2/SUMMARY.txt"
  bash $M/tools/gate_plan.sh "$B" "$PAGE" >> "$B/checks2/SUMMARY.txt" 2>&1   # 7 Nov 2026 (S1): the gate plan made fresh on every build
  echo "FAST ROUND PASSED $(date +%H:%M:%S). Next: the separate review of this package (writes $B/REVIEW.md), then: check_round.sh ... long"
else
  bash $M/tools/run_checks.sh "$C" "$Z" "$B/checks" || { echo "ROUND STOPPED in run_checks.sh"; exit 1; }
  bash $M/tools/more_checks.sh "$B" "$B/checks2" "$SET" "$DOCX" "$PDF" "$TPL" "$MENU" long > "$B/long.log" 2>&1 || { echo "ROUND STOPPED in the long checks:"; tail -3 "$B/checks2/SUMMARY.txt"; exit 1; }
  echo "LONG ROUND PASSED $(date +%H:%M:%S). Next: the gate's full run with the review report."
fi
