#!/usr/bin/env python3
"""make_fix.py <live folder>/<slug> <protection file> <out check zip> [--protect]   (30 Oct 2026)
Fix A (the 29 Oct line, owner 17:19) on the live index.html; with --protect also copy protection (the owner's 15:49 "Yes" for the
7 pages without it), inserted exactly as build_page.py does: the mm-protect style before </head>, the mm-protect-js script
before </body>. Writes the CHECK zip (index.html + the downloaded images, for checking only) and <out>.index.html (the file
delivered)."""
import sys, os, re, zipfile
L, P, Z = sys.argv[1], sys.argv[2], sys.argv[3]; prot = '--protect' in sys.argv; slug = os.path.basename(L.rstrip('/'))
OLD = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"
NEW = "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */"
s = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
assert s.count(OLD) == 1, 'old line %d times' % s.count(OLD)
s = s.replace(OLD, NEW)
if prot:
    pr = open(P, encoding='utf-8').read()
    css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
    assert s.count('</head>') == 1 and s.count('</body>') == 1 and 'mm-protect' not in s
    s = s.replace('</head>', css + '</head>', 1).replace('</body>', js + '</body>', 1)
open(Z + '.index.html', 'w', encoding='utf-8').write(s)
with zipfile.ZipFile(Z, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(slug + '/index.html', s)
    for r, _, fs in os.walk(L):
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, L)
            if rel != 'index.html': z.write(p, slug + '/' + rel)
print('made', Z, '(fix A%s)' % (' + copy protection' if prot else ''))
