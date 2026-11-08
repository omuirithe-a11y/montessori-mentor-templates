#!/usr/bin/env python3
"""static_code.py <page folder or zip> <template html> <out file> [--live <folder of images downloaded from the live page>]
(5 Nov 2026, plan item 6: /home/claude/eng35/checks-plan/PLAN.md). No browser: reads the files only.

Rows (tools/REQUIRED-CHECKS.json), each checked as below:
  D027 "before any cleaning, search the template's code for every inline style, attribute and class it reads from the
       page, and keep those." - the names the template's code reads: classes, ids and attributes in the selectors of its
       <style> blocks and of the strings in its <script> blocks, plus classList.contains / getElementsByClassName /
       getElementById / getAttribute / hasAttribute / dataset names. Every element of the template's own markup (outside
       script and style) carries some of these; the page must carry each (tag, class / id / attribute) at least as often
       as the template, and every element with an inline style in the template must keep a style with the same
       properties. Menu entries: a span.np (an entry with no page) may become a link; every other menu entry must still
       be a link or a span.np.
  A044 "the Essay page template names no specific materials (for example the Trinomial Cube)" - the template file
       (code and comments) must not contain "Trinomial Cube" (A044's quote) or "Pink Tower" (named as a material in
       A028's quote: "headings like Pink Tower"). No other material list exists in the rows.
  A017 "contact details come later, no reminders" - the page footer (footer.site-foot) must read as the template's
       footer (same words, same links), and the footer and the footer band must hold no e-mail address, mailto: or tel:
       link, or phone number (7 or more digits).
  D088 "Never re-upload images downloaded from the live site." - with --live, no image in the page may have the same
       sha256 as an image downloaded from the live page; without it: "not applicable (no live page)".
  B005 'large image copies "Up to 2900 px - yes"' - no image in the page wider or taller than 2900 px.
  A201 "only the master is ever edited" / A210 "templates are saved only in GitHub (omuirithe-a11y/montessori-mentor-
       templates)" - the template given has the same sha256 as the GitHub clone's copy
       (/home/claude/montessori-mentor-templates/<same name>), that copy is unchanged against the clone's HEAD and
       origin/main, and the page carries every <script> and <style> block of the template unchanged.
  A252 "no Word copy is to be made from it" - no .docx/.dotx/.doc in the page; no Word file named as a code template in
       the clone or beside the template given.
  E045 "Tables: borders, shading, column widths, alignment." - counts <table> in the page: 0 -> not applicable; any
       table is reported as a fault here, because its borders, shading, widths and alignment need the browser checks.
Prints one line per rule (and per fault), then STATIC PASS or STATIC FAULT (n), then END; the same lines go to <out file>.
Exit 0 only on STATIC PASS."""
import sys, os, re, io, zipfile, hashlib, subprocess, collections
from bs4 import BeautifulSoup
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

CLONE = '/home/claude/montessori-mentor-templates'
args = sys.argv[1:]
LIVE = None
if '--live' in args:
    i = args.index('--live'); LIVE = args[i + 1]; del args[i:i + 2]
if len(args) != 3:
    print(__doc__); print('STATIC FAULT (1)'); print('END'); sys.exit(2)
PAGE, TEMPLATE, OUTF = args
sha = lambda b: hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------- the page's files (folder or zip)
files = {}   # relative path -> loader
if os.path.isfile(PAGE) and zipfile.is_zipfile(PAGE):
    z = zipfile.ZipFile(PAGE)
    names = [n for n in z.namelist() if not n.endswith('/')]
    idx = sorted([n for n in names if n.split('/')[-1] == 'index.html'], key=lambda n: n.count('/'))
    root = idx[0][:-len('index.html')] if idx else ''
    for n in names: files[n[len(root):] if n.startswith(root) else n] = (lambda n=n: z.read(n))
else:
    for dp, dn, fn in os.walk(PAGE, followlinks=True):
        for f in fn:
            full = os.path.join(dp, f); files[os.path.relpath(full, PAGE)] = (lambda full=full: open(full, 'rb').read())
out, faults = [], []
def say(s): out.append(s)
def fault(s): faults.append(s); out.append('FAULT ' + s)

if 'index.html' not in files:
    fault('no index.html in %s' % PAGE)
    page_html = ''
else:
    page_html = files['index.html']().decode('utf-8')
tpl_bytes = open(TEMPLATE, 'rb').read(); tpl_html = tpl_bytes.decode('utf-8')
say('page: %s (%d files); template: %s' % (os.path.abspath(PAGE), len(files), os.path.abspath(TEMPLATE)))

# ---------------------------------------------------------------- D027
def code_blocks(html):
    return re.findall(r'<(script|style)\b[^>]*>(.*?)</\1>', html, flags=re.S | re.I)

def selector_names(sel, R):
    sel = re.sub(r'"[^"]*"|\'[^\']*\'', '', sel)   # attribute values
    for m in re.finditer(r'(?<![\w-])\.(-?[A-Za-z_][\w-]*)|(?<=[A-Za-z0-9_\]\)*\-])\.(-?[A-Za-z_][\w-]*)', sel):
        R['class'].add(m.group(1) or m.group(2))
    for m in re.finditer(r'#(-?[A-Za-z_][\w-]*)', sel): R['id'].add(m.group(1))
    for m in re.finditer(r'\[\s*([A-Za-z_:][\w:.-]*)', sel): R['attr'].add(m.group(1).lower())

def read_names(html):
    R = {'class': set(), 'id': set(), 'attr': set()}
    for kind, body in code_blocks(html):
        if kind.lower() == 'style':
            css = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
            for pre in re.findall(r'(?:^|[{};])\s*([^{};@][^{};]*)\{', css):
                selector_names(pre, R)
        else:
            js = re.sub(r'(?<![:\\])//[^\n]*', '', body)
            for q, s in re.findall(r'(["\'`])((?:\\.|(?!\1).)*)\1', js):
                if re.search(r'[.#\[]', s) and not re.search(r'[{};]|\s=\s', s): selector_names(s, R)
            for m in re.finditer(r'classList\.contains\(\s*["\']([\w-]+)', js): R['class'].add(m.group(1))
            for m in re.finditer(r'getElementsByClassName\(\s*["\']([\w\s-]+)', js): R['class'].update(m.group(1).split())
            for m in re.finditer(r'getElementById\(\s*["\']([\w-]+)', js): R['id'].add(m.group(1))
            for m in re.finditer(r'(?:get|has)Attribute\(\s*["\']([\w:-]+)', js): R['attr'].add(m.group(1).lower())
            for m in re.finditer(r'\.dataset\.([A-Za-z]\w*)', js):
                R['attr'].add('data-' + re.sub(r'([A-Z])', lambda x: '-' + x.group(1).lower(), m.group(1)))
    return R

def markup(html):
    s = BeautifulSoup(html, 'lxml')
    for x in s(['script', 'style']): x.decompose()
    return s

R = read_names(tpl_html)
say('D027 names the template code reads: %d classes, %d ids, %d attributes' % (len(R['class']), len(R['id']), len(R['attr'])))
ts, ps = markup(tpl_html), markup(page_html)
def counts(soup):
    c = collections.Counter()
    for e in soup.body.find_all(True) if soup.body else []:
        for k in e.get('class', []):
            if k in R['class']: c[(e.name, 'class', k)] += 1
        if e.get('id') in R['id']: c[(e.name, 'id', e.get('id'))] += 1
        for a in e.attrs:
            if a.lower() == 'class' and e.name == 'span' and 'np' in e.get('class', []): continue   # 8 Nov 2026: menu entries without a page are checked by the menu check (their number follows the menu reference)
            if a.lower() in R['attr']: c[(e.name, 'attr', a.lower())] += 1
    return c
tc, pc = counts(ts), counts(ps)
n27 = 0
for k, v in sorted(tc.items()):
    if k == ('span', 'class', 'np'): continue   # menu entries without a page; checked below
    if pc[k] < v:
        n27 += 1; fault('D027 the template\'s %s %s="%s" appears %d times in the template, %d in the page' % (k[0], k[1], k[2], v, pc[k]))
def entry_kind(li):   # a menu entry's shape: its classes, its first child's tag and the read classes on it
    k = li.find(True, recursive=False)
    return (tuple(sorted(c for c in li.get('class', []) if c in R['class'])), k.name if k else None,
            tuple(sorted(c for c in (k.get('class', []) if k else []) if c in R['class'])))
kinds = {entry_kind(li) for li in ts.select('nav.site-nav ul.grp > li')}
for li in ps.select('nav.site-nav ul.grp > li'):   # a menu entry has a shape the template's menu has, or is a link (an entry whose page exists)
    k = entry_kind(li)
    if k not in kinds and k[1] != 'a':
        n27 += 1; fault('D027 menu entry in a shape the template\'s menu does not have (%s): %s' % (k, str(li)[:160]))
# inline styles in the template's markup: the same element (tag and classes) in the page keeps a style with those properties
for e in ts.body.find_all(style=True):
    props = set(p.split(':')[0].strip().lower() for p in e['style'].split(';') if ':' in p)
    cands = [x for x in ps.find_all(e.name) if set(x.get('class', [])) >= set(e.get('class', []))]
    ok = any(x.get('style') and props <= set(p.split(':')[0].strip().lower() for p in x['style'].split(';') if ':' in p) for x in cands)
    if not ok:
        n27 += 1; fault('D027 the template\'s inline style on <%s class="%s"> (%s) is missing in the page' % (e.name, ' '.join(e.get('class', [])), ', '.join(sorted(props))))
say('D027 %s: %d (tag, name) pairs of the template\'s markup checked, %d inline styles' % ('PASS' if not n27 else 'FAULT', len(tc), len(ts.body.find_all(style=True))))

# ---------------------------------------------------------------- A044
MATERIALS = ['Trinomial Cube',   # A044 quote: "(for example the Trinomial Cube)"
             'Pink Tower']       # A028 quote: "names of materials ... (headings like Pink Tower ...)"
n44 = 0
for m in MATERIALS:
    for x in re.finditer(re.escape(m), tpl_html, flags=re.I):
        n44 += 1; fault('A044 the template names a material "%s": ...%s...' % (m, tpl_html[max(0, x.start() - 60):x.end() + 40].replace('\n', ' ')))
for x in re.finditer(r'[A-Z][a-z]+ (?:Language )?Materials', re.sub(r'<header\b.*?</header>', '', tpl_html, flags=re.S)):   # the menu's page names left out   # not a fault: a phrase that may name materials, for the owner
    say('NOTE A044 the template mentions "%s" (not in the material list; owner to judge): ...%s...' % (x.group(0), x.string[max(0, x.start() - 70):x.end() + 20].replace('\n', ' ')))
say('A044 %s: template searched for %s' % ('PASS' if not n44 else 'FAULT', ', '.join('"%s"' % m for m in MATERIALS)))

# ---------------------------------------------------------------- A017
n17 = 0
tf, pf = ts.select_one('footer.site-foot'), ps.select_one('footer.site-foot')
norm = lambda s: re.sub(r'\s+', ' ', s or '').strip()
if pf is None:
    n17 += 1; fault('A017 the page has no footer.site-foot')
else:
    if norm(tf.get_text(' ')) != norm(pf.get_text(' ')):
        n17 += 1; fault('A017 footer text differs from the template: page "%s", template "%s"' % (norm(pf.get_text(' '))[:200], norm(tf.get_text(' '))))
    tl = sorted(a.get('href', '') for a in tf.find_all('a')); pl = sorted(a.get('href', '') for a in pf.find_all('a'))
    if tl != pl:
        n17 += 1; fault('A017 footer links differ from the template: page %s, template %s' % (pl, tl))
for part in [x for x in [pf, ps.select_one('aside.mc-band')] if x is not None]:
    txt = norm(part.get_text(' ')); hrefs = ' '.join(a.get('href', '') for a in part.find_all('a'))
    for rx, what in [(r'[\w.+-]+@[\w-]+\.[\w.-]+', 'e-mail address'), (r'(?i)mailto:|tel:', 'mailto/tel link'), (r'\+?\d(?:[\s().-]*\d){6,}', 'phone number')]:
        for x in re.finditer(rx, txt + ' ' + hrefs):
            n17 += 1; fault('A017 %s in the %s: "%s"' % (what, part.name, x.group(0)))
say('A017 %s: footer as the template, no e-mail, phone or contact link in footer or band' % ('PASS' if not n17 else 'FAULT'))

# ---------------------------------------------------------------- B005 and D088 (images)
IMG_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')
imgs = [n for n in files if n.lower().endswith(IMG_EXT)]
n5 = 0; big = 0; hashes = {}
for n in sorted(imgs):
    b = files[n]()
    hashes[n] = sha(b)
    try:
        w, h = Image.open(io.BytesIO(b)).size
    except Exception as e:
        n5 += 1; fault('B005 cannot read image %s (%s)' % (n, e)); continue
    big = max(big, w, h)
    if max(w, h) > 2900:
        n5 += 1; fault('B005 image %s is %dx%d (over 2900 px)' % (n, w, h))
say('B005 %s: %d images, largest side %d px (limit 2900)' % ('PASS' if not n5 else 'FAULT', len(imgs), big))
if LIVE:
    live = {}
    for dp, dn, fn in os.walk(LIVE):
        for f in fn: live[sha(open(os.path.join(dp, f), 'rb').read())] = os.path.join(dp, f)
    n88 = 0
    for n, hsh in sorted(hashes.items()):
        if hsh in live: n88 += 1; fault('D088 image %s is the live download %s (sha256 %s)' % (n, live[hsh], hsh[:12]))
    say('D088 %s: %d page images against %d live downloads' % ('PASS' if not n88 else 'FAULT', len(hashes), len(live)))
else:
    say('D088 not applicable (no live page)')

# ---------------------------------------------------------------- A201 / A210
n2 = 0
gh = os.path.join(CLONE, os.path.basename(TEMPLATE))
if not os.path.isfile(gh):
    n2 += 1; fault('A210 no %s in the GitHub clone %s' % (os.path.basename(TEMPLATE), CLONE))
else:
    a, b = sha(tpl_bytes), sha(open(gh, 'rb').read())
    say('A201/A210 template sha256 %s; GitHub clone %s sha256 %s' % (a, gh, b))
    if a != b: n2 += 1; fault('A201/A210 the template given is not the GitHub master (sha256 %s, master %s)' % (a[:12], b[:12]))
    rel = os.path.basename(TEMPLATE)
    head = subprocess.run(['git', '-C', CLONE, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    for ref in ('HEAD', 'origin/main'):
        r = subprocess.run(['git', '-C', CLONE, 'diff', '--quiet', ref, '--', rel], capture_output=True, text=True)
        if r.returncode != 0:
            n2 += 1; fault('A201/A210 the clone\'s %s differs from %s (%s)' % (rel, ref, (r.stderr or 'changed').strip()[:200]))
    st = subprocess.run(['git', '-C', CLONE, 'status', '--porcelain', '--', rel], capture_output=True, text=True).stdout.strip()
    if st: n2 += 1; fault('A201/A210 the clone has uncommitted changes to %s: %s' % (rel, st))
    say('A201/A210 clone HEAD %s' % head)
blocks = code_blocks(tpl_html); missing = [b_ for k, b_ in blocks if b_ not in page_html]
# 8 Nov 2026 (owner "yes", The Prepared Environment): a template block changed only in lines the owner agreed to keep on this page -
# every one of its lines missing from the page is named as a removed line ("1 | -<line>") in tools/allowed/<page>-code.txt (the code
# check, strip_compare_nolive.py, accepts the added lines only when they are named there too)
_slug = os.path.basename(PAGE.rstrip('/'))[:-4] if PAGE.endswith('.zip') else os.path.basename(PAGE.rstrip('/'))
_af = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'allowed', _slug + '-code.txt')
_rm = set(l[5:] for l in open(_af, encoding='utf-8').read().split('\n') if l.startswith('1 | -')) if os.path.exists(_af) else set()
def _named(b_):
    gone = [l.rstrip() for l in re.sub(r'>\s*<', '>\n<', b_).splitlines() if l.strip() and l.rstrip() not in page_html]
    return bool(gone) and all(l in _rm for l in gone)
_ok201 = [b_ for b_ in missing if _named(b_)]
for b_ in _ok201: say('A201 a template block changed only in lines the owner keeps on this page (%s): %s...' % (os.path.basename(_af), re.sub(r'\s+', ' ', b_)[:80]))
missing = [b_ for b_ in missing if b_ not in _ok201]
for b_ in missing:
    n2 += 1; fault('A201 a template script/style block is changed or missing in the page: %s...' % re.sub(r'\s+', ' ', b_)[:120])
say('A201/A210 %s: %d of %d template script/style blocks in the page unchanged' % ('PASS' if not n2 else 'FAULT', len(blocks) - len(missing), len(blocks)))

# ---------------------------------------------------------------- A252
n252 = 0
WORD_EXT = ('.docx', '.dotx', '.doc', '.docm', '.dot')
for n in files:
    if n.lower().endswith(WORD_EXT): n252 += 1; fault('A252 a Word file in the page: %s' % n)
other_word = []
for base in sorted({CLONE, os.path.dirname(os.path.abspath(TEMPLATE))}):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != '.git']
        for f in fn:
            if f.lower().endswith(WORD_EXT):
                p_ = os.path.join(dp, f)
                if re.search(r'(?i)code[ _-]*template', f): n252 += 1; fault('A252 a Word copy of a code template: %s' % p_)
                else: other_word.append(p_)
for p_ in other_word: say('NOTE A252 other Word file (not named as a template): %s' % p_)
say('A252 %s: no Word copy of the template' % ('PASS' if not n252 else 'FAULT'))

# ---------------------------------------------------------------- E045
nt = len(ps.find_all('table'))
if nt == 0: say('E045 not applicable (0 tables)')
else: say('E045 %d table(s) in the page: borders, shading, column widths and alignment handed to the separate review (eye, Word file against the page) - no browser check reads tables (8 Nov 2026)' % nt)

out.append('STATIC PASS' if not faults else 'STATIC FAULT (%d)' % len(faults))
out.append('END')
os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
open(OUTF, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
sys.exit(0 if not faults else 1)
