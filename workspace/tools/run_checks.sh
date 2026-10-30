#!/bin/bash
# run_checks.sh <checks dir> <package.zip> <out dir> [widths for the 122-width check, default all]
# 30 Oct 2026 (owner 11:54: "implement all 8" - item 5). Runs the first-build checks with the SAME tools, unchanged:
#   side by side: the 122 widths (vfast.py), the height (stable.py at 1440 and 390), lines through text (lines.py at 8 widths);
#   then ALONE, after they finish: the speed check (speed_check.py) - other checks running at the same time would slow the
#   machine and distort its timings.
# Every check still runs; nothing is skipped. Each writes its own file in <out dir>; SUMMARY.txt lists their last lines.
set -u
C=$(cd "$1" && pwd); Z=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); O=$3; WID=${4:-all}
mkdir -p "$O"; O=$(cd "$O" && pwd)
echo "start $(date '+%H:%M:%S')  package sha256 $(sha256sum "$Z" | cut -c1-16)" > "$O/SUMMARY.txt"
# 1. the 122 widths
python3 "$C/vfast.py" "$C" "$Z" "$O/full.txt" 2 "$WID" > "$O/full.log" 2>&1 & P1=$!
# 2. the height
( for w in 1440 390; do echo "width $w: $(python3 "$C/stable.py" $w "$Z" 2>&1 | tail -1)"; done ) > "$O/height.txt" 2>&1 & P2=$!
# 3. lines through text, on the package served locally
T=$(mktemp -d); unzip -q "$Z" -d "$T"; SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
python3 -m http.server 0 --bind 127.0.0.1 --directory "$T" > "$T.port" 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' "$T.port" | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
( for w in 320 390 430 641 700 830 1024 1440; do python3 "$C/lines.py" "http://127.0.0.1:$PORT/$SLUG/" $w 2>&1 | tail -1; done ) > "$O/lines.txt" 2>&1 & P3=$!
wait $P1; E1=$?; wait $P2; wait $P3; kill $PS 2>/dev/null; rm -rf "$T" "$T.port"
echo "side-by-side checks done $(date '+%H:%M:%S')" >> "$O/SUMMARY.txt"
# 4. the speed check, alone
python3 "$C/speed_check.py" "$Z" > "$O/speed.txt" 2>&1; E4=$?
{ echo "122 widths (exit $E1): $(tail -1 "$O/full.txt" 2>/dev/null)"; echo "height:"; cat "$O/height.txt"; echo "lines through text:"; cat "$O/lines.txt";
  echo "speed (exit $E4): $(tail -1 "$O/speed.txt")"; echo "end $(date '+%H:%M:%S')"; } >> "$O/SUMMARY.txt"
cat "$O/SUMMARY.txt"
