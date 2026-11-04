#!/usr/bin/env python3
"""format_check_word.py <finished package .zip> <Word .docx>   (31 Oct 2026, owner 21:08 - 8.1, a page with no live version:
words compared with the Word file instead of a live page). The page side is format_check.py's own reading (same script, 1440 and 390):
each word the reader sees in the text area with its colour, italic/upright, bold/regular, underline. The Word side: each word of the
document body in order, with its run's colour, italic, bold, underline (hyperlink text counts as underlined only if Word underlines it).
Prints: words in Word not seen on the page and the reverse; every word whose italic, bold or underline differs; and every pair
(Word colour -> page colour) with its count and first words, so each colour mapping can be checked against the site's colour rules.
Every line is a difference to account for; nothing is judged allowed by this script."""
import sys, os, zipfile, tempfile, threading, http.server, functools, asyncio, difflib, re, collections
from playwright.async_api import async_playwright
import docx
from docx.oxml.ns import qn
Z, DOCX = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp(prefix='fw-'); zipfile.ZipFile(Z).extractall(tmp)
import atexit, shutil; atexit.register(shutil.rmtree, tmp, True)
idx = [os.path.join(r, 'index.html') for r, d, f in os.walk(tmp) if 'index.html' in f]; assert len(idx) == 1
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def serve(d):
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=d)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s.server_address[1]
pp = serve(os.path.dirname(idx[0]))
JS = r"""() => { const clipRect = e => { let r = e.getBoundingClientRect(); let L = r.left, T = r.top, Rr = r.right, B = r.bottom;   for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) { const s = getComputedStyle(a);     if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return null;
    if (a.tagName === 'DETAILS' && !a.open) { const sm = a.querySelector(':scope > summary'); if (!sm || !sm.contains(e)) return null; }     if (/(hidden|clip)/.test(s.overflow + s.overflowX + s.overflowY)) { const q = a.getBoundingClientRect(); L = Math.max(L, q.left); T = Math.max(T, q.top); Rr = Math.min(Rr, q.right); B = Math.min(B, q.bottom); if (Rr - L < 1 || B - T < 1) return null; } }   return {left: L, top: T, right: Rr, bottom: B, width: Rr - L, height: B - T}; };  const m = document.querySelector('main#content'), out = [], w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT); let n;
 while ((n = w.nextNode())) { const e = n.parentElement; if (!n.nodeValue.trim() || e.closest('script,style')) continue; const s = getComputedStyle(e); if (s.display === 'none') continue;
  let u = false; for (let a = e; a && a !== m.parentElement; a = a.parentElement) if (getComputedStyle(a).textDecorationLine.includes('underline')) { u = true; break; }
  const r0 = document.createRange(); r0.selectNodeContents(n); const rs = [...r0.getClientRects()].filter(q => q.width > 0.5 && q.height > 0.5); if (!rs.length || clipRect(e) === null || s.visibility === 'hidden' || parseFloat(s.opacity) === 0 || parseFloat(s.fontSize) < 4) continue;
  for (const word of n.nodeValue.split(/\s+/)) if (word) out.push([word, s.color, s.fontStyle === 'italic' ? 'italic' : 'upright', parseInt(s.fontWeight) >= 600 ? 'bold' : 'regular', u ? 'underlined' : '']); }
 const imgs = [...m.querySelectorAll('img')].filter(i => { const s = getComputedStyle(i), r = i.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 1 && r.height > 1 && clipRect(i) !== null; }).map(i => (i.getAttribute('src') || '').replace(/-(480|960)\.jpg$/, '.jpg'));
 return [out, imgs]; }"""
async def grab(b, port, W):
    ph = W <= 640; ctx = await b.new_context(viewport={'width': W, 'height': 900}, is_mobile=ph, has_touch=ph); pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/' % port, wait_until='load', timeout=60000)
    await pg.evaluate("async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); await document.fonts.ready; [...document.images].forEach(i => { i.loading = 'eager'; }); await Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }))), new Promise(r => setTimeout(r, 20000))]); await new Promise(r => setTimeout(r, 1500)); }"); r = await pg.evaluate(JS); await ctx.close(); return r

D = docx.Document(DOCX); ST = {s.style_id: s for s in D.styles}
def _val(rpr, key):
    x = rpr.find(qn(key)) if rpr is not None else None
    if x is None: return None
    if key == 'w:u': return x.get(qn('w:val')) or 'none'   # 4 Nov 2026: a <w:u> with no w:val (only w:color) is not an underline - Word and its PDF show none (The English Curriculum, 224 such runs); was 'single'
    v = x.get(qn('w:val')); return v if v is not None else 'true'
def _style_chain(sid):   # character style, then the styles it is based on
    out = []
    while sid and sid in ST and len(out) < 10:
        st = ST[sid]; out.append(st.element.find(qn('w:rPr'))); b = st.element.find(qn('w:basedOn')); sid = b.get(qn('w:val')) if b is not None else None
    return out
def rp(r, key):   # the run's own setting, else its character style's (e.g. Word's Hyperlink style underlines)
    e = r.find(qn('w:rPr')); v = _val(e, key)
    if v is not None: return v
    rs = e.find(qn('w:rStyle')) if e is not None else None
    for sr in _style_chain(rs.get(qn('w:val')) if rs is not None else None):
        v = _val(sr, key)
        if v is not None: return v
    return None
TOK = re.compile(r"[\w'’]+|[^\w\s]")
def tok(seq):   # word and punctuation pieces, each keeping its formatting (the page splits text at every element edge)
    out = []
    for x in seq:
        for t in TOK.findall(x[0]): out.append([t] + list(x[1:]))
    return out
# rebuild with spacing: a run whose text starts without a space continues the previous word
words = []
for p in D.element.body.iter(qn('w:p')):
    cont = False
    for r in p.iter(qn('w:r')):
        t = ''.join(x.text or '' for x in r if x.tag == qn('w:t'))
        if r.find(qn('w:tab')) is not None and not t: cont = False; continue
        if not t: continue
        f = lambda v: v not in (None, '0', 'false', 'none')
        fmt = [(rp(r, 'w:color') or 'auto').upper(), 'italic' if f(rp(r, 'w:i')) else 'upright', 'bold' if f(rp(r, 'w:b')) else 'regular', 'underlined' if f(rp(r, 'w:u')) else '']
        parts = re.split(r'(\s+)', t)
        for k, piece in enumerate(parts):
            if not piece: continue
            if piece.isspace(): cont = False; continue
            if cont and words: words[-1][0] += piece
            else: words.append([piece] + fmt)
            cont = True
    cont = False
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); res = {Wd: await grab(b, pp, Wd) for Wd in (1440, 390)}; await b.close()
    n = 0
    for Wd, (P, PI) in res.items():
        print('-- width', Wd, ': words in Word %d, seen on the page %d, images seen %d' % (len(words), len(P), len(PI)))
        P = tok(P); WW = tok(words)
        sm = difflib.SequenceMatcher(None, [x[0] for x in WW], [x[0] for x in P], autojunk=False)
        cols = collections.OrderedDict()
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                n += 1; print('%s: Word "%s" -> page "%s"' % (tag, ' '.join(x[0] for x in WW[i1:i2])[:200], ' '.join(x[0] for x in P[j1:j2])[:200])); continue
            for a, c in zip(WW[i1:i2], P[j1:j2]):
                if a[2:] != list(c[2:]):
                    n += 1; print('"%s": Word %s -> page %s' % (a[0], ' '.join(x for x in a[2:] if x), ' '.join(x for x in c[2:] if x)))
                k = (a[1], c[1]); cols.setdefault(k, []).append(a[0])
        print('colour pairs (Word -> page: count, first words):')
        for (wc, pc), ws in cols.items(): print('  %s -> %s: %d  %s' % (wc, pc, len(ws), ' '.join(ws[:8])))
    print('RESULT: %d differences (words and italic/bold/underline); colour pairs listed above for checking against the site\'s colour rules' % n)
asyncio.run(main())
