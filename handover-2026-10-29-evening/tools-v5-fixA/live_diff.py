#!/usr/bin/env python3
"""live_diff.py (fix-A version, 29 Oct 2026 20:4x) <candidate.zip> <live page folder> - for the 15 pages the owner confirmed at
20:08 ("Fix A on the 15 pages: the one image-load line, nothing else - confirmed"). The ONLY allowed change is fix A: the new line
must be found exactly once and the old line not at all; with fix A undone, index.html must equal the live index.html byte for
byte; every other file must be present and byte-identical. Prints ALL CHECKS OK or the faults."""
import sys, zipfile, os
Z, L = sys.argv[1], sys.argv[2]
OLD = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"
NEW = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */"
zf = zipfile.ZipFile(Z); names = [n for n in zf.namelist() if not n.endswith('/')]
slug = names[0].split('/')[0]; bad = []
idx = zf.read(slug + '/index.html').decode('utf-8'); live = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
if live.count(OLD) != 1: bad.append('the old line is in the live page %d times (must be 1)' % live.count(OLD))
if idx.count(NEW) != 1: bad.append('fix A found %d times in the page (must be 1)' % idx.count(NEW))
if idx.count(OLD) != 0: bad.append('the old line is still in the page')
if idx.replace(NEW, OLD) != live: bad.append('the page differs from the live page by more than fix A')
lf = sorted(os.path.relpath(os.path.join(r, f), L) for r, _, fs in os.walk(L) for f in fs)
zfs = sorted(n[len(slug) + 1:] for n in names)
if lf != zfs: bad.append('files differ from the live folder: only in zip %s, only live %s' % (sorted(set(zfs) - set(lf))[:5], sorted(set(lf) - set(zfs))[:5]))
for n in zfs:
    if n == 'index.html' or n not in lf: continue
    if zf.read(slug + '/' + n) != open(os.path.join(L, n), 'rb').read(): bad.append('file differs from live: ' + n)
print('%s: %d files, index.html %d chars (live %d)' % (slug, len(zfs), len(idx), len(live)))
print('\n'.join('FAULT: ' + b for b in bad) if bad else 'ALL CHECKS OK')
sys.exit(1 if bad else 0)
