#!/usr/bin/env python3
"""pe_diff.py <check.zip> <live folder with index.html>  (7 Nov 2026)
The code check for The Prepared Environment's 7 Nov edits: the owner's 25 agreed edits are made by build_pe.py from the live
index.html; the zip's index.html must equal that build byte for byte (so nothing else changed), the copy protection of the live
page must be in it unchanged, and every image the page names must be in the zip. Prints ALL CHECKS OK or the faults."""
import sys, os, re, zipfile, subprocess, tempfile, hashlib
Z, L = sys.argv[1], sys.argv[2]; bad = []
zf = zipfile.ZipFile(Z); slug = zf.namelist()[0].split('/')[0]
idx = zf.read(slug + '/index.html').decode('utf-8')
with tempfile.TemporaryDirectory() as t:
    os.symlink(os.path.abspath(os.path.join(L, 'images')), os.path.join(t, 'images'))
    r = subprocess.run([sys.executable, '-I', '/home/claude/tpl/scripts/build_pe.py', os.path.join(L, 'index.html'), t], capture_output=True, text=True)
    if 'BUILT' not in r.stdout: bad.append('build from live failed: ' + (r.stdout + r.stderr)[-300:])
    else:
        b = open(os.path.join(t, 'index.html'), encoding='utf-8').read()
        if b != idx: bad.append('the page differs from the agreed edits made on the live page (sha %s vs %s)' % (hashlib.sha256(idx.encode()).hexdigest()[:8], hashlib.sha256(b.encode()).hexdigest()[:8]))
live = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
for k in ('<style id="mm-protect">', '<script id="mm-protect-js">'):
    a = re.findall(re.escape(k) + r'.*?</(?:style|script)>', live, re.S); c = re.findall(re.escape(k) + r'.*?</(?:style|script)>', idx, re.S)
    if len(a) != 1 or a != c: bad.append('copy protection %s not as live' % k)
names = set(zf.namelist())
for src in set(re.findall(r'(?:src|data-full)="(images/[^"]+)"', idx)) | set(re.findall(r"url\('(images/[^']+)'\)", idx)):
    if slug + '/' + src not in names: bad.append('image missing from the zip: ' + src)
dl = Z + '.index.html'
if not os.path.exists(dl) or open(dl, encoding='utf-8').read() != idx: bad.append('the delivered file %s is missing or differs from the zip\'s index.html' % dl)
print('\n'.join(bad) if bad else 'ALL CHECKS OK')
