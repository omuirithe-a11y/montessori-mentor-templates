#!/bin/bash
# send_gate_pe12.sh (12 Nov 2026): send_gate_pe.sh with one change - placement: a stacked image 40 from the text is her 12 Nov rule ("photos 40/40", The Prepared Environment), not a fault; every other placement fault still stops the gate
# send_gate_pe.sh (8 Nov 2026, owner: "yes - this page being built using the preview you just created is the priority. nothingmust be allowed to prevent that from happeing or even slow that from happening"): send_gate_nolive.sh for The Prepared Environment with two changes only:
#  1. 'spacing against the PDF' is replaced by the one spacing rule check against the approved preview (<zip>.one.txt from pe-final/onecheck.js, all widths, last line RESULT: ALL OK) - owner "yes" to replacing it
#  2. placement: a GAP line for an image followed by a quotation reading 40 is her rule ("make the space of 40 above and below quotations"), not a fault; every other placement fault still stops the gate
# send_gate_nolive.sh <cand.zip> <checks dir> <template.html> <Word .docx> <menu reference index.html> </address/> <full-check file> <allowed-fault regex or NONE> <out dir>
# 1 Nov 2026: send_gate.sh v8 for a page with NO live version (owner 31 Oct 21:08: "the code check compares the page's code with the
# Resources Code Template and its words with the Word file, instead of with a live page"). The ONLY change from v8: the code check is
# strip_compare_nolive.py (template + Word + menu reference) instead of strip_compare.py (template + live). Everything else is v8.
# send_gate.sh v5 <cand.zip> <checks dir> <template.html> <live index.html> <full-check file> <allowed-fault regex or NONE> <out dir>
# v4 (29 Oct 19:5x): tools from this folder (the 28 Oct report-folder paths do not exist in new sessions); <zip>.changes.txt printed;
# click speed (speed_check.py); copy protection must be present; makes <slug>-UPLOAD.zip and <slug>-NO-COPY-PROTECTION-REVIEW-ONLY.zip
# 28 Oct 2026 (owner 20:46 "do it"; Anthropic: "a deterministic gate ... blocks ... until it passes").
# Makes send-named/<slug>-NO-COPY-PROTECTION.zip ONLY if: code check OK; the full check was run on THIS zip and every
# FAULT line is allowed; height is the same at 4 s and after scrolling at 1440 and 390, with no margin over 150 px.
set -u; Z=$1; C=$2; T=$3; W=$4; M=$5; U=$6; F=$7; A=$8; O=$9; G=/home/claude/montessori-mentor-templates/handover-2026-10-29-evening/tools-v5-fixA   # v8 (31 Oct 18:1x): chk/v6 does not exist in this session; the same check scripts from tools-v5-fixA (the only change from v7)
SHA=$(sha256sum "$Z" | cut -d' ' -f1); SLUG=$(unzip -Z1 "$Z" | head -1 | cut -d/ -f1); bad=0
echo "gate $(TZ=Asia/Shanghai date +%H:%M:%S) $SLUG ${SHA:0:8}"
if [ -s "$Z.changes.txt" ]; then echo "changes checked (the owner confirms this list):"; sed 's/^/  /' "$Z.changes.txt"; else echo "changes list missing: $Z.changes.txt"; bad=1; fi
# v5: the owner's own confirming words for that list, with their time, copied word for word from her message (<zip>.confirmed.txt)
if [ -s "$Z.confirmed.txt" ]; then echo "owner's confirmation:"; sed 's/^/  /' "$Z.confirmed.txt"; else echo "owner's confirmation missing: $Z.confirmed.txt"; bad=1; fi
r=$(python3 -I $C/strip_compare_nolive.py "$T" "$Z" "$W" "$M" "$U" 2>&1 | tail -1); echo "code check (no live page: template + Word): $r"; [[ "$r" == *"ALL CHECKS OK"* ]] || bad=1
if grep -q "package sha256: $SHA" "$F" 2>/dev/null && grep -q '^RESULT' "$F"; then
  n=$(grep -cE '^ *[0-9]+ (ok|FAULT)' "$F"); echo "full check: $n widths"
  python3 -I $G/faults_allowed.py "$F" "$A" || bad=1   # 22:0x: line by line, item by item (the old grep -v let a line through if the allowed text was anywhere in it)
  python3 -I $G/faults_allowed.py "$F" "$A" >/dev/null || bad=1
else echo "full check: not run on this zip"; bad=1; fi
mkdir -p "$O"; HC=$O/$SLUG-${SHA:0:16}-height   # 28 Oct 22:0x: height results kept per exact zip and width (run early, alongside the full check), reused here
for W in 1440 390; do if [ -s "$HC-$W.txt" ]; then o=$(cat "$HC-$W.txt"); else o=$(timeout 900 python3 $G/stable.py $W "$Z" 2>/dev/null | grep "^$SLUG"); [ -n "$o" ] && echo "$o" > "$HC-$W.txt"; fi; echo "height $W: ${o#* }"
  python3 -I -c "
import json,sys;r=json.loads(sys.argv[1].split(' ',1)[1]);ok=r['4s']==r['scrolled'] and r.get('closed again',r['4s'])==r['4s'] and r['largest margin'][0]<=150 and r.get('largest margin, open',[0])[0]<=150   # 22:0x: also height after opening and closing albums (Culture's fault)
o=[v for k,v in r.items() if k.startswith('all ')];print('  ok' if ok else '  FAULT');sys.exit(0 if ok else 1)" "$o" || bad=1; done
python3 -I $G/image_sizes.py "$Z"   # v5: report only
timeout 1200 python3 -I $G/speed_check.py "$Z" 1440,390 | sed 's/^/speed /'; [ ${PIPESTATUS[0]} = 0 ] || bad=1
p=$(unzip -p "$Z" "$SLUG/index.html" | grep -o 'id="mm-protect"\|id="mm-protect-js"' | sort | uniq -c | awk '{print $1}' | tr '\n' ' ')
[ "$p" = "1 1 " ] && echo "copy protection: present" || { echo "copy protection: MISSING in the checked zip ($p)"; bad=1; }
# v7 (30 Oct 18:2x, plan item 4; owner 16:22 "implement them all"): also requires the placement check, lines through text (every
# width reads 0), the format check and the separate checker's screenshot review - <zip>.place.txt, .lines.txt, .format.txt,
# .screens.txt, each saved after the zip was made
for k in place lines format screens one; do f="$Z.$k.txt"; if [ ! -s "$f" ] || [ "$f" -ot "$Z" ]; then echo "$k: missing or older than the zip"; bad=1; continue; fi
  case $k in
    place) if tail -1 "$f" | grep -q '^PLACE OK$'; then echo "placement: PLACE OK"; else o=$(grep -E 'fault' "$f" | python3 -I -c "
import sys,re,ast
for l in sys.stdin:
    m=re.match(r'^ *\d+ GAP fault: stacked image not 30 px from the text \[image, side, px\]: (\[.*\])$',l.strip())
    if m and all(x[2]==40 for x in ast.literal_eval(m.group(1))): continue
    print(l.rstrip())
"); if [ -z "$o" ]; then echo "placement: OK - only images 40 above/below text (her rule 12 Nov: \"photos 40/40\"), $(grep -c fault "$f") widths"; else echo "placement: $o"; bad=1; fi; fi ;;
    one) tail -1 "$f" | grep -q '^RESULT: ALL OK$' && echo "one spacing rule against the approved preview: ALL OK ($(grep -cE '^ *[0-9]+ ok' "$f") widths)" || { echo "one spacing rule: $(tail -1 "$f")"; bad=1; } ;;
    lines) n0=$(grep -c 'line-through-text 0$' "$f"); nl=$(grep -c . "$f"); if [ "$n0" -ge 8 ] && [ "$n0" = "$nl" ]; then echo "lines through text: 0 at $n0 widths"; else echo "lines through text: FAULT ($n0 of $nl lines read 0)"; bad=1; fi ;;
    format) echo "format: $(tail -1 "$f")"; grep -q '^RESULT' "$f" || bad=1 ;;
    space) tail -1 "$f" | grep -q '^RESULT: SPACING OK$' && echo "spacing against the PDF: SPACING OK ($(grep -c '^ *[0-9]* |' "$f") gaps)" || { echo "spacing against the PDF: $(tail -1 "$f")"; bad=1; } ;;   # 3 Nov 2026 (owner 17:08-17:23): spacecheck.py, 13 widths
    screens) tail -1 "$f" | grep -q 'NO UNLISTED FAULTS SEEN' && echo "screenshot review: NO UNLISTED FAULTS SEEN" || { echo "screenshot review: $(tail -1 "$f")"; bad=1; } ;;
  esac; done
if [ $bad = 0 ]; then cp "$Z" "$O/$SLUG-UPLOAD.zip" && cmp -s "$Z" "$O/$SLUG-UPLOAD.zip" && python3 -I $G/strip_protect.py "$Z" "$O/$SLUG-NO-COPY-PROTECTION-REVIEW-ONLY.zip" && echo "GATE PASSED - upload: $O/$SLUG-UPLOAD.zip (${SHA:0:8}) | review only: $O/$SLUG-NO-COPY-PROTECTION-REVIEW-ONLY.zip"; else echo "GATE FAILED: nothing made"; fi
