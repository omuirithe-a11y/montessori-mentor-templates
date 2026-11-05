#!/usr/bin/env python3
"""format_check_word.py <finished package .zip, or a folder with index.html> <Word .docx> [--settings <page settings .py>]
(31 Oct 2026, owner 21:08 - 8.1, a page with no live version: words compared with the Word file instead of a live page).
The page side is format_check.py's own reading (same script, 1440 and 390): each word the reader sees in the text area with
its colour, italic/upright, bold/regular, underline. The Word side: each word of the document body in order, with its run's
colour, italic, bold, underline (hyperlink text counts as underlined only if Word underlines it).
Prints: words in Word not seen on the page and the reverse; every word whose italic, bold or underline differs; and every pair
(Word colour -> page colour) with its count and first words, so each colour mapping can be checked against the site's colour rules.
Every line is a difference to account for; nothing is judged allowed by this script, except the lines listed apart under
"ALLOWED BY A QUOTED OWNER RULE" (below), which are still printed.

5 Nov 2026 (checkfix, /home/claude/eng35/checkfix/README.md) - the check's own misreadings on The English Curriculum (build 22,
review /home/claude/eng35/checks-plan/format-b22-review.md, class C), each fixed in the reading, not by hiding a line:
 C-MERGE   formats are kept per character on both sides (was: a word took the format of its first run, so the comma after
           an italic title, or the letters after a bold opening quotation mark, were read as italic/bold).
 C-CAPSTYLE a run's format falls back to its paragraph style (and that style's bases) and then the document defaults (was: run
           and character style only, so Word's Caption style, italic, was read as upright).
 C-BULLET  a dash standing alone at the start of a paragraph (a bullet mark) is not a word, on both sides (Word draws its
           list dashes as numbering, not text; the page writes "- " before a citation as text).
 C-TXBX    a text box is read once: paragraphs inside mc:Fallback (Word's second, VML copy of a text box) are skipped, and a
           paragraph's runs are only its own (was: the outer paragraph also read the runs of the text-box paragraphs in it).
 C-TAB     a tab, line break or carriage return in a run is a space (was: a run with a tab and text joined the words).
 C-TOC     the page's contents box (.toc-wrap, outside main#content) is read before main#content (Word's contents list is
           text in the body).
 C-BOM / C-ZWSP  U+FEFF and U+200B (zero width, never seen) are removed on both sides.
 C-SPLIT   the page's text nodes inside one block are joined before splitting into words (was: each node split on its own,
           so "phoneme<tag>s" was two words).
Lines of class A (US to UK spelling, long to short dash) are NOT hidden: a replace whose Word words become the page's words under
the builder's own text rules (tools/build_page.py site_rules and UK table, and the page's TEXT_EDITS when --settings is given)
outside a quotation is printed in a separate list "ALLOWED BY A QUOTED OWNER RULE", with the rule:
 A005 "short dashes only, everywhere on the site" (REQUIRED-CHECKS.txt line 7, preferences.md line 12);
 A023 "always UK English on the site; change US spellings when they appear" (REQUIRED-CHECKS.txt line 24, preferences.md line 24).
Every other line (for example bold in a quotation shown at weight 400, a typing error) stays in the differences."""
import sys, os, zipfile, tempfile, threading, http.server, functools, asyncio, difflib, re, collections, ast, importlib.util
from playwright.async_api import async_playwright
import docx
from docx.oxml.ns import qn
SETTINGS = None
if '--settings' in sys.argv:
    i_ = sys.argv.index('--settings'); SETTINGS = sys.argv[i_ + 1]; del sys.argv[i_:i_ + 2]
Z, DOCX = sys.argv[1], sys.argv[2]
if os.path.isdir(Z):
    idx = [os.path.join(Z, 'index.html')]; assert os.path.exists(idx[0])
else:
    tmp = tempfile.mkdtemp(prefix='fw-'); zipfile.ZipFile(Z).extractall(tmp)
    import atexit, shutil; atexit.register(shutil.rmtree, tmp, True)
    idx = [os.path.join(r, 'index.html') for r, d, f in os.walk(tmp) if 'index.html' in f]; assert len(idx) == 1
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def serve(d):
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=d)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s.server_address[1]
pp = serve(os.path.dirname(idx[0]))
# page side: every text node of the contents box and of main#content, in page order, with its format, the block it sits in
# (nearest ancestor whose display is not inline or contents; an inline-block is a block of its own) and whether it is inside a quotation. Whitespace-only nodes are kept as spaces.
JS = r"""() => { const clipRect = e => { let r = e.getBoundingClientRect(); let L = r.left, T = r.top, Rr = r.right, B = r.bottom;   for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) { const s = getComputedStyle(a);     if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return null;
    if (a.tagName === 'DETAILS' && !a.open) { const sm = a.querySelector(':scope > summary'); if (!sm || !sm.contains(e)) return null; }     if (/(hidden|clip)/.test(s.overflow + s.overflowX + s.overflowY)) { const q = a.getBoundingClientRect(); L = Math.max(L, q.left); T = Math.max(T, q.top); Rr = Math.min(Rr, q.right); B = Math.min(B, q.bottom); if (Rr - L < 1 || B - T < 1) return null; } }   return {left: L, top: T, right: Rr, bottom: B, width: Rr - L, height: B - T}; };
 const ids = new Map(); let nid = 0;
 const blockOf = e => { let b = e; while (b && b.parentElement && ['inline', 'contents'].includes(getComputedStyle(b).display)) b = b.parentElement; if (!ids.has(b)) ids.set(b, ++nid); return ids.get(b); };
 const out = [];
 const roots = [document.querySelector('.toc-wrap'), document.querySelector('main#content')].filter(Boolean);
 for (const m of roots) { const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT); let n;
 while ((n = w.nextNode())) { const e = n.parentElement; if (e.closest('script,style')) continue; const s = getComputedStyle(e); if (s.display === 'none') continue;
  if (!n.nodeValue.trim()) { out.push([' ', '', '', '', '', blockOf(e), false]); continue; }
  let u = false; for (let a = e; a && a !== m.parentElement; a = a.parentElement) if (getComputedStyle(a).textDecorationLine.includes('underline')) { u = true; break; }
  const r0 = document.createRange(); r0.selectNodeContents(n); const rs = [...r0.getClientRects()].filter(q => q.width > 0.5 && q.height > 0.5); if (!rs.length || clipRect(e) === null || s.visibility === 'hidden' || parseFloat(s.opacity) === 0 || parseFloat(s.fontSize) < 4) continue;
  out.push([n.nodeValue, s.color, s.fontStyle === 'italic' ? 'italic' : 'upright', parseInt(s.fontWeight) >= 600 ? 'bold' : 'regular', u ? 'underlined' : '', blockOf(e), !!e.closest('blockquote')]); } }
 const m = document.querySelector('main#content');
 const imgs = [...m.querySelectorAll('img')].filter(i => { const s = getComputedStyle(i), r = i.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 1 && r.height > 1 && clipRect(i) !== null; }).map(i => (i.getAttribute('src') || '').replace(/-(480|960)\.jpg$/, '.jpg'));
 return [out, imgs]; }"""
async def grab(b, port, W):
    ph = W <= 640; ctx = await b.new_context(viewport={'width': W, 'height': 900}, is_mobile=ph, has_touch=ph); pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/' % port, wait_until='load', timeout=60000)
    await pg.evaluate("async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); await document.fonts.ready; [...document.images].forEach(i => { i.loading = 'eager'; }); await Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }))), new Promise(r => setTimeout(r, 20000))]); await new Promise(r => setTimeout(r, 1500)); }"); r = await pg.evaluate(JS); await ctx.close(); return r

D = docx.Document(DOCX); ST = {s.style_id: s for s in D.styles}
DEF_P = next((s.style_id for s in D.styles if s.element.get(qn('w:default')) in ('1', 'true') and s.element.get(qn('w:type')) == 'paragraph'), None)
_dd = D.element.find('.//' + qn('w:docDefaults')); DOC_RPR = _dd.find('.//' + qn('w:rPr')) if _dd is not None else None
def _val(rpr, key):
    x = rpr.find(qn(key)) if rpr is not None else None
    if x is None: return None
    if key == 'w:u': return x.get(qn('w:val')) or 'none'   # 4 Nov 2026: a <w:u> with no w:val (only w:color) is not an underline - Word and its PDF show none (The English Curriculum, 224 such runs); was 'single'
    v = x.get(qn('w:val')); return v if v is not None else 'true'
def _style_chain(sid):   # a style, then the styles it is based on
    out = []
    while sid and sid in ST and len(out) < 10:
        st = ST[sid]; out.append(st.element.find(qn('w:rPr'))); b = st.element.find(qn('w:basedOn')); sid = b.get(qn('w:val')) if b is not None else None
    return out
def rp(r, key, pstyle):   # the run's own setting, else its character style's, else its paragraph style's, else the document default
    e = r.find(qn('w:rPr')); v = _val(e, key)
    if v is not None: return v
    rs = e.find(qn('w:rStyle')) if e is not None else None
    for sr in _style_chain(rs.get(qn('w:val')) if rs is not None else None) + _style_chain(pstyle) + [DOC_RPR]:
        v = _val(sr, key)
        if v is not None: return v
    return None
TOK = re.compile(r"[\w'’]+|[^\w\s]")
ZW = '﻿​'
SEP = ('', '', '', '')   # the format of a space between paragraphs/blocks

def tokens(stream):
    """stream: list of (character, format tuple, in quotation). Returns tokens [text, [formats per character], in quotation]."""
    text = ''.join(c for c, f, q in stream)
    return [[m.group(0), [stream[i][1] for i in range(m.start(), m.end())], stream[m.start()][2]] for m in TOK.finditer(text)]

def bullet_strip(chars):   # C-BULLET: a dash standing alone at the start of a paragraph/block is a bullet mark, not a word
    k = 0
    while k < len(chars) and chars[k][0].isspace(): k += 1
    if k + 1 < len(chars) and chars[k][0] in '-–' and chars[k + 1][0].isspace(): return chars[:k] + chars[k + 1:]
    return chars

# Word side, per character
f_ = lambda v: v not in (None, '0', 'false', 'none')
W_STREAM = []
for p in D.element.body.iter(qn('w:p')):
    if any(a.tag == '{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback' for a in p.iterancestors()): continue   # C-TXBX: Word's VML copy of a text box
    pp_ = p.find(qn('w:pPr')); ps_ = pp_.find(qn('w:pStyle')) if pp_ is not None else None; pstyle = ps_.get(qn('w:val')) if ps_ is not None else DEF_P
    chars = []
    for r in p.iter(qn('w:r')):
        if next(r.iterancestors(qn('w:p'))) is not p: continue   # C-TXBX: runs of a text-box paragraph inside this one are read with that paragraph
        fmt = ((rp(r, 'w:color', pstyle) or 'auto').upper(), 'italic' if f_(rp(r, 'w:i', pstyle)) else 'upright', 'bold' if f_(rp(r, 'w:b', pstyle)) else 'regular', 'underlined' if f_(rp(r, 'w:u', pstyle)) else '')
        for x in r:
            if x.tag == qn('w:t'):
                for c in (x.text or ''):
                    if c not in ZW: chars.append((c, fmt, False))
            elif x.tag in (qn('w:tab'), qn('w:br'), qn('w:cr')): chars.append((' ', SEP, False))   # C-TAB
    W_STREAM += bullet_strip(chars) + [(' ', SEP, False)]

def page_stream(nodes):
    out, cur, blk = [], [], None
    for t, col, it, bo, un, b, q in nodes:
        if b != blk:
            if cur: out += bullet_strip(cur) + [(' ', SEP, False)]
            cur, blk = [], b
        for c in t:
            if c not in ZW: cur.append((c, (col, it, bo, un), q))
    if cur: out += bullet_strip(cur) + [(' ', SEP, False)]
    return out

# the builder's text rules (tools/build_page.py site_rules, UK table, KEEP) and the page's TEXT_EDITS, for the "allowed" list only
BUILDER = '/home/claude/mm/tools/build_page.py'
_tree = ast.parse(open(BUILDER, encoding='utf-8').read()); _got = {}
for _n in _tree.body:
    if isinstance(_n, ast.Assign) and len(_n.targets) == 1 and isinstance(_n.targets[0], ast.Name) and _n.targets[0].id in ('UK', 'KEEP'):
        _got[_n.targets[0].id] = ast.literal_eval(_n.value)
UK, KEEP = _got['UK'], _got['KEEP']; TEXT_EDITS = []
if SETTINGS:
    spec_ = importlib.util.spec_from_file_location('page_settings', SETTINGS); ps__ = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(ps__)
    TEXT_EDITS = list(getattr(ps__, 'TEXT_EDITS', [])); KEEP = KEEP + list(getattr(ps__, 'KEEP_SPELLING', []))
def dash_rule(s): return s.replace('–', '-').replace('—', '-')
def uk_rule(s):
    for pat, r_ in UK:
        s = re.sub(pat, lambda m: m.group(0) if any(k in s[max(0, m.start() - 20):m.end() + 25] for k in KEEP) else m.expand(r_), s)
    for o, n in TEXT_EDITS: s = s.replace(o, n)
    return s
def allowed(WW, P, i1, i2, j1, j2):
    """a replace allowed by a quoted owner rule: the Word words (with 4 words of context each side) become the page's words
    under the dash rule (A005, "everywhere") or the UK rules (A023, not inside a quotation on the page: A109)"""
    inq = any(x[2] for x in P[j1:j2])
    a, b = max(0, i1 - 4), j1 - (i1 - max(0, i1 - 4))
    wtxt = ' '.join(x[0] for x in WW[a:i2 + 4]); ptxt = ' '.join(x[0] for x in P[max(0, b):j2 + 4])
    if dash_rule(wtxt) == ptxt: return 'A005 "short dashes only, everywhere on the site"'
    if inq: return None
    if uk_rule(wtxt) == ptxt or uk_rule(dash_rule(wtxt)) == ptxt: return 'A023 "always UK English on the site; change US spellings when they appear"'
    return None

def fmt_s(fs):
    u = sorted(set(fs))
    if len(u) == 1: return ' '.join(x for x in u[0][1:] if x)
    return 'mixed [' + ', '.join(' '.join(x for x in f[1:] if x) for f in fs) + ']'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); res = {Wd: await grab(b, pp, Wd) for Wd in (1440, 390)}; await b.close()
    n = 0; nal = 0
    WW = tokens(W_STREAM)
    for Wd, (P, PI) in res.items():
        P = tokens(page_stream(P))
        print('-- width', Wd, ': words in Word %d, seen on the page %d (contents box and main), images seen %d' % (len(WW), len(P), len(PI)))
        sm = difflib.SequenceMatcher(None, [x[0] for x in WW], [x[0] for x in P], autojunk=False)
        cols = collections.OrderedDict(); al = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                line = '%s: Word "%s" -> page "%s"' % (tag, ' '.join(x[0] for x in WW[i1:i2])[:200], ' '.join(x[0] for x in P[j1:j2])[:200])
                rule = allowed(WW, P, i1, i2, j1, j2) if tag == 'replace' else None
                if rule: al.append(line + '   [' + rule + ']')
                else: n += 1; print(line)
                continue
            for a, c in zip(WW[i1:i2], P[j1:j2]):
                if [f[1:] for f in a[1]] != [f[1:] for f in c[1]]:
                    n += 1; print('"%s": Word %s -> page %s' % (a[0], fmt_s(a[1]), fmt_s(c[1])))
                k = (a[1][0][0], c[1][0][0]); cols.setdefault(k, []).append(a[0])
        print('colour pairs (Word -> page: count, first words):')
        for (wc, pc), ws in cols.items(): print('  %s -> %s: %d  %s' % (wc, pc, len(ws), ' '.join(ws[:8])))
        print('ALLOWED BY A QUOTED OWNER RULE (width %d, %d lines; still listed, not counted as differences):' % (Wd, len(al)))
        for x in al: print('  ' + x)
        nal += len(al)
    print('RESULT: %d differences (words and italic/bold/underline); %d lines allowed by a quoted owner rule (listed apart); colour pairs listed above for checking against the site\'s colour rules' % (n, nal))
asyncio.run(main())
