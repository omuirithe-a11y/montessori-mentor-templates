#!/usr/bin/env python3
"""live_diff.py <candidate.zip> <live page folder> - the code check for a page corrected from its live copy (owner 29 Oct 2026, 11:50:
"yes" - the corrected page is compared with the live page, and passes only if the differences are exactly the agreed changes).
Undoes each agreed change (each must be found exactly once); the result must equal the live index.html byte for byte.
Every other file must be in both, byte-identical, and the folder must hold the same files (uploads replace folders: rule 10).
Prints ALL CHECKS OK or the faults."""
import sys, zipfile, os, re, hashlib
Z, L = sys.argv[1], sys.argv[2]
zf = zipfile.ZipFile(Z); names = [n for n in zf.namelist() if not n.endswith('/')]
slug = names[0].split('/')[0]; bad = []
idx = zf.read(slug + '/index.html').decode('utf-8'); live = open(os.path.join(L, 'index.html'), encoding='utf-8').read()
c = idx
for sid in ('mm-toc-align', 'mm-type-29oct', 'mm-quote-image-29oct'):
    c, k = re.subn(r'<style id="%s">.*?</style>' % sid, '', c, flags=re.S)
    if k != 1: bad.append('block %s found %d times' % (sid, k))
c, k = re.subn(r'<script id="mm-image-gap-29oct">.*?</script>', '', c, flags=re.S)   # owner 12:12: "they should all have a gap of 30"
if k != 1: bad.append('block mm-image-gap-29oct found %d times' % k)
PAIRS = [
 ("var isFl = function(e){ return e && (e.classList.contains('mm-float') || e.classList.contains('mm-fspacer')) && getComputedStyle(e).cssFloat !== 'none'; };   /* 29 Oct 2026: an image box only counts as beside the text while it floats - at 830px and narrower it stands in the text, and skipping it pulled the next text up over the image */",
  "var isFl = function(e){ return e && (e.classList.contains('mm-float') || e.classList.contains('mm-fspacer')); };"),
 ("if (!e || e.nodeType !== 1 || !(e.classList.contains('mm-row') || (e.classList.contains('mm-float') && getComputedStyle(e).cssFloat === 'none'))) return null;   /* 29 Oct 2026: an image box standing in the text is measured like a row */",
  "if (!e || e.nodeType !== 1 || !e.classList.contains('mm-row')) return null;"),
 ("var rowLike = function(e){ return e && (e.classList.contains('mm-row') || (e.classList.contains('mm-float') && getComputedStyle(e).cssFloat === 'none')); };\n      if (rowLike(nx)) nx.style.setProperty('margin-top', '0px', 'important');",
  "if (nx && nx.classList.contains('mm-row')) nx.style.setProperty('margin-top', '0px', 'important');"),
 ("(stk ? 30 : (rowLike(nx) || rowLike(pv) || (nx && nx.tagName === 'BLOCKQUOTE' && nx.firstElementChild && rowLike(nx.firstElementChild)) ? TP : T))",
  "((nx && nx.classList.contains('mm-row')) || (pv && pv.classList.contains('mm-row')) ? TP : T)"),
 ("var lead = nx && nx.tagName === 'BLOCKQUOTE' && nx.firstElementChild && nx.firstElementChild.classList.contains('mm-float') && getComputedStyle(nx.firstElementChild).cssFloat === 'none' ? nx.firstElementChild : null;   /* 29 Oct 2026: a quotation that opens with its image standing above the text is measured from the image */\n        var it = lead ? lead.getBoundingClientRect().top : (isTxt(nx) ? glInkTop(nx) : edge(nx, true));",
  "var it = isTxt(nx) ? glInkTop(nx) : edge(nx, true);")]
PAIRS.insert(0, ("var stk = nx && nx.classList.contains('mm-float') && rowLike(nx);   /* 29 Oct 2026 (owner 12:15): 30 from the last line's letters (baseline) to an image standing above its text */\n        var ib = stk && isTxt(pv) ? (function(){ var ws = glWords(pv); if (!ws.length) return null; var mb = Math.max.apply(null, ws.map(function(x){ return x.bottom; })), b = -1e9; ws.forEach(function(x){ if (Math.abs(x.bottom - mb) < 2) b = Math.max(b, x.top + glExt(x).fa); }); return b; })() : (isTxt(pv) ? glInkBottom(pv) : edge(pv, false));", 'var ib = isTxt(pv) ? glInkBottom(pv) : edge(pv, false);'))   # owner 12:15
PAIRS.append(("q('main .mm-float[data-topline]').forEach(function(f){\n      var sp = f.previousElementSibling; if (sp && sp.classList.contains('mm-fspacer')) sp.parentNode.removeChild(sp);\n      if (getComputedStyle(f).cssFloat === 'none') return;   /* 29 Oct 2026: an image standing above its text (830px and narrower) has no text beside it to line up with - its space above is set by the quotation-line script (owner 12:15: 30) */ f.style.removeProperty('margin-top');", "q('main .mm-float[data-topline]').forEach(function(f){\n      var sp = f.previousElementSibling; if (sp && sp.classList.contains('mm-fspacer')) sp.parentNode.removeChild(sp);\n      f.style.removeProperty('margin-top');"))   # 29 Oct: glTopline leaves stacked images alone
PAIRS.append(("q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', function(){ var r = document.querySelector('main').getBoundingClientRect(), m = window.__mmSize; if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return; schedule(); }); });   /* 29 Oct 2026 (owner 17:19, fix A): an image that loads re-spaces the page only if the page's size changed - measured: 0 of 49 passes moved anything, and they delayed clicks 2-5 s */", "q('img.doc-img').forEach(function(i){ if (!i.complete) i.addEventListener('load', schedule); });"))   # 29 Oct 17:19: fix A, image loads re-space only on a size change
for new, old in PAIRS:
    k = c.count(new)
    if k != 1: bad.append('script change found %d times: %s' % (k, new[:60]))
    c = c.replace(new, old)
if c != live:
    import difflib
    d = [x for x in difflib.unified_diff(live.split('><'), c.split('><'), lineterm='', n=0) if x[:1] in '+-' and x[:3] not in ('+++', '---')]
    bad.append('%d other differences from the live page, e.g. %s' % (len(d), [x[:120] for x in d[:4]]))
lf = sorted(os.path.relpath(os.path.join(r, f), L) for r, _, fs in os.walk(L) for f in fs)
zfs = sorted(n[len(slug) + 1:] for n in names)
if lf != zfs: bad.append('files differ from the live folder: only in zip %s, only live %s' % (sorted(set(zfs) - set(lf))[:5], sorted(set(lf) - set(zfs))[:5]))
for n in zfs:
    if n == 'index.html' or n not in lf: continue
    if zf.read(slug + '/' + n) != open(os.path.join(L, n), 'rb').read(): bad.append('file differs from live: ' + n)
print('%s: %d files, index.html %d chars (live %d)' % (slug, len(zfs), len(idx), len(live)))
print('\n'.join('FAULT: ' + b for b in bad) if bad else 'ALL CHECKS OK')
sys.exit(1 if bad else 0)
