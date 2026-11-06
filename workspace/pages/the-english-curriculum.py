# 3.5.0 The English Curriculum - page settings (4 Nov 2026). Essay Code Template (owner 15:30 "Build it using the essai template").
# Word file: Drive "3.5.0 The English Curriculum.docx" (uploaded 4 Nov 17:50, sha256 183a9075); PDF f204969d. Page title and hero
# title "The English Curriculum" (owner 18:09). Hero: the image she sent 18:14 (language shelves, sha256 97e3f429). Address
# /the-english-curriculum/ (follows the other curriculum pages). A new page with no live version: the no-live checks and gate.
# Faces: 165 images; 51 images are "no blurring" by her screenshots (19:09 "yes"); the rest go through the rounds.
# Preview build from the round 1 blurred images agreed 18:08 ("yes"), record pages/the-english-curriculum-faces-preview.json.
# 4 Nov 21:5x (build 2): fixes for the separate review of build 1 (claude/checks/english-curriculum-b1-faults.md, 45 faults),
# each settled by a rule: the PDF/Word decide what is a heading and its colour, the template decides sizes and spacing.
import re as _re
WORD_FILE = '/home/claude/eng35/src/3.5.0 The English Curriculum.docx'   # the owner's Word file of 5 Nov (sha256 36a76415)
from bs4 import BeautifulSoup as _BS

TEXT_EDITS = [   # UK spelling (owner 13 Oct, 26 Oct 15:54): "practice" as a verb is "practise"
    ('to practice copying', 'to practise copying'), ('to practice reading', 'to practise reading'),
    ('to practice colouring', 'to practise colouring'), ('Practice left to right', 'Practise left to right'),
    ('the sound ....', 'the sound\u00a0....'),
    # 6 Nov (build 31 review faults 2-3; owner 27 Oct: "correct all typos on every page"; UK spelling)
    ('so they game doesn', 'so the game doesn'), ('almost a quarter an hour', 'almost a quarter of an hour'),
    ('a sense of the how extensive', 'a sense of how extensive'), ('and help child learn', 'and help the child learn'),
    ('gaining an understanding the perspective', 'gaining an understanding of the perspective'), ('circle time instills', 'circle time instils'),
    # 6 Nov 11:2x (build 32 review fault 1; owner 27 Oct typo rule)
    ('so they unconsciously they absorb', 'so they unconsciously absorb'), ('with the title’s ‘', 'with the titles ‘'),   # both lines (the quoted word is in <em>, so the match stops before it)   # 6 Nov 02:5x (wrap check PUNCT, 361-367 px): Word's space before the dots let a line start with "."; a no-break space keeps the dots with "sound"
]
PAGE_CODE_REPLACE = []
ALT_TEXT = {}            # owner 28 Oct: image descriptions "are not necessary anymore"
CSS = ""   # 5 Nov 13:38: the two page rules moved into the Essay Code Template (owner agreement)
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
    # 5 Nov (owner's new Word file of 4 Nov 22:49 UTC): Word's own "Table of Contents" list (Word paragraphs 0-7) is the
    # contents box, not page text - its seven lines leave the page; the template's contents box shows its entries in the
    # PDF's two columns (TOC_EXTRA / TOC_SPLIT below). The intro paragraph the converter put under the last entry stays.
    _tocw = ['Table of Contents', 'Spoken Language', 'Writing - Abstract', 'Keys to Literacy', 'Writing - Concrete', 'Reading Stages', 'Grammar']
    _intro = next((p for p in m.find_all('p') if _t(p).startswith('When I did my AMI training')), None)
    _gone = 0
    for h in list(m.find_all(['h2', 'p'])):
        if h is _intro: break
        if h.name in ('h2', 'p') and _t(h) in _tocw:   # 5 Nov (format review B0): "Reading Stages" came as a p and stayed at the top
            _tocw.remove(_t(h)); _sec = h.find_parent('section'); h.decompose(); _gone += 1
            if _sec is not None and not _sec.get_text(strip=True) and not _sec.find(['img', 'figure']): _sec.decompose()
    report.append(('settings', "Word's own contents list taken off the page (it is the contents box)", '%d lines' % _gone))
    # 5 Nov: what is a heading, and its colour, comes from the owner's Word file (the PDF is printed from it; one font size,
    # the levels are colours: green sections, red sub-headings, blue labels). Each heading on the page is matched, in order,
    # to the Word paragraph with the same words: a heading whose Word paragraph is black is an ordinary line (underlined or
    # italic as Word); the others take their Word colour. (The converter's own colour classes were not Word's: all four
    # "Spoken Language" came out green.)
    import docx as _docx
    _wp = []
    for _p in _docx.Document(WORD_FILE).paragraphs:
        _tx = _re.sub(r'\s+', ' ', _p.text).strip()
        if not _tx or len(_tx) > 90: continue
        _r = next((r for r in _p.runs if r.text.strip()), None)
        _col = str(_r.font.color.rgb) if (_r is not None and _r.font.color is not None and _r.font.color.type is not None and _r.font.color.rgb is not None) else '000000'
        _wp.append((_tx, _col, bool(_r is not None and _r.underline), bool(_r is not None and _r.italic)))
    _k = 0; _kinds = {}
    for h in list(m.find_all('h2')):
        tx = _t(h)
        j = next((i for i in range(_k, len(_wp)) if _wp[i][0] == tx), None)
        if j is None: report.append(('settings', 'WARNING: heading not found in Word (kept as built)', tx)); continue
        _k = j + 1; col, ul, it = _wp[j][1].upper(), _wp[j][2], _wp[j][3]
        if col in ('000000', '222222'):
            inner = tx if not ul else '<u>%s</u>' % tx
            inner = inner if not it else '<em>%s</em>' % inner
            n = replace(h, '<p>%s</p>' % inner); merge_section(n); _kinds['line'] = _kinds.get('line', 0) + 1
        else:
            cls = {'0000FF': 'mm-hc-0432FF', '0432FF': 'mm-hc-0432FF', 'FF0000': 'mm-hc-EE0000', 'EE0000': 'mm-hc-EE0000', '00B050': 'mm-hc-00B050'}.get(col, 'mm-hc-' + col)
            h['class'] = [c for c in (h.get('class') or []) if not c.startswith('mm-hc-')] + [cls]; _kinds[cls] = _kinds.get(cls, 0) + 1
    report.append(('settings', 'headings as Word (black = an ordinary line; others their Word colour)', str(_kinds)))
    # 5 Nov 10:1x (review fault 40; b13 at 1440: "Pink Language Materials" and "Green Language Materials" black): a whole line
    # in Word's pink (FF40FF) or second green (2AB116) takes the template's class for that colour (Essay template 71dd8bf8,
    # owner 5 Nov 04:00 "Yes")
    _pg = {}; _kpg = 0; _blk = set()
    for _i, _p in enumerate(_docx.Document(WORD_FILE).paragraphs):   # every run of the line in that colour (not only the first)
        _rs = [r for r in _p.runs if r.text.strip()]
        _cs = {str(r.font.color.rgb).upper() if (r.font.color is not None and r.font.color.type is not None and r.font.color.rgb is not None) else '000000' for r in _rs}
        if _rs and len(_cs) == 1 and next(iter(_cs)) in ('FF40FF', '2AB116'): _pg[_re.sub(r'\s+', ' ', _p.text).strip()] = next(iter(_cs))
        # 6 Nov 05:5x (b25 review fault 2: the list titles "Spoken Language", "Reading Stages", "Function of Words" in Word
        # blue 0000FF, PDF p2 blue, were black on the page): a whole line in Word blue takes the template's blue class
        elif _rs and len(_cs) == 1 and next(iter(_cs)) in ('0000FF', '0432FF') and '\t' not in _p.text.strip(): _pg.setdefault(_re.sub(r'\s+', ' ', _p.text).strip(), '0432FF')
        # (a blue line whose words Word also has as a black line - "Word Study", "Reading Analysis" in the PDF p2 list -
        # is left as built: the black one would take the blue too; a label line with a tab (Series 3-5) is coloured by its
        # own spans already; Word paragraphs 0-7 are Word's contents list, off the page)
        elif _rs and _cs <= {'000000'} and _i > 7: _blk.add(_re.sub(r'\s+', ' ', _p.text).strip())
    for _x in _blk:
        if _pg.get(_x) == '0432FF': del _pg[_x]
    for p_ in m.find_all('p'):
        c_ = _pg.get(_t(p_))
        if c_ and not p_.find(class_=_re.compile('^mm-hc-')) and 'mm-hc-' + c_ not in (p_.get('class') or []):
            p_['class'] = (p_.get('class') or []) + ['mm-hc-' + c_]; _kpg += 1
    report.append(('settings', 'whole lines in Word pink / green coloured', str(_kpg)))
    # 5 Nov 13:4x (owner 13:34 agreement: lines and headings centred in Word stay centred at 641 px and wider): a heading
    # whose Word paragraph is centred takes the template's class centred
    _ctr = {_re.sub(r'\s+', ' ', _p.text).strip() for _p in _docx.Document(WORD_FILE).paragraphs if _p.alignment is not None and int(_p.alignment) == 1}
    _kc = 0
    for h in m.find_all('h2'):
        if _t(h) in _ctr and 'centred' not in (h.get('class') or []): h['class'] = (h.get('class') or []) + ['centred']; _kc += 1
    report.append(('settings', 'headings centred as Word', str(_kc)))
    # the contents box entries jump to these headings (the PDF's contents list; owner 1 Nov 10:01: headings in the contents
    # are red on the page). "Reading Stages" in the contents jumps to the green heading "Reading" (Word paragraph 522).
    def _tag(text, k, tid):   # the k-th heading with exactly this text (colour classes are not yet Word's at this stage)
        after = m.find(id='toc-wabs') if tid == 'toc-keys' else None   # Keys to Literacy: the first after "Writing - Abstract" (Word paragraph 302)
        L = [h for h in (after.find_all_next('h2') if after is not None else m.find_all('h2')) if _t(h) == text]
        if k < len(L):
            h = L[k]; h['id'] = tid; h['class'] = [c for c in (h.get('class') or []) if not c.startswith('mm-hc-')] + ['mm-hc-EE0000']
            report.append(('settings', 'contents entry and red heading', text)); return
        report.append(('settings', 'WARNING: contents heading not found', text))
    # Word paragraphs 124 (the 1st "Spoken Language" heading: the list title of Word paragraph 43 is a line, not a heading;
    # 6 Nov 05:5x b25 review fault 1: k=1 went to the red heading of Word paragraph 171), 287, 302, 360, 522, 644
    for text, k, tid in [('Spoken Language', 0, 'toc-spoken'), ('Writing - Abstract', 0, 'toc-wabs'), ('Keys to Literacy', 0, 'toc-keys'),
                         ('Writing - Concrete', 0, 'toc-wcon'), ('Reading', 0, 'toc-reading'), ('Grammar', 0, 'toc-grammar')]:
        _tag(text, k, tid)
    for sec in list(m.find_all('section')):   # sections left with nothing but empty space join the next one's text
        if not sec.find(['h2']) and not _t(sec) and not sec.find('img'): sec.decompose()
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
    # the 4 Nov list of headings made lines was fitted to the old PDF; replaced on 5 Nov by the Word-colour rule above
    plan = [('Series 1', 0, '<p class="mm-hanglab"><span class="mm-lab mm-hc-0432FF">Series 1 </span><span class="mm-hc-0432FF">Subject and Verb</span></p>'),
            ('Series 2', 0, '<p class="mm-hanglab"><span class="mm-lab mm-hc-0432FF">Series 2 </span><span class="mm-hc-0432FF">Subject, Verb, Object</span></p>')]
    targets = [(H(t, k), h, t, k) for t, k, h in plan]
    kl = wr = None   # 5 Nov: colours come from Word (above)
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
            h = ('<p class="centred mm-hc-0432FF">Letter Bingo: learning</p><div class="mm-row" data-above="40" data-level="91"><div class="mm-imgs">%s%s</div></div>'
                 '<p class="centred mm-hc-0432FF">Letter Bingo: teaching</p><div class="mm-row" data-above="40" data-level="92"><div class="mm-imgs">%s%s</div></div>') % tuple(str(f) for f in figs)
            row.decompose(); n = replace(lb, h); merge_section(n); report.append(('settings', 'Letter Bingo: each caption over its two images (one pair under the other; the template has no side-by-side captioned groups)', ''))
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
        if _t(d) == 'Pink Language Materials': d['class'] = d.get('class', []) + ['mm-hc-FF40FF']   # template class since 5 Nov (owner 04:00 "Yes")
        if _t(d) == 'Green Language Materials': d['class'] = d.get('class', []) + ['mm-hc-2AB116']
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
    # 5 Nov 19:1x (images check D143 on build 21): the template's 20 Oct rule main .mm-row[data-level="10"]{gap:19.2px} was made for
    # The Culture Curriculum's rows; this page's tenth row took level 10 by count and its gaps were forced to 19.2 px. Its own level name.
    for _r in m.select('div.mm-row[data-level="10"]'): _r['data-level'] = '10e'
    # 6 Nov 00:2x (Word-format check, fixed): "ˈrī-tiŋ" is bold in Word (its paragraph's Heading1 style) and in the PDF (p11)
    for _a in m.select('a.mm-box'):
        if _a.get_text(strip=True).startswith('ˈrī') and _a.find('strong') is None:
            _s = sp.new_tag('strong'); [_s.append(x.extract()) for x in list(_a.contents)]; _a.append(_s)
    # 6 Nov 00:3x: the colon after "Wikipedia" is bold in Word (Heading1 style) and in the PDF (p11, TimesNewRomanPS-BoldMT)
    for _a in m.select('a[href*="wikipedia.org/wiki/Writing"]'):
        _n = _a.next_sibling
        if isinstance(_n, str) and _n.startswith(':'):
            _s = sp.new_tag('strong'); _s.string = ':'; _n.replace_with(_n[1:]); _a.insert_after(_s)
    pin = next((h for h in m.find_all('h2') if _t(h) == 'Pinning'), None)
    if pin is not None:
        fl = pin.find_next_sibling(); para = fl.find_next_sibling() if fl is not None else None
        if fl is not None and 'mm-float' in (fl.get('class') or []) and para is not None and para.name == 'p':
            fig = fl.find('figure'); st = sp.new_tag('div', attrs={'class': 'mm-set mm-col', 'data-h': '120'})   # 5 Nov 19:1x: 120, the owner's 1 Nov 14:34 rule (was 168)
            tx = sp.new_tag('div', attrs={'class': 'mm-text'}); im = sp.new_tag('div', attrs={'class': 'mm-imgs'})
            fl.insert_before(st); tx.append(para.extract()); im.append(fig.extract()); fl.decompose(); st.append(tx); st.append(im)
            report.append(('settings', 'Pinning: side image and its paragraph as one set', ''))
    # Word Study cards (PDF p21): the three cards stood beside the lines and overlapped; one row of the three after the list
    cards = [m.select_one('img[data-full="images/%s.jpg"]' % n) for n in ('155', '156', '157')]
    if all(cards):
        flo = [c.find_parent('div', class_='mm-float') for c in cards]
        last = next((p for p in m.select('p.mm-hanglab') if _t(p).startswith('Word Families')), None)
        if last is not None and all(flo):
            row = _BS('<div class="mm-row" data-above="40" data-level="93"><div class="mm-imgs"></div></div>', 'html.parser').div
            for c in cards: row.select_one('.mm-imgs').append(c.find_parent('figure').extract())
            for f in flo: f.decompose()
            last.insert_after(row); report.append(('settings', 'Word Study cards: one row after the list (they overlapped beside it)', ''))
    # p19: the four labels each over its image (Blue Series, Green Series, Action Cards - Set 2, Puzzle Words)
    lab = next((p for p in m.find_all('p') if _t(p).startswith('The Blue Series') and 'Puzzle Words' in _t(p)), None)
    if lab is not None:
        imgs = {n: m.select_one('img[data-full="images/%s.jpg"]' % n) for n in ('144', '145', '146', '147')}   # 5 Nov 10:2x: the 5 Nov Word file has one image fewer before here (old image74 removed): every number one lower; checked by eye on b13 images 140-152
        if all(imgs.values()):
            caps = [('145', '<span class="mm-hc-EE0000">The Blue Series</span>'), ('144', '<span class="mm-hc-EE0000">The Green Series</span>'), ('146', '<span class="mm-hc-EE0000">Action Cards - Set 2</span>'), ('147', '<span class="mm-hc-EE0000">Puzzle Words</span> (aka <span class="mm-hc-EE0000">Sight Words</span>)')]   # 5 Nov: regular, red as Word (review fault 44)
            figs = []
            for n, cap in caps:
                f = imgs[n].find_parent('figure'); old = f.find_parent('div', class_=['mm-float', 'mm-row'])
                f = f.extract(); f['class'] = (f.get('class') or []) + ['mm-cf']
                f.insert(0, _BS('<figcaption class="mm-cap mm-up">%s</figcaption>' % cap, 'html.parser').figcaption); figs.append(f)   # 5 Nov (format review B2): upright as Word P638 and the PDF
                if old is not None and not old.find('figure'): old.decompose()
            row = _BS('<div class="mm-row" data-above="40" data-level="94"><div class="mm-imgs"></div></div>', 'html.parser').div
            for f in figs: row.select_one('.mm-imgs').append(f)
            lab.insert_before(row); lab.decompose(); report.append(('settings', 'p19: each label over its image, as the PDF', ''))
    # an image Word uses twice: placed at both places (p2 beside the text: image1 = 046; p19 Early Readers row: image136 = 134, 4th of 5)
    f1 = m.select_one('img[data-full="images/001.jpg"]'); f46 = m.select_one('img[data-full="images/046.jpg"]')
    if f1 is not None and f46 is not None:
        f1.find_parent('figure').insert_after(_BS(str(f46.find_parent('figure')), 'html.parser').figure); report.append(('settings', 'image1 (046) also beside the p2 text, as Word', ''))
        fl = f1.find_parent('div', class_='mm-float'); para = fl.find_next_sibling() if fl is not None else None
        if fl is not None and para is not None and para.name == 'p':   # the two images side by side beside their paragraph, as the PDF (one set)
            st = sp.new_tag('div', attrs={'class': 'mm-set mm-col', 'data-h': '120'})   # 5 Nov 19:1x: 120, the owner's 1 Nov 14:34 rule for images beside text (rule D142; was 167)
            tx = sp.new_tag('div', attrs={'class': 'mm-text'}); im = sp.new_tag('div', attrs={'class': 'mm-imgs'})
            fl.insert_before(st); tx.append(para.extract())
            for f in fl.find_all('figure'): im.append(f.extract())
            fl.decompose(); st.append(tx); st.append(im)
    f134 = m.select_one('img[data-full="images/133.jpg"]'); f152 = m.select_one('img[data-full="images/151.jpg"]')   # 5 Nov 10:2x: numbers one lower (old image74 removed); 133 = the teacher with children at a table, 151 = the circle (checked by eye on b13)
    if f134 is not None and f152 is not None:
        f152.find_parent('figure').insert_before(_BS(str(f134.find_parent('figure')), 'html.parser').figure); report.append(('settings', 'the teacher-with-children image (133) also in the Early Readers row, 4th of 5, as Word', ''))
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

    # a side image level with the first line of text, never the label above it (owner 20 Oct): image 003 moved after the bold label "Storytelling and book readings"
    im3 = m.select_one('img[data-full="images/003.jpg"]')
    fl3 = im3.find_parent('div', class_='mm-float') if im3 is not None else None
    nx3 = fl3.find_next_sibling() if fl3 is not None else None
    if nx3 is not None and 'micro-label' in (nx3.get('class') or []) and _t(nx3).startswith('Storytelling'):
        nx3.insert_after(fl3.extract()); report.append(('settings', 'image 003 level with the first line of text, after its label', ''))

    # a second line under a label line ("Cards of a contrasting colour ..." under Number and Gender) starts at the text column, as the PDF
    for p in m.find_all('p'):
        pv = p.find_previous_sibling()
        fc = next((c for c in p.contents if not (isinstance(c, str) and not c.strip())), None)
        if pv is not None and 'mm-hanglab' in (pv.get('class') or []) and getattr(fc, 'name', None) == 'span' and 'mm-t' in (fc.get('class') or []):
            fc.decompose(); p['class'] = [c for c in (p.get('class') or []) if c != 'mm-form'] + ['mm-hanglab']
            p.insert(0, _BS('<span class="mm-lab"></span>', 'html.parser').span); report.append(('settings', 'second line under a label line at the text column', _t(p)[:40]))

    # the spacing check's rule (owner 3 Nov 17:23): Word and the PDF decide which lines are together and where the breaks are, the template the
    # sizes - every plain gap the check lists is set to one size for "together" and one for "apart" (the template's own two paragraph gaps)
    import json as _json, os as _os
    _gf = _os.environ.get('ENG_GAPS', '/home/claude/eng35/space/gaps.json')
    if _os.path.exists(_gf):
        _T, _A = _os.environ.get('ENG_GAP_T', '20'), _os.environ.get('ENG_GAP_A', '29')
        _norm = lambda s: _re.sub(r'[^a-z0-9]', '', s.lower())
        _blocks = [e for e in m.find_all(['p', 'li', 'div']) if (e.name != 'div' or 'micro-label' in (e.get('class') or [])) and not e.find(['p', 'li']) and _t(e)]
        _cur = 0; _set = 0; _miss = []
        for g in _json.load(open(_gf)):
            k = _norm(g['b'].replace('Practice left', 'Practise left'))[:30]
            if not k: continue
            j = next((i for i in range(_cur, len(_blocks)) if _norm(_t(_blocks[i])).startswith(k)), None)
            if j is None: _miss.append(g['b'][:30]); continue
            _el = _blocks[j]; _bq = _el.find_parent('blockquote')
            if _bq is not None and _bq.find(['p', 'li']) is _el: _el = _bq   # a quotation: the gap is the quotation's own
            _el['data-gap'] = _T if g['kind'] == 'together' else _A; _cur = j + 1; _set += 1
        # headings: one size above and one below, every heading (the template's sizes, measured on build 8: 60 above, 36 below, line to line)
        _HA, _HB = _os.environ.get('ENG_GAP_HA', '48'), _os.environ.get('ENG_GAP_HB', '24')
        for _h in m.find_all('h2'):
            _sec = _h.find_parent('section')
            if _sec is not None and _sec.find_previous_sibling('section') is not None: _h['data-gap'] = _HA
            _nx = _h.find_next_sibling()
            while _nx is not None and 'mm-float' in (_nx.get('class') or []): _nx = _nx.find_next_sibling()   # 6 Nov 08:1x (spacing b28, P1): the line under a heading, not a photo float
            if _nx is not None and _nx.name in ('p', 'div', 'ul', 'ol', 'blockquote') and 'mm-row' not in (_nx.get('class') or []) and 'mm-set' not in (_nx.get('class') or []): _nx['data-gap'] = _HB
        report.append(('settings', 'PDF together/apart gaps set (T=%s, A=%s): %d; not found: %d' % (_T, _A, _set, len(_miss)), '; '.join(_miss[:8])))
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
    # 5 Nov 13:1x (review fault 5; format check b18: Word "Keys to Literacy" deleted): Word paragraph 60, the blue label
    # "Keys to Literacy" between "Sound Game" and "Sandpaper Letters" in the AMI list, was taken by the converter as the page
    # title (src.html h1) and so was missing; put back as a blue line, as the PDF p2
    kk = 0
    sg = next((p_ for p_ in m.find_all('p') if _t(p_) == 'Sound Game'), None)
    nx_ = sg.find_next_sibling() if sg is not None else None
    if nx_ is not None and _t(nx_) == 'Sandpaper Letters':
        sg.insert_after(_BS('<p class="mm-hc-0432FF">Keys to Literacy</p>', 'html.parser').p); kk = 1
    report.append(('settings', 'Word paragraph 60 "Keys to Literacy" put back in the AMI list', str(kk)))
    # 6 Nov 05:5x (b25 review fault 2): in Word the lines before the blue titles "Keys to Literacy" and "Function of Words"
    # (Word paragraphs 59 "Sound Game" and 88 "Definition Stages") keep Word's default space after (6 pt) where every other
    # line of the list has none, so the PDF p2 shows a blank space before those two titles: they take the "apart" gap
    _ka = 0
    for _tt in ('Keys to Literacy', 'Function of Words'):
        _e = next((p_ for p_ in m.find_all('p') if _t(p_) == _tt and p_.find_previous_sibling('p') is not None and _t(p_.find_previous_sibling('p')) in ('Sound Game', 'Definition Stages')), None)
        if _e is not None: _e['data-gap'] = _os.environ.get('ENG_GAP_A', '29'); _ka += 1
    report.append(('settings', 'blank space before the list titles Keys to Literacy and Function of Words, as the PDF p2', str(_ka)))
    # 5 Nov 13:1x (review fault 20; style check E041 on b18): the beige line Word puts before "Keys to Literacy" was placed
    # before the first line with those words - Word's contents line, taken off the page - so it stood at the top of the essay
    # and was missing between the three wall images and the "Keys to Literacy" heading (PDF p9); moved there
    kgl = 0
    fe = next((c for c in m.find_all(True) if c.get_text(strip=True) or (c.name == 'p' and 'mm-gl' in (c.get('class') or []))), None)
    hk = m.find(id='toc-keys')
    if fe is not None and fe.name == 'p' and 'mm-gl' in (fe.get('class') or []) and hk is not None:
        tgt_ = hk.find_parent('section') or hk
        tgt_.insert_before(fe.extract()); kgl = 1
    report.append(('settings', 'beige line moved from the top of the essay to before "Keys to Literacy"', str(kgl)))
    _columns(m, report, replace, merge_section)
    # 6 Nov 08:1x (spacing b28, P3): the first block after a Word-column grid where Word has a blank line before it takes the "apart" gap (PDF 2.00-2.69 lines)
    _kg = 0
    _AFTER = ('The Spoken Language curriculum listed', 'The questions I ask myself', 'Here\u2019s another option, from the Supple',
              'This necessitates', '\u201cA necessary condition for writing', '\u201cWe thus began to communicate',
              'Writing emerged independently', 'I\u2019ve adopted many', 'Object Box 1', '\u201cReading penetrates directly')
    for _g in m.select('div.mm-wcols2, div.mm-cols3'):
        _n = _g.find_next_sibling()
        if _n is None or _n.has_attr('data-gap') or _n.name not in ('p', 'blockquote'): continue
        if any(_t(_n).startswith(s_) for s_ in _AFTER):
            _n['data-gap'] = _os.environ.get('ENG_GAP_A', '29'); _kg += 1
    report.append(('settings', 'apart gap on the first block after a Word-column grid (Word blank line)', str(_kg)))
    # 5 Nov 09:5x (review fault 48; b12 122-width check: images 154/155/156 over each other at every width, over "Number"
    # 320-830): the three Word Study images stand one under another at the right, as in the PDF - the template's own
    # ext-float class (wrapFloats: "stand one under another (clear:right), not centred on the paragraph"). Tested on a b12
    # copy at 1440: stacked, no overlap.
    # 5 Nov 12:5x: ext-float kept them apart only at 831 and wider; at 320-830 the third was pulled 399 px up over the first
    # (b18 122 widths). Now one float holding the three figures, one under another (tested on a b18 copy at 1440 and 390).
    ws = m.find('section', id='word-study'); kws = 0
    fls = ws.find_all('div', class_='mm-float', recursive=False) if ws is not None else []
    if len(fls) > 1:
        im0 = fls[0].find(class_='mm-imgs')
        for f_ in fls[1:]:
            for fig in f_.find_all('figure'): im0.append(fig.extract()); kws += 1
            f_.decompose()
    report.append(('settings', 'Word Study images: one float, one under another at the right', str(kws)))
    # 5 Nov 10:1x (review fault 24; column check p10): Word's one centred line "Letter Bingo: learning <tabs> Letter Bingo:
    # teaching" over two groups of two images side by side, as the PDF - the template's own .mm-twocap line ("centres its first
    # caption over the first half of the row's photos and its second over the second half (as the PDF)") over one row
    kb = 0
    a_ = next((p_ for p_ in m.find_all('p') if _t(p_) == 'Letter Bingo: learning'), None)
    b_ = next((p_ for p_ in m.find_all('p') if _t(p_) == 'Letter Bingo: teaching'), None)
    if a_ is not None and b_ is not None:
        ra, rb = a_.find_next_sibling(), b_.find_next_sibling()
        if ra is not None and rb is not None and 'mm-row' in (ra.get('class') or []) and 'mm-row' in (rb.get('class') or []) and ra.find_next_sibling() is b_:
            cls = [c for c in (a_.get('class') or []) if c != 'centred']
            cap = _BS('<p class="%s"><span>Letter Bingo: learning</span><span>Letter Bingo: teaching</span></p>' % ' '.join(['mm-twocap'] + cls), 'html.parser').p
            a_.replace_with(cap); ia = ra.find(class_='mm-imgs'); ib = rb.find(class_='mm-imgs')
            for f_ in list(ib.find_all('figure', recursive=False)): ia.append(f_.extract())
            b_.decompose(); rb.decompose(); kb = 1
    report.append(('settings', 'Letter Bingo: one row of four under its two captions (template mm-twocap)', str(kb)))
    # 5 Nov 10:2x (review faults 42, 46): Word's captions in text boxes, under their images as the PDF - "Run" (image 141),
    # "Hug" (143), "Maria Montessori, 1950, Perugia." (152); numbers checked by eye on b13 images 140-152
    kc = 0
    for n_, cap_ in (('141', 'Run'), ('143', 'Hug'), ('152', 'Maria Montessori, 1950, Perugia.')):
        im_ = m.select_one('img[data-full="images/%s.jpg"]' % n_); f_ = im_.find_parent('figure') if im_ is not None else None
        if f_ is not None and f_.find('figcaption') is None:
            f_['class'] = (f_.get('class') or []) + ['mm-cf']; f_.append(_BS('<figcaption class="mm-cap mm-cap-below">%s</figcaption>' % cap_, 'html.parser').figcaption); kc += 1
    report.append(('settings', "captions from Word's text boxes under their images", str(kc)))
    # 5 Nov 13:0x (b18 122 widths, 641-830: "Maria Montessori, 1950, Perugia." over the text; 630-640 the image shown larger
    # than its file): the template measures a caption only above its image, in a captioned set (.mm-set[data-cap], its own
    # style). The Grammar image and its first paragraph become one set with the caption above the image; the PDF has it below
    # (placement roughly as the PDF, A011).
    im_ = m.select_one('img[data-full="images/152.jpg"]'); kg = 0
    fl_ = im_.find_parent('div', class_='mm-float') if im_ is not None else None
    pa_ = fl_.find_next_sibling() if fl_ is not None else None
    if fl_ is not None and pa_ is not None and pa_.name == 'p':
        fig = im_.find_parent('figure'); cap = fig.find('figcaption')
        # 6 Nov 06:1x (b25 review fault 7: the PDF p19 has the caption under the image): the caption stays under its image,
        # in the flow of the captioned set (mm-cap-below is not lifted above the image)
        if cap is not None: cap['class'] = ['mm-cap', 'mm-cap-below']
        st = sp.new_tag('div', attrs={'class': 'mm-set mm-col', 'data-h': '120', 'data-cap': '1'})   # 5 Nov 20:4x: 120, the owner's 1 Nov 14:34 rule for images beside text (was 168)
        if fl_.has_attr('data-gap'): st['data-gap'] = fl_['data-gap']
        tx = sp.new_tag('div', attrs={'class': 'mm-text'}); imd = sp.new_tag('div', attrs={'class': 'mm-imgs'})
        fl_.insert_before(st); tx.append(pa_.extract()); imd.append(fig.extract()); fl_.decompose(); st.append(tx); st.append(imd); kg = 1
    report.append(('settings', 'Grammar image and its first paragraph as one captioned set (caption above)', str(kg)))
    # 6 Nov 05:5x (b25 review faults 3, 4, 5, 8):
    # fault 3 - Word's tab at the start of the attribution "- Maria Montessori, The 1946 London Lectures" (PDF p4) put it
    # 95 px in where every other attribution starts at the quotation's edge, as the PDF: the leading tab is dropped
    _k3 = 0
    for _c in m.find_all('cite'):
        _fc = next((c for c in _c.contents if not (isinstance(c, str) and not c.strip())), None)
        if getattr(_fc, 'name', None) == 'span' and 'mm-t' in (_fc.get('class') or []): _fc.decompose(); _k3 += 1
    report.append(('settings', 'tab at the start of an attribution dropped (PDF p4)', str(_k3)))
    # fault 4 - a line after Word's grey line (p.mm-gl; "In the environments I have prepared", PDF p6) kept the spacing
    # check's gap figure, which the letter-gap script measures from the text above the grey line: the line stood on the
    # text (1440). The figure is dropped, so the template spaces it from the grey line, as every other line after one
    _k4 = 0
    for _g in m.select('p.mm-gl'):
        _n = _g.find_next_sibling()
        if _n is not None and _n.name == 'p' and _n.has_attr('data-gap'): del _n['data-gap']; _k4 += 1
    report.append(('settings', "gap figure dropped on a line after Word's grey line", str(_k4)))
    # 6 Nov 09:2x (spacing b29, P5): a heading that opens a section straight after Word's grey line, with text (not photos) above
    # the line, keeps no gap figure - mm-letter-gaps-js measures data-gap from the text above the grey line (empty p.mm-gl has no
    # letters), so "The Peace Table" and "Art/Drawing/Colouring" stood 12-18 px under the line where every heading after a grey
    # line below photos stands 36-37 (letter gaps step aside there; the template spaces the heading from the line). As fault 4 above.
    _k11 = 0
    for _g in m.select('p.mm-gl'):
        _s = _g.find_next_sibling(); _pv = _g.find_previous_sibling()
        if _s is None or _s.name != 'section' or _pv is None: continue
        _h = _s.find(True, recursive=False); _last = _pv
        while _last is not None and _last.name == 'section' and _last.find(True, recursive=False) is not None: _last = _last.find_all(True, recursive=False)[-1]
        if _h is not None and _h.name == 'h2' and _h.has_attr('data-gap') and _last is not None and _last.name == 'p' and _last.find('img') is None and 'mm-gl' not in (_last.get('class') or []):
            del _h['data-gap']; _k11 += 1
    report.append(('settings', "gap figure dropped on a heading after Word's grey line with text above the line", str(_k11)))
    # fault 5 (part) - the PDF p18 Pink list is evenly spaced (24.4 pt every line); "Puzzle Words" and "Pink Phrase Cards"
    # had the "together" gap where the list's other lines have "apart": the list's own gap for every line
    _k5 = 0
    _pk = next((p_ for p_ in m.find_all('p') if _t(p_) == 'Pink Language Materials'), None)
    if _pk is not None:
        _L = [x for x in _pk.find_next_siblings('p')]
        _v = [x.get('data-gap') for x in _L if x.has_attr('data-gap')]
        if _v:
            _maj = max(set(_v), key=_v.count)
            for x in _L:
                if x.get('data-gap') not in (None, _maj): x['data-gap'] = _maj; _k5 += 1
    report.append(('settings', 'PDF p18 Pink list: every line the same gap, as the PDF', str(_k5)))
    # fault 8 - Reading Analysis "a." to "e." (PDF p22): Word indents them 36 pt (48 px), the PDF shows them indented: the
    # template's 48 px offset (mm-tab1; none on phones)
    _k8 = 0
    _ra = [h for h in m.find_all(['h2', 'p']) if _t(h) == 'Reading Analysis']
    if _ra:
        for x in _ra[-1].find_all_next('p'):
            if _re.match(r'^[a-e]\.', _t(x)) and x.find('span', class_='mm-t') is not None:
                x['class'] = (x.get('class') or []) + ['mm-tab1']; _k8 += 1
    report.append(('settings', 'Reading Analysis a.-e. indented 48 px as Word', str(_k8)))
    for _e in m.find_all(class_=True):   # 6 Nov 06:0x: a class given twice by two settings is kept once
        if len(set(_e['class'])) != len(_e['class']): _e['class'] = list(dict.fromkeys(_e['class']))
    # 6 Nov 07:0x (b25 review fault 6; owner 6 Nov 06:54 agreement, template class mm-ind104): the PDF p18 sequence of
    # presentations (Object Box 1 ... Grammar, etc.) is indented 78 pt in Word - the columns start 104 px in, at 641 px and wider
    _k6 = 0
    for _g in m.select('div.mm-wcols2'):
        _f = _g.find('p')
        if _f is not None and _t(_f) == 'Object Box 1' and 'Pink Series' in _t(_g):
            _g['class'] = _g['class'] + ['mm-ind104']; _k6 += 1
    report.append(('settings', 'Object Box sequence indented as Word (mm-ind104)', str(_k6)))
    # 6 Nov 09:2x (spacing b29, P4 - corrected check, PDF lines matched by anchors per page and column): Word's own default
    # space after (6 pt, styles.xml docDefaults w:after=120) stands on these paragraphs, and the PDF shows it: 1.33-1.49 lines.
    # gaps.json (written from the old check's matching) called them together; they take the "apart" gap.
    # P4a - the Object Box sequence (PDF p18, 24.2-27.1 pt between lines): every line but the columns' first lines
    _k10 = 0
    for _g in m.select('div.mm-wcols2.mm-ind104'):
        for _p in _g.find_all('p'):
            if _p.get('data-gap') == _os.environ.get('ENG_GAP_T', '20'): _p['data-gap'] = _os.environ.get('ENG_GAP_A', '29'); _k10 += 1
    # P4b - the quotation after "The questions I ask myself..." (PDF p4, 24.5 pt); P4c - the quotation after "I've been working
    # as a Montessori guide..." (PDF p19, 24.3 pt; no visible change until template item T3, the letter gaps stepping aside after a set with photos)
    for _s in ('The questions I ask myself', 'I’ve been working as a Montessori guide'):
        _q = next((p_ for p_ in m.find_all('p') if _t(p_).startswith(_s)), None)
        _bq = _q.find_next('blockquote') if _q is not None else None
        if _bq is not None and 'pullquote' in (_bq.get('class') or []) and _bq.get('data-gap') == _os.environ.get('ENG_GAP_T', '20'):
            _bq['data-gap'] = _os.environ.get('ENG_GAP_A', '29'); _k10 += 1
    report.append(('settings', 'apart gap where Word keeps its default 6 pt after and the PDF shows 1.33-1.49 lines (Object Box sequence, two quotations)', str(_k10)))
    # 6 Nov 10:5x (build 31 review faults 4-5; spacing check 1440 lines 260, 523, 536, 628): the PDF shows these apart (a blank
    # line in Word, or Word's 6 pt), the page had the list's "together" gap
    _k12 = 0
    for _s in ('What the child is doing here', 'Decoding:', 'Kate Millie’s Supplemental Language Album - Reading', 'Action Cards - Set 1'):
        _e = next((p_ for p_ in m.find_all(['p', 'li']) if _t(p_).startswith(_s)), None)
        if _e is not None: _e['data-gap'] = _os.environ.get('ENG_GAP_A', '29'); _k12 += 1
    report.append(('settings', 'apart gap on 4 lines the PDF shows apart (review b31 faults 4-5)', str(_k12)))
    # 6 Nov 10:5x (build 31 review fault 1): in the PDF p2 AMI list the eight blue titles are one kind (Word Normal, blue);
    # Writing Stages, Word Study and Reading Analysis were built as headings (48) while Keys to Literacy and Function of Words
    # are lines (29): all are lines with the list-title gap; Reading Analysis keeps the larger gap (Word's empty paragraph before it)
    _k13 = 0
    for _h in list(m.select('h2.mm-hc-0432FF')):
        _x = _t(_h)
        if _x in ('Writing Stages', 'Word Study', 'Reading Analysis'):
            _h.name = 'p'; _h['data-gap'] = '48' if _x == 'Reading Analysis' else _os.environ.get('ENG_GAP_A', '29'); _k13 += 1
    report.append(('settings', 'PDF p2 list titles Writing Stages, Word Study, Reading Analysis as lines like the other titles (review b31 fault 1)', str(_k13)))
    # 6 Nov 11:3x (build 31 review fault 6): the Spoken Language shelf image stood before the beige line in the code, so at 768 the
    # line (a block that keeps clear of floats) was cut to 416 px beside it, and at 390 the image stood above the line. In the PDF
    # the line comes first: the image is moved after the line (the template's own order, p.mm-gl + .mm-float). The style check
    # E041 must then skip the image between the line and its paragraph (check change put to her 6 Nov).
    _k14 = 0
    for _g in m.select('p.mm-gl'):
        _pv = _g.find_previous_sibling()
        if _pv is not None and 'mm-float' in (_pv.get('class') or []):
            _g.insert_after(_pv.extract()); _k14 += 1
    report.append(('settings', 'image moved after the beige line before it (review b31 fault 6)', str(_k14)))
    # 5 Nov 13:0x: two sections had id="grammar" (the opening section kept the id of Word's contents line "Grammar")
    _secs = m.find_all('section', id='grammar')
    for _s in _secs[:-1]: del _s['id']
    report.append(('settings', 'duplicate section id "grammar" removed from the opening section', str(len(_secs) - 1)))
    # 5 Nov 14:1x (placement check, build 19, 831-1920): image 052 beside the list "I-Spy ... Reading" stood 8.3 px below the
    # capitals of "I-Spy" - the list's first line kept its own gap figure after the image was placed; that figure is dropped
    # (the list then follows the paragraph with the template's own spacing). Image 112, the writing strip, stood 20 px above
    # "Metal Insets" - it floated before the Writing Stages columns, which the template does not place it against; it now
    # floats at the top of the second column, at the right as in the PDF p15. Tested with place_check.py on a build 19 copy.
    kp = 0
    im_ = m.select_one('img[data-full="images/052.jpg"]'); fl_ = im_.find_parent('div', class_='mm-float') if im_ is not None else None
    ol_ = fl_.find_next_sibling() if fl_ is not None else None
    if ol_ is not None and ol_.name in ('ol', 'ul') and ol_.find('li') is not None: ol_.find('li')['data-gap'] = '20'; kp += 1   # 6 Nov 08:1x (spacing b28, P2): "I-Spy" together with the line above (PDF p10 1.03); template 847b6adb no longer steps aside for a floated image
    im_ = m.select_one('img[data-full="images/112.jpg"]'); fl_ = im_.find_parent('div', class_='mm-float') if im_ is not None else None
    g_ = fl_.find_next_sibling() if fl_ is not None else None
    if g_ is not None and 'mm-wcols2' in (g_.get('class') or []):
        g_.find_all('div', recursive=False)[1].insert(0, fl_.extract()); kp += 1
    report.append(('settings', 'images 052 and 112 level with the first line of their text', str(kp)))
    # 5 Nov 14:3x (code check, build 20, section 3: "inline style counter-reset on <ol>"): the converter writes the count on a
    # list that continues as an inline style; the template reads the list's start attribute and sets it itself (27 Oct)
    kcr = 0
    for ol_ in m.find_all('ol', start=True):
        if 'counter-reset' in (ol_.get('style') or ''): del ol_['style']; kcr += 1
    report.append(('settings', 'inline counter-reset dropped from continuing lists (the template reads start)', str(kcr)))
    # 5 Nov 10:3x (review fault 30): a tab Word puts before a quotation's opening mark ("Not one of them had ever...") is not
    # kept - the template's quotation style sets the indent; with the tab the first line stood about 50 px further in than
    # every other quotation
    kq = 0
    for q_ in m.select('blockquote p'):
        first = next((c for c in q_.descendants if (isinstance(c, str) and c.strip()) or (getattr(c, 'name', None) == 'span' and 'mm-t' in (c.get('class') or []))), None)
        if getattr(first, 'name', None) == 'span': first.decompose(); kq += 1
    report.append(('settings', 'leading tabs in quotations dropped', str(kq)))
    # 5 Nov 10:5x (review fault 36; b16 at 1440): the reading sequence (Object Box 1 ... Definition Stages) with its six
    # images beside it in two rows of three, as the PDF p16 - one set (it was two, the second holding the 3.1-3.17 columns,
    # which were squeezed beside the images); the paragraph above and the lines after Definition Stages stand outside it.
    # Two rows: the page style mm-grid3 (CSS above). Tested on a b16 copy at 1440.
    kr = 0
    p0 = next((p_ for p_ in m.find_all('p') if _t(p_).startswith('The AMI Montessori reading system')), None)
    A_ = p0.find_parent('div', class_='mm-set') if p0 is not None else None
    B_ = A_.find_next_sibling('div') if A_ is not None else None
    if A_ is not None and B_ is not None and 'mm-set' in (B_.get('class') or []):
        tA, iA = A_.find(class_='mm-text'), A_.find(class_='mm-imgs'); tB, iB = B_.find(class_='mm-text'), B_.find(class_='mm-imgs')
        for c in list(tB.find_all(True, recursive=False)):
            if c.name == 'p' and _t(c) in ('Reading Folders', 'Environment Cards', 'Classified Reading', 'Definition Stages'): tA.append(c.extract())
        for f_ in list(iB.find_all('figure', recursive=False)): iA.append(f_.extract())
        rest = [c.extract() for c in tB.find_all(True, recursive=False)]
        for c in reversed(rest): B_.insert_after(c)
        B_.decompose(); A_['class'] = A_['class'] + ['mm-grid3']
        A_.insert_before(p0.extract()); kr = 1
    report.append(('settings', 'reading sequence: one set, six images in two rows of three beside it', str(kr)))


DEBUG = []
PDF_FILE = '/home/claude/eng35/src/3.5.0 The English Curriculum.pdf'   # the owner's PDF of 5 Nov (sha256 4e44885a)


def _pdf_regions():
    """Rows of the PDF with text in two or three columns (the same reading as tools/col_check.py), grouped into regions:
    rows on one PDF page less than 60 pt apart. Each region: a list of columns, each a list of cell texts in order."""
    import pymupdf
    d = pymupdf.open(PDF_FILE); regions = []
    for pn in range(len(d)):
        p = d[pn]; Wp = p.rect.width; lines = {}
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                cells, cur, x0, xe = [], '', None, None
                for s_ in l['spans']:
                    if not s_['text'].strip(): continue
                    if cur and s_['bbox'][0] - xe > 20: cells.append((x0, cur)); cur, x0 = '', None
                    if x0 is None: x0 = s_['bbox'][0]
                    cur += s_['text']; xe = s_['bbox'][2]
                if cur: cells.append((x0, cur))
                for cx, t in cells:
                    t = t.strip()
                    if len(_re.sub(r'[^a-z0-9]', '', t.lower())) < 4 or _re.fullmatch(r'[\d.\-\s]+', t): continue
                    lines.setdefault(round(l['bbox'][1] / 3) * 3, []).append((cx, t))
        rows = []
        for y, v in sorted(lines.items()):
            v.sort()
            if len(v) >= 2 and v[0][0] < Wp * 0.3 and any(x > Wp * 0.4 for x, _ in v[1:]): rows.append((y, v))
        # one region per page and column layout: rows whose right-hand cells start at the same places (within 15 pt) belong
        # together however far apart - Word sets a whole page in columns, the left column's lines first
        g = []
        for y, v in rows:
            xs = [x for x, _ in v[1:]]
            hit = next((r for r in g if any(abs(a - b) < 15 for a in xs for b in r['xs'])), None)
            if hit is None: g.append({'xs': xs, 'rows': [(y, v)]})
            else: hit['rows'].append((y, v)); hit['xs'] = sorted(set(hit['xs'] + xs))
        for r in g: regions.append((pn + 1, r['rows']))
    out = []
    for pn, rws in regions:
        # column boundaries: the x of each cell in the row with the most cells
        ref = max(rws, key=lambda r: len(r[1]))[1]; xs = [x for x, _ in ref]
        cols = [[] for _ in xs]
        for y, v in rws:
            for x, t in v:
                k = min(range(len(xs)), key=lambda i: abs(xs[i] - x)); cols[k].append(t)
        out.append((pn, cols))
    return out


def _columns(m, report, replace, merge_section):
    """5 Nov (owner 04:59: "these lists go in two columns, as in the PDF, using the template's two-column style"): every
    region the PDF sets in two or three columns stands in the template's own column style - div.mm-wcols2 (two columns)
    or div.mm-cols3 (three), one child div per column (template: one column at 640 px and narrower)."""
    def key(s): return _re.sub(r'[^a-z0-9]', '', s.lower())
    blocks_all = lambda: [b for b in m.find_all(['p', 'li', 'h2', 'h3', 'div', 'figcaption']) if b.get_text(strip=True)]
    # 5 Nov: which paragraphs stand in columns comes from the Word file itself - its sections set in 2 or 3 columns
    # (w:cols w:num) - and where each column starts from the PDF (the first line at the top of the next column; Word
    # balances the columns, there are no column breaks). Each Word paragraph is then found on the page in order.
    import docx as _docx
    from docx.oxml.ns import qn as _qn
    _d = _docx.Document(WORD_FILE); ps = _d.paragraphs; secs = []; st = 0
    for i, p_ in enumerate(ps):
        sp_ = p_._p.pPr.find(_qn('w:sectPr')) if p_._p.pPr is not None else None
        if sp_ is not None:
            c_ = sp_.find(_qn('w:cols')); secs.append((st, i, int(c_.get(_qn('w:num')) or 1) if c_ is not None else 1)); st = i + 1
    regions = _pdf_regions()
    done = 0; miss = []; cursor_el = None
    for a_, b_, n in secs:
        if n < 2: continue
        texts = [_re.sub(r'\s+', ' ', ps[i].text).strip() for i in range(a_, b_ + 1)]
        texts = [t for t in texts if len(key(t)) >= 4]
        if not texts: continue
        if a_ < 10: continue   # Word paragraphs 2-8: the contents list (the contents box)
        # column starts: the PDF region holding this section's lines; column k starts at the first line of the section
        # that the PDF shows at the top of column k or below (the earliest section line found among column k's cells)
        def wk(t): return key(_re.sub(r'^\d+(\.\d+)*\s+', '', t))[:25]
        tk = [wk(t) for t in texts]
        reg = None
        for pn_, cols in regions:
            ck = [set(wk(c) for c in col) for col in cols]
            if len(cols) == n and tk[0] in ck[0] and all(any(t in ck[k] for t in tk) for k in range(1, n)): reg = ck; break
        if reg is None: miss.append('Word %d-%d (no PDF columns found for it)' % (a_, b_)); continue
        starts = []
        for k in range(1, n):
            j = next((i for i, t in enumerate(tk) if t in reg[k] and (not starts or i > starts[-1])), None)
            if j is None: break
            starts.append(j)
        if len(starts) != n - 1: miss.append('Word %d-%d (column start not found)' % (a_, b_)); continue
        cand = blocks_all()
        cursor = next((i + 1 for i, e in enumerate(cand) if e is cursor_el), 0)
        found = []; pos = cursor; reach = 600
        for j, t in enumerate(texts):
            kt = key(_re.sub(r'^\d+(\.\d+)*\s+', '', t))[:30]
            i = None
            for q in range(pos, min(pos + reach, len(cand))):
                # 5 Nov 08:2x: a hanging label (span.mm-lab "3.1") is stripped like Word's numbering, so "3.1Cursive..." matches
                kl = lambda e: key(_re.sub(r'^\s*\d+(\.\d+)*\s*', '', e.get_text()))
                kb = kl(cand[q])
                if kb.startswith(kt) and not any(kl(c).startswith(kt) for c in cand[q].find_all(['p', 'li', 'h2', 'div', 'figcaption'])): i = q; break
            if i is None: continue
            ci = sum(1 for s0 in starts if j >= s0)
            found.append((ci, cand[i])); pos = i + 1; reach = 40
        if found: cursor_el = found[-1][1]   # the next section's lines are searched after this section's last line
        pn = a_
        if len({ci for ci, _ in found}) < 2: miss.append('Word %d (one column only found)' % pn); continue
        # the columns' container: the deepest element holding every found cell; its children that hold the cells are the
        # blocks that move into the columns (a list's items when one list holds both columns, as Word's numbered 3.1-3.17)
        els = [el for _, el in found]
        anc = els[0]
        def holds(a, e): return a is e or any(x is a for x in e.parents)
        while anc is not None and not all(holds(anc, e) for e in els): anc = anc.parent
        if anc is None or anc.name in ('figure', 'figcaption') or (anc.get('class') and 'mm-imgs' in anc.get('class', [])):
            miss.append('p%d (image captions - set elsewhere)' % pn); continue
        if any(holds(e, anc) for e in els):   # one found element is the container itself: take its parent
            anc = anc.parent
        if anc.name in ('main', '[document]'):   # the columns run over several sections: join those sections first
            secs = []
            for e in els:
                s_ = e.find_parent('section')
                if s_ is not None and s_ not in secs: secs.append(s_)
            if len(secs) > 1:
                allsec = [c for c in anc.children if getattr(c, 'name', None)]
                i0 = allsec.index(secs[0]); i1 = allsec.index(secs[-1])
                for s_ in allsec[i0 + 1:i1 + 1]:
                    if s_.name == 'section':
                        for c in list(s_.contents): secs[0].append(c.extract())
                        s_.decompose()
                    else: secs[0].append(s_.extract())
                anc = secs[0]
        def child_of(e):
            while e.parent is not None and e.parent is not anc: e = e.parent
            return e
        lifted = [(ci, child_of(el)) for ci, el in found]
        sib = [c for c in anc.children if getattr(c, 'name', None)]
        idx = {id(b_): i for i, b_ in enumerate(sib)}
        lo = min(idx[id(b_)] for _, b_ in lifted if id(b_) in idx); hi = max(idx[id(b_)] for _, b_ in lifted if id(b_) in idx)
        span = sib[lo:hi + 1]
        colof = {}
        for ci, b_ in lifted: colof.setdefault(id(b_), ci)
        cur = lifted[0][0]; parts = [[] for _ in range(n)]
        for b_ in span:
            cur = colof.get(id(b_), cur); parts[cur].append(b_)
        if any(not p_ for p_ in parts): miss.append('p%d (a column found empty)' % pn); continue
        cls = 'mm-wcols2' if n == 2 else 'mm-cols3'
        if n > 3: miss.append('Word %d (%d columns)' % (pn, n)); continue
        wrap = _BS('<div class="%s"></div>' % cls, 'html.parser').div
        if anc.name in ('ul', 'ol'):   # one list holds the columns: one list per column, numbering continued
            anc.insert_before(wrap); n_before = 0
            for ci, pt in enumerate(parts):
                colw = _BS('<div></div>', 'html.parser').div; wrap.append(colw)
                lst = _BS('<%s></%s>' % (anc.name, anc.name), 'html.parser').find(anc.name)
                for k_, v_ in anc.attrs.items(): lst[k_] = v_
                if anc.name == 'ol' and n_before: lst['start'] = str(int(anc.get('start', 1)) + n_before)
                for b_ in pt: lst.append(b_.extract())
                n_before += len(pt); colw.append(lst)
            if not [c for c in anc.children if getattr(c, 'name', None)]: anc.decompose()
        else:
            span[0].insert_before(wrap)
            for ci, pt in enumerate(parts):
                colw = _BS('<div></div>', 'html.parser').div; wrap.append(colw)
                for b_ in pt: colw.append(b_.extract())
        # 5 Nov 09:4x: the first line of each column carries no data-gap - the template's grid rule sets it level with the
        # grid's top (colStart, margin 0) while mm-letter-gaps-js also set its data-gap, which pulled the second column up over
        # the text above (b12 122-width check: text over text 680-1920; tested on a b12 copy at 1440: gone)
        # 5 Nov 10:0x: the space above the grid is the first column's first line's own figure, moved onto the grid itself
        # (mm-letter-gaps-js then moves the whole grid); every column's first line gets data-space="0" so mm-kind-gaps-js
        # adds no 40 to a blue or bold line there (it pulled "Preparation of the hand" 98 px up - traced at 1440 on b13)
        for ci_, colw in enumerate(wrap.find_all('div', recursive=False)):
            f_ = colw.find(True, recursive=False)
            if f_ is not None and f_.name in ('ul', 'ol'):
                if f_.has_attr('data-gap'):   # 5 Nov 10:3x: a list's own figure (b14: Chalkboard 8 px below Crayons)
                    if ci_ == 0 and not wrap.has_attr('data-gap'): wrap['data-gap'] = f_['data-gap']
                    del f_['data-gap']
                f_ = f_.find('li')
            if f_ is None: continue
            if f_.has_attr('data-gap'):
                if ci_ == 0 and not wrap.has_attr('data-gap'): wrap['data-gap'] = f_['data-gap']
                del f_['data-gap']
            elif ci_ == 0 and not wrap.has_attr('data-gap') and ((f_.name == 'h2' and 'mm-hc-0432FF' in (f_.get('class') or [])) or (f_.find('strong') is not None and f_.find('strong').get_text(strip=True) == f_.get_text(strip=True))):
                wrap['data-gap'] = '40'   # what mm-kind-gaps-js gives a blue heading or a bold line
            # 5 Nov 12:4x (b18 122 widths, 320-640: a second column's first line over the first column's last - data-space is
            # the line's own gap, used at phone widths where the columns follow one another; 0 drew them together): column 1's
            # first line 0 (the grid carries its gap), a later column's first line the PDF's "together" gap, a heading the heading gap
            # 13:0x: column 1's first line carries the grid's own gap (b18: "Pink Language Materials" drawn over the image row
            # above it at 320-600 with 0)
            if ci_ == 0:
                if wrap.has_attr('data-gap'): f_['data-space'] = wrap['data-gap']
            else: f_['data-space'] = '48' if f_.name == 'h2' else '20'
        done += 1; DEBUG.append((pn, anc.name, [(ci, b.name, b.get_text(' ', strip=True)[:20]) for ci, b in found], len(span), [len(p_) for p_ in parts]))
    report.append(('settings', "PDF columns in the template's column style (mm-wcols2 / mm-cols3)", '%d regions; not placed: %s' % (done, '; '.join(miss[:10]))))

# 5 Nov: the contents box as the PDF's contents list (two columns of three), each entry jumping to its heading (ids set in SOUP_FIX)
TOC_ONLY = ['\u0000none']
TOC_EXTRA = [(0, 'toc-spoken', 'Spoken Language'), (1, 'toc-wabs', 'Writing - Abstract'), (2, 'toc-keys', 'Keys to Literacy'),
             (3, 'toc-wcon', 'Writing - Concrete'), (4, 'toc-reading', 'Reading Stages'), (5, 'toc-grammar', 'Grammar')]
TOC_SPLIT = [3, 3]
