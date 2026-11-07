#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 4; lesson 48): copy changed files to the repo's workspace/, refresh both
# fingerprint lists, check them, commit, push, then read GitHub's copy back - "pushed" is reported only when origin's main
# equals the local commit.  Usage: commit_push.sh "<message>" <path relative to /home/claude/mm> [...]
set -u
MSG=$1; shift; M=/home/claude/mm; R=/home/claude/montessori-mentor-templates; W=$R/workspace
# 7 Nov 2026 (S9): a decisions-log line written with a time later than the clock is refused
for f in "$@"; do case "$f" in records/DECISIONS-LOG*.md) python3 "$M/tools/log_time_check.py" "$W/$f" "$M/$f" || exit 3;; esac; done
for f in "$@"; do mkdir -p "$W/$(dirname "$f")"; cp "$M/$f" "$W/$f" || { echo "COMMIT FAILED: cannot copy $f"; exit 1; }; done
[ -f "$M/templates/Essay Code Template.html" ] && ! cmp -s "$M/templates/Essay Code Template.html" "$R/Essay Code Template.html" && echo "NOTE: the Essay template differs from the repo copy - not copied (template changes need her agreement and are copied by hand)"
cd "$W" && python3 - <<'P'
import hashlib,os
for fp,base in [('tools/v8/FINGERPRINTS.txt','tools/v8'),('FINGERPRINTS.txt','.')]:
    out=[]
    for line in open(fp):
        line=line.rstrip('\n')
        if '  ' not in line: out.append(line); continue
        h,p=line.split('  ',1); f=os.path.join(base,p)
        if os.path.exists(f) and len(h)==64: h=hashlib.sha256(open(f,'rb').read()).hexdigest()
        out.append(h+'  '+p)
    open(fp,'w').write('\n'.join(out)+'\n')
P
BAD=$(sha256sum -c FINGERPRINTS.txt 2>/dev/null | grep -vc ": OK"); BAD8=$(cd tools/v8 && sha256sum -c FINGERPRINTS.txt 2>/dev/null | grep -vc ": OK")
[ "$BAD" = 0 ] && [ "$BAD8" = 0 ] || { echo "COMMIT FAILED: fingerprints do not check ($BAD, $BAD8)"; exit 1; }
cp FINGERPRINTS.txt "$M/"; cp tools/v8/FINGERPRINTS.txt "$M/tools/v8/"
cd "$R" && git add -A && git commit -q -m "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01TK2yJvF3NhLKpn9GUhVUFc" || { echo "COMMIT FAILED: nothing to commit or commit refused"; exit 1; }
git push -q 2>&1 | tail -2
L=$(git rev-parse HEAD); O=$(git ls-remote origin -h refs/heads/main | cut -f1)
[ "$L" = "$O" ] && echo "PUSHED AND READ BACK: GitHub main = ${L:0:7}" || { echo "PUSH NOT CONFIRMED: local ${L:0:7}, GitHub ${O:0:7}"; exit 1; }
