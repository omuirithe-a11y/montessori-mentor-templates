cd /home/claude/mm; Z=/home/claude/res80/b81x/n10/build/books-by-montessori.zip; O=/home/claude/res80/b81x/n10/checks; C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA
mkdir -p $O
python3 -I tools/v8/strip_compare.py "templates/Resources Code Template.html" $Z live/books-by-montessori/index.html > $O/code-live.txt 2>&1
bash tools/run_checks.sh $C $Z $O > $O/run_checks.log 2>&1
python3 tools/v8/place_check.py $Z > $O/place-v2.txt 2>&1
bash /home/claude/res80/b81/more_checks.sh $Z $O > $O/more.log 2>&1
echo ALLDONE
