"""block_compare.py <new zip> <previous build's zip> <out file>   (7 Nov 2026, owner "implement all of these changes", S3 refined)

Compares a build with the build before it, at the 13 key widths, so a fix's side effects are found in the fast round:
  - every block (p, li, h1-h4, blockquote, table, figure, img, .mm-set, .mm-row, .mm-float) is measured after the page has
    loaded, every image has finished loading and 4 s have passed: its width, height, and its gap to the block before it;
  - the new build is measured twice; a difference counts only when it is seen in both runs (layouts that differ from one load
    to the next are reported apart, not as faults);
  - blocks whose HTML changed between the two builds are found by the script (not named by the person running it); any
    OTHER block whose size or gap changed by more than 1 px is a FAULT;
  - inside the changed blocks, at every width: the line count, and on justified lines the largest word gap against the
    paragraph's median gap - a gap over 2x the median (and over 12 px) is a FAULT (b42's "sound:" line);
  - images: any image drawn under 0.6 of its size in the previous build where its block's HTML did not change is a FAULT.
The previous build's measurements are kept in <previous build>/checks2/blocks.json and reused.
Last lines: "BLOCKS OK" or "BLOCKS FAULT (n)", then END."""
import sys, os, json, zipfile, tempfile, asyncio, hashlib, threading, http.server, functools, statistics
from playwright.async_api import async_playwright
WIDTHS = [1440, 1279, 1180, 1099, 1023, 961, 960, 831, 830, 768, 641, 640, 390]
JS = r"""() => {
  const sel = 'main p, main li, main h1, main h2, main h3, main h4, main blockquote, main table, main figure, main img, main .mm-set, main .mm-row, main .mm-float';
  const els = [...document.querySelectorAll(sel)];
  const out = []; let prev = null;
  const hash = s => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h; };
  const seen = {};
  for (const e of els) {
    const r = e.getBoundingClientRect(); if (!r.width && !r.height) continue;
    const txt = (e.tagName === 'IMG' ? (e.getAttribute('src') || '') : (e.textContent || '').replace(/\s+/g, ' ').trim()).slice(0, 80);
    let key = e.tagName + ':' + txt; seen[key] = (seen[key] || 0) + 1; key += '#' + seen[key];
    const o = {k: key, w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top + scrollY), html: hash(e.outerHTML)};
    if (prev) o.gap = Math.round(r.top - prev.bottom);
    if (e.tagName === 'P' || e.tagName === 'LI') {
      const st = getComputedStyle(e);
      if (st.textAlign === 'justify') {
        const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n; const words = [];
        while ((n = w.nextNode())) { const re = /\S+/g; let m; while ((m = re.exec(n.nodeValue))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const rr = rg.getClientRects()[0]; if (rr) words.push([Math.round(rr.top), rr.left, rr.right]); } }
        const tabs = [...e.querySelectorAll('span.mm-t')].map(s => s.getBoundingClientRect());
        const lines = {}; for (const [t, l, rgt] of words) { const kk = Object.keys(lines).find(x => Math.abs(x - t) < 4); (lines[kk ?? t] = lines[kk ?? t] || []).push([l, rgt]); }
        const ls = Object.values(lines); const gaps = [];
        ls.forEach((L, i) => { if (i === ls.length - 1) return; L.sort((a, b) => a[0] - b[0]); for (let j = 1; j < L.length; j++) { const a0 = L[j - 1][1], a1 = L[j][0]; if (tabs.some(r => r.left < a1 && r.right > a0 - 1)) continue; gaps.push([i, a1 - a0]); } });
        o.lines = ls.length; o.gaps = gaps.map(g => [g[0], Math.round(g[1] * 10) / 10]);
      }
    }
    if (e.tagName === 'IMG') { o.iw = Math.round(r.width); o.ih = Math.round(r.height); }
    out.push(o); prev = r;
  }
  return out;
}"""
def unpack(z):
    t = tempfile.mkdtemp(prefix='blk-'); zipfile.ZipFile(z).extractall(t); slug = sorted(os.listdir(t))[0]; return t, slug
def serve(d):
    H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=d)
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=s.serve_forever, daemon=True).start(); return s
async def measure(z):
    root, slug = unpack(z); s = serve(root); url = 'http://127.0.0.1:%d/%s/' % (s.server_address[1], slug); res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        cx = await b.new_context(java_script_enabled=False); pg0 = await cx.new_page(); await pg0.goto(url)
        res['static'] = {o['k']: o['html'] for o in await pg0.evaluate(JS)}; await cx.close()
        for w in WIDTHS:
            pg = await b.new_page(viewport={'width': w, 'height': 900}); await pg.goto(url, wait_until='networkidle')
            await pg.evaluate("document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; })")   # all images load without scrolling (scrolling took 30 s a width)
            await pg.wait_for_function('[...document.images].every(i => i.complete)', timeout=30000)
            await pg.wait_for_timeout(4000)
            res[str(w)] = await pg.evaluate(JS); await pg.close()
        await b.close()
    s.shutdown(); return res
def main():
    import subprocess
    if subprocess.run(['bash', '/home/claude/mm/tools/roundlock.sh', 'check']).returncode != 0: sys.exit(3)   # S7
    new, old, out = sys.argv[1:4]
    pj = os.path.join(os.path.dirname(old), 'checks2', 'blocks.json'); osha = hashlib.sha256(open(old, 'rb').read()).hexdigest()
    prev = None
    if os.path.exists(pj):
        d = json.load(open(pj)); prev = d['m'] if d.get('sha') == osha else None
    if prev is None:
        prev = asyncio.run(measure(old)); os.makedirs(os.path.dirname(pj), exist_ok=True); json.dump({'sha': osha, 'm': prev}, open(pj, 'w'))
    a1 = asyncio.run(measure(new)); a2 = asyncio.run(measure(new))
    nj = os.path.join(os.path.dirname(new), 'checks2', 'blocks.json'); os.makedirs(os.path.dirname(nj), exist_ok=True)
    json.dump({'sha': hashlib.sha256(open(new, 'rb').read()).hexdigest(), 'm': a1}, open(nj, 'w'))
    faults, unsteady, changed_html = [], [], set()
    L = ['block_compare.py %s against %s' % (os.path.basename(os.path.dirname(new)), os.path.basename(os.path.dirname(old)))]
    for w in map(str, WIDTHS):
        P = {o['k']: o for o in prev[w]}; N1 = {o['k']: o for o in a1[w]}; N2 = {o['k']: o for o in a2[w]}
        prevkey = {a1[w][i]['k']: a1[w][i - 1]['k'] for i in range(1, len(a1[w]))}
        for k, n1 in N1.items():
            p = P.get(k); n2 = N2.get(k)
            ps, ns = prev.get('static', {}), a1.get('static', {})
            if k in ns and ps.get(k) != ns.get(k): changed_html.add(k)
        for k, n1 in N1.items():
            p = P.get(k); n2 = N2.get(k)
            if k in changed_html:
                for o in (n1,):
                    gs = [g for _, g in o.get('gaps', []) if g > 0]
                    if len(gs) >= 4:
                        med = statistics.median(gs); worst = max(o['gaps'], key=lambda x: x[1])
                        if worst[1] > 2 * med and worst[1] > 12:
                            n2g = max([g for _, g in (n2 or {}).get('gaps', [])] or [0])
                            if n2g > 2 * med: faults.append('FAULT %s %s: a justified line has a word gap of %.1f px (median %.1f) - line %d' % (w, k[:70], worst[1], med, worst[0] + 1))
                    if p and p.get('gaps') and o.get('gaps'):   # a justified line stretched against the same block in the build before
                        pm = max(g for _, g in p['gaps']); nm = max(g for _, g in o['gaps'])
                        n2m = max([g for _, g in (n2 or {}).get('gaps', [])] or [0])
                        if nm > 1.5 * pm and nm - pm > 3 and n2m > 1.5 * pm:
                            faults.append('FAULT %s %s: widest word gap %.1f px (build before: %.1f) - a justified line stretched' % (w, k[:70], nm, pm))
                    if p and o.get('lines') and p.get('lines') and o['lines'] != p['lines']:
                        L.append('INFO %s %s: lines %d -> %d (changed block)' % (w, k[:70], p['lines'], o['lines']))
                continue
            if p is None or n2 is None: continue
            if prevkey.get(k) in changed_html and 'gap' in p and 'gap' in n1:   # straight after a changed block: the spacing may move between gap and height
                if abs((n1['gap'] + n1['h']) - (p['gap'] + p['h'])) <= 1 and abs(n1['w'] - p['w']) <= 1: continue
            for f in ('w', 'h', 'gap'):
                if f in p and f in n1 and abs(n1[f] - p[f]) > 1:
                    same2 = f in n2 and abs(n2[f] - p[f]) > 1
                    msg = '%s %s: %s %s -> %s' % (w, k[:70], f, p[f], n1[f])
                    (faults if same2 else unsteady).append(('FAULT ' if same2 else 'UNSTEADY ') + msg + ('' if same2 else ' (not seen in the second run)'))
            if 'iw' in p and 'iw' in n1 and p['iw'] and n1['iw'] < 0.6 * p['iw'] and n2 and n2.get('iw', 0) < 0.6 * p['iw']:
                faults.append('FAULT %s %s: image drawn %dx%d, was %dx%d' % (w, k[:70], n1['iw'], n1['ih'], p['iw'], p['ih']))
    L.append('blocks whose HTML changed: %d (%s)' % (len(changed_html), '; '.join(sorted(changed_html))[:600]))
    L += sorted(set(faults)) + sorted(set(unsteady))[:200]
    L.append('BLOCKS OK' if not faults else 'BLOCKS FAULT (%d)' % len(set(faults))); L.append('END')
    open(out, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-30:]))
main()
