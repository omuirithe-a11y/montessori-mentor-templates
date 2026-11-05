"""Curriculum essays: Word + its PDF -> a source page in the approved frame (25 Sept), for site/make_page.py.
Usage: python3 site/convert_curriculum.py <doc>.docx <doc>.pdf site/pages/frame.html src.html /<page-link>/ "<Page Title>"
          [--photos=<folder of blurred working copies>] [--preview]

What it reads from Word (rules, the same for every curriculum essay; nothing here names a page):
  first coloured, centred-or-first line  -> the page title (shown in the hero)
  a line in Word blue #0432FF or red #EE0000, on its own -> section heading (h2, a Contents entry)
  a short line, bold, on its own          -> label (div.micro-label; template/curriculum.py decides bold or not)
  italic paragraph that opens with a quotation mark, or orange (#ED7D31) italic -> quotation;
      the line after it that starts with a dash / "=" / a Word bullet, or with "Maria Montessori" -> its attribution
  Word numbered list -> ol; Word bulleted list -> ul;  table -> table.mm-table
  hidden text (Word "vanish") is left out; links, italics and bold inside a line are kept.
What it reads from the PDF (layout only, never sizes):
  each photo is found in the PDF by its picture; photos with text beside them (text to their left on the same lines)
  -> one photo: floated single; two or more: a set beside that text; photos with no text beside them, side by side
  -> a row, placed after the text that comes before it in the PDF.
Photos: the blurred working copy when one exists (--photos), else the Word original; originals are never altered.
--preview makes the photos small (long side 900px) so the preview page stays light; the Hostinger build uses full size.
"""
import sys as _sys, os as _os, subprocess as _sp
# OA1 (7 Oct 2026, chat 22 - your order of work: "let's do them one by one, as I still need to check
# each"): one page built between your messages; qa/one_at_a_time.py refuses the second.
_q = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "qa", "one_at_a_time.py")
if _os.path.exists(_q) and len(_sys.argv) > 1:
    # 8 Oct 2026: the page is recorded by its NAME (the settings' name), as make_page.py records it - by file name the
    # converter recorded src.docx and make_page src.html, and one page counted as two
    _r = _sp.run([_sys.executable, _q, "touch", _os.path.basename(next((a.split("=", 1)[1] for a in _sys.argv if a.startswith("--settings=")), _sys.argv[1])).replace("_settings.py", "")], capture_output=True, text=True)
    if _r.returncode: _sys.exit((_r.stdout + _r.stderr).strip())
import re, sys, io, os, json, base64, zipfile, html as H
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None   # 21 Oct 2026 (5.5): the Word file's NCMPS sheet is 296 million pixels; the user's own file (build_page.py allows the same)
from bs4 import BeautifulSoup
import docx
from docx.oxml.ns import qn
import pymupdf as fitz

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
docx_path, pdf_path, frame_path, out_path, href, title_menu = args[:6]
PHOTOS = opts.get('photos'); PREVIEW = 'preview' in opts; TEST = 'test' in opts   # --test: tiny photos (long side 200px), a light copy for measuring only
log = []

D = docx.Document(docx_path)
Z = zipfile.ZipFile(docx_path)
RELS = {r.rId: r for r in D.part.rels.values()}
num_xml = Z.read('word/numbering.xml').decode('utf-8') if 'word/numbering.xml' in Z.namelist() else ''
NUMS = dict(re.findall(r'<w:num w:numId="(\d+)"[^>]*>.*?<w:abstractNumId w:val="(\d+)"/>', num_xml, re.S))
def num_fmt(num_id, ilvl='0'):
    a = NUMS.get(num_id); m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="%s".*?</w:abstractNum>' % a, num_xml, re.S) if a else None
    lv = re.search(r'<w:lvl w:ilvl="%s".*?</w:lvl>' % ilvl, m.group(0), re.S) if m else None
    if not lv: return 'bullet'
    return re.search(r'numFmt w:val="(\w+)"', lv.group(0)).group(1)

BLUE, RED, ORANGE = {'0432FF'}, {'EE0000', 'FF0000'}, {'ED7D31', 'E97132'}   # 20 Oct (5.3): E97132, Word's newer orange, too
# 29 Sept: --settings=site/pages/<page>_settings.py (optional; without it nothing changes) - what a page's settings tell the
# converter: WORD_COLOURS (a page whose Word colours differ: heading colours, material-name colours, heading lines by text;
# every other short blue line is a label), REMOVED (photos left out), EXTRA_PHOTOS (a photo not in Word/PDF -> the photo
# whose row or set it joins, right after it; the file comes from --photos).
import runpy
S = runpy.run_path(opts['settings']) if opts.get('settings') else {}
WC = S.get('WORD_COLOURS') or {}
HEAD_C, MAT_C, HEAD_TXT = set(WC.get('heading', ())), set(WC.get('material', ())), set(WC.get('heading_lines', ()))
REMOVED = set(S.get('REMOVED', ())); EXTRA = dict(S.get('EXTRA_PHOTOS', {}))
NO_CROP = set(S.get('NO_CROP', ()))   # 2 Oct (20th chat): photos shown whole although Word crops them - only when the user says so
WORD_PIC = set(S.get('WORD_PICTURE', ()))   # 29 Sept: Word's own picture, with Word's crop, instead of the working copy
COLS = set(S.get('COLUMNS', {}))   # a single photo beside its own text, set by the page as a one-material column: a set, not a float
UPRIGHT = set(S.get('UPRIGHT', ()))   # working copies already stored upright: Word's turn is not applied again
QUOTE_OPEN = '“"‘\''

# ------------------------------------------------------------------ Word: paragraphs, runs, photos
CSTYLE = {}
for st in D.styles:
    try:
        if st.type == 2: CSTYLE[st.style_id] = dict(b=st.font.bold, i=st.font.italic)     # character styles (e.g. Emphasis)
    except Exception: pass
def rprops(r):
    rp = r.find(qn('w:rPr'))
    rs = rp.find(qn('w:rStyle')) if rp is not None else None
    cs = CSTYLE.get(rs.get(qn('w:val')), {}) if rs is not None else {}
    def on(tag, key=None):
        e = rp.find(qn(tag)) if rp is not None else None
        if e is None: return bool(cs.get(key)) if key else False         # not set on the run: its character style decides
        return e.get(qn('w:val')) not in ('0', 'false')
    c = rp.find(qn('w:color')) if rp is not None else None
    u = rp.find(qn('w:u')) if rp is not None else None
    bd = rp.find(qn('w:bdr')) if rp is not None else None   # 6 Nov 2026 (owner 00:19): a run Word shows in a box
    if bd is not None and bd.get(qn('w:val')) not in (None, 'none', 'nil'):
        u = 'box:' + (bd.get(qn('w:color')) or 'auto').upper()
        return dict(b=on('w:b', 'b'), i=on('w:i', 'i'), hidden=on('w:vanish'), color=(c.get(qn('w:val')).upper() if c is not None else None), u=u)
    return dict(b=on('w:b', 'b'), i=on('w:i', 'i'), hidden=on('w:vanish'), color=(c.get(qn('w:val')).upper() if c is not None else None),
                u=('none' if u is not None and u.get(qn('w:val')) == 'none' else (u is not None and u.get(qn('w:val')) not in (None, 'none', '0', 'false'))))   # 5 Nov 2026 (The English Curriculum, format check): an explicit "no underline" (w:u none) is kept as 'none', so a link Word shows without underline has none on the page   # 1 Oct (16th chat): <w:u> with no w:val shows no underline in Word (PDF)   # 1 Oct: underline kept (rule: follow the Word/PDF)

def segments(p_el):
    """The paragraph's visible text as (text, bold, italic, link, colour) pieces, in order; fields and links followed."""
    segs, link, field, instr = [], None, [], ''
    def walk(el, href=None):
        nonlocal link, instr
        for ch in el:
            tag = ch.tag.split('}')[1]
            if tag == 'hyperlink':
                rid = ch.get(qn('r:id')); url = RELS[rid].target_ref if rid in RELS else None
                if ch.get(qn('w:anchor')): url = (url + '#' + ch.get(qn('w:anchor'))) if url else None   # 20 Oct (5.4): a link to a heading inside another document keeps its address; only a link to a place in this document (no address) is dropped
                walk(ch, url)
            elif tag in ('smartTag', 'ins', 'customXml', 'sdt', 'sdtContent', 'fldSimple'):
                u = None
                if tag == 'fldSimple':
                    m = re.search(r'HYPERLINK\s+"([^"]+)"', ch.get(qn('w:instr')) or ''); u = m.group(1) if m else None
                walk(ch, u or href)
            elif tag == 'r':
                fc = ch.find(qn('w:fldChar'))
                if fc is not None:
                    t = fc.get(qn('w:fldCharType'))
                    if t == 'begin': field.append(None); instr = ''
                    elif t == 'separate':
                        m = re.search(r'HYPERLINK\s+"([^"]+)"', instr)
                        if field: field[-1] = m.group(1) if m else ''
                    elif t == 'end' and field: field.pop()
                    continue
                it = ch.find(qn('w:instrText'))
                if it is not None: instr += it.text or ''; continue
                if field and field[-1] is None: continue          # the field's instruction, not its text
                pr = rprops(ch)
                if pr['hidden']: continue
                txt = ''
                for x in ch:
                    xt = x.tag.split('}')[1]
                    if xt == 't': txt += x.text or ''
                    elif xt == 'tab': txt += '\t'
                    elif xt in ('br', 'cr'): txt += '\n'
                    elif xt == 'noBreakHyphen': txt += '-'
                    elif xt == 'sym': txt += ''
                if txt: segs.append([txt, pr['b'], pr['i'], href or (field[-1] if field and field[-1] else None), pr['color'], pr['u']])
    walk(p_el)
    return segs

def seg_html(segs, strip_bold=False, strip_italic=False):
    out, i = [], 0
    merged = []
    # 1 Oct (fifteenth chat), your rule - follow the Word/PDF: a word Word colours inside a line keeps its colour (only when
    # the line mixes colours - a line wholly in one colour is a heading or label, decided elsewhere); Word's underline kept;
    # Word's tabs kept (tab stops every 48px, as Word's default half inch); tabs at the end of a line dropped
    segs = [list(s) + [None] * (6 - len(s)) for s in segs]
    vis = [s for s in segs if s[0].strip()]
    norm = lambda c: None if c in (None, 'AUTO', '000000', '141414', '0D0D0D') else c
    mixed = len({norm(s[4]) for s in vis}) > 1
    for s in segs:
        if merged and merged[-1][1:] == s[1:]: merged[-1][0] += s[0]
        else: merged.append(list(s))
    for t, b, it, url, col, ul in merged:
        h = H.escape(t).replace('\n', '<br/>')
        h = re.sub(r'\t+', lambda m: '<span class="mm-t">' + '\t' * len(m.group(0)) + '</span>', h)
        if it and not strip_italic and t.strip(): h = f'<em>{h}</em>'
        if b and not strip_bold and t.strip(): h = f'<strong>{h}</strong>'
        if ul is True and t.strip(): h = f'<u>{h}</u>'
        # 26 Oct 2026 (2.2.0 page check): orange is never kept (the standing rule: orange Word text shows as regular black), and a
        # colour on punctuation or spaces alone is not kept (a yellow opening quotation mark, a red comma - no meaning on the page)
        if mixed and norm(col) and col not in ORANGE and re.search(r'\w', t): h = f'<span class="mm-wcol" style="color:#{col}">{h}</span>'
        if url: h = f'<a href="{H.escape(url)}" rel="noopener" target="_blank"' + ((' class="mm-nou"' if ul == 'none' else (' class="mm-nou mm-box mm-box-%s"' % ul[4:] if isinstance(ul, str) and ul.startswith('box:') else ''))) + f'>{h}</a>'
        out.append(h)
    h = re.sub(r'(?<=\S) {3,}(?=\S)', lambda m: ' ' * len(m.group(0)), ''.join(out))   # 20 Oct (5.3 "p. 248.   (1949)"): Word's run of 3+ spaces is kept (the site's gap rule)
    h = re.sub(r'[ \n\r]{2,}', ' ', h).strip()
    return re.sub(r'(<span class="mm-t">\t+</span>\s*)+$', '', h).strip()

CROP = {}            # photo -> Word's crop (left, top, right, bottom, fractions); applied to every photo (2 Oct, 20th chat; was WORD_PICTURE only)
TURN = {}            # photo -> (degrees clockwise, flip H, flip V) as set in Word (26 Sept: honoured, e.g. a photo turned 180 in Word)
def photos_of(p_el):
    out = []
    for dr in p_el.iter(qn('w:drawing')):
        blip = dr.find('.//' + qn('a:blip'))
        if blip is None: continue
        rid = blip.get(qn('r:embed')); name = RELS[rid].target_ref.split('/')[-1]
        sr = dr.find('.//' + qn('a:srcRect'))
        if sr is not None: CROP[name] = tuple(int(sr.get(k) or 0) / 100000 for k in ('l', 't', 'r', 'b'))
        xf = dr.find('.//' + qn('a:xfrm'))
        if xf is not None and (xf.get('rot') or xf.get('flipH') == '1' or xf.get('flipV') == '1'):
            TURN[name] = (int(xf.get('rot') or 0) / 60000, xf.get('flipH') == '1', xf.get('flipV') == '1')
        out.append(name)
    return out

paras = []            # records in document order (tables too)
for el in D.element.body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'tbl':
        paras.append(dict(kind='table', el=el, text='', photos=[])); continue
    if tag != 'p': continue
    segs = segments(el)
    text = ''.join(s[0] for s in segs)
    vis = [s for s in segs if s[0].strip()]
    chars = sum(len(s[0].strip()) for s in vis) or 1
    ppr = el.find(qn('w:pPr')); numpr = ppr.find(qn('w:numPr')) if ppr is not None else None
    num = None
    if numpr is not None and numpr.find(qn('w:numId')) is not None and numpr.find(qn('w:numId')).get(qn('w:val')) != '0':
        nid = numpr.find(qn('w:numId')).get(qn('w:val')); il = numpr.find(qn('w:ilvl')); il = il.get(qn('w:val')) if il is not None else '0'
        num = (nid, num_fmt(nid, il))
    jc = ppr.find(qn('w:jc')) if ppr is not None else None
    paras.append(dict(kind='p', el=el, segs=segs, text=text.strip(), photos=photos_of(el), num=num,
                      centred=jc is not None and jc.get(qn('w:val')) == 'center',
                      bold=sum(len(s[0].strip()) for s in vis if s[1]) / chars, italic=sum(len(s[0].strip()) for s in vis if s[2]) / chars,
                      colours={s[4] for s in vis}))

# ------------------------------------------------------------------ classify
def colour_of(p):
    c = {x for x in p['colours'] if x not in (None, '000000', 'AUTO')}
    return c.pop() if len(c) == 1 else None
title = None
# 24 Oct 2026 (2.2.0): Word's first line that reads the page's own title is the title, whatever its colour - the first
# coloured line (the blue heading "My experience preparing environments") had been taken as the title and left out
_first = next((p for p in paras if p['kind'] == 'p' and p['text']), None)
if _first is not None and re.sub(r'\s+', ' ', _first['text']).strip().lower() == re.sub(r'\s+', ' ', title_menu).strip().lower():
    _first['role'] = 'title'; title = _first['text']
for k, p in enumerate(paras):
    if p.get('role') == 'title': continue
    if p['kind'] != 'p' or not p['text']: p.setdefault('role', 'empty' if p['kind'] == 'p' else 'table'); continue
    c = colour_of(p); t = p['text']
    if title is None and c in RED | BLUE | HEAD_C | MAT_C:
        title = t; p['role'] = 'title'; continue
    if WC and len(t) < 90 and not p['num'] and p['italic'] < .5 and not re.search(r'[.:,;]$', t) and (
            t in HEAD_TXT or c in HEAD_C or c in MAT_C or c in BLUE):
        p['role'] = 'heading' if (t in HEAD_TXT or c in HEAD_C) else 'label'
        if c in MAT_C and t not in HEAD_TXT: p['material'] = True
    if p.get('role'): continue
    if not p['num'] and p['italic'] < .5 and c in BLUE | RED and any(sg[3] and sg[0].strip() == 'PDF' for sg in p['segs']): p['role'] = 'p'; p['pdfline'] = True; continue   # 22 Oct 2026 (user 22:26, "1"; 2.1.2): a blue or red line holding a PDF link is a text line, not a heading - as a heading it lost its link
    if not WC and c in BLUE | RED and len(t) < 90 and not p['num'] and p['italic'] < .5 and not re.search(r'[.:,;]$', t):
        p['role'] = 'heading'
    elif p['bold'] > .9 and len(t) < 70 and not re.search(r'[.;,]$', t):   # 20 Oct (5.3): a short line wholly bold is a label, even in italics within quotation marks ('One-up, one-down')
        p['role'] = 'label'
    elif (p['italic'] > .8 and t[0] in QUOTE_OPEN) or (c in ORANGE and p['italic'] > .5) or (ORANGE & p['colours'] and p['italic'] > .5):
        p['role'] = 'quote'
    elif p['num']:
        p['role'] = 'ol' if p['num'][1] in ('decimal', 'lowerLetter', 'upperLetter', 'lowerRoman', 'upperRoman') else 'ul'
    else:
        p['role'] = 'p'
# a short line on its own, not bold in Word, between labels of the same kind (label, then its paragraph) is a label too (25 Sept)
def nxt(k, step):
    j = k + step
    while 0 <= j < len(paras) and paras[j].get('role') == 'empty' and not paras[j]['photos']: j += step
    return j if 0 <= j < len(paras) else None
for k, p in enumerate(paras):
    if p.get('role') != 'p' or p.get('pdfline') or len(p['text']) > 60 or re.search(r'[.:;,]$', p['text']): continue
    a, b = nxt(k, 1), nxt(k, -1)
    if a is None or paras[a].get('role') != 'p' or len(paras[a]['text']) <= 120: continue
    if b is not None and paras[b].get('role') == 'p' and len(paras[b]['text']) < 120: continue      # a line in a list, not a label
    two_on = nxt(a, 1); two_back = nxt(b, -1) if b is not None else None
    if (two_on is not None and paras[two_on].get('role') == 'label') or (two_back is not None and paras[two_back].get('role') == 'label'):
        p['role'] = 'label'
# attributions: the line after a quotation
for k, p in enumerate(paras):
    if p.get('role') != 'quote': continue
    j = k + 1
    while j < len(paras) and paras[j].get('role') == 'empty' and not paras[j]['photos']: j += 1
    if j < len(paras) and paras[j]['kind'] == 'p':
        q = paras[j]; t = q['text']
        if re.match(r'^[-‐-―=]\s', t) or re.match(r'^Maria Montessori\b', t) or (q['num'] and q['num'][1] == 'bullet' and len(t) < 160):
            q['role'] = 'cite'
# a numbered label (Word list, bold): keeps its number
labels_numbered = 0
for p in paras:
    if p.get('role') == 'label' and p['num']: labels_numbered += 1

# ------------------------------------------------------------------ PDF: where each photo sits
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im); im = bg
    return im.convert('RGB')
def sig(im):
    a = np.asarray(flat(im).resize((24, 24), Image.BILINEAR), float).ravel(); return (a - a.mean()) / (a.std() + 1e-6)
# 28 Sept: pictures are opened one at a time, only when needed (full-size documents - Sensorial, 207 photos up to
# 4608px - ran out of memory when every picture was kept open); picture matching uses a reduced decode (tested on Sensorial only)
MEDIA_PATH = {n.split('/')[-1]: n for n in Z.namelist() if n.startswith('word/media/') and not n.endswith('.wdp')}
def open_media(name, small=None):
    im = Image.open(io.BytesIO(Z.read(MEDIA_PATH[name])))
    if small and im.format == 'JPEG': im.draft('RGB', (small, small))
    return im
media = {}
for n in MEDIA_PATH:
    try: open_media(n); media[n] = True
    except Exception: pass
order = [n for p in paras for n in p['photos']]
msig = {n: sig(open_media(n, 96)) for n in order if n in media}
pdf = fitz.open(pdf_path)
norm = lambda t: re.sub(r'[^a-z0-9]', '', t.lower().replace('’', "'"))
# the Word text as one stream, to find which paragraph each PDF line belongs to
stream, owner = '', []
for k, p in enumerate(paras):
    if p['kind'] == 'p' and p['text']:
        s = norm(p['text']); stream += s; owner += [k] * len(s)
    elif p['kind'] == 'table':
        s = norm(' '.join(c.text for c in p['el'].iter(qn('w:t')) if c.text)); stream += s; owner += [k] * len(s)
cursor = 0
placed = {}           # photo -> dict(page, bbox)
lines_all = []        # (page, bbox, para index)
cands = []           # 20 Oct 2026: every PDF picture first, then the best overall fit (was: first come, first served,
                     # so Word's line pictures, drawn as images in the PDF, took real photos - 5.3, 5.5)
for pn, page in enumerate(pdf):
    for info in page.get_image_info(xrefs=True):
        x0, y0, x1, y1 = info['bbox']
        if y1 - y0 < 6 or x1 - x0 < 6: continue          # a line picture
        try: pm = fitz.Pixmap(pdf, info['xref']); pm = fitz.Pixmap(fitz.csRGB, pm) if pm.n - pm.alpha > 3 or pm.alpha else pm
        except Exception: continue
        s = sig(Image.frombytes('RGB', (pm.width, pm.height), pm.samples) if pm.n == 3 else Image.open(io.BytesIO(pm.tobytes('png'))))
        cands.append((pn, info['bbox'], s))
for pn, page in enumerate(pdf):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']); nt = norm(t)
            if len(nt) < 2: continue
            j = stream.find(nt, cursor)
            if j < 0 or j - cursor > 4000: j = stream.find(nt[:12], cursor)
            if j - cursor > 300: j = -1   # 29 Sept: the 12-letter fallback only near the cursor (a caption, "Presentation complete", matched 80 paragraphs ahead)
            if j < 0 and re.match(r'^\s*\d{1,3}[.)]\s', t):   # 2 Oct (nineteenth chat): a Word-numbered line - the PDF shows its number, the Word text does not
                nt = norm(re.sub(r'^\s*\d{1,3}[.)]\s*', '', t)); j = stream.find(nt, cursor) if len(nt) >= 2 else -1
                if j - cursor > 4000: j = -1
            if j < 0: continue
            cursor = j + len(nt); lines_all.append((pn, l['bbox'], owner[min(j, len(owner) - 1)]))
pairs = sorted((float(np.mean((msig[n] - s) ** 2)), ci, n) for ci, (_, _, s) in enumerate(cands) for n in msig)
used = set()
for err, ci, n in pairs:
    if n in placed or ci in used: continue
    placed[n] = dict(page=cands[ci][0], bbox=cands[ci][1], err=err); used.add(ci)
CAPTION = {}   # captions from Word text boxes: removed 29 Sept (sixth chat, your answer 12b)
for n in REMOVED: placed.pop(n, None)       # 29 Sept (--settings): matched in the PDF, then left out
missing = [n for n in order if n not in placed and n not in REMOVED]
bad = [n for n in placed if placed[n]['err'] > 0.35]
log.append(f'PDF: {len(placed)} of {len(order)} photos found' + (f'; not found: {missing}' if missing else '') + (f'; weak matches: {bad}' if bad else ''))

# group photos: beside text (text to their left on the same lines) or rows (side by side, nothing beside)
def vov(a, b, frac=.5):                  # vertical overlap as a share of the smaller height
    o = min(a[3], b[3]) - max(a[1], b[1]); return o > frac * min(a[3] - a[1], b[3] - b[1])
LEFT_SIDE = set()      # 30 Sept: single photos Word places at the left of their text (marked data-side="left")
groups = []
for pn in range(len(pdf)):
    ph = sorted([n for n in placed if placed[n]['page'] == pn], key=lambda n: (placed[n]['bbox'][1], placed[n]['bbox'][0]))
    lines = [(bb, k) for (p0, bb, k) in lines_all if p0 == pn]
    for n in ph:
        bb = placed[n]['bbox']
        beside = sorted({k for (lb, k) in lines if lb[2] <= bb[0] + 4 and min(lb[3], bb[3]) - max(lb[1], bb[1]) > 2})
        # 30 Sept (3.1.1): a single photo Word places at the LEFT of its text (text to its right, no other photo beside
        # it) is a single photo beside that text too (TEMPLATE F2: at the right margin); a heading beside it is left out
        if not beside and not any(m != n and vov(placed[m]['bbox'], bb, .3) for m in ph):
            beside = sorted({k for (lb, k) in lines if lb[0] >= bb[2] - 4 and min(lb[3], bb[3]) - max(lb[1], bb[1]) > 2
                             and paras[k].get('role') != 'heading'})
            if beside: LEFT_SIDE.add(n)
        # 30 Sept (3.1.1): a photo level with a section heading and the text under it belongs to that section - the
        # heading is not counted as text beside it (else the photo is placed before the heading, in the section above)
        if any(paras[k].get('role') == 'heading' for k in beside) and any(paras[k].get('role') != 'heading' for k in beside):
            beside = [k for k in beside if paras[k].get('role') != 'heading']
        g = next((g for g in groups if g['page'] == pn and (
                  (beside and g['beside'] and set(beside) & set(g['beside'])) or
                  (not beside and not g['beside'] and any(vov(placed[m]['bbox'], bb, .3) for m in g['photos'])))), None)
        if g: g['photos'].append(n); g['beside'] = sorted(set(g['beside']) | set(beside))
        else: groups.append(dict(page=pn, photos=[n], beside=beside))
    # the text before each row in the PDF (last line above it on the page; else the page before)
    for g in groups:
        if g['page'] != pn or g['beside'] or 'after' in g: continue
        top = min(placed[m]['bbox'][1] for m in g['photos'])
        above = [k for (lb, k) in lines if lb[3] <= top + 2]
        if above: g['after'] = max(above)
        else:
            prev = [k for (p0, lb, k) in lines_all if p0 < pn]
            g['after'] = max(prev) if prev else -1
for g in groups:
    g['photos'].sort(key=lambda n: (round(placed[n]['bbox'][1] / 40), placed[n]['bbox'][0])) if g['beside'] else g['photos'].sort(key=lambda n: placed[n]['bbox'][0])

# a set beside a list covers the list's lines (the run of short lines it sits in); two sets on one run share it out
def short(k): p = paras[k]; return p['kind'] == 'p' and p.get('role') in ('p', 'ul', 'ol') and 0 < len(p['text']) < 120
def run_of(k):
    a = b = k
    while a - 1 >= 0 and (short(a - 1) or (paras[a - 1].get('role') == 'empty' and not paras[a - 1]['photos'] and a - 2 >= 0 and short(a - 2))): a -= 1
    while b + 1 < len(paras) and (short(b + 1) or (paras[b + 1].get('role') == 'empty' and not paras[b + 1]['photos'] and b + 2 < len(paras) and short(b + 2))): b += 1
    while paras[a].get('role') == 'empty': a += 1
    while paras[b].get('role') == 'empty': b -= 1
    return a, b
bes = sorted([g for g in groups if g['beside'] and len(g['photos']) > 1], key=lambda g: g['beside'][0])
for g in bes:
    if all(short(k) for k in g['beside']): g['run'] = run_of(g['beside'][0])
for i, g in enumerate(bes):
    if 'run' not in g: continue
    a, b = g['run']; lo, hi = g['beside'][0], g['beside'][-1]
    prev = bes[i - 1] if i and bes[i - 1].get('run') == g['run'] else None
    nxt = bes[i + 1] if i + 1 < len(bes) and bes[i + 1].get('run') == g['run'] else None
    lo = a if prev is None else prev['beside'][-1] + 1
    hi = b if nxt is None else nxt['beside'][0] - 1
    g['beside'] = list(range(lo, hi + 1))
    if prev is not None or nxt is not None: g['pair'] = f'{a}-{b}'
for g in groups:
    if g['beside'] and len(g['photos']) == 1 and all(short(k) for k in g['beside']): g['beside'] = list(range(*[x + y for x, y in zip(run_of(g['beside'][0]), (0, 1))]))

for g in groups:                         # 29 Sept: a one-material column set holds its own label (Block 1 ...), as on the approved page
    if g['beside'] and len(g['photos']) == 1 and g['photos'][0] in COLS:
        j = g['beside'][0] - 1
        while j >= 0 and paras[j].get('role') == 'empty' and not paras[j]['photos']: j -= 1
        if j >= 0 and paras[j].get('role') == 'label' and not any(j in h['beside'] for h in groups if h is not g):
            g['beside'] = list(range(j, g['beside'][-1] + 1))
        e = g['beside'][-1]; j = e + 1        # ... and the rest of its item's lines, up to the next label or heading
        while j < len(paras) and (paras[j].get('role') == 'empty' and not paras[j]['photos'] or paras[j].get('role') == 'p'):
            if paras[j].get('role') == 'p':
                if any(j in h['beside'] for h in groups if h is not g) or len(paras[j]['text']) >= 120: break
                e = j
            j += 1
        g['beside'] = list(range(g['beside'][0], e + 1))
for new, after in EXTRA.items():          # 29 Sept (--settings): a photo not in Word joins the group of the photo named
    g = next(g for g in groups if after in g['photos']); g['photos'].insert(g['photos'].index(after) + 1, new)
    log.append(f'Added (not in Word): {new} after {after}')
# ------------------------------------------------------------------ build the page
def photo_bytes(name):
    # 26 Sept: --photos may name several folders of working copies, comma-separated; the first that has the photo wins
    src = next((os.path.join(d, name) for d in (PHOTOS or '').split(',') if d and os.path.exists(os.path.join(d, name))), None)
    if name in WORD_PIC: src = None
    im = Image.open(src) if src else open_media(name)
    im = flat(im)
    if name in CROP and name not in NO_CROP:   # 2 Oct (20th chat, your question): Word's crop on EVERY photo, working copies included
        l, t, r, b = CROP[name]; W0, H0 = im.size
        im = im.crop((round(W0 * l), round(H0 * t), round(W0 * (1 - r)), round(H0 * (1 - b))))
    if name in TURN and not (src and name in UPRIGHT):
        deg, fh, fv = TURN[name]
        if fh: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if fv: im = im.transpose(Image.FLIP_TOP_BOTTOM)
        if deg: im = im.rotate(-deg, expand=True)
    cap = 200 if TEST else 900
    if (PREVIEW or TEST) and max(im.size) > cap:
        k = cap / max(im.size); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=60 if TEST else 80 if PREVIEW else 90); return im.size, b.getvalue(), bool(src)
store = {}; nblur = 0
def figure(name):
    global nblur
    (w, h), data, bl = photo_bytes(name); nblur += bl
    k = f'__IMG{len(store)}__'; store[k] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
    ar = w / h
    return (f'<figure class="ph {"landscape" if ar >= 1 else "portrait"}" style="--h:180;--hg:180;--hp:180;--ar:{ar:.5f}">'
            f'<div class="pim" style="aspect-ratio:{ar:.5f}"><img alt="" class="doc-img" data-name="{name}" loading="lazy" src="{k}"/></div>'
            + (f'<figcaption>{H.escape(CAPTION[name])}</figcaption>' if name in CAPTION else '') + '</figure>')

def table_html(el):
    rows = []
    for ri, tr in enumerate(el.iter(qn('w:tr'))):
        cells = []
        for tc in tr.iter(qn('w:tc')):
            ps = [seg_html(segments(p)) for p in tc.iter(qn('w:p'))]
            cells.append('<br/>'.join(x for x in ps if x))
        tagc = 'th' if ri == 0 else 'td'
        rows.append('<tr>' + ''.join(f'<{tagc}>{c}</{tagc}>' for c in cells) + '</tr>')
    return '<div class="mm-table-wrap"><table class="mm-table"><thead>' + rows[0] + '</thead><tbody>' + ''.join(rows[1:]) + '</tbody></table></div>'

def fmt_num(k, fm):
    if fm == 'lowerLetter': return chr(96 + k) if k <= 26 else str(k)
    if fm == 'upperLetter': return chr(64 + k) if k <= 26 else str(k)
    if fm in ('lowerRoman', 'upperRoman'):
        v, out = k, ''
        for val, sym in ((1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')):
            while v >= val: out += sym; v -= val
        return out if fm == 'lowerRoman' else out.upper()
    return str(k)
def para_html(p):
    r = p['role']
    if r == 'heading': return None
    if r == 'label':
        n = ''
        if p['num']:
            counters.setdefault(p['num'][0], 0); counters[p['num'][0]] += 1; n = f'{counters[p["num"][0]]}. '
            n = f'{fmt_num(counters[p["num"][0]], p["num"][1])}. '   # 20 Oct 2026: in Word's format (5.5: a., b.)
        # 26 Sept list, item 4: a label keeps Word's weight and colour (template/curriculum.py applies them)
        wc = colour_of(p); wa = f' data-word-bold="{1 if p["bold"] > .5 else 0}"' + (f' data-word-colour="{wc}"' if wc else '')
        if p.get('material'): wa = ' data-word-bold="0" data-word-colour="0432FF" data-material="1"'   # 29 Sept: shown in Word blue (--settings)
        return f'<div class="micro-label"{wa}>{H.escape(n)}{seg_html(p["segs"], strip_bold=True)}</div>'
    if r == 'p': return f'<p{" class=\"centred\"" if p["centred"] else ""}>{seg_html(p["segs"])}</p>'
    if r in ('ol', 'ul'): return f'<li>{seg_html(p["segs"])}</li>'
    if r == 'table': return table_html(p['el'])
    return None
counters = {}

beside_of = {}          # first paragraph of a beside-text group -> group
# 2 Oct (twentieth chat): a group's text never runs past a section heading - the heading starts a new section, so a
# set beside text that spans one (3.6.1: photos 3, 4 beside the lines either side of a heading) stops before it
for g in groups:
    if g['beside']:
        cut = next((j for j in range(g['beside'][0] + 1, g['beside'][-1] + 1) if paras[j].get('role') == 'heading'), None)
        if cut is not None: g['beside'] = [j for j in g['beside'] if j < cut]
rows_after = {}         # paragraph index -> rows that follow it
for g in groups:
    if g['beside']: beside_of.setdefault(g['beside'][0], []).append(g)
    else: rows_after.setdefault(g['after'], []).append(g)
in_group = {k for g in groups if g['beside'] for k in range(g['beside'][0], g['beside'][-1] + 1)}

out, secs, toc = [], [], []
def row_html(g): return '<div class="photo-row">' + ''.join(figure(n) for n in g['photos']) + '</div>'
def close_list():
    if out and out[-1] in ('</ol>', '</ul>'): return
k = 0; open_list = None; pending_quote = None
open_num = None; ol_count = {}   # Word numId -> items numbered so far (30 Sept)
def emit(h):
    global open_list
    if open_list and not h.startswith('<li>'):
        out.append(f'</{open_list}>'); open_list = None
    out.append(h)
while k < len(paras):
    p = paras[k]; r = p.get('role')
    for g in rows_after.get(k - 1, []) if k == 0 else []: emit(row_html(g))
    if k in beside_of:
        for g in beside_of[k]:
            if len(g['photos']) == 1 and g['photos'][0] not in COLS:
                if all(paras[j].get('role') in ('quote', 'cite', 'empty') for j in g['beside']): paras[g['beside'][0]]['float_in'] = g['photos'][0]; continue
                for j in g['beside']:   # 26 Sept: a quotation that stands beside the photo in the PDF, after text, sits beside it too
                    if paras[j].get('role') == 'quote': paras[j]['beside_float'] = True
                fg = figure(g['photos'][0])
                if g['photos'][0] in LEFT_SIDE: fg = fg.replace('<figure ', '<figure data-side="left" ', 1)
                emit('<div class="photo-row ext-float">' + fg + '</div>'); continue
            last = g['beside'][-1]; inner = []
            for j in range(k, last + 1):
                pj = paras[j]; rj = pj.get('role')
                if rj == 'quote':
                    c = ''
                    if j + 1 <= last and paras[j + 1].get('role') == 'cite': c = f"<cite>{seg_html(paras[j + 1]['segs'])}</cite>"
                    inner.append(f"<blockquote class=\"pullquote\"><p>{seg_html(pj['segs'], strip_italic=True)}</p>{c}</blockquote>"); continue
                if rj in ('cite', 'empty', 'title'): continue
                h = para_html(pj)
                if rj in ('ol', 'ul') and h: h = f'<p>{h[4:-5]}</p>'
                if h: inner.append(h)
            emit('<div class="pdf-set"' + (f' data-pair="{g["pair"]}"' if g.get('pair') else '') + '><div class="ps-text">' + ''.join(inner) + '</div><div class="ps-imgs">' + ''.join(figure(n) for n in g['photos']) + '</div></div>')
            for j in range(k, last + 1): paras[j]['done'] = True
            for j in range(k, last + 1):
                for g2 in rows_after.get(j, []): emit(row_html(g2))
        if any(len(g['photos']) > 1 or g['photos'][0] in COLS for g in beside_of[k]):
            k = max(g['beside'][-1] for g in beside_of[k] if len(g['photos']) > 1 or g['photos'][0] in COLS) + 1; continue
    if not p.get('done'):
        if r == 'heading':
            if open_list: out.append(f'</{open_list}>'); open_list = None
            sid = re.sub(r'[^a-z0-9]+', '-', p['text'].lower()).strip('-'); toc.append((sid, p['text']))
            out.append(f'@@SECTION@@{sid}@@<h2>{seg_html(p["segs"])}</h2>')   # 22 Oct 2026 (user 22:26, "1"; 2.1.2): a heading keeps Word's links (was its plain text)
        elif r == 'quote':
            # 20 Oct (5.3 "Let us always remember..."): an attribution Word puts in the quotation's own paragraph, after a line
            # break ("...present."  /  - Maria Montessori, ...), is the attribution line
            qs, cs_ = list(p['segs']), []
            full = ''.join(x[0] for x in qs); m_ = re.search(r'\n[\t ]*[-‐-―]\s', full)
            if m_:
                cut = m_.start(); acc = 0
                for ix, sg in enumerate(qs):
                    if acc + len(sg[0]) > cut:
                        a_, b_ = sg[0][:cut - acc], sg[0][cut - acc:].lstrip('\n').lstrip('\t ')
                        cs_ = ([tuple([b_] + list(sg[1:]))] if b_ else []) + qs[ix + 1:]; qs = qs[:ix] + ([tuple([a_] + list(sg[1:]))] if a_ else [])
                        while cs_ and not cs_[0][0].strip(): cs_ = cs_[1:]
                        if cs_: cs_[0] = tuple([cs_[0][0].lstrip('\t ')] + list(cs_[0][1:]))
                        break
                    acc += len(sg[0])
            q = seg_html(qs, strip_italic=True)
            c = f'<cite>{seg_html(cs_)}</cite>' if cs_ else ''
            if not c and k + 1 < len(paras) and paras[k + 1].get('role') == 'cite':
                cp = paras[k + 1]; ct = seg_html(cp['segs'])
                if cp['num'] and cp['num'][1] == 'bullet': ct = '- ' + ct
                c = f'<cite>{ct}</cite>'; cp['done'] = True
            if p.get('float_in'): emit('<div class="photo-row ext-float">' + figure(p['float_in']) + '</div>')
            emit(f'<blockquote class="pullquote{" beside-photo" if p.get("float_in") or p.get("beside_float") else ""}"><p>{q}</p>{c}</blockquote>')
        elif r == 'cite':
            emit(f'<p>{seg_html(p["segs"])}</p>')
        elif r in ('ol', 'ul'):
            # 20 Oct 2026: a different Word numbered list starts its own list (5.4: i-iii inside 1-4 were counted as 2-4)
            if open_list != r or (r == 'ol' and open_num != p['num'][0]):
                if open_list: out.append(f'</{open_list}>')
                # 30 Sept (3.1.1): a Word numbered list that resumes after a bulleted list keeps counting, as in Word
                st = ol_count.get(p['num'][0], 0) if r == 'ol' else 0
                fm = {'lowerRoman': ' class="mm-lroman"', 'upperRoman': ' class="mm-uroman"', 'lowerLetter': ' class="mm-lalpha"', 'upperLetter': ' class="mm-ualpha"'}.get(p['num'][1], '') if r == 'ol' else ''
                out.append(f'<{r}{fm} start="{st + 1}" style="counter-reset:mmn {st}">' if st else f'<{r}{fm}>'); open_list = r   # the page numbers lists with a CSS counter
                open_num = p['num'][0] if r == 'ol' else None
            if r == 'ol': ol_count[p['num'][0]] = ol_count.get(p['num'][0], 0) + 1
            out.append(para_html(p))
        elif r in ('p', 'label', 'table'):
            emit(para_html(p))
    for g in rows_after.get(k, []): emit(row_html(g))
    k += 1
if open_list: out.append(f'</{open_list}>')

# sections
body = ''.join(out)
parts = body.split('@@SECTION@@')
sec_html = []
if parts[0].strip(): sec_html.append(f'<section class="section">{parts[0]}</section>')
for part in parts[1:]:
    sid, rest = part.split('@@', 1); sec_html.append(f'<section class="section" id="{sid}">{rest}</section>')

# ------------------------------------------------------------------ into the frame
def tok(m): kk = f'__IMG{len(store)}__'; store[kk] = m.group(0); return kk
fr = BeautifulSoup(re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+', tok, open(frame_path, encoding='utf-8').read()), 'html.parser')
fm = fr.select_one('main'); fm.clear(); fm.append(BeautifulSoup(''.join(sec_html).replace('\t', '␉'), 'html.parser'))   # 20 Oct 2026: tabs kept through BeautifulSoup (4.15 turned a tab-only text into one space)
fr.title.string = f'{title_menu} | Montessori Mentor'
h1 = fr.select_one('.hero h1'); h1.clear(); t0 = title or title_menu
if ': ' in t0:
    a0, b0 = t0.split(': ', 1); sp = fr.new_tag('span'); sp.string = b0; h1.append(sp); sub = fr.new_tag('span', attrs={'class': 'sub'}); sub.string = a0; h1.append(sub)
else:
    sp = fr.new_tag('span'); sp.string = t0; h1.append(sp)
grid = fr.select_one('nav.toc .toc-grid'); grid.clear(); ul = fr.new_tag('ul', attrs={'class': 'toc-essays'})
for sid, t in toc:
    li = fr.new_tag('li'); a = fr.new_tag('a', href='#' + sid); a.string = t; li.append(a); ul.append(li)
grid.append(ul)
for a in fr.select('nav .panel a[aria-current]'): del a['aria-current']
for a in fr.select('nav .panel a'):
    if a.get('href') == href: a['aria-current'] = 'page'
_li = next((a.find_parent('li', class_='has-panel') for a in fr.select('nav .panel a[aria-current]')), None)   # 4 Oct (chat 10): the top item of the panel
if _li is not None:                                                                                          # holding this page is the active one
    for a in fr.select('nav a.top[aria-current]'): del a['aria-current']
    _li.find('a', class_='top')['aria-current'] = 'page'
res = str(fr)
for kk, v in store.items(): res = res.replace(kk, v)
res = res.replace('​', '').replace('␉', '\t')   # 2 Oct (20th chat): Word's zero-width spaces (3.6.1 'Fine Motor Skills') - invisible, but they break every text match
open(out_path, 'w', encoding='utf-8').write(res)

roles = {}
for p in paras: roles[p.get('role')] = roles.get(p.get('role'), 0) + 1
log.append(f'Title (hero): {title}')
log.append('Paragraphs: ' + ', '.join(f'{v} {k}' for k, v in sorted(roles.items(), key=lambda x: str(x[0]))))
log.append(f"Photo groups from the PDF: {sum(1 for g in groups if not g['beside'])} rows, "
           f"{sum(1 for g in groups if g['beside'] and len(g['photos']) > 1)} sets beside text, {sum(1 for g in groups if g['beside'] and len(g['photos']) == 1)} floated singles")
log.append(f'Photos: {len(order)} ({nblur} from blurred working copies); sections: {len(toc)}; turned as in Word: {sorted(TURN)}')
json.dump(dict(groups=groups, roles={i: p.get('role') for i, p in enumerate(paras)}, texts={i: p['text'][:80] for i, p in enumerate(paras) if p['kind'] == 'p'}),
          open(out_path + '.json', 'w'), indent=0, default=str)
print('\n'.join(log))
