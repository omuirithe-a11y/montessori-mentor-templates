#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 1; lesson 18): refuse a build when free disk space is under 4 GB (a build and
# its checks use about 1.5 GB; on 6 Nov 09:57 a full disk stopped build 31)
FREE=$(df -Pk /home/claude | awk 'NR==2{print int($4/1048576)}'); [ "${FREE:-0}" -ge 4 ] || { echo "BUILD REFUSED: only ${FREE} GB free on the disk (4 GB needed) - clear superseded builds' bulky files first (tools/clear_old_builds.sh)"; exit 3; }
# build_guard.sh <builds folder> <new build name>
# 6 Nov 2026 (owner 08:01 "analyse the effectiveness ... then adjust"; BUILD-ORDER item 5/6): a new build is refused while the
# newest build's check round is unfinished - the fast round must have STOPPED at a fault or PASSED, and if it passed, a
# separate review report (REVIEW.md, naming the package sha256) must exist. So every fault a round finds is fixed together in
# ONE new build, not one build per fix. Override only with the owner's words in <builds>/<new>.override.txt.
set -u; D=$1; N=$2
[ -s "$D/$N.override.txt" ] && { echo "build guard: override by the owner's words in $D/$N.override.txt"; exit 0; }
P=$(ls -d "$D"/b[0-9]* 2>/dev/null | sed 's/.*\/b//' | grep -E '^[0-9]+$' | sort -n | tail -1)
if [ -z "$P" ]; then   # 6 Nov 08:2x (owner 08:15 "adjust accordingly"): build 1 needs the decisions sheet answered first
  DS=${DECISIONS_SHEET:-}; { [ -n "$DS" ] && [ -s "$DS" ] && grep -q "^OWNER ANSWER:" "$DS"; } || { echo "BUILD REFUSED: first build - no answered decisions sheet (set DECISIONS_SHEET to a file holding a line 'OWNER ANSWER: <her words>')"; exit 3; }
  # 8 Nov 06:44 (owner "yes" to removing it): the 7 Nov S4b wait for the template test page is removed - the template test page was deleted from the to-do list (owner 8 Nov 06:43)
  touch "/home/claude/mm/records/.guard-ok-$(basename "$D")-$N"; echo "build guard: first build, decisions sheet answered ($DS)"; exit 0; fi
B="$D/b$P"; S="$B/checks2/SUMMARY.txt"
[ -f "$S" ] || { echo "BUILD REFUSED: build b$P has no check round (run tools/check_round.sh ... fast on it first)"; exit 3; }
grep -q "^STOPPED at" "$S" && { [ -s "$B/REVIEW.md" ] || { echo "BUILD REFUSED: b$P's round stopped at a fault, but b$P has no separate review report (REVIEW.md) - run the review on b$P, then fix the round's and the review's faults together"; exit 3; }; echo "build guard: b$P's round stopped at a fault and b$P has its review - fix every fault found, then build $N"; exit 0; }   # 6 Nov 12:1x: the review on every build
grep -q "^FAST CHECKS PASSED" "$S" || { echo "BUILD REFUSED: build b$P's fast round has not finished"; exit 3; }
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1); SHA=$(sha256sum "$Z" | cut -c1-16)
[ -f "$B/REVIEW.md" ] && grep -q "$SHA" "$B/REVIEW.md" || { echo "BUILD REFUSED: build b$P passed its fast round but has no separate review report naming $SHA"; exit 3; }
# 7 Nov 2026 (owner "implement all of these changes"): S1 - the gate plan; S4b - the template test page; S10 - a cause for each build
PG=$(basename "$Z" .zip); GP=/home/claude/mm/records/gate-plans/$PG.md; GR=/home/claude/mm/tools/allowed/$PG-gate-rows.txt
python3 - "$GP" "$GR" <<'PY' || exit 3
import sys, os, re, hashlib, glob
gp, gr = sys.argv[1:3]
def refuse(m): print('BUILD REFUSED: ' + m); sys.exit(3)
if not os.path.exists(gp): refuse('no gate plan %s - run tools/gate_plan.sh on the last build (S1)' % gp)
t = open(gp).read(); m = re.search(r'^rules sha256 (\w+)', t, re.M)
if not m or m.group(1) != hashlib.sha256(open('/home/claude/mm/tools/REQUIRED-CHECKS.json', 'rb').read()).hexdigest():
    refuse('the rules list changed since the gate plan was made - run tools/gate_plan.sh again and bring the new rows to the owner (S1)')
todo = re.findall(r'^TO DECIDE ([A-E]\d{3})', t, re.M)
rows, quote = set(), None
if os.path.exists(gr):
    g = open(gr).read(); rows = set(re.findall(r'^([A-E]\d{3}) \|', g, re.M))
    q = re.search(r'word for word: "(.{40,}?)"\s*$', g, re.M); quote = q.group(1) if q else None
# 7 Nov 2026 (owner: "yes to the B026 change."): a row whose own rule says it is checked after upload is read as checked after publishing
import json as _j
_rq = {r['id']: r for r in _j.load(open('/home/claude/mm/tools/REQUIRED-CHECKS.json'))}
own = [r for r in todo if re.match(r'^\s*after upload', _rq.get(r, {}).get('item', ''), re.I)]
left = [r for r in todo if r not in rows and r not in own]
if left: refuse('rows with no check written or met only after upload have no decision of the owner in %s: %s (S1)' % (gr, ' '.join(left)))
if todo:
    logs = ''.join(open(f).read() for f in glob.glob('/home/claude/mm/records/DECISIONS-LOG*.md'))
    if not quote or quote[:120] not in logs: refuse('%s does not quote the owner\'s words found in the decisions log (S1)' % gr)
PY
[ -n "${BUILD_CAUSE:-}" ] || { echo "BUILD REFUSED: no cause given for build $N - set BUILD_CAUSE (review fault / check fault / template change / owner change: what) (S10)"; exit 3; }
echo "$(date '+%d %b %Y %H:%M:%S') | $N | cause: $BUILD_CAUSE" >> /home/claude/mm/records/build-causes-$PG.txt
touch "/home/claude/mm/records/.guard-ok-$(basename "$D")-$N"; echo "build guard: b$P checked and reviewed - build $N"
