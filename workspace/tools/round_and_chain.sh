#!/bin/bash
# 7 Nov 2026: one command for a build's whole round - the fast round, then (tools/chain.sh) screenshots, wait for the
# separate review (FAULTS: 0), the long round. It returns only when all of it has ended, so started as ONE tracked
# background command (Bash run_in_background) nothing is left detached to be stopped after a reply (b36, b40).
# Usage: bash tools/round_and_chain.sh b<N>
set -u; N=${1:?usage: round_and_chain.sh b<N>}; M=/home/claude/mm; S=/home/claude/eng35/src; cd $M
bash $M/tools/chain.sh $N & CH=$!
bash tools/check_round.sh build-35/$N pages/the-english-curriculum.py "$S/3.5.0 The English Curriculum.docx" "$S/3.5.0 The English Curriculum.pdf" "templates/Essay Code Template.html" /home/claude/eng35/live/picture-books/index.html /home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA-200 the-english-curriculum fast > /home/claude/eng35/round-$N-fast.log 2>&1
echo "fast round ended $(date +%T): $(tail -1 build-35/$N/checks2/SUMMARY.txt)"
wait $CH; echo "chain ended $(date +%T)"; tail -4 /home/claude/eng35/chain-$N.log; tail -3 build-35/$N/checks/SUMMARY.txt 2>/dev/null; tail -3 build-35/$N/checks2/SUMMARY.txt
