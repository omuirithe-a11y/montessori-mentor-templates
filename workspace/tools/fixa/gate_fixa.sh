#!/bin/bash
# gate_fixa.sh <check.zip> <live folder>/<slug> <full-check file> <out dir> <allowed faults regex or NONE> [--protect]   (30 Oct 2026)
# gate_live.sh v5 (29 Oct) for the fix-A pages, with three changes: (1) the code check is live_diff2.py - fix A, plus copy
# protection with --protect (owner 15:49 "Yes" for the 7 pages without it); (2) allowed faults are an argument (owner 15:5x:
# Culture's squeezed text at 1020-1050 "Allow it this time"); (3) what is delivered is index.html ONLY - Hostinger sends back
# re-compressed images (30 Oct 16:1x), so the images on the server are never replaced. Every check runs on the full check zip.
set -u; Z=$1; L=$2; F=$3; O=$4; A=$5; PROT=${6:-}; G=$(dirname "$(readlink -f "$0")"); C=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA; bad=0
P=/home/claude/mm/templates/copy-protection.html
SHA=$(sha256sum "$Z" | cut -d' ' -f1); SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1)
echo "gate $(TZ=Asia/Shanghai date +%H:%M:%S) $SLUG ${SHA:0:8}"
if [ -s "$Z.changes.txt" ]; then echo "changes (the owner confirmed):"; sed 's/^/  /' "$Z.changes.txt"; else echo "changes list missing: $Z.changes.txt"; bad=1; fi
if [ -s "$Z.confirmed.txt" ]; then echo "owner's confirmation:"; sed 's/^/  /' "$Z.confirmed.txt"; else echo "owner's confirmation missing: $Z.confirmed.txt"; bad=1; fi
r=$(python3 -I $G/live_diff2.py "$Z" "$L" "$P" $PROT 2>&1 | tail -1); echo "code check: $r"; [[ "$r" == "ALL CHECKS OK" ]] || bad=1
if grep -q "package sha256: $SHA" "$F" 2>/dev/null && grep -q '^RESULT' "$F"; then
  n=$(grep -cE '^ *[0-9]+ (ok|FAULT)' "$F"); echo "full check: $n widths"; [ "$n" -ge 122 ] || bad=1
  grep -q '^1280 narrowed to 390: sideways 0$' "$F" || { echo "narrowing test missing or failed"; bad=1; }
  echo "allowed faults: $A"; python3 -I $C/faults_allowed.py "$F" "$A" | cut -c1-300 || bad=1
  python3 -I $C/faults_allowed.py "$F" "$A" >/dev/null || bad=1
else echo "full check: not run on this zip"; bad=1; fi
for W in 1440 390; do o=$(timeout 900 python3 $C/stable.py $W "$Z" 2>/dev/null | grep "^$SLUG"); echo "height $W: ${o#* }" | cut -c1-300
  python3 -I -c "
import json,sys;r=json.loads(sys.argv[1].split(' ',1)[1]);ok=r['4s']==r['scrolled'] and r.get('closed again',r['4s'])==r['4s'] and r['largest margin'][0]<=150 and r.get('largest margin, open',[0])[0]<=150
print('  ok' if ok else '  FAULT');sys.exit(0 if ok else 1)" "$o" || bad=1; done
timeout 1800 python3 -I $C/speed_check.py "$Z" 1440,390 | sed 's/^/speed /'; [ ${PIPESTATUS[0]} = 0 ] || bad=1
p=$(unzip -p "$Z" "$SLUG/index.html" | grep -o 'id="mm-protect"\|id="mm-protect-js"' | sort | uniq -c | awk '{print $1}' | tr '\n' ' ')
[ "$p" = "1 1 " ] && echo "copy protection: present" || { echo "copy protection: MISSING ($p)"; bad=1; }
# 30 Oct 16:2x (owner 16:22 "implement them all"; Project instructions: every check on the first build; plan item 4): the gate
# also requires the placement check, lines through text, the format check and the separate checker's screenshot review, each
# saved beside the zip AFTER the zip was made (newer than it) - <zip>.place.txt, .lines.txt, .format.txt, .screens.txt
for k in place lines format screens; do f="$Z.$k.txt"; if [ ! -s "$f" ] || [ "$f" -ot "$Z" ]; then echo "$k: missing or older than the zip"; bad=1; continue; fi
  case $k in
    place) tail -1 "$f" | grep -q '^PLACE OK$' && echo "placement: PLACE OK" || { echo "placement: $(tail -1 "$f")"; bad=1; } ;;
    lines) if grep -q 'line-through-text [1-9]' "$f"; then echo "lines through text: FAULT"; bad=1; else echo "lines through text: 0 at $(grep -c 'line-through-text 0' "$f") widths"; fi ;;
    format) echo "format: $(tail -1 "$f" | cut -c1-160)"; grep -q '^RESULT' "$f" || bad=1 ;;
    screens) tail -1 "$f" | grep -q 'NO UNLISTED FAULTS SEEN' && echo "screenshot review: NO UNLISTED FAULTS SEEN" || { echo "screenshot review: $(tail -1 "$f" | cut -c1-120)"; bad=1; } ;;
  esac; done
mkdir -p "$O/$SLUG-UPLOAD"
if [ $bad = 0 ]; then cp "$Z.index.html" "$O/$SLUG-UPLOAD/index.html" && unzip -p "$Z" "$SLUG/index.html" | cmp -s - "$O/$SLUG-UPLOAD/index.html" && echo "GATE PASSED - deliver ONLY: $O/$SLUG-UPLOAD/index.html (into public_html/$SLUG/, replacing index.html; images untouched)"; else echo "GATE FAILED: nothing made"; fi
