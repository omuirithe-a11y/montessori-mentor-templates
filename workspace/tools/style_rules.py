#!/usr/bin/env python3
"""style_rules.py <page folder with index.html> <template html> <out file>   (5 Nov 2026; checks plan item 1,
/home/claude/eng35/checks-plan/PLAN.md - rows A077, A119-A127, D136, D122, D128, D194, E015, E039, E041, E043, E047,
E051, E036, D066, E054; figures from /home/claude/mm/tools/REQUIRED-CHECKS.json, each cited below with its row id)

What it does, at each of the plan's widths, with one Chromium (Playwright) page at a time:
  1. FIGURES: reads computed font-size, line-height, text-align, colour of each kind of text (hero title, contents
     label and entries, headings, paragraphs, lists, quotations, captions, band quote, footer, name lines) and
     compares them with the owner's figures (rows A119-A127, D136, D204/E036, D122, D128, D194, E015).
  2. TEMPLATE (A077, E043, E047, E051): builds a reference copy of the page whose every <style>/<script> block is the
     template's own (a page block the template does not have - the page settings <style id="mm-page"> or anything
     added - is left out; a block whose code differs from the template's is replaced by the template's). Every
     computed difference between the page and the reference (font, size, line height, alignment, indents, letter and
     word spacing, colours, backgrounds, borders) is a FAULT unless a rule of the page settings block (mm-page) that
     matches the element sets that property and names its source in a comment.
  3. LINES (E041, A052, E039): every beige line the template draws (rules of the template's or page's CSS that use
     #D9C9AB), visible or not, colour, height, and count against the reference; every visible thin line or border in
     the page body must be #D9C9AB; no border or line round a quotation; the beige lines the build placed from Word
     (the build report next to the folder: <folder>/../report.json) must stand where the report says, and the number
     of p.mm-gl must equal the report's count.
  4. MARGINS SET TWICE (D066, E054): an init script records every write to an element's margins (style.margin*,
     setProperty/removeProperty, cssText, style attribute) with the <script> block that made it; two different
     script blocks writing the same side of one element is a FAULT.
Prints one line per fault (FAULT <rule id> <width> <element> measured vs expected), everything, no truncation, then
STYLE PASS or STYLE FAULT (n), then END. Writes the same lines to <out file>. Exit 0 only on STYLE PASS."""
import sys, os, re, json, asyncio, http.server, threading, socket, bisect
from playwright.async_api import async_playwright

if len(sys.argv) != 4:
    print(__doc__); print('END'); sys.exit(2)
FOLDER, TEMPLATE, OUT = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
PAGE = os.path.join(FOLDER, 'index.html')

# ---------------------------------------------------------------- figures, each from a row's quote ----------------
# Widths: plan item 1 (/home/claude/eng35/checks-plan/PLAN.md): "Widths 320,390,640,641,768,830,831,1024,1280,1440,1920"
WIDTHS = [320, 390, 640, 641, 768, 830, 831, 1024, 1280, 1440, 1920]
# E015: "justified on computers (641px and wider), left-aligned on phones (640px and narrower)"
COMPUTER_FROM = 641          # E015, A119-A127 ("on computers (641px and wider)"), D136 ("computers 641px and wider")
PHONE_TO = 640               # E015, D128 ("on phones (640px and narrower) text is not justified")
# A119-A127: "confirmed page-text font sizes on computers (641px and wider): hero title 40, contents label 20,
#   contents entries 18, headings 18, paragraphs and lists 18, quotations 18, captions 16, band quote 18, footer 15"
# D136: "computers 641px and wider: contents label 20, contents entries 18, headings 18, quotations 18, band quote 18"
SIZE_COMPUTER = {
    'hero': (40, 'A119'), 'tocl': (20, 'A120/D136'), 'toce': (18, 'A121/D136'), 'heading': (18, 'A122/D136'),
    'p': (18, 'A123'), 'li': (18, 'A123'), 'quote': (18, 'A124/D136'), 'caption': (16, 'A125'),
    'band': (18, 'A126/D136'), 'footer': (15, 'A127'),
}
# D136: "Phones (21 Oct rule): the phone step the templates use - contents label 19, contents entries 17, headings 17"
SIZE_PHONE = {'tocl': (19, 'D136'), 'toce': (17, 'D136'), 'heading': (17, 'D136')}
# D136: "quotations and band at 641-830 take the 40px the page uses for 18px quotations"
QUOTE_BAND_LH = (40, 641, 830, 'D136')
# D204 (the full form of E036, "DECIDED 20 Oct 15:46 - Type 1, name lines"): "blue #0432FF, 20px, regular"
NAME_LINE = {'size': 20, 'color': 'rgb(4, 50, 255)', 'weight': '400', 'row': 'D204/E036'}
# A052: "all dividers (the beige lines) on every page, past, present and future, are #D9C9AB"
BEIGE_HEX = 'D9C9AB'; BEIGE = 'rgb(217, 201, 171)'
# D122: "Quotations in their own block, captions, centred lines and headings are left exactly as they were" -
#   a centred line (class centred, the build's mark for a Word centred line) stays centred at every width
# D122 / D194 ("numbered lists too") / E015: body paragraphs and list items justified from 641
# E039: "no lines round quotations"
# Page settings source words: the gate's settings_sources() rule (tools/settings_check.py)
SOURCE_WORDS = r'\b(user|your|you|Word|PDF|template|live|site rule)\b'

lines_out = []
def out(s):
    print(s, flush=True); lines_out.append(s)

def finish(faults, code=None):
    with open(OUT, 'w') as f:
        f.write('\n'.join(lines_out + ['STYLE PASS' if not faults else 'STYLE FAULT (%d)' % len(faults), 'END']) + '\n')
    print('STYLE PASS' if not faults else 'STYLE FAULT (%d)' % len(faults)); print('END', flush=True)
    sys.exit(0 if not faults else 1)

page_html = open(PAGE, encoding='utf-8').read()
tpl_html = open(TEMPLATE, encoding='utf-8').read()

# ---------------------------------------------------------------- reference copy: the page with the template's code -
BLOCK = re.compile(r'<(style|script)\b([^>]*)>(.*?)</\1\s*>', re.S | re.I)
def blocks(s):
    res, unnamed = [], {}
    for m in BLOCK.finditer(s):
        tag = m.group(1).lower(); attrs = m.group(2)
        idm = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs)
        if idm: key = (tag, idm.group(1))
        else:
            n = unnamed.get(tag, 0); unnamed[tag] = n + 1; key = (tag, '#%d' % n)
        res.append({'key': key, 'm': m, 'tag': tag, 'attrs': attrs, 'body': m.group(3)})
    return res

pb, tb = blocks(page_html), blocks(tpl_html)
tmap = {b['key']: b for b in tb}
pkeys = {b['key'] for b in pb}
code_notes, code_faults = [], []
parts, pos = [], 0
for b in pb:
    parts.append(page_html[pos:b['m'].start()]); pos = b['m'].end()
    t = tmap.get(b['key'])
    name = '<%s %s>' % (b['key'][0], b['key'][1])
    if t is None:
        code_notes.append('INFO code: page block %s is not in the template - left out of the reference%s' %
                          (name, ' (the page settings)' if b['key'] == ('style', 'mm-page') else ''))
        continue
    if t['body'] != b['body']:
        code_notes.append('INFO code: page block %s differs from the template\'s (%d vs %d characters) - the reference uses the template\'s' %
                          (name, len(b['body']), len(t['body'])))
    parts.append('<%s%s>%s</%s>' % (t['tag'], t['attrs'], t['body'], t['tag']))
parts.append(page_html[pos:])
ref_html = ''.join(parts)
for t in tb:
    if t['key'] not in pkeys:
        code_faults.append('FAULT E051 all template block <%s %s> missing from the page vs present in the template' % t['key'])
        blk = '<%s%s>%s</%s>' % (t['tag'], t['attrs'], t['body'], t['tag'])
        ref_html = ref_html.replace('</head>', blk + '</head>', 1) if t['tag'] == 'style' else ref_html.replace('</body>', blk + '</body>', 1)
REF_SAME = ref_html == page_html

# ---------------------------------------------------------------- beige line rules from the CSS ---------------------
def css_rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S); res = []
    def parse(s, media):
        i = 0
        while i < len(s):
            j = s.find('{', i)
            if j < 0: break
            sel = s[i:j].strip(); d, k = 1, j + 1
            while d and k < len(s):
                d += {'{': 1, '}': -1}.get(s[k], 0); k += 1
            body = s[j + 1:k - 1]
            if sel.startswith('@media') or sel.startswith('@supports') or sel.startswith('@layer'): parse(body, media + [sel])
            elif not sel.startswith('@'): res.append((media, sel, body))
            i = k
    parse(css, []); return res

def beige_specs(html):
    css = ''.join(b['body'] for b in blocks(html) if b['tag'] == 'style')
    specs = []
    for media, sel, body in css_rules(css):
        if not re.search(BEIGE_HEX + r'|217,\s*201,\s*171', body, re.I): continue
        kinds = []
        for side in ('top', 'right', 'bottom', 'left'):
            if re.search(r'border-%s\s*:[^;]*(%s|217,\s*201)' % (side, BEIGE_HEX), body, re.I): kinds.append('border-' + side)
        if re.search(r'(^|;)\s*border\s*:[^;]*(%s|217,\s*201)' % BEIGE_HEX, body, re.I): kinds += ['border-top', 'border-right', 'border-bottom', 'border-left']
        if re.search(r'gradient\([^)]*%s' % BEIGE_HEX, body, re.I): kinds.append('grad')
        elif re.search(r'background(-color)?\s*:[^;]*(%s|217,\s*201)' % BEIGE_HEX, body, re.I): kinds.append('bg')
        for one in sel.split(','):
            one = one.strip(); pseudo = ''
            m = re.search(r'::?(before|after)\s*$', one)
            if m: pseudo = '::' + m.group(1); one = one[:m.start()].strip()
            for k in kinds:
                if [one, pseudo, k] not in specs: specs.append([one, pseudo, k])
    return specs
SPECS = beige_specs(tpl_html)
for s in beige_specs(page_html):
    if s not in SPECS: SPECS.append(s)

# ---------------------------------------------------------------- build report: beige lines placed from Word --------
REPORT = os.path.join(os.path.dirname(FOLDER), 'report.json')
rep_before, rep_count = [], None
if os.path.exists(REPORT):
    try:
        for e in json.load(open(REPORT))['report']:
            if e and e[0] == 'beige line':
                if str(e[1]).startswith('from a line picture in Word, before'): rep_before.append(str(e[2]))
                elif 'p.mm-gl' in str(e[1]):
                    try: rep_count = int(e[2])
                    except ValueError: pass
    except Exception as ex:
        code_faults.append('FAULT E041 all build report %s unreadable (%s) vs a readable report' % (REPORT, ex))
else:
    code_faults.append('FAULT E041 all build report %s not found vs the build\'s record of the beige lines placed from Word (the count cannot be checked)' % REPORT)

# ---------------------------------------------------------------- where each script block sits (for D066) ------------
def script_map(html):
    starts = [0] + [m.end() for m in re.finditer('\n', html)]
    spans = []
    for i, b in enumerate(blocks(html)):
        if b['tag'] != 'script': continue
        ln = html.count('\n', 0, b['m'].start()) + 1
        label = ('script#%s' % b['key'][1]) if not b['key'][1].startswith('#') else 'script (no id, %s, line %d)' % (b['key'][1], ln)
        spans.append((b['m'].start(2) + len(b['attrs']) + 1, b['m'].end(3), label))
    def which(line, col):
        if line < 1 or line > len(starts): return 'outside the page code (line %d:%d)' % (line, col)
        off = starts[line - 1] + col - 1
        for a, z, lab in spans:
            if a <= off <= z: return lab
        return 'not in a <script> block (line %d:%d)' % (line, col)
    return which

# ---------------------------------------------------------------- browser code ---------------------------------------
INIT = r"""(() => {
  if (window.__srInit) return; window.__srInit = 1;
  const W = window.__srWrites = []; const els = window.__srEls = []; const ids = new WeakMap(), prox = new WeakMap();
  const idOf = e => { let i = ids.get(e); if (i === undefined) { i = els.length; els.push(e); ids.set(e, i); } return i; };
  const where = () => { const lim = Error.stackTraceLimit; Error.stackTraceLimit = 12; const st = (new Error()).stack.split('\n'); Error.stackTraceLimit = lim;
    for (const l of st) { if (l.includes('__sr_init')) continue; const m = l.match(/(https?:\/\/[^\s()]+?):(\d+):(\d+)/); if (m) return [m[1], +m[2], +m[3]]; }
    return ['?', 0, 0]; };
  const SIDES = {'margin-top': ['top'], 'margin-right': ['right'], 'margin-bottom': ['bottom'], 'margin-left': ['left'],
    'margin': ['top', 'right', 'bottom', 'left'], 'margin-block': ['top', 'bottom'], 'margin-block-start': ['top'], 'margin-block-end': ['bottom'],
    'margin-inline': ['left', 'right'], 'margin-inline-start': ['left'], 'margin-inline-end': ['right']};
  const dash = p => String(p).replace(/[A-Z]/g, c => '-' + c.toLowerCase());
  const rec = (el, prop, val) => { const s = SIDES[dash(prop)]; if (!s) return; const w = where(); for (const side of s) W.push([idOf(el), side, w[0], w[1], w[2], String(val)]); };
  const recText = (el, txt) => { String(txt || '').split(';').forEach(d => { const i = d.indexOf(':'); if (i > 0) rec(el, d.slice(0, i).trim(), d.slice(i + 1).trim()); }); };
  const sd = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'style');
  Object.defineProperty(HTMLElement.prototype, 'style', { configurable: true, enumerable: sd.enumerable,
    get: function () { const real = sd.get.call(this); let p = prox.get(real); if (p) return p; const el = this;
      p = new Proxy(real, {
        get(t, k) { const v = Reflect.get(t, k, t);
          if (k === 'setProperty') return function (n, v2, pr) { rec(el, n, v2); return t.setProperty(n, v2, pr); };
          if (k === 'removeProperty') return function (n) { rec(el, n, ''); return t.removeProperty(n); };
          return typeof v === 'function' ? v.bind(t) : v; },
        set(t, k, v) { if (k === 'cssText') recText(el, v); else rec(el, k, v); t[k] = v; return true; } });
      prox.set(real, p); return p; },
    set: function (v) { recText(this, v); sd.set.call(this, v); } });
  const sa = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function (n, v) { if (String(n).toLowerCase() === 'style' && this instanceof HTMLElement) recText(this, v); return sa.call(this, n, v); };
})();
//# sourceURL=__sr_init.js"""

MEASURE = r"""(args) => {
  const specs = args.specs, BEIGE = args.beige, before = args.before;
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const desc = e => { if (!e || !e.tagName) return String(e); const c = (e.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean);
    const t = norm(e.textContent).slice(0, 40); return e.tagName.toLowerCase() + (c.length ? '.' + c.join('.') : '') + (t ? ' "' + t + '"' : ''); };
  const vis = e => e.checkVisibility({checkOpacity: true, checkVisibilityCSS: true});
  const alpha = c => { const m = /rgba\([^)]*,\s*([\d.]+)\)/.exec(c); return m ? +m[1] : (c === 'transparent' ? 0 : 1); };
  const ownText = e => [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim());
  // ---- text elements by kind
  const seen = new Set(), recs = [];
  const PROPS = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'textAlign', 'textIndent', 'letterSpacing', 'wordSpacing',
    'textTransform', 'color', 'backgroundColor', 'backgroundImage', 'paddingLeft', 'paddingRight', 'marginLeft', 'marginRight',
    'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderRightWidth', 'borderRightStyle', 'borderRightColor',
    'borderBottomWidth', 'borderBottomStyle', 'borderBottomColor', 'borderLeftWidth', 'borderLeftStyle', 'borderLeftColor'];
  const KINDS = [
    ['hero', '.hero h1', e => true],
    ['tocl', '.toc-wrap .toc-label', e => true],
    ['toce', '.toc-wrap li', e => true],
    ['name', 'main p.mm-name', e => true],
    ['heading', 'main h1, main h2, main h3, main h4, main h5, main h6', e => true],
    ['quote', 'main blockquote, main blockquote p', e => true],
    ['caption', 'main figcaption, main .mm-cap', e => norm(e.textContent)],
    ['band', '.mc-band p', e => true],
    ['footer', 'footer', e => true],
    ['p', 'main p', e => !e.classList.contains('mm-gl') && norm(e.textContent)],
    ['li', 'main li', e => !e.closest('.toc-wrap')],
  ];
  // page settings (mm-page): which properties its rules set on an element, and whether each rule names a source
  const settings = document.getElementById('mm-page'); const setRules = [];
  if (settings && settings.sheet) {
    const raw = settings.textContent; const SRC = new RegExp(args.srcWords, 'i');
    const walk = rules => { for (const r of rules) {
      if (r.cssRules && r.media) { if (matchMedia(r.media.mediaText).matches) walk(r.cssRules); continue; }
      if (!r.selectorText) continue;
      const i = raw.indexOf(r.selectorText.split(',')[0].trim()); let src = false;
      if (i >= 0) { const prevEnd = raw.lastIndexOf('}', i); const j = raw.indexOf('}', i); const around = raw.slice(prevEnd + 1, j);
        const cm = around.match(/\/\*[\s\S]*?\*\//g) || []; src = cm.some(c => SRC.test(c)); }
      const props = []; for (let k = 0; k < r.style.length; k++) props.push(r.style[k].replace(/-([a-z])/g, (a, b) => b.toUpperCase()));
      setRules.push({sel: r.selectorText, props, src}); } };
    walk(settings.sheet.cssRules);
  }
  const occ = {};
  const SKIP = new Set(['BR', 'IMG', 'SVG', 'PATH', 'PICTURE', 'SOURCE', 'VIDEO', 'SCRIPT', 'STYLE', 'BUTTON']);
  for (const [kind, sel, keep] of KINDS) {
    const list = []; for (const r of document.querySelectorAll(sel)) { list.push(r); r.querySelectorAll('*').forEach(x => list.push(x)); }   // the element and the words inside it
    for (const e of list) {
      if (seen.has(e) || SKIP.has(e.tagName.toUpperCase()) || e.closest('svg') || !keep(e)) continue; seen.add(e);
      const c = getComputedStyle(e), props = {}; for (const p of PROPS) props[p] = c[p];
      const t = norm(e.textContent).slice(0, 60); const k0 = kind + '|' + e.tagName + '|' + t; occ[k0] = (occ[k0] || 0) + 1;
      const allowed = {}, nosrc = [];
      for (const r of setRules) { let m = false; try { m = e.matches(r.sel); } catch (x) {} if (!m) continue;
        for (const p of r.props) { if (r.src) allowed[p] = r.sel; else nosrc.push(r.sel + ' ' + p); } }
      recs.push({kind, key: k0 + '#' + occ[k0], desc: desc(e), props, cls: e.getAttribute('class') || '', allowed, nosrc,
                 own: ownText(e), block: ['block', 'list-item', 'flow-root', 'table-cell'].includes(c.display) && !!t,
                 shown: vis(e), inQuote: !!e.closest('blockquote'), inFig: !!e.closest('figcaption, .mm-cap, .mm-twocap'), inCols: !!e.closest('.mm-wcols2, .mm-cols3')});   // 6 Nov 2026 (owner 11:59 and 12:15 agreements): lines in Word's two- and three-column lists are left-aligned at every width   // 5 Nov 2026 (checkfix): .mm-cap and .mm-twocap are captions too (template: ".mm-twocap ... centres its first caption over ... and its second ..."; D122 leaves captions as they were)
    }
  }
  // ---- beige lines the CSS draws
  const lineEls = new Map(), lines = [];
  specs.forEach(([sel, pseudo, kind], si) => {
    let list = []; try { list = [...document.querySelectorAll(sel)]; } catch (x) { return; }
    list.forEach((e, idx) => {
      const id = kind + pseudo; let m = lineEls.get(e); if (!m) { m = {}; lineEls.set(e, m); }
      if (m[id]) return;
      const c = getComputedStyle(e), r = e.getBoundingClientRect(); let shown = vis(e) && r.width > 0, h = 0, color = '';
      if (pseudo) { const pc = getComputedStyle(e, pseudo); color = pc.backgroundColor; h = parseFloat(pc.height) || 0;
        shown = shown && pc.content !== 'none' && pc.content !== 'normal' && pc.display !== 'none' && pc.visibility === 'visible' && h > 0 && alpha(color) > 0; }
      else if (kind === 'bg') { color = c.backgroundColor; h = parseFloat(c.height) || 0; shown = shown && r.height > 0 && h > 0 && alpha(color) > 0; }
      else if (kind === 'grad') { const g = /rgba?\([^)]*\)/.exec(c.backgroundImage); color = g ? g[0] : ''; h = parseFloat((/(\d+(\.\d+)?)px\s*$/.exec(c.backgroundSize) || [0, 0])[1]); shown = shown && /gradient/.test(c.backgroundImage) && r.height > 0; }
      else { const side = kind.split('-')[1], S = side[0].toUpperCase() + side.slice(1);
        color = c['border' + S + 'Color']; h = parseFloat(c['border' + S + 'Width']) || 0;
        shown = shown && h > 0 && !['none', 'hidden'].includes(c['border' + S + 'Style']) && alpha(color) > 0; }
      const rec = {key: sel + pseudo + '|' + kind + '|' + idx, desc: desc(e) + pseudo + ' (' + kind + ')', shown, h, color, isGl: e.matches('p.mm-gl')};
      m[id] = rec; lines.push(rec);
    });
  });
  // ---- every other visible thin line or border in the page body (A052: all dividers beige; E039: none round quotations)
  const others = [];
  const scope = [...document.querySelectorAll('main, .hero, .toc-wrap, .toc-rule-wrap, .mc-band, footer')];
  const all = new Set(); scope.forEach(s => { all.add(s); s.querySelectorAll('*').forEach(x => all.add(x)); });
  for (const e of all) {
    if (!vis(e)) continue; const c = getComputedStyle(e), r = e.getBoundingClientRect();
    for (const S of ['Top', 'Right', 'Bottom', 'Left']) { const w = parseFloat(c['border' + S + 'Width']) || 0, col = c['border' + S + 'Color'];
      if (w > 0 && !['none', 'hidden'].includes(c['border' + S + 'Style']) && alpha(col) > 0) {
        // 6 Nov 2026 (owner 00:19: "a link Word shows in a box is shown in a box of Word's colour"): such a box is not a divider;
        // its border must be the Word colour its class names (mm-box-RRGGBB), else it is reported as a box fault
        const bx = e.matches('a.mm-box') ? [...e.classList].map(k => (k.match(/^mm-box-([0-9A-Fa-f]{6})$/) || [])[1]).find(Boolean) : null;
        if (e.matches('a.mm-box')) { const want = bx ? 'rgb(' + [0, 2, 4].map(i => parseInt(bx.substr(i, 2), 16)).join(', ') + ')' : null;
          if (col !== want) others.push({desc: desc(e), what: 'box border-' + S.toLowerCase() + ' (Word colour ' + (bx || 'none named') + ')', w, color: col, quote: false, box: true});
          continue; }
        others.push({desc: desc(e), what: 'border-' + S.toLowerCase(), w, color: col, quote: !!e.closest('blockquote')}); } }
    if (r.width >= 20 && r.height > 0 && r.height <= 6 && !norm(e.textContent) && !e.querySelector('img,svg,video') && alpha(c.backgroundColor) > 0)
      others.push({desc: desc(e), what: 'thin line', w: r.height, color: c.backgroundColor, quote: !!e.closest('blockquote')});
    for (const ps of ['::before', '::after']) { const pc = getComputedStyle(e, ps);
      if (pc.content !== 'none' && pc.content !== 'normal' && pc.display !== 'none' && alpha(pc.backgroundColor) > 0 && (parseFloat(pc.height) || 0) > 0 && (parseFloat(pc.height) || 0) <= 6)
        others.push({desc: desc(e) + ps, what: 'thin line', w: parseFloat(pc.height), color: pc.backgroundColor, quote: !!e.closest('blockquote')});
      for (const S of ['Top', 'Right', 'Bottom', 'Left']) { const w = parseFloat(pc['border' + S + 'Width']) || 0, col = pc['border' + S + 'Color'];
        if (pc.content !== 'none' && pc.content !== 'normal' && w > 0 && !['none', 'hidden'].includes(pc['border' + S + 'Style']) && alpha(col) > 0)
          others.push({desc: desc(e) + ps, what: 'border-' + S.toLowerCase(), w, color: col, quote: !!e.closest('blockquote')}); } }
  }
  // ---- the beige lines the build placed from Word: a visible line straight before each listed paragraph
  const main = document.querySelector('main'); const placed = [];
  const isShownLine = e => { const m = lineEls.get(e); return m && Object.values(m).some(x => x.shown); };
  // 5 Nov 2026 (checkfix, E041 misreadings on The English Curriculum b22): (1) the report lists the lines in the Word/PDF
  // order, so each paragraph is looked for after the one found for the line before it (was: from the top of main, which
  // found an earlier paragraph with the same words - a blue line "Keys to Literacy" under "Sound Game" - instead of the
  // heading the line stands before); the whole of main is searched again only if nothing is found after. (2) The words are
  // compared as the builder writes them: short dashes and no spaces round a slash (tools/build_page.py site_rules,
  // "Site text rules: short dashes only; no spaces round a slash") - Word's "Art / Drawing / Colouring" is the page's
  // "Art/Drawing/Colouring".
  const site = s => norm(s).replace(/[\u2013\u2014]/g, '-').replace(/\s+\/\s+/g, '/');
  const cand = main ? [...main.querySelectorAll('p, li, h2, h3, h4, blockquote')] : []; let lastIdx = -1;
  for (const t of before) {
    const want = site(t).slice(0, 60); let el = null;
    let ix = cand.findIndex((e, i) => i > lastIdx && site(e.textContent).startsWith(want));
    if (ix < 0) ix = cand.findIndex(e => site(e.textContent).startsWith(want));
    if (ix >= 0) { el = cand[ix]; lastIdx = ix; }
    if (!el) { placed.push({text: t, ok: false, found: 'paragraph not found'}); continue; }
    let n = el, res = null;
    while (n && n !== main && !res) {
      if (n.previousElementSibling) { n = n.previousElementSibling;
        if (n.classList && n.classList.contains('mm-float')) continue;   // 6 Nov 2026 (owner 11:59 agreement): an image placed beside the paragraph (the template's p.mm-gl + .mm-float) is not between the line and its paragraph
        if (isShownLine(n)) res = {ok: true, found: desc(n)};
        else if (norm(n.textContent) || n.querySelector('img')) res = {ok: false, found: desc(n)}; }
      else n = n.parentElement;
    }
    placed.push(Object.assign({text: t}, res || {ok: false, found: 'nothing before it'}));
  }
  // ---- margin writes (D066)
  const groups = {};
  for (const [id, side, url, line, col, val] of (window.__srWrites || [])) {
    const k = id + '|' + side; (groups[k] = groups[k] || {id, side, writes: []}).writes.push([url, line, col, val]); }
  const margins = Object.values(groups).map(g => ({desc: desc(window.__srEls[g.id]), side: g.side, writes: g.writes}));
  return {recs, lines, others, placed, glCount: document.querySelectorAll('main p.mm-gl').length, margins, nosettings: !settings};
}"""

def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p

REF_BYTES = ref_html.encode('utf-8')
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=FOLDER, **k)
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.split('?')[0] == '/__sr_reference.html':
            self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(REF_BYTES))); self.end_headers(); self.wfile.write(REF_BYTES); return
        super().do_GET()

async def render(browser, url, w):
    pg = await browser.new_page(viewport={'width': w, 'height': 900})
    await pg.add_init_script(INIT)
    await pg.goto(url, wait_until='domcontentloaded', timeout=120000)
    await pg.wait_for_timeout(3500)
    r = await pg.evaluate(MEASURE, {'specs': SPECS, 'beige': BEIGE, 'before': rep_before, 'srcWords': SOURCE_WORDS})
    await pg.close(); return r

def px(v):
    try: return float(str(v).replace('px', ''))
    except ValueError: return None

async def main():
    faults = list(code_faults)
    out('style_rules.py  page %s  template %s' % (PAGE, TEMPLATE))
    out('INFO widths %s; beige line rules found in the CSS: %d; build report: %s (lines from Word: %d, p.mm-gl count: %s)' %
        (','.join(map(str, WIDTHS)), len(SPECS), REPORT if os.path.exists(REPORT) else 'none', len(rep_before), rep_count))
    for n in code_notes: out(n)
    out('INFO reference copy %s' % ('identical to the page (every block is the template\'s): the page render serves as the reference' if REF_SAME
                                     else 'differs from the page: both are rendered at each width'))
    which_page = script_map(page_html)
    port = free_port()
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d' % port
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for w in WIDTHS:
            pr = await render(browser, base + '/index.html', w)
            rr = pr if REF_SAME else await render(browser, base + '/__sr_reference.html', w)
            f0 = len(faults)
            computer, phone = w >= COMPUTER_FROM, w <= PHONE_TO
            # ---- 1. figures
            for r in pr['recs']:
                k, c, d = r['kind'], r['props'], r['desc']
                fs, lh = px(c['fontSize']), px(c['lineHeight'])
                fig = (SIZE_COMPUTER if computer else SIZE_PHONE).get(k)
                if not r['own']: fig = None   # a figure is the size of words: only elements that hold words themselves
                if fig and fs != fig[0]:
                    faults.append('FAULT %s %d %s font-size %s vs %dpx' % (fig[1], w, d, c['fontSize'], fig[0]))
                if r['own'] and k in ('quote', 'band') and QUOTE_BAND_LH[1] <= w <= QUOTE_BAND_LH[2] and lh != QUOTE_BAND_LH[0]:
                    faults.append('FAULT %s %d %s line-height %s vs %dpx' % (QUOTE_BAND_LH[3], w, d, c['lineHeight'], QUOTE_BAND_LH[0]))
                if k == 'name' and r['own']:
                    if fs != NAME_LINE['size']: faults.append('FAULT %s %d %s font-size %s vs %dpx' % (NAME_LINE['row'], w, d, c['fontSize'], NAME_LINE['size']))
                    if c['color'] != NAME_LINE['color']: faults.append('FAULT %s %d %s colour %s vs %s (#0432FF)' % (NAME_LINE['row'], w, d, c['color'], NAME_LINE['color']))
                    if c['fontWeight'] != NAME_LINE['weight']: faults.append('FAULT %s %d %s font-weight %s vs %s (regular)' % (NAME_LINE['row'], w, d, c['fontWeight'], NAME_LINE['weight']))
                cls = r['cls'].split()
                ta = c['textAlign']
                if not r['block']: pass   # alignment is a property of a block of text
                elif 'centred' in cls:
                    if ta != 'center': faults.append('FAULT D122 %d %s text-align %s vs center (a centred line stays as it was)' % (w, d, ta))
                elif phone:
                    if ta == 'justify': faults.append('FAULT D128/E015 %d %s text-align justify vs left (phones not justified)' % (w, d))
                elif k in ('p', 'li') and r.get('inCols'):   # 6 Nov 2026 (owner 11:59, 12:15): Word's column lists left-aligned at every width
                    if ta not in ('left', 'start'): faults.append('FAULT D122/E015 %d %s text-align %s vs left (a line in Word\'s column lists, owner 6 Nov 11:59/12:15)' % (w, d, ta))
                elif k in ('p', 'li') and not r['inQuote'] and not r['inFig'] and 'mm-name' not in cls:
                    if ta != 'justify': faults.append('FAULT %s %d %s text-align %s vs justify' % ('D122/D194/E015' if k == 'li' else 'D122/E015', w, d, ta))
            # ---- 2. template comparison
            if not REF_SAME:
                pm = {r['key']: r for r in pr['recs']}; rm = {r['key']: r for r in rr['recs']}
                for key in pm:
                    if key not in rm: faults.append('FAULT E051 %d %s present on the page vs not in the template render' % (w, pm[key]['desc'])); continue
                    a, b = pm[key], rm[key]
                    for prop in a['props']:
                        if a['props'][prop] == b['props'][prop]: continue
                        if prop in a['allowed']:
                            out('INFO %d %s %s %s vs template %s - set by the page settings (%s, source named)' % (w, a['desc'], prop, a['props'][prop], b['props'][prop], a['allowed'][prop]))
                            continue
                        rid = 'A077/E051/' + ('E047' if 'olor' in prop or 'background' in prop.lower() or 'border' in prop.lower() else 'E043')
                        faults.append('FAULT %s %d %s %s %s vs %s (template)' % (rid, w, a['desc'], prop, a['props'][prop], b['props'][prop]))
                for key in rm:
                    if key not in pm: faults.append('FAULT E051 %d %s missing from the page vs present in the template render' % (w, rm[key]['desc']))
            for r in pr['recs']:
                for ns in r['nosrc']: faults.append('FAULT A077 %d %s page settings rule %s names no source vs a source in a comment' % (w, r['desc'], ns))
            # ---- 3. lines
            pl = {l['key']: l for l in pr['lines']}; rl = {l['key']: l for l in rr['lines']}
            shown_p = [l for l in pr['lines'] if l['shown']]; shown_r = [l for l in rr['lines'] if l['shown']]
            for l in shown_p:
                if l['color'] != BEIGE: faults.append('FAULT A052/E041 %d %s colour %s vs %s (#D9C9AB)' % (w, l['desc'], l['color'], BEIGE))
            for key, l in rl.items():
                if not l['shown']: continue
                q = pl.get(key)
                if not q or not q['shown']: faults.append('FAULT E041 %d %s not shown on the page vs shown in the template render (height %s, %s)' % (w, l['desc'], l['h'], l['color']))
                elif q['h'] != l['h']: faults.append('FAULT E041 %d %s height %spx vs %spx (template)' % (w, q['desc'], q['h'], l['h']))
            for key, l in pl.items():
                if l['shown'] and not (rl.get(key) or {}).get('shown'): faults.append('FAULT E041 %d %s shown on the page vs not shown in the template render' % (w, l['desc']))
            if len(shown_p) != len(shown_r): faults.append('FAULT E041 %d beige lines shown: %d vs %d (template render)' % (w, len(shown_p), len(shown_r)))
            for l in pr['lines']:
                if l['shown'] and l['h'] <= 0: faults.append('FAULT E041 %d %s height %s vs more than 0' % (w, l['desc'], l['h']))
            for o in pr['others']:
                if o['quote']: faults.append('FAULT E039 %d %s %s %spx %s vs no line round quotations' % (w, o['desc'], o['what'], o['w'], o['color']))
                elif o['color'] != BEIGE: faults.append('FAULT A052/E041 %d %s %s %spx colour %s vs %s (#D9C9AB, all dividers)' % (w, o['desc'], o['what'], o['w'], o['color'], BEIGE))
            if not REF_SAME:
                key_o = lambda o: (o['desc'], o['what'], o['w'], o['color'])
                ro = [key_o(o) for o in rr['others']]
                for o in pr['others']:
                    if key_o(o) in ro: ro.remove(key_o(o))
                    else: faults.append('FAULT E041/E047 %d %s %s %spx %s on the page vs not in the template render' % (w, o['desc'], o['what'], o['w'], o['color']))
                for o in ro: faults.append('FAULT E041/E047 %d %s %s %spx %s in the template render vs not on the page' % ((w,) + o))
            for pl_ in pr['placed']:
                if not pl_['ok']: faults.append('FAULT E041 %d beige line before "%s" (build report, from Word) not found vs a shown beige line straight before it (found before it: %s)' % (w, pl_['text'][:60], pl_['found']))
            if rep_count is not None and pr['glCount'] != rep_count:
                faults.append('FAULT E041 %d p.mm-gl count %d vs %d (build report)' % (w, pr['glCount'], rep_count))
            # ---- 4. margins set by two scripts
            nwrites = 0
            for m in pr['margins']:
                by = {}
                for url, line, col, val in m['writes']:
                    nwrites += 1
                    lab = which_page(line, col) if url.rstrip('/').endswith(str(port)) or url.endswith('/index.html') else 'not the page (%s)' % url
                    by.setdefault(lab, []).append(val)
                if len(by) > 1:
                    faults.append('FAULT D066/E054 %d %s margin-%s written by %d scripts: %s vs one script' %
                                  (w, m['desc'], m['side'], len(by), '; '.join('%s (%s)' % (k, ', '.join(repr(v) for v in sorted(set(vs)))) for k, vs in by.items())))
            out('INFO %d text elements %d, beige lines shown %d (template render %d), other lines/borders %d, margin writes %d on %d element sides, faults at this width %d' %
                (w, len(pr['recs']), len(shown_p), len(shown_r), len(pr['others']), nwrites, len(pr['margins']), len(faults) - f0))
            for f in faults[f0:]: out(f)
        await browser.close()
    srv.shutdown()
    for f in code_faults: out(f)
    finish(faults)

asyncio.run(main())
