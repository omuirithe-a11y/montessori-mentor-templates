#!/usr/bin/env python3
"""The one proof script every agent runs, unedited (27 Oct 2026, checks-v9: a PDF image box is matched to the live one by its image file name (with or without -480/-960), not by data-name, which the cleaning removes; checks-v8: PDF-placed image boxes keep the live inline size, compared element for element; v9 14:4x: part 5 shows each changed word in its sentence; part 6 flags names in descriptions that the page text does not contain; v8 13:5x: the code-only formatting part 9 is removed - it could not see colours set by a page's own styles, so it both missed and invented changes; format_check.py, which compares what the browser shows, is the formatting proof).
usage: python3 strip_compare.py <template.html> <finished package .zip, or its index.html> <live index.html>
Run it on the ZIP you will hand over: the zip is unpacked to a fresh folder and that copy is what is checked.
Prints 6 parts. The page is acceptable only if parts 1-4 each end in OK; parts 5-6 list every allowed change for the owner."""
import sys, re, difflib, html
from bs4 import BeautifulSoup
import hashlib, os
TPL, PAGE, LIVE = sys.argv[1:4]
if PAGE.endswith('.zip'):
    import zipfile, tempfile
    tmp = tempfile.mkdtemp(prefix='sc-'); zipfile.ZipFile(PAGE).extractall(tmp)
    import atexit, shutil; atexit.register(shutil.rmtree, tmp, True)   # v7: the unpacked copy is deleted when the check ends (copies filled the disk on 27 Oct)
    found = [os.path.join(r, 'index.html') for r, d, f in os.walk(tmp) if 'index.html' in f]
    assert len(found) == 1, 'STOP: the zip must hold exactly one folder with one index.html'
    print('checking the copy unpacked from', PAGE); PAGE = found[0]
    top = {n.split('/')[0] for n in zipfile.ZipFile(sys.argv[2]).namelist() if n.strip('/')}
    slug = os.path.basename(os.path.dirname(os.path.abspath(LIVE)))
    assert top == {slug}, 'STOP: the zip must hold one folder named %s (the live page\'s folder); it holds %s' % (slug, sorted(top))
    print('zip folder name:', slug, '- matches the live page')
H = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()
FIX = {'Essay Code Template.html': 'aa5d50394f2dabd8b67e40b79b64f93f6f10e031bcc7d2eeb114d0025e56c2fb',
       'Resources Code Template.html': '44a6b6241d99f4d8ba834e67bf47704308bbe5e8215e226ab534f13dbc0bbf95'}
assert os.path.basename(TPL) in FIX and H(TPL) == FIX[os.path.basename(TPL)], 'STOP: the template is not the template pinned 1 Nov 21:0x (sha256 2cbb78e3)'
assert H('/home/claude/reports/copy-protection.html') == '0d180ad65627bb99f5edd29c476727c29d68a34efccd4ab5fd8f64a777026ce4', 'STOP: copy-protection.html has been changed'
print('template and copy protection fingerprints: correct')
PROT = open('/home/claude/reports/copy-protection.html', encoding='utf-8').read()
P_STYLE = re.search(r'<style id="mm-protect">.*?</style>', PROT, re.S).group(0)
P_JS = re.search(r'<script id="mm-protect-js">.*?</script>', PROT, re.S).group(0)
PROTECT = re.compile(r'<style id="mm-protect">.*?</style>|<script id="mm-protect-js">.*?</script>', re.S)
def lines(s): return [l.rstrip() for l in re.sub(r'>\s*<', '>\n<', str(s)).splitlines() if l.strip()]
def strip(raw):
    s = BeautifulSoup(PROTECT.sub('', raw), 'html.parser')
    if s.title: s.title.string = ''
    h = s.select_one('.hero h1')
    if h: h.clear()
    hero = s.select_one('.hero')
    if hero and hero.get('style'): hero['style'] = re.sub(r"url\([^)]*\)", 'url()', hero['style'])
    for ul in s.select('nav.toc ul'): ul.clear()
    for li in s.select('.menu li'): li.decompose()      # menu markup kept, link entries removed
    main = s.select_one('main#content')
    if main:
        for ch in list(main.children):
            if getattr(ch, 'name', None) != 'script': ch.extract()
    return s
traw, praw, lraw = (open(f, encoding='utf-8').read() for f in (TPL, PAGE, LIVE))
TCODE = re.sub(r'<!--.*?-->', ' ', traw, flags=re.S)
TCODE = re.sub(r'/\*.*?\*/', ' ', TCODE, flags=re.S)
TCODE = re.sub(r'(?m)(?<![:"\'\\])//[^\n]*', ' ', TCODE)      # template comments do not count as the template using a name
TREAD = set(re.findall(r"getPropertyValue\('(--[\w-]+)'\)|var\((--[\w-]+)", TCODE)) ; TREAD = {a or b for a, b in TREAD}
ok = True
# 1. everything outside the slots, menu markup included
d = list(difflib.unified_diff(lines(strip(traw)), lines(strip(praw)), 'template', 'page', n=0, lineterm=''))
print('== 1. CODE OUTSIDE THE SLOTS'); print('\n'.join(d))
print('OK' if not d else 'FAULT: %d lines differ' % sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---'))); ok &= not d
# 2. copy protection, byte for byte, once each, in place
c1, c2 = praw.count(P_STYLE), praw.count(P_JS)
inplace = praw.find(P_STYLE) < praw.find('</head>') and 0 < praw.find(P_JS) < praw.rfind('</body>')
print('== 2. COPY PROTECTION'); r = c1 == 1 and c2 == 1 and inplace and len(PROTECT.findall(praw)) == 2
print('OK' if r else 'FAULT: style %d, script %d, in place %s' % (c1, c2, inplace)); ok &= r
# 3. every class, data- attribute and inline style property inside main must be read by the template (whole-word match)
ps = BeautifulSoup(praw, 'html.parser'); pm = ps.select_one('main#content')
def known(tok): return re.search(r'(?<![\w-])' + re.escape(tok) + r'(?![\w-])', TCODE) is not None
FORBID = ['script', 'style', 'link', 'iframe', 'object', 'embed', 'form', 'input', 'meta', 'base', 'svg']
bad = set(); kept = []
# v8 (27 Oct 18:2x): PDF-placed images (div.mm-pdf boxes) take their size and place from the owner's PDF; the build writes them as inline
# styles, which the template's CSS needs. They are content, so they must equal the live page's, element for element.
norm = lambda st: ';'.join(x.strip().replace(' ', '') for x in (st or '').split(';') if x.strip())
def _pdfmap(raw):
    m = {}
    for box in BeautifulSoup(raw, 'html.parser').select('main#content div.mm-pdf'):
        names = ','.join(re.sub(r'-(480|960)(?=\.\w+$)', '', os.path.basename(i.get('data-full') or i.get('src') or '')) for i in box.find_all('img'))
        for k, e in enumerate([box] + box.find_all(True)):
            m[(names, k)] = norm(e.get('style'))
    return m
LIVEPDF = _pdfmap(lraw)
_pk = {}
for box in BeautifulSoup(praw, 'html.parser').select('main#content div.mm-pdf'):
    pass
def PDFKEY(el):
    box = el if ('mm-pdf' in el.get('class', []) and el.name == 'div') else el.find_parent('div', class_='mm-pdf')
    if box is None: return None
    names = ','.join(re.sub(r'-(480|960)(?=\.\w+$)', '', os.path.basename(i.get('data-full') or i.get('src') or '')) for i in box.find_all('img'))
    k = ([box] + box.find_all(True)).index(el)
    return (names, k)
def PDFSTYLE(el):
    k = PDFKEY(el)
    if k is None: return None
    return LIVEPDF.get(k, '')
TM = BeautifulSoup(traw, 'html.parser').select('.menu li')
TM_TAGS = {e.name for li in TM for e in [li] + li.find_all(True)}
TM_ATTRS = {a for li in TM for e in [li] + li.find_all(True) for a in e.attrs}
for li in ps.select('.menu li'):            # menu entries: only the tags and attributes the template's own menu entries have
    for e in [li] + li.find_all(True):
        if e.name not in TM_TAGS: bad.add('menu element <%s> (not in the template menu)' % e.name)
        for a in e.attrs:
            if a not in TM_ATTRS and not (a == 'aria-current' and e.get(a) == 'page'): bad.add('menu attribute %s (not in the template menu)' % a)
        if e.get('style'): bad.add('menu inline style on <%s>' % e.name)
_t = BeautifulSoup(traw, 'html.parser'); _tm = _t.select_one('main#content')
FRAME = {c for e in _t.find_all(True) if not (_tm and (e is _tm or _tm in e.parents)) for c in e.get('class', [])} - {c for e in (_tm.find_all(True) if _tm else []) for c in e.get('class', [])}
TIDS = {e.get('id') for e in _t.find_all(True) if e.get('id') and not (_tm and _tm in e.parents)}
for el in pm.find_all(True):
    for c in el.get('class', []):
        if c in FRAME: bad.add('class %s inside the content (the template uses it only for the page frame: hero, menu, contents, footer)' % c)
    if el.get('id') in TIDS: bad.add('id %s inside the content (the template already has that id)' % el.get('id'))
zones = [pm] + ps.select('nav.toc ul') + ps.select('.hero h1')
els = [e for z in zones for e in ([z] + z.find_all(True))]
for el in els:
    if el.name in FORBID and not (el.name == 'script' and el.parent is pm): bad.add('element <%s> inside the content' % el.name)
    for c in el.get('class', []):
        if not known(c): bad.add('class ' + c)
    for a, v in el.attrs.items():
        if a.startswith('data-'):
            if not known(a): bad.add('attribute ' + a)
            elif re.search(r'data-(h|scale|column|match|likerows|gaps|hscale|row-h|crop|rot|w)$', a): kept.append('%s="%s" on <%s class="%s">' % (a, v, el.name, ' '.join(el.get('class', []))))
        elif a == 'start' and el.name == 'ol' and v.isdigit(): kept.append('start="%s" on <ol> (a list that continues; the template reads it, 27 Oct)' % v)
        elif a not in ('class', 'style', 'id', 'src', 'srcset', 'alt', 'href', 'width', 'height', 'colspan', 'rowspan', 'loading', 'target', 'rel', 'title', 'aria-label', 'aria-hidden', 'role', 'sizes'):
            bad.add('attribute ' + a)
    if PDFSTYLE(el) is not None:   # v8: a PDF-placed image box keeps the size and place the build gave it from the PDF, exactly as on the live page
        if PDFSTYLE(el) != norm(el.get('style')): bad.add('PDF-placed image box <%s class="%s"> for %s: inline style differs from the live page' % (el.name, ' '.join(el.get('class', [])), PDFKEY(el)))
        continue
    for decl in (el.get('style') or '').split(';'):
        prop = decl.split(':')[0].strip()
        if not prop: continue
        if prop.startswith('--'):
            if prop not in TREAD: bad.add('inline style %s (the template never reads it)' % prop)
        elif not (prop == 'aspect-ratio' and 'pim' in el.get('class', [])): bad.add('inline style %s on <%s class="%s">' % (prop, el.name, ' '.join(el.get('class', []))))
tmenu = BeautifulSoup(traw, 'html.parser').select('.menu li')
tli = {c for li in tmenu for e in [li] + li.find_all(True) for c in e.get('class', [])}
for li in ps.select('.menu li'):
    for e in [li] + li.find_all(True):
        for c in e.get('class', []):
            if c not in tli: bad.add('menu class %s (not on the template\'s menu entries)' % c)
mh = {a.get('href') for a in ps.select('.menu a[href]')}; lh = {a.get('href') for a in BeautifulSoup(lraw, 'html.parser').select('.menu a[href]')}
if mh != lh: bad.add('menu links differ from the live page: missing %s, extra %s' % (sorted(lh - mh), sorted(mh - lh)))
print('menu: %d distinct links' % len(mh))
print('== 3. CONTENT CLEANED'); print('\n'.join(sorted(bad)))
print('OK' if not bad else 'FAULT: %d items the template does not use' % len(bad)); ok &= not bad
print('-- size settings kept (listed for the owner):'); print('\n'.join(kept) or 'none')
# 4. main's own attributes
tm = BeautifulSoup(traw, 'html.parser').select_one('main#content')
r = dict(tm.attrs) == dict(pm.attrs)
print('== 4. MAIN ATTRIBUTES'); print('OK' if r else 'FAULT: template %s page %s' % (dict(tm.attrs), dict(pm.attrs))); ok &= r
# 5. every change from the live page: words, links, descriptions, images
def facts(raw):
    s = BeautifulSoup(raw, 'html.parser'); m = s.select_one('main#content')
    head = [(s.title.get_text() if s.title else ''), (s.select_one('.hero h1').get_text(' ', strip=True) if s.select_one('.hero h1') else '')] + [a.get_text(' ', strip=True) for a in s.select('nav.toc a')]
    for x in m.find_all(['script', 'style']): x.decompose()
    words = re.sub(r'\s+', ' ', m.get_text(' ')).strip().split(' ')
    links = [(a.get_text(' ', strip=True), a.get('href')) for a in m.find_all('a')]
    imgs = [(i.get('src'), i.get('alt')) for i in m.find_all('img')]
    return head + words, links, imgs
lw, ll, li_ = facts(lraw); pw, pl, pi = facts(praw)
print('== 5. WORDS CHANGED FROM THE LIVE PAGE')
for op in difflib.SequenceMatcher(None, lw, pw, autojunk=False).get_opcodes():
    if op[0] != 'equal': print('%s: "%s" -> "%s"\n   live: ...%s...\n   page: ...%s...' % (op[0], ' '.join(lw[op[1]:op[2]]), ' '.join(pw[op[3]:op[4]]), ' '.join(lw[max(0, op[1] - 10):op[2] + 10]), ' '.join(pw[max(0, op[3] - 10):op[4] + 10])))
print('== 6. LINKS, IMAGES AND DESCRIPTIONS CHANGED')
for x in difflib.unified_diff([repr(x) for x in ll], [repr(x) for x in pl], 'live links', 'page links', n=0, lineterm=''): print(x)
for x in difflib.unified_diff([str(x[0]) for x in li_], [str(x[0]) for x in pi], 'live images', 'page images', n=0, lineterm=''): print(x)
print('descriptions:'); [print(s, '->', a) for s, a in pi]
ptext = ' '.join(pw)
nm = []
for src, a in pi:
    for w in re.findall(r"(?<!^)(?<![.!?] )\b([A-Z][a-z\u00C0-\u017F'’]+(?:\s+[A-Z][a-z\u00C0-\u017F'’]+)*)", a or ''):
        if w.split()[0] in ('A', 'An', 'The', 'Two', 'Three', 'Four', 'Five', 'Montessori', 'Sensorial', 'Chinese', 'Irish', 'English'): continue
        if w not in ptext: nm.append('%s: "%s" is named in the description but not in the page text' % (src, w))
print('-- names in descriptions not found in the page text (each is a fault unless the name is printed in the image itself):')
print('\n'.join(nm) or 'none')
print('== 7. IMAGE FILES (sha256, finished folder vs live folder)')
pd, ld = os.path.dirname(PAGE), os.path.dirname(LIVE)
for src, _ in pi:
    if not src or src.startswith('http'): continue
    a, b = os.path.join(pd, src), os.path.join(ld, src)
    ha = H(a) if os.path.exists(a) else 'MISSING'; hb = H(b) if os.path.exists(b) else 'not in live folder'
    if ha != hb: print('%s: page %s live %s' % (src, ha[:16], hb[:16]))
print('(every line above must be a restored file listed in the report with its sha256 and proof, or it is a fault)')
print('== 8. FILES AND IMAGE SHAPES')
from PIL import Image
f8 = []
ps8 = BeautifulSoup(praw, 'html.parser')
hero8 = ps8.select_one('.hero'); hu = re.findall(r"url\(['\"]?([^'\")]+)", hero8.get('style', '')) if hero8 else []
if hu != ['images/hero.jpg']: f8.append('hero image is %s, must be images/hero.jpg' % hu)
refs = set(hu)
for e in ps8.find_all(True):
    for a in ('src', 'data-full', 'href'):
        v = e.get(a)
        if v and not re.match(r'^(https?:|mailto:|#|/|tel:|data:|javascript:)', v) and (a != 'href' or re.search(r'\.(jpe?g|png|gif|webp|pdf)$', v, re.I)): refs.add(v)
    for part in (e.get('srcset') or '').split(','):
        v = part.strip().split(' ')[0]
        if v and not re.match(r'^(https?:|/|data:)', v): refs.add(v)
for v in sorted(refs):
    if not os.path.exists(os.path.join(pd, v)): f8.append('missing file: ' + v)
for pim in ps8.select('main#content .pim'):
    if pim.find_parent('div', class_='mm-pdf') is not None: continue   # v9: a PDF-placed box keeps the live page's size (checked in part 3); a crop there is listed in part 8b
    m = re.search(r'aspect-ratio:\s*([0-9.]+)', pim.get('style') or ''); im = pim.find('img')
    if not im: continue
    src = im.get('data-full') or im.get('src'); fp = os.path.join(pd, src or '')
    if m and os.path.exists(fp):
        w, h = Image.open(fp).size
        if abs(float(m.group(1)) - w / h) / (w / h) > 0.01: f8.append('%s: aspect-ratio %s but the file is %dx%d (%.5f)' % (src, m.group(1), w, h, w / h))
for im in ps8.select('main#content img[width][height]'):
    fp = os.path.join(pd, im.get('data-full') or im.get('src') or '')
    if os.path.exists(fp):
        w, h = Image.open(fp).size
        if abs(int(im['width']) / int(im['height']) - w / h) / (w / h) > 0.01: f8.append('%s: width/height %s x %s but the file is %dx%d' % (im.get('src'), im['width'], im['height'], w, h))
print('\n'.join(f8)); print('OK' if not f8 else 'FAULT: %d' % len(f8)); ok &= not f8
print('-- 8b. PDF-placed images shown with a shape that differs from the file by more than 1% (kept as on the live page; listed for the owner, step 7):')
_c8 = 0
for pim in ps8.select('main#content div.mm-pdf .pim'):
    m = re.search(r'aspect-ratio:\s*([0-9.]+)', pim.get('style') or ''); im = pim.find('img')
    if not (m and im): continue
    fp = os.path.join(pd, im.get('data-full') or im.get('src') or '')
    if os.path.exists(fp):
        w, h = Image.open(fp).size
        if abs(float(m.group(1)) - w / h) / (w / h) > 0.01: _c8 += 1; print('%s: shown %s, file %dx%d (%.5f)' % (im.get('data-full') or im.get('src'), m.group(1), w, h, w / h))
print('none' if not _c8 else '%d image(s)' % _c8)
print('== RESULT:', 'ALL CHECKS OK (parts 1-4 and 8)' if ok else 'NOT ACCEPTABLE')
