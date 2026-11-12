cd /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/rF
Z=/home/claude/ec/final/the-english-curriculum.zip
t(){ echo "== $1 $(date -u +%T)"; }; t code; python3 /home/claude/montessori-mentor-templates/workspace/tools/v8/strip_compare_nolive.py "/home/claude/montessori-mentor-templates/Essay Code Template.html" $Z /home/claude/ec/src/3.5.0.docx /home/claude/montessori-mentor-templates/workspace/pages/pe-final/approved-preview-index.html /the-english-curriculum/ > code.txt 2>&1; tail -1 code.txt
t(){ echo "== $1 $(date -u +%T)"; }; t format; (cd /home/claude/montessori-mentor-templates/workspace/tools/v8 && python3 format_check_word.py /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/z/the-english-curriculum /home/claude/ec/src/3.5.0.docx) > format.txt 2>&1; echo exit $?

t(){ echo "== $1 $(date -u +%T)"; }; t spacing; CHK=/home/claude/ec/chk/onecheck-v5.js /home/claude/ec/chk/spacing122.sh file:///home/claude/ec/final/index.html /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/rF/spacing.txt
t(){ echo "== $1 $(date -u +%T)"; }
t vfast; (cd /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA-200 && python3 vfast.py /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA-200 $Z /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/rF/vfast.txt 2) > vfast.log 2>&1; tail -2 vfast.txt
t stable; (cd /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA-200 && python3 stable.py 1440 $Z > /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/rF/stable1440.txt 2>&1; python3 stable.py 390 $Z > /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/rF/stable390.txt 2>&1); tail -1 stable1440.txt stable390.txt
t place; python3 /home/claude/montessori-mentor-templates/workspace/tools/v8/place_check.py $Z > place.txt 2>&1; tail -1 place.txt
t speed; (cd /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA && python3 speed_check.py $Z) > speed.txt 2>&1; tail -1 speed.txt
t lines; python3 -m http.server 8765 -d /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/checks/z >/dev/null 2>&1 & S=$!; sleep 1
for w in 1440 1280 1024 961 768 641 480 390; do python3 /home/claude/montessori-mentor-templates/workspace/tools/lines_v2.py http://127.0.0.1:8765/the-english-curriculum/ $w --open; done > lines.txt 2>&1; kill $S; grep -c 'line-through-text 0' lines.txt
t done
