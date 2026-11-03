B=${1:?usage: all-nolive-8.2-shots-first.sh <build number>}; cd /home/claude/mm; Z=${2:-/home/claude/mm/build-82/b$B/books-of-interest-b$B-CHECK-ONLY.zip}; O=${3:-/home/claude/mm/build-82/b$B/checks}; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
[ -n "${NOSHOTS:-}" ] || python3 /home/claude/mm/tools/res2nov/shots2.py /home/claude/mm/build-82/b$B/books-of-interest-b$B-CHECK-ONLY.zip /home/claude/mm/build-82/b$B/shots > /home/claude/mm/build-82/b$B/shots.log 2>&1; echo SHOTSDONE
T="templates/Resources Code Template.html"; D="src/8.2/8.2 Books - Education, Parenting, Child Development.docx"
mkdir -p $O
python3 -I tools/v8/strip_compare_nolive.py "$T" $Z "$D" live/resources/index.html /books-of-interest/ > $O/code-word.txt 2>&1
python3 -I tools/v8/format_check_word.py $Z "$D" > $O/format-word.txt 2>&1
python3 tools/v8/place_check.py $Z > $O/place-v2.txt 2>&1
TM=$(mktemp -d); unzip -q $Z -d $TM; python3 -m http.server 0 --bind 127.0.0.1 --directory $TM > $TM.port 2>&1 & PS=$!
for i in $(seq 50); do PORT=$(grep -o 'port [0-9]*' $TM.port | grep -o '[0-9]*'); [ -n "$PORT" ] && break; sleep 0.2; done
echo "address http://127.0.0.1:$PORT/books-of-interest/" > $O/lines_v2.txt
for w in 320 390 430 641 700 830 1024 1440; do python3 tools/lines_v2.py "http://127.0.0.1:$PORT/books-of-interest/" $w 2>&1 | tail -1; done >> $O/lines_v2.txt
kill $PS; rm -rf $TM $TM.port
bash tools/run_checks.sh $C $Z $O > $O/run_checks.log 2>&1
echo ALLDONE
