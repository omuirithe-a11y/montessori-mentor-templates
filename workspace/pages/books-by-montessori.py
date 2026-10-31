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
    """Word pieces -> HTML: links as links (PDF links as the template's PDF badge), blue as mm-blue, red as mm-hc-FF0000,
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
        elif col in REDS: h = '<span class="mm-hc-FF0000">%s</span>' % h
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

    # faults 9-13, 15: the chronological list rebuilt from the Word file, one line per Word paragraph, in the template's
    # label line (p.mm-hanglab, the year in its .mm-lab column, red; titles blue; PDF links as the template's badges);
    # every description under its title (an empty label, so it starts in the title column)
    w0 = next(i for i, p in enumerate(paras) if p.text.strip().startswith('The following is a chronological list'))
    w1 = next(i for i, p in enumerate(paras) if i > w0 and p.text.strip().startswith('This list comes from'))
    start = next(e for e in main.find_all('p') if norm(e.get_text()).startswith('The following is a chronological list'))
    stop = next(e for e in start.find_all_next() if e.name == 'div' and 'beige-rule' in (e.get('class') or []))
    nodes = []
    for e in list(start.find_all_next()):
        if e is stop: break
        if e.parent is not None and e.parent.name in ('section', 'main') and e.name in ('p', 'div', 'ul'): nodes.append(e)
    for e in nodes: e.extract()
    out = []; n_e = n_d = 0
    for p in paras[w0 + 1:w1]:
        pcs = _runs(p, qn)
        if not ''.join(x[0] for x in pcs).strip(): continue
        if _is_entry(pcs):
            y, rest = _year_split(pcs)
            lab = '<span class="mm-hc-FF0000">%s</span>' % y if y else ''
            out.append('<p class="mm-hanglab"><span class="mm-lab">%s</span>%s</p>' % (lab, _pieces_html(rest))); n_e += 1
        else:
            out.append('<p class="mm-hanglab"><span class="mm-lab"></span>%s</p>' % _pieces_html(pcs)); n_d += 1
    frag = BeautifulSoup(''.join(out), 'html.parser')
    for x in list(frag.contents)[::-1]: start.insert_after(x)
    report.append(('settings', 'chronological list rebuilt from Word: %d title lines, %d descriptions (page setting)' % (n_e, n_d), 'faults 9-13, 15'))

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
        for o, (lab, txt) in zip(old, lines):
            o.replace_with(BeautifulSoup('<p class="mm-hanglab"><span class="mm-lab"><em>%s</em></span>%s</p>' % (_esc(lab), _esc(txt)), 'html.parser'))
        report.append(('settings', 'label lines rebuilt from Word, labels italic (page setting)', head))

    # fault 7: Required Readings and Recommended Readings by Maria Montessori in two columns, as Word (the template's
    # two-column list, .materials-table)
    for lead in ('By Dr Maria Montessori:', 'By Dr Maria Montessori -'):
        p = next(x for x in main.find_all('p') if norm(x.get_text()) == lead)
        ul = p.find_next_sibling()
        assert ul is not None and ul.name == 'ul', lead
        ul['class'] = (ul.get('class') or []) + ['materials-table']
        report.append(('settings', 'list in two columns, as Word (page setting)', lead))

    # fault 18: Word's superscript "th"
    for t in main.find_all(string=re.compile(r'20th Century')):
        a, b = t.split('20th', 1); t.replace_with(NavigableString(a), BeautifulSoup('20<sup>th</sup>', 'html.parser'), NavigableString(b))
        report.append(('settings', 'superscript as Word (page setting)', '20th Century'))

    # fault 17: the AI / P / E key lines indented as Word (the template's 24px spacer, twice)
    p = next(x for x in main.find_all('p') if norm(x.get_text()).startswith('AI = Assistance to Infancy'))
    sp = '<span class="mm-lsp"> </span><span class="mm-lsp"> </span>'
    html = p.decode_contents().replace('<br/>', '<br/>' + sp)
    p.clear(); p.append(BeautifulSoup(sp + html, 'html.parser'))
    report.append(('settings', 'key lines indented as Word (page setting)', 'AI / P / E'))

    # code check (fault 20): only the template's classes and settings in the content
    for e in main.select('span.mm-wcol'):
        st = (e.get('style') or '').upper()
        if any(b in st for b in BLUES): e['class'] = ['mm-blue']; del e['style']
        elif any(r in st for r in REDS): e['class'] = ['mm-hc-FF0000']; del e['style']
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
    if t is None: report.append(('settings', 'WARNING: covers grid not found', '')); return
    prev = t.find_previous_sibling()
    if prev is not None and 'mm-float' in (prev.get('class') or []) and prev.find('img') is not None:
        prev.decompose()
    t.decompose()
    report.append(('settings', 'covers grid left out (owner 31 Oct 22:14 "delete that grid . don\'t use it on the page")', ''))
