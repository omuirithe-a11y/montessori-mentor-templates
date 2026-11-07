#!/usr/bin/env python3
"""speed_ok.py <speed_check output file>  (7 Nov 2026, owner "yes" to the agreement in <zip>.confirmed.txt): The Prepared Environment only -
OK when, at 1440 and 390, the longest busy stretch is no longer than the live page's (190 ms, 300 ms) and every click opens in under 1.0 s."""
import sys, re, json
LIM = {'1440': 190, '390': 300}; bad = []; seen = set()
for l in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r'(?:speed )?(\d+) (?:FAULT|OK)\s+longest busy stretch (\d+) ms.*clicks (\{[^}]*\})', l.strip())
    if not m: continue
    w, b, c = m.group(1), int(m.group(2)), json.loads(m.group(3)); seen.add(w)
    if w in LIM and b > LIM[w]: bad.append('%s busy %d ms vs live %d' % (w, b, LIM[w]))
    for k, v in c.items():
        if v >= 1.0: bad.append('%s click %s %.2f s' % (w, k, v))
if seen != set(LIM): bad.append('widths measured %s vs 1440 and 390' % sorted(seen))
print('SPEED AGREED OK' if not bad else 'SPEED FAULT (agreement): ' + '; '.join(bad)); sys.exit(1 if bad else 0)
