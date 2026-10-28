#!/bin/bash
# send_gate.sh <cand.zip> <checks dir> <template.html> <live index.html> <full-check file> <allowed-fault regex or NONE>
# 28 Oct 2026 (owner 20:46 "do it"; Anthropic: "a deterministic gate ... blocks ... until it passes").
# Makes send-named/<slug>-NO-COPY-PROTECTION.zip ONLY if: code check OK; the full check was run on THIS zip and every
# FAULT line is allowed; height is the same at 4 s and after scrolling at 1440 and 390, with no margin over 150 px.
set -u; Z=$1; C=$2; T=$3; L=$4; F=$5; A=$6; S=/tmp/claude-0/-home-claude/457824cb-7342-52d8-8229-8cd580a6aa46/scratchpad
SHA=$(sha256sum "$Z" | cut -d' ' -f1); SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1); bad=0
echo "gate $(TZ=Asia/Shanghai date +%H:%M:%S) $SLUG ${SHA:0:8}"
r=$(python3 -I $C/strip_compare.py "$T" "$Z" "$L" 2>&1 | tail -1); echo "code check: $r"; [[ "$r" == *"ALL CHECKS OK"* ]] || bad=1
if grep -q "package sha256: $SHA" "$F" 2>/dev/null && grep -q '^RESULT' "$F"; then
  n=$(grep -cE '^ *[0-9]+ (ok|FAULT)' "$F"); echo "full check: $n widths"
  python3 -I /home/claude/reports/tools/faults_allowed.py "$F" "$A" | cut -c1-300 || bad=1   # 22:0x: line by line, item by item (the old grep -v let a line through if the allowed text was anywhere in it)
  python3 -I /home/claude/reports/tools/faults_allowed.py "$F" "$A" >/dev/null || bad=1
else echo "full check: not run on this zip"; bad=1; fi
HC=/home/claude/reports/final-checks/$SLUG-${SHA:0:16}-height   # 28 Oct 22:0x: height results kept per exact zip and width (run early, alongside the full check), reused here
for W in 1440 390; do if [ -s "$HC-$W.txt" ]; then o=$(cat "$HC-$W.txt"); else o=$(timeout 900 python3 $S/elist/stable.py $W "$Z" 2>/dev/null | grep "^$SLUG"); [ -n "$o" ] && echo "$o" > "$HC-$W.txt"; fi; echo "height $W: ${o#* }" | cut -c1-300
  python3 -I -c "
import json,sys;r=json.loads(sys.argv[1].split(' ',1)[1]);ok=r['4s']==r['scrolled'] and r.get('closed again',r['4s'])==r['4s'] and r['largest margin'][0]<=150 and r.get('largest margin, open',[0])[0]<=150   # 22:0x: also height after opening and closing albums (Culture's fault)
o=[v for k,v in r.items() if k.startswith('all ')];print('  ok' if ok else '  FAULT');sys.exit(0 if ok else 1)" "$o" || bad=1; done
if [ $bad = 0 ]; then python3 -I /home/claude/reports/tools/strip_protect.py "$Z" "/home/claude/reports/send-named/$SLUG-NO-COPY-PROTECTION.zip" && echo "GATE PASSED: send-named/$SLUG-NO-COPY-PROTECTION.zip"; else echo "GATE FAILED: nothing made"; fi
