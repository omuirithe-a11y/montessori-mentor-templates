#!/usr/bin/env python3
"""vfast.py <checks dir> <package.zip> <out.txt> [workers=2] [widths=all] [--skip-done parts-dir]
28 Oct 2026 22:1x (owner: "use those ways"). The SAME on-screen check as <checks dir>/visual_check.py, run faster:
 - the check's own code is read from visual_check.py and run unchanged per width (same JS, same waits, same line format);
 - one browser per worker for the whole run (was one per 15-width part, 9 starts);
 - workers take the next unchecked width from one shared queue (no fixed parts, no repeated part, no idle runner);
 - band edges and the menu widths first, so a faulty build shows within minutes;
 - the 1280 -> 390 narrowing test once (was once per part, 9 times);
 - images and fonts served with a cache rule, so a width does not re-read files another width already read;
 - each width's time is recorded (TIME lines), so the slow steps can be found.
Output: one line per width in width order, the narrowing line, RESULT - the same format run_visual_split.sh writes,
with 'package sha256' and 'visual_check.py sha256' at the top, so the send gate reads it unchanged."""
import sys, os, re, hashlib, subprocess, tempfile, time, json
C, Z, OUT = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
K = int(sys.argv[4]) if len(sys.argv) > 4 else 2
V = os.path.join(C, 'visual_check.py'); src = open(V, encoding='utf-8').read()
VS = hashlib.sha256(src.encode()).hexdigest(); ZS = hashlib.sha256(open(Z, 'rb').read()).hexdigest()
W_ALL = eval(re.search(r'^WIDTHS = (.*?)\s*#', src, re.M).group(1))
MENU_W = eval(re.search(r'^MENU_W = (\{.*?\})', src, re.M).group(1))
if len(sys.argv) > 5 and sys.argv[5] != 'all': W_ALL = [int(x) for x in sys.argv[5].split(',')]
EDGES = [390, 1440] + sorted(MENU_W)
order = [w for w in EDGES if w in W_ALL]; order += [w for w in W_ALL if w not in order]
order = list(dict.fromkeys(order))
done = {}
if '--skip-done' in sys.argv:   # widths already finished by the old runner on THIS zip and THIS check (its parts files)
    D = sys.argv[sys.argv.index('--skip-done') + 1]
    for f in sorted(os.listdir(D)):
        if re.match(r'part\d+\.txt(\.tmp2?)?$', f):   # a finished part, or the lines a stopped part had already printed (each line is a whole width)
            t = open(os.path.join(D, f), encoding='utf-8').read()
            if True:
                for l in re.findall(r'(?m)^ *(\d+) (?:ok|FAULT).*$', t): pass
                for m in re.finditer(r'(?m)^( *(\d+) (?:ok|FAULT).*)$', t): done[int(m.group(2))] = m.group(1)
                n = re.search(r'(?m)^1280 narrowed to 390: sideways (\d+)', t)
                if n: done['narrow'] = '1280 narrowed to 390: sideways ' + n.group(1)
order = [w for w in order if w not in done]
# --- the worker: visual_check.py's own text, with only the loop source and the narrowing step changed
i0 = src.index('        for W in WIDTHS:'); i1 = src.index('        # narrowing an open window')
i2 = src.index("    print('RESULT:'")
body = src[:i0] + '''        import fcntl
        def claim():
            while True:
                with open(QF, 'r+') as fq:
                    fcntl.flock(fq, fcntl.LOCK_EX); ws = json.load(fq)
                    if not ws: return None
                    w = ws.pop(0); fq.seek(0); fq.truncate(); json.dump(ws, fq); return w
        while True:
            W = claim()
            if W is None: break
            __t0 = time.time()
''' + src[src.index('\n', i0) + 1:i1].replace('    ' * 3 + 'await pg.close()', '    ' * 3 + 'await pg.close(); print("TIME %d %.1f" % (W, time.time() - __t0), flush=True)') + '''        if DO_NARROW:
''' + re.sub(r'(?m)^', '    ', src[i1:src.index('        await b.close()', i1)]) + '''        await b.close()
''' + src[i2:]
body = body.replace('import sys, os,', 'import time, json, sys, os,', 1)
body = body.replace("class Q(http.server.SimpleHTTPRequestHandler):\n    def log_message(self, *a): pass",
  "class Q(http.server.SimpleHTTPRequestHandler):\n    def log_message(self, *a): pass\n    def end_headers(self):\n        self.send_header('Cache-Control', 'max-age=86400'); super().end_headers()")
assert 'max-age' in body and 'claim()' in body and 'DO_NARROW' in body and 'print("TIME' in body
work = tempfile.mkdtemp(prefix='vfast-', dir=os.path.dirname(os.path.abspath(OUT)))
QF = os.path.join(work, 'queue.json'); json.dump(order, open(QF, 'w'))
wsrc = os.path.join(work, 'worker.py'); open(wsrc, 'w', encoding='utf-8').write(body)
t0 = time.time(); procs = []
for k in range(K):
    env = dict(os.environ)
    pre = 'QF=%r; DO_NARROW=%r\n' % (QF, k == 0 and 'narrow' not in done)
    wk = os.path.join(work, 'w%d.py' % k); s = open(wsrc, encoding='utf-8').read()
    s = s.replace('from playwright.async_api import async_playwright', 'from playwright.async_api import async_playwright\n' + pre, 1)
    open(wk, 'w', encoding='utf-8').write(s)
    procs.append(subprocess.Popen([sys.executable, '-u', wk, Z, '320'], stdout=open(os.path.join(work, 'w%d.out' % k), 'w'), stderr=subprocess.STDOUT))
    time.sleep(3)
for p in procs: p.wait()
lines = dict((k, v) for k, v in done.items()); times = {}
for k in range(K):
    for l in open(os.path.join(work, 'w%d.out' % k), encoding='utf-8'):
        l = l.rstrip('\n'); m = re.match(r'^ *(\d+) (?:ok|FAULT)', l)
        if m: lines[int(m.group(1))] = l
        elif l.startswith('1280 narrowed'): lines['narrow'] = l
        elif l.startswith('TIME '): a = l.split(); times[int(a[1])] = float(a[2])
missing = [w for w in W_ALL if w not in lines]
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('visual_check.py sha256: %s\npackage sha256: %s\nrun by tools/vfast.py with %d workers, %d widths reused from the parts files; %.0f s\n----\n' % (VS, ZS, K, len([k for k in done if k != 'narrow']), time.time() - t0))
    for w in W_ALL:
        if w in lines: f.write(lines[w] + '\n')
    if 'narrow' in lines: f.write(lines['narrow'] + '\n')
    ok = not missing and 'narrow' in lines and all(' ok ' in lines[w][:12] for w in W_ALL) and lines['narrow'].endswith('sideways 0')
    if missing: f.write('MISSING WIDTHS: %s\n' % missing)
    f.write('RESULT: %s\n' % ('every width ok' if ok else 'FAULTS - see the lines marked FAULT'))
open(OUT + '.times', 'w').write('\n'.join('%d %.1f' % (w, times[w]) for w in sorted(times)) + '\n')
print('written', OUT, 'missing', missing, 'seconds', round(time.time() - t0))
