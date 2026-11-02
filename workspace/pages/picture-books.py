# 8.3 Picture Books - page settings (2 Nov 2026, Resources Code Template f0bac9f8)
# Word file: 8.3 Picture Books.docx (Drive 1myTm7zv6IX7xQFJYzWVR0Z1KjyAHlV8W, saved 1 Nov 14:09, sha256 ef4ea8d5...); PDF 83ae0c07...
# Owner 2 Nov 08:44: address /picture-books/. 2 Nov 08:52: no faces to be blurred. 2 Nov 09:50: "8.3".
# First build (raw converter output) faults: red organisations and blue titles made headings (sections), Word colours as inline
# styles, a 2167 px runaway margin at 1440, text over the cover rows at 320-610 px, text over text at 360-470 and 390 px.
# So, as on 8.1 (owner 31 Oct 22:34-22:37: lists in the Resources template's entry style, as the live Culture Resources page),
# the text area is rebuilt from the Word file in the template's own entry style: each organisation a red source line
# (h3.material-name.res-src) opening an entry (div.res-entry); each blue title a res-item (blue title, PDF badges); the text
# under them res-desc; the green headings h2; Word's line pictures beige lines; the images the converter made from Word
# (two images beside text, three rows of covers/hornbooks) kept and put back at their place in Word.
import re, os, sys, runpy

_H = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books-by-montessori.py'))
_runs, _pieces_html, _esc, _res_item = _H['_runs'], _H['_pieces_html'], _H['_esc'], _H['_res_item']
BLUES, REDS = _H['BLUES'], _H['REDS']
GREENS = ('00B050',)

NO_TOC = True


def _share(pcs, cols):
    tot = sum(len(t.strip()) for t, c, it, h, s in pcs if t not in ('\t', '\n'))
    hit = sum(len(t.strip()) for t, c, it, h, s in pcs if t not in ('\t', '\n') and c in cols)
    return hit / tot if tot else 0


def _word():
    import docx
    from docx.oxml.ns import qn
    a = sys.argv; f = a[a.index('--docx') + 1]
    return docx.Document(f), qn


def POST_MAIN(main, s, report):
    from bs4 import BeautifulSoup
    D, qn = _word()
    import io
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    rel = {r.rId: r for r in D.part.rels.values() if 'image' in r.reltype}

    def kind_of_images(p):
        ids = [x for x in re.findall(r'r:(?:embed|id)="(rId\d+)"', p._p.xml) if x in rel]
        lines = photos = 0
        for x in ids:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            try:
                w, h = Image.open(io.BytesIO(rel[x].target_part.blob)).size
            except Exception:
                w, h = 1000, 1000
            if h <= 4 and w >= 300: lines += 1
            else: photos += 1
        return lines, photos

    floats = [x.extract() for x in main.select('div.mm-float')]
    rows = [x.extract() for x in main.select('div.mm-row')]
    if len(floats) > 1: floats[1]['class'] = floats[1].get('class', []) + ['mm-left']
    report.append(('settings', 'the Victorian Web "A" image on the left, as Word and the PDF (template .mm-float.mm-left)', ''))
    for f in floats:
        for e in [f] + f.find_all(True):
            if e.has_attr('data-side'): del e['data-side']   # the template does not read it (code check)
    for f in floats + rows:
        for fig in f.find_all('figure', style=True):   # --h is not read by the template (--hp is)
            fig['style'] = ';'.join(x for x in fig['style'].split(';') if x.strip() and not x.strip().startswith('--h:'))
    report.append(('settings', 'images from the converter kept: %d beside text, %d rows' % (len(floats), len(rows)), ''))
    fi = ri = 0

    out = []; entry = None   # entry: list of html parts of the open res-entry

    def close():
        nonlocal entry
        if entry is not None: out.append('<div class="res-entry">%s</div>' % ''.join(entry)); entry = None

    def add(h):
        (entry if entry is not None else out).append(h)

    paras = D.paragraphs
    in_list = []
    for i, p in enumerate(paras):
        if i == 0: continue   # the title (the hero)
        pcs = _runs(p, qn)
        txt = ''.join(x[0] for x in pcs).strip()
        lines, photos = kind_of_images(p)
        num = p._p.find('.//' + qn('w:numPr')) is not None
        if in_list and not num:
            add('<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in in_list)); in_list = []
        if photos:
            if txt and photos == 1 and fi < len(floats):   # an image beside its paragraph (Word anchors it there)
                add(str(floats[fi])); report.append(('settings', 'image beside text %d placed at Word paragraph %d' % (fi + 1, i), '')); fi += 1
            elif photos > 1 and ri < len(rows):
                # a row of covers between Word's two lines: the row in an entry of its own (on the live Resources pages a row is
                # always inside a res-entry; a line straight after a bare row is pulled up over it by the template's spacing)
                close()
                if lines: out.append('<div class="beige-rule mm-org-rule"></div>')
                out.append('<div class="res-entry">%s</div>' % str(rows[ri])); report.append(('settings', 'row %d of images placed at Word paragraph %d' % (ri + 1, i), '')); ri += 1
            elif photos == 1 and fi < len(floats):
                add(str(floats[fi])); fi += 1
            if not txt: continue
        elif lines and not txt:
            close(); out.append('<div class="beige-rule mm-org-rule"></div>'); continue
        if not txt: continue
        if num:
            in_list.append(_pieces_html(pcs).replace('<span class="mm-blue">', '').replace('</span>', '')); continue
        green, red, blue = _share(pcs, GREENS), _share(pcs, REDS), _share(pcs, BLUES)
        first = next((x for x in pcs if x[0].strip()), None)
        if green > 0.6:
            close(); out.append('<h2 class="mm-hc-00B050">%s</h2>' % _strip_col(_pieces_html(pcs))); continue
        if red > 0.5 or (first is not None and first[1] in REDS and red > 0.3):
            close(); entry = []
            body, badges = _split_badges(pcs)
            entry.append('<h3 class="material-name res-src">%s%s</h3>' % (_strip_col(_pieces_html(body)), ''.join(' ' + b for b in badges)))
            continue
        if '\t' in txt and first is not None and first[1] in BLUES and not first[3] and _plain(pcs).split('\t')[0].strip() and 'PDF' not in _plain(pcs).split('\t', 1)[1]:
            lab, rest = _split_tab(pcs)   # a blue label, a tab, then its text (Learning to Read ...)
            add('<p class="mm-hanglab"><span class="mm-lab"><span class="mm-blue">%s</span> </span>%s</p>' % (_strip_col(_pieces_html(lab)), _pieces_html(rest)))
            continue
        if blue > 0.5:
            add(re.sub(r'<span class="res-title"><em>(.*?)</em></span>', r'<span class="res-title">\1</span>', _res_item(pcs), count=1)); continue   # titles upright, as Word (8.1's were italic)
        if p.runs and all((r.font.underline or not r.text.strip()) for r in p.runs) and not any(x[3] for x in pcs):
            add('<p class="mm-ul"><u>%s</u></p>' % _pieces_html(pcs)); continue   # the <u> as the converter writes it (build_page.py 20 Oct rule); the template underlines nothing by class
        cls = ' class="res-desc"' if entry is not None else ''
        add('<p%s>%s</p>' % (cls, _tabbed(pcs)))
    if in_list: add('<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in in_list))
    close()
    assert fi == len(floats) and ri == len(rows), (fi, len(floats), ri, len(rows))
    main.clear()
    main.append(BeautifulSoup('<section class="section">%s</section>' % ''.join(out), 'html.parser'))
    for a in main.find_all('a'):
        if re.sub(r'\s+', ' ', a.get_text()).strip() == 'PDF' and 'pdf' not in (a.get('class') or []): a['class'] = (a.get('class') or []) + ['pdf']
    report.append(('settings', 'text area rebuilt from Word in the template\'s entry style (as 8.1 and Culture Resources): %d entries' % len(main.select('div.res-entry')), ''))


def _plain(pcs): return ''.join(x[0] for x in pcs)


def _tabbed(pcs):
    # Word tabs in an ordinary paragraph: the template's 24 px spacer (span.mm-lsp), so linked words on either side of a tab
    # do not run together ("2 to 4 4 to 6") and the groups after "lists for:" stay apart (fault list 22, 23, 37)
    parts = []; cur = []
    for x in pcs:
        if x[0] == '\t':
            parts.append(cur); cur = []
        else: cur.append(x)
    parts.append(cur)
    hs = [_pieces_html(c) for c in parts]
    return '<span class="mm-lsp"> </span>'.join(h for h in hs if h.strip()) if len(hs) > 1 else hs[0]


def _strip_col(h): return re.sub(r'<span class="(mm-blue|mm-hc-EE0000)">(.*?)</span>', r'\2', h)


def _split_badges(pcs):
    body = []; badges = []; i = 0
    while i < len(pcs):
        t, c, it, href, sup = pcs[i]
        if href:
            j = i; acc = ''
            while j < len(pcs) and pcs[j][3] == href: acc += pcs[j][0]; j += 1
            if acc.strip() == 'PDF':
                badges.append('<a class="pdf" href="%s" rel="noopener" target="_blank">PDF</a>' % _esc(href)); i = j; continue
        if t == '\t': i += 1; continue
        body.append(pcs[i]); i += 1
    return body, badges


def _split_tab(pcs):
    lab = []; rest = []; seen = False
    for x in pcs:
        if x[0] == '\t': seen = True; continue
        (rest if seen else lab).append(x)
    return lab, rest
