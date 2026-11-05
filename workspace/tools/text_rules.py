#!/usr/bin/env python3
"""text_rules.py <page folder> <word.docx> <out dir> [--settings pages/<page>.py]   (5 Nov 2026, plan item 2:
/home/claude/eng35/checks-plan/PLAN.md)

The site's text rules on a built page's visible text. Rows (tools/REQUIRED-CHECKS.json): A005, A006, A023, A108, A062,
A091, A102, A107, A109, A111, A112, A113, D139, E017.

How the text is read: the folder is served over local http (as tools/col_check.py) and opened in Playwright Chromium.
Every text node of the body is read with its element; a node counts when its element is visible
(Element.checkVisibility with opacity and visibility) at 1440 x 900 or at 390 x 844, or when it is inside the site menu
(header.site-head: its panels are hidden until opened, but their words are shown on the site). Text inside script, style,
noscript and template is never read. Text nodes are joined per block element (p, li, h1-h6, td ...) as the browser
shows them; a <br> counts as a line break. CSS ::before/::after content is read too, for long dashes.

Faults (each line names its row):
  A005  a long dash (en dash U+2013, em dash U+2014) anywhere in the visible text, quotations included
  A006  a space (or no-break space) before or after a "/"
  A023/A108  a US spelling: the patterns are the builder's own UK table (tools/build_page.py UK, read from that file at
        run time, so the check and the build use one list); see NOTE A023 below
  A062  "lead guide" written any other way than "Lead Guide" (plural "Lead Guides" allowed)
  A107  "judgmental"
  A111  "math" as a word ("maths" is right)
  D139  "Froëbel"
  A109  a word the page changed from Word (a spelling correction) inside a quotation
Exempt from the word rules (A023/A108, A062, A107, A111, D139), per A109: text inside blockquote, q or cite; text between
quotation marks (“...”, "...", ‘...’); organisation names and published titles the build keeps (tools/build_page.py KEEP
and the page settings' KEEP_SPELLING, when --settings is given). Each exempt match is listed in doubts.txt.
Allowed always: "artifacts" (A112), "kids" (A113).
Typos (A091, A102, E017): there is no en_GB dictionary here, so possible typos are not faults: words not in the en_US
hunspell dictionary (/usr/share/hunspell/en_US.dic, with its affix rules), after allowing UK forms, go to
<out dir>/doubts.txt for the owner.
<out dir>/corrections.txt: each correction the page makes against Word (word in Word -> word on page, rule, count),
found by comparing the Word text with the page's own text (hero, contents, main) word by word, so the word check can
allow them.
Prints one line per fault, then TEXT PASS or TEXT FAULT (n), then END. The same lines go to <out dir>/text-result.txt.
Exit 0 only on TEXT PASS."""
import sys, os, re, ast, asyncio, http.server, threading, functools, socket, unicodedata, difflib, collections, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:]]
SETTINGS = None
if '--settings' in args:
    i = args.index('--settings'); SETTINGS = args[i + 1]; del args[i:i + 2]
if len(args) != 3:
    print(__doc__); print('TEXT FAULT (1)'); print('END'); sys.exit(2)
FOLDER, WORD, OUT = args
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- the rules' word lists, each from its row's quote
# A005 "short dashes only, everywhere on the site" - pass: "no long (en/em) dashes in page text"
LONG_DASHES = {'–': 'en dash', '—': 'em dash'}
# A006 'no spaces around a slash ("Junk/Adventure")'
SLASH_RE = re.compile(r'\s/|/\s')
# A062 "\"capitalise 'Lead Guide' always\" on the site's pages"
LEAD_RE = re.compile(r'\blead[\s\-]*guide(s?)\b', re.I)
LEAD_OK = re.compile(r'Lead Guides?')
# A107 "\"Always use judgemental\" (26 Oct 2026) - that spelling everywhere on the site, not \"judgmental\""
JUDG_RE = re.compile(r'\bjudgmental(ly)?\b', re.I)
# A111 "\"maths\", never \"math\", in ordinary text on the site"
MATH_RE = re.compile(r'\bmath\b', re.I)
# D139 "23 Oct 2026 (owner): Fröbel, not Froëbel as in 1. Menu.docx and 7.0 Education.docx"
FROEBEL_RE = re.compile(r'Froëbel', re.I)
# A112 "\"artifacts\" stays as spelt"; A113 "\"kids\" stays (ordinary British English)"
ALLOWED = re.compile(r'^(artifacts?|kids?)$', re.I)

# A023 "always UK English on the site; change US spellings when they appear" / A108 "USE BRITISH ENGLISH IN ALL INSTANCES":
# the rows give no word list. NOTE A023: the patterns are the build's UK table and KEEP list (tools/build_page.py), read
# from that file here - not a list written for this check, and not from a row's quote.
def _builder_lists():
    src = open(os.path.join(HERE, 'build_page.py'), encoding='utf-8').read()
    tree = ast.parse(src); got = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('UK', 'KEEP'):
            got[node.targets[0].id] = ast.literal_eval(node.value)
    return got['UK'], got['KEEP']
UK, KEEP = _builder_lists()
UK_RE = [(re.compile(p), r) for p, r in UK]
TEXT_EDITS = []
if SETTINGS:   # the page's own settings: KEEP_SPELLING (A109 names and titles) and TEXT_EDITS (owner's wording changes)
    spec = importlib.util.spec_from_file_location('page_settings', SETTINGS); ps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ps)
    KEEP = list(KEEP) + list(getattr(ps, 'KEEP_SPELLING', []))
    TEXT_EDITS = list(getattr(ps, 'TEXT_EDITS', []))

def nfc(s): return unicodedata.normalize('NFC', s)

# ---------------------------------------------------------------- the page's visible text (Playwright)
JS_COLLECT = r"""() => {
  const BLOCK = new Set(['P','LI','H1','H2','H3','H4','H5','H6','FIGCAPTION','BLOCKQUOTE','TD','TH','DT','DD','DIV','SECTION','MAIN',
    'NAV','HEADER','FOOTER','ASIDE','UL','OL','DL','BUTTON','FIGURE','CAPTION','BODY','ARTICLE','TABLE','TR','PRE','ADDRESS','FORM','LABEL']);
  const SKIP = 'script,style,noscript,template';
  const blocks = new Map(); let nb = 0;
  const blockOf = el => { let e = el; while (e && !BLOCK.has(e.tagName)) e = e.parentElement; e = e || document.body;
    if (!blocks.has(e)) blocks.set(e, {i: nb++, tag: e.tagName.toLowerCase(), cls: (e.getAttribute('class') || '')}); return blocks.get(e); };
  const region = el => el.closest('header.site-head') ? 'menu' : el.closest('.hero') ? 'hero' : el.closest('.toc-wrap,.toc') ? 'contents'
    : el.closest('main') ? 'main' : el.closest('.mc-band') ? 'band' : el.closest('footer') ? 'footer' : el.closest('.lightbox') ? 'lightbox' : 'other';
  const vis = el => el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true, opacityProperty: true, visibilityProperty: true});
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
  const out = []; window.__tn = []; let n;
  while ((n = w.nextNode())) {
    if (n.nodeType === 1) { if (n.tagName === 'BR' && !n.closest(SKIP)) { window.__tn.push(n); const b = blockOf(n.parentElement);
        out.push({t: '\n', b: b.i, btag: b.tag, bcls: b.cls, q: !!n.closest('blockquote,q,cite'), it: false, reg: region(n), v: vis(n.parentElement)}); } continue; }
    const el = n.parentElement; if (!el || el.closest(SKIP)) continue;
    if (!n.nodeValue) continue;
    window.__tn.push(n); const b = blockOf(el);
    let sep = false; for (let e = el; e && !BLOCK.has(e.tagName); e = e.parentElement) if (!getComputedStyle(e).display.startsWith('inline') || getComputedStyle(e).display === 'inline-block') { sep = true; break; }
    out.push({t: n.nodeValue, sep: sep, b: b.i, btag: b.tag, bcls: b.cls, q: !!el.closest('blockquote,q,cite'),
      it: !!el.closest('i,em') || getComputedStyle(el).fontStyle === 'italic', reg: region(el), v: vis(el)});
  }
  // CSS-generated text (::before / ::after) of visible elements, for long dashes
  const pseudo = [];
  for (const el of document.body.querySelectorAll('*')) { if (el.closest(SKIP)) continue;
    for (const ps of ['::before', '::after']) { const c = getComputedStyle(el, ps).content;
      if (c && c !== 'none' && c !== 'normal' && /[–—]/.test(c) && (vis(el) || el.closest('header.site-head')))
        pseudo.push({el: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.getAttribute('class') ? '.' + el.getAttribute('class').trim().split(/\s+/).join('.') : ''), ps: ps, c: c, reg: region(el)}); } }
  return {nodes: out, pseudo: pseudo};
}"""
JS_VIS_AGAIN = r"""() => { const vis = el => el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true, opacityProperty: true, visibilityProperty: true});
  return window.__tn.map(n => !!(n.isConnected && n.parentElement && vis(n.parentElement))); }"""

async def read_page():
    from playwright.async_api import async_playwright
    port = (lambda s: (s.bind(('127.0.0.1', 0)), s.getsockname()[1], s.close())[1])(socket.socket())
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=FOLDER)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto('http://127.0.0.1:%d/' % port, wait_until='domcontentloaded', timeout=120000); await pg.wait_for_timeout(4000)
        r = await pg.evaluate(JS_COLLECT)
        await pg.set_viewport_size({'width': 390, 'height': 844}); await pg.wait_for_timeout(2500)
        v390 = await pg.evaluate(JS_VIS_AGAIN)
        await b.close()
    srv.shutdown()
    for nd, v in zip(r['nodes'], v390): nd['v390'] = v
    return r

# ---------------------------------------------------------------- blocks with a flag per character
class Block:
    def __init__(s, i, tag, cls, reg): s.i, s.tag, s.cls, s.reg = i, tag, cls, reg; s.chars = []; s.q = []; s.it = []
def build_blocks(nodes):
    bl = {}; order = []
    for nd in nodes:
        if not (nd['v'] or nd.get('v390') or nd['reg'] == 'menu'): continue
        if nd['b'] not in bl: bl[nd['b']] = Block(nd['b'], nd['btag'], nd['bcls'], nd['reg']); order.append(nd['b'])
        B = bl[nd['b']]
        if nd.get('sep') and B.chars:   # a flex item or inline-block (e.g. the footer's two parts) stands apart from its neighbours
            B.chars.append(' '); B.q.append(nd['q']); B.it.append(nd['it']); B.sepnext = True
        elif getattr(B, 'sepnext', False) and B.chars:
            B.chars.append(' '); B.q.append(nd['q']); B.it.append(nd['it'])
        B.sepnext = bool(nd.get('sep'))
        for ch in nfc(nd['t']):
            B.chars.append(ch); B.q.append(nd['q']); B.it.append(nd['it'])
    res = []
    for k in order:
        B = bl[k]; t, q, it = [], [], []
        for ch, a, c in zip(B.chars, B.q, B.it):   # collapse white space as the browser shows it (no-break space kept as a space)
            if ch.isspace():
                if t and t[-1] == ' ': continue
                ch = ' '
            t.append(ch); q.append(a); it.append(c)
        while t and t[0] == ' ': t.pop(0); q.pop(0); it.pop(0)
        while t and t[-1] == ' ': t.pop(); q.pop(); it.pop()
        if not t: continue
        B.text = ''.join(t); B.qel = q; B.ital = it; B.qspan = quoted_spans(B.text); res.append(B)
    return res

def quoted_spans(s):
    """Characters between quotation marks: “...” (to the block's end when not closed), "..." pairs, ‘...’ (a ‘ not after a
    letter, closed by a ’ not followed by a letter)."""
    m = [False] * len(s); i = 0; n = len(s)
    while i < n:
        c = s[i]
        if c == '“':
            j = s.find('”', i + 1); j = n - 1 if j < 0 else j
            for k in range(i, j + 1): m[k] = True
            i = j + 1; continue
        if c == '"':
            j = s.find('"', i + 1)
            if j > 0:
                for k in range(i, j + 1): m[k] = True
                i = j + 1; continue
        if c == '‘' and (i == 0 or not s[i - 1].isalnum()):
            j = i + 1
            while j < n and not (s[j] == '’' and (j + 1 >= n or not s[j + 1].isalpha())): j += 1
            if j < n:
                for k in range(i, j + 1): m[k] = True
                i = j + 1; continue
        i += 1
    return m

def ctx(B, a, b, w=45):
    s = B.text; return ('...' if a > w else '') + s[max(0, a - w):a] + '[' + s[a:b] + ']' + s[b:b + w] + ('...' if b + w < len(s) else '')

def where(B): return '%s %s%s' % (B.reg, B.tag, ('.' + '.'.join(B.cls.split()[:2])) if B.cls.strip() else '')

def kept_by_name(B, a, b):
    for k in KEEP:
        for m in re.finditer(re.escape(k), B.text):
            if m.start() < b and a < m.end(): return k
    return None

# ---------------------------------------------------------------- en_US hunspell (doubts only)
def load_hunspell(base='/usr/share/hunspell/en_US'):
    aff = open(base + '.aff', encoding='utf-8', errors='replace').read().splitlines()
    rules = {}; i = 0
    while i < len(aff):
        f = aff[i].split()
        if len(f) >= 4 and f[0] in ('PFX', 'SFX') and f[2] in ('Y', 'N') and f[3].isdigit():
            kind, flag, cross, cnt = f[0], f[1], f[2] == 'Y', int(f[3]); rs = []
            for line in aff[i + 1:i + 1 + cnt]:
                g = line.split()
                strip = '' if g[2] == '0' else g[2]; add = '' if g[3].split('/')[0] == '0' else g[3].split('/')[0]
                cond = g[4] if len(g) > 4 else '.'
                rs.append((strip, add, re.compile((cond + '$') if kind == 'SFX' else ('^' + cond))))
            rules[flag] = (kind, cross, rs); i += cnt + 1; continue
        i += 1
    words = set()
    for line in open(base + '.dic', encoding='utf-8', errors='replace').read().splitlines()[1:]:
        st, _, fl = line.partition('/'); st = st.strip()
        if not st: continue
        forms = {st}; sfx = set()
        for f in fl:
            r = rules.get(f)
            if r and r[0] == 'SFX':
                for strip, add, cond in r[2]:
                    if cond.search(st) and (not strip or st.endswith(strip)):
                        w = (st[:-len(strip)] if strip else st) + add; forms.add(w)
                        if r[1]: sfx.add(w)
        for f in fl:
            r = rules.get(f)
            if r and r[0] == 'PFX':
                for strip, add, cond in r[2]:
                    for base_ in [st] + (list(sfx) if r[1] else []):
                        if cond.search(base_): forms.add(add + base_[len(strip):])
        for w in forms: words.add(w.lower())
    return words

UK_TO_US = [(r'our(s|ed|ing|ful|ite|ites|able|ably|al)?$', r'or\1'), (r'is(e|ed|es|ing|ation|ations|er|ers)$', r'iz\1'),
            (r'ys(e|ed|es|ing)$', r'yz\1'), (r'tre(s)?$', r'ter\1'), (r'ogue(s)?$', r'og\1'), (r'll(ed|ing|er|ers|ous)$', r'l\1'), (r'is(e|ed|es|ing)$', r'ic\1'),
            (r'mme(s)?$', r'm\1'), (r'ence(s)?$', r'ense\1'), (r'ae', 'e'), (r'oe', 'e'), (r'ement', 'ment'), (r'^maths$', 'math')]
def known(w, D):
    lw = w.lower().replace('’', "'")
    if lw in D: return True
    lw2 = re.sub(r"'s$", '', lw)
    if lw2 in D: return True
    for p, r in UK_TO_US:   # UK forms count as known words (doubts only; not used for faults)
        v = re.sub(p, r, lw2)
        if v != lw2 and v in D: return True
    return False

# ---------------------------------------------------------------- Word text (python-docx)
def word_paragraphs(path):
    from docx import Document
    from docx.oxml.ns import qn
    d = Document(path); out = []
    MCF = '{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback'
    for p in d.element.body.iter(qn('w:p')):
        a = p.getparent(); skip = False
        while a is not None:
            if a.tag == MCF: skip = True; break
            a = a.getparent()
        if skip: continue
        s = []
        for e in p.iter(qn('w:t'), qn('w:tab'), qn('w:br'), qn('w:cr')):
            a = e.getparent()   # a text box's paragraphs are read on their own: keep only this paragraph's own text
            while a is not None and a.tag != qn('w:p'): a = a.getparent()
            if a is not p: continue
            s.append((e.text or '') if e.tag == qn('w:t') else ('\t' if e.tag == qn('w:tab') else '\n'))
        out.append(nfc(''.join(s)))
    return out

TOK = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.U)

def site_word(w):
    """What the site rules make of one Word word (UK table, maths, judgemental, Fröbel), with the rule's row."""
    v, rows = w, []
    for rx, rep in UK_RE:
        v2 = rx.sub(lambda m: m.expand(rep), v)
        if v2 != v: v = v2; rows.append('A023/A108')
    if re.fullmatch(r'[Mm]ath', v): v = v + 's'; rows.append('A111')
    v2 = re.sub(r'(?i)^(judg)(mental(ly)?)$', r'\1e\2', v)
    if v2 != v: v = v2; rows.append('A107')
    v2 = v.replace('Froëbel', 'Fröbel').replace('froëbel', 'fröbel')
    if v2 != v: v = v2; rows.append('D139')
    return v, '+'.join(dict.fromkeys(rows))

# ---------------------------------------------------------------- main
def main():
    r = asyncio.run(read_page())
    blocks = build_blocks(r['nodes'])
    faults, doubts = [], []
    F = lambda row, B, a, b, what: faults.append('FAULT %s %s in %s: %s' % (row, what, where(B), ctx(B, a, b)))

    for p in r['pseudo']:   # A005 in CSS content
        faults.append('FAULT A005 long dash in CSS %s content of %s (%s): %s' % (p['ps'], p['el'], p['reg'], p['c']))

    word_rules = [('A062', LEAD_RE, '"lead guide" not written "Lead Guide"'), ('A107', JUDG_RE, '"judgmental" (the site spells "judgemental")'),
                  ('A111', MATH_RE, '"math" (the site writes "maths")'), ('D139', FROEBEL_RE, '"Froëbel" (the site spells "Fröbel")')]
    n_words = 0
    for B in blocks:
        s = B.text
        for i, ch in enumerate(s):
            if ch in LONG_DASHES: F('A005', B, i, i + 1, 'long dash (%s, U+%04X)' % (LONG_DASHES[ch], ord(ch)))
        for m in SLASH_RE.finditer(s):
            a = m.start(); b = m.end()
            F('A006', B, a, b, 'space round "/"')
        hits = []
        for row, rx, what in word_rules:
            for m in rx.finditer(s):
                if row == 'A062' and LEAD_OK.fullmatch(m.group(0)): continue
                hits.append((row, m.start(), m.end(), what))
        for rx, rep in UK_RE:
            for m in rx.finditer(s):
                if m.expand(rep) == m.group(0): continue
                wa = m.start(); wb = m.end()
                while wa > 0 and s[wa - 1].isalpha(): wa -= 1
                while wb < len(s) and s[wb].isalpha(): wb += 1
                word = s[wa:wb]
                if ALLOWED.match(word): continue   # A112 / A113
                hits.append(('A023/A108', m.start(), m.end(), 'US spelling "%s" (UK: "%s")' % (word, word[:m.start() - wa] + m.expand(rep) + word[m.end() - wa:])))
        seen = set()
        for row, a, b, what in sorted(hits, key=lambda x: x[1]):
            if (row, a) in seen: continue
            seen.add((row, a))
            why = None
            if any(B.qel[a:b]): why = 'inside blockquote/q/cite'
            elif any(B.qspan[a:b]): why = 'between quotation marks'
            else:
                k = kept_by_name(B, a, b)
                if k: why = 'organisation name or title the build keeps ("%s")' % k
            if why:
                doubts.append('EXEMPT (A109, %s) %s %s in %s: %s' % (why, row, what, where(B), ctx(B, a, b)))
                continue
            note = '  (italic: if this is a published title, name it in the page settings KEEP_SPELLING)' if any(B.ital[a:b]) else ''
            F(row, B, a, b, what + note)
        n_words += len(TOK.findall(s))

    # ---- Word against the page: corrections (word in Word -> word on page)
    paras = word_paragraphs(WORD)
    wtext = '\n'.join(paras)
    W = TOK.findall(wtext)
    own = [B for B in blocks if B.reg in ('hero', 'contents', 'main')]
    P, Pq = [], []
    for B in own:
        for m in TOK.finditer(B.text):
            P.append(m.group(0)); Pq.append(any(B.qel[m.start():m.end()]) or any(B.qspan[m.start():m.end()]))
    sm = difflib.SequenceMatcher(None, W, P, autojunk=False)
    corr = collections.Counter(); unexplained = 0; quoted_changes = []
    edit_pairs = {}
    for o_, n_ in TEXT_EDITS:
        ow, nw = TOK.findall(o_), TOK.findall(n_)
        if len(ow) == len(nw):
            for x, y in zip(ow, nw):
                if x != y: edit_pairs[(x, y)] = 'page setting TEXT_EDITS'
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'replace': continue
        ws, ps_ = W[i1:i2], list(range(j1, j2))
        pairs = []
        if len(ws) == len(ps_): pairs = list(zip(ws, ps_))
        else:
            left = list(ps_)
            for w in ws:
                exp, _ = site_word(w)
                for j in left:
                    if P[j] == exp or (w, P[j]) in edit_pairs: pairs.append((w, j)); left.remove(j); break
        for w, j in pairs:
            p = P[j]; exp, rows = site_word(w)
            if exp == p and exp != w: rule = rows
            elif (w, p) in edit_pairs: rule = edit_pairs[(w, p)]
            elif w.lower() == p.lower() and w.lower() in ('lead', 'guide'): rule = 'A062'
            else: unexplained += 1; continue
            corr[(w, p, rule)] += 1
            if Pq[j] and rule not in ('A062', 'page setting TEXT_EDITS'): quoted_changes.append((w, p, rule, j))
    # Lead Guide written another way in Word (phrase level)
    for m in LEAD_RE.finditer(wtext):
        if not LEAD_OK.fullmatch(m.group(0)): corr[(m.group(0).replace('\n', ' '), 'Lead Guide' + m.group(1), 'A062 (phrase)')] += 1
    nd_w = sum(wtext.count(c) for c in LONG_DASHES); ns_w = len(SLASH_RE.findall(wtext))
    for w, p, rule, j in quoted_changes:
        faults.append('FAULT A109 a word inside a quotation changed from Word: "%s" -> "%s" (%s) near: %s' % (w, p, rule, ' '.join(P[max(0, j - 6):j + 7])))

    with open(os.path.join(OUT, 'corrections.txt'), 'w', encoding='utf-8') as f:
        f.write('# text_rules.py: corrections the page makes against the Word file (word in Word -> word on page<TAB>rule<TAB>count)\n')
        f.write('# Word: %s\n# page: %s\n' % (os.path.abspath(WORD), os.path.abspath(FOLDER)))
        for (w, p, rule), c in sorted(corr.items(), key=lambda x: (x[0][2], x[0][0].lower())):
            f.write('%s -> %s\t%s\t%d\n' % (w, p, rule, c))
        f.write('– -> -\tA005\t%d\n' % wtext.count('–')); f.write('— -> -\tA005\t%d\n' % wtext.count('—'))
        f.write('" / " -> "/"\tA006\t%d\n' % ns_w)
        f.write('# word pairs that differ and are not a site rule (left to the word check): %d\n' % unexplained)
        f.write('END\n')

    # ---- doubts: possible typos (en_US dictionary, UK forms allowed)
    D = load_hunspell()
    wset = set(t.lower() for t in W)
    unk = collections.OrderedDict()
    for B in blocks:
        for m in TOK.finditer(B.text):
            t = m.group(0)
            if any(c.isdigit() for c in t) or len(t) < 2: continue
            if t.isupper() and len(t) <= 6: continue   # initials and short capitals (AMI, PDF)
            parts = [x for x in re.split(r"['’]s$", t)[0:1]]
            w = parts[0]
            if known(w, D): continue
            key = w
            if key not in unk: unk[key] = [0, B.reg, ctx(B, m.start(), m.end(), 30), key.lower() in wset]
            unk[key][0] += 1
    with open(os.path.join(OUT, 'doubts.txt'), 'w', encoding='utf-8') as f:
        f.write('# text_rules.py doubts for the owner (not faults). Page: %s\n' % os.path.abspath(FOLDER))
        f.write('# 1. Word-rule matches left alone under A109 (quotations, organisation names, published titles): check each is right.\n')
        for d in doubts: f.write(d + '\n')
        f.write('# 2. Possible typos (A091, A102, E017): words not in the en_US hunspell dictionary after allowing UK forms. There is no en_GB\n')
        f.write('#    dictionary here, so each is a question, not a fault. Columns: word, times on page, where first, in Word too, context.\n')
        low = [(k, v) for k, v in unk.items() if not k[0].isupper()]
        cap = [(k, v) for k, v in unk.items() if k[0].isupper()]
        f.write('## lower-case words (%d)\n' % len(low))
        for k, v in low: f.write('%s\t%d\t%s\t%s\t%s\n' % (k, v[0], v[1], 'in Word' if v[3] else 'NOT in Word', v[2]))
        f.write('## capitalised words - mostly names (%d)\n' % len(cap))
        for k, v in cap: f.write('%s\t%d\t%s\t%s\t%s\n' % (k, v[0], v[1], 'in Word' if v[3] else 'NOT in Word', v[2]))
        f.write('END\n')

    lines = list(faults)
    regs = collections.Counter(B.reg for B in blocks)
    lines.append('read: %d blocks (%s), %d words; Word: %d paragraphs, %d words' % (len(blocks), ', '.join('%s %d' % kv for kv in sorted(regs.items())), n_words, len(paras), len(W)))
    lines.append('US spelling patterns from tools/build_page.py UK: %d; names kept (KEEP%s): %d' % (len(UK), ' + KEEP_SPELLING' if SETTINGS else '', len(KEEP)))
    lines.append('exempt matches (A109) listed in doubts: %d; possible typos listed in doubts: %d' % (len(doubts), len(unk)))
    lines.append('corrections against Word: %d kinds, %d places -> %s' % (len(corr), sum(corr.values()), os.path.join(OUT, 'corrections.txt')))
    lines.append('doubts -> %s' % os.path.join(OUT, 'doubts.txt'))
    lines.append('TEXT PASS' if not faults else 'TEXT FAULT (%d)' % len(faults))
    lines.append('END')
    with open(os.path.join(OUT, 'text-result.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(lines) + '\n')
    for l in lines: print(l)
    sys.exit(0 if not faults else 1)

main()
