#!/bin/bash
# 8.0 build 1: the checks run_checks.sh does not run (lines_v2, format vs live, format vs Word, screenshots vs live), one after another
set -u; Z=$1; O=$2; M=/home/claude/mm; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
while pgrep -f place_check.py >/dev/null; do sleep 2; done
T=$(mktemp -d); unzip -q "$Z" -d "$T"; python3 -m http.server 0 --bind 127.0.0.1 --directory "$T" > "$T.port" 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' "$T.port" | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
echo "address http://127.0.0.1:$PORT/books-by-montessori/" > "$O/lines_v2.txt"
for w in 320 390 430 641 700 830 1024 1440; do python3 $M/tools/lines_v2.py "http://127.0.0.1:$PORT/books-by-montessori/" $w 2>&1 | tail -1; done >> "$O/lines_v2.txt"
kill $PS; rm -rf "$T" "$T.port"
python3 -I $C/format_check.py "$Z" /home/claude/res80/live81/books-by-montessori > "$O/format-live.txt" 2>&1
python3 -I $M/tools/v8/format_check_word.py "$Z" "$M/src/8.1/8.1 Books by Maria Montessori.docx" > "$O/format-word.txt" 2>&1
mkdir -p "$O/vslive"; python3 $M/tools/scratch-30oct/vslive.py "$Z" /home/claude/res80/live81/books-by-montessori "$O/vslive" > "$O/vslive.txt" 2>&1
echo DONE
