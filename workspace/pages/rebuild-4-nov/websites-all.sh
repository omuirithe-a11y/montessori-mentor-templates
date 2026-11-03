#!/bin/bash
# 8.4 Websites t3 (4 Nov, lesson 33 rebuild t3 on Resources template 4567809f): every check, one after another
set -u; cd /home/claude/mm; P=websites; B=build-res/$P/t4; Z=$B/build/$P.zip; O=$B/checks; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
T="templates/Resources Code Template.html"; D="src/8.4/8.4 Websites.docx"; mkdir -p $O
python3 -I tools/v8/strip_compare.py "$T" $Z live/$P/index.html > $O/code-live.txt 2>&1
python3 -I tools/v8/format_check_word.py $Z "$D" > $O/format-word.txt 2>&1
python3 -I $C/format_check.py $Z build-res/$P/livecopy/$P > $O/format-live.txt 2>&1
mkdir -p $B/space; SPACE_AGREED=build-res/websites/space-agreed.txt timeout 1500 python3 tools/spacecheck.py "$D" "${D%.docx}.pdf" $B/build/hostinger/$P $B/space > $B/space.log 2>&1; cp $B/space/spacecheck.txt $O/space.txt
python3 tools/v8/place_check.py $Z > $O/place-v2.txt 2>&1
TM=$(mktemp -d); unzip -q $Z -d $TM; python3 -m http.server 0 --bind 127.0.0.1 --directory $TM > $TM.port 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' $TM.port | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
echo "address http://127.0.0.1:$PORT/$P/" > $O/lines_v2.txt
for w in 320 390 430 641 700 830 1024 1440; do python3 tools/lines_v2.py "http://127.0.0.1:$PORT/$P/" $w 2>&1 | tail -1; done >> $O/lines_v2.txt
kill $PS; rm -rf $TM $TM.port
python3 tools/res2nov/shots2.py $Z $B/shots > $B/shots.log 2>&1
bash tools/run_checks.sh $C $Z $O > $O/run_checks.log 2>&1
echo ALLDONE; TZ=Asia/Shanghai date +%H:%M:%S > $O/DONE
