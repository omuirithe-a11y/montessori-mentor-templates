#!/usr/bin/env python3
"""Rule checks (21 Oct 2026): the user's rules in tools/rules.json that fault_checks.py and check_page.py do not test.

  python3 tools/rule_checks.py <build folder> [page settings file]        -> prints PASS/FAIL per check, writes rule_checks.json
  python3 tools/rule_checks.py prove <build folder> <settings>            -> each check on a copy with one fault put in

Widths 1440, 1280, 830, 768, 641, 390 (the settled widths plus both sides of the 640 and 830 breakpoints). Each page is
scrolled to the foot and back, fonts awaited, and measured only once two full screenshots in a row are identical; a width
that never settles is a FAIL, not skipped. Gaps are measured from the screenshot's pixels (device scale 2), never by the
page's own scripts. Positions within 0.5px, gaps within 1px, colours exact."""
import sys, os, re, json, io, shutil, tempfile, asyncio, functools, threading, http.server, socketserver, hashlib, zipfile
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); MM = os.path.dirname(HERE)
WIDTHS = [1440, 1280, 830, 768, 641, 390]
TEMPLATE = os.path.join(MM, 'templates', 'Essay Code Template.html')
FACES = '/home/claude/admin/faces'
# blocks a build may add to the template, each with where it was asked for (rule B3)
ADDED_OK = {
    'mm-org-rule-essay': 'user 21 Oct 19:39 (beige lines between Resources entries, 30/30)', 'mm-org-rule-essay-js': 'user 21 Oct 19:39',
    'mm-swipe-middle-js': 'preferences 16 Oct (swipe photos stop in the middle, space at both ends)', 'mm-phone-gaps-js': 'user 21 Oct 13:4x (phones: mean of the live pages)',
    'mm-wrap': 'build: Word list indents and labels (20 Oct)', 'mm-page': 'the page settings CSS (each line names its source)',
    'mm-pdf-column-js': 'user 20 Oct 19:13 (PDF badges in one column)', 'mm-res-live-css': 'user 21 Oct 13:39 (Resources at the live figures)',
    'mm-res-live-js': 'user 21 Oct 13:39', 'mm-org-rule-css': 'user 20 Oct (beige lines 30/30)', 'mm-org-rule-js': 'user 20 Oct',
    'mm-left': 'user 21 Oct (5.4, left-align a line)', 'mm-labphone': 'user 21 Oct 00:1x (5.4)', 'mm-labcol': '20 Oct (5.4)',
    'mm-phone-gaps-js': 'user 20 Oct 22:0x (5.4)', 'mm-centre-on-js': 'user 20 Oct 23:28 (5.4)', 'mm-protect': 'START-HERE rule 13 (Hostinger copy only)',
    'mm-protect-js': 'START-HERE rule 13 (Hostinger copy only)'}
INK = (0x2B, 0x2B, 0x2B)

def serve(folder):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=folder))
    threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv

JS = open(os.path.join(HERE, 'rule_checks.js'), encoding='utf-8').read()

async def settle(pg):
    for _ in range(2):
        h = await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0, h + 900, 700): await pg.evaluate('window.scrollTo(0,%d)' % y); await pg.wait_for_timeout(60)
        await pg.evaluate('window.scrollTo(0,0)')
    await pg.evaluate('document.fonts.ready.then(()=>1)'); await pg.wait_for_timeout(1200)
    h = await pg.evaluate('document.documentElement.scrollHeight')
    await pg.set_viewport_size({'width': pg.viewport_size['width'], 'height': h}); await pg.wait_for_timeout(1800)
    prev = None
    for k in range(10):
        shot = await pg.screenshot(full_page=True)
        if prev is not None and shot == prev: return shot
        prev = shot; await pg.wait_for_timeout(700)
    return None

def pixgap(im, x0, x1, top_y, bot_y):
    """Gap in CSS px between the last ink above y=top_y (searching up) and the first ink at or below bot_y (searching down),
    in the columns x0..x1 (CSS px). Ink = any pixel not the page background and not a beige line."""
    a = np.asarray(im.convert('RGB'), dtype=np.int16); H, W = a.shape[:2]
    c0, c1 = max(0, int(x0 * 2)), min(W, int(x1 * 2))
    band = a[:, c0:c1, :]
    bg = (np.abs(band[:, :, 0] - band[:, :, 1]) < 12) & (band[:, :, 0] > 225) & (band[:, :, 2] > 205)
    inkrow = ~bg.all(axis=1)
    y = int(bot_y * 2)
    while y < H and not inkrow[y]: y += 1
    yb = y; y = int(top_y * 2)
    while y > 0 and not inkrow[y]: y -= 1
    return round((yb - y - 1) / 2, 1)

async def measure(b, base, w, settings, live=False):
    pg = await (await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=2, ignore_https_errors=True, has_touch=(w < 500))).new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:80]))
    await pg.goto(base + ('/' if live else '/index.html'), wait_until='networkidle' if live else 'load', timeout=120000)
    await pg.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i=>i.loading="eager")')
    shot = await settle(pg)
    d = await pg.evaluate(JS, settings)
    d['settled'] = shot is not None; d['errors'] = errs
    d['shot'] = shot
    # hover test (rule M1): hovering a menu name must not open its panel
    if w >= 1024:
        tops = await pg.query_selector_all('#site-nav .top, #site-nav > ul > li > a, #site-nav > ul > li > button')
        hov = []
        for t in tops[:9]:
            try:
                await t.hover(); await pg.wait_for_timeout(250)
                hov.append(await pg.evaluate('[...document.querySelectorAll(".panel")].some(p=>{const r=p.getBoundingClientRect(),c=getComputedStyle(p);return r.height>20&&c.display!=="none"&&c.visibility!=="hidden"&&c.opacity!=="0"})'))
            except Exception: pass
        await pg.mouse.move(1, 1); d['hover_opens'] = any(hov)
    if w < 500 and not live:
        d['swipes'] = []
        rows = await pg.query_selector_all('main .mm-row')
        cdp = await pg.context.new_cdp_session(pg)
        for i, el in enumerate(rows):
            info = await el.evaluate('r=>[r.scrollWidth>r.clientWidth+1, r.querySelectorAll("figure").length]')
            if not info[0] or info[1] < 2: continue
            await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            bb = await el.bounding_box(); y = bb['y'] + bb['height'] / 2; x0, x1 = bb['x'] + bb['width'] * 0.75, bb['x'] + bb['width'] * 0.35
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y}]})
            for k in range(1, 9): await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * k / 8, 'y': y}]}); await pg.wait_for_timeout(16)
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); await pg.wait_for_timeout(1200)
            off = await el.evaluate('r=>{const c=r.getBoundingClientRect(),m=(c.left+c.right)/2;return Math.min(...[...r.querySelectorAll("figure")].map(f=>{const q=f.getBoundingClientRect();return Math.abs((q.left+q.right)/2-m)}))}')
            d['swipes'].append([i + 1, round(off, 1)])
    # keyboard (rule X4): the first Tab lands on the skip link
    await pg.evaluate('window.scrollTo(0,0)'); await pg.keyboard.press('Tab')
    d['first_tab'] = await pg.evaluate('(()=>{const a=document.activeElement;return a?[a.tagName,a.getAttribute("href")||"",a.textContent.trim().slice(0,30)]:null})()')
    await pg.close(); return d

def check(build, settings_path):
    S = {}
    if settings_path:
        import runpy; S = runpy.run_path(settings_path)
    def _te(t):   # the words as the page shows them, after the user's wording changes (TEXT_EDITS)
        for o_, n_ in S.get('TEXT_EDITS', []): t = t.replace(o_, n_)
        return t
    sset = {'labels': S.get('UNDERLINE_LABELS', []), 'links': S.get('LINK_TEXT', []), 'spaceAfter': S.get('SPACE_AFTER', []),
            'spaceAbove': S.get('SPACE_ABOVE', []), 'dividers': {k: list(v) for k, v in S.get('DIVIDER_SPACE', {}).items()},
            'noDivider': S.get('NO_DIVIDER_BEFORE', []), 'noToc': bool(S.get('NO_TOC')),
            'spaceSet': [[_te(x[0])] + list(x[1:]) + [None] * (3 - len(x)) for x in S.get('SPACE_SET', [])], 'headAfter': S.get('HEAD_AFTER', {})}
    pv = os.path.join(build, 'preview'); hs_root = os.path.join(build, 'hostinger')
    hs = os.path.join(hs_root, os.listdir(hs_root)[0]) if os.path.isdir(hs_root) and os.listdir(hs_root) else None
    from playwright.async_api import async_playwright
    async def run():
        srv = serve(pv); base = 'http://127.0.0.1:%d' % srv.server_address[1]; out = {}
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for w in WIDTHS: out[w] = await measure(b, base, w, sset)
            await b.close()
        srv.shutdown(); return out
    M = asyncio.run(run())
    LIVEM = {}
    if (S.get('RES_FROM') or os.environ.get('MM_RESLIVE')) and not os.environ.get('MM_LIVE_CACHE'):   # prove mode reuses the live figures measured by the run before it
        async def runlive():
            out = {}
            async with async_playwright() as p:
                b = await p.chromium.launch(proxy={'server': os.environ['HTTPS_PROXY']} if os.environ.get('HTTPS_PROXY') else None)
                for w in WIDTHS:
                    try: out[w] = await measure(b, 'https://montessorimentor.co.uk/culture-resources', w, sset, live=True)
                    except Exception as e: out[w] = None
                await b.close()
            return out
        LIVEM = asyncio.run(runlive())
    R = {}
    def put(k, faults, n): R[k] = {'ok': not faults, 'faults': faults, 'checked': n}
    # SETTLE: every width settled (a width that never settles fails)
    put('SETTLE', ['%d: two screenshots in a row never matched' % w for w in WIDTHS if not M[w]['settled']], len(WIDTHS))
    def px(w): return Image.open(io.BytesIO(M[w]['shot'])) if M[w]['shot'] else None
    # LISTMARGIN (L1)
    f = []; n = 0
    for w in WIDTHS:
        for t, x in M[w]['olMarkers']:
            n += 1
            if abs(x) > 0.5: f.append('%d: "%s" number starts %.1fpx from the margin' % (w, t, x))
    put('LISTMARGIN', f, n)
    # JUSTIFY (T1): every wrapped paragraph and list line justified
    f = []; n = 0
    for w in WIDTHS:
        n += M[w]['wrapped']; f += ['%d: not justified (%s): "%s"' % (w, a, t) for t, a in M[w]['notJustified']]
    put('JUSTIFY', f[:60], n)
    # DASHES (T4)
    put('DASHES', ['long dash in "%s"' % t for t in M[1280]['dashes']], 1)
    # LINECOLOUR (B1)
    f = []; n = 0
    for w in WIDTHS:
        for c in M[w]['lineColours']:
            n += 1
            if c != 'rgb(217, 201, 171)': f.append('%d: beige line is %s' % (w, c))
    put('LINECOLOUR', f, n)
    # NOINVISIBLE (B2)
    put('NOINVISIBLE', ['%d: invisible line %s' % (w, x) for w in WIDTHS for x in M[w]['invisible']], len(WIDTHS))
    # QUOTE (Q1, Q2)
    f = []; n = 0
    for w in WIDTHS:
        for q in M[w]['quotes']:
            n += 1; fs, lh, st = (18, 40, 'italic') if w > 830 else (17, 38, 'italic')   # 21 Oct 18:5x: the live Sensorial page (the model) sets 17/38 at 830 and below, measured at 830 768 700 641 640 390
            if abs(q['fs'] - fs) > 0.1 or abs(q['lh'] - lh) > 0.1 or q['style'] != st: f.append('%d: quotation %spx / %spx %s: "%s"' % (w, q['fs'], q['lh'], q['style'], q['t']))
            for c in q['cites']:
                if c['style'] != 'normal' or abs(c['fs'] - q['fs']) > 0.1 or not c['ownLine']: f.append('%d: attribution %spx %s, own line %s: "%s"' % (w, c['fs'], c['style'], c['ownLine'], c['t']))
    put('QUOTE', f[:40], n)
    # NAMELINES (N1)
    f = []; n = 0
    for w in WIDTHS:
        im = px(w)
        for nl in M[w]['nameLines']:
            n += 1; want = (30, 20) if w > 640 else (36, 30.3)
            g1 = pixgap(im, nl['x0'], nl['x1'], nl['lineBottom'] - 0.5, nl['lineBottom'] + 0.5) if im else None
            if g1 is not None and abs(g1 - want[0]) > 1: f.append('%d: line to "%s" %.1f, want %s' % (w, nl['t'], g1, want[0]))
    put('NAMELINES', f, n)
    # FOOTER (F1-F4)
    f = []
    for w in WIDTHS:
        ft = M[w]['footer']; im = px(w)
        if not ft: f.append('%d: no footer band' % w); continue
        g = pixgap(im, ft['x0'], ft['x1'], ft['bandTop'] - 1, ft['bandTop']) if im else None
        wb = 60 if w > 640 else (40 if ft.get('endsPhoto') else 35.2)   # 21 Oct 18:5x: the Essay template's 20 Oct figure 60 above 640; phones 35.2 (mean of 17 live pages, user 21 Oct 13:4x) or 40 when the page ends in a photo (user 21 Oct 13:56) - as check_page; the 18 Oct 40 was replaced
        if g is not None and abs(g - wb) > 1: f.append('%d: last letters or photo to the band %.1f, want %s' % (w, g, wb))
        if ft['bg'] != 'rgb(30, 77, 123)': f.append('%d: band colour %s, want #1E4D7B' % (w, ft['bg']))
        if (ft['pt'], ft['pb']) != (40.0, 30.0): f.append('%d: band padding %s / %s, want 40 / 30' % (w, ft['pt'], ft['pb']))
        if not ft['breaksOk']: f.append('%d: quotation lines %s' % (w, ft['lines']))
        if ft['strip'] != ['© 2026 Montessori Mentor', 'Back to top']: f.append('%d: strip reads %s' % (w, ft['strip']))
        if ft['stripCol'] != 'rgb(107, 107, 107)' or ft['stripFs'] != 15: f.append('%d: strip %s %spx, want #6B6B6B 15px' % (w, ft['stripCol'], ft['stripFs']))
    put('FOOTER', f, len(WIDTHS))
    # MENU (M1-M4)
    f = []
    for w in WIDTHS:
        mn = M[w]['menu']
        f += ['%d: line under menu entry "%s"' % (w, t) for t in mn['lined']]
        if w > 830 and mn['panelBg'] and mn['panelBg'] != 'rgb(245, 238, 227)': f.append('%d: menu panel %s, want #F5EEE3' % (w, mn['panelBg']))   # computers: the menu bar shows its panels above 830
        f += ['%d: %s' % (w, x) for x in mn['own']]
        if w >= 1024 and M[w].get('hover_opens'): f.append('%d: a menu panel opens on hover' % w)
    put('MENU', f, len(WIDTHS))
    # BLUES (M5)
    put('BLUES', ['%s used outside the menu: %s' % (c, t) for c, t in M[1280]['blues']], 1)
    # HERO (H1)
    put('HERO', ['rotating hero on a page that is not Play or Education'] if M[1280]['heroRotates'] else [], 1)
    # A11Y (X4)
    f = []
    ft_ = M[1280]['first_tab']
    if not ft_ or not (ft_[1] or '').startswith('#'): f.append('first Tab lands on %s, not a skip link' % (ft_,))
    # (photo descriptions no longer checked: 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere)
    put('A11Y', f, 1)
    # PROTECT (C1)
    f = []
    ph = open(os.path.join(pv, 'index.html'), encoding='utf-8').read()
    if 'mm-protect' in ph: f.append('the preview has copy protection')
    if hs is None: f.append('no Hostinger copy')
    elif 'mm-protect-js' not in open(os.path.join(hs, 'index.html'), encoding='utf-8').read(): f.append('the Hostinger copy has no copy protection')
    put('PROTECT', f, 2)
    # ADDED (B3) and TEMPLATE (X8): every block the build added is a named, asked-for one; outside main the page is the template
    t = open(TEMPLATE, encoding='utf-8').read()
    for o_, n_ in S.get('PAGE_CODE_REPLACE', []): t = t.replace(o_, n_)   # a page's own named change to the template's code (each with its source in the page settings)
    ids_t = set(re.findall(r'<(?:style|script)[^>]*\bid="([^"]+)"', t)); ids_p = re.findall(r'<(?:style|script)[^>]*\bid="([^"]+)"', ph)
    put('ADDED', ['block "%s" added, not asked for' % i for i in ids_p if i not in ids_t and i not in ADDED_OK], len(ids_p))
    def outside(h):
        h = re.sub(r'<main\b.*?</main>', '<main/>', h, flags=re.S)
        h = re.sub(r'<(style|script)[^>]*\bid="(%s)"[^>]*>.*?</\1>' % '|'.join(map(re.escape, ADDED_OK)), '', h, flags=re.S)
        h = re.sub(r'<title>.*?</title>', '', h, flags=re.S)
        h = re.sub(r'<div class="hero"[^>]*>.*?</div>', '<hero/>', h, count=1, flags=re.S)
        h = re.sub(r'<nav aria-label="Contents".*?</nav>', '', h, flags=re.S).replace('<div class="toc-rule-wrap"><div class="beige-rule"></div></div>', '')
        h = re.sub(r'<li><a href="[^"]*" aria-current="page">([^<]*)</a></li>', r'<li><span class="np">\1</span></li>', h)
        h = h.replace(' aria-current="page"', '')
        return [x.strip() for x in re.split(r'(?=<)', re.sub(r'\s+', ' ', h)) if x.strip()]   # tag by tag, white space ignored
    import difflib
    dl = [x for x in difflib.unified_diff(outside(t), outside(ph), lineterm='', n=0) if x[:1] in '+-' and not x.startswith(('+++', '---'))]
    put('TEMPLATE', ['outside the text the page differs from the template: %s' % x[:120] for x in dl][:20], len(outside(t)))
    # HEADINGS (S1, S2)
    f = []; n = 0
    for w in WIDTHS:
        for h in M[w]['headings']:
            if h['colour'] not in ('rgb(4, 50, 255)', 'rgb(238, 0, 0)', 'rgb(255, 0, 0)'): continue
            n += 1; want = 18   # user 21 Oct 20:49-20:51: blue and red headings 18
            if abs(h['fs'] - want) > 0.1 or h['border'] > 0: f.append('%d: "%s" %spx, line %spx; want %spx, no line' % (w, h['t'], h['fs'], h['border'], want))
    put('HEADINGS', f, n)
    # NOTOC (S5)
    put('NOTOC', ['the page has a table of contents'] if sset['noToc'] and M[1280]['toc'] else [], 1 if sset['noToc'] else 0)
    # LINKS (S6, S8)
    f = []
    f += ['link "%s" is %s, want #0432FF' % (t, c) for t, c in M[1280]['linkColours'] if c != 'rgb(4, 50, 255)']
    for tx, href in sset['links']:
        if [tx, href] not in M[1280]['linkTargets']: f.append('"%s" is not a link to %s' % (tx, href))
    put('LINKS', f, len(M[1280]['linkColours']))
    # UNDERLINE (S7)
    f = ['"%s" not underlined (%d)' % (l, w) for w in WIDTHS for l in sset['labels'] if l not in M[w]['underlinedLabels']]
    put('UNDERLINE', f, len(sset['labels']) * len(WIDTHS))
    # GAPS (S3, S4, S9): the page settings' spaces, from the pixels
    f = []; n = 0
    for w in WIDTHS:
        im = px(w)
        if im is None: continue
        for gp in M[w]['gaps']:
            if gp.get('missing'): f.append('%d: %s' % (w, gp['what'])); continue
            n += 1; g = pixgap(im, gp['x0'], gp['x1'], gp['aBottom'], gp['bTop'])
            if abs(g - gp['want']) > 1: f.append('%d: %s %.1f, want %s' % (w, gp['what'], g, gp['want']))
    put('GAPS', f, n)
    # RESLIVE (S10): the Resources section's spaces against the live Culture Resources page, both measured from pixels the same
    # way, median per kind (head = green line to the first name, name = name to its first line, entry = entry to entry)
    f = []; n = 0
    def med(MM_, w_, kind):
        im_ = Image.open(io.BytesIO(MM_[w_]['shot'])) if MM_[w_]['shot'] else None
        v = sorted(pixgap(im_, g['x0'], g['x1'], g['aBottom'], g['bTop']) for g in MM_[w_]['res'] if g['kind'] == kind) if im_ else []
        return v[len(v) // 2] if v else None
    cache = os.path.join(HERE, 'live-res-medians.json')
    if LIVEM:
        LMED = {str(w): {k: med(LIVEM, w, k) for k in ('head', 'name', 'entry')} if LIVEM.get(w) else None for w in WIDTHS}
        json.dump({'measured': __import__('datetime').datetime.now().isoformat(timespec='seconds'), 'medians': LMED}, open(cache, 'w'), indent=1)
    else:
        LMED = json.load(open(cache))['medians'] if os.path.exists(cache) else {}
    for w in WIDTHS:
        if not LMED.get(str(w)): f.append('%d: the live page could not be measured' % w); continue
        for kind in ('head', 'name', 'entry'):
            a_, b_ = LMED[str(w)][kind], med(M, w, kind)
            if b_ is None: continue
            n += 1
            if a_ is None or abs(a_ - b_) > 1: f.append('%d: %s live %s, page %s' % (w, kind, a_, b_))
        im_ = px(w)
        for g in (M[w]['res'] if im_ else []):   # 21 Oct 19:39-19:40 (user): the beige lines between entries, 30 above and 30 below
            if g['kind'] != 'line': continue
            n += 1; v = pixgap(im_, g['x0'], g['x1'], g['aBottom'], g['bTop'])
            if abs(v - g['want']) > 1: f.append('%d: %s %.1f, want %s' % (w, g['what'], v, g['want']))
    put('RESLIVE', f, n)
    # RESNAME (user 21 Oct 20:52): a source's red name never sits inside another entry's description
    put('RESNAME', ['red name inside a description: "%s"' % t for t in M[1280].get('redStarts', [])], 1)
    # RESNAME (user 21 Oct 20:52): a source's red name never sits inside another entry's description
    put('RESNAME', ['red name inside a description: "%s"' % t for t in M[1280].get('redStarts', [])], 1)
    # FLOATTOP (P3 at 1440 and 390): a photo beside text starts level with the top of the first line's letters
    f = []; n = 0
    for w in (1440, 390):
        for t_, off in M[w]['floatTops']:
            n += 1
            if abs(off) > 1: f.append('%d: photo beside "%s" %.1fpx off the first line' % (w, t_, off))
    put('FLOATTOP', f, n)
    # SWIPE (P4): at 390 a row wider than the screen scrolls, has one dot per photo, and after a swipe a photo stops in the
    # middle (within 2px); a row that fits shows no dots
    f = []; n = 0
    sw = dict((i, o_) for i, o_ in M[390].get('swipes', []))
    for r in M[390]['rows']:
        n += 1
        if r['overflows']:
            if not (r['scrolls'] and r['dots'] == r['photos']): f.append('photo row %d: scrolls %s, dots %s of %s' % (r['i'], r['scrolls'], r['dots'], r['photos']))
            if r['i'] in sw and sw[r['i']] > 2: f.append('photo row %d: after a swipe the nearest photo is %.1fpx off the middle' % (r['i'], sw[r['i']]))
        elif r['dotsShown']: f.append('photo row %d fits the screen but shows dots' % r['i'])
    put('SWIPE', f, n)
    # ORANGE (W7): Word's orange text shows in the text colour
    f = []
    try:
        import docx
        from docx.oxml.ns import qn
        d = docx.Document(S.get('_DOCX') or os.environ.get('MM_DOCX', ''))
        oranges = []
        for p_ in d.paragraphs:
            for r_ in p_.runs:
                rp = r_._r.find(qn('w:rPr')); c = rp.find(qn('w:color')) if rp is not None else None
                v = (c.get(qn('w:val')) or '').upper() if c is not None else ''
                if re.fullmatch(r'[0-9A-F]{6}', v):
                    R_, G_, B_ = int(v[:2], 16), int(v[2:4], 16), int(v[4:], 16)
                    if R_ > 200 and 80 <= G_ <= 200 and B_ < 90 and r_.text.strip(): oranges.append(r_.text.strip())
        def orange(c):
            v = [int(x) for x in re.findall(r'\d+', c)[:3]]
            return len(v) == 3 and v[0] > 200 and 80 <= v[1] <= 200 and v[2] < 90
        for o in oranges:
            for t_, c in M[1280]['coloured']:
                if o[:30] in t_ and orange(c): f.append('Word orange "%s" shows %s' % (o[:30], c)); break
        put('ORANGE', f, len(oranges))
    except Exception as e:
        put('ORANGE', ['could not read the Word file: %s' % str(e)[:60]], 0)
    # FACES (P2): every face faces.json marks for blurring is blurred on the page (smoother than Word's original there)
    f = []; n = 0
    fj = S.get('_FACES') or os.environ.get('MM_FACES', '')
    if fj and os.path.exists(fj):
        fd = json.load(open(fj)); zf = zipfile.ZipFile(S.get('_DOCX') or os.environ.get('MM_DOCX'))
        media = {os.path.basename(x): x for x in zf.namelist() if x.startswith('word/media/')}
        names = M[1280]['imgNames']   # data-name -> data-full
        from docx.oxml.ns import qn as _qn
        import docx as _dx
        _d = _dx.Document(S.get('_DOCX') or os.environ.get('MM_DOCX')); _rels = {r.rId: r for r in _d.part.rels.values()}; CROP = {}
        for dr in _d.element.body.iter(_qn('w:drawing')):
            bl = dr.find('.//' + _qn('a:blip')); sr = dr.find('.//' + _qn('a:srcRect'))
            if bl is not None and sr is not None and bl.get(_qn('r:embed')) in _rels and any(sr.get(k) for k in 'ltrb'):
                CROP[_rels[bl.get(_qn('r:embed'))].target_ref.split('/')[-1]] = tuple(int(sr.get(k) or 0) / 100000 for k in 'ltrb')
        ROT = {}   # 21 Oct 2026 (9a, image10): Word turns a photo by its a:xfrm rot (60000ths of a degree, clockwise); the page shows it turned, so the check turns Word's copy and its face boxes the same way
        for dr in _d.element.body.iter(_qn('w:drawing')):
            bl = dr.find('.//' + _qn('a:blip')); xf = dr.find('.//' + _qn('a:xfrm'))
            if bl is not None and xf is not None and bl.get(_qn('r:embed')) in _rels and int(xf.get('rot') or 0) % 21600000:
                ROT[_rels[bl.get(_qn('r:embed'))].target_ref.split('/')[-1]] = round(int(xf.get('rot')) / 5400000) % 4
        def lap(a):
            a = a.astype(float); return float(np.var(a[1:-1, 2:] + a[1:-1, :-2] + a[2:, 1:-1] + a[:-2, 1:-1] - 4 * a[1:-1, 1:-1]))
        for nm, rec in fd.items():
            blur = S.get('FACES_BLUR') if S.get('FACES_BLUR') is not None else list((rec.get('faces') or {}).keys())
            if nm not in names or nm not in media: continue
            orig = Image.open(io.BytesIO(zf.read(media[nm]))).convert('L'); page = Image.open(os.path.join(pv, names[nm])).convert('L')
            cl, ct, cr, cb = CROP.get(nm, (0, 0, 0, 0)); W0, H0 = orig.size; ox, oy = W0 * cl, H0 * ct
            orig = orig.crop((round(W0 * cl), round(H0 * ct), round(W0 * (1 - cr)), round(H0 * (1 - cb))))   # Word's crop, as the build does
            q_ = ROT.get(nm, 0); oW, oH = orig.size
            if q_: orig = orig.rotate(-90 * q_, expand=True)
            sx, sy = page.width / orig.width, page.height / orig.height
            for k, box in (rec.get('faces') or {}).items():
                if k not in blur: continue
                x, y, bw, bh = box[:4]; x -= ox; y -= oy; n += 1
                for _ in range(q_): x, y, bw, bh, oW, oH = oH - (y + bh), x, bh, bw, oH, oW   # one quarter turn clockwise
                if abs(sx - sy) > 0.02: f.append('%s %s: page photo is not Word\'s shape, face not checked' % (nm, k)); continue
                po = np.asarray(orig.crop((int(x), int(y), int(x + bw), int(y + bh))).resize((64, 64)))
                pp = np.asarray(page.crop((int(x * sx), int(y * sy), int((x + bw) * sx), int((y + bh) * sy))).resize((64, 64)))
                if lap(pp) > 0.5 * lap(po): f.append('%s face %s not blurred (detail %.0f, Word %.0f)' % (nm, k, lap(pp), lap(po)))
    put('FACES', f, n)
    # ERRORS on the Hostinger copy too (X1): its index must equal the preview apart from copy protection
    if hs:
        hh = open(os.path.join(hs, 'index.html'), encoding='utf-8').read()
        hh2 = re.sub(r'<style id="mm-protect">.*?</style>', '', hh, flags=re.S); hh2 = re.sub(r'<script id="mm-protect-js">.*?</script>', '', hh2, flags=re.S)
        put('HOSTINGER', [] if hh2 == ph else ['the Hostinger copy differs from the preview beyond copy protection'], 1)
    return R

BREAK = {   # one fault per check, all put into one copy of the build (prove mode)
 'DASHES': ('a long dash in the text', 'html', lambda h: re.sub(r'(<p>[^<]{20,}?) - ', '\\1 \u2014 ', h, count=1)),
 'LINECOLOUR': ('beige lines #E7DCC6', 'css', 'main p.mm-gl{background:#E7DCC6 !important}'),
 'MENU': ('a line under every panel entry', 'css', '.panel a{text-decoration:underline !important}'),
 'BLUES': ('a paragraph in another blue', 'css', 'main section > p{color:#3366CC !important}'),
 'HERO': ('a rotating hero', 'html', lambda h: h.replace('<div class="hero" ', '<div class="hero" ', 1).replace('<h1><span>', '<div class="mm-hs"></div><h1><span>', 1)),
 'PROTECT': ('copy protection in the preview', 'html', lambda h: h.replace('</head>', '<style id="mm-protect">body{}</style></head>', 1)),
 'ADDED': ('a block nobody asked for', 'html', lambda h: h.replace('</head>', '<style id="mm-extra">body{}</style></head>', 1)),
 'HEADINGS': ('blue headings 22px', 'css', 'html body main .section h2.mm-hc-0432FF.mm-hc-0432FF{font-size:22px !important}'),
 'NOTOC': ('a contents box', 'html', lambda h: h.replace('<main', '<nav aria-label="x" class="toc-wrap" style="display:block">Table of contents</nav><main', 1)),
 'LINKS': ('links navy', 'css', 'html body main a:not(.pdf):not(.mmx1):not(.mmx2):not(.mmx3){color:#1E4D7B !important}'),
 'UNDERLINE': ('the labels not underlined', 'css', 'html body main .micro-label.mm-ulab{text-decoration:none !important}'),
 'FLOATTOP': ('the cover no longer lined up with its first line', 'html', lambda h: h.replace('function tops(){', 'function tops(){return;', 1)),
 'ORANGE': ('quotations in orange', 'css', 'html body main blockquote p{color:#ED7D31 !important}'),
 'HOSTINGER': ('the preview changed after the build', 'html', lambda h: h.replace('</body>', '<!-- changed --></body>', 1)),
 'GAPS': ('the Right: lines (mm-pairend) moved 8px down', 'css', 'html body main p.mm-pairend{transform:translateY(8px) !important}'),   # moving every label line moved both lines of each pair, so the gap did not change; only the Right: lines are moved now
 'FOOTER': ('the footer band another colour', 'css', 'html body .mc-band{background:#123456 !important}'),
 'QUOTE': ('quotations upright', 'css', 'html body main blockquote.pullquote.pullquote p{font-style:normal !important}'),
 'JUSTIFY': ('paragraphs left-aligned', 'css', 'html body main section > p{text-align:left !important}'),
 'LISTMARGIN': ('lists moved 10px in', 'css', 'html body main ol.mm-wi.mm-wi{margin-left:10px !important}'),
 'A11Y': ('no skip link', 'html', lambda h: re.sub(r'<a class="skip[^"]*"[^>]*>.*?</a>', '', h, count=1, flags=re.S)),
 'NOINVISIBLE': ('a hidden beige line', 'html', lambda h: h.replace('</main>', '<div class="beige-rule" style="visibility:hidden;width:300px;height:2px"></div></main>', 1)),
 'TEMPLATE': ('an extra element outside the text', 'html', lambda h: h.replace('<body>', '<body><div id="mm-x"></div>', 1) if '<body>' in h else re.sub(r'(<body[^>]*>)', r'\1<div id="mm-x"></div>', h, count=1)),
 'RESNAME': ('a red name put back inside the description before it', 'html', lambda h: h.replace('</div><div class="beige-rule mm-org-rule" data-setting="res"></div><div class="res-entry mm-lstart"><h3 class="material-name res-src">The University of San Diego Division of Professional and Continuing Education</h3><p class="res-desc">', '<p class="res-desc"><span style="color:#EE0000">The University of San Diego Division of Professional and Continuing Education</span> ', 1)),
 'RESNAME': ('a red name put back inside the description before it', 'html', lambda h: h.replace('</div><div class="beige-rule mm-org-rule" data-setting="res"></div><div class="res-entry mm-lstart"><h3 class="material-name res-src">The University of San Diego Division of Professional and Continuing Education</h3><p class="res-desc">', '<p class="res-desc"><span style="color:#EE0000">The University of San Diego Division of Professional and Continuing Education</span> ', 1)),
 'RESLIVE': ('the live Resources spacing switched off', 'html', lambda h: h.replace('function run(){var sec', 'function run(){return;var sec', 1)),
 'SWIPE': ('photo rows that do not scroll', 'css', 'html body main .mm-row.mm-row{overflow-x:hidden !important}'),
 'SETTLE': ('something that never stops moving', 'html', lambda h: h.replace('</main>', '<div style="height:20px;width:200px;animation:mmx 0.3s infinite alternate;background:#fff"></div><style>@keyframes mmx{from{opacity:1}to{opacity:.2}}</style></main>', 1)),
}

def prove(build, settings_path):
    rj = os.path.join(build, 'rule_checks.json')
    real = json.load(open(rj)) if os.path.exists(rj) else check(build, settings_path)   # the last run on this same build
    os.environ['MM_LIVE_CACHE'] = '1'
    d = tempfile.mkdtemp(prefix='rule-proof-', dir='/tmp/claude-0/-home-claude/63e05c82-dcea-58b1-8b9e-4cfa5333876d/scratchpad'); bb = os.path.join(d, 'build')
    shutil.copytree(build, bb)
    page = os.path.join(bb, 'preview', 'index.html'); h = open(page, encoding='utf-8').read(); css = []
    only = [x for x in os.environ.get('MM_ONLY', '').split(',') if x]
    for k, (what, kind, f) in list(BREAK.items()):
        if only and k not in only: continue
        if kind == 'css': css.append(f)
        else:
            h2 = f(h)
            if h2 == h: print('breaker for %s found nothing to break' % k)
            h = h2
    h = h.replace('</head>', '<style id="mm-break">%s</style></head>' % '\n'.join(css), 1)
    open(page, 'w', encoding='utf-8').write(h)
    # FACES: the first blurred photo replaced by Word's original (unblurred)
    S = {}
    if settings_path:
        import runpy; S = runpy.run_path(settings_path)
    try:
        nm = re.search(r'data-full="(images/\d+\.jpg)" data-name="image2\.jpeg"|data-name="image2\.jpeg"[^>]*data-full="(images/\d+\.jpg)"', h)
        full = (nm.group(1) or nm.group(2)) if nm else None
        zf = zipfile.ZipFile(os.environ['MM_DOCX']); orig = Image.open(io.BytesIO(zf.read('word/media/image2.jpeg'))).convert('RGB')
        tgt = os.path.join(bb, 'preview', full); W_, H_ = Image.open(tgt).size; orig.resize((W_, H_)).save(tgt, quality=92)
        BREAK['FACES'] = ('a blurred photo swapped for Word\'s original', 'file', None)
    except Exception as e: print('FACES breaker failed:', e)
    bad = check(bb, settings_path)
    src = open(__file__, encoding='utf-8').read(); code = hashlib.sha256((src[:src.index('BREAK = {')] + open(os.path.join(HERE, 'rule_checks.js'), encoding='utf-8').read()).encode()).hexdigest()   # the checks' code, not the faults put in
    pf = os.path.join(HERE, 'rule-proofs.json'); proofs = json.load(open(pf)) if os.path.exists(pf) else {}
    for k in BREAK:
        if only and k not in only and k != 'FACES': continue
        new = [x for x in bad.get(k, {}).get('faults', []) if x not in real.get(k, {}).get('faults', [])]
        proofs[k] = {'proved': bool(new), 'fault_put_in': BREAK[k][0], 'caught': new[:3], 'code': code}
        print('%-11s %s: "%s" -> %s' % (k, 'PROVED' if new else 'NOT PROVED', BREAK[k][0], new[:1]))
    json.dump(proofs, open(os.path.join(HERE, 'rule-proofs.json'), 'w'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'prove': prove(a[1], a[2] if len(a) > 2 else None); sys.exit(0)
    R = check(a[0], a[1] if len(a) > 1 else None)
    json.dump(R, open(os.path.join(a[0], 'rule_checks.json'), 'w'), indent=1, ensure_ascii=False)
    for k, v in R.items():
        print('%-11s %s (%d checked)%s' % (k, 'PASS' if v['ok'] else 'FAIL', v['checked'], ''.join('\n     - ' + x for x in v['faults'][:25])))
    print('\nALL PASS' if all(v['ok'] for v in R.values()) else '\nFAILURES: ' + ', '.join(k for k, v in R.items() if not v['ok']))
