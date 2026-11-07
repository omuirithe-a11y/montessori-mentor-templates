"""gate_early_judge.py <gate-early.txt> (7 Nov 2026, owner "implement all of these changes", S1 refined): the early gate run
stops the round only on what can be known after the fast round. Left out: the order lines for the review and the long
checks (they come later), and rows met only by the gate itself when every other part of the row passes. Prints the lines
that stop the round; exit 1 if any."""
import sys, re
EXPECTED = re.compile(r'order: (no separate review report written after the fast round passed|run_checks\.sh has not run|more_checks\.sh long has not run)')
FAST = re.compile(r'checks2/(strip-nolive|static|format-word|col|text\.log|text/|style|tablet|space)')
bad = []
for l in open(sys.argv[1]).read().splitlines():
    if re.match(r'^INTEGRITY FAULT', l) and not EXPECTED.search(l): bad.append(l)
    m = re.match(r'^([A-E]\d{3}) \| (.*?) \| FAULT \| (.*?) \| (.*)$', l)
    if m and FAST.search(l):
        how, det = m.group(2), m.group(4)
        parts = det.split(' || ')
        own = [p for p in parts if not p.startswith('SELF:') and not p.startswith('rests on the gate')]
        if 'this gate' in how and not any(p.startswith('FAULT') for p in own) and len(parts) > 1: continue
        bad.append(l[:220])
for l in bad: print(l)
sys.exit(1 if bad else 0)
