#!/bin/bash
# gate_plan.sh <build dir> <page slug>  (S1, owner 7 Nov 2026 "implement all of these changes"): runs the gate on a build
# (no review) and sorts every row that applies by HOW it is met - a check's result, a review, a file record, the gate itself,
# no check yet, after upload. Writes records/gate-plans/<page>.md. The rows "no check yet" and "after upload" are the ones
# the owner decides at build 1; each decision goes in tools/allowed/<page>-gate-rows.txt (modes: script / browser review /
# after publishing). tools/build_guard.sh refuses build 2 and later until every such row has a line there, and refuses a
# build when tools/REQUIRED-CHECKS.json has changed since the plan was made.
set -u; B=$1; P=$2; M=/home/claude/mm; Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1)
O=$M/records/gate-plans/$P.md; T=$(mktemp)
python3 $M/tools/gate_list.py "$Z" "$B" NONE "$T" --page "$P" >/dev/null 2>&1
python3 - "$T" "$O" "$P" "$B" <<'PY'
import sys, re, hashlib, datetime, os
t, o, page, b = sys.argv[1:5]
rows = [l for l in open(t).read().splitlines() if re.match(r'^[A-E]\d{3} \|', l)]
mp = {}
mf = '/home/claude/mm/tools/allowed/%s-gate-rows.txt' % page
if os.path.exists(mf):
    for l in open(mf):
        f = [x.strip() for x in l.split('|')]
        if len(f) >= 3 and re.match(r'^[A-E]\d{3}$', f[0]): mp[f[0]] = f[1] + ' | ' + f[2]
cat = {}
for l in rows:
    f = [x.strip() for x in l.split(' | ')]
    rid, how, out, det = f[0], f[1], f[2], ' | '.join(f[4:])
    if 'page row map' in how: k = 'decided (page row map)'
    elif 'after upload' in how or 'after upload' in det or 'after her upload' in det: k = 'after upload'
    elif out == 'NO CHECK YET': k = 'no check yet'
    elif 'eye' in how: k = 'a review'
    elif 'this gate' in how and '+' not in how: k = 'the gate itself'
    elif 'gate_files' in how or 'plan 8' in how: k = 'a file record'
    else: k = 'a check\'s result'
    cat.setdefault(k, []).append(rid)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
todo = cat.get('no check yet', []) + cat.get('after upload', [])
with open(o, 'w') as w:
    w.write('# Gate plan - %s (made %s from %s)\n' % (page, datetime.datetime.now().strftime('%d %b %Y %H:%M'), b))
    w.write('rules sha256 %s\n' % sha('/home/claude/mm/tools/REQUIRED-CHECKS.json'))
    w.write('rows that apply: %d\n\n' % len(rows))
    for k in ("a check's result", 'a review', 'a file record', 'the gate itself', 'decided (page row map)', 'no check yet', 'after upload'):
        w.write('## %s (%d)\n%s\n\n' % (k, len(cat.get(k, [])), ' '.join(cat.get(k, [])) or '-'))
    w.write('## TO DECIDE AT BUILD 1 (owner) - each needs a line in tools/allowed/%s-gate-rows.txt\n' % page)
    for r in todo: w.write('TO DECIDE %s%s\n' % (r, (' -> decided: ' + mp[r]) if r in mp else ''))
print('gate plan written: %s | %s' % (o, ', '.join('%s %d' % (k, len(v)) for k, v in cat.items())))
print('to decide: %d, of them decided in the page row map: %d' % (len(todo), sum(1 for r in todo if r in mp)))
PY
rm -f "$T"
