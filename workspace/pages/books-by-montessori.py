# 8.1 Books by Montessori - page settings (31 Oct 2026, Resources Code Template 3f884aae)
# Owner 20:57: title and hero "Books by Montessori". Owner 20:58: "No photos to blur on this page".
# Owner 21:45 "Ok" to the fault list of build 1 (22 faults): faults 2-22 fixed here in the build settings, using only the
# template's own classes (the code check proves it); fault 1 (the covers grid) waits for her agreement to a template element.
# Word file: 8.1 Books by Maria Montessori.docx (Drive 1fVNemFxwxGL_bbO_KR4tT6jMAj7ZoIbC, sha256 00689679...).
import re, os, sys

DOCX = None   # set by POST_MAIN from the build's own --docx (sys.argv)

BLUES = ('0432FF', '3366CC', '0000FF')
REDS = ('FF0000', 'EE0000')
HEADINGS_THAT_ARE_TITLES = ('The Organisation of Intellectual Work in School', 'Psychogeometry')   # blue whole lines the converter made headings; in Word they are book titles in the list (fault 14)


def _word():
    import docx
    from docx.oxml.ns import qn
    a = sys.argv; f = a[a.index('--docx') + 1]
    return docx.Document(f), qn


def _runs(p, qn):
    """Word paragraph -> pieces (text, colour, italic, href, superscript); tabs become '\t'."""
    rels = {r.rId: r.target_ref for r in p.part.rels.values() if r.is_external}
    out = []
    def rp(r, k):
        e = r.find(qn('w:rPr')); x = e.find(qn(k)) if e is not None else None
        if x is None: return None
        return x.get(qn('w:val')) or 'true'
    def walk(el, href):
        for c in el:
            if c.tag == qn('w:hyperlink'):
                walk(c, rels.get(c.get(qn('r:id'))))
            elif c.tag == qn('w:r'):
                col = (rp(c, 'w:color') or '').upper()
                it = rp(c, 'w:i') not in (None, '0', 'false')
                sup = rp(c, 'w:vertAlign') == 'superscript'
                for x in c:
                    if x.tag == qn('w:t'): out.append([x.text or '', col, it, href, sup])
                    elif x.tag == qn('w:tab'): out.append(['\t', col, it, href, sup])
                    elif x.tag == qn('w:br'): out.append(['\n', col, it, href, sup])
            elif c.tag in (qn('w:smartTag'), qn('w:ins'), qn('w:fldSimple')):
                walk(c, href)
    walk(p._p, None)
    return out


def _esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _pieces_html(pcs):
    """Word pieces -> HTML: links as links (PDF links as the template's PDF badge), blue as mm-blue, red as mm-hc-EE0000 (the template colours red words inside a line with that class),
    italic as em; spaces kept outside coloured spans (fault 15: an inline-block span drops a trailing space)."""
    html = []; i = 0
    while i < len(pcs):
        t, col, it, href, sup = pcs[i]
        if href:   # a whole link
            txt = ''; j = i
            while j < len(pcs) and pcs[j][3] == href: txt += pcs[j][0]; j += 1
            core = txt.strip()
            lead = ' ' if txt[:1].isspace() else ''; tail = ' ' if txt[-1:].isspace() and len(txt) > 1 else ''
            cls = ' class="pdf"' if core == 'PDF' else ''
            inner = '<em>%s</em>' % _esc(core) if pcs[i][2] and core != 'PDF' else _esc(core)
            html.append('%s<a%s href="%s" rel="noopener" target="_blank">%s</a>%s' % (lead, cls, _esc(href), inner, tail)); i = j; continue
        if t in ('\t', '\n'): html.append(' ' if t == '\t' else '<br/>'); i += 1; continue
        txt = t; j = i + 1
        while j < len(pcs) and not pcs[j][3] and pcs[j][0] not in ('\t', '\n') and pcs[j][1] == col and pcs[j][2] == it and pcs[j][4] == sup: txt += pcs[j][0]; j += 1
        core = txt.strip(); lead = txt[:len(txt) - len(txt.lstrip())]; tail = txt[len(txt.rstrip()):]
        if not core: html.append(' ' if txt else ''); i = j; continue
        h = _esc(core)
        if it: h = '<em>%s</em>' % h
        if sup: h = '<sup>%s</sup>' % h
        if col in BLUES: h = '<span class="mm-blue">%s</span>' % h
        elif col in REDS: h = '<span class="mm-hc-EE0000">%s</span>' % h
        html.append((' ' if lead else '') + h + (' ' if tail else '')); i = j
    return re.sub(r' {2,}', ' ', ''.join(html)).strip()


def _year_split(pcs):
    txt = ''.join(p[0] for p in pcs).lstrip()
    m = re.match(r'(\d{4})\s', txt)
    if not m: return None, pcs
    y = m.group(1); rest = []; seen = ''
    for p in pcs:
        if len(seen.strip()) < 4 or (len(seen.strip()) == 4 and p[0] in ('\t', ' ')):
            seen += p[0]
            if len(seen.strip()) > 4:   # the run held the year and more
                k = p[0].index(y) + 4 if y in p[0] else 0
                rest.append([p[0][k:]] + p[1:])
            continue
        rest.append(p)
    return y, rest


def _is_entry(pcs):
    """A list line (year and/or a book title, with its badges) - not a description: Word gives the title in blue,
    or the line is a link that starts the line, or it starts with a year."""
    txt = ''.join(p[0] for p in pcs).strip()
    if re.match(r'\d{4}\s', txt): return True
    first = next((p for p in pcs if p[0].strip()), None)
    if first is None: return False
    return first[1] in BLUES or (first[3] is not None and first[0].strip() != 'PDF' and len(txt) < 90)


def _res_item(pcs):
    """Word pieces of a book line -> the Resources template's res-item: the title (blue, as the template sets res-title),
    other words (a year in brackets, "(Lectures)") as meta, and every PDF link as a badge, in Word's order."""
    title = []; meta = []; badges = []; seen_title = False
    i = 0
    while i < len(pcs):
        t, col, it, href, sup = pcs[i]
        if href and ''.join(x[0] for x in pcs[i:] if x[3] == href).strip() == 'PDF' or (href and t.strip() == 'PDF'):
            j = i; acc = ''
            while j < len(pcs) and pcs[j][3] == href and acc.strip() != 'PDF': acc += pcs[j][0]; j += 1   # two PDF links side by side to one address stay two badges, as Word
            badges.append('<a class="pdf" href="%s" rel="noopener" target="_blank">PDF</a>' % _esc(href)); i = j; seen_title = True; continue
        if t in ('\t',):
            if title: seen_title = True
            i += 1; continue
        if not seen_title and (col in BLUES or href or not title): title.append(pcs[i])
        else: seen_title = True; meta.append(pcs[i])
        i += 1
    th = _pieces_html(title).replace('<span class="mm-blue">', '').replace('</span>', '') if title else ''
    mh = _pieces_html(meta)
    if mh.strip() == 'PDF':   # 1948: "PDF" in Word with no link. Owner 1 Nov 02:58 "find a link": no free copy of the book was found
        # (searched 1 Nov 03:0x: the web, Scribd (a 5-page condensed version), academia.edu (unreachable), the Italian edition);
        # the badge links the publisher Montessori-Pierson's English e-books page, which lists the book
        mh = ''; badges.append('<a class="pdf" href="https://montessori-pierson.com/pages/ebooks" rel="noopener" target="_blank">PDF</a>')
    # 1 Nov (checker b12 fault 2): a space before each badge - on phones the template sets the line as text, and with no space
    # the last word of the title and the badges were one unbreakable piece ("Dr. Montessori's Own" / "Handbook PDF PDF");
    # wider than 640 px the line is a flex row, where the spaces have no effect
    return '<div class="res-item"><span class="res-title"><em>%s</em></span>%s%s</div>' % (th, (' <span class="meta">%s</span>' % mh) if mh.strip() else '', ''.join(' ' + b for b in badges))


def POST_MAIN(main, s, report):
    from bs4 import BeautifulSoup, NavigableString
    _drop_covers_grid(main, report)
    D, qn = _word()
    paras = [p for p in D.paragraphs]
    norm = lambda x: re.sub(r'\s+', ' ', x).strip()

    # fault 14: the two book titles the converter made headings go back into the list (their section joins the one before)
    for h in list(main.find_all('h2')):
        if norm(h.get_text()) in HEADINGS_THAT_ARE_TITLES:
            sec = h.find_parent('section'); prev = sec.find_previous_sibling('section') if sec is not None else None
            p = s.new_tag('p'); p.string = norm(h.get_text()); h.replace_with(p)
            if sec is not None and prev is not None:
                for c in list(sec.contents): prev.append(c.extract())
                sec.decompose()
            report.append(('settings', 'a book title made a heading by the converter, put back in the list (page setting)', norm(p.get_text())))

    # 31 Oct 22:3x (owner 22:34 "the page looks awful"; 22:37 "fix the ... page"): the chronological list in the Resources
    # template's own entry style, as the live Culture Resources page: each year a red source line (h3.material-name.res-src),
    # each book a res-item (blue title, PDF badges in one column), each description a res-desc under its book
    w0 = next(i for i, p in enumerate(paras) if p.text.strip().startswith('The following is a chronological list'))
    # 2 Nov: in the 1 Nov Word file the owner removed "This list comes from Montessori Album" herself; the list ends at "Montessori Nuggets"
    w1 = next(i for i, p in enumerate(paras) if i > w0 and p.text.strip().startswith(('This list comes from', 'Montessori Nuggets')))
    start = next(e for e in main.find_all('p') if norm(e.get_text()).startswith('The following is a chronological list'))
    stop = next(e for e in start.find_all_next() if e.name == 'div' and 'beige-rule' in (e.get('class') or []))
    nodes = []
    for e in list(start.find_all_next()):
        if e is stop: break
        if e.parent is not None and e.parent.name in ('section', 'main') and e.name in ('p', 'div', 'ul'): nodes.append(e)
    for e in nodes: e.extract()
    entries = []
    for p in paras[w0 + 1:w1]:
        pcs = _runs(p, qn)
        if not ''.join(x[0] for x in pcs).strip(): continue
        if _is_entry(pcs):
            y, rest = _year_split(pcs)
            if y or not entries: entries.append([y, []])
            entries[-1][1].append(['item', _res_item(rest)])
        else:
            if not entries: entries.append([None, []])
            entries[-1][1].append(['desc', _pieces_html(pcs)])
    out = []
    for y, parts in entries:
        h = '<h3 class="material-name res-src">%s</h3>' % y if y else ''
        body = ''.join(x if k == 'item' else '<p class="res-desc">%s</p>' % x for k, x in parts)
        out.append('<div class="res-entry">%s%s</div>' % (h, body))
    frag = BeautifulSoup(''.join(out), 'html.parser')
    for x in list(frag.contents)[::-1]: start.insert_after(x)
    report.append(('settings', 'chronological list in the template\'s entry style (as Culture Resources): %d years' % len(entries), 'owner 22:34-22:37'))

    # the reading list after "If you're looking to delve a little deeper" in the same entry style (titles, badges, descriptions)
    r0 = next(i for i, p in enumerate(paras) if p.text.strip().startswith('If you') and 'delve a little deeper' in p.text)
    r1 = next(i for i, p in enumerate(paras) if i > r0 and p.text.strip() == 'So many books, so little time')
    rstart = next(e for e in main.find_all('p') if 'delve a little deeper' in e.get_text())
    floats = []; rnodes = []
    for e in list(rstart.find_next_siblings()):
        if e.name in ('h2', 'section') or 'beige-rule' in (e.get('class') or []): break
        if 'mm-float' in (e.get('class') or []): floats.append(e.extract()); continue
        rnodes.append(e)
    for e in rnodes: e.extract()
    ents = []
    for p in paras[r0 + 1:r1]:
        pcs = _runs(p, qn)
        if not ''.join(x[0] for x in pcs).strip(): continue
        if _is_entry(pcs): ents.append([_res_item(pcs), []])
        elif ents: ents[-1][1].append(_pieces_html(pcs))
    out = []
    for i, (it, ds) in enumerate(ents):
        fl = str(floats[0]) if (i == 0 and floats) else ''   # the cover beside its description, as in Word and the PDF
        # 1 Nov (checker b11 faults 3, 12): the template's book line (.res-item.res-book: 35px above each book, 3.5px to its
        # description) - the books were 8px apart and the first sat on the paragraph above, unlike Word's blank lines
        it = it.replace('<div class="res-item">', '<div class="res-item res-book">', 1)
        out.append('%s%s%s' % (it, fl, ''.join('<p class="res-desc">%s</p>' % d for d in ds)))
    frag = BeautifulSoup(''.join(out), 'html.parser')
    for x in list(frag.contents)[::-1]: rstart.insert_after(x)
    report.append(('settings', 'reading list in the template\'s entry style: %d books, the cover beside the first' % len(ents), 'owner 22:34-22:37'))

    # faults 5-6: the Key Principles and Key Areas lines rebuilt from Word: italic label in the label column, then the text
    for head in ('Key Principles Summarized', 'Key Areas and Examples of Materials'):
        h = next(x for x in main.find_all('h2') if norm(x.get_text()).replace('Summarised', 'Summarized') == head)
        sec = h.find_parent('section')
        wi = next(i for i, p in enumerate(paras) if p.text.strip() == head)
        k = wi + 1; lines = []
        while k < len(paras) and '\t' in paras[k].text:
            lab, txt = paras[k].text.split('\t', 1); lines.append((lab.strip(), txt.strip())); k += 1
        old = [x for x in sec.find_all('p', recursive=False) if 'mm-hanglab' in (x.get('class') or [])]
        assert len(old) == len(lines), (head, len(old), len(lines))
        for o, (lab, txt) in zip(old, lines):   # 22:3x: the label on its own line (the template's label column is 8em; these labels are longer)
            o.replace_with(BeautifulSoup('<p><em>%s</em><br/>%s</p>' % (_esc(lab), _esc(txt)), 'html.parser'))   # 22:5x: the label on the line straight above its text (checker b8 fault 6)
        report.append(('settings', 'label lines rebuilt from Word, labels italic (page setting)', head))

    # fault 7: Required Readings and Recommended Readings by Maria Montessori in two columns, as Word (the template's
    # two-column list, .materials-table)
    for lead in ('By Dr Maria Montessori:', 'By Dr Maria Montessori -'):
        p = next((x for x in main.find_all('p') if norm(x.get_text()) == lead), None)
        if p is None: report.append(('settings', 'line "%s" not in the 1 Nov Word file as written before (nothing to do)' % lead, '')); continue
        ul = p.find_next_sibling()
        if ul is None or ul.name != 'ul':   # 2 Nov: report what the 1 Nov Word file gives there, instead of stopping the build
            report.append(('settings', 'WARNING: no list after "%s" - found %s' % (lead, ul.name if ul is not None else 'nothing'), '')); continue
        # 22:5x (checker b8 faults 2-4): the template's two-column list is at most 640 px wide - titles broke ("Vol." / "1"),
        # the columns sat 8 px apart in height and squeezed on phones; the lists stay in one column, as the other lists on the page
        report.append(('settings', 'list kept in one column (the template\'s two-column list is too narrow for these titles)', lead))

    # 2 Nov (checker, 2 Nov build 1, faults 1-2): the 1 Nov Word file has the Key Principles / Key Areas labels as their own
    # paragraphs (no tab), so each label sat between two paragraph gaps; the label goes on the line straight above its text, as the
    # live page and the PDF (label, then its text, then the gap)
    for head in ('Key Principles Summarised', 'Key Areas and Examples of Materials'):
        h = next((x for x in main.find_all('h2') if norm(x.get_text()).replace('Summarized', 'Summarised') == head), None)
        if h is None: continue
        sec = h.find_parent('section'); n = 0
        for lab in list(sec.find_all('p', recursive=False)):
            kids = [c for c in lab.contents if not (isinstance(c, NavigableString) and not c.strip())]
            if len(kids) == 1 and getattr(kids[0], 'name', None) == 'em':
                nx = lab.find_next_sibling()
                if nx is not None and nx.name == 'p' and nx.find('em') is None:
                    lab.append(s.new_tag('br'))
                    for c in list(nx.contents): lab.append(c.extract())
                    nx.decompose(); n += 1
        report.append(('settings', 'label on the line straight above its text, as live and the PDF (2 Nov checker fault 2): %d' % n, head))
    # the reading lists: the book titles under each "By Dr Maria Montessori" line set as one block, line under line, as the PDF
    # (single-spaced, a gap only before the next "By ..." line); live had bullets, which the 1 Nov Word file no longer has
    for lead in ('By Dr Maria Montessori:', 'By Dr Maria Montessori'):
        bp = next((x for x in main.find_all('p') if norm(x.get_text()) == lead), None)
        if bp is None: continue
        group = []; nx = bp.find_next_sibling()
        while nx is not None and nx.name == 'p' and not norm(nx.get_text()).startswith('By ') and norm(nx.get_text()) and not nx.get('class'):
            group.append(nx); nx = nx.find_next_sibling()
        if len(group) > 1:
            first = group[0]
            for g in group[1:]:
                first.append(s.new_tag('br'))
                for c in list(g.contents): first.append(c.extract())
                g.decompose()
        report.append(('settings', 'book titles under "%s" set line under line, as the PDF (2 Nov checker fault 1): %d titles' % (lead, len(group)), ''))

    # owner 2 Nov 15:52: "make the space between the author and the title the same as between the titles. also remove the colons after
    # all the author names" - each "By ..." line joins the paragraph of titles under it (a line break, so the gap is the titles' own),
    # and loses its colon
    nby = 0
    for bp in [x for x in main.find_all('p') if re.match(r'By [A-Z]', norm(x.get_text())) and len(norm(x.get_text())) < 60 and not x.get('class')]:
        for t in bp.find_all(string=True)[::-1]:
            if t.strip():
                if t.rstrip().endswith(':'): t.replace_with(NavigableString(t.rstrip()[:-1].rstrip()))
                break
        nx = bp.find_next_sibling()
        if nx is not None and nx.name == 'p' and not nx.get('class') and norm(nx.get_text()) and not norm(nx.get_text()).startswith('By '):
            bp.append(s.new_tag('br'))
            for c in list(nx.contents): bp.append(c.extract())
            nx.decompose(); nby += 1
    report.append(('settings', 'author line joined to its titles, no colon (owner 2 Nov 15:52)', str(nby)))

    # owner 2 Nov 15:54 (queued 15:53): "Remove all dividers above these headings" - no beige line straight above a green heading
    nrm = 0
    for r in main.select('.beige-rule'):
        nx = r.find_next_sibling()
        while nx is not None and nx.name == 'div' and not nx.get_text(strip=True) and not nx.find('img'): nx = nx.find_next_sibling()
        if nx is None and r.parent is not None and r.parent.name == 'section':
            ns = r.parent.find_next_sibling(); nx = ns.find(True) if ns is not None else None
        if nx is not None and nx.name == 'section': nx = nx.find(True)   # a line between two sections: the next section's first element
        if nx is not None and nx.name == 'h2':
            r.decompose(); nrm += 1   # the space above it: the template (owner 2 Nov 16:08)
    report.append(('settings', 'beige lines above green headings left out (owner 2 Nov 15:54)', str(nrm)))

    # owner 2 Nov 15:56 (queued): "The Montessori Foundation should be in blue, and the spacing should match the spacing under The Montessori
    # Bibliography Online, just above" - the heading as the MBO heading above it: the template's blue heading, no red class
    for h in main.find_all('h2'):
        if norm(h.get_text()) == 'The Montessori Foundation':
            h['class'] = [c for c in (h.get('class') or []) if c != 'mm-hc-EE0000']
            if not h['class']: del h['class']
            report.append(('settings', 'The Montessori Foundation blue, as The Montessori Bibliography Online (owner 2 Nov 15:56)', ''))

    # fault 18: Word's superscript "th"
    for t in main.find_all(string=re.compile(r'20th Century')):
        a, b = t.split('20th', 1); sp_ = s.new_tag('sup'); sp_.string = 'th'
        t.replace_with(NavigableString(a + '20'), sp_, NavigableString(b))   # 22:5x: a real tag, so "th" stays after "20" (checker b8 fault 1)
        report.append(('settings', 'superscript as Word (page setting)', '20th Century'))

    # 1 Nov (checker b11 fault 9): the quoted summary under "A Resource for the Global Montessori Community" and its badge
    # is a description, as every other text under a title and badge on the page (the template's res-desc)
    q = next(x for x in main.find_all('p') if norm(x.get_text()).startswith('\u2018The Montessori Bibliography Online (MBO)'))
    q['class'] = ['res-desc']
    # 1 Nov (checker b11 faults 4, 5): a word joiner before the badges was tried and does not stop the browser wrapping a badge
    # alone on phones (the badges are boxes); that needs a template rule - not done here

    # 1 Nov (checker b14 fault 1): Word's blank line before the italic note "'Other Books of Interest'- in case ..." (PDF page 3),
    # so the note is not read as a fifth book; an empty line, as Word's empty paragraph
    note = next(x for x in main.find_all('p') if norm(x.get_text()).startswith('\u2018Other Books of Interest\u2019'))
    note.insert_before(BeautifulSoup('<p><br/></p>', 'html.parser'))
    em = note.find('em')   # the dash written against the quote ("'-"), spaced as the site's other dashes (typo rule)
    if em is not None and em.string and em.string.endswith('\u2019- '): em.string = em.string[:-2] + ' - '
    report.append(('settings', 'blank line before the Other Books of Interest note, as Word', 'b14 fault 1'))

    # fault 17: the AI / P / E key lines indented as Word (the template's 24px spacer, twice)
    p = next(x for x in main.find_all('p') if norm(x.get_text()).startswith('AI = Assistance to Infancy'))
    sp = '<span class="mm-lsp"> </span><span class="mm-lsp"> </span>'
    html = p.decode_contents().replace('<br/>', '<br/>' + sp)
    p.clear(); p.append(BeautifulSoup(sp + html, 'html.parser'))
    report.append(('settings', 'key lines indented as Word (page setting)', 'AI / P / E'))

    # owner 1 Nov 03:47: "Delete the whole Montessori World Educational Institute section" - its heading, introduction and the
    # book lists under its nine sub-headings (Child Development/Learning ... On The Subject of Montessori Education) go; the
    # beige line and the chronological list after it stay, joined to the section before
    first = main.find(id='the-montessori-world-educational-institute')
    last = main.find(id='on-the-subject-of-montessori-education')
    if first is None and last is None and not any(norm(x.get_text()).startswith('Here\u2019s a different perspective') for x in main.find_all('p')):
        # 2 Nov: the owner removed the section from the 1 Nov Word file herself - nothing to leave out
        report.append(('settings', 'Montessori World Educational Institute section: not in the 1 Nov Word file (removed by the owner) - nothing left out', ''))
        _post_tail(main, s, report, norm); return
    assert first is not None and last is not None
    prev = first.find_previous_sibling('section')
    n = 0
    while True:
        nxt = first.find_next_sibling('section')
        if first is last: break
        first.decompose(); n += 1; first = nxt
    kids = [c for c in last.children if getattr(c, 'name', None)]
    k = next(i for i, c in enumerate(kids) if 'beige-rule' in (c.get('class') or []))
    for c in kids[:k]: c.decompose()
    for c in list(last.contents): prev.append(c.extract())
    last.decompose()
    # its lead-in line "Here's a different perspective on what constitutes a Reading List..." (Word: between two beige lines, just
    # before the section heading) goes with it, with one of its two beige lines (checker b17 fault 1)
    lead = next(x for x in main.find_all('p') if norm(x.get_text()).startswith('Here\u2019s a different perspective'))
    nx = lead.find_next_sibling()
    assert nx is not None and 'beige-rule' in (nx.get('class') or [])
    nx.decompose(); lead.decompose()
    report.append(('settings', 'Montessori World Educational Institute section left out (owner 1 Nov 03:47 "Delete the whole ... section"): %d sections' % (n + 1), ''))

    _post_tail(main, s, report, norm)


def _post_tail(main, s, report, norm):
    # code check (fault 20): only the template's classes and settings in the content
    for e in main.select('span.mm-wcol'):
        st = (e.get('style') or '').upper()
        if any(b in st for b in BLUES): e['class'] = ['mm-blue']; del e['style']
        elif any(r in st for r in REDS): e['class'] = ['mm-hc-EE0000']; del e['style']
        else: e.unwrap()
    for e in main.select('.mm-form, .mm-wordline'):
        e['class'] = [c for c in e['class'] if c not in ('mm-form', 'mm-wordline')]
        if not e['class']: del e['class']
    for h in main.select('h2.mm-hc-0432FF'):   # a blue Word heading takes the template's own heading colour (the Resources template has no blue heading class)
        h['class'] = [c for c in h['class'] if c != 'mm-hc-0432FF']
        if not h['class']: del h['class']
    for f in main.select('figure[style]'):   # --h is not read by the template (--hp is)
        f['style'] = ';'.join(x for x in f['style'].split(';') if x.strip() and not x.strip().startswith('--h:'))
    for a in main.find_all('a'):   # every PDF link is the template's PDF badge
        if norm(a.get_text()) == 'PDF' and 'pdf' not in (a.get('class') or []): a['class'] = (a.get('class') or []) + ['pdf']
    report.append(('settings', 'Word colours as the template\'s classes; PDF links as badges (page setting)', 'fault 20'))

def _drop_covers_grid(main, report):
    """Owner 31 Oct 22:14: "delete that grid . don't use it on the page" - the Word table of 23 covers with their titles
    is left out, with the line picture (623 x 2) the converter had placed as an image just above it."""
    t = main.select_one('div.mm-table-wrap')
    if t is None: report.append(('settings', 'covers grid: not in the 1 Nov Word file (removed by the owner) - nothing left out', '')); return
    prev = t.find_previous_sibling()
    if prev is not None and 'mm-float' in (prev.get('class') or []) and prev.find('img') is not None:
        prev.decompose()
    t.decompose()
    # owner 31 Oct 22:29 "remove it": the line "By Maria Montessori" that introduced the grid goes too
    by = [x for x in main.find_all('p') if x.get_text(strip=True) == 'By Maria Montessori']
    if len(by) == 1: by[0].decompose(); report.append(('settings', 'line "By Maria Montessori" left out (owner 31 Oct 22:29 "remove it")', ''))
    else: report.append(('settings', 'WARNING: "By Maria Montessori" line found %d times' % len(by), ''))
    # owner 1 Nov 02:58 ("Obviously it should go ... YES!"): the beige line that came after the grid goes, so "This list comes
    # from Montessori Album" no longer sits alone between two lines
    src = next((x for x in main.find_all('p') if x.get_text(strip=True).startswith('This list comes from')), None)
    nx = src.find_next_sibling() if src is not None else None
    if nx is not None and 'beige-rule' in (nx.get('class') or []): nx.decompose(); report.append(('settings', 'beige line after the grid left out (owner 1 Nov 02:58)', ''))
    else: report.append(('settings', 'WARNING: beige line after "This list comes from" not found', ''))
    report.append(('settings', 'covers grid left out (owner 31 Oct 22:14 "delete that grid . don\'t use it on the page")', ''))

# 31 Oct 22:3x: the contents box lists the page's main sections only - the headings in Word's red and green (the colours the
# Word file gives its section headings); the blue sub-headings (Stress, Nutrition ...) stay on the page as headings
# owner 1 Nov 03:47 "No table of contents" (the template hides its empty contents box; this list is no longer used)
NO_TOC = True
TOC_ONLY = ['So many books, so little time', 'Bibliography', 'The Montessori Foundation']

# 31 Oct 22:5x: typo corrected (owner 27 Oct: "correct all typos on every page. do not ask about this again"): "**whole child" -> "whole child"
TEXT_EDITS = [('**whole child', 'whole child'),
              # 1 Nov (checker b12 fault 7; owner: UK spelling, typos corrected without asking)
              ('not to mold them', 'not to mould them'), ('focus toward the', 'focus towards the'),
              # 1 Nov (checker b13 faults 1-5): typos corrected (owner 27 Oct: "correct all typos on every page")
              ('an authorative/', 'an authoritative/'),
              ('responsibility, and social contribution', 'responsibility, and social contribution.'),
              ('act as respectful guides', 'act as respectful guides.'),
              ('in London -having just returned', 'in London - having just returned'), ('in India- which', 'in India - which'),
              ('future directions for the MBO.', 'future directions for the MBO.\u2019'),
              # (checker b13 fault 6; owner 26 Oct: words inside a quotation stay as written) - the site's UK spelling
              # rule had changed them; put back as the quoted source writes them
              ('training centre in North America', 'training center in North America'),
              ('links to digitised source materials', 'links to digitized source materials'),
              ('hyperlinks to digitised source material', 'hyperlinks to digitized source material'),
              # (checker b13 fault 9): number ranges kept on one line (non-breaking hyphen U+2011, which looks the same)
              ('aged 3-6', 'aged 3\u20116'), ('ages 12-18', 'ages 12\u201118'), ('AMI\u2019s 3-6', 'AMI\u2019s 3\u20116'),
              ('ages 7-12', 'ages 7\u201112'), ('June 1-12', 'June 1\u201112'), ('ages 0-3', 'ages 0\u20113'), ('ages 3-6', 'ages 3\u20116')]
