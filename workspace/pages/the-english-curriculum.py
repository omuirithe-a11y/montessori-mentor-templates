# 3.5.0 The English Curriculum - page settings (4 Nov 2026). Essay Code Template (owner 15:30 "Build it using the essai template").
# Word file: Drive "3.5.0 The English Curriculum.docx" (uploaded 4 Nov 17:50, sha256 183a9075); PDF f204969d. Page title and hero
# title "The English Curriculum" (owner 18:09). Hero: the image she sent 18:14 (language shelves, sha256 97e3f429). Address
# /the-english-curriculum/ (follows the other curriculum pages). A new page with no live version: the no-live checks and gate.
# Faces: 165 images; 51 images are "no blurring" by her screenshots (19:09 "yes"); the rest go through the rounds.
# Preview build from the round 1 blurred images agreed 18:08 ("yes"), record pages/the-english-curriculum-faces-preview.json.
# 4 Nov 21:5x (build 2): fixes for the separate review of build 1 (claude/checks/english-curriculum-b1-faults.md, 45 faults),
# each settled by a rule: the PDF/Word decide what is a heading and its colour, the template decides sizes and spacing.
import re as _re
from bs4 import BeautifulSoup as _BS

TEXT_EDITS = [   # UK spelling (owner 13 Oct, 26 Oct 15:54): "practice" as a verb is "practise"
    ('to practice copying', 'to practise copying'), ('to practice reading', 'to practise reading'),
    ('to practice colouring', 'to practise colouring'), ('Practice left to right', 'Practise left to right'),
]
PAGE_CODE_REPLACE = []
ALT_TEXT = {}            # owner 28 Oct: image descriptions "are not necessary anymore"
CSS = ""
# objects on a white background have the white masked (owner's rule); cards with words and printed pages keep their white
MASK_WHITE = ['image13.jpg', 'image46.jpg', 'image156.jpg', 'image166.png', 'image144.png', 'image148.jpg']

# label widths at 1440 (measured on build 1 in the page font, 4 Nov 21:5x) - for the Symbol Box columns, which Word sets with tab stops
_LABW = {'2 very large red circles': 148, '2 large black circles': 130.3, '2 medium black circles': 155.8, '8 medium orange circles': 166,
         '1 small black circle': 127.8, '1 blue triangle': 97.6, '1 black triangle': 104}


def _t(e): return _re.sub(r'\s+', ' ', e.get_text()).strip()


def SOUP_FIX(sp, report):
    m = sp
    def frag(h): return list(_BS(h, 'html.parser').contents)
    def replace(el, h):
        new = frag(h)
        for n in new: el.insert_before(n)
        el.decompose(); return new[0]
    def merge_section(el):   # a heading made a line: its section joins the one before (the contents box lists headings only)
        sec = el.find_parent('section')
        if sec is None: return
        prev = sec.find_previous_sibling('section')
        if prev is None or sec.find('h2') is not None: return
        for c in list(sec.contents): prev.append(c.extract())
        sec.decompose()
    h2s = {}
    for h in m.find_all('h2'): h2s.setdefault(_t(h), []).append(h)
    def H(text, k=0):
        L = [h for t, hs in h2s.items() if t.startswith(text) for h in hs]
        return L[k] if k < len(L) else None
    def demote(text, k, h):
        el = H(text, k)
        if el is None: report.append(('settings', 'WARNING: heading to make a line not found', '%s #%d' % (text, k))); return None
        n = replace(el, h); merge_section(n); report.append(('settings', 'heading made a line, as the PDF', '%s #%d' % (text, k))); return n
    # fetch everything first (occurrences counted on build 1's headings)
    plan = [('Keys to Literacy', 0, '<div class="micro-label mm-hc-0432FF">Keys to Literacy</div>'),
            ('Metal Insets', 0, '<p>Metal Insets</p>'), ('Word Study', 0, '<p>Word Study</p>'), ('Reading Analysis', 0, '<p>Reading Analysis</p>'),
            ('Enrichment of Vocabulary', 1, '<p><u>Enrichment of Vocabulary</u></p>'), ('Expansion of Oral Language', 1, '<p><u>Expansion of Oral Language</u></p>'),
            ('Spoken Language', 1, '<p><u>Spoken Language</u></p>'), ('Spoken Language', 2, '<p><u>Spoken Language</u></p>'),
            ('Metal Insets', 2, '<p><em>Metal Insets</em></p>'), ('Early Readers', 0, '<p>Early Readers</p>'),
            ('Blue Language Materials', 0, '<div class="micro-label mm-hc-0432FF">Blue Language Materials</div>'),
            ('Series 1', 0, '<p class="mm-hanglab"><span class="mm-lab mm-hc-0432FF">Series 1 </span><span class="mm-hc-0432FF">Subject and Verb</span></p>'),
            ('Series 2', 0, '<p class="mm-hanglab"><span class="mm-lab mm-hc-0432FF">Series 2 </span><span class="mm-hc-0432FF">Subject, Verb, Object</span></p>')]
    targets = [(H(t, k), h, t, k) for t, k, h in plan]
    kl = H('Keys to Literacy', 1); wr = H('Writing', 1) if (H('Writing', 1) is not None and _t(H('Writing', 1)) == 'Writing') else None
    lb = H('Letter Bingo', 0)
    for el, h, t, k in targets:
        if el is None: report.append(('settings', 'WARNING: heading to make a line not found', '%s #%d' % (t, k))); continue
        n = replace(el, h); merge_section(n); report.append(('settings', 'heading made a line, as the PDF', '%s #%d' % (t, k)))
    # red headings as Word and the PDF (Keys to Literacy, the second Writing)
    for el in (kl, wr):
        if el is not None: el['class'] = [c for c in (el.get('class') or []) if not c.startswith('mm-hc-')] + ['mm-hc-EE0000']; report.append(('settings', 'heading red, as Word', _t(el)))
    # Letter Bingo: two blue captions, each over its two images (PDF p10), not one heading
    if lb is not None:
        row = lb.find_next_sibling('div')
        figs = row.select('figure') if row is not None else []
        if len(figs) == 4:
            h = ('<div class="mm-wcols2"><div><p class="centred mm-hc-0432FF">Letter Bingo: learning</p><div class="mm-row" data-above="40" data-level="1"><div class="mm-imgs">%s%s</div></div></div>'
                 '<div><p class="centred mm-hc-0432FF">Letter Bingo: teaching</p><div class="mm-row" data-above="40" data-level="1"><div class="mm-imgs">%s%s</div></div></div></div>') % tuple(str(f) for f in figs)
            row.decompose(); n = replace(lb, h); merge_section(n); report.append(('settings', 'Letter Bingo: two captions over two pairs of images, as the PDF', ''))
    # Series 3-5: blue, as Series 1-2 and the PDF
    for p in m.select('p.mm-hanglab'):
        lab = p.find('span', class_='mm-lab')
        if lab is not None and _re.match(r'Series [345]\b', _t(lab)):
            lab['class'] = lab['class'] + ['mm-hc-0432FF']
            rest = [c for c in p.contents if c is not lab]
            sp_ = sp.new_tag('span', attrs={'class': 'mm-hc-0432FF'})
            for c in rest: sp_.append(c.extract())
            p.append(sp_)
    # blue lines as the PDF
    for p in m.find_all('p'):
        if _t(p) in ('Homophones, weakly',) or _t(p).startswith('A sample of some useless'):
            p['class'] = (p.get('class') or []) + ['mm-hc-0432FF']
    # pink and green list titles in their Word colours (FF40FF, 2AB116), as the PDF - see the open question on colours the template lacks
    for d in m.select('div.micro-label'):
        if _t(d) == 'Pink Language Materials': d['style'] = 'color:#FF40FF'
        if _t(d) == 'Green Language Materials': d['style'] = 'color:#2AB116'
    # Writing Stages list (PDF p15): Word's italic items; the strip image beside the list (one set with it)
    wsl = [d for d in m.select('div.micro-label') if _t(d) == 'Writing Stages']
    if len(wsl) >= 2:
        d = wsl[-1]; items = []; x = d.find_next_sibling()
        fl = None
        while x is not None and len(items) < 14:
            if x.name == 'div' and 'mm-float' in (x.get('class') or []) and fl is None: fl = x; x = x.find_next_sibling(); continue
            if x.name != 'p' or len(_t(x)) > 60: break
            items.append(x); x = x.find_next_sibling()
        for p in items:
            if _t(p) in ('Metal Insets', 'Writing Letters', 'Placement of Letters', 'Writing Copies') and p.find('em') is None:
                em = sp.new_tag('em')
                for c in list(p.contents): em.append(c.extract())
                p.append(em)
        if fl is None:
            nx = d.find_next_sibling()
            fl = nx if (nx is not None and 'mm-float' in (nx.get('class') or [])) else None
        if fl is None:   # the float may stand before the label
            pv = d.find_previous_sibling()
            fl = pv if (pv is not None and 'mm-float' in (pv.get('class') or [])) else None
        if fl is not None:
            fig = fl.find('figure'); fl.extract()
            st = sp.new_tag('div', attrs={'class': 'mm-set mm-col', 'data-h': '430'})
            tx = sp.new_tag('div', attrs={'class': 'mm-text'}); im = sp.new_tag('div', attrs={'class': 'mm-imgs'})
            d.insert_before(st); tx.append(d.extract())
            for p in items: tx.append(p.extract())
            im.append(fig); st.append(tx); st.append(im)
            report.append(('settings', 'Writing Stages list with the tall image beside it, as the PDF', ''))
    # Pinning: the side image and its paragraph as one set, so the row of five below starts after it
    pin = next((h for h in m.find_all('h2') if _t(h) == 'Pinning'), None)
    if pin is not None:
        fl = pin.find_next_sibling(); para = fl.find_next_sibling() if fl is not None else None
        if fl is not None and 'mm-float' in (fl.get('class') or []) and para is not None and para.name == 'p':
            fig = fl.find('figure'); st = sp.new_tag('div', attrs={'class': 'mm-set mm-col', 'data-h': '168'})
            tx = sp.new_tag('div', attrs={'class': 'mm-text'}); im = sp.new_tag('div', attrs={'class': 'mm-imgs'})
            fl.insert_before(st); tx.append(para.extract()); im.append(fig.extract()); fl.decompose(); st.append(tx); st.append(im)
            report.append(('settings', 'Pinning: side image and its paragraph as one set', ''))
    # Word Study cards (PDF p21): the three cards stood beside the lines and overlapped; one row of the three after the list
    cards = [m.select_one('img[data-full="images/%s.jpg"]' % n) for n in ('155', '156', '157')]
    if all(cards):
        flo = [c.find_parent('div', class_='mm-float') for c in cards]
        last = next((p for p in m.select('p.mm-hanglab') if _t(p).startswith('Word Families')), None)
        if last is not None and all(flo):
            row = _BS('<div class="mm-row" data-above="40" data-level="1"><div class="mm-imgs"></div></div>', 'html.parser').div
            for c in cards: row.select_one('.mm-imgs').append(c.find_parent('figure').extract())
            for f in flo: f.decompose()
            last.insert_after(row); report.append(('settings', 'Word Study cards: one row after the list (they overlapped beside it)', ''))
    # p19: the four labels each over its image (Blue Series, Green Series, Action Cards - Set 2, Puzzle Words)
    lab = next((p for p in m.find_all('p') if _t(p).startswith('The Blue Series')), None)
    if lab is not None:
        imgs = {n: m.select_one('img[data-full="images/%s.jpg"]' % n) for n in ('145', '146', '147', '148')}
        if all(imgs.values()):
            caps = [('146', '<strong>The Blue Series</strong>'), ('145', 'The Green Series'), ('147', 'Action Cards - Set 2'), ('148', '<strong>Puzzle Words</strong> (aka Sight Words)')]
            figs = []
            for n, cap in caps:
                f = imgs[n].find_parent('figure'); old = f.find_parent('div', class_=['mm-float', 'mm-row'])
                f = f.extract(); f['class'] = (f.get('class') or []) + ['mm-cf']
                f.insert(0, _BS('<figcaption class="mm-cap">%s</figcaption>' % cap, 'html.parser').figcaption); figs.append(f)
                if old is not None and not old.find('figure'): old.decompose()
            row = _BS('<div class="mm-row" data-above="40" data-level="1"><div class="mm-imgs"></div></div>', 'html.parser').div
            for f in figs: row.select_one('.mm-imgs').append(f)
            lab.insert_before(row); lab.decompose(); report.append(('settings', 'p19: each label over its image, as the PDF', ''))
    # an image Word uses twice: placed at both places (p2 beside the text: image1 = 046; p19 Early Readers row: image136 = 134, 4th of 5)
    f1 = m.select_one('img[data-full="images/001.jpg"]'); f46 = m.select_one('img[data-full="images/046.jpg"]')
    if f1 is not None and f46 is not None:
        f1.find_parent('figure').insert_after(_BS(str(f46.find_parent('figure')), 'html.parser').figure); report.append(('settings', 'image1 (046) also beside the p2 text, as Word', ''))
    f134 = m.select_one('img[data-full="images/134.jpg"]'); f152 = m.select_one('img[data-full="images/152.jpg"]')
    if f134 is not None and f152 is not None:
        f152.find_parent('figure').insert_before(_BS(str(f134.find_parent('figure')), 'html.parser').figure); report.append(('settings', 'image136 (134) also in the Early Readers row, as Word', ''))
    # Grapheme: a label line like Phoneme above it (the leading tab had been dropped: "GraphemeThe")
    for p in m.select('p.mm-under'):
        if _t(p).startswith('Grapheme'):
            em = p.find('em'); h = '<p class="mm-hanglab"><span class="mm-lab">Grapheme </span>%s</p>' % (str(em) if em else '')
            replace(p, h); report.append(('settings', 'Grapheme as a label line, as Phoneme', ''))
    # Symbol Box lists (PDF p22-23): every line indented as Word; Circles and Triangles values in one column (Word's tab stop)
    for d in m.select('div.micro-label'):
        kind = _t(d)
        if kind not in ('Circles', 'Triangles', 'Arrows'): continue
        x = d.find_next_sibling(); lines = []
        while x is not None and x.name in ('p', 'blockquote') and not (x.name == 'div'):
            lines.append(x); x = x.find_next_sibling()
            if x is not None and x.name == 'div': break
        for ln in lines:
            txt = _t(ln)
            if kind == 'Arrows':
                mq = _re.match(r'^(.*?\bquestions?\s)(.*)$', txt)
                body = (mq.group(1), mq.group(2)) if mq else (txt, '')
                pre = body[0].replace('blue', '<span class="mm-hc-0432FF">blue</span>', 1) if body[0].startswith('1 blue') else body[0]
                h = '<p><span class="mm-t">␉</span>%s%s</p>' % (pre, ('<em>%s</em>' % body[1]) if body[1] else '')
            else:
                lab_ = ln.find('span', class_='mm-lab')
                if lab_ is not None: label, val = _t(lab_), txt[len(_t(lab_)):].strip()
                else:
                    parts = ln.get_text().split('␉'); label, val = _re.sub(r'\s+', ' ', parts[0]).strip(), _re.sub(r'\s+', ' ', ''.join(parts[1:])).strip()
                w = _LABW.get(label)
                if w is None: continue
                end = 48 + w; first = (int(end // 48) + 1) * 48; ntab = 1 + max(0, (240 - first) // 48)
                lab_h = label.replace('red', '<span class="mm-hc-EE0000">red</span>', 1).replace('blue', '<span class="mm-hc-0432FF">blue</span>', 1)
                h = '<p><span class="mm-t">␉</span>%s<span class="mm-t">%s</span>%s</p>' % (lab_h, '␉' * ntab, val)
            replace(ln, h)
        report.append(('settings', 'Symbol Box list as Word (indent, one value column)', kind))
    # Word's trailing tabs at the end of a list line ("Conversation<tab>") made those lines a different kind of paragraph: dropped
    k = 0
    for t_ in m.select('span.mm-t'):
        par = t_.find_parent('p')
        if par is None: continue
        after = ''.join(str(s) for s in t_.next_siblings) if t_.parent is par else ''
        if t_.parent is par and not _re.sub(r'<[^>]+>|\s', '', after):
            t_.decompose(); k += 1
        elif t_.parent.name == 'strong' and t_.parent.parent is par and not _re.sub(r'\s', '', ''.join(s.get_text() if hasattr(s, 'get_text') else str(s) for s in t_.next_siblings)) and not _re.sub(r'\s', '', ''.join(s.get_text() if hasattr(s, 'get_text') else str(s) for s in t_.parent.next_siblings)):
            t_.decompose(); k += 1
    report.append(('settings', "Word's trailing tabs at line ends dropped", str(k)))
