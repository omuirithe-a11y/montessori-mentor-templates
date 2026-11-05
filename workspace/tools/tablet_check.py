"""tablet_check.py <page folder (unpacked zip copy)> <out.txt> [widths]
6 Nov 2026 (owner 07:16 "implement all 6 immediately", item 2): a short check of the tablet widths (641 to 830 px), where the
other quick checks measure only the computer width. At each width, after the page has settled (lazy images loaded):
  1. text over an image: a line of text whose box overlaps an image box (more than 2 px across and 3 px down);
  2. images beside text: every image set (.mm-set) and floated image (.mm-float) stands beside its text, unless the set was
     put under its text because the text would be narrower than 200 px (class mm-stack; the owner's 5 Nov 09:16 rule) or it
     is a fixed set whose images do not fit beside the text (display block, the 24 Oct rule);
  3. sideways scrolling: the page is wider than the screen;
  4. column tops level: in Word's columns (.mm-wcols2 / .mm-cols3) laid out side by side, the capitals of the first line of
     each column start at the same height (a column that opens with an image: the image's top, level with the capitals);
  5. captions shown: every caption in a row of images lies inside the row's visible box (a scrolling row cuts off what lies
     outside it).
Prints one line per fault and, last, TABLET PASS or TABLET FAULT (n).
"""
import sys, os, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

folder, out = sys.argv[1], sys.argv[2]
widths = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [641, 680, 720, 768, 800, 830]

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=folder)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=folder))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = 'http://127.0.0.1:%d/' % srv.server_address[1]

JS = r"""() => {
const F = [];
const cv = document.createElement('canvas').getContext('2d');
// the top of the capitals of a line (as the template's letter-gap script measures it): image tops are level with it (the placement rule)
const capTop = (q, el) => { const cs = getComputedStyle(el); cv.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily; const m = cv.measureText('H');
  return (q.top + q.bottom) / 2 + (m.fontBoundingBoxAscent - m.fontBoundingBoxDescent) / 2 - m.actualBoundingBoxAscent; };
const R = e => e.getBoundingClientRect();
const pims = [...document.querySelectorAll('main .pim')].filter(p => { const r = R(p); return r.width > 0 && r.height > 0; });
const pr = pims.map(R);
const wk = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT); let n; const rg = document.createRange(); const seen = new Set();
while ((n = wk.nextNode())) { if (!n.nodeValue.trim() || n.parentElement.closest('figure,.lightbox,script,style')) continue; rg.selectNodeContents(n);
  for (const q of rg.getClientRects()) { if (q.width < 1) continue; for (const r of pr) { if (Math.min(q.right, r.right) - Math.max(q.left, r.left) > 2 && Math.min(q.bottom, r.bottom) - Math.max(q.top, r.top) > 3) { const t = n.nodeValue.trim().slice(0, 40); if (!seen.has(t)) { seen.add(t); F.push('text over an image: "' + t + '"'); } break; } } } }
document.querySelectorAll('main .mm-float').forEach(f => { if (f.closest('blockquote')) return; if (getComputedStyle(f).cssFloat === 'none') F.push('image not beside its text (float): ' + (f.querySelector('img') || {}).getAttribute?.('data-full')); });
document.querySelectorAll('main .mm-set').forEach(s => { if (s.classList.contains('mm-stack') || s.classList.contains('mm-intro') || s.classList.contains('mm-formula')) return;
  const tx = s.querySelector('.mm-text'), im = s.querySelector('.mm-imgs'); if (!tx || !im) return;
  if (s.style.display === 'block') return;   // a fixed set whose images do not fit beside the text (the 24 Oct rule)
  const a = R(tx), b = R(im); if (!(b.left >= a.right - 1 || b.right <= a.left + 1)) F.push('image set not beside its text: ' + tx.textContent.trim().slice(0, 40)); });
if (document.documentElement.scrollWidth > innerWidth + 1) F.push('sideways scrolling: page ' + document.documentElement.scrollWidth + ' px wide');
document.querySelectorAll('main .mm-wcols2, main .mm-cols3').forEach(g => { const cols = getComputedStyle(g).gridTemplateColumns.trim().split(/\s+/).length; if (cols < 2) return;
  const tops = [...g.children].map(c => { const f = c.firstElementChild; if (!f) return null; if (f.querySelector && f.querySelector('.pim') && !f.textContent.trim()) return R(f.querySelector('.pim')).top;
    const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let t; while ((t = w.nextNode())) { if (!t.nodeValue.trim()) continue; const r2 = document.createRange(); r2.selectNodeContents(t); const q = r2.getClientRects()[0]; if (q) return capTop(q, t.parentElement); } return null; }).filter(x => x !== null);
  if (tops.length > 1 && Math.max(...tops) - Math.min(...tops) > 3) F.push('column tops not level (' + Math.round(Math.max(...tops) - Math.min(...tops)) + ' px): ' + g.textContent.trim().slice(0, 40)); });
document.querySelectorAll('main .mm-row figcaption, main .mm-set .mm-imgs figcaption').forEach(c => { const row = c.closest('.mm-row') || c.closest('.mm-imgs'); const cs = getComputedStyle(row);
  if (cs.overflowX === 'visible' && cs.overflowY === 'visible') return; const a = R(c), b = R(row); if (a.height === 0) return;
  if (a.top < b.top - 1 || a.bottom > b.bottom + 1) F.push('caption cut off by its row: ' + c.textContent.trim().slice(0, 40)); });
return F; }"""

faults = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in widths:
        pg = b.new_page(viewport={'width': w, 'height': 900})
        pg.goto(url, wait_until='networkidle')
        pg.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(6000)
        for f in pg.evaluate(JS):
            faults.append('width %d: %s' % (w, f))
        pg.close()
    b.close()
srv.shutdown()
with open(out, 'w') as o:
    o.write('tablet check, widths %s, page %s\n' % (','.join(map(str, widths)), folder))
    for f in faults: o.write(f + '\n')
    o.write('TABLET PASS\n' if not faults else 'TABLET FAULT (%d)\n' % len(faults))
    o.write('END\n')
print('TABLET PASS' if not faults else 'TABLET FAULT (%d)' % len(faults))
