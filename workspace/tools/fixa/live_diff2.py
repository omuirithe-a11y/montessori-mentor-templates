#!/usr/bin/env python3
"""live_diff2.py <check.zip> <live folder>/<slug> <protection file> [--protect | --style-only | --upgrade | --replace]   (30 Oct 2026)
The code check for the fix-A pages. Allowed changes, nothing else: fix A (always) and, with --protect, copy protection - the
exact mm-protect style just before </head> and the exact mm-protect-js script just before </body>, from the protection file.
Undoing exactly those must give the live index.html byte for byte. The live page must have the old line once and no copy
protection (--protect) or both protection blocks already (without --protect). Every image the page names must be in the zip.
The delivered file (<check.zip>.index.html) must equal the zip's index.html. Prints ALL CHECKS OK or the faults."""
import sys, os, re, zipfile
Z, L, P = sys.argv[1], sys.argv[2], sys.argv[3]; prot = '--protect' in sys.argv; sty = '--style-only' in sys.argv; upg = '--upgrade' in sys.argv; rep = '--replace' in sys.argv; bad = []
OLD = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"
NEW = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */"
zf = zipfile.ZipFile(Z); slug = zf.namelist()[0].split('/')[0]
idx = zf.read(slug + '/index.html').decode('utf-8'); live = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
pr = open(P, encoding='utf-8').read()
css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
nofix = '--no-fixa' in sys.argv   # 30 Oct 21:2x: protection only (no old line on the live page; none added)
if nofix:
    if live.count(OLD) or idx.count(NEW) or live.count(NEW): bad.append('--no-fixa needs a page with neither the old line nor fix A')
else:
    if live.count(OLD) != 1: bad.append('the old line is in the live page %d times (must be 1)' % live.count(OLD))
    if idx.count(NEW) != 1: bad.append('fix A found %d times (must be 1)' % idx.count(NEW))
if idx.count(OLD) != 0: bad.append('the old line is still in the page')
u = idx.replace(NEW, OLD)
if prot:
    if 'mm-protect' in live: bad.append('the live page already has copy protection - use the fix-A-alone check')
    if u.count(css + '</head>') != 1 or u.count(js + '</body>') != 1: bad.append('copy protection not found exactly once, in place, word for word')
    u = u.replace(css + '</head>', '</head>', 1).replace(js + '</body>', '</body>', 1)
elif rep:   # 30 Oct 20:3x: live has an older style and script; the current ones must stand in their places, word for word
    oc = re.findall(r'<style id="mm-protect">.*?</style>', live, re.S); oj = re.findall(r'<script id="mm-protect-js">.*?</script>', live, re.S)
    if len(oc) != 1 or len(oj) != 1: bad.append('--replace needs a live page with one protection style and one script')
    elif u.count(css) != 1 or u.count(js) != 1: bad.append('the current copy protection not found exactly once, word for word')
    else: u = u.replace(css, oc[0], 1).replace(js, oj[0], 1)
elif upg:   # 30 Oct 20:0x: live has an older protection script and no style; the current script must replace it word for word, in its place, and the style be added before </head>
    oj = re.findall(r'<script id="mm-protect-js">.*?</script>', live, re.S)
    if len(oj) != 1 or 'id="mm-protect"' in live or oj[0] == js: bad.append('--upgrade needs a live page with one older protection script and no style')
    elif u.count(css + '</head>') != 1 or u.count(js) != 1: bad.append('the current copy protection not found exactly once, in place, word for word')
    else: u = u.replace(css + '</head>', '</head>', 1).replace(js, oj[0], 1)
elif sty:   # 30 Oct 19:5x: live has the script but not the style; only the style may be added, word for word, just before </head>
    if live.count('id="mm-protect-js"') != 1 or 'id="mm-protect"' in live: bad.append('--style-only needs a live page with the protection script and no style block')
    if u.count(css + '</head>') != 1: bad.append('the copy-protection style not found exactly once, in place, word for word')
    u = u.replace(css + '</head>', '</head>', 1)
    if js not in live: bad.append('the live page\'s protection script differs from the protection file (not word for word)')
else:
    if live.count('id="mm-protect"') != 1 or live.count('id="mm-protect-js"') != 1: bad.append('the live page has no copy protection - this page needs --protect')
if u != live: bad.append('the page differs from the live page by more than the allowed change(s)')
names = set(n[len(slug) + 1:] for n in zf.namelist() if not n.endswith('/'))
refs = set(re.findall(r'(?:src|data-full)="(images/[^"]+)"', idx) + re.findall(r"url\(['\"]?(images/[^)'\"]+)", idx))
if refs - names: bad.append('images named but not in the check zip: %s' % sorted(refs - names)[:5])
if os.path.exists(Z + '.index.html') and open(Z + '.index.html', encoding='utf-8').read() != idx: bad.append('the delivered index.html differs from the checked one')
if not os.path.exists(Z + '.index.html'): bad.append('the delivered index.html is missing')
# 30 Oct 16:5x (owner 16:57: accepted only "if it checks everything send_gate.sh checks"): part 8 of send_gate's code check
# (strip_compare.py, checks-v6), the same rules: the hero is images/hero.jpg; every file the page names (src, data-full, srcset,
# links to image/PDF files) exists; every image box's shape (aspect-ratio) and every width/height pair is within 1% of its file;
# PDF-placed boxes (div.mm-pdf) are only listed, as in send_gate
from bs4 import BeautifulSoup
from PIL import Image
import tempfile, io
ps8 = BeautifulSoup(idx, 'html.parser'); f8 = []
def fbytes(v):
    n = slug + '/' + v
    return zf.read(n) if n in zf.namelist() else None
hero8 = ps8.select_one('.hero'); hu = re.findall(r"url\(['\"]?([^'\")]+)", hero8.get('style', '')) if hero8 else []
if hu != ['images/hero.jpg']: f8.append('hero image is %s, must be images/hero.jpg' % hu)
r8 = set(hu)
for e in ps8.find_all(True):
    for a in ('src', 'data-full', 'href'):
        v = e.get(a)
        if v and not re.match(r'^(https?:|mailto:|#|/|tel:|data:|javascript:)', v) and (a != 'href' or re.search(r'\.(jpe?g|png|gif|webp|pdf)$', v, re.I)): r8.add(v)
    for part in (e.get('srcset') or '').split(','):
        v = part.strip().split(' ')[0]
        if v and not re.match(r'^(https?:|/|data:)', v): r8.add(v)
for v in sorted(r8):
    if fbytes(v) is None: f8.append('missing file: ' + v)
def size(v):
    b = fbytes(v); return Image.open(io.BytesIO(b)).size if b else None
for pim in ps8.select('main#content .pim'):
    if pim.find_parent('div', class_='mm-pdf') is not None: continue
    m = re.search(r'aspect-ratio:\s*([0-9.]+)', pim.get('style') or ''); im = pim.find('img')
    if not im or not m: continue
    src = im.get('data-full') or im.get('src'); sz = size(src or '')
    if sz and abs(float(m.group(1)) - sz[0] / sz[1]) / (sz[0] / sz[1]) > 0.01: f8.append('%s: aspect-ratio %s but the file is %dx%d' % (src, m.group(1), sz[0], sz[1]))
for im in ps8.select('main#content img[width][height]'):
    sz = size(im.get('data-full') or im.get('src') or '')
    if sz and abs(int(im['width']) / int(im['height']) - sz[0] / sz[1]) / (sz[0] / sz[1]) > 0.01: f8.append('%s: width/height %s x %s but the file is %dx%d' % (im.get('src'), im['width'], im['height'], sz[0], sz[1]))
bad += f8
print('%s: %d images named, index.html %d chars (live %d)%s' % (slug, len(refs), len(idx), len(live), ', fix A + copy protection' if prot else ', fix A + the copy-protection style' if sty else ', fix A + copy protection brought up to date' if (upg or rep) else ', fix A alone'))
print('\n'.join('FAULT: ' + b for b in bad) if bad else 'ALL CHECKS OK')
sys.exit(1 if bad else 0)
