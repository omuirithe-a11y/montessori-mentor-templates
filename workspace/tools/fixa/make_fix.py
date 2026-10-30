#!/usr/bin/env python3
"""make_fix.py <live folder>/<slug> <protection file> <out check zip> [--protect | --style-only | --upgrade | --replace]   (30 Oct 2026)
Fix A (the 29 Oct line, owner 17:19) on the live index.html; with --protect also copy protection (the owner's 15:49 "Yes" for the
7 pages without it), inserted exactly as build_page.py does: the mm-protect style before </head>, the mm-protect-js script
before </body>. Writes the CHECK zip (index.html + the downloaded images, for checking only) and <out>.index.html (the file
delivered)."""
import sys, os, re, zipfile
L, P, Z = sys.argv[1], sys.argv[2], sys.argv[3]; prot = '--protect' in sys.argv; sty = '--style-only' in sys.argv; upg = '--upgrade' in sys.argv; rep = '--replace' in sys.argv; slug = os.path.basename(L.rstrip('/'))
OLD = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"
NEW = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */"
s = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
nofix = '--no-fixa' in sys.argv   # 30 Oct 21:2x: protection only, for pages without the old line (home, play)
if nofix: assert s.count(OLD) == 0 and s.count(NEW) == 0
else:
    assert s.count(OLD) == 1, 'old line %d times' % s.count(OLD)
    s = s.replace(OLD, NEW)
if prot:
    pr = open(P, encoding='utf-8').read()
    css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
    assert s.count('</head>') == 1 and s.count('</body>') == 1 and 'mm-protect' not in s
    s = s.replace('</head>', css + '</head>', 1).replace('</body>', js + '</body>', 1)
if sty:   # 30 Oct 19:5x (owner 19:56 "add fix A and copy protection to all pages that need it"): the page has the mm-protect-js script but no mm-protect style
    pr = open(P, encoding='utf-8').read(); css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0)
    assert s.count('</head>') == 1 and s.count('id="mm-protect-js"') == 1 and 'id="mm-protect"' not in s
    s = s.replace('</head>', css + '</head>', 1)
if upg:   # 30 Oct 20:0x: the page has the OLDER protection script (28 Sept: protects main and hero only, no paste/selectstart block) and no style - replace that script with the current one word for word and add the style
    pr = open(P, encoding='utf-8').read(); css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
    old_js = re.findall(r'<script id="mm-protect-js">.*?</script>', s, re.S)
    assert len(old_js) == 1 and old_js[0] != js and 'id="mm-protect"' not in s and s.count('</head>') == 1
    s = s.replace(old_js[0], js, 1).replace('</head>', css + '</head>', 1)
if rep:   # 30 Oct 20:3x: the page has an older protection style AND script - replace both, word for word, in their places
    pr = open(P, encoding='utf-8').read(); css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
    oc = re.findall(r'<style id="mm-protect">.*?</style>', s, re.S); oj = re.findall(r'<script id="mm-protect-js">.*?</script>', s, re.S)
    assert len(oc) == 1 and len(oj) == 1 and (oc[0] != css or oj[0] != js)
    s = s.replace(oc[0], css, 1).replace(oj[0], js, 1)
open(Z + '.index.html', 'w', encoding='utf-8').write(s)
with zipfile.ZipFile(Z, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(slug + '/index.html', s)
    for r, _, fs in os.walk(L):
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, L)
            if rel != 'index.html': z.write(p, slug + '/' + rel)
print('made', Z, '(fix A%s)' % (' + copy protection' if prot else ' + the copy-protection style' if sty else ' + copy protection brought up to date' if (upg or rep) else ''))
