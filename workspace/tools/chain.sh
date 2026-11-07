#!/bin/bash
# 7 Nov 2026: generic chain (was eng35/chainNN.sh). RUN IT ONLY INSIDE A TRACKED BACKGROUND COMMAND (the Bash tool with run_in_background, which waits for it): a chain left detached after a reply is stopped (b36, b40). Usage: bash tools/chain.sh b<N>
# waits for the build fast pass, takes the review screenshots, waits for a review written after the pass with FAULTS: 0, starts the long round
N=${1:?usage: chain.sh b<N>}; B=/home/claude/mm/build-35/$N; L=/home/claude/eng35/chain-$N.log
# 7 Nov 2026 (S1 refined): waits for the gate's early run to pass (checks2/GATE-EARLY-PASSED), not only the fast checks
until [ -f $B/checks2/GATE-EARLY-PASSED ] || grep -q "^STOPPED" <(tac $B/checks2/SUMMARY.txt | sed '/stage fast start/q'); do sleep 5; done
[ -f $B/checks2/GATE-EARLY-PASSED ] || { echo "fast round stopped $(date +%T)" >> $L; exit 1; }
echo "fast passed; screenshots $(date +%T)" >> $L
cd /home/claude/eng35; rm -rf "/home/claude/eng35/u-$N"; mkdir "/home/claude/eng35/u-$N"; unzip -q $B/the-english-curriculum.zip -d "/home/claude/eng35/u-$N"; mkdir -p $B/shots
bash /home/claude/mm/tools/serve.sh start /home/claude/eng35/u-$N/the-english-curriculum 8799 >/dev/null; python3 shots.py http://127.0.0.1:8799/ $B/shots >> $L 2>&1; bash /home/claude/mm/tools/serve.sh stop 8799 >/dev/null; rm -f $B/shots/*-full.png
PREVN=$(ls -d /home/claude/mm/build-35/b[0-9]* | sed "s/.*\/b//" | sort -n | awk -v me=${N#b} '$1<me' | tail -1); bash /home/claude/mm/tools/review_brief.sh $B the-english-curriculum "/home/claude/eng35/src/3.5.0 The English Curriculum.docx" /home/claude/eng35/review31/pdf /home/claude/mm/build-35/b$PREVN >> $L 2>&1; touch $B/shots/READY; echo "screenshots ready $(date +%T)" >> $L
until [ -f $B/REVIEW.md ] && [ $B/REVIEW.md -nt $B/checks2/FAST-PASSED ] && [ "$(grep -v '^\s*$' $B/REVIEW.md | tail -1)" != "" ]; do sleep 5; done
sleep 3; LAST=$(grep -v '^\s*$' $B/REVIEW.md | tail -1); echo "review: $LAST $(date +%T)" >> $L
[ "$LAST" = "FAULTS: 0" ] || exit 1
S=/home/claude/eng35/src; cd /home/claude/mm; echo "long start $(date +%T)" >> $L
bash tools/check_round.sh build-35/$N pages/the-english-curriculum.py "$S/3.5.0 The English Curriculum.docx" "$S/3.5.0 The English Curriculum.pdf" "templates/Essay Code Template.html" /home/claude/eng35/live/picture-books/index.html /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA-200 the-english-curriculum long > /home/claude/eng35/round-$N-long.log 2>&1
echo "long ended $(date +%T)" >> $L
