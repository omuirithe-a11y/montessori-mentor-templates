#!/bin/bash
# run_checks.sh <checks dir> <package.zip> <out dir> [widths for the 122-width check, default all] [--rows-one-width]
# 5 Nov 2026 16:0x: runs the scripts the agreed list names (REQUIRED-CHECKS rows): lines_v2.py (was lines.py) and v8/place_check.py (was place_check.py v1); the 122-width check is the checks dir given (tools-v5-fixA-200 since the owner's 09:16 and 16:05 agreements).
# 30 Oct 2026 (owner 11:54: "implement all 8" - item 5). Runs the first-build checks with the SAME tools, unchanged:
#   one after another, nothing else running (30 Oct 13:5x, lessons 15 and 40: the machine has 2 processors; more browsers at
#   once is not faster): the 122 widths (vfast.py, 2 workers), the height (stable.py at 1440 and 390), lines through text
#   (lines.py at 8 widths), then the speed check (speed_check.py).
# Every check still runs; nothing is skipped. Each writes its own file in <out dir>; SUMMARY.txt lists their last lines.
set -u
C=$(cd "$1" && pwd); Z=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); O=$3; WID=${4:-all}; ROWSARG=${5:-}; G=$(dirname "$(readlink -f "$0")")
mkdir -p "$O"; O=$(cd "$O" && pwd)
echo "start $(date '+%H:%M:%S')  package sha256 $(sha256sum "$Z" | cut -c1-16)" > "$O/SUMMARY.txt"
# 1. the 122 widths
python3 "$C/vfast.py" "$C" "$Z" "$O/full.txt" 2 "$WID" > "$O/full.log" 2>&1; E1=$?
# 2. the height
( for w in 1440 390; do echo "width $w: $(python3 "$C/stable.py" $w "$Z" 2>&1 | tail -1)"; done ) > "$O/height.txt" 2>&1
# 3. lines through text, on the package served locally
T=$(mktemp -d); unzip -q "$Z" -d "$T"; SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
python3 -m http.server 0 --bind 127.0.0.1 --directory "$T" > "$T.port" 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' "$T.port" | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
( for w in 320 390 430 641 700 830 1024 1440; do python3 "$G/lines_v2.py" "http://127.0.0.1:$PORT/$SLUG/" $w 2>&1 | tail -1; done ) > "$O/lines.txt" 2>&1
kill $PS 2>/dev/null; rm -rf "$T" "$T.port"
echo "widths, height and lines done $(date '+%H:%M:%S')" >> "$O/SUMMARY.txt"
# 4. placement (30 Oct 13:5x): images inside the text column, image tops level with the first line, rows (place_check.py)
python3 "$G/v8/place_check.py" "$Z" $ROWSARG > "$O/place.txt" 2>&1; E5=$?
# 5. the speed check
python3 "$C/speed_check.py" "$Z" > "$O/speed.txt" 2>&1; E4=$?
{ echo "122 widths (exit $E1): $(tail -1 "$O/full.txt" 2>/dev/null)"; echo "height:"; cat "$O/height.txt"; echo "lines through text:"; cat "$O/lines.txt";
  echo "placement (exit $E5): $(tail -1 "$O/place.txt")"; echo "speed (exit $E4): $(tail -1 "$O/speed.txt")"; echo "end $(date '+%H:%M:%S')"; } >> "$O/SUMMARY.txt"
cat "$O/SUMMARY.txt"
