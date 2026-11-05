#!/usr/bin/env python3
"""wrap_sweep.py <page folder with index.html> <word.docx> <out file> [from=320] [to=1920] [step=1]
(5 Nov 2026, REQUIRED-CHECKS rows D101 "sweep the changed line 1 px at a time across every width before sending it to
review", E043 "...indents...", E044 "List bullets and numbers.")

At every width from..to (1 px steps by default):
  HANG    in every list item and every hanging-label line (p.mm-hanglab), each wrapped line starts at the same left edge
          as the first line's text (after the marker or label) - within 1 px;
  PUNCT   no visual line of a paragraph or list item starts with , . ; : ) ? or !;
At 1440 once:
  MARKER  every list on the page has the same kind of marker as the matching Word list: numbered in Word -> <ol> (numbers),
          bulleted in Word -> <ul> (the template's dash), and a Word paragraph that is not a list item is not an <li>.
          Matched by the item's first 40 letters.
Prints every fault, then WRAP PASS or WRAP FAULT (n), then END. Exit 0 only on pass."""
import sys, re, asyncio, http.server, threading, functools, socket, unicodedata
import docx
from playwright.async_api import async_playwright

FOLDER, DOCX, OUT = sys.argv[1:4]
A = int(sys.argv[4]) if len(sys.argv) > 4 else 320
B = int(sys.argv[5]) if len(sys.argv) > 5 else 1920
S = int(sys.argv[6]) if len(sys.argv) > 6 else 1

def norm(s):
    s = unicodedata.normalize('NFKC', s).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'[^a-z0-9]', '', s.lower())

def word_lists():
    d = docx.Document(DOCX); out = {}
    for p in d.paragraphs:
        t = p.text.strip()
        if len(norm(t)) < 6: continue
        numpr = p._p.pPr is not None and p._p.pPr.numPr is not None
        kind = None
        if numpr:
            # numbered or bulleted: look up the numbering format of this level
            try:
                numId = p._p.pPr.numPr.numId.val; ilvl = p._p.pPr.numPr.ilvl.val if p._p.pPr.numPr.ilvl is not None else 0
                numbering = d.part.numbering_part.numbering_definitions._numbering
                num = numbering.xpath('./w:num[@w:numId="%s"]' % numId)[0]
                absId = num.xpath('./w:abstractNumId')[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                lvl = numbering.xpath('./w:abstractNum[@w:abstractNumId="%s"]/w:lvl[@w:ilvl="%s"]/w:numFmt' % (absId, ilvl))[0]
                fmt = lvl.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                kind = 'ul' if fmt in ('bullet', 'none') else 'ol'
            except Exception:
                kind = 'list?'
        out.setdefault(norm(t)[:40], kind)
    return out

JS_SWEEP = r"""() => {
  const out = [];
  const lineStarts = el => { // left of each visual line's first glyph
    const r = document.createRange(); r.selectNodeContents(el);
    const rects = [...r.getClientRects()].filter(q => q.width > 1 && q.height > 4);
    const lines = []; for (const q of rects) { const L = lines.find(l => Math.abs(l.top - q.top) < q.height * 0.5); if (L) { L.left = Math.min(L.left, q.left); } else lines.push({top: q.top, left: q.left}); }
    return lines.sort((a, b) => a.top - b.top);
  };
  const vis = el => { const s = getComputedStyle(el); const q = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && q.width > 0 && q.height > 0; };
  const m = document.querySelector('main#content') || document.body;
  // HANG: list items and hanging-label lines
  for (const el of m.querySelectorAll('li, p.mm-hanglab')) {
    if (!vis(el)) continue;
    if (el.matches('p.mm-hanglab') && innerWidth <= 640) continue;   // template mm-hanglab-css: no hanging column at 640 and narrower
    let lines = lineStarts(el); if (lines.length < 2) continue;
    // first line's text start: for a hanging label, the text after the label; for an li, its own text start
    let first = lines[0].left;
    if (el.matches('p.mm-hanglab')) { const lab = el.querySelector('.mm-lab'); if (lab) { const lr = lab.getBoundingClientRect(); first = lr.left + Math.max(lr.width, parseFloat(getComputedStyle(lab).minWidth) || 0); } }
    for (let i = 1; i < lines.length; i++) if (Math.abs(lines[i].left - first) > 1) { out.push(['HANG', (el.innerText || '').trim().slice(0, 50), Math.round(lines[i].left - first)]); break; }
  }
  // PUNCT: a visual line starting with punctuation
  const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT); let n; let prevTop = null, prevBlock = null;
  while ((n = w.nextNode())) {
    const p = n.parentElement; if (!p || !vis(p)) continue;
    const blk = p.closest('p, li, h2, h3, div'); const v = n.nodeValue;
    for (let i = 0; i < v.length; i++) {
      if (/\s/.test(v[i])) continue;
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1); const q = r.getBoundingClientRect(); if (!q.height) continue;
      if (blk === prevBlock && prevTop !== null && q.top > prevTop + q.height * 0.5 && /[,.;:)?!]/.test(v[i])) out.push(['PUNCT', (blk.innerText || '').trim().slice(0, 50), v[i]]);
      prevTop = q.top; prevBlock = blk;
    }
  }
  return out;
}"""

JS_LISTS = r"""() => [...(document.querySelector('main#content') || document.body).querySelectorAll('p, li')].map(e => [e.tagName, e.closest('ol') ? 'ol' : (e.closest('ul') ? 'ul' : ''), e.innerText.trim()])"""

async def main():
    wl = word_lists()
    port = (lambda s: (s.bind(('127.0.0.1', 0)), s.getsockname()[1], s.close())[1])(socket.socket())
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=FOLDER); h.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    faults = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto('http://127.0.0.1:%d/' % port, wait_until='domcontentloaded', timeout=90000); await pg.wait_for_timeout(4000)
        for tag, inlist, text in await pg.evaluate(JS_LISTS):
            k = norm(text)[:40]
            if k not in wl: continue
            want = wl[k]
            have = inlist if tag == 'LI' else None
            if want in ('ul', 'ol') and have != want: faults.append('MARKER  Word %s, page %s: %s' % (want, have or 'not a list item', text[:60]))
            if want is None and tag == 'LI': faults.append('MARKER  Word not a list item, page %s: %s' % (inlist, text[:60]))
        seen = set()
        for W in range(A, B + 1, S):
            await pg.set_viewport_size({'width': W, 'height': 900}); await pg.wait_for_timeout(120)
            for kind, txt, val in await pg.evaluate(JS_SWEEP):
                key = (kind, txt)
                faults.append('%s  %d  %s  (%s)' % (kind, W, txt, val))
                seen.add(key)
        await b.close()
    srv.shutdown()
    with open(OUT, 'w') as f:
        for x in faults: f.write(x + '\n')
        f.write('widths %d-%d step %d\n' % (A, B, S))
        f.write(('WRAP PASS' if not faults else 'WRAP FAULT (%d)' % len(faults)) + '\nEND\n')
    print(open(OUT).read()[-3000:])
    sys.exit(0 if not faults else 1)

asyncio.run(main())
