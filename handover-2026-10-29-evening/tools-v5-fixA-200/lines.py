"""Find horizontal lines (borders / hr) that cross text glyph boxes. Also check strips hidden under fixed header."""
import sys, time, json
from playwright.sync_api import sync_playwright
url, w = sys.argv[1], int(sys.argv[2])
JS = r"""() => {
  const lines = [];
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el); if (cs.display==='none' || cs.visibility==='hidden') continue;
    const r = el.getBoundingClientRect(); if (r.width < 50) continue;
    const sy = window.scrollY;
    const tb = parseFloat(cs.borderTopWidth), bb = parseFloat(cs.borderBottomWidth);
    if (tb>0 && cs.borderTopStyle!=='none') lines.push({y: r.top+sy, h: tb, x0: r.left, x1: r.right, el: el.tagName+'.'+el.className, side:'top'});
    if (bb>0 && cs.borderBottomStyle!=='none') lines.push({y: r.bottom+sy-bb, h: bb, x0: r.left, x1: r.right, el: el.tagName+'.'+el.className, side:'bottom'});
    if (el.tagName==='HR') lines.push({y: r.top+sy, h: r.height, x0:r.left, x1:r.right, el:'HR.'+el.className, side:'hr'});
  }
  // pseudo-element lines: read their real box via a temporary probe is not possible; use computed ::before/::after geometry
  for (const el of document.querySelectorAll('main *')) {
    for (const ps of ['::before','::after']) {
      const c = getComputedStyle(el, ps);
      if (!c || c.content==='none' || c.content==='normal' || c.display==='none') continue;
      const bg = c.backgroundColor, bt = parseFloat(c.borderTopWidth);
      const visible = (bg && bg!=='rgba(0, 0, 0, 0)' && bg!=='transparent') || (bt>0 && c.borderTopStyle!=='none');
      if (!visible) continue;
      const r = el.getBoundingClientRect(); const sy = window.scrollY;
      let y, h;
      if (c.position==='absolute') {
        const top = parseFloat(c.top), bottom = parseFloat(c.bottom);
        if (!isNaN(top) && c.top!=='auto') y = r.top + sy + top; else y = r.bottom + sy - bottom;
        h = bt>0 ? bt : parseFloat(c.height)||1;
      } else if (ps==='::before') { y = r.top + sy + parseFloat(c.marginTop||0) + parseFloat(getComputedStyle(el).paddingTop||0) + parseFloat(getComputedStyle(el).borderTopWidth||0); h = parseFloat(c.height)||bt||1; }
      else continue;
      if (h > 6) continue;
      lines.push({y, h, x0: r.left, x1: r.right, el: el.tagName+'.'+el.className+ps, side:'pseudo'});
    }
  }
  const texts = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while ((n = tw.nextNode())) {
    if (!n.textContent.trim()) continue;
    const pe = n.parentElement; const cs = getComputedStyle(pe);
    if (cs.visibility==='hidden' || pe.closest('header, nav, .mc-menu, [hidden]')) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) { if (r.width<2) continue; texts.push({t: n.textContent.trim().slice(0,50), top: r.top+window.scrollY, bot: r.bottom+window.scrollY, x0:r.left, x1:r.right, fs: parseFloat(cs.fontSize)}); }
  }
  const hits = [];
  for (const L of lines) for (const T of texts) {
    if (T.x1 <= L.x0 || T.x0 >= L.x1) continue;
    // glyph area: ignore top 10% and bottom 8% of line box (leading); line inside text box = crossing
    const gt = T.top + (T.bot-T.top)*0.15, gb = T.bot - (T.bot-T.top)*0.12;
    if (L.y + L.h > gt && L.y < gb) hits.push({line: L.el+' '+L.side+' y='+Math.round(L.y), text: T.t, textBox: [Math.round(T.top), Math.round(T.bot)]});
  }
  return {nLines: lines.length, nTexts: texts.length, hits};
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": 900}); pg.set_default_timeout(240000)
    pg.goto(url, wait_until="domcontentloaded", timeout=120000)
    try: pg.wait_for_load_state("load", timeout=90000)
    except Exception: print("load timeout")
    pg.evaluate("document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager')")
    try: pg.wait_for_function("[...document.images].every(i=>i.complete)", timeout=120000)
    except Exception: print("img wait timeout")
    time.sleep(5)
    r = pg.evaluate(JS)
    print(f"width {w}: lines {r['nLines']} text boxes {r['nTexts']} line-through-text {len(r['hits'])}")
    seen=set()
    for h in r['hits']:
        k=(h['line'],h['text'])
        if k in seen: continue
        seen.add(k); print("  CROSS", h['line'], '|', repr(h['text']), h['textBox'])
    b.close()
