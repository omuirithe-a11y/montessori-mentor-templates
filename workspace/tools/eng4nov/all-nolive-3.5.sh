# every first-build check for The English Curriculum (no live version): screenshots first, then code, format, spacing, placement, lines, run_checks (122 widths, height, speed)
B=${1:?usage: all-nolive-3.5.sh <build number> [zip] [out]}; cd /home/claude/mm; Z=${2:-/home/claude/mm/build-35/b$B/the-english-curriculum-b$B-CHECK-ONLY.zip}; O=${3:-/home/claude/mm/build-35/b$B/checks}; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
[ -n "${NOSHOTS:-}" ] || python3 /home/claude/mm/tools/res2nov/shots2.py $Z /home/claude/mm/build-35/b$B/shots > /home/claude/mm/build-35/b$B/shots.log 2>&1; echo SHOTSDONE
T="templates/Essay Code Template.html"; D="/home/claude/eng35/src/3.5.0 The English Curriculum.docx"
mkdir -p $O
python3 -I tools/v8/strip_compare_nolive.py "$T" $Z "$D" /home/claude/eng35/live/picture-books/index.html /the-english-curriculum/ > $O/code-word.txt 2>&1
python3 -I tools/v8/format_check_word.py $Z "$D" > $O/format-word.txt 2>&1
TS=$(mktemp -d); unzip -q $Z -d $TS; python3 tools/spacecheck.py "$D" "${D%.docx}.pdf" $TS/the-english-curriculum $O/space > $O/space.log 2>&1; cp $O/space/spacecheck.txt $O/space.txt 2>/dev/null; rm -rf $TS
python3 tools/v8/place_check.py $Z > $O/place-v2.txt 2>&1
TM=$(mktemp -d); unzip -q $Z -d $TM; python3 -m http.server 0 --bind 127.0.0.1 --directory $TM > $TM.port 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' $TM.port | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
echo "address http://127.0.0.1:$PORT/the-english-curriculum/" > $O/lines_v2.txt
for w in 320 390 430 641 700 830 1024 1440; do python3 tools/lines_v2.py "http://127.0.0.1:$PORT/the-english-curriculum/" $w 2>&1 | tail -1; done >> $O/lines_v2.txt
kill $PS; rm -rf $TM $TM.port
bash tools/run_checks.sh $C $Z $O > $O/run_checks.log 2>&1
echo ALLDONE; date +%H:%M:%S > $O/DONE
