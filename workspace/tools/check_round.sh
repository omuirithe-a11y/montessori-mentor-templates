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
  # 8 Nov 2026 (owner "yes" to the decisions audit, claude/DECISIONS-AUDIT-8nov.md): the 524-item list (gate_list.py, its early run, the gate plan) is no longer run or required
  echo "FAST ROUND PASSED $(date +%H:%M:%S). Next: the separate review of this package (writes $B/REVIEW.md), then: check_round.sh ... long"
else
  bash $M/tools/run_checks.sh "$C" "$Z" "$B/checks" || { echo "ROUND STOPPED in run_checks.sh"; exit 1; }
  bash $M/tools/more_checks.sh "$B" "$B/checks2" "$SET" "$DOCX" "$PDF" "$TPL" "$MENU" long > "$B/long.log" 2>&1 || { echo "ROUND STOPPED in the long checks:"; tail -3 "$B/checks2/SUMMARY.txt"; exit 1; }
  echo "LONG ROUND PASSED $(date +%H:%M:%S). Next: the gate's full run with the review report."
fi
