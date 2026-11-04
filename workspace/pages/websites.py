# 8.4 Websites - page settings (2 Nov 2026, Resources Code Template 1a89e1c1, now d85d9d19), made from 8.3 Picture Books' settings (pages/picture-books.py)
# Word file: 8.4 Websites.docx (Drive, saved 1 Nov); the next lines describe 8.3, whose settings these were made from - 8.3 Picture Books.docx (Drive 1myTm7zv6IX7xQFJYzWVR0Z1KjyAHlV8W, saved 1 Nov 14:09, sha256 ef4ea8d5...); PDF 83ae0c07...
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

# Word and the PDF have a contents list (Word paragraphs 0-11, ending with a line picture): the template's own contents box
# ("Table of contents", owner preference) lists the green headings; Word's copy of the list is not repeated in the text.
TOC_END = 11
TOC_SPLIT = [3, 4]   # owner 2 Nov 16:22 (queued): two columns as the PDF - 3 headings on the left, 4 on the right (template 2-column rule, item 10)
TEXT_EDITS = [('theDevelopmental', 'the Developmental'), ('sectioncontains', 'section contains'), ('colleting', 'collecting'),
              ('teachings.’They', 'teachings.’ They'), ('students-and teachers-to', 'students - and teachers - to'),
              ('affiliations -including AMS and AMI- ensuring', 'affiliations - including AMS and AMI - ensuring'),
              ('‘A collaborative project', '“A collaborative project'),
              ('it has become primary U.S.', 'it has become the primary U.S.'),   # owner 2 Nov 15:37
              ('The ‘Historical journals “collects', 'The ‘Historical journals’ section “collects')]   # owner 2 Nov 15:42 (A)   # N4b: the quotation closes with ” and Word 138 opens the same quotation with “   # 8.4 build 2 review N4a   # typos (owner 27 Oct: correct all typos); Word's long dashes as spaced short dashes
# owner 26 Oct 15:57: names and words inside a quotation keep their spelling (8.4 first-build faults 8)
KEEP_SPELLING = ['offering programs', 'online training programs', 'mentoring programs', 'strong training centers', 'and behavioral qualities', 'Recognized Organ']


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
    pending_rule = False
    pend_badges = None
    blank = False   # an empty Word paragraph just before (2 Nov review: Word's blank line between entries starts a new entry)
    for i, p in enumerate(paras):
        if i <= TOC_END: continue   # Word's contents list and its line (the template's contents box lists the headings)
        if pending_rule:   # a line picture inside the text paragraph before (Word 92, after "The Little List"): the line after that paragraph
            close(); out.append('<div class="beige-rule mm-org-rule"></div>'); pending_rule = False
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
            close(); out.append('<div class="beige-rule mm-org-rule"></div>'); blank = False; continue
        if not txt:
            blank = True; continue
        was_blank, blank = blank, False
        pb, pend_badges = pend_badges, None   # a name line's badge waiting for the line straight below (owner 2 Nov 16:06)
        if lines and not photos: pending_rule = True
        if num:
            in_list.append(_pieces_html(pcs).replace('<span class="mm-blue">', '').replace('</span>', '')); continue
        green, red, blue = _share(pcs, GREENS), _share(pcs, REDS), _share(pcs, BLUES)
        first = next((x for x in pcs if x[0].strip()), None)
        if green > 0.6:
            close()
            if out and 'beige-rule' in out[-1]:   # owner 2 Nov 15:54 (queued 15:53): "Remove all dividers above these headings" (green headings)
                out.pop(); report.append(('settings', 'beige line above a green heading left out (owner 2 Nov 15:54)', txt))
            out.append('<h2 class="mm-hc-00B050">%s</h2>' % _strip_col(_pieces_html(pcs))); continue   # spacing above: the template (owner 2 Nov 16:08 "On all pages and in the template")
        if red > 0.5 or (first is not None and first[1] in REDS and red > 0.3):
            close(); entry = []
            body, badges = _split_badges(pcs)
            entry.append('<h3 class="material-name res-src">%s%s</h3>' % (_src_html(body), ''.join(' ' + b for b in badges)))
            # owner 2 Nov 16:06 (queued): "Place the PDF on the same line as the title it refers to, not on the line with the author" - a badge on
            # the name line moves to the blue title straight below it (if the next line is not a blue title, it stays on the name line)
            pend_badges = (len(entry) - 1, _src_html(body), badges) if badges else None
            continue
        if '\t' in txt and first is not None and first[1] in BLUES and not first[3] and _plain(pcs).split('\t')[0].strip() and 'PDF' not in _plain(pcs).split('\t', 1)[1]:
            lab, rest = _split_tab(pcs)   # a blue label, a tab, then its text (Learning to Read ...)
            add('<p class="mm-hanglab"><span class="mm-lab"><span class="mm-blue">%s</span> </span>%s</p>' % (_strip_col(_pieces_html(lab)), _pieces_html(rest)))
            continue
        if pb is not None:
            k, nm, bd = pb
            if blue > 0.5 and 'PDF' not in _plain(pcs):
                entry[k] = '<h3 class="material-name res-src">%s</h3>' % nm
                item = re.sub(r'<span class="res-title"><em>(.*?)</em></span>', r'<span class="res-title">\1</span>', _res_item(pcs), count=1)
                assert item.endswith('</div>'), item[-40:]
                add(item[:-6] + ''.join(' ' + x for x in bd) + '</div>'); report.append(('settings', 'PDF badge moved to the title below its name (owner 2 Nov 16:06)', txt[:40])); continue
        if blue > 0.5:
            add(re.sub(r'<span class="res-title"><em>(.*?)</em></span>', r'<span class="res-title">\1</span>', _res_item(pcs), count=1)); continue   # titles upright, as Word (8.1's were italic)
        if p.runs and all((r.font.underline or not r.text.strip()) for r in p.runs) and not any(x[3] for x in pcs):
            add('<p class="mm-ul"><u>%s</u></p>' % _pieces_html(pcs)); continue   # the <u> as the converter writes it (build_page.py 20 Oct rule); the template underlines nothing by class
        if was_blank and entry is not None:
            # a plain line after Word's blank line inside an open entry ("Montessori Education", "Society of Antiquaries of London",
            # "They also have a selection ..."): an entry of its own, as Word and the PDF space it (2 Nov build 6 review, items 19 and NEW 3)
            close(); entry = []; report.append(('settings', 'a new entry after Word\'s blank line', txt[:40]))
        cls = ' class="res-desc"' if entry is not None else ''
        add('<p%s>%s</p>' % (cls, _tabbed(pcs)))
    if in_list: add('<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in in_list))
    close()
    if pending_rule: out.append('<div class="beige-rule mm-org-rule"></div>')
    assert fi == len(floats) and ri == len(rows), (fi, len(floats), ri, len(rows))
    main.clear()
    main.append(BeautifulSoup('<section class="section">%s</section>' % ''.join(out), 'html.parser'))

    # 8.4 build 9 review A1: each green heading opens a section of its own (as the converter's pages and 8.1), so the template's
    # heading rules (first entry 25 px below the heading; 51 px above a heading with no beige line above) apply to every heading alike
    _sec = main.find('section', class_='section'); _cur = _sec
    for _h in list(_sec.find_all('h2', recursive=False)):
        if _h.previous_sibling is None: continue
        _new = BeautifulSoup('<section class="section"></section>', 'html.parser').section
        _cur.insert_after(_new); _cur = _new
        _x = _h
        while _x is not None:
            _n = _x.next_sibling
            if _x is not _h and getattr(_x, 'name', None) == 'h2': break
            _new.append(_x.extract()); _x = _n
    for a in main.find_all('a'):
        if re.sub(r'\s+', ' ', a.get_text()).strip() == 'PDF' and 'pdf' not in (a.get('class') or []): a['class'] = (a.get('class') or []) + ['pdf']
    from bs4 import NavigableString
    # blue words inside a line (span.mm-blue, inline-block in the template): a space at either end of the span is lost on screen, so
    # it stands outside the span ("Albums (teacher's guides)", 8.4 first-build fault 6); Word's "theDevelopmental" gets its space (typo)
    for sp in main.select('span.mm-blue'):
        t = sp.string
        if t is None: continue
        if t != t.lstrip():
            sp.string = t.lstrip(); sp.insert_before(NavigableString(' '))
        if sp.string != sp.string.rstrip():
            sp.string = sp.string.rstrip(); sp.insert_after(NavigableString(' '))
        pv = sp.previous_sibling
        if isinstance(pv, NavigableString) and pv.endswith('the') and sp.get_text().startswith('Developmental'):
            pv.replace_with(NavigableString(pv + ' '))
    for a in main.select('p a.pdf'):   # a badge in running text keeps to the word before it (2 Nov build 6 review, NEW 5: "Lower Elementary" / PDF at 390;
        pv = a.previous_sibling       # no space character holds an inline-block badge: the Resources template's span.mm-keep, owner's agreement 2 Nov)
        if isinstance(pv, NavigableString) and pv.strip():
            lsp = pv.previous_sibling
            tab_unit = getattr(lsp, 'name', None) == 'span' and 'mm-lsp' in (lsp.get('class') or [])
            if not tab_unit and a.parent.name == 'p' and a.find_next_sibling() is None and any(
                    q is not None and q.name == 'p' and q.find_all(True, recursive=False) and (q.find_all(True, recursive=False)[-1].name == 'a' and 'pdf' in (q.find_all(True, recursive=False)[-1].get('class') or [])
                        or q.find_all(True, recursive=False)[-1].select_one(':scope > a.pdf:last-child') is not None)
                    for q in (a.parent.find_previous_sibling(), a.parent.find_next_sibling())):
                continue   # 8.3 build 12 review, fault 5: a badge ending a line whose neighbouring line also ends in a badge is left to the template's 20 Oct badge column (one column; phones: 24 after the text, or the margin)
            txt = str(pv).rstrip(); k = 0 if tab_unit else txt.rfind(' ') + 1   # a label after a tab ("Lower Elementary PDF") is kept whole (8.3 build 12 review, fault 7)
            keep = BeautifulSoup('<span class="mm-keep"></span>', 'html.parser').span
            pv.replace_with(NavigableString(txt[:k])); a.insert_before(keep); keep.append(NavigableString(txt[k:] + ' ')); keep.append(a.extract())
    # the green headings get ids, so the template's contents box lists them (8.4 build 2 review N1: the box was empty and hidden)
    seen = set()
    for h in main.select('h2'):
        sl = re.sub(r'[^a-z0-9]+', '-', h.get_text().lower()).strip('-')
        while sl in seen: sl += '-2'
        seen.add(sl); h['id'] = sl
    # "Scale": Word colours "Scal" blue and "e" black (a colour slip); the whole word blue, so it cannot break between the two (N2)
    for sp in main.select('span.mm-blue'):
        nx = sp.next_sibling
        if sp.string and sp.string.endswith('Scal') and isinstance(nx, NavigableString) and nx.startswith('e'):
            sp.string = sp.string + 'e'; nx.replace_with(NavigableString(nx[1:]))
    # 8.4 build 7 review 3, 4: a lone punctuation mark Word colours red or blue inside black text (the comma after "Montessori Glossary
    # Community Project", the opening quote mark of the Greenspring quotation) is a colour slip: shown in the text colour, as "Scale" (N2)
    for sp in main.select('p span.mm-blue, p span[class^="mm-hc-"]'):
        if re.fullmatch(r'[\s,.;:‘’“”\'"()!?-]+', sp.get_text() or ''): sp.unwrap()
    # 8.4 build 7 review 5: a blue phrase of several words (span.mm-blue, inline-block in the template) cannot break, so the line
    # before it is stretched or left short ("Developmental Environment Rating Scale"): each word its own blue span, the spaces between them
    for sp in main.select('p span.mm-blue'):
        w = (sp.string or '').split(' ')
        if sp.string is None or len(w) < 2: continue
        for k_, x in enumerate(w):
            if k_: sp.insert_before(NavigableString(' '))
            n = BeautifulSoup('<span class="mm-blue"></span>', 'html.parser').span; n.string = x; sp.insert_before(n)
        sp.decompose()
    # 8.4 build 7 review 7: an age range ("6 - 12") is not split across two lines: the template's span.mm-keep (nowrap)
    for tn in list(main.find_all(string=re.compile(r'\d+ - \d+'))):
        if tn.find_parent(['a', 'h2', 'h3']) is not None or tn.find_parent('span', class_='mm-keep') is not None: continue
        parts = re.split(r'(\d+ - \d+)', str(tn)); new_ = []
        for k_, x in enumerate(parts):
            if k_ % 2: n = BeautifulSoup('<span class="mm-keep"></span>', 'html.parser').span; n.string = x; new_.append(n)
            elif x: new_.append(NavigableString(x))
        for x in new_: tn.insert_before(x)
        tn.extract()
    report.append(('settings', 'contents box: the green headings, with ids', str(len(seen))))

    # owner 2 Nov 18:07 (question 1 of 4, her screenshot of "Building Effective Teacher Mentoring Communities"): a line that is only a link,
    # straight under a red name, is a blue title line (div.res-item > span.res-title), spaced as every other title
    for _h in main.select('h3.res-src'):
        _p = _h.find_next_sibling()
        if _p is None or _p.name != 'p': continue
        _k = [c for c in _p.contents if not (isinstance(c, str) and not c.strip())]
        if not _k or getattr(_k[0], 'name', None) != 'a' or 'pdf' in (_k[0].get('class') or []): continue
        if not all(getattr(c, 'name', None) == 'span' and 'mm-blue' in (c.get('class') or []) for c in _k[1:]): continue
        _it = BeautifulSoup('<div class="res-item"><span class="res-title"></span></div>', 'html.parser').div
        _t = _it.span
        for c in list(_p.contents): _t.append(c.extract())
        _p.replace_with(_it); report.append(('settings', 'link line under a red name as a title line (owner 2 Nov 18:07)', _t.get_text()[:40]))
    # 4 Nov queued edit (owner 07:17 "Remove the words 'Professional Development'", her contents screenshot; 07:19 "yes they should" -
    # the headings too): the four green headings lose "Professional Development: " (ids kept), so the contents box follows them
    _pd = 0
    for _h in main.find_all('h2'):
        for _t in _h.find_all(string=True):
            if 'Professional Development: ' in _t: _t.replace_with(_t.replace('Professional Development: ', '')); _pd += 1
    assert _pd == 4, ('Professional Development headings', _pd)
    report.append(('settings', 'headings without "Professional Development: " (owner 4 Nov 07:17, 07:19)', str(_pd)))
    # 4 Nov (owner 07:48 "Websites on this page also: 50 before the organisation names", her screenshot): every red name line that starts
    # an entry 50 below the text above it; one straight under a heading, a divider or a row of images keeps 40 (3 Nov rules)
    _n50 = _k40 = 0
    for _h in main.select('div.res-entry > h3.material-name'):
        if _h.parent.find(True) is not _h: continue
        _pv = _h.parent.find_previous_sibling()
        if _pv is None or _pv.name == 'h2': continue
        if 'beige-rule' in (_pv.get('class') or []) or 'mm-row' in (_pv.get('class') or []) or _pv.select_one('.mm-row') is not None: _k40 += 1; continue
        _h['data-gap'] = '50'; _n50 += 1
    report.append(('settings', 'red name lines 50 above (owner 4 Nov 07:48); under a heading, divider or images kept 40', '%d / %d' % (_n50, _k40)))
    # 4 Nov (owner 07:49 "what is the spacing above the section headings?" - 40; 07:51 "above the section headings = 60"): every green
    # section heading 60 below the text above it, except the first, which keeps the 66 under the contents box
    _hs = [h for h in main.find_all('h2') if 'mm-hc-00B050' in (h.get('class') or [])]
    for _h in _hs[1:]: _h['data-gap'] = '60'
    report.append(('settings', 'section headings 60 above (owner 4 Nov 07:51)', str(len(_hs) - 1)))
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
    # 2 Nov build 6 review (NEW 5, NEW 6): a PDF link after a tab is the badge of the words before it - joined to them by a narrow
    # no-break space (U+202F: the build turns U+00A0 into a plain space), as a title and its badge are (the badge's own 24 px margin is the gap), so the badge never starts a line
    # away from its words at 390 and is not 48 px from them on computers
    hs = []
    for c in parts:
        h = _pieces_html(c)
        if not h.strip(): continue
        if hs and ''.join(x[0] for x in c).strip() == 'PDF' and all(x[3] for x in c if x[0].strip()):
            hs[-1] = hs[-1].rstrip() + '\u202f' + h; continue
        hs.append(h)
    return '<span class="mm-lsp"> </span>'.join(hs) if len(parts) > 1 else _pieces_html(parts[0])


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
        if t == '\t':
            if body and body[-1][0] != '\t' and body[-1][0].strip() == '' : body.pop()   # 8.4 build 7 review 1: a space before the tab (NAMTA, MPPI) gives way to it
            if body and body[-1][0][-1:] == ' ': body[-1] = (body[-1][0].rstrip(),) + tuple(body[-1][1:])   # "Action " (PMAI): no space as well as the spacer
            if body and body[-1][0] != '\t': body.append(('\t',) + tuple(pcs[i][1:]))   # kept as a tab: the 24 px spacer before the short name (owner 2 Nov 16:24)
            i += 1; continue
        body.append(pcs[i]); i += 1
    while body and body[-1][0] in ('\t', ' '): body.pop()   # no spacer at the end of a name line
    return body, badges


def _split_tab(pcs):
    lab = []; rest = []; seen = False
    for x in pcs:
        if x[0] == '\t': seen = True; continue
        (rest if seen else lab).append(x)
    return lab, rest


def _src_html(pcs):
    # a red source line in Word's own colours (2 Nov reviews: 8.3 NEW 4 the TES/NATE "/", 8.4 N5 the abbreviation links, N6 "(AMI)"):
    # red words and red links are red (the template's source-line colour); a link Word leaves in its link colour is a link
    # (a.mm-link); words Word sets black are black (span.mm-ink) - classes of the Resources Code Template (owner's agreement 2 Nov)
    html = []; i = 0
    while i < len(pcs):
        t, col, it, href, sup = pcs[i]
        if href:
            txt = ''; j = i; cols = set()
            while j < len(pcs) and pcs[j][3] == href:
                txt += pcs[j][0]
                if pcs[j][0].strip(): cols.add(pcs[j][1])
                j += 1
            core = txt.strip(); lead = ' ' if txt[:1].isspace() else ''; tail = ' ' if txt[-1:].isspace() and len(txt) > 1 else ''
            cls = ' class="pdf"' if core == 'PDF' else ('' if cols & set(REDS) else ' class="mm-link"')
            html.append('%s<a%s href="%s" rel="noopener" target="_blank">%s</a>%s' % (lead, cls, _esc(href), _esc(core), tail)); i = j; continue
        if t == '\t':   # 8.4 build 9 review A2: the spacer kept with the word before it (span.mm-keep), so a short name that wraps starts at the margin
            prev = html[-1] if html else ''
            mt = re.search(r'(\S+)$', prev)
            if mt and not prev.endswith('>'):
                html[-1] = prev[:mt.start()] + '<span class="mm-keep">' + mt.group(1) + '<span class="mm-lsp"> </span></span>'
            else: html.append('<span class="mm-lsp"> </span>')
            i += 1; continue   # owner 2 Nov 16:24 (queued): "a clear separation between the organisations and their acronym" - the template's 24 px space
        if t == '\n': html.append(' '); i += 1; continue
        txt = t; j = i + 1
        while j < len(pcs) and not pcs[j][3] and pcs[j][0] not in ('\t', '\n') and pcs[j][1] == col: txt += pcs[j][0]; j += 1
        core = txt.strip(); lead = txt[:len(txt) - len(txt.lstrip())]; tail = txt[len(txt.rstrip()):]
        if not core: html.append(' ' if txt else ''); i = j; continue
        h = _esc(core)
        if col == '000000': h = '<span class="mm-ink">%s</span>' % h
        html.append((' ' if lead else '') + h + (' ' if tail else '')); i = j
    return re.sub(r' {2,}', ' ', ''.join(html)).strip()

