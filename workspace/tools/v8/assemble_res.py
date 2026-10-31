"""assemble.py <template.html> <live index.html> <out folder>   (31 Oct 2026, owner 14:53: "in this instance building from the live
page counts as a rebuild"). The template's code everywhere; from the live page only the slots the code check allows to differ:
the title, the hero title, the contents entries, the menu entries and main's content (main's scripts come from the template).
Writes <out>/preview/index.html (no copy protection) and <out>/hostinger/index.html (copy protection added as build_page.py does)."""
import sys, re, os
T, L, O = sys.argv[1:4]
t = open(T, encoding='utf-8').read(); l = open(L, encoding='utf-8').read()
def one(pat, x):
    m = list(re.finditer(pat, x, re.S)); assert len(m) == 1, (pat, len(m)); return m[0]
# title
t = t.replace(one(r'<title>.*?</title>', t).group(0), one(r'<title>.*?</title>', l).group(0))
# hero title
ht = one(r'(<div class="hero"[^>]*>)<h1>(.*?)</h1>', t); hl = one(r'(<div class="hero"[^>]*>)<h1>(.*?)</h1>', l)
assert ht.group(1) == hl.group(1), 'hero tag differs'
t = t[:ht.start()] + hl.group(0) + t[ht.end():]
# contents entries
gt = one(r'<div class="toc-grid[^"]*">.*?</div>', t); gl = one(r'<div class="toc-grid[^"]*">.*?</div>', l)
assert gt.group(0).count('<ul class="toc-groups">') == gl.group(0).count('<ul class="toc-groups">')
t = t[:gt.start()] + gl.group(0) + t[gt.end():]
# menu entries: the menu list as on live (current page marked)
mt = one(r'<ul class="menu"[^>]*>.*?</ul>\s*</nav>', t) if '<ul class="menu"' in t else None
assert mt, 'menu list not found'
ml = one(r'<ul class="menu"[^>]*>.*?</ul>\s*</nav>', l)
t = t[:mt.start()] + ml.group(0) + t[mt.end():]
# main content: live's children without scripts, then the template's scripts
mT = one(r'(<main[^>]*>)(.*?)(</main>)', t); mL = one(r'(<main[^>]*>)(.*?)(</main>)', l)
assert mT.group(1) == mL.group(1), 'main tag differs'
tscripts = ''.join(re.findall(r'<script\b.*?</script>', mT.group(2), re.S))
lcontent = re.sub(r'<script\b.*?</script>', '', mL.group(2), flags=re.S)
n0 = len(re.findall(r'<img\b[^>]*\balt="[^"]+"', lcontent))
lcontent = re.sub(r'(<img\b[^>]*\balt=)"[^"]*"', r'\1""', lcontent)   # 28 Oct (owner): image descriptions "are not necessary anymore"; 30 Oct 12:26 "yes": rebuilt pages lose theirs
print('descriptions removed:', n0)
t = t[:mT.start()] + mT.group(1) + lcontent + tscripts + mT.group(3) + t[mT.end():]
os.makedirs(O + '/preview', exist_ok=True); os.makedirs(O + '/hostinger', exist_ok=True)
open(O + '/preview/index.html', 'w', encoding='utf-8').write(t)
pr = open('/home/claude/mm/templates/copy-protection.html', encoding='utf-8').read()
css = one(r'<style id="mm-protect">.*?</style>', pr).group(0); js = one(r'<script id="mm-protect-js">.*?</script>', pr).group(0)
assert t.count('</head>') == 1 and t.count('</body>') == 1 and 'mm-protect' not in t
open(O + '/hostinger/index.html', 'w', encoding='utf-8').write(t.replace('</head>', css + '</head>', 1).replace('</body>', js + '</body>', 1))
print('built', len(t), 'bytes (preview);', len(t) + len(css) + len(js), 'with protection')
