#!/usr/bin/env python3
"""live_diff2.py <check.zip> <live folder>/<slug> <protection file> [--protect]   (30 Oct 2026)
The code check for the fix-A pages. Allowed changes, nothing else: fix A (always) and, with --protect, copy protection - the
exact mm-protect style just before </head> and the exact mm-protect-js script just before </body>, from the protection file.
Undoing exactly those must give the live index.html byte for byte. The live page must have the old line once and no copy
protection (--protect) or both protection blocks already (without --protect). Every image the page names must be in the zip.
The delivered file (<check.zip>.index.html) must equal the zip's index.html. Prints ALL CHECKS OK or the faults."""
import sys, os, re, zipfile
Z, L, P = sys.argv[1], sys.argv[2], sys.argv[3]; prot = '--protect' in sys.argv; bad = []
OLD = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"
NEW = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */"
zf = zipfile.ZipFile(Z); slug = zf.namelist()[0].split('/')[0]
idx = zf.read(slug + '/index.html').decode('utf-8'); live = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
pr = open(P, encoding='utf-8').read()
css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
if live.count(OLD) != 1: bad.append('the old line is in the live page %d times (must be 1)' % live.count(OLD))
if idx.count(NEW) != 1: bad.append('fix A found %d times (must be 1)' % idx.count(NEW))
if idx.count(OLD) != 0: bad.append('the old line is still in the page')
u = idx.replace(NEW, OLD)
if prot:
    if 'mm-protect' in live: bad.append('the live page already has copy protection - use the fix-A-alone check')
    if u.count(css + '</head>') != 1 or u.count(js + '</body>') != 1: bad.append('copy protection not found exactly once, in place, word for word')
    u = u.replace(css + '</head>', '</head>', 1).replace(js + '</body>', '</body>', 1)
else:
    if live.count('id="mm-protect"') != 1 or live.count('id="mm-protect-js"') != 1: bad.append('the live page has no copy protection - this page needs --protect')
if u != live: bad.append('the page differs from the live page by more than the allowed change(s)')
names = set(n[len(slug) + 1:] for n in zf.namelist() if not n.endswith('/'))
refs = set(re.findall(r'(?:src|data-full)="(images/[^"]+)"', idx) + re.findall(r"url\(['\"]?(images/[^)'\"]+)", idx))
if refs - names: bad.append('images named but not in the check zip: %s' % sorted(refs - names)[:5])
if os.path.exists(Z + '.index.html') and open(Z + '.index.html', encoding='utf-8').read() != idx: bad.append('the delivered index.html differs from the checked one')
if not os.path.exists(Z + '.index.html'): bad.append('the delivered index.html is missing')
print('%s: %d images named, index.html %d chars (live %d)%s' % (slug, len(refs), len(idx), len(live), ', fix A + copy protection' if prot else ', fix A alone'))
print('\n'.join('FAULT: ' + b for b in bad) if bad else 'ALL CHECKS OK')
sys.exit(1 if bad else 0)
