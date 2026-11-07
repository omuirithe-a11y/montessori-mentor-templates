#!/bin/bash
# after_long.sh b<N> (7 Nov 2026): run as a tracked background command; waits for the build's long round to end, then at once
# (no waiting on anyone): the gate proof on this build (tools/gate-proofs/run-build.sh, rows D089/B007), installs its
# PROOFS.txt, and the gate's full run with the review report - so the only step left after it is the browser review.
set -u; N=${1:?}; M=/home/claude/mm; B=$M/build-35/$N; S=$B/checks2/SUMMARY.txt
until grep -qE "LONG CHECKS \(more_checks\) PASSED|^STOPPED|REFUSED" <(sed -n '/stage long start/,$p' $S 2>/dev/null) || grep -q "^STOPPED" $B/checks/SUMMARY.txt 2>/dev/null; do sleep 20; done
if ! grep -q "LONG CHECKS (more_checks) PASSED" $S; then echo "long round did not pass: $(tail -2 $S | tr '\n' ' ') $(tail -2 $B/checks/SUMMARY.txt 2>/dev/null | tr '\n' ' ')"; exit 1; fi
until bash $M/tools/roundlock.sh check >/dev/null 2>&1; do sleep 5; done   # the round has let go of the lock
bash $M/tools/gate-proofs/run-build.sh $N > /home/claude/eng35/gproof-$N.out 2>&1; grep -h "RESULT" /home/claude/eng35/gproof/PROOFS.txt
grep -q "RESULT: NOT SHOWN" /home/claude/eng35/gproof/PROOFS.txt || cp /home/claude/eng35/gproof/PROOFS.txt $M/tools/gate-proofs/PROOFS.txt
python3 $M/tools/gate_list.py $B/the-english-curriculum.zip $B $B/REVIEW.md $B/gate-full.txt --page the-english-curriculum > /dev/null 2>&1
echo "gate full run: $(tail -1 $B/gate-full.txt)"; grep -E "^[A-E][0-9]{3} \|.*\| (FAULT|NOT CHECKED|NO CHECK YET) \|" $B/gate-full.txt | cut -c1-200 > $B/gate-open-rows.txt; echo "open rows: $(wc -l < $B/gate-open-rows.txt) (in $B/gate-open-rows.txt)"
