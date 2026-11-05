#!/usr/bin/env python3
"""images_behaviour.py <page folder with index.html> <out file> [widths] [parts]   (5 Nov 2026; checks plan item 3,
/home/claude/eng35/checks-plan/PLAN.md - rows D142, D143, D205, D213, A034, A035, E025, E049, E050, A013)

widths: a comma list, or "full" for the 122 widths of visual_check.py. Default: the band edges only -
320,390,640,641,700,768,830,831,960,961,1024,1280,1440,1920 (the gate's run should pass "full").
parts (for proofs only; the gate runs all): a comma list of heights,swipe,late,behaviour. Default: all.
Phone and tablet widths (830 and narrower, the template's phone() limit) are measured as a touch phone
(is_mobile, has_touch); wider widths as a computer.

Parts (every figure is quoted from a row of /home/claude/mm/tools/REQUIRED-CHECKS.json, cited by its id):
 1 HEIGHTS at every width
   D142 "rows of images at most 150 px high on computers (was 170)" - from 831 up every photo in a row (.mm-row)
        and in a group of 2+ photos side by side (.mm-set .mm-imgs, other .mm-imgs) is at most 150 high. (Not a
        single photo in a set - not a row; not .mm-intro: the template's own introduction photo rule has no row
        figure; not .mm-float: D205.)
   D143 "a row that does not fit shrinks to 120 px before its gaps shrink (was 140)" - from 831 up a row of 2+
        photos under 150: if under 120, the gaps of its row group must be at the template's minimum (RMIN = 10,
        Essay template line 861; rows that share a data-level take one height, template rows()); if over 120,
        its gaps must not be under the template's full gap (RGAP 38.4 scaled to min(38.4, (window - 80) x 38.4 /
        1140), template rows()).
   D205 "120 (was 150)" - from 831 up a photo beside text (.mm-float) is 120 high.
   D213 "from 641 to 830 px the images in groups above their text are 180 px high instead of 70 px" - 641-830:
        .mm-set.mm-col photos 180; 640 and narrower: 70. AMBIGUITY SETTLED WITH THE TEMPLATE: the Essay template
        (block mm-owner-27oct, line 2227-2228, and line 588) gives 70 px at 640 and narrower ONLY to
        .mm-set.mm-col groups; other groups keep --hp (180) and the introduction photo 240. So only .mm-set.mm-col
        is held to 70 here. (641-830 the template's rule is min(--hp, 200); with --hp 180, as every figure here, 180.)
   A035 "a row that fits the screen stays still as one centred group with no dots, on every page and width" -
        at every width a row (.mm-row; and below 831 a group .mm-set .mm-imgs, which is a swipe strip there)
        that fits: no scrolling, no visible dots, the space left of the first photo equals the space right of the
        last (1 px).
 2 SWIPE at 390, 640, 768 (touch): a strip that does not fit:
   E025 "pose as a phone and swipe each photo row to check it moves and the dots follow (simulated touch)" -
        one dot per photo, the strip moves on a swipe, the lit dot is the photo that came to rest.
   A034 "in swipe rows each photo stops in the middle of the screen (space added at both ends)" - at the start,
        after two swipes, and at the end, the resting photo's centre is within 1 px of the screen's centre.
        A strip that fits: a swipe must not move it (A035).
 3 LATE IMAGES at 1280, 768, 390 - E049 "Faults that appear only while a visitor scrolls, before every image has
   loaded": every image file held back 3 s, the page scrolled through in 400 px steps; at each step, in the
   window: no text over a photo, no photo over a photo (photos clipped to their strip); and no layout shift
   (Chromium's layout-shift entries) while scrolling or as the images arrive.
 4 BEHAVIOUR at 1440 and 390 - E050 "the image viewer, swiping on phones, contents links jumping to their
   heading, hover": the viewer opens on a photo with its full-size file, next/previous change photo and counter,
   Escape and a click on the backdrop close it; each contents link brings its heading to the top of the window
   (its top within 3 px of the template's landing place, html scroll-padding-top - Essay template line 21, 76 px,
   and line 123, 64 px on phones - or the page at its end) and its letters not hidden under the sticky header; hover (1440): a menu name
   does not open its panel, and a photo does not move or change size under the pointer.
 5 HERO at 1440 and 390 - A013 "hero images rotate in Play and Education only": on any other page the hero is one
   image and its pixels are unchanged between 0 s and 12 s after loading.

Every fault is printed; then IMAGES PASS or IMAGES FAULT (n), then END. The same lines go to <out file>.
Screenshots of the first faults of each kind go to <out file>.shots/."""
import sys, os, re, asyncio, http.server, threading, functools, socket, json, io, time

FOLDER, OUT = sys.argv[1], sys.argv[2]
FULL = sorted(set(list(range(320, 1441, 10)) + [640, 641, 830, 831, 960, 961, 1023, 1024, 1099, 1100, 1180, 1181, 1279, 1280, 1920]))   # visual_check.py's 122 widths
EDGES = [320, 390, 640, 641, 700, 768, 830, 831, 960, 961, 1024, 1280, 1440, 1920]
ARG = sys.argv[3] if len(sys.argv) > 3 else ''
WIDTHS = FULL if ARG == 'full' else ([int(x) for x in ARG.split(',')] if ARG else EDGES)
PARTS = set((sys.argv[4] if len(sys.argv) > 4 else 'heights,swipe,late,behaviour').split(','))
SWIPE_W = [390, 640, 768]          # plan item 3 (A034, E025)
LATE_W = [1280, 768, 390]          # as fault_checks.py check E
BEHAV_W = [1440, 390]
SHOTS = OUT + '.shots'
os.makedirs(SHOTS, exist_ok=True)

# figures, each from its row's quote
ROW_MAX = 150        # D142 "rows of images at most 150 px high on computers (was 170)"
ROW_SHRINK = 120     # D143 "a row that does not fit shrinks to 120 px before its gaps shrink (was 140)"
FLOAT_H = 120        # D205 "120 (was 150)"
COL_641_830 = 180    # D213 "from 641 to 830 px the images in groups above their text are 180 px high instead of 70 px"
COL_640 = 70         # D213 "... instead of 70 px" (kept at 640 and narrower: Essay template line 588 and line 2227)
CENTRE_TOL = 1       # A034 plan item 3: "photo centre within 1 px of screen centre after settle"
HERO_T = 12          # A013 plan item 3: "unchanged at 0 s and 12 s"
DELAY = 3            # E049 plan item 3: "delay images 3 s"
# the template's own figures (Essay Code Template.html), used only where a row points at the template's rule
RMIN = 10            # line 861: var RGAP = 38.4, RMIN = 10, RSHRINK = 120 - the gaps' minimum (D143 "before its gaps shrink")
RGAP = 38.4          # line 861: the full row gap, scaled in rows(): Math.min(RGAP, (window.innerWidth - 80) * RGAP / 1140)
TOL = 0.5

lines_out = []
def say(s):
    print(s, flush=True); lines_out.append(s)
faults = []
def fault(s):
    faults.append(s); say('FAULT ' + s)

def serve(folder):
    port = (lambda s: (s.bind(('127.0.0.1', 0)), s.getsockname()[1], s.close())[1])(socket.socket())
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Q, directory=folder)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port

# the image groups on the page, each with a name a reader can find: kind, number, first photo file, heading above
JS_GROUPS = r"""() => {
  const main = document.querySelector('main') || document.body;
  const head = el => { let e = el; while (e && e !== main) { let p = e.previousElementSibling; while (p) { if (/^H[23]$/.test(p.tagName)) return p.textContent.trim().slice(0, 40); const h = p.querySelector && p.querySelector('h2,h3'); if (h) { const hs = p.querySelectorAll('h2,h3'); return hs[hs.length-1].textContent.trim().slice(0, 40); } p = p.previousElementSibling; } e = e.parentElement; } return ''; };
  const name = el => { const i = el.querySelector('img.doc-img'); return i ? (i.getAttribute('data-full') || i.getAttribute('src') || '').split('/').pop() : ''; };
  const out = []; const seen = new Set();
  const add = (kind, el, scroller, dots) => { if (seen.has(el)) return; seen.add(el); out.push({kind, el, scroller, dots}); };
  main.querySelectorAll('.mm-row').forEach(r => add('row', r, r, r.nextElementSibling && r.nextElementSibling.classList.contains('mm-dots') ? r.nextElementSibling : null));
  main.querySelectorAll('.mm-set').forEach(s => { const im = s.querySelector('.mm-imgs'); if (im) add(s.classList.contains('mm-col') ? 'set-col' : (s.classList.contains('mm-intro') ? 'set-intro' : 'set'), s, im, s.nextElementSibling && s.nextElementSibling.classList.contains('mm-dots') ? s.nextElementSibling : null); });
  main.querySelectorAll('.mm-float').forEach(f => add('float', f, f, null));
  main.querySelectorAll('.mm-imgs').forEach(im => { if (!im.closest('.mm-row,.mm-set,.mm-float')) add('group', im, im, null); });
  window.__mmG = out;
  const cnt = {};
  return out.map((g, i) => { cnt[g.kind] = (cnt[g.kind] || 0) + 1; g.label = g.kind + ' ' + cnt[g.kind] + ' (' + name(g.el) + (head(g.el) ? ', under "' + head(g.el) + '"' : '') + ')'; return g.label; });
}"""

JS_MEASURE = r"""() => {
  const G = window.__mmG, vw = window.innerWidth, base = Math.min(%(RGAP)s, (vw - 80) * %(RGAP)s / 1140);
  const main = document.querySelector('main'), one = main && main.getAttribute('data-rows') === 'one';
  return G.map((g, i) => {
    const figs = [...g.el.querySelectorAll('figure.ph')].filter(f => f.getBoundingClientRect().width > 0);
    const pims = [...g.el.querySelectorAll('.pim')].filter(p => p.getBoundingClientRect().width > 0);
    const fr = figs.map(f => f.getBoundingClientRect()).sort((a, b) => a.left - b.left);
    const gaps = []; for (let k = 1; k < fr.length; k++) gaps.push(fr[k].left - fr[k-1].right);
    const sc = g.scroller, sr = sc.getBoundingClientRect(), cs = getComputedStyle(sc);
    const d = g.dots, dcs = d ? getComputedStyle(d) : null, dr = d ? d.getBoundingClientRect() : null;
    return {i, kind: g.kind, label: g.label, level: one ? 'one' : (g.el.getAttribute('data-level') || ''),
      hs: pims.map(p => +p.getBoundingClientRect().height.toFixed(2)), n: figs.length,
      gaps: gaps.map(x => +x.toFixed(2)), base: +base.toFixed(2),
      tweak: ['data-hscale', 'data-hmatch', 'data-gaps', 'data-h'].filter(a => g.el.hasAttribute(a)).map(a => a + '=' + g.el.getAttribute(a)).join(' '),
      sw: sc.scrollWidth, cw: sc.clientWidth, sl: sc.scrollLeft, ox: cs.overflowX,
      igap: g.el.style.gap || '', cgap: getComputedStyle(g.el).columnGap,
      // 5 Nov 2026 (checkfix, A035 misreading on The English Curriculum b22): a group that wraps onto several lines is measured
      // from its outermost photos (smallest left, largest right), not from the first and last in page order
      left: fr.length ? +(Math.min(...fr.map(r => r.left)) - sr.left).toFixed(2) : 0, right: fr.length ? +(sr.right - Math.max(...fr.map(r => r.right))).toFixed(2) : 0,
      fw: fr.length ? Math.max(...fr.map(r => r.right)) - Math.min(...fr.map(r => r.left)) : 0,
      dots: d ? d.querySelectorAll('span').length : 0,
      dotsShown: !!(d && dcs.display !== 'none' && dcs.visibility !== 'hidden' && dr.height > 0 && dr.width > 0),
      shown: sr.width > 0 && sr.height > 0};
  });
}""" % {'RGAP': RGAP}

async def settle(pg):
    await pg.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i => i.loading = "eager")')
    h = await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0, h + 900, 800):
        await pg.evaluate('window.scrollTo({top: %d, behavior: "instant"})' % y); await pg.wait_for_timeout(40)
    await pg.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
    await pg.evaluate('document.fonts.ready.then(() => 1)')
    for _ in range(40):   # every image decoded
        if await pg.evaluate('[...document.images].every(i => i.complete)'): break
        await pg.wait_for_timeout(250)
    await pg.wait_for_timeout(1500)
    prev = None
    for _ in range(12):   # the layout has stopped moving (the template re-runs on load + 700 ms and on resize)
        cur = await pg.evaluate('JSON.stringify([...document.querySelectorAll("main .pim, main h2, main p")].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.left), Math.round(r.height)]; }))')
        if cur == prev: return True
        prev = cur; await pg.wait_for_timeout(600)
    return False

async def new_page(b, w, late=False):
    mob = w <= 830
    ctx = await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
    pg = await ctx.new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    if late:
        async def slow(route):
            await asyncio.sleep(DELAY); await route.continue_()
        await pg.route(re.compile(r'.*/images/.*'), slow)
    pg._errs = errs
    return ctx, pg

shot_count = {}
async def shot(pg, key, sel_js=None, clip=None):
    """a screenshot of the first faults of each kind (sel_js: JS returning an element)"""
    n = shot_count.get(key.split(' ')[0], 0)
    if n >= 3: return ''
    shot_count[key.split(' ')[0]] = n + 1
    fn = os.path.join(SHOTS, re.sub(r'[^A-Za-z0-9_.-]+', '_', key)[:90] + '.png')
    try:
        if sel_js:
            el = await pg.evaluate_handle(sel_js)
            el = el.as_element()
            if el:
                await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
                bb = await el.bounding_box()
                if bb:
                    vp = pg.viewport_size
                    x0 = max(0, bb['x'] - 20); y0 = max(0, bb['y'] - 60)
                    await pg.screenshot(path=fn, clip={'x': x0, 'y': y0, 'width': min(vp['width'] - x0, bb['width'] + 40), 'height': min(vp['height'] - y0, bb['height'] + 120)})
                    return fn
        await pg.screenshot(path=fn, clip=clip) if clip else await pg.screenshot(path=fn)
        return fn
    except Exception as e:
        return '(screenshot failed: %s)' % str(e)[:60]

# ---------------------------------------------------------------- 1 heights + A035 at every width
async def heights(b, base, w):
    ctx, pg = await new_page(b, w)
    await pg.goto(base, wait_until='load', timeout=120000)
    ok = await settle(pg)
    if not ok: fault('%d: the layout did not stop moving within 7 s after loading - measured as it stood' % w)
    labels = await pg.evaluate(JS_GROUPS)
    M = await pg.evaluate(JS_MEASURE)
    n0 = len(faults); local = []
    def F(rule, g, msg):
        local.append((rule, g, msg)); fault('%d %s: %s %s' % (w, rule, g['label'], msg))
    if w >= 831:
        # D143: the row groups the template sizes together (rows(): data-level, or the whole page with data-rows=one)
        grp = {}
        for g in M:
            if g['kind'] == 'row': grp.setdefault(g['level'], []).append(g)
        for g in M:
            if not g['shown'] or not g['hs']: continue
            hmax, hmin = max(g['hs']), min(g['hs'])
            # a "row of images" (D142): every .mm-row, and a group of 2+ photos side by side; a single photo in a set
            # (a page's fixed data-h size, such as a tall narrow strip) is not a row and is not held to 150
            if (g['kind'] == 'row' or (g['kind'] in ('set', 'set-col', 'group') and g['n'] >= 2)) and hmax > ROW_MAX + TOL:
                F('D142', g, 'photos %.1f px high, over %d (rows of images at most 150 px high on computers)%s' % (hmax, ROW_MAX, ' [page sets %s]' % g['tweak'] if g['tweak'] else ''))
            if g['kind'] == 'float' and abs(hmax - FLOAT_H) > TOL:
                F('D205', g, 'photo beside text %.1f px high, not %d' % (hmax, FLOAT_H))
            if g['kind'] == 'row' and g['n'] >= 2:
                mates = grp.get(g['level'], [g])
                forced = ''
                if g['igap'] and g['cgap'] and abs(float(re.sub('[^0-9.]', '', g['igap']) or 0) - float(re.sub('[^0-9.]', '', g['cgap']) or 0)) > 0.1:
                    forced = ' [a stylesheet rule forces the gap to %s over the %s the template\'s row script set]' % (g['cgap'], g['igap'])
                at_min = any(x['gaps'] and min(x['gaps']) <= RMIN + TOL for x in mates) or any(x['n'] == 1 and x['fw'] >= x['cw'] - 1 for x in mates)
                if hmin < ROW_SHRINK - TOL and not at_min:
                    F('D143', g, 'photos %.1f px high, under %d, while the gaps are %s px (its row group\'s smallest gap %.1f; the template shrinks photos under 120 only once the gaps are at %d)%s%s'
                      % (hmin, ROW_SHRINK, '/'.join('%.1f' % x for x in g['gaps']), min(min(x['gaps']) for x in mates if x['gaps']), RMIN, ' [page sets %s]' % g['tweak'] if g['tweak'] else '', forced))
                if ROW_SHRINK + TOL < hmin < ROW_MAX - TOL and min(g['gaps']) < g['base'] - TOL:
                    F('D143', g, 'gaps %.1f px, under the full gap %.1f, while the photos are %.1f px (over 120): the gaps shrank before the photos reached 120%s%s'
                      % (min(g['gaps']), g['base'], hmin, ' [page sets %s]' % g['tweak'] if g['tweak'] else '', forced))
    elif w >= 641:
        for g in M:
            if g['kind'] == 'set-col' and g['shown'] and g['hs'] and (abs(max(g['hs']) - COL_641_830) > TOL or abs(min(g['hs']) - COL_641_830) > TOL):
                F('D213', g, 'photos %s px high, not %d (641-830 px)' % ('/'.join('%.1f' % x for x in sorted(set(g['hs']))), COL_641_830))
    else:
        for g in M:
            if g['kind'] == 'set-col' and g['shown'] and g['hs'] and (abs(max(g['hs']) - COL_640) > TOL or abs(min(g['hs']) - COL_640) > TOL):
                F('D213', g, 'photos %s px high, not %d (640 px and narrower)' % ('/'.join('%.1f' % x for x in sorted(set(g['hs']))), COL_640))
    # A035 a fitting row: still, centred, no dots - every width (groups beside text are rows only below 831, where they are strips)
    for g in M:
        if not g['shown'] or g['n'] < 1: continue
        strip = g['kind'] == 'row' or (w <= 830 and g['kind'] in ('set', 'set-col', 'set-intro', 'group'))
        if not strip: continue
        fits = g['fw'] <= g['cw'] + 1   # the photos (with their gaps) fit in the strip's width
        if fits and g['n'] >= 2:   # a single photo is not a row (template: "single photos are plain" on phones)
            if g['sw'] > g['cw'] + 1 and g['ox'] in ('auto', 'scroll'): F('A035', g, 'fits the screen (photos %.1f px in %d px) but scrolls (%d px wide)' % (g['fw'], g['cw'], g['sw']))
            if g['dotsShown']: F('A035', g, 'fits the screen but shows %d dots' % g['dots'])
            if abs(g['left'] - g['right']) > 1: F('A035', g, 'fits the screen but is not centred: %.1f px space on the left, %.1f on the right' % (g['left'], g['right']))
    # screenshots of the first faults
    for rule, g, msg in local:
        fn = await shot(pg, '%s %d %s' % (rule, w, g['label']), '() => window.__mmG[%d].el' % g['i'])
        if fn: say('  screenshot: %s' % fn)
    if pg._errs: fault('%d: script errors on the page: %s' % (w, ' | '.join(pg._errs[:3])))
    say('%d: %d groups measured, %d faults%s' % (w, len(M), len(faults) - n0, '' if w >= 831 else ' (touch phone)'))
    await ctx.close()
    return M

# ---------------------------------------------------------------- 2 swipe (A034, E025, A035)
JS_REST = r"""(i) => { const g = window.__mmG[i], sc = g.scroller, mid = window.innerWidth / 2;
  const f = [...g.el.querySelectorAll('figure.ph')].filter(x => x.getBoundingClientRect().width > 0);
  let k = 0, best = 1e9; f.forEach((x, j) => { const r = x.getBoundingClientRect(), dd = Math.abs((r.left + r.right) / 2 - mid); if (dd < best) { best = dd; k = j; } });
  const on = g.dots ? [...g.dots.querySelectorAll('span')].findIndex(s => s.classList.contains('on')) : -1;
  const sr = sc.getBoundingClientRect(), pk = f[k] ? f[k].getBoundingClientRect().width : 0;
  return {sl: sc.scrollLeft, k: k, off: +best.toFixed(2), on: on, n: f.length, max: sc.scrollWidth - sc.clientWidth,
          why: (pk > sc.clientWidth + 1 ? ' (the photo is ' + Math.round(pk) + ' px wide, wider than its ' + sc.clientWidth + ' px strip)' : '') +
               (Math.abs((sr.left + sr.right) / 2 - mid) > 1 ? ' (the strip\'s own middle is ' + ((sr.left + sr.right) / 2 - mid).toFixed(1) + ' px from the screen\'s)' : '')}; }"""

async def still(pg, i):
    prev = None
    for _ in range(20):
        r = await pg.evaluate(JS_REST, i)
        if prev and abs(r['sl'] - prev['sl']) < 0.5: return r
        prev = r; await pg.wait_for_timeout(150)
    return r

async def swipe(pg, cdp, i, dist):
    bb = await pg.evaluate('(i) => { const r = window.__mmG[i].scroller.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }', i)
    y = bb[1] + bb[3] / 2; xm = bb[0] + bb[2] / 2
    # a finger drag of dist px to the left across the strip's middle (simulated touch, 20 moves 16 ms apart), as a reader's swipe
    vw = pg.viewport_size
    x0 = min(vw['width'] - 4, xm + dist / 2); x1 = max(4, x0 - dist); y = min(vw['height'] - 4, max(4, y))
    await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y}]})
    for k in range(1, 21):
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * k / 20, 'y': y}]}); await asyncio.sleep(0.016)
    await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    await pg.wait_for_timeout(800)

async def swipes(b, base, w):
    ctx, pg = await new_page(b, w)
    await pg.goto(base, wait_until='load', timeout=120000); await settle(pg)
    await pg.evaluate(JS_GROUPS); M = await pg.evaluate(JS_MEASURE)
    cdp = await ctx.new_cdp_session(pg)
    n0 = len(faults); nstrip = 0
    for g in M:
        if not g['shown'] or g['n'] < 2: continue
        if not (g['kind'] == 'row' or g['kind'].startswith('set') or g['kind'] == 'group'): continue
        i = g['i']; lab = g['label']
        await pg.evaluate('(i) => window.__mmG[i].scroller.scrollIntoView({block: "center", behavior: "instant"})', i); await pg.wait_for_timeout(250)
        fits = g['fw'] <= g['cw'] + 1
        if fits:
            await swipe(pg, cdp, i, min(200, g['cw'] * 0.5)); r = await still(pg, i)
            if r['sl'] > 0.5: fault('%d A035: %s fits the screen but moved %.1f px on a swipe' % (w, lab, r['sl']))
            continue
        nstrip += 1; bad = []
        if g['dots'] != g['n']: bad.append('E025 %d dots for %d photos' % (g['dots'], g['n']))
        if not g['dotsShown']: bad.append('E025 no dots shown')
        r = await still(pg, i)
        if r['off'] > CENTRE_TOL: bad.append('A034 at the start photo %d rests %.1f px off the middle of the screen%s' % (r['k'] + 1, r['off'], r['why']))
        if g['dots'] and r['on'] != r['k']: bad.append('E025 at the start dot %d lit, photo %d in the middle' % (r['on'] + 1, r['k'] + 1))
        for s in range(2):
            # the finger moves by the distance from the screen's middle to the next photo's centre (as a reader's swipe to the next photo)
            dn = await pg.evaluate('(a) => { const f = [...window.__mmG[a[0]].el.querySelectorAll("figure.ph")].filter(x => x.getBoundingClientRect().width > 0)[a[1] + 1]; if (!f) return 0; const q = f.getBoundingClientRect(); return (q.left + q.right) / 2 - innerWidth / 2; }', [i, r['k']])
            if dn <= 0: break
            before = r['sl']
            await swipe(pg, cdp, i, max(40, min(dn, g['cw'] * 0.9))); r = await still(pg, i)
            if r['sl'] <= before + 0.5 and before < r['max'] - 0.5: bad.append('E025 swipe %d did not move the strip' % (s + 1)); break
            if r['off'] > CENTRE_TOL: bad.append('A034 after swipe %d photo %d rests %.1f px off the middle of the screen%s' % (s + 1, r['k'] + 1, r['off'], r['why']))
            if g['dots'] and r['on'] != r['k']: bad.append('E025 after swipe %d dot %d lit, photo %d in the middle' % (s + 1, r['on'] + 1, r['k'] + 1))
        await pg.evaluate('(i) => { const s = window.__mmG[i].scroller; s.scrollTo({left: s.scrollWidth, behavior: "instant"}); }', i); r = await still(pg, i)
        if r['k'] != r['n'] - 1 or r['off'] > CENTRE_TOL: bad.append('A034 at the end photo %d of %d rests %.1f px off the middle of the screen%s' % (r['k'] + 1, r['n'], r['off'], r['why']))
        if g['dots'] and r['on'] != r['k']: bad.append('E025 at the end dot %d lit, photo %d in the middle' % (r['on'] + 1, r['k'] + 1))
        await pg.evaluate('(i) => { window.__mmG[i].scroller.scrollTo({left: 0, behavior: "instant"}); }', i)
        for x in bad:
            fault('%d %s: %s' % (w, x.split(' ')[0], lab + ' ' + x.split(' ', 1)[1]))
        if bad:
            fn = await shot(pg, 'swipe %d %s' % (w, lab), '() => window.__mmG[%d].el' % i)
            if fn: say('  screenshot: %s' % fn)
    say('%d swipe: %d strips that do not fit swiped, %d faults' % (w, nstrip, len(faults) - n0))
    await ctx.close()

# ---------------------------------------------------------------- 3 late images (E049)
JS_OVER = r"""() => { const m = document.querySelector('main'), vh = window.innerHeight, R = [];
  const clipOf = el => { let r = el.getBoundingClientRect(); let L = r.left, T = r.top, Rr = r.right, B = r.bottom;
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) { const cs = getComputedStyle(p);
      if (cs.overflowX !== 'visible' || cs.overflowY !== 'visible') { const q = p.getBoundingClientRect(); L = Math.max(L, q.left); T = Math.max(T, q.top); Rr = Math.min(Rr, q.right); B = Math.min(B, q.bottom); } }
    return {left: L, top: T, right: Rr, bottom: B}; };
  const pims = [...m.querySelectorAll('.pim')].map(p => [p, clipOf(p)]).filter(([p, r]) => r.right - r.left > 4 && r.bottom - r.top > 4 && r.bottom > 0 && r.top < vh);
  const name = p => { const i = p.querySelector('img'); return i ? (i.getAttribute('data-full') || i.getAttribute('src') || '').split('/').pop() : '?'; };
  const ov = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT), rg = document.createRange(); let n;
  while ((n = w.nextNode())) { if (!n.nodeValue.trim()) continue; const pe = n.parentElement; if (!pe || pe.closest('figcaption,script,style,.mm-dots')) continue;
    rg.selectNodeContents(n); for (const q of rg.getClientRects()) { if (q.width <= 2 || q.height <= 2 || q.bottom < 0 || q.top > vh) continue;
      for (const [p, r] of pims) if (ov(q, r)) R.push('text "' + n.nodeValue.trim().slice(0, 30) + '" over photo ' + name(p)); } }
  for (let i = 0; i < pims.length; i++) for (let j = i + 1; j < pims.length; j++) if (ov(pims[i][1], pims[j][1])) R.push('photo ' + name(pims[i][0]) + ' over photo ' + name(pims[j][0]));
  return R; }"""

async def late(b, base, w):
    ctx, pg = await new_page(b, w, late=True)
    await pg.goto(base, wait_until='domcontentloaded', timeout=120000); await pg.wait_for_timeout(1500)
    await pg.evaluate("""() => { window.__ls = []; new PerformanceObserver(l => { for (const e of l.getEntries()) { if (e.hadRecentInput) continue;
        window.__ls.push({t: Math.round(performance.now()), v: e.value, y: scrollY, src: (e.sources || []).map(s => { const nd = s.node && s.node.nodeType === 1 ? s.node : (s.node ? s.node.parentElement : null);
          return [nd ? (nd.tagName + (nd.className && typeof nd.className === 'string' ? '.' + nd.className.split(' ')[0] : '') + ' "' + (nd.textContent || '').trim().slice(0, 30) + '"') : '?', Math.round(s.previousRect.top), Math.round(s.currentRect.top), Math.round(s.previousRect.height), Math.round(s.currentRect.height)]; })}); } }).observe({type: 'layout-shift', buffered: false}); }""")
    H = await pg.evaluate('document.documentElement.scrollHeight')
    seen = {}; steps = 0; t0 = time.time()
    y = 0
    while y < H + 900:
        await pg.mouse.wheel(0, 400); await pg.wait_for_timeout(150); y += 400; steps += 1
        loading = await pg.evaluate('[...document.querySelectorAll("main img")].filter(i => !i.complete).length')
        for x in await pg.evaluate(JS_OVER):
            if x not in seen:
                seen[x] = (await pg.evaluate('scrollY'), loading)
                fn = await shot(pg, 'E049 %d %s' % (w, x))
                fault('%d E049: while scrolling (window at %d px, %d images still loading): %s%s' % (w, seen[x][0], loading, x, ('  screenshot: ' + fn) if fn else ''))
        H = await pg.evaluate('document.documentElement.scrollHeight')
    for _ in range(60):
        if await pg.evaluate('[...document.images].every(i => i.complete)'): break
        await pg.wait_for_timeout(250)
    await pg.wait_for_timeout(1500)
    for x in await pg.evaluate(JS_OVER):
        if x not in seen: fault('%d E049: after the images arrived (window at the end): %s' % (w, x)); seen[x] = 1
    ls = await pg.evaluate('window.__ls')
    big = [e for e in ls if e['v'] >= 0.001]
    for e in big:
        src = '; '.join('%s top %d->%d height %d->%d' % tuple(s) for s in e['src'][:3])
        fault('%d E049: layout shift %.4f while scrolling with images loading (window at %d px): %s' % (w, e['v'], e['y'], src))
    say('%d late images: %d scroll steps, %d overlaps, %d layout shifts (%d tiny ones under 0.001 ignored)' % (w, steps, len(seen), len(big), len(ls) - len(big)))
    await ctx.close()

# ---------------------------------------------------------------- 4 behaviour (E050) + 5 hero (A013)
async def behaviour(b, base, w):
    ctx, pg = await new_page(b, w)
    await pg.goto(base, wait_until='load', timeout=120000)
    # A013 hero: 0 s and 12 s after loading
    hero = await pg.evaluate("""() => { const h = document.querySelector('.hero'); if (!h) return null; const t = (h.querySelector('h1') || h).textContent.trim();
        const bg = getComputedStyle(h).backgroundImage, urls = (bg.match(/url\\(/g) || []).length;
        return {title: t, urls: urls, imgs: h.querySelectorAll('img').length, slides: h.querySelectorAll('.mm-hs').length + document.querySelectorAll('.hero .slide, .hero [data-slide]').length}; }""")
    he = await pg.query_selector('.hero')
    s0 = await he.screenshot() if he else None
    await settle(pg)
    if hero is None: fault('%d A013: no hero on the page' % w)
    else:
        rot_ok = re.fullmatch(r'(Play|Education)', hero['title'] or '') is not None
        n_img = hero['urls'] + hero['imgs'] + hero['slides']
        if not rot_ok and n_img != 1: fault('%d A013: the hero has %d images (%d background, %d img, %d slides) on "%s", not Play or Education - one still image' % (w, n_img, hero['urls'], hero['imgs'], hero['slides'], hero['title']))
    await pg.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
    # viewer
    n0 = len(faults)
    grp = await pg.evaluate("""() => { const all = [...document.querySelectorAll('main img.doc-img')];
        const g = all.find(i => { const c = i.closest('.mm-imgs, .mm-pfig, .mm-trio'); return c && c.querySelectorAll('img.doc-img').length >= 2 && i === c.querySelector('img.doc-img'); });
        if (!g) return null; g.setAttribute('data-ib-first', '1'); const c = g.closest('.mm-imgs, .mm-pfig, .mm-trio'); const imgs = [...c.querySelectorAll('img.doc-img')];
        imgs[1].setAttribute('data-ib-second', '1'); return {n: imgs.length, full: imgs.map(i => i.getAttribute('data-full') || i.getAttribute('src'))}; }""")
    LB = """() => { const lb = document.getElementById('lightbox'), im = document.getElementById('lightbox-img'), c = document.getElementById('lb-counter');
        if (!lb) return null; const cs = getComputedStyle(lb), r = lb.getBoundingClientRect();
        return {open: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0, src: im ? (im.getAttribute('src') || '') : '', loaded: im ? im.complete && im.naturalWidth > 0 : false,
                counter: c && getComputedStyle(c).display !== 'none' ? c.textContent.trim() : '', iw: im ? im.getBoundingClientRect().width : 0}; }"""
    async def lbstate():
        for _ in range(20):
            s = await pg.evaluate(LB)
            if not s or not s['open'] or s['loaded']: return s
            await pg.wait_for_timeout(150)
        return s
    async def tap(el):   # a finger on phones (touchscreen at the element's centre), the mouse on computers
        await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(150)
        if w <= 830:
            bb = await el.bounding_box(); await pg.touchscreen.tap(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
        else: await el.click()
    async def press(sel):
        el = await pg.query_selector(sel)
        if not el: return False
        await tap(el); await pg.wait_for_timeout(400); return True
    if grp is None: say('%d viewer: no group of 2+ photos on the page - the viewer not tried on a group' % w)
    else:
        if not await press('img[data-ib-first]'): fault('%d E050: the first photo of a group could not be clicked' % w)
        s = await lbstate()
        if not s: fault('%d E050: the page has no image viewer (#lightbox)' % w)
        else:
            if not s['open']: fault('%d E050: clicking a photo did not open the image viewer' % w)
            else:
                if not s['src'].endswith(grp['full'][0]) or not s['loaded']: fault('%d E050: the viewer shows "%s" (loaded %s), not the photo\'s full-size file %s' % (w, s['src'], s['loaded'], grp['full'][0]))
                if s['counter'] != '1 / %d' % grp['n']: fault('%d E050: viewer counter "%s", not "1 / %d"' % (w, s['counter'], grp['n']))
                await press('#lb-next'); s = await lbstate()
                if not (s['open'] and s['src'].endswith(grp['full'][1]) and s['counter'] == '2 / %d' % grp['n']): fault('%d E050: next did not show photo 2 (shows "%s", counter "%s")' % (w, s['src'], s['counter']))
                top_el = await pg.evaluate("() => { const b = document.getElementById('lb-prev'); if (!b) return 'no button'; const r = b.getBoundingClientRect(), e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return e === b ? '' : (e ? (e.id || e.className || e.tagName) : 'nothing'); }")
                if top_el:
                    fn = await shot(pg, 'E050 viewer-prev-covered %d' % w)
                    if fn: say('  screenshot (before pressing previous): %s' % fn)
                await press('#lb-prev'); s = await lbstate()
                if not (s['open'] and s['src'].endswith(grp['full'][0]) and s['counter'] == '1 / %d' % grp['n']):
                    fault('%d E050: previous did not go back to photo 1 (viewer %s, shows "%s", counter "%s")%s' % (w, 'open' if s['open'] else 'closed', s['src'], s['counter'], (' - the previous button is covered by #%s, which takes the tap' % top_el) if top_el else ''))
                    if not s['open']: await press('img[data-ib-first]'); await press('#lb-next')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300); s = await pg.evaluate(LB)
                if s['open']: fault('%d E050: Escape did not close the viewer' % w)
                await press('img[data-ib-second]'); s = await lbstate()
                if not (s['open'] and s['src'].endswith(grp['full'][1])): fault('%d E050: clicking photo 2 did not open it in the viewer' % w)
                else:
                    vp = pg.viewport_size
                    if w <= 830: await pg.touchscreen.tap(8, vp['height'] / 2)
                    else: await pg.mouse.click(8, vp['height'] / 2)
                    await pg.wait_for_timeout(400); s = await pg.evaluate(LB)
                    if s['open']: fault('%d E050: a click on the dark backdrop did not close the viewer' % w)
        if len(faults) > n0:
            fn = await shot(pg, 'E050 viewer %d' % w)
            if fn: say('  screenshot: %s' % fn)
    # contents links
    links = await pg.evaluate("""() => [...document.querySelectorAll('.toc a[href^="#"], nav.toc a[href^="#"]')].filter((a, i, all) => all.indexOf(a) === i).map(a => [a.getAttribute('href'), a.textContent.trim().slice(0, 40)])""")
    nl = 0; n1 = len(faults)
    for href, txt in links:
        await pg.evaluate('window.scrollTo({top: 0, behavior: "instant"})'); await pg.wait_for_timeout(150)
        a = await pg.query_selector('.toc a[href="%s"]' % href.replace('"', '\\"'))
        if not a: continue
        vis = await a.is_visible()
        if not vis: fault('%d E050: contents link "%s" is not visible to click' % (w, txt)); continue
        await tap(a)
        same = 0; prev = None
        for _ in range(50):
            cur = await pg.evaluate('scrollY')
            same = same + 1 if cur == prev else 0
            if same >= 3: break
            prev = cur; await pg.wait_for_timeout(120)
        r = await pg.evaluate("""(id) => { let h = document.getElementById(decodeURIComponent(id)); if (!h) return null; if (!/^H[1-6]$/.test(h.tagName)) h = h.querySelector('h1,h2,h3,h4') || h; const r = h.getBoundingClientRect();
            const sh = document.querySelector('.site-head'), sr = sh ? sh.getBoundingClientRect() : null, sp = sh ? getComputedStyle(sh).position : '';
            const cover = sh && (sp === 'sticky' || sp === 'fixed') && sr.bottom > r.top + 1 && sr.top <= r.top ? sr.bottom - r.top : 0;
            const end = scrollY >= document.documentElement.scrollHeight - innerHeight - 1;
            // where the template lands a heading: its html scroll-padding-top (Essay template line 21: 76 px; line 123: 64 px on phones), under the sticky header
            const under = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
            // the heading's letters (not its box) hidden under the sticky header
            const rg = document.createRange(); rg.selectNodeContents(h); const ink = [...rg.getClientRects()].filter(q => q.width > 1 && q.height > 1);
            const it = ink.length ? Math.min(...ink.map(q => q.top)) : r.top;
            const hid = sh && (sp === 'sticky' || sp === 'fixed') && sr.bottom > it + 0.5 ? sr.bottom - it : 0;
            return {top: +r.top.toFixed(1), under: +under.toFixed(1), cover: +hid.toFixed(1), end: end, tag: h.tagName, text: h.textContent.trim().slice(0, 40)}; }""", href[1:])
        nl += 1
        if r is None: fault('%d E050: contents link "%s" points at %s, which is not on the page' % (w, txt, href)); continue
        if not (abs(r['top'] - r['under']) <= 3 or (r['end'] and r['top'] > r['under'])):
            fault('%d E050: contents link "%s": its heading "%s" stands %.1f px from the top of the window, not at the template\'s %.1f (html scroll-padding-top, under the header)' % (w, txt, r['text'], r['top'], r['under']))
        if r['cover'] > 0:
            fault('%d E050: contents link "%s": the letters of its heading "%s" are under the sticky header (%.1f px hidden)' % (w, txt, r['text'], r['cover']))
    if len(faults) > n1:
        fn = await shot(pg, 'E050 contents %d' % w)
        if fn: say('  screenshot (the last link tried): %s' % fn)
    # hover (computers)
    nh = 0
    if w >= 831:
        await pg.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
        tops = await pg.query_selector_all('#site-nav .top')
        for t in tops[:12]:
            try:
                await t.hover(); await pg.wait_for_timeout(250); nh += 1
                if await pg.evaluate('[...document.querySelectorAll(".panel")].some(p => { const r = p.getBoundingClientRect(), c = getComputedStyle(p); return r.height > 20 && c.display !== "none" && c.visibility !== "hidden" && c.opacity !== "0"; })'):
                    fault('%d E050: hovering the menu name "%s" opens its panel' % (w, (await t.text_content()).strip()))
            except Exception: pass
        await pg.mouse.move(1, 1)
        imgs = await pg.query_selector_all('main img.doc-img')
        for im in imgs[:: max(1, len(imgs) // 12)][:12]:
            try:
                await im.scroll_into_view_if_needed(); await pg.mouse.move(1, 1); await pg.wait_for_timeout(100)
                b0 = await im.bounding_box(); await im.hover(); await pg.wait_for_timeout(350); b1 = await im.bounding_box(); nh += 1
                if b0 and b1 and max(abs(b0[k] - b1[k]) for k in b0) > 0.5:
                    fault('%d E050: photo %s moves or changes size under the pointer (%s -> %s)' % (w, (await im.get_attribute('data-full') or '').split('/')[-1], {k: round(v) for k, v in b0.items()}, {k: round(v) for k, v in b1.items()}))
            except Exception: pass
        await pg.mouse.move(1, 1)
    # A013: pixels at 12 s
    if he is not None and s0 is not None:
        await pg.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
        el = await pg.query_selector('.hero')
        rest = HERO_T - 0
        await pg.wait_for_timeout(1000 * HERO_T)   # the time already spent above is extra; the hero must stay still throughout
        s1 = await el.screenshot()
        if s0 != s1:
            from PIL import Image, ImageChops
            a, c = Image.open(io.BytesIO(s0)).convert('RGB'), Image.open(io.BytesIO(s1)).convert('RGB')
            if a.size != c.size: fault('%d A013: the hero changed size between loading and 12 s later (%s -> %s)' % (w, a.size, c.size))
            else:
                bbox = ImageChops.difference(a, c).point(lambda v: 255 if v > 24 else 0).getbbox()
                if bbox and hero and not re.fullmatch(r'(Play|Education)', hero['title'] or ''):
                    fn = os.path.join(SHOTS, 'A013_hero_%d_12s.png' % w); c.save(fn)
                    fault('%d A013: the hero picture changed between loading and 12 s later (area %s)  screenshot: %s' % (w, bbox, fn))
    say('%d behaviour: viewer %s, %d contents links, %d hovers, hero checked at 0 s and %d s' % (w, 'tried' if grp else 'not tried', nl, nh, HERO_T))
    if pg._errs: fault('%d: script errors on the page: %s' % (w, ' | '.join(pg._errs[:3])))
    await ctx.close()

async def main():
    from playwright.async_api import async_playwright
    srv, port = serve(FOLDER)
    base = 'http://127.0.0.1:%d/index.html' % port
    say('images_behaviour.py %s  widths: %s%s' % (FOLDER, 'the 122 widths' if ARG == 'full' else ','.join(map(str, WIDTHS)), ' (the band edges only - default; pass "full" for the 122 widths)' if not ARG else ''))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if PARTS != {'heights', 'swipe', 'late', 'behaviour'}: say('PARTS RUN: %s only (a proof run - not a full check)' % ','.join(sorted(PARTS)))
        say('== 1 heights (D142, D143, D205, D213) and fitting rows (A035)')
        for w in (WIDTHS if 'heights' in PARTS else []):
            try: await heights(b, base, w)
            except Exception as e: fault('%d: heights could not be measured: %s' % (w, str(e)[:200]))
        say('== 2 swipe (A034, E025, A035) at %s' % ','.join(map(str, SWIPE_W)))
        for w in (SWIPE_W if 'swipe' in PARTS else []):
            try: await swipes(b, base, w)
            except Exception as e: fault('%d: swipe could not be tried: %s' % (w, str(e)[:200]))
        say('== 3 late-loading images (E049) at %s, images held back %d s' % (','.join(map(str, LATE_W)), DELAY))
        for w in (LATE_W if 'late' in PARTS else []):
            try: await late(b, base, w)
            except Exception as e: fault('%d: late images could not be tried: %s' % (w, str(e)[:200]))
        say('== 4-5 viewer, contents links, hover (E050) and hero (A013) at %s' % ','.join(map(str, BEHAV_W)))
        for w in (BEHAV_W if 'behaviour' in PARTS else []):
            try: await behaviour(b, base, w)
            except Exception as e: fault('%d: behaviour could not be tried: %s' % (w, str(e)[:200]))
        await b.close()
    srv.shutdown()
    say('IMAGES PASS' if not faults else 'IMAGES FAULT (%d)' % len(faults))
    say('END')
    with open(OUT, 'w') as f: f.write('\n'.join(lines_out) + '\n')
    sys.exit(0 if not faults else 1)

asyncio.run(main())
