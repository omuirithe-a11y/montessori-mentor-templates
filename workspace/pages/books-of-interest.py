# 8.2 Books of Interest - page settings (3 Nov 2026, Resources Code Template cf017c93 = 38fd0f9b + the owner's 12:45 agreement, mm-res-3nov-a)
# Word file: 8.2 Books - Education, Parenting, Child Development.docx (Drive, saved 3 Nov 11:44, 79,289,498 bytes); PDF of the same time.
# Made from 8.4 Websites' settings (pages/websites.py), which were made from 8.3's. Owner's decisions (claude/DECISIONS-LOG-3-nov.md):
# 09:12 all book titles in italics; 10:21 title "Books of Interest"; 11:45 (2) MWEI heading as built (red h2), (3) Required and
# Recommended Reading side by side on computers, one under the other on phones (template mm-pair, 12:45), (5) DVD and magazine titles
# italic, (6) "organizations" keeps its spelling; 12:35 (2A) the contents entry "AMI Trainers Reading Recommendations" jumps to the
# paragraph "After I registered for the AMI training..." with no heading. Faults: claude/checks/books-of-interest-b1-faults.md (81).
import re, os, sys, runpy

_H = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books-by-montessori.py'))
_runs, _pieces_html, _esc, _res_item = _H['_runs'], _H['_pieces_html'], _H['_esc'], _H['_res_item']
BLUES, REDS = _H['BLUES'], _H['REDS']
GREENS = ('00B050',)

# Word and the PDF have a contents list (Word paragraphs 0-11, ending with a line picture): the template's own contents box
# ("Table of contents", owner preference) lists the green headings; Word's copy of the list is not repeated in the text.
TOC_END = 11
TOC_SPLIT = [3, 3]   # the PDF's contents list: two columns of three (as 8.4, owner 2 Nov 16:22 "match the layout of the PDF")
TOC_EXTRA = [(0, 'ami-trainers-reading-recommendations', 'AMI Trainers Reading Recommendations')]   # owner 3 Nov 12:35 (2A): no heading; the entry jumps to the introduction
MWEI_PARA = 78   # "The Montessori World Educational Institute" (red in Word)
AMI_PARA = 12    # "After I registered for the AMI training..." (the contents entry's target, owner 12:35 2A)
PAIR_LABELS = (15, 27)   # "Required Reading", "Recommended Reading" (owner 11:45 (3), template agreement 12:45)
PAIR_END = 35            # the last line of the second list
# typos (owner 27 Oct: correct all typos; build 1 fault list D 13-43), applied to Word's text before the page is made
TYPOS = [('and this is the list the training center’s 2026 list', 'and this is the training center’s 2026 list'), 
         ('changing the bible', 'changing the Bible'), ('Making sense of Preschoolers', 'Making Sense of Preschoolers'),
         ('Punished by Rewards The Trouble', 'Punished by Rewards: The Trouble'), ('from our trainers. –', 'from our trainers –'),
         ('deeply  and', 'deeply and'), ('weight of  social', 'weight of social'), ('A guide to  implementation', 'A guide to implementation'),
         ('guide them- or', 'guide them – or'), ('Piaget, by Nathan Isaacs.', 'Piaget, by Nathan Isaacs'), ('by John Holt;', 'by John Holt'),
         ('Jane Nelson', 'Jane Nelsen'), ('(Parents Guide to)', '(Parents’ Guide to)'), ('Notes From A School Teacher', 'Notes from a Schoolteacher'),
         ('Observing And Recording', 'Observing and Recording'), ('On The Subject of', 'On the Subject of'),
         ('Children Who Are Not Peaceful: Preventing Exclusion in an Elementary class', 'Children Who Are Not Yet Peaceful: Preventing Exclusion in the Early Elementary Classroom'),
         ('Children Who are Not Yet Peaceful', 'Children Who Are Not Yet Peaceful'),
         ("A Parents' Guide to the Montessori Classroom, Aline D. Wolf", "A Parent's Guide to the Montessori Classroom, Aline D. Wolf"),
         ('The Essential Montessori. Elizabeth G. Hainstock.', 'The Essential Montessori, Elizabeth G. Hainstock'), ('Trevor Eisler', 'Trevor Eissler'), ('Eisler’s book', 'Eissler’s book'),
         ('How to Raise An Amazing Child the Montessori Way', 'How to Raise an Amazing Child the Montessori Way'),
         ('How to raise an Amazing Child, the Montessori way', 'How to Raise an Amazing Child the Montessori Way'),
         ('Can Succeed. Jessica Lahey', 'Can Succeed, Jessica Lahey'), ('Compassionate Teaching. Catherine McTamaney', 'Compassionate Teaching, Catherine McTamaney'),
         ('Montessori Life ,', 'Montessori Life,'), ('Preparation for Life:  Montessori Infant-Toddler Communities"', 'Preparation for Life: Montessori Infant-Toddler Communities”'),
         ('Montessori Today, A Comprehensive Approach', 'Montessori Today: A Comprehensive Approach'), ('dual-career couples. Is a Montessori', 'dual-career couples: Is a Montessori'),
         ('Angelline S. Lillard', 'Angeline S. Lillard'), ('Lesley Brittan', 'Lesley Britton'),
         ('How to talk so Kids Will Listen and Listen so Kids will Talk', 'How to Talk So Kids Will Listen and Listen So Kids Will Talk'),
         ('Growing up with 2 languages, Una Cunninham & Staffan Anderssen', 'Growing Up with Two Languages, Una Cunningham-Andersson & Staffan Andersson'),
         ('The Child in The Family', 'The Child in the Family'), ('anyone -- educator', 'anyone – educator'), ('parent -- seeking', 'parent – seeking'),
         ('from  2 Voices', 'from 2 Voices'), ('Punished By Rewards: The Trouble With Gold Stars', 'Punished by Rewards: The Trouble with Gold Stars'), ('for Primary Classes, \tJoanne', 'for Primary Classes, Joanne'),   # b5 review 3: one space, as the PDF
        
         ('Montessori From the Start, Paula', 'Montessori from the Start, Paula'), ('On Learning To Read', 'On Learning to Read'), ('Preschoolers At Risk', 'Preschoolers at Risk')]
# owner 26 Oct 15:57: published titles and words inside a quotation keep their spelling (fault list C 8-10); owner 3 Nov 11:45 (6): "organizations" American
KEEP_SPELLING = ['The Art of Normalization', 'this essential program', 'education, programs, and research', 'Montessori organizations']   # the rule looks 20 letters back, so the phrase is kept short
NO_END_STOP = list(range(121, 132)) + list(range(162, 173))   # fault list D 26: these lists end their lines with a full stop, the others do not
TAB_COMMA = [138]   # "The Montessori Way<tab>Tim Seldin" (fault 27)
CLOSE_QUOTE = [275]
ROW_CONTINUES = [133]   # Word anchors row 3's images in two paragraphs (132: image9, image10; 133: image11, image12) - one row (8.2 b3: row 4 was placed here)
LINE_BEFORE_TEXT = [134, 214]   # a line picture in the heading's own paragraph stands ABOVE its text, as the PDF draws it (8.4's rule puts it after)
RED_AS_TEXT = [214, 252, 269]   # b4 review 6: the red 'following list' lines are lines of text (red), not entry names, so their lists are spaced as the other lists
BOLD_LINES = [15, 27, 81, 88, 92, 97, 102, 106, 109, 112, 115]   # b4 review 11: bold in Word and the PDF
GAP_LINES = [81, 88, 92, 97, 102, 106, 109, 112, 115]   # b4 review 12: the MWEI category lines have a blank line above them in the PDF
SHOWN_SIZE = {'image2.jpg': 960}   # fault 73: the 4096x1152 panorama shown up to 602 px wide; its shown copy 960 on the long side   # the Mahoning Valley quotation opens and never closes (fault 37)
ITALIC_TITLES = {45: 'Rest, Play, Grow: Making Sense of Preschoolers',
    48: 'Punished by Rewards: The Trouble with Gold Stars, Incentive Plans, A’s, Praise and Other Bribes',
    51: 'Sapiens: A Brief History of Humankind',
    54: 'Human Instinct',
    57: 'The Gardener and the Carpenter',
    60: 'Humankind: A Hopeful History',
    63: 'The Ascent of Man',
    66: 'Up the Down Staircase',
    82: 'A Brief Introduction to Piaget',
    83: 'Guiding Young Children',
    84: 'How Children Learn',
    85: 'On Learning to Read',
    86: "Your Child's Growing Mind",
    89: 'Positive Discipline',
    90: 'Understanding Discipline',
    93: 'Among Schoolchildren',
    94: 'Notes from a Schoolteacher',
    95: 'Teacher',
    98: 'Helping Parents Help Their Children',
    99: 'Miseducation: Preschoolers at Risk',
    103: 'A Good Enough Parent',
    104: 'Families: Crisis and Caring',
    107: 'Raising Self-Reliant Children in a Self-Indulgent World',
    110: 'Feed Your Kids Right',
    113: 'Observational Strategies for Child Study',
    116: "A Parent's Guide to the Montessori Classroom",
    117: 'Montessori and Your Child: A Primer for Parents',
    121: '8 Characteristics of the Master Teacher',
    122: 'I Wonder What’s Out There: A Vision of the Universe for Primary Classes',
    123: 'Developing Minds: A Resource Book for Teaching Thinking',
    124: 'Habits of Mind Across the Curriculum: Practical Strategies for Teachers',
    125: 'Montessori Math and the Developing Brain',
    126: 'Nurturing the Young Scientist: Experiences in Physics for Children',
    127: 'The Pink What? A Curriculum Guide',
    128: 'Children Who Are Not Yet Peaceful: Preventing Exclusion in the Early Elementary Classroom',
    129: 'The Tao of Montessori',
    130: 'The Teaching Gap',
    131: 'Punished by Rewards: The Trouble with Gold Stars',
    135: 'Maria Montessori: Her Life and Work',
    137: 'Maria Montessori: A Biography',
    138: 'The Montessori Way',
    139: "A Parent's Guide to the Montessori Classroom",
    141: 'The Essential Montessori',
    142: 'The Montessori Controversy',
    143: 'Montessori: The Science Behind the Genius',
    144: 'Montessori Today',
    145: 'Montessori: A Modern Approach',
    147: 'Basic Montessori',
    148: 'Basic Montessori',
    149: 'Montessori and Early Childhood Education',
    150: 'Montessori Madness',
    151: 'Montessori Learning in the 21st Century: A Guide for Parents & Teachers',
    152: 'Montessori and Your Child: A Primer for Parents',
    162: 'How to Raise an Amazing Child the Montessori Way',
    163: 'Montessori from the Start: The Child at Home, from Birth to Age Three',
    164: 'Montessori Madness! A Parent to Parent Argument for Montessori Education',
    165: 'The Montessori Toddler',
    166: 'Montessori Play and Learn: A Parent’s Guide to Purposeful Play',
    167: 'Teaching Montessori in the Home: The Pre-school Years',
    168: 'Montessori in the Home: The School Years',
    169: 'Montessori Parenting: Unveiling the Authentic Self',
    170: "Child's Play: Montessori Games and Activities for Your Baby",
    171: 'Understanding Montessori: A Guide for Parents',
    172: 'Last Child in the Woods',
    176: 'The Self-Driven Child: The Science and Sense of Giving Your Kids More Control Over Their Lives',
    177: 'Simplicity Parenting: Using the Extraordinary Power of Less to Raise Calmer, Happier, and More Secure Kids',
    178: 'Raising Kids: Your Essential Guide to Everyday Parenting',
    179: 'The Enchanted Hour: The Miraculous Power of Reading Aloud in the Age of Distraction',
    180: 'The Gift of Failure: How the Best Parents Learn to Let Go So Their Children Can Succeed',
    181: 'The Anxious Generation: How the Great Rewiring of Childhood Is Causing an Epidemic of Mental Illness',
    182: 'The Art of Happiness in a Troubled World',
    188: 'The Self-Driven Child:\xa0The Science and Sense of Giving Your Kids More Control Over Their Lives',
    189: 'Simplicity Parenting:\xa0Using the Extraordinary Power of Less to Raise Calmer, Happier, and More Secure Kids',
    190: 'Raising Kids: Your Essential Guide to Everyday Parenting',
    191: 'The Enchanted Hour: The Miraculous Power of Reading Aloud in the Age of Distraction',
    192: 'The Gift of Failure',
    193: 'The Anxious Generation',
    194: 'The Art of Happiness',
    197: 'Montessori from the Start: The Child at Home, from Birth to Age Three',
    198: 'Montessori: A Modern Approach',
    199: 'Montessori Today: A Comprehensive Approach to Education from Birth to Adulthood',
    200: 'Montessori: The Science Behind the Genius',
    201: 'The Montessori Potential: How to Foster Independence, Respect, and Joy in Every Child',
    205: "Montessori in the Classroom: A Teacher's Account of How Children Really Learn",
    206: 'Montessori: Why It Matters for Your Child’s Success and Happiness',
    207: "The Montessori Toddler: A Parent's Guide to Raising a Curious and Responsible Human Being",
    215: 'At Home with Montessori',
    216: 'Children Who Are Not Yet Peaceful',
    217: 'Classroom Management: The Art of Normalization',
    218: 'Maria Montessori and the Social Party of the Child',
    219: 'In a Montessori Home',   # b5 review 4: '(book and DVD)' upright, as the PDF
    220: 'Let Out the Sunshine',
    221: 'Maria Montessori: Her Life and Work',
    222: 'Understanding the Human Being',
    223: 'Nurturing the Spirit',
    224: '100 Child Development Tips',
    225: 'The Outdoor Classroom',
    226: 'Tao of Montessori: Reflections on Compassionate Teaching',
    227: 'Tending the Light',
    228: 'Montessori Play and Learn',
    238: 'Montessori International',
    239: 'Montessori Life',
    240: 'Tomorrow’s Child',
    243: 'Following Your Child: A Montessori Philosophy of Parenting',
    244: 'Preparation for Life: Montessori Infant-Toddler Communities',
    245: 'Montessori for the Early Childhood Years',
    246: 'Imagine a School: Montessori for Elementary Age Children',
    247: 'Montessori Middle School for the 21st Century',
    248: 'Educating for Peace: The Essence of Montessori',
    254: 'Montessori Today: A Comprehensive Approach to Education from Birth to Adulthood',
    255: 'Montessori: The Science Behind the Genius',
    256: 'Montessori Madness!',
    257: 'A Parent’s Guide to the Montessori Classroom',
    258: 'To Educate the Human Potential',
    259: 'The Absorbent Mind',
    261: 'Montessori from the Start',
    262: 'Living Simply with Children',
    263: 'Endangered Minds',
    264: 'Punished by Rewards',
    265: 'Emotional Intelligence',
    266: 'Siblings Without Rivalry',
    267: 'Between Parent and Child',
    277: 'Montessori: A Modern Approach',
    280: 'Montessori Madness',
    282: 'Montessori: Science Behind the Genius',
    285: 'Montessori from the Start: The Child at Home from Birth to Age Three',
    288: 'How to Raise an Amazing Child the Montessori Way',
    291: 'Montessori Parenting: Unveiling the Authentic Self',
    298: 'Montessori Madness',
    299: 'Understanding the Human Being',
    300: 'How to Raise an Amazing Child the Montessori Way',
    301: 'Montessori Play and Learn',
    302: 'Montessori Read and Write',
    303: 'How to Talk So Kids Will Listen and Listen So Kids Will Talk',
    304: 'Raising Boys',
    305: 'Endangered Minds',
    306: 'Toxic Childhood',
    307: 'Detoxing Childhood',
    308: '21st Century Boys',
    309: 'Growing Up with Two Languages',
    310: 'The Joyful Child',
    311: 'Child of the World',
    312: 'The Secret of Childhood',
    313: 'The Child in the Family'}


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
        pcs = _fix(i, _runs(p, qn), report)
        txt = ''.join(x[0] for x in pcs).strip()
        lines, photos = kind_of_images(p)
        num = p._p.find('.//' + qn('w:numPr')) is not None
        if in_list and not num:
            add('<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in in_list)); in_list = []
        if photos:
            if txt and photos == 1 and fi < len(floats):   # an image beside its paragraph (Word anchors it there)
                add(str(floats[fi])); report.append(('settings', 'image beside text %d placed at Word paragraph %d' % (fi + 1, i), '')); fi += 1
            elif i in ROW_CONTINUES:
                pass   # the rest of the row placed at the paragraph before
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
        if lines and not photos:
            if i in LINE_BEFORE_TEXT: close(); out.append('<div class="beige-rule mm-org-rule"></div>')
            else: pending_rule = True
        if num:
            in_list.append(_pieces_html(pcs).replace('<span class="mm-blue">', '').replace('</span>', '')); continue
        green, red, blue = _share(pcs, GREENS), _share(pcs, REDS), _share(pcs, BLUES)
        first = next((x for x in pcs if x[0].strip()), None)
        if green > 0.6:
            close()
            out.append('<h2 class="mm-hc-00B050">%s</h2>' % _strip_col(_pieces_html(pcs))); continue   # spacing above: the template (owner 2 Nov 16:08 "On all pages and in the template")
        if i == MWEI_PARA:   # owner 3 Nov 11:45 (2) "as built": the red heading the converter made (h2, red), one of the contents sections
            close(); out.append('<h2 class="mm-hc-EE0000">%s</h2>' % _strip_col(_pieces_html(pcs))); continue
        if i == AMI_PARA:   # owner 3 Nov 12:35 (2A): the contents entry jumps to this paragraph; no heading
            close(); out.append('<p id="ami-trainers-reading-recommendations">%s</p>' % _tabbed(pcs)); continue
        if i in PAIR_LABELS:   # owner 11:45 (3) and 12:45: Required / Recommended Reading side by side (template div.mm-pair)
            close(); out.append('<!--pair-%d-->' % PAIR_LABELS.index(i)); out.append('<p><strong>%s</strong></p>' % _pieces_html(pcs)); continue
        if i in BOLD_LINES:
            close(); out.append('<p%s><strong>%s</strong></p>' % (' data-gap="51"' if i in GAP_LINES else '', _pieces_html(pcs))); continue
        if i in RED_AS_TEXT:
            close(); out.append('<p>%s</p>' % _pieces_html(pcs)); continue
        if PAIR_LABELS[0] < i <= PAIR_END:
            out.append('<p>%s</p>' % _pieces_html(pcs))
            if i == PAIR_END: out.append('<!--pair-end-->')
            continue
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
    _html = ''.join(out)
    _html, _k = re.subn(r'<!--pair-0-->(.*?)<!--pair-1-->(.*?)<!--pair-end-->', r'<div class="mm-pair"><div>\1</div><div>\2</div></div>', _html, flags=re.S)
    assert _k == 1, 'pair'
    _html = re.sub(r'<a ([^>]*?)href="([^"]*)#mmred"([^>]*)>(.*?)</a>', r'<a \1href="\2"\3><span class="mm-hc-EE0000">\4</span></a>', _html, flags=re.S)
    for _t in [ITALIC_TITLES[k] for k in range(243, 249)]:   # b4 review 10: the DVD titles are links; the link text in italics, inside its quotation marks
        _k = _html.count('>“%s”</a>' % _t) + _html.count('>“%s</a>' % _t)
        _html = _html.replace('>“%s' % _t, '>“<em>%s</em>' % _t)
        assert _k == 1, ('DVD title', _t, _k)
    # owner 3 Nov 14:27 (question 4, the one-line previews: "right"): a Discussion Guide link never breaks across two lines; it moves whole to the next line (template class mm-keep)
    _n = len(re.findall(r'<a ([^>]*)>((?:Abridged )?Discussion Guide PDF)</a>', _html))
    _html = re.sub(r'<a ([^>]*)>((?:Abridged )?Discussion Guide PDF)</a>', r'<a class="mm-keep" \1>\2</a>', _html)
    assert _n == 5, ('Discussion Guide links', _n)
    # owner 15:02 (template agreement): the entries holding those links are set flush left (template class mm-left), so a moved link leaves no spread line
    _parts = re.split(r'(<p>(?:(?!</p>).)*?class="mm-keep".*?</p>)', _html, flags=re.S)
    _k = sum(1 for x in _parts if x.startswith('<p>') and 'class="mm-keep"' in x)
    _html = ''.join(('<p class="mm-left">' + x[3:]) if (x.startswith('<p>') and 'class="mm-keep"' in x) else x for x in _parts)
    assert _k == 4, ('Discussion Guide entries', _k)
    report.append(('settings', 'Required and Recommended Reading as a pair, side by side on computers (owner 11:45, template 12:45)', ''))
    main.append(BeautifulSoup('<section class="section">%s</section>' % _html, 'html.parser'))

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
    report.append(('settings', 'text area rebuilt from Word in the template\'s entry style (as 8.1 and Culture Resources): %d entries' % len(main.select('div.res-entry')), ''))


def _fix(i, pcs, report):
    """8.2: the Word text of paragraph i with the typos corrected and the book titles in italics, letter by letter (each letter keeps
    its Word colour, link and superscript; a corrected letter takes the attributes of the first letter it replaces)."""
    ch = []
    for t, col, it, href, sup in pcs:
        for c in t: ch.append([c.replace('\xa0', ' ') if c == '\xa0' else c, col, it, href, sup])
    def text(): return ''.join(x[0] for x in ch)
    import difflib
    for old, new in TYPOS:
        k = text().find(old)
        while k >= 0:
            seg = ch[k:k + len(old)]; rep_ = []
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
                if tag == 'equal': rep_ += [list(x) for x in seg[i1:i2]]
                elif j2 > j1:
                    src = seg[i1] if i1 < len(seg) else seg[-1]
                    rep_ += [[c] + src[1:] for c in new[j1:j2]]
            ch[k:k + len(old)] = rep_
            report.append(('settings', 'typo corrected (owner 27 Oct: all typos)', '%s -> %s' % (old, new)))
            k = text().find(old, k + len(new))
    if i in TAB_COMMA:
        for x in ch:
            if x[0] == '\t': x[0] = ', '; break
        report.append(('settings', 'comma before the author (fault 27)', text()[:40]))
    if i in NO_END_STOP:
        while ch and ch[-1][0] in ' .': ch.pop()
    if i in CLOSE_QUOTE and not text().rstrip().endswith('”'):
        while ch and ch[-1][0] == ' ': ch.pop()
        ch.append(['”'] + ch[-1][1:]); report.append(('settings', 'closing quotation mark added (fault 37)', text()[:40]))
    ti = (ITALIC_TITLES.get(i) or '').replace('\xa0', ' ')
    if ti:
        t = text(); k = t.find(ti)
        if k < 0: raise SystemExit('ITALIC_TITLES %d: "%s" not found in "%s"' % (i, ti, t[:120]))
        prose = i in (148, 238, 239, 240)   # a title inside a sentence: only the title is set italic, the rest keeps Word's
        for j, x in enumerate(ch):
            if k <= j < k + len(ti): x[2] = True
            elif not prose and x[0].strip(): x[2] = False
    for j in range(len(ch) - 1, -1, -1):
        if ch[j][3] and ch[j][0] in ' ,;.:' and (j == len(ch) - 1 or ch[j + 1][3] != ch[j][3]):
            ch[j][3] = None; ch[j][2] = False if ch[j][0] in ',;.:' else ch[j][2]
    out = []
    for c, col, it, href, sup in ch:
        if out and out[-1][1:] == [col, it, href, sup] and c not in '\t\n' and out[-1][0][-1:] not in ('\t', '\n'): out[-1][0] += c
        else: out.append([c, col, it, href, sup])
    for x in out:
        if x[3] and x[1] in REDS: x[3] = x[3] + '#mmred'
    return [tuple(x) for x in out]


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
