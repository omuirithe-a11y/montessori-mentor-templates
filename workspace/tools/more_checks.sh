#!/bin/bash
# more_checks.sh <build dir> <out dir> <page settings .py> <Word .docx> <PDF> <template .html> <menu reference index.html>
# (5 Nov 2026, owner 09:27 "this work is too slow make it faster. read and implement lessonslearned")
# The checks run_checks.sh does not run, one after another with nothing else beside them (lessons 15, 40): the Word format
# check, the column check, the text, code, style, images and wrap checks. Every check runs; nothing skipped (lesson 44).
# 6 Nov 2026 (gatefix2, installed under the owner's 6 Nov 06:54 agreement):
#  - D090: the page is taken from the input - settings, Word file, PDF, template and menu reference are arguments; no page
#    name is written here (the build folder's zip gives the page's folder name).
#  - D040/C025: every check reads the build's upload zip itself (format, code, code-against-Word) or a copy unpacked from it
#    (the browser checks), not a CHECK-ONLY copy and not preview/; SUMMARY.txt names the zip and its sha256 (16 characters)
#    and says the browser checks read a copy unpacked from it. The unpacked copy is deleted at the end.
#  - rows naming strip_compare(_nolive).py and spacecheck.py: their results are written here (checks2/strip-nolive.txt,
#    checks2/space.txt); before, no runner wrote them.
# 6 Nov 2026 (owner 07:16 "implement all 6 immediately", items 1, 2, 5): stage 8th argument, "fast" (default) or "long".
#  fast: the code check, then the quick checks, the tablet check (new) and the spacing check, in that order; the run STOPS at
#        the first step that does not pass (tools/round_judge.py; allowed faults AF001/AF002 judged as the gate judges them).
#        When all pass it writes <out>/FAST-PASSED with the package sha256.
#  long: the images checks and the wrap check. REFUSES to start unless <out>/FAST-PASSED names this package and the build
#        folder holds a separate review report (REVIEW.md) newer than the package, naming the package sha256 and ending
#        "FAULTS: 0". Stops at the first step that does not pass.
#  Both: a step whose result file is newer than the package and every script, and passes, is not run again (after a
#        restart the round picks up where it stopped); the SUMMARY line says "kept".
set -u
[ $# -ge 7 ] || { echo "usage: more_checks.sh <build dir> <out dir> <settings.py> <Word.docx> <PDF> <template.html> <menu reference index.html> [fast|long]"; exit 2; }
STAGE=${8:-fast}
B=$(cd "$1" && pwd); O=$2; mkdir -p "$O"; O=$(cd "$O" && pwd); M=/home/claude/mm
SET=$3; DOCX=$4; PDF=$5; TPL=$6; MENU=$7
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$')
[ "$(echo "$Z" | grep -c .)" = 1 ] || { echo "not one upload zip in $B: $Z"; exit 2; }
SHA=$(sha256sum "$Z" | cut -c1-16); SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT; unzip -q "$Z" -d "$T/zip"; P=$T/zip/$SLUG
[ -f "$B/report.json" ] && cp "$B/report.json" "$T/zip/report.json"   # 6 Nov 07:38: the style check reads the build's report (beige lines placed from Word) next to the page folder
[ -f $O/SUMMARY.txt ] && head -1 $O/SUMMARY.txt | grep -q "package sha256 $SHA" || echo "start $(date +%H:%M:%S)  package sha256 $SHA  $(basename "$Z")" > $O/SUMMARY.txt
grep -q "^browser checks read a copy unpacked" $O/SUMMARY.txt || echo "browser checks read a copy unpacked from $(basename "$Z") sha256 $SHA (not preview/)" >> $O/SUMMARY.txt
echo "stage $STAGE start $(date +%H:%M:%S)" >> $O/SUMMARY.txt
PAGE=$(basename "$SET" .py)
fresh() {   # fresh <result file> <scripts...>: newer than the package and every script given
  local r=$1; shift; [ -s "$r" ] || return 1; [ "$r" -nt "$Z" ] || return 1
  for x in "$@"; do [ "$r" -nt "$x" ] || return 1; done; return 0; }
step() {   # step <judge step> <label> <result file> <scripts (for freshness)> -- <command...>
  local js=$1 label=$2 res=$3; shift 3; local deps=(); while [ "$1" != "--" ]; do deps+=("$1"); shift; done; shift
  if fresh "$res" "${deps[@]}" && python3 $M/tools/round_judge.py $js "$res" $PAGE > /dev/null 2>&1; then
    echo "$label: kept (passed $(date -r "$res" +%H:%M:%S)) $(tail -2 "$res" | grep -v '^END' | tail -1)" >> $O/SUMMARY.txt; return 0; fi
  "$@"
  local j; j=$(python3 $M/tools/round_judge.py $js "$res" $PAGE 2>&1); local e=$?
  echo "$label: $(tail -2 "$res" 2>/dev/null | grep -v '^END' | tail -1)  [$j]" >> $O/SUMMARY.txt
  if [ $e -ne 0 ]; then echo "STOPPED at $label $(date +%H:%M:%S): $j" >> $O/SUMMARY.txt; cat $O/SUMMARY.txt; exit 1; fi; }
if [ "$STAGE" = fast ]; then
  rm -f $O/FAST-PASSED
  step strip "code against template and Word" $O/strip-nolive.txt $M/tools/v8/strip_compare_nolive.py "$TPL" -- sh -c "python3 -I $M/tools/v8/strip_compare_nolive.py \"$TPL\" \"$Z\" \"$DOCX\" \"$MENU\" \"/$SLUG/\" > $O/strip-nolive.txt 2>&1"
  step static "code (static)" $O/static.txt $M/tools/static_code.py "$TPL" -- sh -c "python3 $M/tools/static_code.py \"$Z\" \"$TPL\" $O/static.txt > $O/static.log 2>&1"
  step format "format (Word)" $O/format-word.txt $M/tools/v8/format_check_word.py "$SET" -- sh -c "python3 $M/tools/v8/format_check_word.py \"$Z\" \"$DOCX\" --settings \"$SET\" > $O/format-word.txt 2>&1"
  step columns "columns" $O/col.txt $M/tools/col_check.py "$SET" -- sh -c "python3 $M/tools/col_check.py \"$PDF\" \"$P\" --settings \"$SET\" > $O/col.txt 2>&1"
  step text "text" $O/text.log $M/tools/text_rules.py "$SET" -- sh -c "python3 $M/tools/text_rules.py \"$P\" \"$DOCX\" $O/text --settings \"$SET\" > $O/text.log 2>&1"
  step style "style" $O/style.txt $M/tools/style_rules.py "$TPL" -- sh -c "python3 $M/tools/style_rules.py \"$P\" \"$TPL\" $O/style.txt > $O/style.log 2>&1"
  step tablet "tablet (641-830)" $O/tablet.txt $M/tools/tablet_check.py -- sh -c "python3 $M/tools/tablet_check.py \"$P\" $O/tablet.txt > $O/tablet.log 2>&1"
  step space "spacing (13 widths)" $O/space.txt $M/tools/spacecheck.py -- sh -c "python3 $M/tools/spacecheck.py \"$DOCX\" \"$PDF\" \"$P\" \"$T/space\" > $O/space.log 2>&1; cp \"$T/space/spacecheck.txt\" $O/space.txt 2>>$O/space.log"
  echo "package sha256 $SHA $(date +%H:%M:%S)" > $O/FAST-PASSED
  echo "FAST CHECKS PASSED $(date +%H:%M:%S) - next: the gate (early run), then the separate review, then: more_checks.sh ... long, and run_checks.sh" >> $O/SUMMARY.txt
else
  [ -f $O/FAST-PASSED ] && grep -q "package sha256 $SHA" $O/FAST-PASSED || { echo "REFUSED $(date +%H:%M:%S): the fast checks have not passed for this package ($SHA)" | tee -a $O/SUMMARY.txt; exit 3; }
  RV=$B/REVIEW.md
  { [ -f "$RV" ] && [ "$RV" -nt "$Z" ] && grep -q "$SHA" "$RV" && [ "$(grep -v '^[[:space:]]*$' "$RV" | tail -1)" = "FAULTS: 0" ]; } || { echo "REFUSED $(date +%H:%M:%S): no separate review report for this package with FAULTS: 0 ($RV)" | tee -a $O/SUMMARY.txt; exit 3; }
  step images "images (heights, 122 widths)" $O/images.txt $M/tools/images_behaviour.py -- sh -c "python3 $M/tools/images_behaviour.py \"$P\" $O/images.txt full heights > $O/images.log 2>&1"
  step images2 "images (swipe, late, behaviour)" $O/images-2.txt $M/tools/images_behaviour.py -- sh -c "python3 $M/tools/images_behaviour.py \"$P\" $O/images-2.txt full swipe,late,behaviour > $O/images-2.log 2>&1"
  step wrap "wrap (1 px, 320-1920)" $O/wrap.txt $M/tools/wrap_sweep.py -- sh -c "python3 $M/tools/wrap_sweep.py \"$P\" \"$DOCX\" $O/wrap.txt 320 1920 1 > $O/wrap.log 2>&1"
  echo "LONG CHECKS (more_checks) PASSED $(date +%H:%M:%S)" >> $O/SUMMARY.txt
fi
echo "end $(date +%H:%M:%S)" >> $O/SUMMARY.txt; cat $O/SUMMARY.txt
