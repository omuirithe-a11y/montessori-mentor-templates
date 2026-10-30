"""Extra page checks (21 Oct 2026, 5.5 - the user: "Measure every gap on the rendered page in pixels against the template's
figures"; "every photo on every page includes a description"; the page against Word). Run after fault_checks.py.
Usage: python3 tools/extra_checks.py <docx> <preview folder or index.html> [page settings]
   (a gap the user has approved is named in the settings' U_ALLOWED by the start of the line above it)
U  gaps: every pair of neighbouring text blocks at 1280, letters to letters (baseline above to the top of the capitals
   below); within one kind of pair, every gap within 1px of the most common one. A different gap is listed - each is
   either fixed or put to the user.
V  descriptions: every photo (img.doc-img) has a description.
W  first-line indents: a plain Word paragraph with a first-line indent has the same indent on the page (1px).
"""
import sys, os, re, asyncio, collections, docx
from playwright.async_api import async_playwright

DOCX, PV = sys.argv[1], sys.argv[2]
import runpy
ALLOWED = runpy.run_path(sys.argv[3]).get('U_ALLOWED', []) if len(sys.argv) > 3 else []
url = 'file://' + os.path.abspath(PV if PV.endswith('.html') else os.path.join(PV, 'index.html'))
JS = r'''(()=>{const m=document.querySelector("main");const cv=document.createElement("canvas").getContext("2d");
const met=el=>{const s=getComputedStyle(el);cv.font=s.fontStyle+" "+s.fontWeight+" "+s.fontSize+" "+s.fontFamily;const t=cv.measureText("H");return [t.fontBoundingBoxAscent,t.fontBoundingBoxDescent,t.actualBoundingBoxAscent]};
const kind=el=>{const c=el.closest("li");if(c)return (c.closest("ol")?"numbered item":"dash item")+(c.parentElement.closest("li")?" (inner)":"");
 if(el.closest("cite"))return "attribution";if(el.closest("blockquote"))return "quotation";if(el.closest(".res-desc"))return "resources description";if(el.closest(".res-item"))return "resources title";if(el.closest(".res-entry h3,.res-src"))return "resources source";
 const h=el.closest("h2,h3");if(h)return "heading "+getComputedStyle(h).color;if(el.closest(".micro-label"))return "bold label";if(el.closest("p.mm-ul"))return "underlined line";
 const p=el.closest("p");if(p){const f=p.firstElementChild;if(f&&f.tagName=="STRONG"&&p.textContent.trim()==f.textContent.trim())return "bold line";return "paragraph"}return el.tagName.toLowerCase()};
const lines=[];const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT,{acceptNode:x=>x.nodeValue.trim()&&x.parentElement.getClientRects().length&&!x.parentElement.closest("script,style,.pdf")?1:3});let x;
while(x=w.nextNode()){const blk=x.parentElement.closest("li,cite,blockquote,p,h2,h3,.micro-label,.res-item,div");const r=document.createRange();r.selectNodeContents(x);
 for(const q of r.getClientRects()){if(q.height<5||q.width<1)continue;const [A,D,C]=met(x.parentElement);const b=(q.top+q.bottom)/2+(A-D)/2;lines.push({b:b+scrollY,t:b-C+scrollY,blk})}}
lines.sort((a,b)=>a.b-b.b);const rows=[];for(const l of lines){const r=rows[rows.length-1];if(r&&Math.abs(r.b-l.b)<3){r.t=Math.min(r.t,l.t)}else rows.push({b:l.b,t:l.t,blk:l.blk})}
const rules=[...m.querySelectorAll(".beige-rule,p.mm-gl")].filter(r=>r.getBoundingClientRect().width>200).map(r=>{const q=r.getBoundingClientRect();return [q.top+scrollY,q.bottom+scrollY]});
const imgs=[...m.querySelectorAll("img")].map(i=>i.getBoundingClientRect()).filter(q=>q.height>20).map(q=>[q.top+scrollY,q.bottom+scrollY]);
const out=[];for(let i=1;i<rows.length;i++){const a=rows[i-1],b=rows[i];if(a.blk===b.blk)continue;
 const rl=rules.some(r=>r[0]>a.b-1&&r[1]<b.t+1),ph=imgs.some(q=>q[1]>a.b&&q[0]<b.t);
 out.push([kind(a.blk)+" > "+kind(b.blk)+(rl?" (beige line)":""),Math.round((b.t-a.b)*10)/10,(ph?"[photo beside] ":"")+a.blk.textContent.trim().slice(0,32),b.blk.textContent.trim().slice(0,32)])}
const alts=[...m.querySelectorAll("img.doc-img")].map(i=>[i.getAttribute("data-name")||i.src.slice(-20),(i.getAttribute("alt")||"").trim()]);
const ind=[...m.querySelectorAll("p")].filter(p=>!p.className&&!p.closest("li,blockquote,figure")).map(p=>[p.textContent.replace(/[^a-z0-9]/gi,"").toLowerCase().slice(0,60),parseFloat(getComputedStyle(p).textIndent)]);
return {out,alts,ind}})()'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1280, 'height': 900})
        await pg.goto(url); await pg.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i=>i.loading="eager")')
        h = await pg.evaluate('document.documentElement.scrollHeight'); await pg.set_viewport_size({'width': 1280, 'height': h})
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(3500)
        r = await pg.evaluate(JS); await b.close(); return r

R = asyncio.run(main()); fails = {}
g = collections.defaultdict(list)
for k, v, a, b in R['out']:
    g[k].append((v, a, b))   # a pair with a photo beside the gap is checked with its kind and marked [photo beside]
fu = []
for k, xs in g.items():
    mode = collections.Counter(round(v) for v, a, b in xs).most_common(1)[0][0]
    for v, a, b in xs:
        if abs(v - mode) > 1 and len(xs) > 1 and not any(a.replace('[photo beside] ', '').startswith(s[:30]) for s in ALLOWED): fu.append('%s: %s (most %s) - "%s" / "%s"' % (k, v, mode, a, b))
print('U gaps, one per kind of pair (1280)', 'FAIL' if fu else 'PASS', '(%d pairs, %d kinds)' % (len(R['out']), len(g)))
for f in fu: print('     -', f)
fv = [n for n, a in R['alts'] if not a]
print('V photo descriptions', 'FAIL' if fv else 'PASS', '(%d photos)' % len(R['alts']))
for f in fv: print('     - no description:', f)
nz = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())[:60]
ind = {k: v for k, v in R['ind']}
fw, n = [], 0
for q in docx.Document(DOCX).paragraphs:
    fi = q.paragraph_format.first_line_indent
    if fi is None or fi.pt <= 0 or (q.paragraph_format.left_indent and q.paragraph_format.left_indent.pt) or nz(q.text) not in ind: continue
    n += 1
    if abs(ind[nz(q.text)] - fi.pt * 4 / 3) > 1: fw.append('"%s": page %s, Word %.1f' % (q.text[:40], ind[nz(q.text)], fi.pt * 4 / 3))
print('W first-line indents (Word)', 'FAIL' if fw else 'PASS', '(%d checked)' % n)
for f in fw: print('     -', f)
bad = [x for x, f in (('U', fu), ('V', fv), ('W', fw)) if f]
print('FAILURES:', ', '.join(bad) if bad else 'none')
