"""Check a page (20 Oct 2026): a built preview folder or a live address.

  python3 tools/check_page.py build/staff/preview          (or https://montessorimentor.co.uk/staff/)

At 1280, 768 and 390: browser errors, sideways scroll, hero to first letters, every beige line's space above and below
(letters to letters), last letters to the blue footer band, the strip under the band, text alignment, the menu panels
(open on the first click, close on the second), photos loaded. Writes <folder>/check-<width>.png full-page screenshots.
Prints one line per width; anything outside the settled figures is marked  <<."""
import asyncio, sys, os
from playwright.async_api import async_playwright
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
target = sys.argv[1]
RES = '--resources' in sys.argv
PG = next((tuple(float(x) for x in a.split('=')[1].split(',')) for a in sys.argv if a.startswith('--phone-gaps=')), None)   # 20 Oct: a page's own phone gaps (5.4: 41,34)   # Resources pages: figures settled 20 Oct (hero 60, lines 30/30, footer 60, strip 60; phones as built)
url = target if target.startswith('http') else 'file://' + os.path.abspath(os.path.join(target, 'index.html'))
shots = target if not target.startswith('http') else '/tmp'
bg = lambda c: abs(c[0] - c[1]) < 12 and c[0] > 225 and c[2] > 205
rule = lambda c: abs(c[0] - 0xD9) < 10 and abs(c[1] - 0xC9) < 10 and abs(c[2] - 0xAB) < 12

async def one(b, w):
    _o = []   # 21 Oct: the three widths run at once; each returns its lines, printed in order
    pg = await b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:80]))
    await pg.goto(url, wait_until='load')
    await pg.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i=>i.loading="eager")')
    await pg.wait_for_timeout(4500)
    # 20 Oct 22:5x: the window is made as tall as the page BEFORE measuring, so the full-page screenshot does not re-lay the
    # page after the positions are read (the old order gave false readings: 26.5/35 for lines that are 30.5/30)
    hh = await pg.evaluate('document.documentElement.scrollHeight'); await pg.set_viewport_size({'width': w, 'height': hh}); await pg.wait_for_timeout(2500)
    g = await pg.evaluate('''(()=>{const m=document.querySelector("main"),p=m.querySelector("p")||m,mr=p.getBoundingClientRect(),
      hero=document.querySelector(".hero"),band=document.querySelector(".mc-band"),foot=document.querySelector(".site-foot");
      return {L:mr.left,R:mr.right,hero:hero?hero.getBoundingClientRect().bottom+scrollY:null,band:band?band.getBoundingClientRect().top+scrollY:null,
       strip:foot?foot.getBoundingClientRect().height:null,side:document.documentElement.scrollWidth>innerWidth,
       /* 22 Oct 2026 (5.5, user 10:55 "switch them to exactly 30/30 letters to letters", 10:56 "only the letters"): a line marked
          data-rule-gap is measured letters to letters - from the baseline of the last line above to the line, and from the line to
          the top of the capitals below (check U's measure); an underline or a descender is not a letter's edge */
       rlet:(()=>{const cv=document.createElement("canvas").getContext("2d"),met=el=>{const s=getComputedStyle(el);cv.font=s.fontStyle+" "+s.fontWeight+" "+s.fontSize+" "+s.fontFamily;const t=cv.measureText("H");return [t.fontBoundingBoxAscent,t.fontBoundingBoxDescent,t.actualBoundingBoxAscent]};
         const ok=n=>{const e=n.parentElement;return n.nodeValue.trim()&&e&&!e.closest("script,style,a.pdf,.mm-float,figure")&&e.getClientRects().length};
         const ln=(n,last)=>{const r=document.createRange();r.selectNodeContents(n);const qs=[...r.getClientRects()].filter(q=>q.height>=5&&q.width>=1);if(!qs.length)return null;const q=last?qs[qs.length-1]:qs[0],k=met(n.parentElement),b=(q.top+q.bottom)/2+(k[0]-k[1])/2;return {b,t:b-k[2]}};
         const all=[];const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode())if(ok(n))all.push(n);
         return [...m.querySelectorAll("[data-rule-gap]")].filter(r=>r.getBoundingClientRect().width>200).map(r=>{const q=r.getBoundingClientRect();let a=null,b=null;
           for(const x of all){if(r.compareDocumentPosition(x)&Node.DOCUMENT_POSITION_PRECEDING){const l=ln(x,true);if(l)a=a===null?l.b:Math.max(a,l.b)}else if(b===null){const l=ln(x,false);if(l)b=l.t}}
           return [a===null?null:Math.round((q.top-a)*10)/10,b===null?null:Math.round((b-q.bottom)*10)/10]})})(),
       rules:[...m.querySelectorAll(".beige-rule,p.mm-gl")].filter(r=>r.getBoundingClientRect().width>200).map(r=>{const q=r.getBoundingClientRect();return [q.top+scrollY,q.bottom+scrollY]}),
       notj:[...m.querySelectorAll("p,li")].filter(p=>p.textContent.trim().length>90&&!p.querySelector("p,li")&&!p.closest("blockquote,figure,[class*=mm-left]")&&getComputedStyle(p).textAlign!=="justify").length,
       left:[...m.querySelectorAll("[class*=mm-left]")].map(e=>getComputedStyle(e).textAlign).join("/"),
       imgs:[...m.querySelectorAll("img")].filter(i=>!(i.complete&&i.naturalWidth)).length,
       endsPhoto:(()=>{let ib=-1e9,tb=-1e9;m.querySelectorAll("img").forEach(i=>{const r=i.getBoundingClientRect();if(r.height>4)ib=Math.max(ib,r.bottom);});const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT),rg=document.createRange();let n;while((n=w.nextNode())){if(!n.nodeValue.trim())continue;rg.selectNodeContents(n);for(const q of rg.getClientRects())if(q.width)tb=Math.max(tb,q.bottom);}return ib>tb;})()}})()''')
    path = os.path.join(shots, 'check-%d.png' % w)
    # 22 Oct 2026 (5.5 at 1280: a 2560x30954 screenshot came back blank below the menu bar - Chromium's largest picture): a tall
    # page is taken in parts of 6000 px and joined, so every page is seen whole
    _H = await pg.evaluate('document.documentElement.scrollHeight')
    if _H * w * 4 <= 6.0e7:
        await pg.screenshot(path=path, full_page=True, timeout=180000)   # 21 Oct: widths run at once; under load 30 s was too short
    else:
        _parts = []
        for _y in range(0, _H, 6000):
            _pp = path + '.%d.png' % _y
            await pg.screenshot(path=_pp, full_page=True, clip={'x': 0, 'y': _y, 'width': w, 'height': min(6000, _H - _y)}, timeout=180000)
            _parts.append(_pp)
        _ims = [Image.open(x_).convert('RGB') for x_ in _parts]
        _all = Image.new('RGB', (_ims[0].width, sum(x_.height for x_ in _ims)))
        _yy = 0
        for x_ in _ims: _all.paste(x_, (0, _yy)); _yy += x_.height
        _all.save(path)
        for x_ in _parts: os.remove(x_)
    im = Image.open(path).convert('RGB'); H = im.height
    x0, x1 = int(g['L'] * 2), int(g['R'] * 2)
    ink = lambda y: any(not bg(im.getpixel((x, y))) and not rule(im.getpixel((x, y))) for x in range(x0, x1, 2))
    def up(y):
        y0 = y
        while y > 0 and not ink(y): y -= 1
        return (y0 - y) / 2
    def down(y):
        y0 = y
        while y < H - 1 and not ink(y): y += 1
        return (y - y0) / 2
    hero = down(int(g['hero'] * 2) + 2) if g['hero'] else None
    # 20 Oct 22:5x: lines and the footer band found in the screenshot itself (positions read from the page could be out of
    # date by the time the screenshot was taken)
    full = lambda y: sum(1 for x in range(x0, x1, 20) if rule(im.getpixel((x, y)))) > 0.8 * len(range(x0, x1, 20))
    rows = [y for y in range(int(g['hero'] * 2) if g['hero'] else 0, H) if full(y)]
    grp = []
    for y in rows:
        if grp and y - grp[-1][-1] <= 2: grp[-1].append(y)
        else: grp.append([y])
    rl = [(up(gg[0] - 1), down(gg[-1] + 1)) for gg in grp]
    if g.get('rlet') and len(g['rlet']) == len(rl): rl = [tuple(x) for x in g['rlet']]   # 22 Oct 2026: lines the page marks letters to letters are measured so (the screenshot still finds every line, and the counts must agree)
    navy = lambda c: abs(c[0] - 0x1E) < 14 and abs(c[1] - 0x4D) < 14 and abs(c[2] - 0x7B) < 14
    nrows = [y for y in range(H) if navy(im.getpixel((6, y)))]
    band = None
    if nrows:
        bt_ = nrows[-1]
        while bt_ - 1 in nrows: bt_ -= 1
        band = up(bt_ - 1)
    off = lambda v, want: '' if (not RES) or v is None or abs(v - want) <= 1.5 else ' <<'
    # 21 Oct 13:4x (user's rule: phones take the mean of the live pages): last letters to the footer band 35.2 - the mean of 17 live
    # pages that end in text, measured at 390 with this method (was 38, no source recorded)
    want_hero, want_band = (PG if PG else (42, 35.2)) if w <= 640 else (60, 60)
    # 21 Oct 13:56 (user: "choose the option that works"): on phones a page that ends in a photo keeps the template's own 40
    # from the photo to the band (the Resources template's footer script: "phones keep 40"); 35.2 is for pages that end in text
    if w <= 640 and not PG and g.get('endsPhoto'): want_band = 40
    _o.append('%d  errors:%s  sideways:%s  hero gap %.1f%s  lines %s%s  footer gap %.1f%s  strip %.1f  not justified:%d%s  photos not loaded:%d' % (
        w, errs or 'none', g['side'], hero or 0, off(hero, want_hero), [(a, b) for a, b in rl],
        ' <<' if RES and any(abs(a - 30) > 1.5 or abs(b - 30) > 1.5 for a, b in rl) else '', band or 0, off(band, want_band), g['strip'] or 0, g['notj'], ('  set lines: ' + g['left']) if g['left'] else '', g['imgs']))   # 21 Oct: lists counted too; lines a setting left-aligns (LEFT_ALIGN) shown by their alignment
    # menu
    await pg.set_viewport_size({'width': w, 'height': 900}); await pg.wait_for_timeout(800)
    mb = pg.locator('.menu-btn')
    if await mb.is_visible(): await mb.click(); await pg.wait_for_timeout(300)
    bad = []
    for i in range(await pg.locator('.sub-toggle').count()):
        t = pg.locator('.sub-toggle').nth(i); pid = await t.get_attribute('aria-controls')
        vis = '(function(){var e=document.getElementById("%s");return e?getComputedStyle(e).display!=="none":null;})()' % pid   # 20 Oct 21:5x: a missing panel is a fault, not a crash
        await t.click(); await pg.wait_for_timeout(150); o = await pg.evaluate(vis)
        await t.click(); await pg.wait_for_timeout(150); c = await pg.evaluate(vis)
        if o is None: bad.append(pid + ' (panel missing)')
        elif not (o and not c): bad.append(pid)
    _o.append('     menu panels open/close: %s' % ('all 8 ok' if not bad else 'FAULT ' + str(bad)))
    await pg.close()
    return _o

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for lines in await asyncio.gather(*(one(b, w) for w in (1280, 768, 390))): print('\n'.join(lines))
        await b.close()
asyncio.run(main())
