#!/bin/bash
# integrate.sh <base.zip> <out.zip> <patchfile.json> <template.html> <checks dir> <live index.html>
# Applies verbatim OLD->NEW patches (JSON list of [old,new]) to the page's index.html and to a copy of the template,
# then runs the fast checks: code check, line comparison, settling, footer/large gaps. One command, one report.
set -u
BASE=$1; OUT=$2; PATCH=$3; TPL=$4; CHK=$5; LIVE=$6
S=/tmp/claude-0/-home-claude/457824cb-7342-52d8-8229-8cd580a6aa46/scratchpad
W=$(mktemp -d -p $S/elist int-XXXX)
( cd $W && unzip -q "$BASE" )
F=$(ls $W/*/index.html); SLUG=$(basename $(dirname $F))
python3 -I - "$F" "$PATCH" "$TPL" "$W/tpl.html" <<'P'
import sys,json
f,pf,t,tout=sys.argv[1:5];s=open(f,encoding='utf-8').read();ts=open(t,encoding='utf-8').read()
for old,new in json.load(open(pf)):
    assert s.count(old)==1,('page',old[:80],s.count(old)); s=s.replace(old,new)
    if ts.count(old)==1: ts=ts.replace(old,new)
open(f,'w',encoding='utf-8').write(s);open(tout,'w',encoding='utf-8').write(ts);print('patches applied')
P
mkdir -p $W/t && mv $W/tpl.html "$W/t/Essay Code Template.html"
( cd $W && zip -qrX "$OUT" "$SLUG" )
echo "build $(sha256sum "$OUT" | cut -c1-8)  template $(sha256sum "$W/t/Essay Code Template.html" | cut -c1-8)"
mkdir -p $W/chk && cp $CHK/*.py $W/chk/ && N=$(sha256sum "$W/t/Essay Code Template.html"|cut -d' ' -f1) && sed -i -E "s/'Essay Code Template.html': '[0-9a-f]{64}'/'Essay Code Template.html': '$N'/" $W/chk/strip_compare.py
python3 -I $W/chk/strip_compare.py "$W/t/Essay Code Template.html" "$OUT" "$LIVE" > $W/strip.txt 2>&1; echo "code check: $(tail -1 $W/strip.txt)"
timeout 600 python3 $S/linecmp/lines3.py "$SLUG|$OUT|$LIVE" 2>/dev/null | head -40
timeout 600 python3 $S/elist/foot.py "$OUT" 2>/dev/null | cut -c1-400
timeout 600 python3 $S/elist/stable.py 1440 "$OUT" 2>/dev/null | grep "^$SLUG" | cut -c1-300
cp "$W/t/Essay Code Template.html" "$OUT.template.html"; rm -rf "$W"
