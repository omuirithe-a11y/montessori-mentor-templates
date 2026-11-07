#!/bin/bash
# review_brief.sh <build dir> <page slug> <docx> <pdf renders dir> <previous build dir>  (7 Nov 2026, owner "implement all of these
# changes", S8): writes <build>/REVIEW-BRIEF.md, the one brief every separate review of a build gets, with every input in it -
# so no reviewer is given too little (b40's had no faces records and left 97 rows unchecked). The long runners refuse a
# review report that does not name this brief's sha256 (first 16 characters).
set -u; B=$(cd "$1" && pwd); P=$2; DOCX=$3; PDFR=$4; PREV=${5:-}; M=/home/claude/mm
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1); ZS=$(sha256sum "$Z" | cut -d' ' -f1)
# the owner's messages, with times, from the session transcripts (only from where the transcript starts) and the log's quotes
OM=$B/owner-messages.txt
python3 - "$OM" <<'PY'
import json, glob, sys, os, re
out = []
for f in sorted(glob.glob('/root/.claude/projects/-home-claude/*.jsonl'), key=os.path.getmtime):
    for line in open(f, errors='replace'):
        try: d = json.loads(line)
        except Exception: continue
        if d.get('type') != 'user' or d.get('isMeta'): continue
        c = d.get('message', {}).get('content')
        txt = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
        txt = re.sub(r'<system-reminder>.*?</system-reminder>', '', txt or '', flags=re.S).strip()
        if txt and not txt.startswith('<') and 'tool_use_id' not in txt: out.append('%s | %s' % (d.get('timestamp', '?'), txt.replace('\n', ' ')[:2000]))
out.append('--- the owner\'s words as quoted in the decisions log (lines with OWNER or AGREEMENT) ---')
for f in sorted(glob.glob('/home/claude/mm/records/DECISIONS-LOG*.md')):
    out += [l.strip() for l in open(f) if re.search(r'OWNER|AGREEMENT', l)]
open(sys.argv[1], 'w').write('\n'.join(out) + '\n'); print('owner messages:', len(out))
PY
EYE=$B/eye-rows.txt
python3 - "$EYE" "$B/checks2/gate-early.txt" <<'PY'
import json, sys, re
# the rows that rest on a review, as the gate's early run on this build reads them (its HOW CHECKED column names 'eye')
ids = [l.split(' | ')[0] for l in open(sys.argv[2]) if re.match(r'^[A-E]\d{3} \|', l) and 'eye' in l.split(' | ')[1]]
rows = {r['id']: r for r in json.load(open('/home/claude/mm/tools/REQUIRED-CHECKS.json'))}
open(sys.argv[1], 'w').write('\n'.join('%s | %s | %s' % (i, rows[i].get('item', ''), rows[i].get('pass', '')) for i in ids) + '\n'); print('eye rows:', len(ids))
PY
cat > "$B/REVIEW-BRIEF.md" <<EOF
# Review brief - made by tools/review_brief.sh $(date '+%d %b %Y %H:%M') for $P, build $(basename "$B")
You are a separate reviewer who has not seen this page being made. Follow $M/tools/briefs/REVIEW-BRIEF-STANDARD.md and the owner's
rules in $M/tools/briefs/ENG-REVIEW-BRIEF.md ("The owner's rules"). Change no file except your report $B/REVIEW.md. Run no build or
check script and use no browser while a check round runs (tools/roundlock.sh check tells you).
Package: $Z, sha256 $ZS - put it in your heading, and put this line in your report: "BRIEF $(basename "$B")/REVIEW-BRIEF.md".
Inputs (all of them; say in the report which you did not use):
- page code $B/preview/index.html; screenshots $B/shots/ (w1440, w768, w390 parts); images $B/images/
- the PDF rendered $PDFR; the Word file $DOCX
- template $M/templates/Essay Code Template.html; rules $M/tools/REQUIRED-CHECKS.txt; allowed $M/tools/ALLOWED-FAULTS.txt and $M/tools/allowed/$P-*.txt
- previous build ${PREV:-none} and its REVIEW*.md; compare files by sha256 and screenshots by pixel; look at every changed part at full size
- faces: $M/build-35/faces/ (review2.json, sheet-check-final.json, pixel-check-after-answer.json/.md, photos-final/) and $M/blur2/
- records: $M/records/DECISIONS-LOG-3-nov.md, the build log $(dirname "$B")/$(basename "$B").log, $B/changes.txt, the check results $B/checks/ and $B/checks2/
- the owner's words: $OM (her messages with times where the transcript holds them, and every OWNER/AGREEMENT line of the log)
- the eye rows: $EYE - your report must have one table line for EVERY row in it: "| ID | checked | what you looked at |" or "| ID | NOT checked | why |"; a row about how the work was done is checked against the records and her words above, not left NOT checked for want of them
End with the two lines "NOT CHECKED: M" then "FAULTS: N" (the last non-empty line).
EOF
echo "brief $B/REVIEW-BRIEF.md sha256 $(sha256sum "$B/REVIEW-BRIEF.md" | cut -c1-16)"
