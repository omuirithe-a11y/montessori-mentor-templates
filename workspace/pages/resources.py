# 8.0 Resources - page settings (2 Nov 2026, Resources Code Template f0bac9f8)
# Word file: 8.0 Resources.docx (Drive 1VvsC3z6H7LyuVxXXpqGSqdfL5KjgxWab, saved 1 Nov 14:14, sha256 e342d1f6...); PDF 15f9b9f3...
# Owner 2 Nov 08:40: "8.0 resources has been changed. The updated files are in Google drive. Rebuilding editing the page is the first task".
# Her note in the Word file (left out, not page text): "there is no Table of Contents on this page: instead, the four blue
# headings are to be links to the four resources pages. Four, not three: I have added an extra page".
# Owner 2 Nov 08:44: addresses "yes" - /books-of-interest/, /picture-books/, /websites/ (Books by Maria Montessori: /books-by-montessori/).
# Owner 2 Nov 08:45: "Four sections".

NO_TOC = True
LISTS = [('Education (including Montessori)', 'Book Lists etc.'), ('Executive Functions,', 'Ambitious Teaching.'),
         ('Introductions to Montessori,', 'Parenting, etc.')]   # owner 2 Nov 15:59 (queued)
DROP = ['[ Claude:']

TEXT_EDITS = [('It is divided into two sections:', 'It is divided into four sections:')]   # owner 2 Nov 08:45 "Four sections"
# "organizations" -> "organisations": done by the build's own UK-spelling rule

HEADING_LINKS = {'Books by Maria Montessori': '/books-by-montessori/',
                 'Books of Interest': '/books-of-interest/',
                 'Picture Books': '/picture-books/',
                 'Websites': '/websites/'}


def POST_MAIN(main, s, report):
    import re
    norm = lambda x: re.sub(r'\s+', ' ', x).strip()
    hs = main.find_all('h2')
    # Word paragraph 12 "Picture Books" is BLACK (a line under Books of Interest, PDF line 332); the converter made it a heading
    # because its words match the blue heading further down. It goes back to a plain line and its section joins Books of Interest.
    pb = [h for h in hs if norm(h.get_text()) == 'Picture Books']
    assert len(pb) == 2, len(pb)
    first = pb[0]; sec = first.find_parent('section'); prev = sec.find_previous_sibling('section')
    assert prev is not None and prev.get('id') == 'books-of-interest'
    p = s.new_tag('p'); p.string = 'Picture Books'; first.replace_with(p)
    for c in list(sec.contents): prev.append(c.extract())
    sec.decompose()
    report.append(('settings', 'black "Picture Books" line under Books of Interest kept a line, not a heading (Word: black; PDF)', ''))
    # owner's note in the Word file: "the four blue headings are to be links to the four resources pages"; addresses owner 2 Nov 08:44
    n = 0
    for h in main.find_all('h2'):
        t = norm(h.get_text())
        if t in HEADING_LINKS:
            h['class'] = [c for c in (h.get('class') or []) if c != 'mm-hc-0432FF']   # the Resources template has no such class
            if not h['class']: del h['class']
            a = s.new_tag('a', href=HEADING_LINKS[t]); a.string = t
            h.clear(); h.append(a); n += 1
    assert n == 4, n
    report.append(('settings', 'the four blue headings made links to the four resources pages (owner\'s Word note; addresses 2 Nov 08:44)', str(n)))
    # the inline first-line indent the converter wrote on the last line (the template allows no inline style in the content)
    for e in main.find_all(style=True):
        if 'text-indent' in e['style']: del e['style']; report.append(('settings', 'inline indent left out (template rule)', norm(e.get_text())[:40]))
    # owner 2 Nov 15:59 (queued 15:53): "The spacing between the heading and the first item on the list (Education (including Montessori)
    # is good. Make this the same spacing between all items in the lists." - the items of each list set line under line in one paragraph
    # (the line spacing is the gap the heading has to the first item; measured after the build)
    from bs4 import BeautifulSoup as _BS
    for first, last in LISTS:
        ps = [x for x in main.find_all('p')]
        i = next((k for k, x in enumerate(ps) if norm(x.get_text()) == first), None)
        j = next((k for k, x in enumerate(ps) if norm(x.get_text()) == last), None)
        if i is None or j is None or j <= i: report.append(('settings', 'WARNING: list not found', first)); continue
        head = ps[i]
        for x in ps[i + 1:j + 1]:
            head.append(_BS('<br/>', 'html.parser'))
            for c in list(x.contents): head.append(c.extract())
            x.decompose()
        report.append(('settings', 'list items line under line (owner 2 Nov 15:59)', '%s ... %s' % (first, last)))
