#!/usr/bin/env python3
"""col_check.py <pdf> <page folder with index.html> [width=1440] [PDF pages, e.g. 1,3 - for tests]  (5 Nov 2026, owner 04:59: "these lists go in two columns,
as in the PDF, using the template's two-column style"; plan agreed 05:48 - the column check)

For every PDF line that has text in two or three columns (left text starting in the left 30% of the page and other text
starting right of 40%), find each column's text on the built page at the given width and check that the columns stand
side by side there too: same line (tops within 0.6 of a line height) and in left-to-right order. A PDF row whose texts are
found on the page but one under the other is a COLUMN FAULT. Texts not found on the page are listed as NOT FOUND (a
fault too: the check cannot judge them). Prints one line per fault, then COLUMNS OK or COLUMNS FAULT (exit 0 only on OK)."""
import sys, re, asyncio, http.server, threading, functools, socket, unicodedata
import pymupdf
from playwright.async_api import async_playwright

PDF, FOLDER = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
PAGES = set(int(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 else None   # optional: PDF pages to check (tests)

def norm(s):  # (the page side strips every space; see JS)
    s = unicodedata.normalize('NFKC', s).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace(' ', ' ')
    return re.sub(r'\s+', ' ', s).strip().lower()

def pdf_rows():
    d = pymupdf.open(PDF); rows = []
    for pn in range(len(d)):
        if PAGES and pn + 1 not in PAGES: continue
        p = d[pn]; Wp = p.rect.width; lines = {}
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                # split a PDF line into cells where its spans stand more than 20 pt apart (tab stops, columns)
                cells, cur, x0, xe = [], '', None, None
                for sp in l['spans']:
                    if not sp['text'].strip():
                        continue
                    if cur and sp['bbox'][0] - xe > 20:
                        cells.append((x0, cur)); cur, x0 = '', None
                    if x0 is None: x0 = sp['bbox'][0]
                    cur += sp['text']; xe = sp['bbox'][2]
                if cur: cells.append((x0, cur))
                for cx, t in cells:
                    t = t.strip()
                    if len(norm(t)) < 4 or re.fullmatch(r'[\d.\-\s]+', t): continue   # dashes, list numbers
                    y = round(l['bbox'][1] / 3) * 3
                    lines.setdefault(y, []).append((cx, t))
        for y, v in sorted(lines.items()):
            v.sort()
            if len(v) >= 2 and v[0][0] < Wp * 0.3 and any(x > Wp * 0.4 for x, _ in v[1:]):
                rows.append((pn + 1, y, [t for _, t in v]))
    return rows

JS = r"""(args) => { const snips = args.snips, start = args.start;
  const m = document.body;   // the whole page: the contents box sits outside main
  const norm = s => s.normalize('NFKC').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/ /g,' ').replace(/\s+/g,'').toLowerCase();
  // the page's text with a map from character position back to text nodes
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT); let n, full = '', map = [];
  while ((n = w.nextNode())) { const v = n.nodeValue; for (let i = 0; i < v.length; i++) { const c = v[i].normalize('NFKC'); for (const ch of c) { map.push([n, i]); full += ch; } } map.push([null, 0]); full += ' '; }
  // normalise while keeping the map
  let nf = '', nm = [], prevSpace = true;
  for (let i = 0; i < full.length; i++) { let c = full[i].replace(/[‘’]/,"'").replace(/[“”]/,'"').replace(/[–—]/,'-').replace(/ /,' ').toLowerCase();
    if (/\s/.test(c)) continue; nf += c; nm.push(map[i]); }
  let k0 = -1;
  return snips.map((sn, j) => {
    // the text as in the PDF, where the page may put up to 3 marks (such as " - ") where the PDF has a space
    const from = j === 0 ? start : Math.max(k0, 0); let k = -1;
    const words = sn.normalize('NFKC').replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"').replace(/[\u2013\u2014]/g,'-').toLowerCase().split(/\s+/).map(w => w.replace(/[,;:]+$/, '')).filter(Boolean);   // a comma or colon at a word's end may differ
    const esc = w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(words.map(esc).join('[^\\p{L}\\p{N}]{0,3}'), 'gu');
    re.lastIndex = from; let mm = re.exec(nf); if (!mm) { re.lastIndex = 0; mm = re.exec(nf); }
    if (mm) k = mm.index;
    if (k < 0) return null;
    if (j === 0) k0 = k;
    const a = nm[k]; if (!a || !a[0]) return null;
    const r = document.createRange(); r.setStart(a[0], a[1]); r.setEnd(a[0], Math.min(a[1] + 1, a[0].nodeValue.length));
    const q = r.getBoundingClientRect(); const lh = parseFloat(getComputedStyle(a[0].parentElement).lineHeight) || q.height;
    return {top: q.top + scrollY, left: q.left, lh: lh, h: q.height, k: k};
  });
}"""

async def main():
    rows = pdf_rows()
    port = (lambda s: (s.bind(('127.0.0.1', 0)), s.getsockname()[1], s.close())[1])(socket.socket())
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=FOLDER)
    h.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    faults = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': W, 'height': 900})
        await pg.goto('http://127.0.0.1:%d/' % port, wait_until='domcontentloaded', timeout=90000); await pg.wait_for_timeout(4000)
        cur = 0; found = []
        for pn, y, texts in rows:
            snips = [t[:60] for t in texts]
            pos = await pg.evaluate(JS, {'snips': snips, 'start': cur})
            if pos and pos[0]: cur = pos[0]['k']
            miss = [t for t, q in zip(texts, pos) if q is None]
            if miss:
                faults.append('NOT FOUND  PDF p%d y%d: %s' % (pn, y, ' | '.join(m[:40] for m in miss))); continue
            found.append((pn, y, texts, pos))
        cw = await pg.evaluate("() => { const m = document.querySelector('main#content') || document.body; const r = m.getBoundingClientRect(); return r.width }")
        # a region = rows on one PDF page less than 60 pt apart; its columns must stand side by side on the page:
        # every later column starts at least half a column's width (text width / number of columns) right of the one before, and lies within the
        # vertical span of the first column (one line of slack)
        regions = []
        for r in found:
            if regions and regions[-1][-1][0] == r[0] and r[1] - regions[-1][-1][1] < 60: regions[-1].append(r)
            else: regions.append([r])
        for g in regions:
            ncol = max(len(r[3]) for r in g)
            firsts = [r[3][0] for r in g]
            lo = min(q['top'] for q in firsts) - max(q['lh'] for q in firsts); hi = max(q['top'] for q in firsts) + max(q['lh'] for q in firsts)
            for pn, y, texts, pos in g:
                bad = []
                for i in range(1, len(pos)):
                    if not (pos[i]['left'] >= pos[i - 1]['left'] + 0.5 * cw / max(ncol, 2) and lo <= pos[i]['top'] <= hi):
                        bad.append(i)
                if bad:
                    faults.append('COLUMN FAULT  PDF p%d y%d: %s  (page tops %s, lefts %s; first column spans %d-%d)' % (pn, y, ' | '.join(t[:30] for t in texts),
                                  [round(q['top']) for q in pos], [round(q['left']) for q in pos], lo, hi))
        await b.close()
    srv.shutdown()
    for f in faults: print(f)
    print('PDF rows in columns: %d; width %d' % (len(rows), W))
    print('COLUMNS OK' if not faults else 'COLUMNS FAULT (%d)' % len(faults))
    sys.exit(0 if not faults else 1)

asyncio.run(main())
