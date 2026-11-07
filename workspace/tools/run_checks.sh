#!/bin/bash
# run_checks.sh <checks dir> <package.zip> <out dir> [widths for the 122-width check, default all] [--rows-one-width]
# 5 Nov 2026 16:0x: runs the scripts the agreed list names (REQUIRED-CHECKS rows): lines_v2.py (was lines.py) and v8/place_check.py (was place_check.py v1); the 122-width check is the checks dir given (tools-v5-fixA-200 since the owner's 09:16 and 16:05 agreements).
# 30 Oct 2026 (owner 11:54: "implement all 8" - item 5). Runs the first-build checks with the SAME tools, unchanged:
#   one after another, nothing else running (30 Oct 13:5x, lessons 15 and 40: the machine has 2 processors; more browsers at
#   once is not faster): the 122 widths (vfast.py, 2 workers), the height (stable.py at 1440 and 390), lines through text
#   (lines.py at 8 widths), then the speed check (speed_check.py).
# Every check still runs; nothing is skipped. Each writes its own file in <out dir>; SUMMARY.txt lists their last lines.
# 6 Nov 2026 (owner 07:16 "implement all 6 immediately", items 1 and 5): these are LONG checks. The script REFUSES to start
#   unless the fast checks passed for this package (<build>/checks2/FAST-PASSED, written by more_checks.sh ... fast) and the
#   build folder holds a separate review report (REVIEW.md) newer than the package, naming its sha256 and whose last line is
#   "FAULTS: 0". It STOPS at the first step that does not pass (tools/round_judge.py), and a step whose result is newer
#   than the package and its scripts and passes is kept, not run again (after a restart it picks up where it stopped).
set -u
C=$(cd "$1" && pwd); Z=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); O=$3; WID=${4:-all}; ROWSARG=${5:-}; G=$(dirname "$(readlink -f "$0")")
mkdir -p "$O"; O=$(cd "$O" && pwd); BD=$(dirname "$Z"); SHA=$(sha256sum "$Z" | cut -c1-16)
[ -f "$BD/checks2/FAST-PASSED" ] && grep -q "package sha256 $SHA" "$BD/checks2/FAST-PASSED" || { echo "REFUSED $(date '+%H:%M:%S'): the fast checks have not passed for this package ($SHA)"; exit 3; }
[ -f "$BD/checks2/GATE-EARLY-PASSED" ] && grep -q "package sha256 $SHA" "$BD/checks2/GATE-EARLY-PASSED" || { echo "REFUSED $(date '+%H:%M:%S'): the gate's early run has not passed for this package ($SHA) (7 Nov 2026, S1 refined)"; exit 3; }
RV=$BD/REVIEW.md
# 7 Nov 2026 (owner 11:18, "yes": "run_checks.sh may start before the separate review has finished, while the review only reads files, and ... a page fault the review finds means a new build and new checks as before"): with MM_BEFORE_REVIEW=1 it starts while this build's review is still being written (no REVIEW.md yet, the brief names this package); the review is still required by the gate (screens file) and by the long round
if [ "${MM_BEFORE_REVIEW:-}" = "1" ] && [ ! -f "$RV" ] && grep -q "$SHA" "$BD/REVIEW-BRIEF.md" 2>/dev/null; then echo "started before the review (owner 11:18 yes) $(date +%H:%M:%S)"; else
{ [ -f "$RV" ] && [ "$RV" -nt "$Z" ] && grep -q "$SHA" "$RV" && [ "$(grep -v '^[[:space:]]*$' "$RV" | tail -1)" = "FAULTS: 0" ]; } || { echo "REFUSED $(date '+%H:%M:%S'): no separate review report for this package with FAULTS: 0 ($RV)"; exit 3; }
{ [ -f "$(dirname "$RV")/REVIEW-BRIEF.md" ] && [ "$RV" -nt "$(dirname "$RV")/REVIEW-BRIEF.md" ] && grep -q "BRIEF $(basename "$(dirname "$RV")")/REVIEW-BRIEF.md" "$RV"; } || { echo "REFUSED $(date +%H:%M:%S): the review report does not come from the brief tools/review_brief.sh wrote for this build (7 Nov 2026, S8)"; exit 3; }
fi
[ -f "$O/SUMMARY.txt" ] && head -1 "$O/SUMMARY.txt" | grep -q "package sha256 $SHA" || echo "start $(date '+%H:%M:%S')  package sha256 $SHA" > "$O/SUMMARY.txt"
fresh() { local r=$1; shift; [ -s "$r" ] || return 1; [ "$r" -nt "$Z" ] || return 1; for x in "$@"; do [ "$r" -nt "$x" ] || return 1; done; return 0; }
judge() {   # judge <step> <file> <label>: record; stop the round on a fault
  local j; j=$(python3 "$G/round_judge.py" $1 "$2" 2>&1); local e=$?
  echo "$3: $(tail -1 "$2" 2>/dev/null)  [$j]" >> "$O/SUMMARY.txt"
  [ $e -eq 0 ] || { echo "STOPPED at $3 $(date '+%H:%M:%S'): $j" >> "$O/SUMMARY.txt"; cat "$O/SUMMARY.txt"; exit 1; }; }
kept() { python3 "$G/round_judge.py" $1 "$2" > /dev/null 2>&1 && fresh "$2" "${@:3}"; }
# 7 Nov 2026 (owner "implement all of these changes"; review of the S-list: run_checks.sh had no proof refusal): every check script
# this runner uses must have a proof on a deliberately broken copy in tools/check-proofs.json (runner vfast.py exempt, as in more_checks.sh)
for s_ in "$C/stable.py" "$G/lines_v2.py" "$G/v8/place_check.py" "$C/speed_check.py"; do
  python3 -c "import json,hashlib,sys;h=hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest();d=json.load(open('$G/check-proofs.json'));sys.exit(0 if any(isinstance(v,dict) and v.get('code')==h for v in d.values()) else 1)" "$s_" || { echo "STOPPED at proofs $(date '+%H:%M:%S'): REFUSED - $(basename "$s_") (this version) has no proof in tools/check-proofs.json" >> "$O/SUMMARY.txt"; cat "$O/SUMMARY.txt"; exit 1; }
done
# 1. the 122 widths
# 6 Nov 2026 (owner 09:25 "#3 to #16 ... implement"): (#4) the widths that failed on the previous build run first, so a fault
# still there stops the round in seconds; (#5) widths a stopped run already finished on THIS package (the vfast-*/w*.out lines
# in this folder) are kept, not run again. Every width still runs on this package.
if ! kept widths "$O/full.txt" "$C/vfast.py"; then
  PREVB=$(ls -d "$(dirname "$BD")"/b[0-9]* 2>/dev/null | sed 's/.*\/b//' | grep -E '^[0-9]+$' | sort -n | awk -v me="$(basename "$BD" | sed 's/^b//')" '$1<me' | tail -1)
  PF="$(dirname "$BD")/b$PREVB/checks/full.txt"
  FW=$( [ -n "$PREVB" ] && [ -f "$PF" ] && grep -E '^ *[0-9]+ FAULT' "$PF" | awk '{print $1}' | paste -sd, - )
  if [ -n "$FW" ]; then
    python3 "$C/vfast.py" "$C" "$Z" "$O/full-first.txt" 2 "$FW" > "$O/full-first.log" 2>&1
    judge widths "$O/full-first.txt" "122 widths: the widths that failed on build b$PREVB first ($FW)"
  fi
  SK=$(mktemp -d); for vd in "$O"/vfast-*; do [ -d "$vd" ] && [ "$vd" -nt "$Z" ] && cat "$vd"/w*.out 2>/dev/null; done | grep -E '^ *[0-9]+ (ok|FAULT)' > "$SK/part01.txt" || true
  if [ -s "$SK/part01.txt" ]; then SKA="--skip-done $SK"; else SKA=""; fi   # only runs made after this package was built
  python3 "$C/vfast.py" "$C" "$Z" "$O/full.txt" 2 "$WID" $SKA > "$O/full.log" 2>&1; rm -rf "$SK"
fi
judge widths "$O/full.txt" "122 widths"
# 2. the height (the gate's rule: 1 s = 4 s = after scrolling at 1440 and 390, no margin over 150 px)
kept height "$O/height.txt" "$C/stable.py" || { ( for w in 1440 390; do echo "width $w: $(python3 "$C/stable.py" $w "$Z" 2>&1 | tail -1)"; done ) > "$O/height.txt" 2>&1; }; judge height "$O/height.txt" "height"
# 3. lines through text, on the package served locally
if ! kept lines "$O/lines.txt" "$G/lines_v2.py"; then
T=$(mktemp -d); unzip -q "$Z" -d "$T"; SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
python3 -m http.server 0 --bind 127.0.0.1 --directory "$T" > "$T.port" 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' "$T.port" | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
( for w in 320 390 430 641 700 830 1024 1440; do python3 "$G/lines_v2.py" "http://127.0.0.1:$PORT/$SLUG/" $w 2>&1 | tail -1; done ) > "$O/lines.txt" 2>&1
kill $PS 2>/dev/null; rm -rf "$T" "$T.port"; fi
judge lines "$O/lines.txt" "lines through text"
# 4. placement
kept place "$O/place.txt" "$G/v8/place_check.py" || { python3 "$G/v8/place_check.py" "$Z" $ROWSARG > "$O/place.txt" 2>&1; }; judge place "$O/place.txt" "placement"
# 5. the speed check (alone)
kept speed "$O/speed.txt" "$C/speed_check.py" || { python3 "$C/speed_check.py" "$Z" > "$O/speed.txt" 2>&1; }; judge speed "$O/speed.txt" "speed"
E_=$(date '+%H:%M:%S'); echo "LONG CHECKS (run_checks) PASSED $E_" >> "$O/SUMMARY.txt"; echo "end $E_" >> "$O/SUMMARY.txt"   # 7 Nov 2026 (owner's agreement): the end line on a line of its own (gate rows D035/D036)
cat "$O/SUMMARY.txt"
