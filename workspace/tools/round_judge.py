"""round_judge.py <step> <result file> [page]
6 Nov 2026 (owner 07:16 "implement all 6 immediately", items 1 and 5): says whether one step of a check round passed, so the
runners can stop at the first fault and skip a step already passed after a restart. Prints PASS or FAULT: <why>; exit 0 / 1.
The allowed faults are judged as the gate judges them: style lines only D066/E054 (AF001, owner 5 Nov 15:20); Word-format
difference lines only those in tools/allowed/<page>-format-word.txt, as many times per width as listed (AF002, 6 Nov 00:19).
"""
import sys, re, os, collections
step, f = sys.argv[1], sys.argv[2]
page = sys.argv[3] if len(sys.argv) > 3 else 'the-english-curriculum'
M = '/home/claude/mm'
if not os.path.exists(f):
    print('FAULT: no result file %s' % f); sys.exit(1)
L = open(f, errors='replace').read().splitlines()
txt = '\n'.join(L)
def ok(): print('PASS'); sys.exit(0)
def bad(w): print('FAULT: %s' % w); sys.exit(1)
last = lambda rx: any(re.search(rx, l) for l in L[-4:])
simple = {'strip': r'ALL CHECKS OK', 'static': r'^STATIC PASS', 'columns': r'^COLUMNS OK', 'text': r'^TEXT PASS',
          'tablet': r'^TABLET PASS', 'space': r'SPACING OK', 'images': r'^IMAGES PASS', 'images2': r'^IMAGES PASS',
          'wrap': r'^WRAP PASS', 'widths': r'RESULT: every width ok', 'place': r'^PLACE OK', 'speed': r'^SPEED OK'}
if step in simple:
    ok() if last(simple[step]) else bad((L[-1] if L else 'empty')[:160])
if step == 'style':
    fl = [l for l in L if l.startswith('FAULT') and not re.match(r'^STYLE FAULT', l)]
    other = [l for l in fl if not l.startswith('FAULT D066/E054')]
    if last(r'^STYLE PASS') or (fl and not other):
        ok()
    bad(other[0][:160] if other else (L[-1] if L else 'empty'))
if step == 'format':
    allowed = collections.Counter()
    af = os.path.join(M, 'tools/allowed/%s-format-word.txt' % page)
    if os.path.exists(af):
        for l in open(af):
            if l.startswith('#') or ' | ' not in l: continue
            allowed[l.rstrip('\n').split(' | ', 1)[1]] += 1
    m = re.search(r'^RESULT: (\d+) differences', txt, re.M)
    if not m: bad('no "RESULT: N differences" line')
    blocks, cur = [], None
    for l in L:
        w = re.match(r'^-- width (\d+)\b', l)
        if w: cur = [w.group(1), [], False]; blocks.append(cur); continue
        if cur is None or cur[2]: continue
        if l.startswith('colour pairs'): cur[2] = True; continue
        if l.strip(): cur[1].append(l)
    for w, diffs, closed in blocks:
        left = allowed.copy()
        for l in diffs:
            k = l.strip()
            hit = next((a for a in left if left[a] > 0 and a.strip() == k), None)
            if hit is None: bad('width %s: %s' % (w, k[:150]))
            left[hit] -= 1
    ok()
if step == 'lines':
    got = [l for l in L if re.match(r'^width \d+:', l)]
    if len(got) < 8: bad('%d widths read, 8 needed' % len(got))
    badl = [l for l in got if not re.search(r'line-through-text 0\b', l)]
    ok() if not badl else bad(badl[0][:160])
if step == 'height':   # the gate's rule (unchanged by the 06:54 agreement): 1 s = 4 s = after scrolling, no margin over 150 px
    import json
    for l in L:
        m = re.search(r'(\{.*\})', l)
        if not m: bad('no reading: ' + l[:120])
        r = json.loads(m.group(1))
        if not (r.get('1s') == r.get('4s') == r.get('scrolled')) or r.get('largest margin', [999])[0] > 150:
            bad(l[:200])
    ok() if L else bad('empty')
bad('unknown step %s' % step)
