#!/bin/bash
# gate_live.sh <cand.zip> <live page folder> <full-check file> <out dir>   (29 Oct 2026; owner 11:50 "yes")
# send_gate.sh for a page corrected from its live copy: the code check is live_diff.py (only the agreed changes differ from
# the live page; every file present and identical); every other step as send_gate.sh: the full check run on THIS zip with no
# fault at any width (no allowed faults), height the same at 4 s and after scrolling (and after albums) at 1440 and 390,
# no margin over 150 px. Only then the no-copy-protection zip is made. Prints GATE PASSED / GATE FAILED.
set -u; Z=$1; L=$2; F=$3; O=$4; C=$(dirname "$(readlink -f "$0")"); bad=0
SHA=$(sha256sum "$Z" | cut -d' ' -f1); SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
echo "gate $(TZ=Asia/Shanghai date +%H:%M:%S) $SLUG ${SHA:0:8}"
r=$(python3 -I $C/live_diff.py "$Z" "$L" 2>&1 | tail -1); echo "code check: $r"; [[ "$r" == "ALL CHECKS OK" ]] || bad=1
if grep -q "package sha256: $SHA" "$F" 2>/dev/null && grep -q '^RESULT' "$F"; then
  n=$(grep -cE '^ *[0-9]+ (ok|FAULT)' "$F"); echo "full check: $n widths"; [ "$n" -ge 122 ] || bad=1
  grep -q '^1280 narrowed to 390: sideways 0$' "$F" || { echo "narrowing test missing or failed"; bad=1; }
  python3 -I $C/faults_allowed.py "$F" NONE | cut -c1-300 || bad=1
  python3 -I $C/faults_allowed.py "$F" NONE >/dev/null || bad=1
else echo "full check: not run on this zip"; bad=1; fi
for W in 1440 390; do o=$(timeout 900 python3 $C/stable.py $W "$Z" 2>/dev/null | grep "^$SLUG"); echo "height $W: ${o#* }" | cut -c1-300
  python3 -I -c "
import json,sys;r=json.loads(sys.argv[1].split(' ',1)[1]);ok=r['4s']==r['scrolled'] and r.get('closed again',r['4s'])==r['4s'] and r['largest margin'][0]<=150 and r.get('largest margin, open',[0])[0]<=150
print('  ok' if ok else '  FAULT');sys.exit(0 if ok else 1)" "$o" || bad=1; done
mkdir -p "$O"
if [ $bad = 0 ]; then python3 -I $C/strip_protect.py "$Z" "$O/$SLUG-NO-COPY-PROTECTION.zip" && echo "GATE PASSED: $O/$SLUG-NO-COPY-PROTECTION.zip"; else echo "GATE FAILED: nothing made"; fi
