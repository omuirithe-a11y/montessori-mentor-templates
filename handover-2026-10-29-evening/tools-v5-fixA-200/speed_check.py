"""speed_check.py <package.zip | https://live page address/> [widths=1440,390]   (29 Oct 2026, after The Role of the Adult's slow clicks)
Checks that the page answers a click quickly. Every image download is delayed 0.7 s, to stand in for the internet.
At each width: load, wait 4 s, scroll top to bottom in 700 px steps with 1.2 s pauses, and record every stretch the page is busy
(the browser's own long-task report: any stretch over 50 ms when a click cannot be handled). Then, in a fresh window, click four
images spread through the page (a fifth, two fifths, three fifths, four fifths of the way) and time click -> enlarged image shown.
Pass, at every width: no busy stretch over 50 ms while scrolling, and every click shown within 1.0 s (0.7 s of it is the delay).
Figures measured 29 Oct on The Role of the Adult (same method): before fix A longest stretch 2,256-2,287 ms and clicks
2.0-4.4 s; after fix A no stretch at all and clicks 0.78-0.84 s. Prints one line per width and SPEED OK or SPEED FAULT."""
import sys, os, time, zipfile, tempfile, shutil, threading, http.server, functools, json
from playwright.sync_api import sync_playwright
Z = sys.argv[1]; WS = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '1440,390').split(',')]
BUSY_MAX, CLICK_MAX, DELAY = 50, 1.0, 0.7   # 50 ms: Google's definition of a long task, during which a click cannot be handled (web.dev/articles/optimize-long-tasks); 1.0 s: beyond 1 s users lose focus (web.dev/articles/rail) - the 0.7 s download delay counts inside it
if Z.startswith('https://'):   # v5: a live page - the real network instead of the 0.7 s delay (the limits stay the same)
    t = tempfile.mkdtemp(); URL = Z; DELAY = 0
else:
    t = tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(t); slug = sorted(os.listdir(t))[0]
    H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=t)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    URL = 'http://127.0.0.1:%d/%s/' % (srv.server_address[1], slug)
INIT = "(function reg(){if(!document.documentElement)return setTimeout(reg,0);window.__lt=[];try{new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(e.duration))).observe({type:'longtask'})}catch(e){}})();"
def route(r):
    if '/images/' in r.request.url: time.sleep(DELAY)
    r.continue_()
ok = True
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WS:
        c = b.new_context(viewport={'width': w, 'height': 900}); c.add_init_script(INIT); c.route('**/*', route); pg = c.new_page()
        pg.goto(URL, wait_until='load', timeout=120000); pg.wait_for_timeout(4000); pg.evaluate("()=>{window.__lt=[]}")
        for y in range(0, pg.evaluate("document.documentElement.scrollHeight"), 700): pg.mouse.wheel(0, 700); pg.wait_for_timeout(1200)
        pg.wait_for_timeout(3000); lt = pg.evaluate("window.__lt"); c.close()
        c = b.new_context(viewport={'width': w, 'height': 900}); c.route('**/*', route); pg = c.new_page()
        pg.goto(URL, wait_until='load', timeout=120000); pg.wait_for_timeout(3000)
        full = pg.evaluate("[...document.querySelectorAll('img.doc-img[data-full]')].map(i=>i.getAttribute('data-full'))")
        pick = [full[int(len(full) * k / 5)] for k in (1, 2, 3, 4)] if len(full) >= 5 else full
        clicks = {}
        for f in pick:
            im = pg.locator('img.doc-img[data-full="%s"]' % f).first; im.scroll_into_view_if_needed(); pg.wait_for_timeout(800); t0 = time.time()
            try:
                im.click(timeout=20000)
                pg.wait_for_function("(f)=>{const i=document.getElementById('lightbox-img');return i&&i.getAttribute('src')===f&&i.complete&&i.naturalWidth>0}", arg=f, timeout=20000)
                clicks[f.split('/')[-1]] = round(time.time() - t0, 2)
            except Exception: clicks[f.split('/')[-1]] = 'did not open'
            pg.evaluate("()=>{const l=document.getElementById('lightbox');if(l)l.classList.remove('open')}"); pg.wait_for_timeout(400)
        c.close()
        # v6 (2 Nov 2026, owner 08:59: "I agree to change the speed check so that a page with no images is judged on its busy time alone,
        # on every page checked with it, starting with 8.0 Resources."): a page with no image to open (no img.doc-img[data-full]) has no
        # clicks to time, so it is judged on the busy stretches alone; a page WITH images still needs every click timed and within the limit
        longest = round(max(lt or [0])); noimg = len(full) == 0
        wok = longest <= BUSY_MAX and (noimg or (all(isinstance(v, float) and v <= CLICK_MAX for v in clicks.values()) and len(clicks) > 0))
        if noimg: print('%d  no images on the page - judged on busy time alone (owner 2 Nov 08:59)' % w, flush=True)
        ok = ok and wok
        print('%d %s  longest busy stretch %d ms (limit %d), busy stretches %d, total %d ms | clicks %s (limit %.1f s)' % (w, 'ok' if wok else 'FAULT', longest, BUSY_MAX, len(lt), round(sum(lt)), json.dumps(clicks), CLICK_MAX), flush=True)
    b.close()
shutil.rmtree(t, True); print('SPEED OK' if ok else 'SPEED FAULT'); sys.exit(0 if ok else 1)
