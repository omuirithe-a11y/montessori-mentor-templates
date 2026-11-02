cd /home/claude/mm; Z=/home/claude/res80/b83/b21/build/picture-books.zip; O=/home/claude/res80/b83/b21/checks; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
T="templates/Resources Code Template.html"; D="src/8.3/8.3 Picture Books.docx"
mkdir -p $O
python3 -I tools/v8/strip_compare_nolive.py "$T" $Z "$D" live/resources/index.html /picture-books/ > $O/code-word.txt 2>&1
bash tools/run_checks.sh $C $Z $O > $O/run_checks.log 2>&1
python3 tools/v8/place_check.py $Z > $O/place-v2.txt 2>&1
TM=$(mktemp -d); unzip -q $Z -d $TM; python3 -m http.server 0 --bind 127.0.0.1 --directory $TM > $TM.port 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' $TM.port | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
echo "address http://127.0.0.1:$PORT/picture-books/" > $O/lines_v2.txt
for w in 320 390 430 641 700 830 1024 1440; do python3 tools/lines_v2.py "http://127.0.0.1:$PORT/picture-books/" $w 2>&1 | tail -1; done >> $O/lines_v2.txt
kill $PS; rm -rf $TM $TM.port
python3 -I tools/v8/format_check_word.py $Z "$D" > $O/format-word.txt 2>&1
echo ALLDONE
python3 /home/claude/res80/tools/shots.py /home/claude/res80/b83/b21/build/picture-books.zip /home/claude/res80/b83/b21/shots > /home/claude/res80/b83/b21/shots.log 2>&1; echo SHOTSDONE
