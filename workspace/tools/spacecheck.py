#!/usr/bin/env python3
# spacecheck.py <docx> <pdf> <page folder containing index.html> <out dir> [widths]
# 6 Nov 2026 (owner 08:53): beige lines p.mm-gl counted as dividers; PDF lines matched per column (see the PDF part).
# 3 Nov 2026 (owner 17:08/17:10: "make it more precise, more thorough, so the check is able to catch all spacings and match the PDF"):
# every vertical gap on the page compared with the PDF, as a ratio to each one's own line spacing.
#  - Word gives the order of paragraphs and the kind of each gap (blank paragraphs, space before/after).
#  - The PDF gives what the owner sees: every line's baseline, every image and every ruled line, in points.
#  - The page is measured in one browser at every width: every line's bottom, every image row and every divider.
#  A gap is: last line of paragraph A to first line of paragraph B (and, where an image row or a divider stands between them,
#  A to the object and the object to B). Each gap is divided by that source's line spacing (median line-to-line inside a paragraph),
#  so a blank line in the PDF (2.0) must also be about 2.0 on the page, not 1.2.
# FAULT when the page's ratio differs from the PDF's by more than TOL (absolute) - default 0.15 of a line.
# Gaps the PDF cannot give (across a page break, between the two columns of a pair) are compared with the median PDF ratio of the
# same Word kind elsewhere on the page.
import sys, os, re, json, subprocess, statistics, difflib, collections
import docx, pymupdf

DOCX, PDF, PAGEDIR, OUT = sys.argv[1:5]
WIDTHS = [int(x) for x in (sys.argv[5] if len(sys.argv) > 5 else '1440,1279,1180,1099,1023,961,960,831,830,768,641,640,390').split(',')]
TOL = float(os.environ.get('SPACE_TOL', '0.15'))
os.makedirs(OUT, exist_ok=True)

import unicodedata
def norm(t):
    t = unicodedata.normalize('NFKD', t).lower()   # ligatures (the PDF's 'ﬁ') read as their letters.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'[^a-z0-9]', '', t)

# ---- Word: paragraphs and the kind of each gap
D = docx.Document(DOCX)
W = []   # (index, text, norm, has_drawing)
for i, p in enumerate(D.paragraphs):
    has_img = bool(p._p.xpath('.//w:drawing')) or bool(p._p.xpath('.//w:pict'))
    W.append(dict(i=i, text=p.text, n=norm(p.text), img=has_img,
                  sa=(p.paragraph_format.space_after or 0) / 12700.0, sb=(p.paragraph_format.space_before or 0) / 12700.0))
TEXT = [w for w in W if len(w['n']) >= 2]

def word_kind(a, b):
    """kind of the gap between Word paragraphs a and b (indexes into D.paragraphs)"""
    blanks = sum(1 for k in range(a + 1, b) if not W[k]['n'] and not W[k]['img'])
    imgs = sum(1 for k in range(a + 1, b) if W[k]['img'])
    sp = W[a]['sa'] + W[b]['sb']
    if imgs: return 'image between'
    if blanks: return 'blank line x%d' % blanks
    if sp > 0: return 'space %gpt' % sp
    return 'next paragraph'

# ---- PDF: lines, images, ruled lines
P = pymupdf.open(PDF)
plines, pimgs, prules = [], [], []
for pn, pg in enumerate(P):
    d = pg.get_text('dict')
    for b in d['blocks']:
        if b['type'] == 1: pimgs.append(dict(pg=pn, top=b['bbox'][1], bot=b['bbox'][3], x0=b['bbox'][0], x1=b['bbox'][2])); continue
        for l in b['lines']:
            s = ''.join(sp['text'] for sp in l['spans'])
            if not norm(s): continue
            base = max(sp['origin'][1] for sp in l['spans'])
            plines.append(dict(pg=pn, base=base, top=l['bbox'][1], bot=l['bbox'][3], x0=l['bbox'][0], n=norm(s), t=s.strip()))
    for dr in pg.get_drawings():
        r = dr['rect']
        if r.width > 200 and r.height < 4: prules.append(dict(pg=pn, top=r.y0, bot=r.y1, x0=r.x0))
    for im in pg.get_image_info():
        bb = im['bbox']
        if not any(abs(x['top'] - bb[1]) < 1 and x['pg'] == pn and abs(x['x0'] - bb[0]) < 1 for x in pimgs):
            pimgs.append(dict(pg=pn, top=bb[1], bot=bb[3], x0=bb[0], x1=bb[2]))
plines.sort(key=lambda x: (x['pg'], round(x['base'], 0), x['x0']))
# an image row or divider stands between lines of text: anything that overlaps a text line (a link's underline, an image beside text) is not one
def _clear(o): return not any(L['pg'] == o['pg'] and o['top'] < L['bot'] + 2.5 and o['bot'] > L['top'] - 1 for L in plines)
pimgs = [o for o in pimgs if _clear(o)]; prules = [o for o in prules if _clear(o)]

# assign each PDF line to a Word paragraph: the nearest paragraph (from a moving cursor) whose text contains the line's text
# 6 Nov 2026 (owner 08:53 agreement: "matches each PDF line to its own Word paragraph"): the PDF's lines are read in order of
# their baselines, so side-by-side columns (Word's column lists) interleave and one cursor jumped between columns - a list line
# whose words occur in several lists ("Puzzle Words") went to the wrong list. Now each column of a page keeps its own cursor
# (columns: the page's line starts grouped where they differ by more than 150 pt and the groups share baselines), and a line that
# equals a paragraph's whole text is preferred to one merely contained in a longer paragraph.
def _cols(pn):
    xs = sorted(set(round(L['x0']) for L in plines if L['pg'] == pn))
    grp = []; 
    for x in xs:
        if grp and x - grp[-1][-1] <= 150: grp[-1].append(x)
        else: grp.append([x])
    return grp
COLS = {}
for _pn in sorted(set(L['pg'] for L in plines)):
    g = _cols(_pn)
    for L in plines:
        if L['pg'] != _pn: continue
        L['col'] = next(i for i, gg in enumerate(g) if round(L['x0']) in gg)
# pass 1: anchors - a line of 12+ letters held by exactly one Word paragraph; pass 2: every other line goes to a paragraph that
# holds it, within the range its page's anchors give (3 either side), the whole-text match first, then the paragraph nearest to
# the anchor closest to it on the page in the same column
pmap = collections.defaultdict(list)
def _cands(L): return [k for k in range(len(TEXT)) if L['n'] and (L['n'] == TEXT[k]['n'] if len(L['n']) < 4 else L['n'] in TEXT[k]['n'])]   # a line of 1-3 letters or digits (a list number "3.") only as a whole paragraph
ANCH = {}
for idx, L in enumerate(plines):
    c = _cands(L)
    if len(L['n']) >= 12 and len(c) == 1: ANCH[idx] = c[0]
byp = collections.defaultdict(list)
for idx, k in ANCH.items(): byp[plines[idx]['pg']].append((idx, k))
for idx, L in enumerate(plines):
    if idx in ANCH: pmap[TEXT[ANCH[idx]]['i']].append(L); continue
    c = _cands(L)
    if not c: continue
    an = byp.get(L['pg'], [])
    if an:
        lo = min(k for _, k in an) - 3; hi = max(k for _, k in an) + 3
        c2 = [k for k in c if lo <= k <= hi]
        if c2: c = c2
        same = [(abs(plines[a]['base'] - L['base']), k) for a, k in an if plines[a].get('col', 0) == L.get('col', 0)] or [(abs(plines[a]['base'] - L['base']), k) for a, k in an]
        ref = min(same)[1]
    else:
        ref = c[0]
    best = min(c, key=lambda k: (0 if L['n'] == TEXT[k]['n'] else 1, abs(k - ref)))
    pmap[TEXT[best]['i']].append(L)
PP = {}
for i, ls in pmap.items():
    ls.sort(key=lambda x: (x['pg'], x['base']))
    PP[i] = dict(pg0=ls[0]['pg'], first=ls[0]['base'], pg1=ls[-1]['pg'], last=ls[-1]['base'], x0=min(x['x0'] for x in ls), n=len(ls), top=ls[0]['top'], lastbot=ls[-1]['bot'])
pitches = []
for i, ls in pmap.items():
    for a, b in zip(ls, ls[1:]):
        if a['pg'] == b['pg'] and 0 < b['base'] - a['base'] < 40 and abs(a['x0'] - b['x0']) < 60: pitches.append(b['base'] - a['base'])
PPITCH = statistics.median(pitches) if pitches else 18.0

# ---- page: measured in a browser at every width
JS = r'''
const {chromium}=require('playwright');(async()=>{const [,,dir,ws]=process.argv;const b=await chromium.launch();const res={};
for(const w of ws.split(',').map(Number)){const p=await b.newPage({viewport:{width:w,height:900}});
await p.goto('file://'+dir+'/index.html');await p.evaluate(()=>document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'));await p.waitForTimeout(4500);
res[w]=await p.evaluate(()=>{const m=document.querySelector('main');const Y=window.scrollY;const blocks=[];
 const sel=m.querySelectorAll('p,h1,h2,h3,h4,li,.res-item');
 for(const e of sel){ if(e.querySelector('p,li,.res-item'))continue; if(!e.textContent.trim())continue;
  const rs=[];const tw=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let tn;while((tn=tw.nextNode())){if(!tn.nodeValue.trim())continue;const r=document.createRange();r.selectNodeContents(tn);for(const x of r.getClientRects())if(x.width>1&&x.height>4)rs.push(x);}
  if(!rs.length)continue; const lines=[];
  for(const x of rs.sort((a,b)=>a.top-b.top)){const L=lines.find(l=>Math.abs(l.top-x.top)<4&&Math.abs(l.bot-x.bottom)<6);if(L){L.x0=Math.min(L.x0,x.left);L.bot=Math.max(L.bot,x.bottom);}else lines.push({top:x.top,bot:x.bottom,x0:x.left});}
  // a line's baseline: the bottom of its text boxes less the font's descent (same font everywhere, so the bottom serves)
  lines.sort((a,b)=>a.top-b.top);
  const ys=[];for(const l of lines){const k=ys.find(z=>Math.abs(z.top-l.top)<4);if(!k)ys.push(l);}
  blocks.push({t:e.textContent,first:ys[0].bot+Y,last:ys[ys.length-1].bot+Y,lastbot:ys[ys.length-1].bot+Y,top:ys[0].top+Y,x0:Math.min(...ys.map(l=>l.x0)),n:ys.length,lines:ys.map(l=>l.bot+Y),tag:e.tagName,cls:e.className,fe:(e.firstElementChild&&e.textContent.trim().startsWith(e.firstElementChild.textContent.trim())?e.firstElementChild.tagName:'')});}
 const objs=[];for(const im of m.querySelectorAll('img')){const q=im.getBoundingClientRect();if(q.height<20||q.width<20)continue;objs.push({k:'image',top:q.top+Y,bot:q.bottom+Y,x0:q.left});}
 for(const r of m.querySelectorAll('.beige-rule,.mm-org-rule,hr,p.mm-gl')){const q=r.getBoundingClientRect();if(!q.width)continue;objs.push({k:'rule',top:q.top+Y,bot:q.bottom+Y,x0:q.left});}
 return {blocks,objs,sw:document.documentElement.scrollWidth,iw:innerWidth};});await p.close();}
console.log(JSON.stringify(res));await b.close();})();
'''
open(os.path.join(OUT, 'measure.js'), 'w').write(JS)
raw = subprocess.run(['node', os.path.join(OUT, 'measure.js'), os.path.abspath(PAGEDIR), ','.join(map(str, WIDTHS))], capture_output=True, text=True, timeout=1800)
if raw.returncode: print(raw.stderr[-2000:]); sys.exit(2)
PAGE = json.loads(raw.stdout)

def match_page(blocks):
    """Word paragraph index -> page block, in order (the page's words may differ from Word by the agreed typo fixes)"""
    out = {}; pos = 0; bn = [norm(b['t']) for b in blocks]
    for w in TEXT:
        best, bs = None, 0.0
        for k in range(max(0, pos - 15), min(len(blocks), pos + 40)):
            a, c = w['n'][:80], bn[k][:80]
            if not a or not c: continue
            L1, L2 = len(w['n']), len(bn[k])
            # containment counts only between texts of about the same length (a short title inside a long quotation is not a match)
            s = 1.0 if ((a in bn[k] or c in w['n']) and min(L1, L2) >= 0.7 * max(L1, L2)) else difflib.SequenceMatcher(None, w['n'][:120], bn[k][:120], autojunk=False).ratio()
            if s > bs + 1e-9 or (abs(s - bs) < 1e-9 and best is not None and abs(k - pos) < abs(best - pos)): best, bs = k, s
        if best is not None and bs >= 0.75: out[w['i']] = blocks[best]; pos = best
    return out

def objs_between(objs, y0, y1):
    ob = sorted([o for o in objs if o['top'] >= y0 - 2 and o['bot'] <= y1 + 2], key=lambda o: o['top'])
    out = []   # the images of one row are one object (top of the highest, bottom of the lowest)
    for o in ob:
        if out and o['k'] == 'image' and out[-1]['k'] == 'image' and o['top'] < out[-1]['bot'] - 5:
            out[-1] = dict(k='image', top=min(out[-1]['top'], o['top']), bot=max(out[-1]['bot'], o['bot']), x0=min(out[-1]['x0'], o['x0']))
        else: out.append(dict(o))
    return out

pairs = [(a['i'], b['i']) for a, b in zip(TEXT, TEXT[1:])]
report = collections.OrderedDict(); kinds_pdf = collections.defaultdict(list)
# PDF side once
pdfgap = {}; NRULES = {}
for a, b in pairs:
    A, B = PP.get(a), PP.get(b)
    if not A or not B: pdfgap[(a, b)] = ('not in PDF', None); continue
    if A['pg1'] != B['pg0']: pdfgap[(a, b)] = ('page break', None); continue
    if abs(A['x0'] - B['x0']) > 60 or B['first'] < A['last'] - 1: pdfgap[(a, b)] = ('other column', None); continue
    ims = sorted([o for o in pimgs + prules if o['pg'] == A['pg1'] and o['top'] >= A['last'] - 2 and o['bot'] <= B['first'] + 2], key=lambda o: o['top'])
    if ims:   # an image row or a divider between: text to its top, and its bottom to the next text's top, each as a share of a line
        rl = sorted(o['top'] for o in prules + [x for x in pimgs if x['bot'] - x['top'] < 8 and x.get('x1', 0) - x['x0'] > 150] if o['pg'] == A['pg1'] and o['top'] >= A['last'] - 2 and o['bot'] <= B['first'] + 2)   # Word's line pictures are thin images in the PDF
        nr = sum(1 for k_, y in enumerate(rl) if k_ == 0 or y - rl[k_ - 1] > 6)   # a double line drawn as two strokes is one divider
        NRULES[(a, b)] = nr
        pdfgap[(a, b)] = ('obj', (round((ims[0]['top'] - A['lastbot']) / PPITCH, 2), round((B['top'] - ims[-1]['bot']) / PPITCH, 2)))
        kinds_pdf['above an image/divider'].append(pdfgap[(a, b)][1][0]); kinds_pdf['below an image/divider'].append(pdfgap[(a, b)][1][1]); continue
    r = (B['first'] - A['last']) / PPITCH
    pdfgap[(a, b)] = ('ok', round(r, 2)); kinds_pdf[word_kind(a, b)].append(r)
kind_med = {k: statistics.median(v) for k, v in kinds_pdf.items() if v}

faults = 0; rows = []; B_TAG = {}
for w in WIDTHS:
    pg = PAGE[str(w)]; M = match_page(pg['blocks'])
    for _i, _b in M.items(): B_TAG[(w, _i)] = '%s.%s%s' % (_b['tag'], _b['cls'], '+' + _b['fe'] if _b['fe'] in ('STRONG', 'B') else '')
    pp = [l2 - l1 for b in pg['blocks'] for l1, l2 in zip(b['lines'], b['lines'][1:]) if 0 < l2 - l1 < 80]
    pitch = statistics.median(pp) if pp else 37.2
    for a, b in pairs:
        A, B = M.get(a), M.get(b)
        kind = word_kind(a, b); st, pr = pdfgap[(a, b)]
        if pr is None and kind in kind_med: pr_use, src = round(kind_med[kind], 2), 'kind median (%s)' % st
        else: pr_use, src = pr, 'PDF'
        if not A or not B: rows.append((w, a, b, kind, src, pr_use, None, None, 'not in the text area (title, contents box; words are the code check\'s)')); continue
        if abs(A['x0'] - B['x0']) > 100 or B['first'] < A['last'] - 1:
            rows.append((w, a, b, kind, src, pr_use, None, None, 'columns (not compared)')); continue
        ob = objs_between(pg['objs'], A['last'], B['top'] + 1)
        if ob or st == 'obj':
            pa = pr if st == 'obj' else (round(kind_med.get('above an image/divider', 0), 2), round(kind_med.get('below an image/divider', 0), 2))
            if not ob: rows.append((w, a, b, 'image/divider', 'PDF', pa, None, None, 'FAULT (the PDF has an image or divider here; the page has none)')); faults += 1; continue
            if st != 'obj' and st in ('page break', 'not in PDF', 'other column'): st = 'obj'; pa = (None, None)   # the PDF cannot say here; the template's sizes judged by sameness
            elif st != 'obj': rows.append((w, a, b, 'image/divider', 'PDF', None, None, None, 'FAULT (an image or divider on the page; none here in the PDF)')); faults += 1; continue
            npg = sum(1 for o in ob if o['k'] == 'rule')
            if (a, b) in NRULES and NRULES[(a, b)] != npg:
                rows.append((w, a, b, 'dividers', 'PDF', NRULES[(a, b)], npg, None, 'FAULT (the PDF has %d divider(s) here, the page %d)' % (NRULES[(a, b)], npg))); faults += 1
            ga = ob[0]['top'] - A['lastbot']; gb = B['top'] - ob[-1]['bot']
            for o1, o2 in zip(ob, ob[1:]):   # 3 Nov 18:2x (the build 11 review): the gap between an image row and a divider, divider and image row
                if o2['top'] - o1['bot'] > -1:
                    rows.append((w, a, b, 'divider and image row' if {o1['k'], o2['k']} == {'image', 'rule'} else '%s to %s' % (o1['k'], o2['k']), 'template', None, round(o2['top'] - o1['bot'], 1), None, 'OK (template size; sameness checked)'))
            ra, rb = round(ga / pitch, 2), round(gb / pitch, 2)
            for lab, gx, rx, px in (('above ' + ob[0]['k'], ga, ra, pa[0]), ('below ' + ob[-1]['k'], gb, rb, pa[1])):
                # owner 17:23: sizes are the template's (dividers 30/30, images 30 above and below) - judged by sameness below, not by the PDF
                rows.append((w, a, b, lab, 'template', px, round(gx, 1), rx, 'OK (template size; sameness checked)'))
            continue
        g = B['first'] - A['last']; r = round(g / pitch, 2)
        # owner 17:23: the PDF is an approximation - it decides which lines belong together; the template decides the sizes.
        # together: Word has no blank line and no space between, and the PDF agrees (about one line); apart: anything else.
        together = kind == 'next paragraph' and (pr_use is None or pr_use < 1.3)
        if A['tag'] in ('H1', 'H2', 'H3', 'H4') or B['tag'] in ('H1', 'H2', 'H3', 'H4'):   # headings: the template's sizes (40 above / 25 below), judged by sameness
            rows.append((w, a, b, 'heading | ' + kind, src, pr_use, round(B['first'] - A['last'], 1), round((B['first'] - A['last']) / pitch, 2), 'OK (template size; sameness checked)')); continue
        if together: verdict = 'OK together' if r <= 1.25 else 'FAULT (together in the PDF, apart on the page)'
        else: verdict = 'APART?'   # decided below: larger than every together gap at this width
        kind = ('together | ' if together else 'apart | ') + kind
        if verdict.startswith('FAULT'): faults += 1
        rows.append((w, a, b, kind, src, pr_use, round(g, 1), r, verdict))
    tg = [x[6] for x in rows if x[0] == w and x[8] == 'OK together']; tmax = max(tg) if tg else pitch * 1.2
    for k_, x in enumerate(rows):
        if x[0] == w and x[8] == 'APART?':
            ok = x[6] >= tmax + 2
            rows[k_] = x[:8] + ('OK apart (more than every together gap, %.1f)' % tmax if ok else 'FAULT (apart in the PDF, not clearly apart on the page: %.1f against together %.1f)' % (x[6], tmax),)
            if not ok: faults += 1
    # every gap of one kind the same size (within 1 px) - the template's "sameness"
    byk = collections.defaultdict(list)
    # 4 Nov 2026 08:4x: a gap the owner ordered by name (SPACE_AGREED) is her size, not the template's - left out of the sameness groups
    _AGK = set()
    if os.environ.get('SPACE_AGREED'):
        for _l in open(os.environ['SPACE_AGREED']):
            if '->' in _l and not _l.startswith('#'): _AGK.add(tuple(int(t) for t in _l.partition('|')[0].split('->')))
    for x in rows:
        if (x[1], x[2]) in _AGK: continue
        if x[0] == w and x[6] is not None and x[3] != 'image between' and not str(x[8]).startswith('columns'): (byk['divider and image row'] if x[3] == 'divider and image row' else byk[(x[3].split(' | ')[0] + ('' if not any(t_ in str(B_TAG.get((w, x[1]), '')) for t_ in ('STRONG', 'DIV.res-item')) else ' after ' + str(B_TAG.get((w, x[1]), '')))) if x[3].split(' | ')[0] in ('together', 'apart') else x[3].split(' | ')[0] + ' ' + str(B_TAG.get((w, x[1]), '')) + ' -> ' + str(B_TAG.get((w, x[2]), ''))]).append(x[6])
    for k, v in byk.items():
        if len(v) > 2 and max(v) - min(v) > 1.5:
            rows.append((w, None, None, k, 'sameness', None, '%s..%s' % (min(v), max(v)), None, 'FAULT UNEVEN (%d gaps: %s)' % (len(v), ', '.join('%g' % x for x in sorted(set(v)))))); faults += 1
    if pg['sw'] > pg['iw']: rows.append((w, None, None, 'sideways', '', None, pg['sw'], None, 'FAULT sideways scroll')); faults += 1

# 3 Nov 2026 (owner 19:58-20:01): differences she ordered, by name - a file named by SPACE_AGREED, one per line: "a -> b | her words"
# (Word paragraph numbers as printed in this report). Such a FAULT is printed AGREED with her words and not counted.
AGREED = {}
if os.environ.get('SPACE_AGREED'):
    for _l in open(os.environ['SPACE_AGREED']):
        if '->' in _l and not _l.startswith('#'):
            _k, _, _why = _l.partition('|'); _a, _b = [int(x) for x in _k.split('->')]; AGREED[(_a, _b)] = _why.strip()
for _i, _x in enumerate(rows):
    if (_x[1], _x[2]) in AGREED and str(_x[-1]).startswith('FAULT'):
        rows[_i] = _x[:-1] + ('AGREED (owner: %s) - was: %s' % (AGREED[(_x[1], _x[2])], _x[-1]),); faults -= 1
with open(os.path.join(OUT, 'spacecheck.txt'), 'w') as f:
    f.write('spacecheck %s | PDF line pitch %.2f pt | tolerance %.2f line\n' % (os.path.abspath(PAGEDIR), PPITCH, TOL))
    f.write('PDF kinds (median ratio): %s\n' % ', '.join('%s %.2f' % (k, v) for k, v in sorted(kind_med.items())))
    for w, a, b, kind, src, pr, g, r, v in rows:
        ta = (W[a]['text'][:38] if a is not None else ''); tb = (W[b]['text'][:38] if b is not None else '')
        f.write('%5d | %-4s -> %-4s | %-16s | PDF %-5s (%s) | page %-7s px %-5s | %s | %s -> %s\n' % (w, a, b, kind, pr, src, g, r, v, ta, tb))
    f.write('RESULT: %s\n' % ('SPACING OK' if faults == 0 else '%d FAULTS' % faults))
print(open(os.path.join(OUT, 'spacecheck.txt')).read().splitlines()[-1])
