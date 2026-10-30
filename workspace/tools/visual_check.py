#!/usr/bin/env python3
"""Step 9, the one on-screen check every agent runs, unedited (27 Oct 2026; checks-v2: same checks as v1, faster - overlaps found by sorting, one browser setup per kind of screen, shorter fixed waits).
usage: python3 visual_check.py <finished package .zip>   or, after upload:   python3 visual_check.py https://montessorimentor.co.uk/<slug>/
Unpacks the zip, serves it locally, opens it in Chromium at every width and prints one line per width per check.
A width passes only if every check on its line reads 0 / none / ok.
Squeezed text: at 641 and wider, a paragraph of more than 60 characters narrower than max(260, 0.35 x the text column) - the templates' own narrow-column limit (Essay line 878, Resources line 914). Enlarged: an image shown more than 20% wider than its file. Oversized: at 641 and wider, an image taller than 200 px (the templates' own image sizes stop at 170: Essay ROW 170 and STD 153, line 836; Resources ROW 168, line 873) unless its set has its own data-h."""
import sys, os, zipfile, tempfile, threading, http.server, functools, asyncio, json
from playwright.async_api import async_playwright
Z = sys.argv[1]
if Z.startswith('https://'):   # after the owner's upload: the live page itself, as Hostinger serves it
    URL = Z
else:
    tmp = tempfile.mkdtemp(prefix='vc-'); zipfile.ZipFile(Z).extractall(tmp)
    import atexit, shutil; atexit.register(shutil.rmtree, tmp, True)   # v7: the unpacked copy is deleted when the check ends (copies filled the disk on 27 Oct)
    idx = [os.path.join(r, 'index.html') for r, d, f in os.walk(tmp) if 'index.html' in f]; assert len(idx) == 1
    root = os.path.dirname(os.path.dirname(idx[0])); slug = os.path.basename(os.path.dirname(idx[0]))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
if not Z.startswith('https://'):
    H = functools.partial(Q, directory=root)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    URL = 'http://127.0.0.1:%d/%s/' % (srv.server_address[1], slug)
WIDTHS = sorted(set(list(range(320, 1441, 10)) + [640, 641, 830, 831, 960, 961, 1023, 1024, 1099, 1100, 1180, 1181, 1279, 1280, 1920]))   # v6: every breakpoint in both templates (640/641, 830/831, 960/961, 1023, 1099, 1180, 1279) and its neighbour
MENU_W = {320, 640, 641, 830, 831, 960, 961, 1023, 1024, 1099, 1100, 1180, 1181, 1279, 1280, 1440, 1920}   # v6: the menu is tested at both edges of every layout band; inside a band its code and styles are the same
if len(sys.argv) > 2: WIDTHS = [int(x) for x in sys.argv[2].split(',')]   # only for a quick look; the report needs the full run
JS = r"""async () => {
 const __S = new Map();   // checks-v5: the same rules as v4, each element's ancestors worked out once and remembered (v4 re-read every ancestor for every element)
 const __st = e => { if (__S.has(e)) return __S.get(e); const p = e.parentElement; let v;
   if (!p || p === document.documentElement) v = {L: -Infinity, T: -Infinity, R: Infinity, B: Infinity};
   else { const up = __st(p); if (up === null) v = null; else { const s = getComputedStyle(p);
     if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') v = null;
     else if (p.tagName === 'DETAILS' && !p.open && !(e.tagName === 'SUMMARY' && e.parentElement === p)) v = null;
     else if (/(hidden|clip)/.test(s.overflow + s.overflowX + s.overflowY)) { const q = p.getBoundingClientRect(); v = {L: Math.max(up.L, q.left), T: Math.max(up.T, q.top), R: Math.min(up.R, q.right), B: Math.min(up.B, q.bottom)}; if (v.R - v.L < 1 || v.B - v.T < 1) v = null; }
     else v = up; } }
   __S.set(e, v); return v; };
 const clipRect = e => { const c = __st(e); if (c === null) return null; const r = e.getBoundingClientRect(); const L = Math.max(r.left, c.L), T = Math.max(r.top, c.T), Rr = Math.min(r.right, c.R), B = Math.min(r.bottom, c.B);
   if ((c.R !== Infinity || c.L !== -Infinity || c.T !== -Infinity || c.B !== Infinity) && (Rr - L < 1 || B - T < 1)) return null; return {left: L, top: T, right: Rr, bottom: B, width: Rr - L, height: B - T}; };
 const R = e => e.getBoundingClientRect(), vis = e => { const s = getComputedStyle(e), r = R(e); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0 && clipRect(e) !== null; };
 const main = document.querySelector('main#content');
 const texts = [...main.querySelectorAll('*')].filter(e => !e.closest('script,style') && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())).filter(vis);   // every element that holds text of its own (13:4x: was a fixed list that missed div.mm-line and similar)
 const imgs = [...document.querySelectorAll('main#content img')].filter(vis);
 const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
 const lineRects = e => { const r = document.createRange(), out = []; const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) { if (!n.nodeValue.trim()) continue; r.selectNodeContents(n); const c = clipRect(e); for (const q of r.getClientRects()) if (q.width > 1 && c && q.right > c.left && q.left < c.right && q.bottom > c.top && q.top < c.bottom) out.push(q); } return out; };
 const tl = texts.map(e => [e, lineRects(e)]);
 let tt = [], ti = [], ii = [], fo = [];
 const bb = rs => rs.reduce((u, q) => ({left: Math.min(u.left, q.left), top: Math.min(u.top, q.top), right: Math.max(u.right, q.right), bottom: Math.max(u.bottom, q.bottom)}), {left: 1e9, top: 1e9, right: -1e9, bottom: -1e9});
 const tb = tl.filter(x => x[1].length).map(x => [x[0], x[1], bb(x[1])]).sort((a, b) => a[2].top - b[2].top);
 for (let i = 0; i < tb.length; i++) { const [a, ra, A] = tb[i]; for (let j = i + 1; j < tb.length && tb[j][2].top < A.bottom; j++) { const [b, rb, B] = tb[j]; if (inter(A, B) <= 4 || a.contains(b) || b.contains(a)) continue;
   let hit = false; for (const x of ra) { for (const y of rb) if (inter(x, y) > 4) { hit = true; break; } if (hit) break; } if (hit) tt.push((a.textContent.trim().slice(0, 30)) + ' / ' + (b.textContent.trim().slice(0, 30))); } }
 const iq = imgs.map(im => [im, clipRect(im) || R(im)]); for (const [a, ra] of tl) { if (!ra.length) continue; const A = bb(ra); for (const [im, q] of iq) { if (inter(A, q) <= 4) continue; for (const x of ra) if (inter(x, q) > 4) { ti.push(a.textContent.trim().slice(0, 30) + ' / ' + (im.getAttribute('src') || '')); break; } } }
 const ib = imgs.map(i => [i, R(i)]).sort((a, b) => a[1].top - b[1].top);
 for (let i = 0; i < ib.length; i++) for (let j = i + 1; j < ib.length && ib[j][1].top < ib[i][1].bottom; j++) if (inter(ib[i][1], ib[j][1]) > 4) ii.push(ib[i][0].getAttribute('src') + ' / ' + ib[j][0].getAttribute('src'));
 const band = document.querySelector('.mc-band, footer'); if (band) { const b = R(band); for (const im of imgs) if (inter(R(im), b) > 4) fo.push(im.getAttribute('src')); }
 const bad = [...document.images].filter(i => i.closest('main#content, .hero') && (!i.complete || i.naturalWidth === 0)).map(i => i.getAttribute('src'));
 const hero = document.querySelector('.hero'); let heroOK = false;   // 14:5x: the hero must actually load, not just be named (it read "ok" on pages whose hero.jpg was 404)
 if (hero) { const m = /url\(["']?([^"')]+)/.exec(getComputedStyle(hero).backgroundImage || ''); if (m && /hero\.jpg/.test(m[1])) { heroOK = await new Promise(r => { const i = new Image(); i.onload = () => r(i.naturalWidth > 0); i.onerror = () => r(false); i.src = m[1]; setTimeout(() => r(false), 15000); }); } }
 const mw = R(main).width, sq = [], up = [];
 if (innerWidth > 640) for (const e of texts) { if (getComputedStyle(e).display.startsWith('inline')) continue; if (e.closest('td,th,li') && e.tagName !== 'LI') continue; const w = R(e).width; if (w < Math.max(260, 0.35 * mw) && e.textContent.trim().length > 60) sq.push(Math.round(w) + 'px: ' + e.textContent.trim().slice(0, 30)); }
 const big = [];
 if (innerWidth > 640) for (const im of imgs) { const q = R(im), set = im.closest('[data-h]'), cap = Math.max(200, set ? parseFloat(set.getAttribute('data-h')) + 2 : 0); if (q.height > cap) big.push((im.getAttribute('src') || '') + ' ' + Math.round(q.width) + 'x' + Math.round(q.height)); }
 for (const im of imgs) { const q = R(im); if (im.naturalWidth && q.width > im.naturalWidth * 1.2 + 1) up.push((im.getAttribute('src') || '') + ' shown ' + Math.round(q.width) + ' of ' + im.naturalWidth); }
 return {big: big.slice(0, 5), bign: big.length, sq: sq.slice(0, 5), sqn: sq.length, up: up.slice(0, 5), upn: up.length, sideways: document.documentElement.scrollWidth - innerWidth, tt: tt.slice(0, 5), ttn: tt.length, ti: ti.slice(0, 5), tin: ti.length, ii: ii.slice(0, 5), iin: ii.length, fo, bad, heroOK};
}"""
MENU = r"""async () => {
 const out = []; const btns = [...document.querySelectorAll('.menu .has-panel > .sub-toggle')];
 const vis = e => e && getComputedStyle(e).display !== 'none';
 const menuBtn = document.querySelector('.menu-toggle, .nav-toggle, button[aria-controls="menu"], .site-head button:not(.sub-toggle)');
 if (innerWidth <= 830 && menuBtn && !vis(document.querySelector('.menu .top'))) menuBtn.click();
 await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
 for (const b of btns) { const li = b.closest('.has-panel'), p = li.querySelector('.panel');
   b.click(); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); const o1 = vis(p);
   b.click(); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); const o2 = vis(p);
   if (!o1 || o2) out.push((li.querySelector('.top') || li).textContent.trim().slice(0, 20) + (o1 ? '' : ' did not open') + (o2 ? ' did not close' : '')); }
 return {panels: btns.length, faults: out};
}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); allok = True
        CTX = {True: await b.new_context(viewport={'width': 390, 'height': 900}, is_mobile=True, has_touch=True), False: await b.new_context(viewport={'width': 1280, 'height': 900})}
        for W in WIDTHS:
            ph = W <= 640
            ctx = CTX[ph]
            pg = await ctx.new_page(); await pg.set_viewport_size({'width': W, 'height': 900}); errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('requestfailed', lambda r: errs.append('failed ' + r.url))
            pg.on('response', lambda r: errs.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
            await pg.goto(URL, wait_until='load', timeout=60000)
            await pg.evaluate("async () => { [...document.images].forEach(i => { i.loading = 'eager'; }); scrollTo(0, document.documentElement.scrollHeight); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); scrollTo(0, 0); await document.fonts.ready; const seen = [...document.images].filter(i => { const s = getComputedStyle(i), q = i.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && q.width > 0 && q.height > 0; }); await Promise.race([Promise.all(seen.map(i => i.complete ? 0 : new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }))), new Promise(r => setTimeout(r, 20000))]); await new Promise(r => setTimeout(r, 500)); }")
            r = await pg.evaluate(JS); m = await pg.evaluate(MENU) if W in MENU_W else {'panels': 0, 'faults': ['not tested at this width: same layout band as its edges']}
            ok = not r['bign'] and not r['sqn'] and not r['upn'] and r['sideways'] <= 0 and not r['ttn'] and not r['tin'] and not r['iin'] and not r['fo'] and not r['bad'] and r['heroOK'] and not [f for f in m['faults'] if not f.startswith('not tested')] and not errs
            allok &= ok
            print('%4d %s oversized images %d %s | squeezed text %d %s | enlarged images %d %s | sideways %d | text over text %d %s | text over image %d %s | image over image %d %s | image over footer %d | images not loaded %d %s | hero %s | menu %d panels, faults %s | errors %d %s' % (
                W, 'ok  ' if ok else 'FAULT', r['bign'], r['big'] or '', r['sqn'], r['sq'] or '', r['upn'], r['up'] or '', max(0, r['sideways']), r['ttn'], r['tt'] or '', r['tin'], r['ti'] or '', r['iin'], r['ii'] or '', len(r['fo']), len(r['bad']), r['bad'][:3] or '', 'ok' if r['heroOK'] else 'MISSING', m['panels'], m['faults'] or 'none', len(errs), errs[:3] or ''))
            await pg.close()
        # narrowing an open window: 1280 -> 390
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); pg = await ctx.new_page(); await pg.goto(URL, wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.set_viewport_size({'width': 390, 'height': 900}); await pg.wait_for_timeout(1500)
        sw = await pg.evaluate('document.documentElement.scrollWidth - innerWidth'); print('1280 narrowed to 390: sideways %d' % max(0, sw)); allok &= sw <= 0
        await b.close()
    print('RESULT:', 'every width ok' if allok else 'FAULTS - see the lines marked FAULT')
asyncio.run(main())
