"""Montessori Mentor - one page from its Word file (20 Oct 2026).

  python3 tools/build_page.py --docx X.docx --template essay|resources --title "Staff" --folder staff
        [--pdf X.pdf] [--hero hero.jpg] [--hero-pos "center 22%"] [--menu "Staff"] [--section-href /administration/]
        [--out build/staff]

What it does, in order:
 1. Word -> PDF with LibreOffice when no PDF is given (the converter reads photo positions from the PDF).
 2. The converter (tools/convert_curriculum.py, from the records repository) turns Word into page HTML:
    title, headings, labels, quotations, lists, links, italics, underlines, photo rows/sets/floats.
 3. Word's line pictures (very thin images, e.g. image1.gif 623x2) become beige lines, where Word has them.
 4. Site text rules: short dashes only; no spaces round a slash; UK spelling (each change is reported).
 1b. (22 Oct 2026) Word's EMF/WMF drawings become pictures in a working copy of the Word file (tools/drawings.py).
 2b. (22 Oct 2026) Photos the converter finds beside text in the PDF stay beside it (mm-float); label lines ("label, tabs,
    text") get one label column, found from Word - BESIDE and ALIGN_LABELS settings are only needed to override these.
 5. The content goes into the code template (templates/Essay Code Template.html or templates/Resources Code Template.html,
    copied from GitHub omuirithe-a11y/montessori-mentor-templates - the one master copy),
    with the title, the hero, a contents list when the page has headings (none when it has none), and this page's
    menu entry made a link and marked as the current page.
 6. Photos are written as images/NNN.jpg (full size, for the enlarged view) and images/NNN-480.jpg (on the page).
    Photos named in MASK_WHITE have their white background painted the page colour (tools/mask_white.py); any other
    photo with a mostly white edge is reported. <out>/<folder>-originals.zip holds the unblurred originals, numbered.
 7. Two builds from the same file: <out>/preview (copy protection off) and <out>/hostinger/<folder> (copy protection on,
    added only here), plus <out>/<folder>.zip.
 8. A word-for-word comparison of the page text with Word (report.json). The page checks are separate tools
    (tools/check_page.py).
Faces are NOT blurred here: photos with children go through tools/faces (YuNet + blur v7) before step 6 - the report
lists every photo so none is missed.
"""
import html as _html
H = _html.escape
import argparse, os, re, subprocess, sys, json, base64, io, shutil, difflib, zipfile
from bs4 import BeautifulSoup
from PIL import Image
Image.MAX_IMAGE_PIXELS = None   # 20 Oct: 5.5 has a 96-million-pixel picture; it is scaled down below, never shown at that size

T = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(T)
TEMPLATES = {'essay': os.path.join(WS, 'templates', 'Essay Code Template.html'),
             'resources': os.path.join(WS, 'templates', 'Resources Code Template.html')}
PROTECT = os.path.join(WS, 'templates', 'copy-protection.html')

UK = [(r'\bsummariz', 'summaris'), (r'\borganiz', 'organis'), (r'\brecogniz', 'recognis'), (r'\brealiz', 'realis'),
      (r'\bpopulariz', 'popularis'), (r'\bcategoriz', 'categoris'), (r'\bemphasiz', 'emphasis'), (r'\bprioritiz', 'prioritis'),
      (r'\bminimiz', 'minimis'), (r'\bmaximiz', 'maximis'), (r'\bspecializ', 'specialis'), (r'\bcriticiz', 'criticis'),
      (r'\bapologiz', 'apologis'), (r'\butiliz', 'utilis'), (r'\bcharacteriz', 'characteris'), (r'\bstandardiz', 'standardis'),
      (r'\bbehavior', 'behaviour'), (r'\bBehavior', 'Behaviour'), (r'\bcolor(?=(s|ed|ing|ful|less)?\b)', 'colour'), (r'\bColor(?=(s|ed|ing|ful|less)?\b)', 'Colour'),
      (r'\bfavorite', 'favourite'), (r'\bFavorite', 'Favourite'), (r'\bhonor(?=(s|ed|ing|able)?\b)', 'honour'), (r'\blabor\b', 'labour'),
      (r'\bneighbor(?=(s|hood|hoods|ing|ly)?\b)', 'neighbour'), (r'\bcenter\b', 'centre'), (r'\bcenters\b', 'centres'), (r'\bprogram\b', 'programme'),
      (r'\bprograms\b', 'programmes'), (r'\bProgram\b', 'Programme'), (r'\bPrograms\b', 'Programmes'),
      (r'\benrollment', 'enrolment'), (r'\bEnrollment', 'Enrolment'), (r'\bimmuniz', 'immunis'), (r'\bspecializ', 'specialis'), (r'\bpracticed\b', 'practised'), (r'\bPracticed\b', 'Practised'),
      (r'\bpracticing\b', 'practising'), (r'\bgroveling\b', 'grovelling'), (r'\bmodeling\b', 'modelling'), (r'\bjudgment\b', 'judgement'), (r'\bcatalog\b', 'catalogue'), (r'\bdialog\b', 'dialogue'),
      # 21 Oct 2026 (5.5: flavor, formalize, individualized ... were missed): the general -ize and -or rules the text check (fault_checks.py UK) already allows
      (r'(?<!\bs)(?<!\bS)(?<!\bpr)(?<!\bPr)(?<!\bse)(?<!\bSe)(?<!caps)(?<!\bmaz)iz(e|ed|es|ing|ation|ations)\b', r'is\1'),   # 24 Oct 2026 (2.2.0): "Size" had become "Sise" - the exceptions now hold with a capital too
      (r'\b((?i:behavi|col|fav|hon|lab|neighb|hum|flav|harb|rum|endeav|vap|savi|arm|od|val|vig|rig|splend|parl|tum))or(s|ed|ing|ite|ites|ful|al)?\b', r'\1our\2')]
# names of organisations keep their own spelling (e.g. "National Center for Montessori", "Center for Guided Montessori Studies")
KEEP = ['National Center', 'Center for', 'Teachers Center', 'Program Directors', 'Educational Programs']

def site_rules(text_html, report, spaced=False):
    soup = BeautifulSoup(text_html, 'html.parser')
    for node in soup.find_all(string=True):
        if node.parent.name in ('script', 'style'): continue
        s = str(node); o = s
        s = s.replace('–', '-').replace('—', '-')
        if spaced:   # 21 Oct 14:09 (user, 5.4: "correct the dashes"): a dash Word writes against a word ("you -the guide- have") gets a space each side, as the page's other dashes; a hyphen left hanging before "and/or/to" ("second- and third-year") stays
            s = re.sub(r'(?<=\s)-(?=[^\W\d_])', '- ', s)
            s = re.sub(r'(?<=[^\W\d_])-(?=\s)(?!\s+(?:and|or|to)\s+\S+-)', ' -', s)
        s = re.sub(r'\s+/\s+', '/', s)
        s = s.replace('\u00a0', ' ')
        s = re.sub(r'\blead guide\b', 'Lead Guide', s, flags=re.I)   # 20 Oct 22:10 (user): capitalise 'Lead Guide' always
        gaps = re.search(r'\S {3,}\S', s) is not None
        s = re.sub(r'(?<=\S)  (?=\S)', ' ', s)
        for pat, rep in UK:
            def sub(m):
                ctx = s[max(0, m.start() - 20):m.end() + 25]
                return m.group(0) if any(k in ctx for k in KEEP) else m.expand(rep)   # 21 Oct 2026: expand, so a rule can keep part of the word
            s = re.sub(pat, sub, s)
        dash = node.parent.name != 'span' or 'mm-nb' not in (node.parent.get('class') or [])
        dash = dash and re.search(r'(?:^|(?<=\s))-\w', s) is not None and not gaps
        dash = False   # 30 Oct 2026 (owner 12:18, "drop it like the live page"): a dash written against the next word is no longer held to it
        if dash:   # 20 Oct (5.2 "School -in Houston" broke after the dash): a dash written against the next word stays with it
            if s.replace(' ', '') != o.replace('\u00a0', '').replace(' ', ''): report.append(('text', o.strip()[:70], s.strip()[:70]))
            bits = re.split(r'((?:^|(?<=\s))-\w+)', s)
            node.replace_with(BeautifulSoup(''.join(('<span class="mm-nb" style="white-space:nowrap">%s</span>' % H(x)) if i % 2 else H(x) for i, x in enumerate(bits)), 'html.parser'))
            continue
        if s != o:
            if s.replace(' ', '') != o.replace('\u00a0', '').replace(' ', ''):
                report.append(('text', o.strip()[:70], s.strip()[:70]))
            if gaps:   # a run of spaces Word uses to line things up -> the site's tab gap
                # 20 Oct: the run keeps its own width (5.1 "Shortlist:" + 11 spaces) - was one space
                bits = re.split(r'( {3,})', s)
                frag = BeautifulSoup(''.join(('<span class="mm-t">%s</span>' % ('\u00a0' * len(x))) if i % 2 else H(x) for i, x in enumerate(bits)), 'html.parser')
                node.replace_with(frag)
            else:
                node.replace_with(s)
    return str(soup)

# 21 Oct (user): "Allow breaks after "/"" - every page, every width: a long word joined by slashes
# (materials/snack/folders/...) may wrap after a slash. The words are unchanged; <wbr> adds no text.
def slash_breaks(text_html, report):
    soup = BeautifulSoup(text_html, 'html.parser'); n = 0
    for node in soup.find_all(string=True):
        if node.parent.name in ('script', 'style'): continue
        s = str(node)
        if not re.search(r'(?<=\w)/(?=\w)', s) or re.search(r'https?:|www\.', s): continue
        bits = re.split(r'(?<=\w)/(?=\w)', s); n += len(bits) - 1
        node.replace_with(BeautifulSoup('/<wbr>'.join(H(b, quote=False) for b in bits), 'html.parser'))
    if n: report.append(('text', 'line break allowed after a slash', '%d places' % n))
    return str(soup)

def word_list(d, start_text, tabs=None):
    """A list part straight from Word (20 Oct): from the paragraph that reads start_text. Its own line in a colour ->
    the heading (h2, in the contents) for the first, a red region name for red lines; other lines -> entries, keeping
    Word's blue names, links and italics; a link reading PDF -> the site's PDF badge; tabs dropped; empty lines dropped."""
    from docx.oxml.ns import qn
    rels = {r.rId: r for r in d.part.rels.values()}
    ps = d.paragraphs; i0 = next(i for i, p in enumerate(ps) if p.text.strip() == start_text)
    out = ['<h2 class="mm-hc-00B050" id="%s">%s</h2>' % (re.sub(r'[^a-z0-9]+', '-', start_text.lower()).strip('-'), H(start_text))]
    def colour(r):
        c = r.find(qn('w:rPr')); c = c.find(qn('w:color')) if c is not None else None
        return (c.get(qn('w:val')) or '').upper() if c is not None else ''
    for p in ps[i0 + 1:]:
        if not p.text.strip(): continue
        parts = []; cols = set()
        for ch in p._p:
            tag = ch.tag.split('}')[1]
            if tag not in ('r', 'hyperlink'): continue
            runs = [ch] if tag == 'r' else ch.findall(qn('w:r'))
            href = None
            if tag == 'hyperlink':
                rid = ch.get(qn('r:id')); href = rels[rid].target_ref if rid in rels else None
            txt = ''.join((x.text or '') for x in ch.iter(qn('w:t')))
            if not txt.strip(): continue
            c = colour(runs[0]) if runs else ''; cols.add(c)
            it = runs and runs[0].find(qn('w:rPr')) is not None and runs[0].find(qn('w:rPr')).find(qn('w:i')) is not None
            bx = runs[0].find(qn('w:rPr')).find(qn('w:b')) if runs and runs[0].find(qn('w:rPr')) is not None else None
            bd = bx is not None and bx.get(qn('w:val')) not in ('0', 'false') and c in ('', '000000', 'AUTO') and not href   # Resources rule: Word's black bold stays bold; nothing coloured is bold
            # 20 Oct (5.2 "Chantilly Montessori,North"): spaces at either end stay outside the colour span or link - the
            # template draws .mm-blue as an inline-block, which swallows a space inside it at its end
            lead, core, trail = re.match(r'^(\s*)(.*?)(\s*)$', txt, re.S).groups()
            s = H(core)
            if it: s = '<em>%s</em>' % s
            if bd and core: s = '<strong>%s</strong>' % s
            if href and core == 'PDF':
                # 20 Oct (5.2, your "the PDF boxes are in the wrong place"): the badge goes where the PDF puts the PDF link -
                # Word's tabs; data-tabx = its distance from the margin, data-tw = where the text before it ends (points)
                pos = tabs.pop(0) if tabs else None
                at = ' data-tabx="%.1f" data-tw="%.1f"' % pos if pos else ''
                parts.append('<a class="pdf"%s href="%s" rel="noopener" target="_blank">PDF</a>' % (at, H(href))); continue
            if href: s = '<a href="%s" rel="noopener" target="_blank">%s</a>' % (H(href), s)
            elif c == '0432FF': s = '<span class="mm-blue">%s</span>' % s
            parts.append((' ' if lead else '') + s + (' ' if trail else ''))
        body = re.sub(r'\s+(?=<a class="pdf")', '', ''.join(parts).strip())   # the badge is placed by its own rule, not by spaces
        if cols <= {'EE0000', 'FF0000'} and cols and '<a' not in body:
            out.append('<p class="mm-region">%s</p>' % body)
        else:
            out.append('<p class="mm-entry">%s</p>' % body)
    return '\n'.join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--docx', required=True); ap.add_argument('--pdf'); ap.add_argument('--template', default='essay')
    ap.add_argument('--title', required=True); ap.add_argument('--folder', required=True)
    ap.add_argument('--hero'); ap.add_argument('--hero-pos', default='')
    ap.add_argument('--menu'); ap.add_argument('--section-href')
    ap.add_argument('--photos', help='folder of blurred working copies, named as in Word (image2.jpg ...)')
    ap.add_argument('--out')
    ap.add_argument('--menu-from', help='a live page (index.html) whose menu the page takes (tools/menu_sync.py rules: this page and its section marked, The Prepared Environment a link)')
    ap.add_argument('--no-toc', action='store_true', help='no table of contents, even when the page has headings')
    ap.add_argument('--no-faces', help='reason: the page has no photo of a child (25 Oct 2026 faces lock)')
    ap.add_argument('--settings', help='page settings file (pages/<folder>.py): ROW_ORDER, DROP, LIST_FROM, CSS')
    ap.add_argument('--shown-width', type=int, default=480, help='width of the copy shown on the page (the page\'s own: 480, or 960 on Biography, Aun Aprendo, A Montessori Journey) - 30 Oct 2026')
    ap.add_argument('--no-blur', help='record file (JSON) of the owner\'s own words that this page needs no blurring (30 Oct 2026)')
    a = ap.parse_args()
    # 30 Oct 2026 (owner 09:24, "I agree to the no-blur option in the build tool"): a page the owner has said needs no blurring is
    # built from the Word originals, with no faces rounds. Only with a record file holding her words, the page's folder name and
    # the Word file's SHA-256 - a page not named, a Word file changed since, or a record without her words is refused.
    if a.no_blur:
        if a.photos or a.no_faces: sys.exit('Refused: --no-blur cannot be used with --photos or --no-faces.')
        import hashlib as _hl
        try: _nb = json.load(open(a.no_blur, encoding='utf-8'))
        except Exception as _e: sys.exit('Refused: --no-blur record %s cannot be read (%s).' % (a.no_blur, _e))
        if not str(_nb.get('words', '')).strip() or not str(_nb.get('said', '')).strip():
            sys.exit('Refused: --no-blur record has no owner\'s words ("words") or no time they were said ("said").')
        if _nb.get('page') != a.folder:
            sys.exit('Refused: --no-blur record is for page "%s", not "%s".' % (_nb.get('page'), a.folder))
        _h = _hl.sha256(open(a.docx, 'rb').read()).hexdigest()
        if _nb.get('docx_sha256') != _h:
            sys.exit('Refused: the Word file is not the one the --no-blur record names (record %s, file %s).' % (str(_nb.get('docx_sha256'))[:16], _h[:16]))
        report_noblur_ = ('faces', 'no blurring - the owner\'s words', '"%s" (%s); Word file %s' % (_nb['words'], _nb['said'], _h[:16]))
    # 25 Oct 2026: the faces lock closed - a page with photos is never built from unblurred copies, and never before the user's
    # round 2 answer. --no-faces "<reason>" is for a page whose Word file has no photo of a child (the reason goes in the report).
    if not a.photos and not a.no_faces and not a.no_blur:
        sys.exit('Refused: no --photos (blurred copies from faces.py blurfull). A page is built only from blurred copies; for a page with no child in any photo pass --no-faces "<reason>".')
    if a.no_faces and not a.photos:   # 25 Oct 2026 (user 13:07): --no-faces only for a Word file with no image at all; a page with images goes through the faces rounds
        import zipfile as _zf   # 26 Oct 2026: a plain 'import zipfile' here made zipfile local to main() and broke every --photos build (UnboundLocalError)
        _media = [n for n in _zf.ZipFile(a.docx).namelist() if n.startswith('word/media/')]
        if _media:
            sys.exit('Refused: --no-faces, but the Word file has %d images. Every page with images goes through faces round 1 and round 2 (START-HERE "Faces"); build with --photos.' % len(_media))
    # 26 Oct 2026 (the owner 14:03, "fix all of these now"): the old routes are closed. Blurred copies come only from
    # faces/photos-final, made by blur2/page.py handoff under the agreed method; photos-full and any other folder are the
    # retired v8 route and are refused, so a page cannot be built from them by habit or by a copied command line.
    if a.photos and os.path.basename(os.path.abspath(a.photos.rstrip('/'))) != 'photos-final':
        sys.exit('Refused: --photos %s. Since 26 Oct 2026 a page is built only from faces/photos-final (the agreed blur '
                 'method version 22). Make it with: python3 blur2/page.py handoff <set> --faces <build/<address>/faces>'
                 % a.photos)
    if a.photos and not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(a.photos.rstrip('/'))), 'review2.json')):
        sys.exit('Refused: no faces round 2 answer recorded (review2.json beside the faces folder). Make the round 2 sheet, send it and record the answer.')
    if a.photos:   # 22 Oct 2026 (user 23:11, "yes i do"): the faces round 2 lock - a page is not built from blurred photos while a round 2
        # sheet (faces/round2.html) waits for the user's answer: review2.json must hold it ("sheet": "round2.html", "words": the
        # user's words), recorded after the sheet was made (round 2 of START-HERE "Faces" was skipped on 2.1.2, 22 Oct)
        _fd = os.path.dirname(os.path.abspath(a.photos.rstrip('/'))); _r2 = os.path.join(_fd, 'round2.html'); _a2 = os.path.join(_fd, 'review2.json')
        # 26 Oct 2026 (blur method v22): the new method's sheets are not faces/round2.html. Its blurred copies are in
        # faces/photos-final (from blur2/m_<set>/images, under the Word names); review2.json "final" holds the user's last answer
        # on that set, word for word ("sheet", "words", "answered"), and "check" the separate agent's pass on that sheet.
        _fin = {}
        try: _fin = json.load(open(_a2)).get('final') or {}
        except Exception: pass
        if os.path.basename(os.path.abspath(a.photos.rstrip('/'))) == 'photos-final':
            if not (str(_fin.get('words', '')).strip() and _fin.get('sheet') and _fin.get('check')):
                sys.exit('Refused: photos-final, but review2.json has no "final" answer (sheet, words, check) from the user on the new method\'s sheet.')
            report_final_ = ('faces', 'blurred copies: method v22, the user\'s last answer', '%s - "%s" (%s)' % (_fin['sheet'], _fin['words'], _fin.get('answered', '')))
        elif os.path.exists(_r2):
            _ok = os.path.exists(_a2) and os.path.getmtime(_a2) >= os.path.getmtime(_r2)
            if _ok:
                try: _j = json.load(open(_a2)); _ok = _j.get('sheet') == 'round2.html' and str(_j.get('words', '')).strip() != ''
                except Exception: _ok = False
            if not _ok: sys.exit('Refused: the faces round 2 sheet (%s) has no answer from the user recorded after it was made (review2.json: "sheet": "round2.html", "words": the answer). Send the sheet and wait for the answer.' % _r2)
    import runpy
    S = runpy.run_path(a.settings) if a.settings else {}
    if S.get('TITLE'): a.title = S['TITLE']   # 22 Oct 2026 (user 04:08, "Hero title: \"Observations - Faculty\""): a page's title set in its settings wins over --title
    out = a.out or os.path.join(WS, 'build', a.folder)
    work = os.path.join(out, 'work'); os.makedirs(work, exist_ok=True)
    report = []
    if 'report_final_' in dir(): report.append(report_final_)
    if 'report_noblur_' in dir(): report.append(report_noblur_)
    # 1
    pdf = a.pdf
    side = os.path.splitext(a.docx)[0] + '.pdf'
    if not pdf and os.path.exists(side):
        pdf = side; report.append(('pdf', 'the PDF from Drive next to the Word file', pdf))
    if not pdf:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', work, a.docx], capture_output=True, timeout=240)
        pdf = os.path.join(work, os.path.splitext(os.path.basename(a.docx))[0] + '.pdf')
        report.append(('pdf', 'WARNING: no PDF from Drive - made with LibreOffice; photo places may differ from Word', pdf))
    # 22 Oct 2026 (user: "do all of this"): Word's EMF/WMF drawings become pictures in a working copy of the Word file
    # (tools/drawings.py; same picture names) - the converter stopped on them and faces.py skipped them. Original unchanged.
    sys.path.insert(0, T); import drawings
    prep_ = os.path.join(work, 'source.docx')
    for nm_, how_ in drawings.prepare(a.docx, prep_): report.append(('drawing', nm_, how_))
    word_original = a.docx; a.docx = prep_
    # 2
    src = os.path.join(work, 'src.html')
    cmd = [sys.executable, os.path.join(T, 'convert_curriculum.py'), a.docx, pdf, os.path.join(T, 'pages', 'frame.html'), src,
           '/' + a.folder + '/', a.title]
    if a.photos: cmd.append('--photos=' + a.photos)
    cmd.append('--preview')   # 24 Oct 2026 (2.2.0: 214 pictures, 1.1 GB): the converter's own copies small (900px); step 6 re-reads every original at full size from the Word file
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode: sys.exit('converter failed:\n' + r.stdout + r.stderr)
    report.append(('converter', r.stdout.strip().replace('\n', ' | '), ''))
    s = BeautifulSoup(open(src, encoding='utf-8').read().replace('\t', '\u2409'), 'html.parser')   # tabs kept through BeautifulSoup (20 Oct)
    main_el = s.select_one('main')
    # 3 Word's line pictures -> beige lines, before the paragraph that follows them in Word
    import docx as D
    from docx.oxml.ns import qn
    d = D.Document(a.docx)
    rels = {r.rId: r for r in d.part.rels.values()}
    after = []
    paras = d.paragraphs
    for i, p in enumerate(paras):
        VML = '{urn:schemas-microsoft-com:vml}imagedata'
        blips = [(x.get(qn('r:embed')), '') for x in p._p.iter(qn('a:blip'))] + \
                [(x.get(qn('r:id')), x.get('{urn:schemas-microsoft-com:office:office}title') or '') for x in p._p.iter(VML)]
        for rid, ttl in blips:
            try:
                im = Image.open(io.BytesIO(rels[rid].target_part.blob))
            except Exception:
                continue
            if (im.height <= 6 and im.width >= 100) or (im.width >= 100 and im.width >= 40 * im.height) or 'line' in ttl.lower():   # 21 Oct 2026 (5.5): a line picture 1129x8 - the PDF draws it as a line, so it is one
                nxt = next((q.text.strip() for q in paras[i + 1:] if q.text.strip()), None)
                if nxt: after.append(nxt[:40])
    # 20 Oct: where the PDF draws each line picture (a thin image) wins - the text line just below it (5.1: Word anchors the
    # first line in the opening paragraph, the PDF shows it under "Dear applicant")
    import fitz as _fz
    pdl = []
    _d = _fz.open(pdf)
    for pn_, pg_ in enumerate(_d):
        spans = [(round(l_['bbox'][3]), ''.join(s_['text'] for s_ in l_['spans'])) for b_ in pg_.get_text('dict')['blocks'] for l_ in b_.get('lines', []) if ''.join(s_['text'] for s_ in l_['spans']).strip()]
        for inf in sorted(pg_.get_image_info(), key=lambda i: i['bbox'][1]):
            x0, y0, x1, y1 = inf['bbox']
            if y1 - y0 < 6 and x1 - x0 > 100:
                below = sorted((y, t) for y, t in spans if y > y1)
                if not below and pn_ + 1 < len(_d):
                    nxt_spans = [(round(l_['bbox'][3]), ''.join(s_['text'] for s_ in l_['spans'])) for b_ in _d[pn_ + 1].get_text('dict')['blocks'] for l_ in b_.get('lines', []) if ''.join(s_['text'] for s_ in l_['spans']).strip()]
                    below = sorted(nxt_spans)
                if below:
                    yb = below[0][0]; pdl.append(''.join(t for y, t in below if abs(y - yb) < 3).strip())
    if pdl and len(pdl) == len(after):
        report.append(('beige line', 'placed where the PDF draws them', ' | '.join(x[:30] for x in pdl)))
        after = pdl
    elif pdl:
        report.append(('beige line', 'WARNING: PDF and Word line counts differ, Word kept', '%d PDF / %d Word' % (len(pdl), len(after))))
    _nz = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())
    for t in after:
        # 21 Oct 2026 (5.5): 60 letters, not 25 - two paragraphs began "The Montessori School of Shang..." and both lines went before the first
        tgt = next((e for e in main_el.find_all(['p', 'div', 'h2', 'h3', 'blockquote']) if _nz(e.get_text()).startswith(_nz(t)[:60])), None)
        if tgt:
            sec = tgt.parent
            if sec is not None and sec.name == 'section' and sec.find(True) is tgt: tgt = sec   # a line before a heading goes before its section
            tgt.insert_before(BeautifulSoup('<div class="beige-rule mm-org-rule"></div>', 'html.parser'))
            report.append(('beige line', 'from a line picture in Word, before', t))
    # 6 photos to files; rows to the template's row markup
    # 22 Oct 2026 (the cause of the BESIDE settings on 5.4 and 5.5): the converter already finds, from the PDF, a photo
    # that stands beside text (div.photo-row.ext-float, placed before that text) - this step turned it into a photo row.
    # It now becomes the template's photo beside text (mm-float, on the right). A photo Word puts on the LEFT (data-side)
    # and a set of photos beside text (pdf-set) have no template style yet: reported.
    for row in main_el.select('div.photo-row.ext-float'):
        figs_ = row.find_all('figure')
        if any(f_.get('data-side') == 'left' for f_ in figs_):
            report.append(('photo', 'WARNING: Word puts this photo on the LEFT of its text - shown on the right (no left style in the template)', figs_[0].find('img').get('data-name', '')))
        fl = BeautifulSoup('<div class="mm-float"><div class="mm-imgs"></div></div>', 'html.parser').div
        for f_ in figs_: fl.select_one('.mm-imgs').append(f_.extract())
        row.replace_with(fl)
        report.append(('photo', 'beside its text, as the PDF', ', '.join(f_.find('img').get('data-name', '') for f_ in figs_)))
    for ps_ in main_el.select('div.pdf-set'):
        report.append(('photo', 'WARNING: a set of photos beside text (no template style yet) - check the page', ', '.join(i_.get('data-name', '') for i_ in ps_.select('img'))))
    for row in main_el.select('div.photo-row'):
        row.name = 'div'; row['class'] = ['mm-row']; row['data-above'] = '40'; row['data-level'] = '1'
        wrap = s.new_tag('div', attrs={'class': 'mm-imgs'})
        for f in list(row.find_all('figure', recursive=False)): wrap.append(f.extract())
        row.append(wrap)
    lev_ = 0   # 21 Oct (5.3): rows that follow one another share a level (the template gives them one height and width); a row on its own has its own
    for row in main_el.select('div.mm-row'):
        pv_ = row.find_previous_sibling()
        if not (pv_ is not None and 'mm-row' in (pv_.get('class') or [])): lev_ += 1
        row['data-level'] = str(lev_)
    for p in main_el.find_all('p'):
        if p.find('span', class_='mm-t'): p['class'] = (p.get('class') or []) + ['mm-form']
    # Word's tabs (20 Oct): shown with the template's tab stops (.mm-t, every 48px). Hanging lists, as the page shows Word's
    # lists at the margin: a typed number before the first tab is set like a list number; a leading tab in a list body is dropped.
    nzt = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())
    wp = {}
    for q in paras:
        k = nzt(q.text)
        if k and k not in wp: wp[k] = q
    for t_ in main_el.select('span.mm-t'):   # 20 Oct: tabs after a long run of text are Word's hand-made line breaks (5.3:
        par = t_.find_parent(['p', 'li'])    # "other children's<4 tabs>access") - on the page they show as a space
        if par is None: continue
        before = ''
        for x in par.descendants:
            if x is t_: break
            if isinstance(x, str): before += x
        if len(before.strip()) > 40:
            report.append(('tab', 'tab after long text shown as a space (a Word line break)', before.strip()[-40:]))
            t_.replace_with(' ')
    # 20 Oct (5.3, as Word): list lines Word indents further than the list line before them (another, deeper list -
    # "Chair in" / "Spills/area cleaned up." under "Restores the environment:") are a list inside that line; a line in
    # Word's List Paragraph style with no number, straight after a list, continues the last line ("." under "Colleagues")
    def _ind(q):
        pPr = q._p.pPr; ind = pPr.find(qn('w:ind')) if pPr is not None else None
        return int(ind.get(qn('w:left')) or 0) if ind is not None and ind.get(qn('w:left')) else None
    def _num(q):
        pPr = q._p.pPr; return pPr is not None and pPr.find(qn('w:numPr')) is not None
    def _own(x):   # 21 Oct 2026 (5.5): a list line's own text - once a deeper line was moved inside it, its text included that line and the next deeper lines found no host
        return ''.join(str(n) for n in x.find_all(string=True) if n.find_parent('li') is x)
    def _li(txt):
        k = re.sub(r'\s+', ' ', txt).strip()
        return next((x for x in main_el.find_all('li') if re.sub(r'\s+', ' ', _own(x)).strip() == k), None) if k else None
    prev = None
    for q in paras:
        if _num(q) and q.text.strip():
            if prev is not None and _ind(q) is not None and _ind(prev) is not None and _ind(q) > _ind(prev) + 100:
                li, host = _li(q.text), _li(prev.text)
                if li is not None and host is not None and li is not host:
                    inner = host.find('ul', class_='mm-inner') or host.find('ol', class_='mm-inner')
                    if inner is None:
                        inner = s.new_tag(li.parent.name, attrs={'class': 'mm-inner'}); host.append(inner)
                    old = li.parent; inner.append(li.extract())
                    if old is not None and not old.find('li'): old.decompose()
                    report.append(('list', 'a deeper Word list, inside the line above it', q.text.strip()[:50]))
                    continue   # the host stays the line the next deeper lines belong to
            prev = q
        elif q.text.strip():
            if prev is not None and q.style.name == 'List Paragraph' and not _num(q):
                last = _li(prev.text)
                pe = next((x for x in main_el.find_all('p') if x.get_text().strip() == q.text.strip()), None)
                if last is not None and pe is not None and pe.find_previous(['ol', 'ul']) is last.parent:
                    pe['class'] = (pe.get('class') or []) + ['mm-licont']; last.append(pe.extract())
                    report.append(('list', 'a line Word sets under the list text, kept there', q.text.strip()[:50]))
            prev = None
    labs = S.get('ALIGN_LABELS', [])   # 20 Oct: labels whose text the PDF starts at one column (5.3 Responsibility:/Right:)
    if 'ALIGN_LABELS' not in S:   # 22 Oct 2026 (the cause of the ALIGN_LABELS settings on 5.3, 5.4, 5.5): Word lines each "label, tabs, text" -
        # Word lines the text up with its default tab stops and a different number of tabs per line, which only works in Word's
        # own font; on the page the texts fell in different columns. Two or more such lines on a page: their labels form one
        # column, found here from Word's text (a short label, then tabs, then the rest with no tab)
        _cand = []
        for p_ in main_el.select('p.mm-form'):
            t_ = p_.find('span', class_='mm-t')
            if t_ is None: continue
            lead_ = ''.join(x.get_text() if hasattr(x, 'get_text') else str(x) for x in t_.previous_siblings).strip().strip('\u00a0').strip()
            rest_ = list(t_.next_siblings)
            while rest_ and getattr(rest_[0], 'name', None) == 'span' and 'mm-t' in (rest_[0].get('class') or []): rest_.pop(0)
            if not lead_ or len(lead_) > 30 or re.fullmatch(r'(\d{1,3}|[ivxIVX]{1,5}|[a-zA-Z])[.)]', lead_) or re.search(r'[.;,]$', lead_): continue
            if any(getattr(x, 'name', None) == 'span' and 'mm-t' in (x.get('class') or []) for x in rest_): continue   # more tabs further on: a table-like line, not a label line
            _cand.append(lead_)
        labs = sorted(set(_cand)) if len(_cand) >= 2 else []
        if labs: report.append(('tab', 'label lines found in Word: labels in one column', ' / '.join(labs)))
    for p in main_el.select('p.mm-form'):
        first = p.find('span', class_='mm-t')
        if not labs or first is None: continue
        lead = ''.join(x.get_text() if hasattr(x, 'get_text') else str(x) for x in first.previous_siblings).strip()
        if lead in labs:
            lab = s.new_tag('span', attrs={'class': 'mm-lab'})
            for x in reversed(list(first.previous_siblings)): lab.append(x.extract())
            # drop every tab straight after the label
            while p.find('span', class_='mm-t') is not None and p.contents and p.contents[0].name == 'span' and 'mm-t' in (p.contents[0].get('class') or []):
                p.contents[0].extract()
            # 20 Oct (5.3, as Word and the PDF): the lines after the first start under the text, not under the label (Word's
            # hanging indent); the label's own trailing spaces go (the column places the text)
            from bs4 import NavigableString as _NS
            for x in list(lab.contents)[::-1]:
                if isinstance(x, _NS) and not x.strip(): x.extract()
                elif isinstance(x, _NS): x.replace_with(_NS(x.rstrip(' \u00a0'))); break
                else: break
            while p.contents and isinstance(p.contents[0], _NS) and not p.contents[0].strip(): p.contents[0].extract()
            if p.contents and isinstance(p.contents[0], _NS): p.contents[0].replace_with(_NS(p.contents[0].lstrip(' \u00a0')))
            lab.append('\u00a0')   # a space that keeps the words apart without moving the text off its column
            p.insert(0, lab); p['class'] = (p.get('class') or []) + ['mm-hanglab']
            # Word's space after a label row (5.3: 12pt after each Right, none after each Responsibility) groups the rows in pairs
            wpar = next((q for q in paras if q.text.replace('\u00a0', ' ').split('\t')[-1].strip()[:40] and q.text.replace('\u00a0', ' ').split('\t')[-1].strip()[:40] in p.get_text().replace('\u00a0', ' ')), None)
            if wpar is not None and wpar.paragraph_format.space_after is not None and wpar.paragraph_format.space_after.pt >= 12: p['class'] = p['class'] + ['mm-pairend']
            report.append(('tab', 'label set in one column (page setting)', lead))
    for p in main_el.select('p.mm-form'):
        q = wp.get(nzt(p.get_text())); hang = False
        if q is not None and q._p.pPr is not None:
            ind = q._p.pPr.find(qn('w:ind')); hang = ind is not None and int(ind.get(qn('w:hanging')) or 0) > 0
        first = p.find('span', class_='mm-t')
        if not hang or first is None: continue
        before = list(first.previous_siblings)
        lead = ''.join(x.get_text() if hasattr(x, 'get_text') else str(x) for x in before).strip()
        if not lead:
            # 20 Oct (5.4 "This is a complex...", as Word and the PDF): the tab put the line under the item's text - so does the page
            first.decompose(); p['class'] = (p.get('class') or []) + ['mm-under']
            report.append(('tab', 'leading tab in a list body dropped; the line starts under the item text', p.get_text()[:50]))
        elif re.fullmatch(r'(\d{1,3}|[ivxIVX]{1,5}|[a-zA-Z])[.)]', lead):
            for x in before: x.extract()
            n = s.new_tag('span', attrs={'class': 'mm-n'}); n.string = lead + ' '; first.replace_with(n)
            p['class'] = [c for c in p['class'] if c != 'mm-form'] + ['mm-numline']
            report.append(('tab', 'typed number set like a list number', p.get_text()[:50]))
    # page settings: photo order in a row (Word names), lines to leave out, a list part built from Word
    for order in S.get('ROW_ORDER', []):
        figs = [f for f in main_el.select('.mm-imgs figure') if f.find('img') and f.find('img').get('data-name') in order]
        if figs:
            par = figs[0].parent; [f.extract() for f in figs]
            for nm in order:
                f = next(x for x in figs if x.find('img').get('data-name') == nm); par.append(f)
            report.append(('settings', 'photo order in the row', ', '.join(order)))
    for nm, start in S.get('BESIDE', {}).items():   # 20 Oct: a photo Word floats beside text -> on the right of that block
        img = main_el.find('img', attrs={'data-name': nm})
        _n = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())   # letters and digits only (Word's spaces, quotes and hyphens vary)
        tgt = next((e for e in main_el.find_all(['p', 'ul', 'ol']) if _n(e.get_text()).startswith(_n(start))), None)
        if img is None or tgt is None:
            report.append(('settings', 'WARNING: photo beside text not placed', nm)); continue
        fig = img.find_parent('figure'); row = fig.find_parent('div', class_='mm-row') or fig.find_parent('div', class_='mm-float')   # 22 Oct: the converter's own float is left empty when a setting moves its photo
        mid = ' mm-mid' if nm in S.get('MIDDLE', []) else ''   # 20 Oct 21:3x (your \"center on the space you print\"): centred on the printed text beside it
        fl = BeautifulSoup('<div class="mm-float%s"><div class="mm-imgs"></div></div>' % mid, 'html.parser')
        fl.select_one('.mm-imgs').append(fig.extract()); tgt.insert_before(fl)
        if row is not None and not row.find('img'): row.decompose()
        report.append(('settings', 'photo on the right, beside', nm + ' - ' + start))
    for start in S.get('JOIN', []):   # 20 Oct: a Word paragraph the PDF shows as the second line of the list item above it
        e = next((x for x in main_el.find_all('p') if x.get_text().strip().startswith(start)), None)
        prev = e.find_previous_sibling() if e is not None else None
        if prev is None or prev.name not in ('ul', 'ol') or not prev.find_all('li', recursive=False):
            report.append(('settings', 'WARNING: not joined to a list item', start)); continue
        li = prev.find_all('li', recursive=False)[-1]; li.append(' ')
        for c in list(e.contents): li.append(c.extract())
        nx_ = e.find_next_sibling()
        e.decompose(); report.append(('settings', 'joined to the list item above (as in the PDF)', start))
        # 21 Oct 2026 (5.5 "How did you as an adult re-direct", as Word and the PDF): the Word list continues after the
        # joined line - its next items were a second list with a list's space above them; they rejoin the list
        if nx_ is not None and nx_.name == prev.name and not nx_.get('start') and not nx_.get('class'):
            for c in list(nx_.contents): prev.append(c.extract())
            nx_.decompose(); report.append(('settings', 'the list continues after the joined line, as in Word', start))
    for t in S.get('DROP', []):
        for e in main_el.find_all(['p', 'h2', 'h3', 'div']):
            if e.get_text().strip().startswith(t):
                sec = e.find_parent('section')   # 20 Oct (5.2): the section had been named after the note (its id) - the name goes too
                if sec is not None and (sec.get('id') or '').startswith(re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')): del sec['id']
                e.decompose(); report.append(('settings', 'left out (your note, not page text)', t)); break
    if S.get('LIST_FROM'):
        lf = S['LIST_FROM']; start = None
        for e in main_el.find_all(['p', 'h2', 'h3', 'div']):
            if e.get_text().strip() == lf: start = e; break
        if start is not None:
            sec = start.find_parent('section') or start
            for nx in list(sec.find_next_siblings()): nx.decompose()
            for nx in list(start.find_next_siblings()): nx.decompose()
            # where the PDF puts each PDF link (Word's tabs): (distance from the margin, end of the text before it), points
            import fitz
            tabs = []
            for pg in fitz.open(pdf):
                ws = pg.get_text('words'); mg = min((w[0] for w in ws), default=0)
                lr = [ln['from'] for ln in pg.get_links() if ln.get('uri')]
                for w in ws:   # the word PDF inside a web link (link boxes overlap the next line, so the word, not the box)
                    cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
                    if w[4] != 'PDF' or not any(r.x0 <= cx <= r.x1 and r.y0 <= cy <= r.y1 for r in lr): continue
                    before = [v for v in ws if abs((v[1] + v[3]) / 2 - cy) < 3 and v[2] <= w[0] + 0.5]
                    tabs.append((round(w[1] / 2), w[0] - mg, (max(v[2] for v in before) - mg) if before else 0, pg.number))
            tabs = [(x, tw) for _, x, tw, _ in sorted(tabs, key=lambda q: (q[3], q[0]))]
            nb = len(tabs)
            html_ = word_list(d, lf, tabs)
            report.append(('settings', 'PDF badges placed at the PDF\'s link positions: %d found in the PDF, %d left over' % (nb, len(tabs)), ''))
            start.replace_with(BeautifulSoup(html_, 'html.parser'))
            report.append(('settings', 'list part built from Word from', lf))
    # Word heading colours (20 Oct): a heading, or a short line Word sets all in one heading colour, keeps Word's colour
    # (class mm-hc-<colour>); a plain line the converter missed becomes a heading. Lines in a list part (classed p) skipped.
    HC = ('EE0000', 'FF0000', '0432FF', '00B050')
    nz = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())
    WC = {}
    for p in paras:
        tx = p.text.strip()
        if not tx or len(tx) > 120: continue
        cs = set()
        for r in p._p.iter(qn('w:r')):
            if not ''.join(x.text or '' for x in r.iter(qn('w:t'))).strip(): continue
            rp = r.find(qn('w:rPr')); c = rp.find(qn('w:color')) if rp is not None else None
            cs.add((c.get(qn('w:val')) or '').upper() if c is not None else '')
        if len(cs) == 1 and next(iter(cs)) in HC: WC.setdefault(nz(tx), next(iter(cs)))
    for e in main_el.find_all(['h2', 'h3', 'p']):
        k = nz(e.get_text())
        if k not in WC: continue
        if e.name == 'p':
            if e.get('class') or e.find('a') or e.find_parent(['li', 'blockquote', 'figure']): continue
            e.name = 'h2'; sid = re.sub(r'[^a-z0-9]+', '-', e.get_text().lower()).strip('-')[:60]
            sec = e.parent
            if sec is not None and sec.name == 'section':   # its own section, as the converter makes for headings (same space above)
                ns = s.new_tag('section', attrs={'class': 'section', 'id': sid})
                sibs = [e] + list(e.find_next_siblings()); sec.insert_after(ns)
                for x in sibs: ns.append(x.extract())
            else:
                e['id'] = sid
            report.append(('heading', 'a line in a heading colour in Word, made a heading', e.get_text()[:60]))
        e['class'] = (e.get('class') or []) + ['mm-hc-' + WC[k]]
    if S.get('DIVIDERS_BEFORE'):   # 20 Oct 22:1x (5.4, user: "dividers before all blue headings 30/30"): a beige line before each heading of that Word colour, after the first
        hs_ = [h for h in main_el.find_all('h2') if 'mm-hc-' + S['DIVIDERS_BEFORE'] in (h.get('class') or [])]
        for h in hs_[1:]:
            sec = h.find_parent('section'); tgt = sec if sec is not None and sec.find(True) is h else h
            tgt.insert_before(BeautifulSoup('<div class="beige-rule mm-org-rule" data-setting="1"></div>', 'html.parser'))
            report.append(('beige line', 'before a heading (page setting)', h.get_text()[:40]))
    if S.get('RES_FROM'):   # 20 Oct: the Resources part built as the Resources template's entries (records site/assemble_resources.py)
        rf = S['RES_FROM']
        part = D.Document(a.docx); body = part.element.body; kids = list(body)
        k0 = next(i for i, el in enumerate(kids) if el.tag == qn('w:p') and ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip() == rf)
        for el in kids[:k0]:
            if el.tag != qn('w:sectPr'): body.remove(el)
        pdocx = os.path.join(work, 'resources-part.docx'); part.save(pdocx); phtml = os.path.join(work, 'resources-part.html')
        r2 = subprocess.run([sys.executable, os.path.join(T, 'res', 'assemble_resources.py'), pdocx, os.path.join(T, 'pages', 'frame.html'), phtml,
                             '/' + a.folder + '/', a.title], capture_output=True, text=True, timeout=600)
        if r2.returncode: sys.exit('assemble_resources failed:\n' + r2.stdout + r2.stderr)
        rm = BeautifulSoup(open(phtml, encoding='utf-8').read().replace('\t', '␉'), 'html.parser').select_one('main')
        for dv in rm.select('div.photo-row.ext-float'):     # a photo beside an entry -> the template's mm-float, first in the entry
            nx = dv.find_next_sibling('div', class_='res-entry')
            fl = BeautifulSoup('<div class="mm-float"><div class="mm-imgs"></div></div>', 'html.parser')
            fl.select_one('.mm-imgs').append(dv.find('figure').extract())
            (nx.insert(0, fl) if nx is not None else dv.insert_before(fl)); dv.decompose()
        for dv in rm.select('div.photo-row'):
            dv['class'] = ['mm-row']; dv['data-above'] = '40'; dv['data-level'] = '1'
            wr = s.new_tag('div', attrs={'class': 'mm-imgs'})
            for fg in list(dv.find_all('figure', recursive=False)): wr.append(fg.extract())
            dv.append(wr)
        reds = []   # red runs inside a mixed-colour paragraph (a source named inside a description) keep Word's red
        for p in part.paragraphs:
            cols = []
            for r in p.runs:
                c = r._r.find(qn('w:rPr')); c = c.find(qn('w:color')) if c is not None else None
                cols.append(((c.get(qn('w:val')) or '').upper() if c is not None else '', r.text))
            if len({c for c, t in cols if t.strip()}) > 1:
                cur = '';
                for c, t in cols + [('', 'x')]:
                    if cur and not t.strip(): cur += t; continue   # a space between red runs keeps the name whole
                    if c in ('EE0000', 'FF0000', '0432FF'):   # 20 Oct (5.3 "Creating Classroom Rules"): blue too
                        if not cur: ccol = c
                        cur += t
                    elif cur.strip(): reds.append((cur.strip(), ccol)); cur = ''
                    else: cur = ''
        from bs4 import NavigableString
        for txt, col in reds:
            for node in list(rm.find_all(string=True)):
                if txt in node and not node.find_parent(['a', 'h3']):
                    i = node.index(txt); sp_ = s.new_tag('span', attrs={'style': 'color:#%s' % col}); sp_.string = txt
                    node.replace_with(NavigableString(node[:i]), sp_, NavigableString(node[i + len(txt):]))
                    report.append(('settings', 'red in Word, inside a description', txt[:60])); break
        hd = next((e for e in main_el.find_all('h2') if e.get_text().strip() == rf), None)
        if hd is None:
            hd = next((e for e in main_el.find_all(['p', 'h2', 'h3']) if e.get_text().strip() == rf), None)
        sec = hd.find_parent('section')
        for nx in list(sec.find_next_siblings()): nx.decompose()
        for nx in list(hd.find_next_siblings()): nx.decompose()
        hd.name = 'h2'; hd['class'] = ['mm-hc-00B050']
        for rs_ in rm.find_all('section', recursive=False):
            for c in list(rs_.contents): sec.append(c.extract())
        report.append(('settings', 'Resources part built as the template\'s entries, from', rf + ' (' + r2.stdout.strip().splitlines()[-3][:120] + ')'))
        # 22 Oct 2026 (restored: the published 5.3 has it - "The University of San Diego ..." its own entry): a description that
        # starts with a red source name (Word: the red name and its description in one paragraph) starts a new entry - the red
        # name its name line, the rest its description, the lines after it in the entry go with it
        for d_ in list(main_el.select('div.res-entry > p.res-desc')):
            f_ = next((c for c in d_.contents if not (isinstance(c, NavigableString) and not c.strip())), None)
            if f_ is None or getattr(f_, 'name', None) != 'span' or not re.search(r'color:#(EE0000|FF0000)', f_.get('style', ''), re.I): continue
            if f_.get_text().strip() in S.get('PLAIN_COLOUR', []): continue   # 22 Oct (5.5, user: "Valerie Polakow" in the text colour): a name the page shows as text stays in its description
            ent_ = d_.find_parent('div', class_='res-entry')
            new_ = s.new_tag('div', attrs={'class': list(ent_.get('class') or ['res-entry'])})
            h_ = s.new_tag('h3', attrs={'class': 'material-name res-src'}); h_.string = f_.get_text().strip(); f_.extract()
            while d_.contents and isinstance(d_.contents[0], NavigableString) and not d_.contents[0].strip(): d_.contents[0].extract()
            if d_.contents and isinstance(d_.contents[0], NavigableString): d_.contents[0].replace_with(NavigableString(d_.contents[0].lstrip()))
            rest_ = [d_] + list(d_.find_next_siblings())
            new_.append(h_)
            for x_ in rest_:
                if d_.get_text().strip() or x_ is not d_: new_.append(x_.extract())
                else: x_.decompose()
            ent_.insert_after(new_); ent_.insert_after(NavigableString('\n'))
            report.append(('settings', 'a red source name starting a description made its own entry', h_.get_text()[:60]))
    for r_ in main_el.select('div.mm-org-rule'):   # 21 Oct (5.3): a divider left as the last thing in a section (its heading was made a section after it was placed) goes just before the next section
        sec_ = r_.parent
        if sec_ is not None and sec_.name == 'section' and r_.find_next_sibling() is None and sec_.find_next_sibling('section') is not None:
            sec_.insert_after(r_.extract()); report.append(('beige line', 'moved from the end of a section to before the next section', (sec_.find_next_sibling('section').find(['h2', 'h3']) or sec_).get_text()[:40]))
    if a.template == 'essay':   # 21 Oct (5.3, user: "correct each of them to follow the template"): on the Essay template a divider is the template's own beige line, p.mm-gl, spaced by its own engine
        for r_ in main_el.select('div.mm-org-rule'):
            r_.name = 'p'; r_['class'] = ['mm-gl']
        report.append(('beige line', "the Essay template's own divider (p.mm-gl)", str(len(main_el.select('p.mm-gl')))))
    for a_ in main_el.select('div.res-entry a, div.res-item a'):   # 21 Oct (5.3): a Word link that reads MP4 is a file badge like PDF (the Resources part's "PDF/MP4 badges")
        if a_.get_text().strip() == 'MP4' and 'pdf' not in (a_.get('class') or []):
            a_['class'] = (a_.get('class') or []) + ['pdf']; report.append(('settings', 'MP4 link shown as a file badge', a_.get('href', '')[:60]))
    for t_, line_ in S.get('PDF_TO_TITLE', []):   # 23 Oct 2026 (2.1.2, user 00:18 "move the pdf so it is alongside the title, as it is in the others"):
        # a title Word gives a line of its own (the converter made it a heading) takes the PDF link of the line under it and becomes a
        # title line like the others (blue, the badge 24 after it); the line under it keeps its text
        h_ = next((x for x in main_el.find_all(['h2', 'h3', 'p']) if re.sub(r'\s+', ' ', x.get_text()).strip() == t_), None)
        l_ = next((x for x in main_el.find_all('p') if re.sub(r'\s+', ' ', x.get_text()).strip().startswith(line_)), None)
        a_ = next((x for x in (l_.find_all('a') if l_ is not None else []) if x.get_text().strip() in ('PDF', 'MP4')), None)
        if h_ is None or a_ is None: report.append(('settings', 'WARNING: PDF_TO_TITLE not found', t_)); continue
        if h_.name != 'p':
            sec_ = h_.parent; h_.name = 'p'; h_.attrs = {}
            sp_ = s.new_tag('span', attrs={'class': 'mm-wcol', 'style': 'color:#0432FF'})
            for c_ in list(h_.contents): sp_.append(c_.extract())
            h_.append(sp_)
            if sec_ is not None and sec_.name == 'section' and sec_.find_previous_sibling('section') is not None and sec_.find(['h2', 'h3']) is None:
                prv_ = sec_.find_previous_sibling('section')   # no longer a heading: its lines join the section before
                for x in list(sec_.contents): prv_.append(x.extract())
                sec_.decompose()
        a_.extract()
        from bs4 import NavigableString as _NS4
        while l_.contents and ((isinstance(l_.contents[-1], _NS4) and not l_.contents[-1].strip()) or (getattr(l_.contents[-1], 'name', None) == 'span' and 'mm-t' in (l_.contents[-1].get('class') or []))): l_.contents[-1].extract()
        if l_.contents and isinstance(l_.contents[-1], _NS4): l_.contents[-1].replace_with(l_.contents[-1].rstrip())
        h_.append(a_)
        if l_.find('span', class_='mm-t') is None and 'mm-form' in (l_.get('class') or []): l_['class'] = [c for c in l_['class'] if c != 'mm-form']   # its tab went with the link
        report.append(('settings', 'PDF link moved up beside its title (page setting)', t_))
    if a.template == 'essay':   # 22 Oct 2026 (user 22:57 "ok", 2.1.2): on an Essay page a Word link reading PDF or MP4 at the end of its line is a
        # file badge, as on 5.3 and 5.5 - Word's tab or spaces before it are dropped (the badge's own 24 is the gap) and the line is
        # not justified (the 21 Oct "A": title lines with a badge are not justified); the badge style and pdf-column.html are added below
        from bs4 import NavigableString
        for a_ in main_el.select('p a'):
            if a_.get_text().strip() not in ('PDF', 'MP4') or 'pdf' in (a_.get('class') or []) or a_.find_parent(class_=['res-entry', 'res-item']) is not None: continue
            p_ = a_.find_parent('p')
            if any((getattr(x, 'name', None) or x.strip()) for x in a_.next_siblings): report.append(('settings', 'WARNING: a PDF/MP4 link not at the end of its line - left as a plain link', p_.get_text()[:60])); continue
            while True:   # the tabs and spaces before it, also a tab left at the end of a coloured span
                pv_ = a_.previous_sibling
                if pv_ is None: break
                if isinstance(pv_, NavigableString):
                    if pv_.strip(): pv_.replace_with(pv_.rstrip()); break
                    pv_.extract(); continue
                if pv_.name == 'span' and 'mm-t' in (pv_.get('class') or []): pv_.decompose(); continue
                lt_ = pv_.find_all(string=True)
                while pv_.contents and getattr(pv_.contents[-1], 'name', None) == 'span' and 'mm-t' in (pv_.contents[-1].get('class') or []): pv_.contents[-1].decompose()
                if lt_ and isinstance(pv_.contents[-1] if pv_.contents else None, NavigableString): pv_.contents[-1].replace_with(pv_.contents[-1].rstrip())
                break
            a_['class'] = ['pdf']
            cl_ = [c for c in (p_.get('class') or []) if not (c == 'mm-form' and p_.find('span', class_='mm-t') is None)]
            p_['class'] = cl_ + ['mm-pdfline']
            report.append(('settings', '%s link shown as a file badge (Essay page)' % a_.get_text().strip(), p_.get_text()[:60]))
    if S.get('NO_DIVIDER_BEFORE'):   # 21 Oct (5.3, user: "Red headings: ... remove the divider above"): no beige line before a heading of these Word colours
        for g_ in list(main_el.select('p.mm-gl')):
            nx_ = g_.find_next_sibling()
            h_ = nx_ if nx_ is not None and nx_.name in ('h2', 'h3') else (nx_.find(['h2', 'h3']) if nx_ is not None and nx_.name == 'section' and nx_.find(True) is nx_.find(['h2', 'h3']) else None)
            _hit = h_ is not None and any(('mm-hc-' + c_ in (h_.get('class') or [])) if re.fullmatch(r'[0-9A-F]{6}', c_) else h_.get_text().strip().startswith(c_) for c_ in S['NO_DIVIDER_BEFORE'])   # 21 Oct 13:34: a Word colour, or a heading's own words
            if _hit:
                g_.decompose(); report.append(('beige line', 'left out before a heading (page setting)', h_.get_text()[:40]))
    for st_, px_ in S.get('DIVIDER_SPACE', {}).items():   # 21 Oct 13:34 (5.3, user: "divider 30/30 above"): the beige line before a heading, so far above and below it
        h_ = next((h for h in main_el.find_all(['h2', 'h3']) if h.get_text().strip().startswith(st_)), None)
        sec_ = h_.find_parent('section') if h_ is not None else None
        g_ = sec_.find_previous_sibling() if sec_ is not None and sec_.find(True) is h_ else (h_.find_previous_sibling() if h_ is not None else None)
        if g_ is None or g_.name != 'p' or 'mm-gl' not in (g_.get('class') or []):
            report.append(('beige line', 'WARNING: no beige line before', st_)); continue
        a_, b_ = px_
        g_['data-space'] = g_['data-space-desk'] = g_['data-space-phone'] = str(a_)
        h_['data-space'] = h_['data-space-desk'] = h_['data-space-phone'] = str(b_)
        report.append(('beige line', 'before "%s": %s above, %s below (page setting)' % (st_[:40], a_, b_), ''))
    for lb_ in S.get('UNDERLINE_LABELS', []):   # 21 Oct 13:29/13:32 (5.3, user: "underline"): a label underlined
        e_ = next((x for x in main_el.select('div.micro-label') if x.get_text().strip() == lb_), None)
        if e_ is None: report.append(('settings', 'WARNING: label to underline not found', lb_)); continue
        e_['class'] = (e_.get('class') or []) + ['mm-ulab']; report.append(('settings', 'label underlined', lb_))
    for tx_, href_ in S.get('LINK_TEXT', []):   # 21 Oct 13:31 (5.3, user): words in Word's colour made a link to the place the user named, in the template's link colour
        sp_ = next((x for x in main_el.select('span.mm-wcol') if x.get_text().strip() == tx_), None)
        if sp_ is None: report.append(('settings', 'WARNING: words to link not found', tx_)); continue
        tail_ = sp_.get_text()[len(sp_.get_text().rstrip()):]
        a_ = s.new_tag('a', attrs={'href': href_, 'rel': 'noopener', 'target': '_blank'}); a_.string = tx_
        sp_.replace_with(a_); a_.insert_after(tail_) if tail_ else None
        report.append(('settings', 'made a link', tx_ + ' -> ' + href_))
    for lab_, px_ in S.get('SPACE_AFTER', []):   # 21 Oct (5.3, user: "Space under each 'Right:' = 40"): the template's data-space on the next block
        for p_ in main_el.find_all('p'):
            if p_.get_text().strip().startswith(lab_):
                nx_ = p_.find_next_sibling()
                if nx_ is not None: nx_['data-space'] = nx_['data-space-desk'] = nx_['data-space-phone'] = str(px_)
    for st_, px_ in S.get('SPACE_ABOVE', []):   # 21 Oct (5.3, user: "correct and/or remove all rules that don't fit"): the template's data-space above a block
        for p_ in main_el.find_all('p'):
            if p_.get_text().strip().startswith(st_) and not p_.has_attr('data-space'):
                p_['data-space'] = p_['data-space-desk'] = p_['data-space-phone'] = str(px_)
    # 22 Oct 2026: restored from the 5.3 chat ("BCD sequence", 21 Oct 19:4x) - its saved build tool was overwritten in the Project
    def _sp(e_, v_):   # data-space on a block; v_ a figure, or (computers, phones)
        d_, ph_ = (v_, v_) if not isinstance(v_, (tuple, list)) else v_
        e_['data-space'] = e_['data-space-desk'] = str(d_); e_['data-space-phone'] = str(ph_)
    for it_ in S.get('SPACE_SET', []):   # 21 Oct 19:27-19:41 (5.3, user): a block's space above (and below) set outright, over SPACE_AFTER/SPACE_ABOVE; the words must match one block only
        st_, ab_, be_ = (list(it_) + [None])[:3]
        hit_ = [e_ for e_ in main_el.find_all(['p', 'div', 'h2', 'h3']) if e_.get_text().strip() == st_ or (len(st_) > 12 and e_.get_text().strip().startswith(st_) and not e_.find(['p', 'div']))]
        if len(hit_) != 1: report.append(('settings', 'WARNING: SPACE_SET matched %d blocks' % len(hit_), st_)); continue
        if ab_ is not None: _sp(hit_[0], ab_)
        if be_ is not None:
            nx_ = hit_[0].find_next_sibling()
            if nx_ is None: report.append(('settings', 'WARNING: SPACE_SET nothing below', st_))
            else: _sp(nx_, be_)
    for col_, px_ in S.get('HEAD_AFTER', {}).items():   # 21 Oct 19:36 (5.3, user: "15"): the space under every heading of that Word colour, letters to letters
        for h_ in main_el.select('h2.mm-hc-' + col_):
            nx_ = h_.find_next_sibling()
            if nx_ is not None: _sp(nx_, px_)
    for nm_ in S.get('DROP_PHOTOS', []):   # 21 Oct 19:39 (5.3, user: "delete the positive discipline photo"): a photo left out, by its Word name
        im_ = main_el.select_one('img[data-name="%s"]' % nm_)
        if im_ is None: report.append(('settings', 'WARNING: photo to leave out not found', nm_)); continue
        box_ = im_.find_parent(class_='mm-float') or im_.find_parent('figure'); box_.decompose(); report.append(('settings', 'photo left out (page setting)', nm_))
    if S.get('RES_ENTRIES_EQUAL'):   # 21 Oct (5.3, "correct all faults"): every Resources entry the same space above (the template's "3 or more short lines are a list" rule does not fit entries)
        for e_ in main_el.select('div.res-entry'): e_['class'] = (e_.get('class') or []) + ['mm-lstart']
    if S.get('EVEN_LIST_STEP'):   # 21 Oct (5.3, "correct all faults"): the lines of a list stand an even step apart (the template's data-step), not an even gap between letters that rise and hang differently
        for l_ in main_el.find_all(['ul', 'ol']):
            for li_ in l_.find_all('li', recursive=False)[1:]: li_['data-step'] = str(S['EVEN_LIST_STEP'])
    if S.get('GREYS_TO_INK'):   # 21 Oct (5.3, user: "correct each ... so your page follows the template"): Word's near-black greys take the template's text colour
        for sp_ in main_el.select('span.mm-wcol'):
            if re.search(r'color:#(1A1A1A|222222|000000)', sp_.get('style', ''), re.I): sp_.unwrap()
    if S.get('FLOAT_TOPLINE'):   # 21 Oct (5.3 on the Essay template): a photo beside text starts level with the top of the letters of the first line beside it (the template's glTopline)
        for f_ in main_el.select('div.mm-float'): f_['data-topline'] = '1'
    if S.get('WORD_LIST_INDENT'):   # 20 Oct 21:3x (5.4, your "fix them"): every list and list-body line at Word's own indent
        _nx = zipfile.ZipFile(a.docx).read('word/numbering.xml').decode('utf-8') if 'word/numbering.xml' in zipfile.ZipFile(a.docx).namelist() else ''
        _nm = dict(re.findall(r'<w:num w:numId="(\d+)"[^>]*>.*?<w:abstractNumId w:val="(\d+)"/>', _nx, re.S))
        def _lvl(nid, il='0'):   # the list level's own indent (twips): left, hanging, firstLine
            m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="%s".*?</w:abstractNum>' % _nm.get(nid, '-1'), _nx, re.S)
            lv = re.search(r'<w:lvl w:ilvl="%s".*?</w:lvl>' % il, m.group(0), re.S) if m else None
            g = lambda k: int((re.search(r'<w:ind [^>]*w:%s="(\d+)"' % k, lv.group(0)) or [0, 0])[1]) if lv else 0
            return g('left'), g('hanging'), g('firstLine')
        def _jc(q):   # Word's alignment of the list number (lvlJc): right-aligned numbers end at the marker position
            pPr = q._p.pPr; np_ = pPr.find(qn('w:numPr')) if pPr is not None else None
            if np_ is None or np_.find(qn('w:numId')) is None: return 'left'
            m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="%s".*?</w:abstractNum>' % _nm.get(np_.find(qn('w:numId')).get(qn('w:val')), '-1'), _nx, re.S)
            il = np_.find(qn('w:ilvl')).get(qn('w:val')) if np_.find(qn('w:ilvl')) is not None else '0'
            lv = re.search(r'<w:lvl w:ilvl="%s".*?</w:lvl>' % il, m.group(0), re.S) if m else None
            j = re.search(r'<w:lvlJc w:val="(\w+)"', lv.group(0)) if lv else None
            return j.group(1) if j else 'left'
        def _ind(q):   # Word's indent for a paragraph: its own settings over its list level's (twips)
            pPr = q._p.pPr; np_ = pPr.find(qn('w:numPr')) if pPr is not None else None
            L, Hh, F = _lvl(np_.find(qn('w:numId')).get(qn('w:val'))) if np_ is not None and np_.find(qn('w:numId')) is not None else (0, 0, 0)
            ind = pPr.find(qn('w:ind')) if pPr is not None else None
            if ind is not None:
                if ind.get(qn('w:left')) is not None: L = int(ind.get(qn('w:left')))
                if ind.get(qn('w:hanging')) is not None: Hh, F = int(ind.get(qn('w:hanging'))), 0
                if ind.get(qn('w:firstLine')) is not None: F, Hh = int(ind.get(qn('w:firstLine'))), 0
            return L, Hh, F
        px = lambda tw: round(tw / 15, 1)   # twips -> CSS px (1440 to the inch, 96px to the inch)
        for lst in main_el.find_all(['ol'] if S.get('WORD_LIST_INDENT') == 'numbered' else ['ul', 'ol']):   # 21 Oct 14:37 (user, 5.4): "fix the dash position to follow the template" - 'numbered': dash lists keep the template's place
            li = lst.find('li', recursive=False)
            q = wp.get(nzt(''.join(x for x in li.find_all(string=True, recursive=False)) or li.get_text())) if li is not None else None
            if q is None and li is not None: q = next((w_ for k_, w_ in wp.items() if k_ and nzt(li.get_text()).startswith(k_[:40])), None)
            if q is None: report.append(('list', 'WARNING: Word indent not found for list', li.get_text()[:40] if li else '')); continue
            L, Hh, F = _ind(q)
            if F:   # first line indented, no hanging: the marker at left+firstLine, the text at Word's next default tab stop (720)
                mk = L + F; tx = (mk // 720 + 1) * 720
            else:
                mk = L - Hh; tx = L
            if _jc(q) == 'right': lst['class'] = (lst.get('class') or []) + ['mm-wr']   # 20 Oct 22:2x (5.4 i/ii/iii, as Word and the PDF): numbers end at the marker position
            lst['class'] = (lst.get('class') or []) + ['mm-wi']; lst['style'] = ((lst.get('style') or '').rstrip(';') + ';' if lst.get('style') else '') + '--wm:%spx;--wt:%spx' % (px(mk), px(tx))   # the list's own counter (start) kept
            report.append(('list', 'Word indent: marker %spx, text %spx' % (px(mk), px(tx)), li.get_text().strip()[:40]))
            for li_ in lst.find_all('li', recursive=False)[1:]:   # 21 Oct (5.3 "Chair in", "Spills/area cleaned up."): an item at its own Word indent (a deeper list Word wrote under another) keeps it
                q_ = wp.get(nzt(''.join(x for x in li_.find_all(string=True, recursive=False)) or li_.get_text()))
                if q_ is None: q_ = next((w_ for k_, w_ in wp.items() if k_ and nzt(li_.get_text()).startswith(k_[:40])), None)
                if q_ is None: continue
                L_, H_, F_ = _ind(q_)
                mk_, tx_ = ((L_ + F_), ((L_ + F_) // 720 + 1) * 720) if F_ else (L_ - H_, L_)
                if (mk_, tx_) != (mk, tx):
                    li_['style'] = ((li_.get('style') or '').rstrip(';') + ';' if li_.get('style') else '') + '--wm:%spx;--wt:%spx' % (px(mk_), px(tx_))
                    report.append(('list', 'Word indent of one item: marker %spx, text %spx' % (px(mk_), px(tx_)), li_.get_text().strip()[:40]))
        for p in main_el.select('p.mm-under, p.mm-numline'):
            q = wp.get(nzt(p.get_text()))
            if q is None: continue
            L, Hh, F = _ind(q); p['style'] = 'padding-left:%spx !important' % px(L)
            report.append(('list', 'Word indent: text %spx' % px(L), p.get_text().strip()[:40]))
    for start_, mk_ in S.get('LIST_MARKERS', {}).items():   # 20 Oct 23:2x (5.4, user: "change to a) b) c)"): a list's markers set by the page settings
        li_ = next((x for x in main_el.find_all('li') if x.get_text().strip().startswith(start_)), None)
        if li_ is None: report.append(('list', 'WARNING: list for LIST_MARKERS not found', start_)); continue
        ol_ = li_.find_parent('ol'); ol_['class'] = [c for c in (ol_.get('class') or []) if c not in ('mm-lroman', 'mm-uroman', 'mm-lalpha', 'mm-ualpha')] + ['mm-mk-' + mk_]
        report.append(('list', 'markers set by the page settings: ' + mk_, start_))
    for p_ in main_el.find_all('p'):   # 20 Oct 22:4x: a line that is wholly an underlined phrase - the template spaces it (mm-ul-gap-js)
        us_ = p_.find_all('u')
        if us_ and re.sub(r'\s+', '', ''.join(u_.get_text() for u_ in us_)) == re.sub(r'\s+', '', p_.get_text()) and p_.get_text().strip():
            p_['class'] = (p_.get('class') or []) + ['mm-ul']
    for t_ in S.get('RES_SPLIT_ITEM', []):   # 22 Oct 2026 (5.5, user: "Busy Bee Montessori Center" a red name line with its PDF badge): a title line made the name line of its own entry, the lines after it go with it
        it_ = next((x for x in main_el.select('div.res-entry > div.res-item') if x.select_one('.res-title') is not None and x.select_one('.res-title').get_text().strip() == t_), None)
        if it_ is None: report.append(('settings', 'WARNING: title line to make an entry not found', t_)); continue
        ent_ = it_.find_parent('div', class_='res-entry'); rest_ = list(it_.find_next_siblings())
        new_ = s.new_tag('div', attrs={'class': list(ent_.get('class') or ['res-entry'])})
        h_ = s.new_tag('h3', attrs={'class': 'material-name res-src'}); h_.append(t_)
        b_ = it_.find('a', class_='pdf')
        if b_ is not None: h_.append(b_.extract())
        new_.append(h_)
        for x_ in rest_: new_.append(x_.extract())
        it_.decompose(); ent_.insert_after(new_); ent_.insert_after('\n')
        report.append(('settings', 'a title line made its own entry, a red name line (page setting)', t_))
    for t_ in S.get('PLAIN_COLOUR', []):   # 22 Oct 2026 (5.5, user: "Valerie Polakow" in the text colour): words Word colours shown in the text colour
        sp_ = next((x for x in main_el.find_all('span', style=True) if x.get_text().strip() == t_ and 'color' in x['style']), None)
        if sp_ is None: report.append(('settings', 'WARNING: words to show in the text colour not found', t_)); continue
        sp_.unwrap(); report.append(('settings', 'in the text colour (page setting)', t_))
    if S.get('RES_FROM') and 'RES_DIVIDERS' not in S: S = dict(S, RES_DIVIDERS='all')   # 22 Oct 2026 (user 14:07, from 5.5): a beige line before every Resources entry, by default
    if S.get('RES_DIVIDERS'):   # 20 Oct 23:54 (5.4, user: "dividers between each element in resources"): a beige line between entries
        ents_ = main_el.select('div.res-entry')
        for e_ in (ents_ if S['RES_DIVIDERS'] == 'all' else ents_[1:]):   # 'all' (22 Oct, 5.5 user: "divider 30/30 for red headings in resources" - the first too)
            e_.insert_before(BeautifulSoup('<div class="beige-rule mm-org-rule" data-setting="res"></div>', 'html.parser'))
        report.append(('beige line', 'between Resources entries (page setting)', str(max(0, len(ents_) - 1))))
    # 22 Oct 2026 (5.5, the user's queued edits): general page settings
    _nzb = lambda t: re.sub(r'\s+', ' ', t).strip()
    def _blk(st_):   # the one block whose text starts with these words (a heading's section stands in for it where the heading opens the section)
        hit_ = [e_ for e_ in main_el.find_all(['p', 'div', 'h2', 'h3', 'ul', 'ol', 'blockquote']) if _nzb(e_.get_text()).startswith(st_) and not e_.find(['p', 'div', 'h2', 'h3'])]
        ex_ = [e_ for e_ in hit_ if _nzb(e_.get_text()) == st_]
        if len(ex_) == 1: return ex_[0]   # the block that reads exactly these words wins
        return hit_[0] if len(hit_) == 1 else (None if not hit_ else hit_)
    for st_ in S.get('RULE_BEFORE', []):   # a beige line (30/30, letters to letters) before a block
        b_ = _blk(st_)
        if b_ is None or isinstance(b_, list): report.append(('beige line', 'WARNING: block for a beige line matched %s' % (len(b_) if b_ else 0), st_)); continue
        sec_ = b_.find_parent('section'); tgt_ = sec_ if sec_ is not None and sec_.find(True) is b_ else b_
        tgt_.insert_before(BeautifulSoup('<div class="beige-rule mm-org-rule" data-setting="1"></div>', 'html.parser'))
        report.append(('beige line', 'before a block (page setting)', st_))
    for st_ in S.get('NO_BOLD', []):   # words Word sets bold shown plain
        hit_ = [x for x in main_el.find_all(['strong', 'b']) if _nzb(x.get_text()) == st_]
        if not hit_: report.append(('settings', 'WARNING: bold words not found', st_)); continue
        for x in hit_: x.unwrap()
        report.append(('settings', 'bold removed (page setting, %d)' % len(hit_), st_))
    for st_, html_, style_ in S.get('BLOCK_HTML', []):   # a line's words and look set by the page settings (html None: the line left out)
        b_ = _blk(st_)
        if b_ is None or isinstance(b_, list): report.append(('settings', 'WARNING: line to set matched %s' % (len(b_) if b_ else 0), st_)); continue
        if html_ is None: b_.decompose(); report.append(('settings', 'line left out (page setting)', st_)); continue
        b_.clear(); b_.append(BeautifulSoup(html_, 'html.parser'))
        if style_ is not None: b_['style'] = style_
        report.append(('settings', 'line set by the page settings', st_))
    # 22 Oct 2026 (5.5, the user's second queue, 11:28-11:56): headings, quotations, entry order and badge columns by page setting
    for st_, col_, txt_ in S.get('MAKE_HEADING', []):   # a line made a heading in a Word heading colour, with the words given (its own section, as the converter's headings)
        b_ = _blk(st_)
        if b_ is None or isinstance(b_, list): report.append(('heading', 'WARNING: line to make a heading matched %s' % (len(b_) if b_ else 0), st_)); continue
        b_.name = 'h2'; b_.attrs = {'class': ['mm-hc-' + col_]}; b_.clear(); b_.append(txt_)
        sec_ = b_.parent
        if sec_ is not None and sec_.name == 'section' and sec_.find(True) is not b_:
            ns_ = s.new_tag('section', attrs={'class': 'section', 'id': re.sub(r'[^a-z0-9]+', '-', txt_.lower()).strip('-')[:60]})
            sibs_ = [b_] + list(b_.find_next_siblings()); sec_.insert_after(ns_)
            for x_ in sibs_: ns_.append(x_.extract())
        report.append(('heading', 'made a heading (page setting)', txt_))
    for st_, col_ in S.get('HEAD_COLOUR', {}).items():   # a heading shown in another Word heading colour
        h_ = next((h for h in main_el.find_all('h2') if _nzb(h.get_text()).startswith(st_)), None)
        if h_ is None: report.append(('heading', 'WARNING: heading to recolour not found', st_)); continue
        h_['class'] = [c for c in (h_.get('class') or []) if not c.startswith('mm-hc-')] + ['mm-hc-' + col_]
        report.append(('heading', 'colour %s (page setting)' % col_, st_))
    for st_, how_ in S.get('UNQUOTE', []):   # a quotation shown as body paragraphs; how_ 'cite': its source line goes, in brackets, after the quotation
        bq_ = next((q for q in main_el.find_all('blockquote') if _nzb(q.get_text()).startswith(st_)), None)
        if bq_ is None: report.append(('settings', 'WARNING: quotation to show as text not found', st_)); continue
        ci_ = bq_.find('cite')
        if ci_ is not None:
            if how_ == 'cite':
                ps_ = bq_.find_all('p'); last_ = ps_[-1] if ps_ else None
                if last_ is not None:
                    inner_ = BeautifulSoup(''.join(str(c) for c in ci_.contents), 'html.parser')
                    f_ = next((n for n in inner_.find_all(string=True) if n.strip()), None)
                    if f_ is not None: f_.replace_with(re.sub(r'^\s*[-–—]\s*', '', str(f_)))
                    sp_ = s.new_tag('span', attrs={'class': 'mm-wordrun', 'style': 'font-style:normal !important'}); sp_.append('('); sp_.append(inner_); sp_.append(')')
                    last_.append(' '); last_.append(sp_)
            ci_.decompose()
        for p_ in bq_.find_all('p'): p_['class'] = (p_.get('class') or []) + ['mm-unq']   # italic, as Word sets the quotation; the rest body text
        bq_.unwrap(); report.append(('settings', 'quotation shown as body text (page setting)', st_))
    for st_, before_ in S.get('MOVE_ENTRY_BEFORE', []):   # a Resources entry moved to directly above another (with its beige line)
        nm_ = lambda e: _nzb(e.select_one('h3').get_text()) if e.select_one('h3') else ''
        ents_ = main_el.select('div.res-entry')
        e_ = next((x for x in ents_ if nm_(x).startswith(st_)), None); t_ = next((x for x in ents_ if nm_(x).startswith(before_)), None)
        if e_ is None or t_ is None: report.append(('settings', 'WARNING: entry to move not found', st_ + ' / ' + before_)); continue
        def _with_rule(x):
            p_ = x.find_previous_sibling()
            return [p_, x] if p_ is not None and 'mm-org-rule' in (p_.get('class') or []) else [x]
        mv_ = [y.extract() for y in _with_rule(e_)]
        at_ = _with_rule(t_)[0]
        for y in mv_: at_.insert_before(y)
        report.append(('settings', 'entry moved (page setting)', st_ + ' -> above ' + before_))
    for k_, grp_ in enumerate(S.get('PDF_GROUPS', [])):   # 'Only the groups the user shows share a PDF column' (user 11:55): badges in the named entries, one column (res-extra.html)
        n_ = 0
        for e_ in main_el.select('div.res-entry'):
            h_ = e_.select_one('h3')
            if h_ is None or not any(_nzb(h_.get_text()).startswith(g_) for g_ in grp_): continue
            for it_ in e_.select('div.res-item'):
                if it_.select_one('a.pdf') is not None: it_['data-pdf-group'] = str(k_ + 1); n_ += 1
        report.append(('settings', 'PDF badges in one column: group %d, %d badges (page setting)' % (k_ + 1, n_), ' / '.join(grp_)))
    for it_ in S.get('GAPS', []):   # letters to letters: (words, above, below) - the page part letter-gaps.html sets them after every layout
        st_, ab_, be_ = (list(it_) + [None])[:3]
        b_ = _blk(st_)
        if b_ is None or isinstance(b_, list): report.append(('settings', 'WARNING: GAPS matched %s blocks' % (len(b_) if b_ else 0), st_)); continue
        if isinstance(ab_, (tuple, list)): b_['data-gap'], b_['data-gap-phone'] = str(ab_[0]), str(ab_[1])   # 22 Oct 2026 (5.3): (computers, phones)
        elif ab_ is not None: b_['data-gap'] = str(ab_)
        if be_ is not None:
            nx_ = b_.find_next_sibling()
            while nx_ is not None and 'mm-float' in (nx_.get('class') or []): nx_ = nx_.find_next_sibling()   # a photo beside the text is not the line below
            if nx_ is None and b_.parent is not None and b_.parent.name == 'section':
                nx_ = b_.parent.find_next_sibling()
            if nx_ is None: report.append(('settings', 'WARNING: GAPS nothing below', st_)); continue
            nx_['data-gap'] = str(be_)
        report.append(('settings', 'gap letters to letters (page setting)', '%s: %s above, %s below' % (st_[:40], ab_, be_)))
    for st_, ab_, be_ in S.get('GAPS_EACH', []):   # 22 Oct 2026 (5.3): as GAPS, on every block that starts with these words (a line that repeats, e.g. "Right:"); (words, above, below), letters to letters
        k_ = 0
        for p_ in main_el.find_all(['p', 'div']):
            if p_.find(['p', 'div']) is not None or not p_.get_text().strip().startswith(st_): continue
            k_ += 1
            if ab_ is not None: p_['data-gap'] = str(ab_)
            if be_ is not None:
                nx_ = p_.find_next_sibling()
                while nx_ is not None and 'mm-float' in (nx_.get('class') or []): nx_ = nx_.find_next_sibling()
                if nx_ is not None and not nx_.has_attr('data-gap'): nx_['data-gap'] = str(be_)
        report.append(('settings', 'gap letters to letters on every block (page setting)', '%s: %s above, %s below, %d blocks' % (st_[:30], ab_, be_, k_)))
    for col_, px_ in S.get('HEAD_GAP', {}).items():   # 22 Oct 2026 (5.5, user: "25 under every blue heading"): letters to letters under every heading of that Word colour, over GAPS
        for h_ in main_el.select('h2.mm-hc-' + col_):
            nx_ = h_.find_next_sibling()
            while nx_ is not None and 'mm-float' in (nx_.get('class') or []): nx_ = nx_.find_next_sibling()
            if nx_ is None and h_.parent is not None and h_.parent.name == 'section': nx_ = h_.parent.find_next_sibling()
            if nx_ is None: report.append(('settings', 'WARNING: nothing under the heading', h_.get_text()[:40])); continue
            nx_['data-gap'] = str(px_)
        report.append(('settings', '%s under every %s heading, letters to letters (page setting)' % (px_, col_), str(len(main_el.select('h2.mm-hc-' + col_)))))
    for col_, px_ in S.get('HEAD_ABOVE', {}).items():   # 22 Oct 2026 (5.5, user 13:30 "Space above the blue lines, outside Resources = 30"): letters to letters above every heading of that Word colour; a heading with a beige line above keeps the line's own spacing
        k_ = 0
        for h_ in main_el.select('h2.mm-hc-' + col_):
            sec_ = h_.find_parent('section'); blk_ = sec_ if sec_ is not None and sec_.find(True) is h_ else h_
            pv_ = blk_.find_previous_sibling()
            if pv_ is not None and pv_.name in ('div', 'p') and any(c in (pv_.get('class') or []) for c in ('mm-org-rule', 'mm-gl', 'beige-rule')):
                pv_['data-rule-gap-below'] = str(px_); k_ += 1; continue   # 22 Oct 2026 (user 14:00 "change all"): from the beige line to the heading, the same space
            h_['data-gap'] = str(px_); k_ += 1
        report.append(('settings', '%s above every %s heading, letters to letters (page setting)' % (px_, col_), str(k_)))
    for st_, ab_ in S.get('GAP_LI', []):   # 22 Oct 2026 (5.5, user: "40 above each numbered bold line"): a list line so far below the letters above it
        li_ = [x for x in main_el.find_all('li') if _nzb(x.get_text()).startswith(st_)]
        if len(li_) != 1: report.append(('settings', 'WARNING: list line matched %d' % len(li_), st_)); continue
        li_[0]['data-gap'] = str(ab_); report.append(('settings', 'list line %s above, letters to letters (page setting)' % ab_, st_))
    for st_, letter_ in S.get('LABEL_LETTER', []):   # a lettered label: the letter 24 in from the margin, its words 24 after it
        b_ = _blk(st_)
        if b_ is None or isinstance(b_, list): report.append(('settings', 'WARNING: lettered label not found', st_)); continue
        n_ = next((x for x in b_.find_all(string=True) if x.strip()), None)
        if n_ is None or not n_.lstrip().startswith(letter_): report.append(('settings', 'WARNING: letter not found', st_)); continue
        rest_ = n_.lstrip()[len(letter_):].lstrip()
        sp_ = s.new_tag('span', attrs={'class': 'mm-letter'}); sp_.string = letter_
        gap_ = s.new_tag('span', attrs={'class': 'mm-lsp'}); gap_.string = ' '   # the space kept (copied text reads "a. Sweep"), drawn 24 wide
        n_.replace_with(sp_); sp_.insert_after(gap_); (gap_.insert_after(rest_) if rest_ else None)
        b_['class'] = (b_.get('class') or []) + ['mm-lettered']
        report.append(('settings', 'lettered label (page setting)', st_))
    if S.get('RULE_GAP'):   # 22 Oct 2026 (5.5, user: "divider 30/30"): every beige line so far from the letters above and below it, letters to letters (letter-gaps.html)
        for r_ in main_el.select('div.mm-org-rule'): r_['data-rule-gap'] = str(S['RULE_GAP'])
    for nm_, g_ in S.get('IMG_FILL_GAP', {}).items():   # 22 Oct 2026 (5.5, user 13:40 "fill the space above, 30 below the line above"): with BOTTOM_ON, the photo fills the space above it (res-extra.html), at every computer width
        im_ = main_el.select_one('img[data-name="%s"]' % nm_)
        if im_ is None: report.append(('settings', 'WARNING: photo for IMG_FILL_GAP not found', nm_)); continue
        im_['data-fill-gap'] = str(g_); report.append(('settings', 'photo fills the space above it (page setting)', '%s: %s below the line above' % (nm_, g_)))
    for nm_, h_ in S.get('IMG_HEIGHT', {}).items():   # 22 Oct 2026 (5.5, user 12:37 "make that image 100 high"): a photo beside text this tall on computers (res-extra.html; with BOTTOM_ON its bottom stays on that line)
        im_ = main_el.select_one('img[data-name="%s"]' % nm_)
        if im_ is None: report.append(('settings', 'WARNING: photo for IMG_HEIGHT not found', nm_)); continue
        im_['data-height'] = str(h_); report.append(('settings', 'photo height (page setting)', '%s: %s' % (nm_, h_)))
    for nm_, words_ in S.get('BOTTOM_ON', {}).items():   # a photo beside text: its bottom level with the bottom of the letters of the line holding these words (computers)
        im_ = main_el.select_one('img[data-name="%s"]' % nm_)
        if im_ is None: report.append(('settings', 'WARNING: photo for BOTTOM_ON not found', nm_)); continue
        im_['data-bottom-on'] = words_; report.append(('settings', 'photo bottom level with a line (page setting)', nm_ + ': ' + words_))
    # 21 Oct 2026 (5.5, as Word): inside an italic quotation, words Word sets upright stay upright ("(Montessori 2012)");
    # inside a bold label, characters Word sets plain stay plain (the ":" after "Some questions you might start with")
    from bs4 import NavigableString as _NS3
    def _wrap(el, txt, style):
        for node in list(el.find_all(string=True)):
            i = str(node).find(txt)
            if i >= 0 and node.find_parent('span', class_='mm-wordrun') is None:
                sp = s.new_tag('span', attrs={'class': 'mm-wordrun', 'style': style}); sp.string = txt
                node.replace_with(_NS3(str(node)[:i]), sp, _NS3(str(node)[i + len(txt):])); return True
        return False
    for q in paras:
        k_ = nzt(q.text)[:40]
        if not k_: continue
        runs_ = [(r.text, r.italic, r.bold) for r in q.runs if r.text.strip()]
        if not runs_: continue
        ita = sum(len(t) for t, i, b in runs_ if i) / max(1, sum(len(t) for t, i, b in runs_))
        if ita > 0.8:
            bq_ = next((x for x in main_el.select('blockquote p, p.mm-unq') if nzt(x.get_text()).startswith(k_)), None)
            for t, i, b in (runs_ if bq_ is not None else []):
                if not i:
                    ok_ = _wrap(bq_, t.strip(), 'font-style:normal !important')
                    report.append(('text', 'upright inside a quotation, as Word' if ok_ else 'WARNING: upright words not found in the quotation', t.strip()[:40]))
        lab_ = next((x for x in main_el.select('div.micro-label[data-word-bold="1"]') if nzt(x.get_text()).startswith(k_[:30]) and abs(len(nzt(x.get_text())) - len(nzt(q.text))) <= 3), None)
        if lab_ is not None:
            for t, i, b in runs_:
                if not b:
                    ok_ = _wrap(lab_, t.strip(), 'font-weight:400 !important')
                    report.append(('text', 'plain inside a bold label, as Word' if ok_ else 'WARNING: plain characters not found in the label', t.strip()[:40]))
    # 21 Oct 2026 (5.5 "Observations of children engaged ..." and its "- 'Bringing the Montessori Approach ...'", as Word
    # and the PDF): a plain paragraph Word indents on its first line keeps that indent (Word's points as px, 96/72)
    for q in paras:
        fi_ = q.paragraph_format.first_line_indent
        if fi_ is None or fi_.pt <= 0 or (q.paragraph_format.left_indent and q.paragraph_format.left_indent.pt): continue
        k_ = nzt(q.text)
        if not k_: continue
        if any(q.text.strip().startswith(w_) for w_ in S.get('NO_FIRST_INDENT', [])): report.append(('text', 'first line at the margin (page setting)', q.text[:50])); continue   # 22 Oct 2026 (5.5, user 12:40)
        p_ = next((x for x in main_el.find_all('p') if not x.get('class') and x.find_parent(['li', 'blockquote', 'figure']) is None and nzt(x.get_text()) == k_), None)
        if p_ is None: continue
        p_['style'] = ((p_.get('style') or '').rstrip(';') + ';' if p_.get('style') else '') + 'text-indent:%spx !important' % round(fi_.pt * 4 / 3, 1)
        report.append(('text', 'first line indented %spx, as Word' % round(fi_.pt * 4 / 3, 1), q.text[:50]))
    # 21 Oct 2026 (5.5 "MH and WHQ Classroom Observation Practices  Beginning March 1, 2022", as Word and the PDF): a line
    # the converter made a heading because one part of it is in a heading colour, while the rest of it is in the text colour,
    # is a text line, not a heading - Word's colour on each part, Word's centring, Word's tab as a tab stop (.mm-t)
    for q in paras:
        k_ = nzt(q.text)
        if not k_: continue
        from docx.text.run import Run as _Run   # 22 Oct 2026 (user 22:26, "1"; 2.1.2): Word's links kept on this line (runs inside a link were left out)
        _rr = []
        for _ch in q._p:
            _tg = _ch.tag.split('}')[1]
            if _tg == 'r': _rr.append((_Run(_ch, q), None))
            elif _tg == 'hyperlink':
                _rid = _ch.get(qn('r:id')); _u = rels[_rid].target_ref if _rid in rels else None
                for _x in _ch.findall(qn('w:r')): _rr.append((_Run(_x, q), _u))
        cr_ = [(r.text, (str(r.font.color.rgb).upper() if r.font.color is not None and r.font.color.type is not None and r.font.color.rgb is not None else ''), u_) for r, u_ in _rr if r.text]
        cs_ = {c for t, c, u_ in cr_ if t.strip()}
        if len(cs_) < 2 or not (cs_ & set(HC)) or not (cs_ - set(HC)): continue
        h_ = next((h for h in main_el.find_all('h2') if nzt(h.get_text()) == k_), None)
        if h_ is None: continue
        bits_ = []
        for t, c, u_ in cr_:
            seg_ = re.sub(r'\t+', lambda m: '<span class="mm-t">' + '\u2409' * len(m.group(0)) + '</span>', H(t))   # \u2409: tabs as kept through BeautifulSoup
            if u_: seg_ = '<a href="%s" rel="noopener" target="_blank">%s</a>' % (H(u_), seg_)
            bits_.append('<span class="mm-blue">%s</span>' % seg_ if c == '0432FF' else ('<span style="color:#%s !important">%s</span>' % (c, seg_) if c in HC else seg_))
        np_ = BeautifulSoup('<p class="mm-wordline"%s>%s</p>' % (' style="text-align:center !important"' if q.alignment == 1 else '', ''.join(bits_)), 'html.parser').p
        sa_ = q.paragraph_format.space_after
        if sa_ is not None and sa_.pt > 6:   # Word's space after it, against Word's usual 6pt between paragraphs (the page's 14px)
            np_['style'] = (np_.get('style', '') + ';margin-bottom:%spx !important' % round(14 * sa_.pt / 6, 1)).lstrip(';')
        sec_ = h_.find_parent('section'); prv_ = sec_.find_previous_sibling('section') if sec_ is not None else None
        h_.replace_with(np_)
        if sec_ is not None and prv_ is not None and sec_.find(['h2', 'h3']) is None:   # no longer a heading: no heading space above it - its lines join the section before
            for x in list(sec_.contents): prv_.append(x.extract())
            sec_.decompose()
        report.append(('text', 'a line in two Word colours: a text line with Word\'s colours%s, not a heading' % (', centred' if q.alignment == 1 else ''), q.text[:60]))
    for st_, html_ in S.get('LATE_HTML', []):   # 22 Oct 2026 (5.5, user 12:44): a line's words and look set after the build's own line handling (e.g. the two-colour line)
        hit_ = [x for x in main_el.find_all(['p', 'div']) if _nzb(x.get_text()).startswith(st_) and not x.find(['p', 'div'])]
        if len(hit_) != 1: report.append(('settings', 'WARNING: LATE_HTML matched %d' % len(hit_), st_)); continue
        hit_[0].clear(); hit_[0].append(BeautifulSoup(html_, 'html.parser')); report.append(('settings', 'line set by the page settings (late)', st_))
    # 30 Oct 2026 (Aun Aprendo; the 27 Oct order "Use the template's own name-line markup and class for those lines"): each
    # line named in NAME_LINES (by how it starts) becomes the template's name line <p class="mm-name">, as on the live page,
    # whether the converter made it a heading or a two-colour text line; a section left without a heading joins the one before
    for st_ in S.get('NAME_LINES', []):
        hit_ = [x for x in main_el.find_all(['h2', 'h3', 'p']) if _nzb(x.get_text()).startswith(st_) and not x.find(['p', 'div'])]
        if len(hit_) != 1: report.append(('settings', 'WARNING: NAME_LINES matched %d' % len(hit_), st_)); continue
        x_ = hit_[0]; np_ = main_el.new_tag('p', attrs={'class': 'mm-name'}) if hasattr(main_el, 'new_tag') else BeautifulSoup('<p class="mm-name"></p>', 'html.parser').p
        np_.string = re.sub(r'\s+', ' ', x_.get_text()).strip()
        sec_ = x_.find_parent('section'); prv_ = sec_.find_previous_sibling('section') if sec_ is not None else None
        x_.replace_with(np_)
        pv_ = np_.find_previous_sibling()
        if pv_ is None or pv_.name != 'p' or 'mm-gl' not in (pv_.get('class') or []):   # the template's beige line before each name line, as live
            gl_ = BeautifulSoup('<p class="mm-gl"> </p>', 'html.parser').p
            np_.insert_before(gl_); np_.insert_before(NavigableString('\n'))
        if sec_ is not None and prv_ is not None and sec_.find(['h2', 'h3']) is None:
            for y_ in list(sec_.contents): prv_.append(y_.extract())
            sec_.decompose()
        report.append(('text', 'a name line (the template\'s mm-name) with the beige line before it, as on the live page', st_))
    if S.get('POST_MAIN'):   # 31 Oct 2026 (8.1, owner 21:45 "Ok" to fixing the first-build faults in the build settings): a page's own
        S['POST_MAIN'](main_el, s, report)   # function in its settings file, run on the converted text area; it must use only the template's own classes (the code check proves it)
    for sec in main_el.find_all('section'):
        if not sec.get_text().strip() and not sec.find('img'): sec.decompose()
    # 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere (replaces the 21 Oct rule "every photo
    # on every page includes a description"): no image gets a description; any ALT_TEXT in page settings is not used
    for im_ in main_el.select('img.doc-img'): im_['alt'] = ''
    # photos numbered in page order, after any reordering (Hostinger names 001, 002 ... in page order)
    CROP, TURN = {}, {}
    for dr in d.element.body.iter(qn('w:drawing')):
        blip = dr.find('.//' + qn('a:blip'))
        if blip is None or blip.get(qn('r:embed')) not in rels: continue
        nm = rels[blip.get(qn('r:embed'))].target_ref.split('/')[-1]
        sr = dr.find('.//' + qn('a:srcRect'))
        if sr is not None and any(sr.get(k) for k in 'ltrb'): CROP[nm] = tuple(int(sr.get(k) or 0) / 100000 for k in 'ltrb')
        xf = dr.find('.//' + qn('a:xfrm'))
        if xf is not None and (xf.get('rot') or xf.get('flipH') == '1' or xf.get('flipV') == '1'):
            TURN[nm] = (int(xf.get('rot') or 0) / 60000, xf.get('flipH') == '1', xf.get('flipV') == '1')
    imgdir = os.path.join(out, 'images')
    if os.path.exists(imgdir): shutil.rmtree(imgdir)
    os.makedirs(imgdir)
    n = 0; origs = []
    for img in main_el.find_all('img'):
        m = re.match(r'data:image/([a-z+]+);base64,(.*)', img.get('src', ''), re.S)
        if not m: continue
        n += 1; k = '%03d' % n
        name = img.get('data-name', '')
        try:   # the Word original at full size (the converter's copy may be reduced)
            im = Image.open(io.BytesIO(zipfile.ZipFile(a.docx).read('word/media/' + name))).convert('RGB')
        except Exception:
            im = Image.open(io.BytesIO(base64.b64decode(m.group(2)))).convert('RGB')
        if a.photos and os.path.exists(os.path.join(a.photos, name)):
            im = Image.open(os.path.join(a.photos, name)).convert('RGB')
        if name in CROP:   # 20 Oct: Word's crop and turn, as the converter does them (re-reading the original had dropped them)
            l, t_, r_, b_ = CROP[name]; W0, H0 = im.size
            im = im.crop((round(W0 * l), round(H0 * t_), round(W0 * (1 - r_)), round(H0 * (1 - b_))))
        if name in TURN:
            deg, fh, fv = TURN[name]
            if fh: im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if fv: im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if deg: im = im.rotate(-deg, expand=True)
            report.append(('photo turned as in Word', name, '%g degrees' % deg))
        origs.append((k, name))
        # 22 Oct 2026 (preferences: "photos of objects on a white background have the white masked, always"; book covers and
        # pages keep their white): the white joined to the picture's edge painted the page colour (tools/mask_white.py,
        # from the records repository) for the photos the page settings name in MASK_WHITE; any other photo with a mostly
        # white edge is reported, so none is missed
        import numpy as _np
        _a = _np.asarray(im.convert('RGB')).min(axis=2) > 200
        _edge = _np.concatenate([_a[0], _a[-1], _a[:, 0], _a[:, -1]]).mean()
        if name in S.get('MASK_WHITE', []):
            sys.path.insert(0, T); import mask_white
            _t = os.path.join(work, 'mask-' + k + '.png'); im.save(_t); _m = os.path.join(work, 'masked-' + k + '.png')
            _f, _share = mask_white.mask(_t, _m); im = Image.open(_m).convert('RGB')
            report.append(('photo', k, name + ' white background painted the page colour (%.0f%% of the picture)' % (_share * 100)))
        elif _edge > 0.6:
            report.append(('photo', k, 'WARNING: %s has a mostly white edge (%.0f%%) - an object on white? If so, name it in MASK_WHITE; a book cover or page keeps its white' % (name, _edge * 100)))
        # 30 Oct 2026 (owner 09:09, "Up to 2900 px - yes"): the large copy up to 2900 on its long side (was 2400), never enlarged
        big = im.copy(); big.thumbnail((2900, 2900)); big.save(os.path.join(imgdir, k + '.jpg'), quality=92)
        # 30 Oct 2026 12:5x: the shown copy fits in a square of the shown size (its longer side), quality 85 - as the live pages'
        # copies (live Aun Aprendo 003-960.jpg: 726x960, quality 85); width-only sizing made upright images up to 1.75x heavier
        sw_ = a.shown_width; sm = im.copy(); sm.thumbnail((sw_, sw_)); sm.save(os.path.join(imgdir, '%s-%d.jpg' % (k, sw_)), quality=85)
        img['src'] = 'images/%s-%d.jpg' % (k, sw_); img['data-full'] = 'images/%s.jpg' % k
        report.append(('photo', k, name + ' %dx%d' % im.size + (' (scaled to 2900 long side)' if max(im.size) > 2900 else '')))
    content = ''.join(str(c) for c in main_el.contents)
    content = site_rules(content, report, S.get('DASH_SPACES'))
    for old_, new_ in S.get('TEXT_EDITS', []):   # 20 Oct 23:34: wording the user changed from the Word file
        k_ = content.count(H(old_, quote=False)); content = content.replace(H(old_, quote=False), H(new_, quote=False)); report.append(('text', 'changed by the user (%d found)' % k_, old_ + ' -> ' + new_))
    content = slash_breaks(content, report)
    if S.get('ENTRY_PERIOD'):   # 21 Oct 12:21 (user, 5.2): "periods after each school" - a full stop ends every list line that has none
        _sp = BeautifulSoup(content, 'html.parser'); _k = 0
        for _p in _sp.select('p.mm-entry'):
            _b = _p.find('a', class_='pdf')
            _txt = ''.join(x.get_text() if hasattr(x, 'get_text') else str(x) for x in (_b.previous_siblings if _b else [])) if _b else _p.get_text()
            if _b: _txt = _txt[::-1] if False else ''.join(reversed([x.get_text() if hasattr(x, 'get_text') else str(x) for x in _b.previous_siblings]))
            if not _txt.strip() or _txt.rstrip().endswith('.'): continue
            if _b: _b.insert_before('.')
            else: _p.append('.')
            _k += 1
        content = str(_sp); report.append(('settings', 'full stop added at the end of list lines', '%d lines' % _k))
    if S.get('PLAIN_COMMAS'):   # 21 Oct 12:3x (user, 5.2): "Make all three plain" - a comma in a list line is plain black text, not bold or part of a blue name
        _sp = BeautifulSoup(content, 'html.parser'); _k = 0
        for _p in _sp.select('p.mm-entry'):
            for _st in _p.find_all(['strong', 'b']):
                if _st.get_text() == ',': _st.replace_with(','); _k += 1
            for _el in _p.find_all(['span', 'a']):
                if 'pdf' in (_el.get('class') or []): continue
                _last = _el.contents[-1] if _el.contents else None
                if isinstance(_last, str) and _last.rstrip().endswith(','):
                    _i = str(_last).rstrip().rfind(','); _last.replace_with(str(_last)[:_i]); _el.insert_after(',' + str(_last)[_i + 1:]); _k += 1
        content = str(_sp); report.append(('settings', 'commas in list lines made plain', '%d commas' % _k))
    if S.get('PDF_COLUMN') == 'longest':   # 21 Oct 12:2x (user, 5.2): "One column, 24 px after longest" - the PDF's place is not used
        content, _k = re.subn(r' data-tabx="[^"]*"', '', content)
        report.append(('settings', 'PDF badges: one column 24 after the longest line (PDF place dropped)', '%d badges' % _k))
    # 21 Oct (4th check: copying gave "Classroom FlowTraffic", "2.How"): the space after a label or typed number is kept as a
    # no-break space inside its span - the browser drops a plain trailing space there when text is copied; the layout is unchanged
    _sp = BeautifulSoup(content, 'html.parser')
    for _x in _sp.select('span.mm-lab, span.mm-n'):
        _last = _x.contents[-1] if _x.contents else None
        from bs4 import NavigableString as _NS2
        if isinstance(_last, _NS2): _last.replace_with(_last.rstrip(' \u00a0') + '\u00a0')
        else: _x.append('\u00a0')
    content = str(_sp)
    # 21 Oct (5.4, user: "Left-align that line"): a line a page setting names is not spread to the full width at the widths given
    _left_css = ''
    if S.get('LEFT_ALIGN'):
        _sp = BeautifulSoup(content, 'html.parser')
        for _k, (_start, _media) in enumerate(S['LEFT_ALIGN'].items()):
            _hit = [e for e in _sp.select('li, p') if re.sub(r'\s+', ' ', e.get_text()).strip().startswith(_start)]
            assert len(_hit) == 1, ('LEFT_ALIGN', _start, len(_hit))
            _hit[0]['class'] = (_hit[0].get('class') or []) + ['mm-left%d' % _k]
            _left_css += '@media %s{html body main .mm-left%d,html body main .mm-left%d *{text-align:left !important;text-align-last:auto !important}}' % (_media, _k, _k)
            report.append(('settings', 'line not justified', '%s at %s' % (_start, _media)))
        content = str(_sp)
    # 30 Oct 2026 (owner 12:50, Aun Aprendo: "this page is an exception ... if the images don't align on the edge they will look
    # bad"): ROWS_ONE_GROUP - every image row in one group (no data-level), so the template gives them all one width, as live
    if S.get('ROWS_ONE_GROUP'):
        _sp = BeautifulSoup(content, 'html.parser'); _rk = 0
        for _r in _sp.select('div.mm-row[data-level]'): del _r['data-level']; _rk += 1
        content = str(_sp); report.append(('settings', 'image rows in one group (one width), as live', '%d rows' % _rk))
    # 30 Oct 2026 (owner 12:15-12:18; her rules of 15 Oct "remove such additions when found" and 27 Oct "The templates are in
    # github. They are the source"): the build's own labels the template never reads are left out of the page - the picture's
    # Word name (data-name, kept only where CENTRE_ON needs it), the classes landscape/portrait, and the inline --ar / --hg
    _keep_nm = set((S.get('CENTRE_ON') or {}).keys()); _sp = BeautifulSoup(content, 'html.parser'); _kc = 0
    for _e in _sp.find_all(True):
        if _e.has_attr('data-name') and _e['data-name'] not in _keep_nm: del _e['data-name']; _kc += 1
        if _e.get('class'):
            _c = [c for c in _e['class'] if c not in ('landscape', 'portrait')]
            if len(_c) != len(_e['class']): _e['class'] = _c; _kc += 1
            if not _e['class']: del _e['class']
        if _e.get('style') and re.search(r'--(?:ar|hg)\s*:', _e['style']):
            _st = ';'.join(x for x in _e['style'].split(';') if x.strip() and not re.match(r'\s*--(?:ar|hg)\s*:', x))
            if _st: _e['style'] = _st
            else: del _e['style']
            _kc += 1
    content = str(_sp); report.append(('code', "the build's own labels the template never reads left out", '%d places' % _kc))
    # 5 template
    t = open(TEMPLATES[a.template], encoding='utf-8').read()
    def s1(pat, rep, txt):
        k = len(re.findall(pat, txt, re.S)); assert k == 1, (pat, k); return re.sub(pat, lambda m: rep, txt, flags=re.S)
    t = s1(r'<title>.*?</title>', '<title>%s | Montessori Mentor</title>' % a.title, t)
    _tp = re.search(r'<div class="hero"[^>]*background-position:([^;"]+)', t)   # 21 Oct (5.3): with no --hero-pos the template's own hero position stays
    hp_ = a.hero_pos or (_tp.group(1).strip() if _tp else '')
    pos = (';background-position:%s' % hp_) if hp_ else ''
    t = s1(r'<div class="hero"[^>]*><h1><span>Page title</span></h1></div>',
           '<div class="hero" style="background-image:url(\'images/hero.jpg\')%s"><h1><span>%s</span></h1></div>' % (pos, a.title), t)
    heads = [((h.get('id') or (h.find_parent('section') or {}).get('id')), h.get_text().strip()) for h in BeautifulSoup(content, 'html.parser').find_all('h2')]
    heads = [x for x in heads if x[0]]
    if S.get('TOC_ONLY'):   # 31 Oct 2026 (8.1): the contents box lists only these headings (the page's main sections); the others stay on the page as headings
        heads = [x for x in heads if x[1] in S['TOC_ONLY']]
    if S.get('NO_TOC'): a.no_toc = True   # a page setting, so the page keeps it at every rebuild (21 Oct)
    if heads and not a.no_toc:
        # 31 Oct 2026 (8.1, code check part 1): the contents lists are the template's own - the Resources template has three
        # empty <ul class="toc-essays"> columns (mm-toc3), the Essay template two toc-groups; the entries are shared out over them
        _tm = re.search(r'<div class="toc-grid[^"]*">(.*?)</div></nav>', t, re.S)
        _uls = re.findall(r'<ul class="([^"]+)"></ul>', _tm.group(1)) if _tm else []
        if not _uls: _uls = ['toc-groups', 'toc-groups']
        _n = len(_uls); per = -(-len(heads) // _n)
        cols = [heads[i * per:(i + 1) * per] for i in range(_n)]
        lis = ''.join('<ul class="%s">%s</ul>' % (_uls[i], ''.join('<li><a href="#%s">%s</a></li>' % h for h in c)) for i, c in enumerate(cols))
        k = len(re.findall(r'<div class="toc-grid[^"]*">.*?</div></nav>', t, re.S)); assert k == 1, ('toc', k)
        t = re.sub(r'(<div class="toc-grid[^"]*">).*?(</div></nav>)', lambda m: m.group(1) + lis + m.group(2), t, flags=re.S)
    else:
        # 30 Oct 2026: the template's own contents box is kept, empty - the template hides an empty one, as on the live Aun
        # Aprendo page; removing it changed the template's code outside the content slots (code check part 1)
        report.append(('contents', 'none - ' + ('your command' if a.no_toc else 'the Word file has no headings') + "; the template's empty contents box kept (the template hides it)", ''))
    t = s1(r'<section class="section"></section>', content.replace('\\', '\\\\') if False else content, t) if t.count('<section class="section"></section>') == 1 else t
    # long web addresses written out in the text break onto the next line instead of pushing the page sideways (20 Oct 2026)
    # 22 Oct 2026 04:07 (user: "Inner list markers: use \"o\"."): lists inside a list item are marked o, as Word and the PDF
    _wrap_used = bool(re.search(r'<a\s', content) or re.search(r'class="[^"]*\b(?:mm-numline|mm-under|mm-wi|mm-lab|mm-licont|mm-inner|mm-lsp|mm-hanglab|mm-pairend|mm-n|mm-lroman|mm-mk-alpha-paren|mm-uroman|mm-lalpha|mm-ualpha)\b', content))   # 30 Oct 2026: the block only where the page has something it styles
    if 'id="mm-wrap"' not in t and _wrap_used: t = t.replace('</head>', '<style id="mm-wrap">main a{overflow-wrap:anywhere}main p.mm-numline{position:relative;padding-left:30px}main p.mm-under{padding-left:30px}main ul.mm-wi,main ol.mm-wi{margin-left:0 !important;padding-left:0 !important}main .mm-wi>li{position:relative;padding-left:var(--wt) !important}main .mm-wi>li::before{position:absolute;left:var(--wm) !important}main .mm-wi.mm-wr>li::before{left:auto !important;right:calc(100% - var(--wm)) !important;text-align:right}main .mm-lab{display:inline-block;min-width:8em;text-indent:0}main li > p.mm-licont{margin:8px 0 0 !important;text-indent:0 !important}main ul.mm-inner{margin:8px 0 0 !important;padding-left:24px !important}main ul.mm-inner > li::before{content:\"o\" !important}main .mm-lsp{display:inline-block;width:24px;white-space:pre}main p.mm-hanglab{padding-left:8em !important;text-indent:-8em !important}main p.mm-pairend{margin-bottom:30px !important}@media (max-width:640px){main p.mm-hanglab{padding-left:0 !important;text-indent:0 !important}main p.mm-hanglab .mm-lab{min-width:0;margin-right:.6em}}main p.mm-numline .mm-n{position:absolute;left:0}main ol.mm-lroman>li::before{content:counter(mmn,lower-roman) "."}main ol.mm-mk-alpha-paren>li::before{content:counter(mmn,lower-alpha) ")"}main ol.mm-uroman>li::before{content:counter(mmn,upper-roman) "."}main ol.mm-lalpha>li::before{content:counter(mmn,lower-alpha) "."}main ol.mm-ualpha>li::before{content:counter(mmn,upper-alpha) "."}</style></head>', 1)
    if 'mm-org-rule' in content and 'mm-org-rule-js' not in t:   # beige lines 30/30, letters to letters (20 Oct 2026)
        _at = '<script id="mm-kind-gaps-js">' if '<script id="mm-kind-gaps-js">' in t else '</body>'   # 22 Oct 2026: before the template's spacing scripts, which hook into it
        t = t.replace(_at, open(os.path.join(WS, 'templates', 'org-rule.html'), encoding='utf-8').read() + _at, 1)
        if a.template == 'essay':   # 21 Oct (5.3): the Essay template's spacing engine pads anything that clears a float, and a divider paints its padding (579px beige blocks) - here a divider does not clear, and is re-spaced 30/30 after every layout of the page
            t = t.replace('</body>', '<style id="mm-org-rule-essay">html body main .mm-org-rule{clear:none !important;padding-top:0 !important;padding-bottom:0 !important}</style><script id="mm-org-rule-essay-js">(function(){var pl=window.__mmAfterLayout;window.__mmAfterLayout=function(){if(pl)pl();if(window.__mmOrgRun)window.__mmOrgRun();};})();</script></body>', 1)
    for o_, n_ in S.get('PAGE_CODE_REPLACE', []):   # 21 Oct 2026 18:4x (5.3): a change to the template's code on this page only, the template itself unchanged (restored 22 Oct from the 5.3 chat)
        if t.count(o_) != 1: report.append(('settings', 'WARNING: code to replace found %d times' % t.count(o_), o_[:40])); continue
        t = t.replace(o_, n_)
    if S.get('PHONE_GAPS'):   # 20 Oct 22:0x (5.4, user: "41 and 34"): at phone width, banner to the first letters and the last letters to the footer band
        hg, fg = S['PHONE_GAPS']
        if 'id="mm-phone-gaps-js"' in t:   # 22 Oct 2026: the template has the phone-gaps script; the page's figures go on main
            t = re.sub(r'<main\b', '<main data-phone-gaps="%s,%s"' % (hg, fg), t, count=1); report.append(('settings', 'phone gaps (banner to letters, letters to footer band)', '%s / %s' % (hg, fg)))
        else:
            js_ = ("<script id=\"mm-phone-gaps-js\">(function(){var HG=%s,FG=%s;var cv=document.createElement('canvas').getContext('2d');"
                   "function ink(m,first){var w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT),n,r=document.createRange(),best=null;var ns=[];while((n=w.nextNode())){if(!n.nodeValue.trim())continue;var e=n.parentElement;if(!e||e.closest('nav,script,style')||getComputedStyle(e).display==='none')continue;ns.push(n);}"
                   "if(!first)ns.reverse();for(var k=0;k<ns.length;k++){n=ns[k];var s=n.nodeValue,cs=getComputedStyle(n.parentElement);cv.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;var fm=cv.measureText('Hg'),fa=fm.fontBoundingBoxAscent,fd=fm.fontBoundingBoxDescent;var line=null;"
                   "for(var j=0;j<s.length;j++){var i=first?j:s.length-1-j;if(!s[i].trim())continue;r.setStart(n,i);r.setEnd(n,i+1);var q=r.getClientRects()[0];if(!q||!q.width)continue;if(line===null)line=q.top;if(Math.abs(q.top-line)>2)break;var base=q.top+(q.height-(fa+fd))/2+fa,mt=cv.measureText(s[i]);"
                   "var v=first?base-mt.actualBoundingBoxAscent:base+mt.actualBoundingBoxDescent;best=best===null?v:(first?Math.min(best,v):Math.max(best,v));}if(best!==null)return best;}return null;}"
                   "function run(){var m=document.querySelector('main'),h=document.querySelector('.hero'),bd=document.querySelector('.mc-band');if(!m||window.innerWidth>640)return;"
                   "for(var k=0;k<4;k++){if(h){var t=ink(m,true);if(t!==null){var pt=parseFloat(getComputedStyle(m).paddingTop)||0;m.style.setProperty('padding-top',Math.max(0,pt+HG-(t-h.getBoundingClientRect().bottom)).toFixed(2)+'px','important');}}"
                   "if(bd){var b=ink(m,false);if(b!==null){var mt2=parseFloat(getComputedStyle(bd).marginTop)||0;bd.style.setProperty('margin-top',(mt2+FG-(bd.getBoundingClientRect().top-b)).toFixed(2)+'px','important');}}}}"
                   "function later(d){clearTimeout(run.t);run.t=setTimeout(run,d);}window.addEventListener('load',function(){later(900);setTimeout(run,1600);if(document.fonts)document.fonts.ready.then(function(){later(600);});});"
                   "window.addEventListener('resize',function(){later(400);});document.addEventListener('load',function(e){if(e.target&&e.target.tagName==='IMG')later(200);},true);})();</script>") % (hg, fg)
            t = t.replace('</body>', js_ + '</body>', 1)
            report.append(('settings', 'phone gaps (banner to letters, letters to footer band)', '%s / %s' % (hg, fg)))
    if _left_css: t = t.replace('</head>', '<style id="mm-left">%s</style></head>' % _left_css, 1)
    if S.get('CENTRE_ON'):   # 20 Oct 23:28 (5.4, user: 'centre on "the others using the same steps"'): a photo beside text centred on one line of it
        for nm_, words_ in S['CENTRE_ON'].items():
            t = t.replace('data-name="%s"' % nm_, 'data-name="%s" data-centre-on="%s"' % (nm_, H(words_)), 1)
        main_marks_ = 1   # the template's photo script leaves a float marked mm-fitlines to its own placing

        # at computer width the photo is taken out of the template's photo scripts (class mm-float -> mm-co) and placed here;
        # the list keeps a fixed width (room on its right), so moving the photo cannot re-wrap the text
        js_ = ("<script id=\"mm-centre-on-js\">(function(){"
               "function rects(blk,words){var w=document.createTreeWalker(blk,NodeFilter.SHOW_TEXT),n;while((n=w.nextNode())){var i=n.nodeValue.indexOf(words);if(i>=0){var r=document.createRange();r.setStart(n,i);r.setEnd(n,i+words.length);return [].filter.call(r.getClientRects(),function(q){return q.width>0;});}}return null;}"
               "function run(){[].forEach.call(document.querySelectorAll('main img[data-centre-on]'),function(img){var f=img.closest('.mm-float,.mm-co'),pim=img.closest('.pim'),words=img.getAttribute('data-centre-on');if(!f||!pim)return;var blk=f.nextElementSibling,sec=f.parentElement;"
               "if(window.innerWidth<1200){if(f.classList.contains('mm-co')){f.classList.remove('mm-co');f.classList.add('mm-float');f.removeAttribute('style');pim.style.removeProperty('height');pim.style.removeProperty('width');blk.style.removeProperty('padding-right');blk.style.removeProperty('margin-bottom');window.dispatchEvent(new Event('resize'));}return;}"
               "if(f.classList.contains('mm-float')){var h0=pim.getBoundingClientRect().height,w0=pim.getBoundingClientRect().width;pim.style.setProperty('height',h0+'px','important');pim.style.setProperty('width',w0+'px','important');f.classList.remove('mm-float');f.classList.add('mm-co');f.removeAttribute('style');}"
               "var w=pim.getBoundingClientRect().width;sec.style.position='relative';f.style.cssText='position:absolute !important;right:0 !important;margin:0 !important;padding:0 !important;float:none !important';"
               "blk.style.setProperty('padding-right',(w+32)+'px','important');"
               "for(var k=0;k<3;k++){var rs=rects(blk,words);if(!rs||!rs.length)return;var top=Math.min.apply(null,rs.map(function(q){return q.top;})),bot=Math.max.apply(null,rs.map(function(q){return q.bottom;}));"
               "var c=(top+bot)/2-sec.getBoundingClientRect().top,h=pim.getBoundingClientRect().height;f.style.setProperty('top',(c-h/2).toFixed(2)+'px','important');}"
               "var pb=pim.getBoundingClientRect().bottom,bb=blk.getBoundingClientRect().bottom;blk.style.removeProperty('margin-bottom');if(pb+16>bb)blk.style.setProperty('margin-bottom',(pb-bb+16).toFixed(2)+'px','important');});}"
               "function later(d){clearTimeout(run.t);run.t=setTimeout(run,d);}"
               "window.addEventListener('load',function(){later(800);setTimeout(run,1800);setTimeout(run,3600);});window.addEventListener('resize',function(){later(500);});})();</script>")
        t = t.replace('</body>', js_ + '</body>', 1)
        report.append(('settings', 'photo centred on a line of its text', ', '.join('%s: %s' % kv for kv in S['CENTRE_ON'].items())))
    if S.get('LABEL_PHONE') == 'own-line':   # 21 Oct 00:1x (5.4, user: "Label on its own line"): on phones the label stands above its description
        t = t.replace('</head>', '<style id="mm-labphone">@media (max-width:640px){html body main p.mm-hanglab{padding-left:0 !important;text-indent:0 !important}html body main p.mm-hanglab .mm-lab{display:block !important;min-width:0 !important;margin:0 0 4px !important}}</style></head>', 1)
    if S.get('LABEL_COL'):   # 20 Oct 21:3x (5.4 "Order and Aesthetics" was 1px wider than 8em): the label column's width, a page setting
        c_ = S['LABEL_COL']; t = t.replace('</head>', '<style id="mm-labcol">@media (min-width:641px){main .mm-lab{min-width:%s !important}main p.mm-hanglab{padding-left:%s !important;text-indent:-%s !important}}</style></head>' % (c_, c_, c_), 1)
    if S.get('CSS'): t = t.replace('</head>', '<style id="mm-page">' + S['CSS'] + '</style></head>', 1)
    for f_ in S.get('BODY_END', []):   # 21 Oct 2026 (5.3 on the Essay template): a page part from the Resources template (e.g. tools/pages/pdf-column.html) added before </body>
        h_ = open(os.path.join(T, 'pages', f_), encoding='utf-8').read()
        if h_.strip() and h_.strip()[:40] not in t: t = t.replace('</body>', h_ + '</body>', 1); report.append(('settings', 'page part added', f_))
    if a.template == 'essay' and 'mm-pdfline' in t:   # 22 Oct 2026 (2.1.2): the badges' look (5.3's) and the column rule, once each
        css_ = ('html body main p.mm-pdfline{text-align:left !important}'
                'html body main p.mm-pdfline a.pdf{display:inline-block;vertical-align:.12em;font-family:var(--sans,sans-serif);font-size:11px;font-weight:400;letter-spacing:.06em;line-height:1;padding:4px 6px;border:1.5px solid #0563C1;border-radius:2px;color:#0563C1 !important;text-decoration:none !important}'
                'html body main p.mm-pdfline a.pdf:hover{background:#0563C1;color:#fff !important}')
        t = t.replace('</head>', '<style id="mm-pdfline">' + css_ + '</style></head>', 1)
        if 'mm-pdf-column-js' not in t:
            t = t.replace('</body>', open(os.path.join(T, 'pages', 'pdf-column.html'), encoding='utf-8').read() + '</body>', 1)
        report.append(('settings', 'Essay page PDF/MP4 badges: style and pdf-column.html added', ''))
    # 20 Oct (5.2): PDF badges on neighbouring lines stand in one column - the rule is in the Resources template
    # (mm-pdf-column-js, your words 19:1x); the build only gives each badge its PDF place (data-tabx)
    if a.menu:
        k = t.count('<span class="np">%s</span>' % a.menu)
        t = t.replace('<li><span class="np">%s</span></li>' % a.menu, '<li><a href="/%s/" aria-current="page">%s</a></li>' % (a.folder, a.menu))
        report.append(('menu', '"%s" made a link to /%s/ and marked (%d found)' % (a.menu, a.folder, k), ''))
    if a.section_href:
        t = t.replace('<a class="top" href="%s">' % a.section_href, '<a class="top" href="%s" aria-current="page">' % a.section_href, 1)
    # 7 builds
    t = t.replace('\u2409', '\t')
    if a.menu_from:   # 26 Oct 2026 (25 Oct to-do for 2.2.0: "run menu_sync with the live menu"): the live menu, before the preview, Hostinger copy and zip are written
        _tmp = os.path.join(work, 'menu-sync.html'); open(_tmp, 'w', encoding='utf-8').write(t)
        _r = subprocess.run([sys.executable, os.path.join(T, 'menu_sync.py'), a.menu_from, a.folder, _tmp], capture_output=True, text=True)
        if _r.returncode: sys.exit('menu_sync failed: ' + _r.stderr[-500:])
        t = open(_tmp, encoding='utf-8').read(); report.append(('menu', 'live menu from ' + a.menu_from, _r.stdout.strip().split(' | ', 1)[-1]))
        # 31 Oct 2026 (8.1, a new page): the live menu shows a page not yet built as plain text; this page's own entry becomes its link, marked
        _np = '<span class="np">%s</span>' % a.menu if a.menu else None
        if _np and 'href="/%s/"' % a.folder not in t and t.count(_np) == 1:
            t = t.replace(_np, '<a href="/%s/" aria-current="page">%s</a>' % (a.folder, a.menu))
            report.append(('menu', 'own entry, plain text in the live menu, made a link and marked', a.menu))
    pv = os.path.join(out, 'preview'); hs = os.path.join(out, 'hostinger', a.folder)
    for dd in (pv, hs):
        if os.path.exists(dd): shutil.rmtree(dd)
        shutil.copytree(imgdir, os.path.join(dd, 'images'))
        if a.hero: Image.open(a.hero).convert('RGB').save(os.path.join(dd, 'images', 'hero.jpg'), quality=90)
    open(os.path.join(pv, 'index.html'), 'w', encoding='utf-8').write(t)
    pr = open(PROTECT, encoding='utf-8').read()
    css = re.search(r'<style id="mm-protect">.*?</style>', pr, re.S).group(0); js = re.search(r'<script id="mm-protect-js">.*?</script>', pr, re.S).group(0)
    open(os.path.join(hs, 'index.html'), 'w', encoding='utf-8').write(t.replace('</head>', css + '</head>', 1).replace('</body>', js + '</body>', 1))
    z = os.path.join(out, a.folder + '.zip')
    # 25 Oct 2026 (user 13:07, "guarantee that all of these steps are used every time"): no upload zip until the checking
    # agent has measured the last faces sheet - faces/sheet-check.json {"sheet": "round2.html", "pass": true, "by": "<agent>",
    # "measured": "<pixels outside the outlines>"}, recorded after that sheet was made. The preview is still built for checking.
    if a.photos and os.path.basename(os.path.abspath(a.photos.rstrip('/'))) == 'photos-final':
        # 26 Oct 2026 (method v22): the old round 2 check (sheet-check.json) is about the retired method and does not count here;
        # the upload zip needs faces/sheet-check-final.json - the separate agent's passed check of the sheet named in
        # review2.json "final" (copied from blur2/m_<set>/sheet-check.json)
        _fd = os.path.dirname(os.path.abspath(a.photos.rstrip('/'))); _scf = os.path.join(_fd, 'sheet-check-final.json')
        try:
            _jc = json.load(open(_scf)); _jf = json.load(open(os.path.join(_fd, 'review2.json')))['final']
            _okf = _jc.get('pass') is True and bool(_jc.get('sheet')) and _jc['sheet'] in _jf.get('sheet', '')
            # 26 Oct 2026 13:4x (Project instructions: "round 2 sheet, my answer, a separate agent's pixel check, then build"): the
            # upload zip also needs faces/pixel-check-after-answer.json - a separate agent's passed pixel check of the final images,
            # made after the user's last answer ("answered" in review2.json "final"), "time" as YYYY-MM-DD HH:MM in Shanghai time
            _pa = json.load(open(os.path.join(_fd, 'pixel-check-after-answer.json')))
            _okf = _okf and _pa.get('pass') is True and str(_pa.get('time', ''))[:16] > str(_jf.get('answered', ''))[:16]
        except Exception: _okf = False
        if not _okf:
            if os.path.exists(z): os.remove(z)
            print('NO UPLOAD ZIP: no passed check by a separate agent (%s) of the sheet the user last answered.' % _scf)
            report.append(('faces', 'NO UPLOAD ZIP - final sheet not checked by a separate agent', _scf)); z = None
        else: report.append(('faces', 'upload zip allowed - final sheet checked by a separate agent', '%s %s' % (_jc['sheet'], _jc.get('time', ''))))
    elif a.photos:
        _fd = os.path.dirname(os.path.abspath(a.photos.rstrip('/'))); _sc = os.path.join(_fd, 'sheet-check.json'); _r2 = os.path.join(_fd, 'round2.html')
        _ok = os.path.exists(_sc) and (not os.path.exists(_r2) or os.path.getmtime(_sc) >= os.path.getmtime(_r2))
        if _ok:
            try: _j = json.load(open(_sc)); _ok = _j.get('pass') is True and _j.get('sheet') == 'round2.html' and bool(_j.get('measured'))
            except Exception: _ok = False
        if not _ok:
            if os.path.exists(z): os.remove(z)
            print('NO UPLOAD ZIP: the faces round 2 sheet has no passed pixel check by a separate agent recorded after it (%s). Preview built for checking only.' % _sc)
            report.append(('faces', 'NO UPLOAD ZIP - round 2 sheet not checked by a separate agent', _sc))
            z = None
    if z:
     with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(os.path.join(out, 'hostinger')):
            for f in fs:
                p = os.path.join(root, f); zf.write(p, os.path.relpath(p, os.path.join(out, 'hostinger')))
    # 22 Oct 2026 (preferences: hi-res photos sent as a numbered download for every page; unblurred originals after
    # publishing): <out>/<folder>-originals.zip - each photo exactly as stored in the Word file (unblurred, uncropped),
    # numbered as on the page (001, 002 ...); a drawing as its picture (drawings.py)
    zo_ = os.path.join(out, a.folder + '-originals.zip')
    with zipfile.ZipFile(word_original) as wz_, zipfile.ZipFile(prep_) as pz_, zipfile.ZipFile(zo_, 'w', zipfile.ZIP_STORED) as oz_:
        for k_, nm_ in origs:
            src_ = pz_ if nm_.lower().endswith(drawings.VECTOR) else wz_
            try: data_ = src_.read('word/media/' + nm_)
            except KeyError: continue
            ext_ = '.png' if nm_.lower().endswith(drawings.VECTOR) else os.path.splitext(nm_)[1].lower()
            oz_.writestr(k_ + ext_, data_)
    report.append(('originals', 'unblurred originals, numbered as on the page', '%s (%d photos)' % (zo_, len(origs))))
    # 8 text check
    words = lambda x: re.sub(r'\s+', ' ', x).split()
    wtxt = ' '.join(p.text for p in d.paragraphs[1:]).replace('\u00a0', ' ')   # the first line is the title, shown in the hero
    for o_, n_ in S.get('TEXT_EDITS', []): wtxt = wtxt.replace(o_, n_)   # 22 Oct 2026: wording the user changed is not a difference from Word
    for tb in d.tables:
        for row in tb.rows:
            for c in row.cells: wtxt += ' ' + c.text
    cs = BeautifulSoup(content.replace('\u2409', ' '), 'html.parser')
    for br in cs.find_all('br'): br.replace_with(' ')
    for pb in cs.select('a.pdf, .meta'): pb.insert_before(' ')
    # 20 Oct (5.3): every piece of text, in order, a space between blocks - a line holding a list or a paragraph of its own
    # ("Restores the environment:" with its inner list) was left out when only blocks with nothing inside them were read
    BL = ('p', 'li', 'h2', 'h3', 'div', 'cite', 'figcaption', 'ul', 'ol', 'blockquote', 'section')
    bits, lastb = [], None
    for node in cs.find_all(string=True):
        if node.parent.name in ('script', 'style'): continue
        b_ = node.find_parent(BL)
        if b_ is not lastb: bits.append(' '); lastb = b_
        bits.append(str(node))
    ptxt = ''.join(bits)
    A, B = words(wtxt), words(ptxt)
    diffs = [(op, ' '.join(A[i1:i2]), ' '.join(B[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes() if op != 'equal']
    rep = {'report': report, 'text_differences_word_vs_page': diffs, 'preview': pv, 'hostinger': hs, 'zip': z}
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1, ensure_ascii=False)
    for r_ in report: print(' - '.join(x for x in r_ if x))
    print('TEXT DIFFERENCES (Word -> page):', len(diffs))
    for x in diffs: print('  ', x)
    print('preview:', pv); print('zip:', z)

if __name__ == '__main__':
    main()
