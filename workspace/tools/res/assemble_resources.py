"""Resources pages: Word -> template source page (24 Sept).
Reads the Word document with build_pages.convert (your colour conventions), then places the content in the frame of an
approved page (menu, hero photo, contents box, scripts), so site/make_page.py can apply the template rules.
  green  -> section heading (and a Contents entry)     red   -> source (styled as a material name)
  blue   -> title, italic, with year and PDF badges      plain -> description; numbered lines -> numbered list
  italic -> quotation, with its attribution               lone picture -> photo floated beside the text; several -> a row
Page-specific placements (a photo moved to the entry the PDF shows it beside, a numbered list Word did not mark)
go in the page's settings file, not here.
Usage: python3 site/assemble_resources.py resources.docx site/pages/frame.html out.html <link of this page> "<page title>"
"""
import sys as _sys, os as _os, subprocess as _sp
# OA1 (7 Oct 2026, chat 22 - your order of work: "let's do them one by one, as I still need to check
# each"): one page built between your messages; qa/one_at_a_time.py refuses the second.
_q = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "qa", "one_at_a_time.py")
if _os.path.exists(_q) and len(_sys.argv) > 1:
    _r = _sp.run([_sys.executable, _q, "touch", _os.path.basename(_sys.argv[1])], capture_output=True, text=True)
    if _r.returncode: _sys.exit((_r.stdout + _r.stderr).strip())
import re, sys, io, base64
from bs4 import BeautifulSoup, NavigableString
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import build_pages as bp

docx_path, frame_path, out_path, href, title = sys.argv[1:6]
import docx_clean   # 27 Sept: hidden text out, field links made ordinary links
_m, _h = docx_clean.clean(docx_path, '/tmp/_res_clean.docx'); docx_path = '/tmp/_res_clean.docx'
print(f'Word clean-up: {_m} field links made links, {_h} hidden runs removed.')
raw = '/tmp/_res_raw.html'
info = bp.convert(docx_path, 'Curriculum', raw)
store = {}
def tok(m): k = f'__IMG{len(store)}__'; store[k] = m.group(0); return k
rs = BeautifulSoup(re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+', tok, open(raw, encoding='utf-8').read()), 'html.parser')
fr = BeautifulSoup(re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+', tok, open(frame_path, encoding='utf-8').read()), 'html.parser')
m = rs.select_one('main'); log = []

def img_fig(fig):     # the template reads each photo's shape from its box
    im = fig.select_one('img'); ar = float(re.search(r'--ar:([0-9.]+)', fig['style']).group(1))
    fig['class'] = ['ph', 'landscape' if ar >= 1 else 'portrait']
    fig['style'] = f'--h:180;--hg:180;--hp:180;--ar:{ar:.5f}'
    fig.select_one('.pim')['style'] = f'aspect-ratio:{ar:.5f}'
    return fig
def entry(src_text):
    for e in m.select('div.res-entry'):
        if e.select_one('.res-src').get_text(strip=True) == src_text: return e
    raise AssertionError(src_text)
def floated(name): return m.find('img', attrs={'data-name': name}).find_parent('div', class_='side-photo')

# ---- placements from the PDF: moving a photo to the entry the PDF shows it beside is done in the page's settings
#      (site/pages/<page>_settings.py, adjust()), so this converter stays general.
# rows: left to right as positioned in Word (the file order is not the order on the page)
import zipfile
x = zipfile.ZipFile(docx_path).read('word/document.xml').decode('utf-8')
rel = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', zipfile.ZipFile(docx_path).read('word/_rels/document.xml.rels').decode('utf-8')))
pos = {}
for d in re.findall(r'<w:drawing>(.*?)</w:drawing>', x, re.S):
    rid = re.search(r'r:embed="(rId\d+)"', d); off = re.search(r'<wp:positionH[^>]*>\s*<wp:posOffset>(-?\d+)<', d)
    if rid and off and rid.group(1) in rel: pos[rel[rid.group(1)]] = int(off.group(1))
for r0 in m.select('div.photo-row:not(.side-photo)'):
    figs = r0.select('figure'); order = sorted(figs, key=lambda f: pos.get(f.select_one('img')['data-name'], 0))
    for f in order: r0.append(f.extract())
log.append('Rows in their left-to-right order in Word.')
# ---- the frame's markup
for bq in m.select('blockquote.mq'):
    bq['class'] = ['pullquote']
    for qp in bq.select('p'):                     # a page reference after the closing quotation mark stays upright, as in Word
        h = str(qp); k = h.rfind('”')
        if k > 0:
            tail = re.sub(r'<[^>]+>', '', h[k + 1:]).strip()
            if re.fullmatch(r'p\.\s*\d+\.?', tail):
                last = [t for t in qp.find_all(string=True) if tail.split()[0] in t][-1]
                sp = rs.new_tag('span', attrs={'class': 'q-ref'}); sp.string = ' ' + tail
                for t in list(qp.find_all(string=True)):
                    if t is last or (t.find_previous(string=True) is not None and False): pass
                par = last.parent if last.parent.name == 'em' else None
                (par or last).replace_with(sp)
    for c in bq.select('cite'):
        t = c.get_text(strip=True)
        if not t.startswith('–'):
            c.clear(); c.append('– ' + re.sub(r'^[-\u2010-\u2014]\s*', '', t))
for e in m.select('div.res-entry'):
    s = e.select_one('.res-src'); h = rs.new_tag('h3', attrs={'class': 'material-name res-src'}); h.extend(list(s.contents)); s.replace_with(h)
for d in m.select('div.side-photo'):
    d['class'] = ['photo-row', 'single', 'ext-float', 'spaced']; img_fig(d.select_one('figure'))
for d in m.select('div.photo-row:not(.ext-float)'):
    d['class'] = ['photo-row', 'pr-justify', 'spaced']
    for f in d.select('figure'): img_fig(f)
# sections: an opening one without a heading, then one per heading
body = BeautifulSoup('', 'html.parser'); sec = rs.new_tag('section', attrs={'class': 'section'}); secs = [sec]; toc = []
for el in list(m.children):
    if getattr(el, 'name', None) == 'h2':
        sid = el.get('id') or bp.slug(el.get_text()); del el['class']; el.attrs.pop('id', None)
        sec = rs.new_tag('section', attrs={'class': 'section', 'id': sid}); secs.append(sec); toc.append((sid, el.get_text(strip=True)))
    sec.append(el.extract())

# ---- into the frame
fm = fr.select_one('main'); fm.clear()
for s in secs:
    if s.contents: fm.append(s)
fr.title.string = f'{title} | Montessori Mentor'
h1 = fr.select_one('.hero h1'); h1.clear(); sp = fr.new_tag('span'); sp.string = title; h1.append(sp)
grid = fr.select_one('nav.toc .toc-grid'); grid.clear(); ul = fr.new_tag('ul', attrs={'class': 'toc-essays'})
for sid, t in toc:
    li = fr.new_tag('li'); a = fr.new_tag('a', href='#' + sid); a.string = t; li.append(a); ul.append(li)
grid.append(ul)
for a in fr.select('nav .panel a[aria-current]'): del a['aria-current']       # the menu bar keeps Curriculum as current
for a in fr.select('nav .panel a'):
    if a.get('href') == href: a['aria-current'] = 'page'
out = str(fr)
for k, v in store.items(): out = out.replace(k, v)
open(out_path, 'w', encoding='utf-8').write(out)
print(info); print('\n'.join(log)); print(f'{len(secs)} sections, Contents: ' + ', '.join(t for _, t in toc))
