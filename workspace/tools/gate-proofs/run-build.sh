#!/bin/bash
# gate_list.py proof on the build given (7 Nov 2026): scratch copies (symlinks to b42 files, checks/ and checks2/ copied with times kept)
set -u; M=/home/claude/mm; N=${1:?build, e.g. b43}; B=$M/build-35/$N; G=/home/claude/eng35/gproof; S=$G/scratch; rm -rf $S; mkdir -p $S
mk(){ d=$S/$1/$N; mkdir -p $d; for f in $B/*; do n=${f##*/}; case $n in checks|checks2) cp -rp $f $d/;; *) ln -s $f $d/$n;; esac; done; ln -s $B.log $S/$1/$N.log; ln -s $M/build-35/faces $S/$1/faces; }
run(){ python3 $M/tools/gate_list.py $S/$1/$N/the-english-curriculum.zip $S/$1/$N $S/$1/$N/REVIEW.md $G/$1.txt --page the-english-curriculum >/dev/null 2>&1; }
row(){ grep -E "^$2 \|" $G/$1.txt | head -1 | cut -c1-220; }
mk base; mk planted; mk notallowed
sed -i -E '0,/^ *500 /s/^( *500 ).*/\1FAULT oversized images 1/' $S/planted/$N/checks/full.txt 2>/dev/null
F=$(ls $S/planted/$N/checks/ | grep -E '^full' | head -1)
L=$(grep -m1 "FAULT D066/E054" $S/notallowed/$N/checks2/style.txt); echo "FAULT D066/E054 320 div.mm-float margin-top set by 2 scripts" >> /dev/null
N=$(grep -n -m1 "FAULT D066/E054" $S/notallowed/$N/checks2/style.txt | cut -d: -f1); sed -i "${N}s/.*/FAULT D066\/E054 320 div.mm-float margin-top set by 2 scripts/" $S/notallowed/$N/checks2/style.txt
for k in base planted notallowed; do run $k; done
{ echo "# gate_list.py proof (6 Nov 2026 $(date +%H:%M)), no browser used"
  echo "gate_list.py sha256 $(sha256sum $M/tools/gate_list.py | cut -d' ' -f1)"
  echo "gate_files.py sha256 $(sha256sum $M/tools/gate_files.py | cut -d' ' -f1)"
  echo "package $B/the-english-curriculum.zip sha256 $(sha256sum $B/the-english-curriculum.zip | cut -d' ' -f1)"
  echo "Each scratch copy: $S/<name>/$N = symlinks to build 42's files, checks/ and checks2/ copied (cp -rp)."
  echo; echo "## base: $(tail -1 $G/base.txt)"
  echo; echo "## 1. PASS row turned FAULT by a planted, allowance-free fault (checks/full.txt width 500 line set to 'FAULT oversized images 1')"
  echo "$(tail -1 $G/planted.txt)"; echo "rows PASS in base and FAULT here:"
  n=0; for r in $(grep -E "^[A-E][0-9]{3} \| .* \| PASS \|" $G/base.txt | cut -d' ' -f1 | sort -u); do grep -qE "^$r \| .* \| FAULT \|" $G/planted.txt && { echo "  $r"; n=$((n+1)); }; done
  [ $n -gt 0 ] && echo "RESULT: PASS row turned FAULT" || echo "RESULT: NOT SHOWN"
  echo; echo "## 2. allowed fault accepted (AF001): base D066 row"; echo "  $(row base D066)"
  grep -qE "^D066 \| .* \| PASS \|" $G/base.txt && grep -q "allowed (AF001)" <(row base D066) && echo "RESULT: allowed fault accepted" || echo "RESULT: NOT SHOWN"
  echo; echo "## 3. one AF001 line changed to a near-miss text (not the allowance's text): refused"; echo "  $(row notallowed D066)"
  grep -qE "^D066 \| .* \| FAULT \|" $G/notallowed.txt && echo "RESULT: only exact allowance text accepted" || echo "RESULT: NOT SHOWN"
} > $G/PROOFS.txt; cat $G/PROOFS.txt
