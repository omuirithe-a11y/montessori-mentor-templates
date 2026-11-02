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
RED_NAMES = ['Old School Classroom Technology']   # owner 2 Nov 16:20 (queued, her screenshot)
CAPTION_SOURCES = ['Far left', 'Far right']   # owner 2 Nov 16:20 (queued)
QUOTE_PLAIN = ['In the early modern era']   # owner 2 Nov 16:20 (queued)
NAME_LINKS = ['Montessori Education']   # owner 2 Nov 16:03 (queued)
SPLIT_LABEL = ['London Museum']   # owner 2 Nov 15:34
TEXT_EDITS = [('Sometime ivory was used', 'Sometimes ivory was used'), ('BookTrust is rhe UK', 'BookTrust is the UK'), ('the Unites States government', 'the United States government'), ('Why is it called "The Horn Book?', 'Why is it called "The Horn Book"?'), ('piece of wood..', 'piece of wood.')]   # typos (owner 27 Oct: correct all typos); the last three from the 8.3 build 12 review   # typo (owner 27 Oct: correct all typos; her 15:34 screenshot has "Sometimes")
NO_RULE_BEFORE = ['Hornbooks']   # owner 2 Nov 15:31: "Delete the divider above Hornbooks"


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
    if len(floats) > 1: floats[1]['class'] = floats[1].get('class', []) + ['mm-initial']   # owner 2 Nov 18:23: the Victorian Web's decorative "A" (the second image beside text, the one on the left) is a decorative first letter (template class mm-initial)
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
    pend_badges = None
    blank = False   # an empty Word paragraph just before (2 Nov review: Word's blank line between entries starts a new entry)
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
            close(); out.append('<div class="beige-rule mm-org-rule"></div>'); blank = False; continue
        if not txt:
            blank = True; continue
        was_blank, blank = blank, False
        pb, pend_badges = pend_badges, None   # a name line's badge waiting for the line straight below (owner 2 Nov 16:06)
        if num:
            in_list.append(_pieces_html(pcs).replace('<span class="mm-blue">', '').replace('</span>', '')); continue
        green, red, blue = _share(pcs, GREENS), _share(pcs, REDS), _share(pcs, BLUES)
        first = next((x for x in pcs if x[0].strip()), None)
        if green > 0.6:
            close()
            if txt in NO_RULE_BEFORE and out and 'beige-rule' in out[-1]:   # owner 2 Nov 15:31: "Delete the divider above Hornbooks"
                out.pop(); report.append(('settings', 'beige line before the heading left out (owner 2 Nov 15:31)', txt))
            out.append('<h2 class="mm-hc-00B050">%s</h2>' % _strip_col(_pieces_html(pcs))); continue   # spacing above: the template (owner 2 Nov 16:08 "On all pages and in the template")
        if red > 0.5 or (first is not None and first[1] in REDS and red > 0.3) or txt in RED_NAMES:   # RED_NAMES: owner 2 Nov 16:20 (queued)
            close(); entry = []
            body, badges = _split_badges(pcs)
            entry.append('<h3 class="material-name res-src">%s%s</h3>' % (_src_html(body), ''.join(' ' + b for b in badges)))
            # owner 2 Nov 16:06 (queued): "Place the PDF on the same line as the title it refers to, not on the line with the author" - a badge on
            # the name line moves to the blue title straight below it (if the next line is not a blue title, it stays on the name line)
            pend_badges = (len(entry) - 1, _src_html(body), badges) if badges else None
            continue
        if was_blank and entry is not None and pb is None and blue > 0.5:
            # 8.3 build 14 review A4: any line after Word's blank line inside an open entry starts an entry of its own - a blue title
            # too ("The Horn Book Magazine"), so it stands 51 px below, as "Society of Antiquaries of London" after the same blank line
            close(); entry = []; was_blank = False; report.append(('settings', 'a new entry after Word\'s blank line', txt[:40]))
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
            if txt in NAME_LINKS:   # owner 2 Nov 16:03 (queued): "Make the spacing under 'Montessori Education' the same as under the other
                # organisations" - the link line is the entry's name line (h3.res-src), its link in Word's link colour (a.mm-link, template 2 Nov 13:19)
                entry.append('<h3 class="material-name res-src">%s</h3>' % _src_html(pcs)); report.append(('settings', 'link line as the entry\'s name line (owner 2 Nov 16:03)', txt)); continue
        cls = ' class="res-desc"' if entry is not None else ''
        cap = next((k for k in CAPTION_SOURCES if txt.startswith(k + ':')), None)
        if cap:   # owner 2 Nov 16:20 (queued, her screenshot): "Far left, from the <link>" on one line, the quotation below in “ ”
            links = [x for x in pcs if x[3]]   # every piece of the link, spaces too ("Victoria and Albert Museum")
            href = next((x[3] for x in links if x[0].strip()), None)
            words = ''.join(x[0] for x in links).strip()
            q = ''.join(x[0] for x in pcs if not x[3] and x[0] != '\t')
            q = q[len(cap) + 1:].strip().strip('‘’').strip()
            q = re.sub(r'\s+', ' ', q)
            add('<p%s>%s, from the <a href="%s" rel="noopener" target="_blank">%s</a></p>' % (cls, cap, _esc(href or ''), _esc(words)))
            add('<p%s>“%s”</p>' % (cls, _esc(q))); report.append(('settings', 'caption: source line, then the quotation (owner 2 Nov 16:20)', cap)); continue
        if any(txt.startswith(k) for k in QUOTE_PLAIN):   # owner 2 Nov 16:20 (queued, her screenshot): upright, in “ ”
            add('<p%s>“%s”</p>' % (cls, _pieces_html([(x[0], x[1], False, x[3], x[4]) for x in pcs]).strip())); continue
        lab0 = next((k for k in SPLIT_LABEL if txt.startswith(k + ':')), None)
        if lab0:   # owner 2 Nov 15:34: "Change the page so it looks like that - seperate line" (her screenshot: the label on its own line, the quotation below in ‘ ’)
            lab, rest = _split_tab(pcs)
            body = _pieces_html(rest).strip()
            add('<p%s>%s</p>' % (cls, re.sub(r'\s*:\s*$', '', _pieces_html(lab).strip())))
            add('<p%s>‘%s’</p>' % (cls, body)); report.append(('settings', 'label on its own line above its quotation (owner 2 Nov 15:34)', lab0)); continue
        add('<p%s>%s</p>' % (cls, _tabbed(pcs)))
    if in_list: add('<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in in_list))
    close()
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
    for a in main.select('p a'):   # 8.3 build 14 review A3: a short link such as "2 to 4" is not split across two lines (span.mm-keep)
        if re.fullmatch(r'\d+\s+to\s+\d+', a.get_text().strip()) and a.find_parent('span', class_='mm-keep') is None:
            k_ = BeautifulSoup('<span class="mm-keep"></span>', 'html.parser').span; a.insert_before(k_); k_.append(a.extract())

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
    # 8.3 build 15 review: (1) a blue title that opens an entry ("The Horn Book Magazine") stands 51 px below the entry above, as an
    # entry with a red name or a plain line does (the template's letters-to-letters data-gap); (2) a label line and the quotation under it
    # ("London Museum", "Society of Antiquaries of London", "Far left, from ...", "Far right, from ...") 21 px apart, as under a red name
    for _e in main.select('div.res-entry'):
        _pv = _e.find_previous_sibling()
        _f = _e.find(True, recursive=False)
        if _pv is not None and _pv.name == 'div' and 'res-entry' in (_pv.get('class') or []) and _f is not None and _f.name == 'div' and 'res-item' in (_f.get('class') or []):
            _f['data-gap'] = '51'; report.append(('settings', 'blue title opening an entry: 51 px below the entry above (8.3 b15 review)', _f.get_text()[:40]))
    for _p in main.find_all('p'):
        _t = re.sub(r'\s+', ' ', _p.get_text()).strip()
        if _t in ('London Museum', 'Society of Antiquaries of London') or _t.startswith(('Far left, from the', 'Far right, from the')):
            _n = _p.find_next_sibling()
            if _n is not None and _n.name == 'p': _n['data-gap'] = '21'; report.append(('settings', 'quotation 21 px below its label (8.3 b15 review)', _t))
    # 8.3 build 16 review: (1) "Far right, from ..." has Word's empty line above it (Word paragraph 139): 51 px below the quotation above,
    # as between two entries; (2) no spaces around a slash (owner's preference, "Junk/Adventure"): "Supplement / National" in the TES/NATE
    # name line, with a line break allowed after the slash (as the build's slash rule)
    for _p in main.find_all('p'):
        if re.sub(r'\s+', ' ', _p.get_text()).strip().startswith('Far right, from the'): _p['data-gap'] = '51'
    from bs4 import NavigableString as _NS2
    for _sp in main.select('h3 span.mm-ink'):
        if _sp.get_text() == '/':
            _a, _b = _sp.previous_sibling, _sp.next_sibling
            if isinstance(_a, _NS2): _a.replace_with(_NS2(str(_a).rstrip()))
            if isinstance(_b, _NS2): _b.replace_with(_NS2(str(_b).lstrip()))
            _sp.insert_after(BeautifulSoup('<wbr/>', 'html.parser').wbr); report.append(('settings', 'no spaces around the slash (owner preference)', 'TES/NATE'))
    # 8.3 build 17 review A1: the lines under "A Selection" evenly spaced, as in the PDF - the three black lines 32 px apart
    # (letters to letters, the paragraph gap at 641 px and wider) and the first of them 32 px below the blue title too, at every width
    for _p in main.find_all('p'):
        _t = re.sub(r'\s+', ' ', _p.get_text()).strip()
        if _t.startswith('It’s Never too Early') or _t.startswith('Wordless Picture Books'):
            _p['data-gap'] = '32'; report.append(('settings', 'A Selection line 32 px below the line above (8.3 b17 review)', _t[:30]))
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
        if t == '\t': i += 1; continue
        body.append(pcs[i]); i += 1
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
        if t in ('\t', '\n'): html.append(' '); i += 1; continue
        txt = t; j = i + 1
        while j < len(pcs) and not pcs[j][3] and pcs[j][0] not in ('\t', '\n') and pcs[j][1] == col: txt += pcs[j][0]; j += 1
        core = txt.strip(); lead = txt[:len(txt) - len(txt.lstrip())]; tail = txt[len(txt.rstrip()):]
        if not core: html.append(' ' if txt else ''); i = j; continue
        h = _esc(core)
        if col == '000000': h = '<span class="mm-ink">%s</span>' % h
        html.append((' ' if lead else '') + h + (' ' if tail else '')); i = j
    return re.sub(r' {2,}', ' ', ''.join(html)).strip()
