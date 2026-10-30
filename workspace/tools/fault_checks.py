"""Automatic checks for the faults found on 20 Oct 2026. One page at a time.

  python3 tools/fault_checks.py <word.docx> <page.pdf> build/<folder>/preview

 A photos      every page photo against the PDF picture in the same place (picture match and shape)
 B headings    every heading's colour against its Word colour
 C formatting  every italic, bold and underlined Word run against the page's computed style
 D dividers    every beige line against the line of text the PDF shows under its line picture
 E overlaps    with photos loading late (held back 3 s) and the page scrolled through: no text line over a
               photo, no photo or text over the footer band, no photo over a photo - at 1280, 768 and 390
 F lists       every numbered item's number/letter against the PDF's
 G tab gaps    no tab gap wider than 60px after the start of a line (a Word hand-made line break left mid-line)
 H words       word-for-word result from the build report
Prints PASS/FAIL per check with every failing item."""
import sys, os, re, io, json, zipfile, asyncio, threading, functools, http.server, socketserver
import numpy as np, docx, fitz
from docx.oxml.ns import qn
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
DOCX, PDF, PV = sys.argv[1], sys.argv[2], sys.argv[3]
import runpy
SET = runpy.run_path(sys.argv[4]) if len(sys.argv) > 4 else {}   # the page's settings file: a photo order it sets (ROW_ORDER) is reported, not failed
nz = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())
res = {}
def out(k, fails, n):
    res[k] = fails
    print('%s %s (%d checked)%s' % (k, 'PASS' if not fails else 'FAIL', n, ''.join('\n     - ' + f for f in fails[:40])))

D = docx.Document(DOCX); paras = D.paragraphs; pdf = fitz.open(PDF)
def wcolour(r):
    rp = r._r.find(qn('w:rPr')); c = rp.find(qn('w:color')) if rp is not None else None
    return (c.get(qn('w:val')) or '').upper() if c is not None else ''

# ---------------------------------------------------------------- PDF pictures and lines
pdfimgs, thin = [], []
for pn, pg in enumerate(pdf):
    lines = sorted((l['bbox'][1], l['bbox'][3], ''.join(s['text'] for s in l['spans']), l['spans'])
                   for b in pg.get_text('dict')['blocks'] for l in b.get('lines', []) if ''.join(s['text'] for s in l['spans']).strip())
    for inf in pg.get_image_info(xrefs=True):
        x0, y0, x1, y1 = inf['bbox']
        if y1 - y0 < 6 and x1 - x0 > 100:
            below = [l for l in lines if l[0] > y1]
            if below: yb = below[0][1]; thin.append((pn, y0, ''.join(l[2] for l in below if abs(l[1] - yb) < 3)))
        elif y1 - y0 > 2 and x1 - x0 > 2:   # 20 Oct 21:4x: every picture; touching ones are joined below
            pdfimgs.append((pn, round(y0 / 20), x0, pg, inf['bbox']))
# 20 Oct 21:4x (5.4 name-card drawing: Word's one picture, stored in the PDF as 8 small touching pictures): pictures on one
# page that touch or overlap (within 3pt) are one picture - the area they cover together; pieces under 15pt left alone are dropped
def _join(items):
    out_ = [list(x) for x in items]; changed = True
    while changed:
        changed = False
        for i in range(len(out_)):
            for j in range(i + 1, len(out_)):
                a_, b_ = out_[i], out_[j]
                if a_[0] != b_[0]: continue
                A_, B_ = a_[4], b_[4]
                if A_[0] - 3 <= B_[2] and B_[0] - 3 <= A_[2] and A_[1] - 3 <= B_[3] and B_[1] - 3 <= A_[3]:
                    u = (min(A_[0], B_[0]), min(A_[1], B_[1]), max(A_[2], B_[2]), max(A_[3], B_[3]))
                    out_[i] = [a_[0], round(u[1] / 20), u[0], a_[3], u]; del out_[j]; changed = True; break
            if changed: break
    return [tuple(x) for x in out_ if x[4][2] - x[4][0] > 15 and x[4][3] - x[4][1] > 15]
pdfimgs = [list(x) for x in pdfimgs]
for x in pdfimgs:   # drawn shapes touching a picture (5.4: the name cards drawn beside the child's photos) are part of it
    shapes = [s_['rect'] for s_ in x[3].get_drawings() if s_['rect'].width < 200 and s_['rect'].height < 200]
    grew = True
    while grew:
        grew = False; A_ = x[4]
        for R_ in shapes:
            if A_[0] - 3 <= R_.x1 and R_.x0 - 3 <= A_[2] and A_[1] - 3 <= R_.y1 and R_.y0 - 3 <= A_[3]:
                u = (min(A_[0], R_.x0), min(A_[1], R_.y0), max(A_[2], R_.x1), max(A_[3], R_.y1))
                if u != tuple(A_): x[4] = u; x[2] = u[0]; x[1] = round(u[1] / 20); grew = True; A_ = u
pdfimgs = _join([tuple(x) for x in pdfimgs])
pdfimgs.sort(key=lambda t: (t[0], t[1], t[2]))
thin.sort()

# ---------------------------------------------------------------- serve the page; photos held back
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=PV)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
from playwright.async_api import async_playwright

JS_FMT = '''(runs)=>{const m=document.querySelector('main');const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);const nodes=[];let n;
 while((n=w.nextNode()))nodes.push(n);const nz=t=>t.toLowerCase().replace(/[^a-z0-9]/g,'');const fails=[];let i0=0;
 for(const r of runs){const k=nz(r.t);if(k.length<1)continue;let hit=null;
  const ex=nodes.findIndex((x,ix)=>ix>=i0&&x.nodeValue.trim()===r.t.trim());const word=(v,t)=>{let a=v.indexOf(t);while(a>=0){const b=v[a-1]||' ',c=v[a+t.length]||' ';if(!/[A-Za-z0-9]/.test(b)&&!/[A-Za-z0-9]/.test(c))return true;a=v.indexOf(t,a+1);}return false;};if(ex>=0){hit=nodes[ex];i0=ex+1;}else{for(let i=0;i<nodes.length;i++){const j=(i0+i)%nodes.length;const v=nodes[j].nodeValue;if(r.t.length<5?word(v,r.t.trim()):nz(v).includes(k)){hit=nodes[j];i0=j;break;}}}
  if(!hit){fails.push('not found: '+r.t.slice(0,40));continue;}
  let e=hit.parentElement,cs=getComputedStyle(e);let ul=false;for(let x=e;x&&x!==m;x=x.parentElement){if(getComputedStyle(x).textDecorationLine.includes('underline'))ul=true;}
  if(r.i&&cs.fontStyle!=='italic')fails.push('italic lost: '+r.t.slice(0,40));
  if(r.b&&parseInt(cs.fontWeight)<600)fails.push('bold lost: '+r.t.slice(0,40));
  if(r.u&&!ul)fails.push('underline lost: '+r.t.slice(0,40));}
 return fails;}'''
JS_OVER = '''()=>{const m=document.querySelector('main'),band=document.querySelector('.mc-band');const R=[];
 const pims=[...m.querySelectorAll('.pim')].map(p=>p.getBoundingClientRect()).filter(r=>r.width>4&&r.height>4);
 const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);let n;const lines=[];const rg=document.createRange();
 while((n=w.nextNode())){if(!n.nodeValue.trim())continue;const pe=n.parentElement;if(pe.closest('figcaption'))continue;rg.selectNodeContents(n);
  for(const q of rg.getClientRects())if(q.width>2&&q.height>2)lines.push([q,n.nodeValue.trim().slice(0,30)]);}
 const ov=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>2&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>2;
 for(const [q,t] of lines)for(const p of pims)if(ov(q,p))R.push('text over photo: "'+t+'"');
 const bb=band.getBoundingClientRect();
 for(const p of pims)if(ov(p,bb))R.push('photo over footer band ('+Math.round(p.bottom-bb.top)+'px)');
 for(const [q,t] of lines)if(ov(q,bb))R.push('text over footer band: "'+t+'"');
 for(let i=0;i<pims.length;i++)for(let j=i+1;j<pims.length;j++)if(ov(pims[i],pims[j]))R.push('photo over photo');
 return [...new Set(R)];}'''
JS_TABS = '''()=>{const F=[];document.querySelectorAll('main span.mm-t').forEach(s=>{const r=s.getBoundingClientRect(),p=s.closest('p,li');if(!p)return;
 const pl=p.getBoundingClientRect().left;if(r.width>60&&r.left-pl>300)F.push(Math.round(r.width)+'px gap mid-line: "'+p.textContent.trim().slice(0,40)+'"');});return F;}'''

# 20 Oct 21:4x (your review steps): K - every list's marker and text against Word's indent; P - every photo beside text
# starts level with the top of the letters of its first line (a photo marked mm-mid: midway between that and the last baseline)
JS_LISTS = '''()=>{const m=document.querySelector('main'),ml=[...m.querySelectorAll('p')].find(p=>!p.closest('li,blockquote')&&getComputedStyle(p).paddingLeft==='0px'&&p.getBoundingClientRect().width>200).getBoundingClientRect().left;
 return [...m.querySelectorAll('ul,ol')].filter(l=>!l.closest('.mm-inner,nav,header,footer')).map(l=>{const li=l.querySelector(':scope>li');if(!li)return null;const r=document.createRange();
  const tn=document.createTreeWalker(li,NodeFilter.SHOW_TEXT);let n;while((n=tn.nextNode())&&!n.nodeValue.trim());if(!n)return null;r.setStart(n,n.nodeValue.search(/\\S/));r.setEnd(n,n.nodeValue.search(/\\S/)+1);
  const tx=r.getClientRects()[0].left,mk=getComputedStyle(li,'::before'),lr=li.getBoundingClientRect();return [li.textContent.trim().slice(0,60),Math.round((lr.left+parseFloat(mk.left)-ml)*10)/10,Math.round((tx-ml)*10)/10,Math.round((lr.left+parseFloat(mk.left)+parseFloat(mk.width)-ml)*10)/10];}).filter(x=>x);}'''
JS_FLOAT = '''()=>{var cv=document.createElement('canvas').getContext('2d');
 function walk(el,cb){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,r=document.createRange();while((n=w.nextNode())){var s=n.nodeValue,cs=getComputedStyle(n.parentElement);cv.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;var fm=cv.measureText('Hg'),fa=fm.fontBoundingBoxAscent,fd=fm.fontBoundingBoxDescent;
   for(var i=0;i<s.length;i++){if(!s[i].trim())continue;r.setStart(n,i);r.setEnd(n,i+1);var b=r.getClientRects()[0];if(!b||!b.width)continue;var y=b.top+(b.height-(fa+fd))/2+fa;if(cb(b,y,y-cv.measureText(s[i]).actualBoundingBoxAscent,cv.measureText(s[i]).actualBoundingBoxDescent)===false)return;}}}
 return [...document.querySelectorAll('main .mm-float, main .mm-co')].map(f=>{const nx=f.nextElementSibling;if(!nx)return null;let line=null,top=null,base=null;
  walk(nx,(b,y,t,d)=>{if(line===null)line=b.top;if(b.top<=line+2)top=top===null?t:Math.min(top,t);base=base===null?y+d:Math.max(base,y+d);});
  const q=f.querySelector('.pim').getBoundingClientRect();if(top===null)return null;if(getComputedStyle(f).cssFloat==='none'&&!f.classList.contains('mm-co'))return null;   /* 21 Oct: a photo the template puts under the text at this width is not beside it */const mid=f.classList.contains('mm-mid');
  const co=f.querySelector('img[data-centre-on]');if(co&&f.classList.contains('mm-co')){const words=co.getAttribute('data-centre-on'),tw=document.createTreeWalker(nx,NodeFilter.SHOW_TEXT);let tn,hit=null;while((tn=tw.nextNode())){const i=tn.nodeValue.indexOf(words);if(i>=0){const rr=document.createRange();rr.setStart(tn,i);rr.setEnd(tn,i+words.length);const qs=[...rr.getClientRects()].filter(q=>q.width>0);const t0=Math.min(...qs.map(q=>q.top)),b0=Math.max(...qs.map(q=>q.bottom));hit={top:t0,height:b0-t0};break;}}   // 21 Oct: the whole phrase, both lines if it wraps (the independent check)

   return [[co.getAttribute('data-name'),'centred on "'+words+'"',hit?Math.round((q.top+q.height/2-(hit.top+hit.height/2))*10)/10:999,nx.textContent.trim().slice(0,30)]];}   // 20 Oct 23:3x: a photo the page settings centre on one line (CENTRE_ON)
  let te=-1e9;const rg=document.createRange(),tw=document.createTreeWalker(nx,NodeFilter.SHOW_TEXT);let tn;while((tn=tw.nextNode())){if(!tn.nodeValue.trim())continue;rg.selectNodeContents(tn);for(const qq of rg.getClientRects())if(qq.width)te=Math.max(te,qq.right);}
  const r=[f.querySelector('img').getAttribute('data-name'),mid?'centred':'top',mid?Math.round((q.top-top-(base-q.bottom))*10)/10:Math.round((q.top-top)*10)/10,nx.textContent.trim().slice(0,30)];
  if(mid&&window.innerWidth>=1200)return [r,[r[0],'centred across',Math.round(((q.left-te)-(nx.getBoundingClientRect().right-q.right))*10)/10,r[3]]];return [r];}).filter(x=>x).flat();}'''

async def browse():
    async with async_playwright() as p:
        b = await p.chromium.launch(); got = {}
        for w in (1280, 768, 390):
            pg = await b.new_page(viewport={'width': w, 'height': 900})
            async def slow(route):
                await asyncio.sleep(3); await route.continue_()
            await pg.route('**/images/0*', slow)
            await pg.goto('http://127.0.0.1:%d/index.html' % port); await pg.wait_for_timeout(1500)
            H = await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0, H + 900, 500): await pg.mouse.wheel(0, 500); await pg.wait_for_timeout(120)
            await pg.wait_for_timeout(6000)
            got['over%d' % w] = await pg.evaluate(JS_OVER)
            if w in (1280, 768): got['float%d' % w] = await pg.evaluate(JS_FLOAT)
            if w == 1280: got['lists'] = await pg.evaluate(JS_LISTS)
            got['bgrp%d' % w] = await pg.evaluate('''()=>{const out=[],seen=new Set();const bd=p=>{const a=p.lastElementChild;if(a&&a.matches('a.pdf'))return a;if(a&&p.classList.contains('res-item')&&a.matches('.meta')&&a.children.length===1&&a.firstElementChild.matches('a.pdf')&&a.textContent.trim()===a.firstElementChild.textContent.trim())return a.firstElementChild;return null;};   /* 22 Oct 2026: a title line's badge may sit alone in its .meta */
              /* 22 Oct 2026 (5.5, user 09:5x "yes"): Resources title lines (div.res-item) that follow one another are neighbours too, as paragraphs are */
              const same=(x,p)=>x&&(p.classList.contains('res-item')?x.classList.contains('res-item'):(x.tagName==='P'&&!x.classList.contains('res-item')));
              for(const a of document.querySelectorAll('main p > a.pdf, main .res-item > a.pdf, main .res-item > .meta > a.pdf')){let p=a.parentElement.classList.contains('meta')?a.parentElement.parentElement:a.parentElement;if(seen.has(p)||bd(p)!==a)continue;let s=p;while(same(s.previousElementSibling,p))s=s.previousElementSibling;
               const g=[];for(let x=s;same(x,p);x=x.nextElementSibling){seen.add(x);const b=bd(x);if(b)g.push([Math.round(b.getBoundingClientRect().left*10)/10,x.textContent.trim().slice(0,30)]);}out.push(g);}return out;}''')
            got['bown%d' % w] = await pg.evaluate('''()=>[...document.querySelectorAll('main a.pdf')].map(a=>{const p=a.parentElement,r=document.createRange();r.setStart(p,0);r.setEndBefore(a);const rs=[...r.getClientRects()].filter(q=>q.width>0.5&&!(q.width<2));const b=a.getBoundingClientRect(),last=rs.length?rs[rs.length-1]:null;const own=last&&b.top>last.top+last.height/2;return [own,b.left-p.getBoundingClientRect().left,last?b.left-last.right:null,p.textContent.trim().slice(0,30)]})''')
            if w == 1280:
                got['tabs'] = await pg.evaluate(JS_TABS)
                got['fmt'] = await pg.evaluate(JS_FMT, RUNS)
                got['chars'] = await pg.evaluate('''()=>{const m=document.querySelector('main'),w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);let n,t='',f='';const memo=new Map();
                  const fl=e=>{if(memo.has(e))return memo.get(e);const cs=getComputedStyle(e);let u=false;for(let x=e;x&&x!==m;x=x.parentElement){if(getComputedStyle(x).textDecorationLine.includes('underline'))u=true;}
                   const v=(cs.fontStyle==='italic'?1:0)+(parseInt(cs.fontWeight)>=600?2:0)+(u?4:0)+(e.closest('.micro-label')?8:0);memo.set(e,v);return v;};
                  while((n=w.nextNode())){const e=n.parentElement;if(!e||e.closest('script,style,a.pdf,figcaption'))continue;if(getComputedStyle(e).display==='none')continue;const v=fl(e);
                   for(const ch of n.nodeValue){if(/\s/.test(ch))continue;t+=ch;f+=v.toString(16);}}return [t,f];}''')
                got['gaps'] = await pg.evaluate('''(keys)=>{const nz=t=>t.toLowerCase().replace(/[^a-z0-9]/g,'');const F=[];
                  const ps=[...document.querySelectorAll('main p,main li,main h2,main h3,main td,main th,main div.micro-label,main a,main cite')];
                  for(const [k,before,n] of keys){const p=ps.find(x=>nz(x.textContent).includes(k));if(!p){F.push('not found: '+before);continue;}
                   const p2=ps.find(x=>nz(x.textContent).includes(nz(before))&&x.querySelector('span.mm-t,span.mm-lab'));const g=[...(p2||p).querySelectorAll('span.mm-t,span.mm-lab')].map(s=>s.getBoundingClientRect().width);   // 21 Oct: the gap is in the attribution (cite), not the quotation's first block
                   if(!g.length||Math.max(...g)<n*3.5)F.push('gap lost after "'+before+'"');}return F;}''', GAPS)
                got['badges'] = await pg.evaluate('''()=>[...document.querySelectorAll('main a.pdf')].map(a=>{const p=a.parentElement,r=document.createRange();r.setStart(p,0);r.setEndBefore(a);const rs=[...r.getClientRects()].filter(q=>q.width>0.5),e=rs.length?rs[rs.length-1].right:null;const b=a.getBoundingClientRect();return [a.dataset.tabx||null,b.left,e,b.top-(rs.length?rs[rs.length-1].top:b.top),p.textContent.trim().slice(0,40),p.getBoundingClientRect().left]})''')
                got['badgemode'] = await pg.evaluate("document.documentElement.getAttribute('data-tab-badges')")
                got['heads'] = await pg.evaluate('''()=>[...document.querySelectorAll('main h2,main h3')].map(h=>[h.textContent.trim(),getComputedStyle(h).color])''')
                got['setrules'] = await pg.evaluate('''()=>[...document.querySelectorAll('main :is(.beige-rule,p.mm-gl)[data-setting="1"]')].map(r=>{let e=r.nextElementSibling;while(e&&!e.textContent.trim())e=e.nextElementSibling;return e?e.textContent.trim().slice(0,60):''})''')
                got['resrules'] = await pg.evaluate('''()=>{const es=[...document.querySelectorAll('main div.res-entry')];return [es.length,es.slice(1).filter(e=>{let p=e.previousElementSibling;return p&&p.matches(':is(.beige-rule,p.mm-gl)[data-setting="res"]')}).length,document.querySelectorAll('main :is(.beige-rule,p.mm-gl)[data-setting="res"]').length]}''')
                got['rules'] = await pg.evaluate('''()=>[...document.querySelectorAll('main :is(.beige-rule,p.mm-gl):not([data-setting])')].map(r=>{let e=r.nextElementSibling;while(e&&!e.textContent.trim())e=e.nextElementSibling;return e?e.textContent.trim().slice(0,60):''})''')
                got['lis'] = await pg.evaluate('''()=>[...document.querySelectorAll('main ol')].flatMap(ol=>{const cr=getComputedStyle(ol).counterReset.split(' '),s=(parseInt(cr[1])||0)+1;return [...ol.querySelectorAll(':scope>li')].map((li,i)=>{const c=getComputedStyle(li,'::before').content,k=ol.classList.contains('mm-mk-alpha-paren')?'mm-mk-alpha-paren':/lower-alpha|lower-latin/.test(c)&&/\\)/.test(c)?'mm-mk-alpha-paren':/upper-roman/.test(c)?'mm-uroman':/lower-roman/.test(c)?'mm-lroman':/upper-alpha|upper-latin/.test(c)?'mm-ualpha':/lower-alpha|lower-latin/.test(c)?'mm-lalpha':'';return [s+i,k,li.textContent.trim().slice(0,50)]})})''')   # the number the page draws (its counter), not the start attribute
                got['imgs'] = await pg.evaluate('''()=>[...document.querySelectorAll('main img.doc-img')].map(i=>[i.getAttribute('data-full'),i.getAttribute('data-name'),i.closest('.pim').getBoundingClientRect().width/i.closest('.pim').getBoundingClientRect().height])''')
            await pg.close()
        await b.close(); return got

# Word runs with formatting (the hero title paragraph left out)
RUNS = []   # Word runs joined where Word splits one word or phrase into pieces with the same formatting; UK spelling as the site
title_seen = False
def UK(a):   # the UK spellings the site rules allow: only these exact changes pass
    w = a
    for us, uk in ((r'(?<!\bs)(?<!\bpr)(?<!\bse)(?<!caps)(?<!\bmaz)iz(e|ed|es|ing|ation|ations)\b', r'is\1'),
                   (r'\b((?i:behavi|col|fav|hon|lab|neighb|hum|flav|harb|rum|endeav|vap|savi|arm|od|val|vig|rig|splend|parl|tum))or(s|ed|ing|ite|ites|ful|al)?\b', r'\1our\2'),
                   (r'\bprogram(s?)\b', r'programme\1'), (r'\bProgram(s?)\b', r'Programme\1'),
                   (r'enroll(ment|ments)\b', r'enrol\1'), (r'practic(ed|ing)\b', r'practis\1'), (r'\b(grovel|model)ing\b', r'\1ling')):
        w = re.sub(us, uk, w)
    return w
for p in paras:
    if not p.text.strip(): continue
    if not title_seen: title_seen = True; continue
    cur = None
    for r in p.runs:
        rp = r._r.find(qn('w:rPr'))
        on = lambda tag, off: rp is not None and rp.find(qn(tag)) is not None and rp.find(qn(tag)).get(qn('w:val')) not in off
        f = (bool(on('w:i', ('0', 'false'))), bool(on('w:b', ('0', 'false'))), bool(on('w:u', ('none', None))))
        if cur and cur[0] == f: cur[1] += r.text; continue
        if cur and any(cur[0]) and cur[1].strip(): RUNS.append({'t': UK(cur[1].strip()), 'i': cur[0][0], 'b': cur[0][1], 'u': cur[0][2]})
        cur = [f, r.text]
    if cur and any(cur[0]) and cur[1].strip(): RUNS.append({'t': UK(cur[1].strip()), 'i': cur[0][0], 'b': cur[0][1], 'u': cur[0][2]})
GAPS = []
for p in paras:
    t = p.text.replace(' ', ' ')
    if re.search(r' {3,}(PDF|PPT|DOC|Word|Video)\s*$', t): continue   # spaces before a file badge: the badge is placed by the Resources format, not by a gap
    for m_ in re.finditer(r'(\S[^\t]*?) {3,}\S', t):
        GAPS.append([nz(t)[:30], m_.group(1)[-25:], len(re.search(r' {3,}', t[m_.start():]).group(0))]); break
G = asyncio.run(browse()); srv.shutdown()

# A photos - every page photo against every PDF picture: the best match must be clearly that picture, each picture once;
# the order must be the PDF's, unless the page's settings set another (ROW_ORDER), which is reported
def sig(im): a = np.asarray(im.convert('RGB').resize((24, 24)), float).ravel(); return (a - a.mean()) / (a.std() + 1e-6)
fails = []
imgs = G['imgs']
if len(imgs) != len(pdfimgs) - len(SET.get('DROP_PHOTOS', [])): fails.append('page has %d photos, PDF %d less %d the page settings leave out' % (len(imgs), len(pdfimgs), len(SET.get('DROP_PHOTOS', []))))   # 21 Oct 19:39 (5.3, user): DROP_PHOTOS
psig = []
for pn, _, _, pg, bb in pdfimgs:
    pm = pg.get_pixmap(dpi=72, clip=fitz.Rect(bb)); psig.append(sig(Image.frombytes('RGB', (pm.width, pm.height), pm.samples)))
used = {}; order = []
for k, (full, name, ar) in enumerate(imgs):
    e = [float(np.mean((sig(Image.open(os.path.join(PV, full))) - q) ** 2)) for q in psig]
    if not e: break
    j = int(np.argmin(e)); order.append(j)
    if e[j] > 0.6: fails.append('photo %d (%s) matches no PDF picture (best difference %.2f)' % (k + 1, name, e[j])); continue
    if j in used: fails.append('photo %d (%s) is the same PDF picture as photo %d' % (k + 1, name, used[j] + 1))
    used[j] = k
    bb = pdfimgs[j][4]; par = (bb[2] - bb[0]) / (bb[3] - bb[1])
    if abs(ar - par) / par > 0.05: fails.append('photo %d (%s) shape %.2f, PDF %.2f (turn or crop)' % (k + 1, name, ar, par))
# each photo is the Word picture it is named after (a photo file swapped with another is caught here)
zw = zipfile.ZipFile(DOCX); media = {os.path.basename(n): n for n in zw.namelist() if n.startswith('word/media/')}
for k, (full, name, ar) in enumerate(imgs):
    if name in media and not name.lower().endswith(('.emf', '.wmf')):
        try: wi = Image.open(io.BytesIO(zw.read(media[name])))
        except Exception: continue
        wi.draft('RGB', (1600, 1600)); wi.thumbnail((1600, 1600))   # 21 Oct 2026 (5.5): Word's 296-million-pixel sheet, turned 8 ways at full size, ran out of memory; the comparison is made at 24x24, so 1600 first changes nothing
        pi_ = sig(Image.open(os.path.join(PV, full)))   # Word's turn or flip (applied by the build) allowed: the nearest of the 8
        e = min(float(np.mean((pi_ - sig(t_)) ** 2)) for t_ in [wi.convert('RGB').transpose(m) for m in (Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.TRANSPOSE, Image.TRANSVERSE)] + [wi.convert('RGB')])
        if e > 0.1: fails.append('photo %d is not Word\'s %s (difference %.2f)' % (k + 1, name, e))
if SET.get('ROW_ORDER'):   # the order the settings set, by Word's names
    want = [n for row in SET['ROW_ORDER'] for n in row]; got = [n for _, n, _ in imgs if n in want]
    if got != want: fails.append('photo order %s, the page settings set %s' % (got, want))
note = ''
if order != sorted(order):
    if SET.get('ROW_ORDER'): note = ' - order differs from the PDF as the page settings set it (ROW_ORDER): page shows PDF pictures %s' % [o + 1 for o in order]
    else: fails.append('photos not in the PDF order: page shows PDF pictures %s' % [o + 1 for o in order])
out('A photos' + note, fails, len(imgs))

# B headings
WC = {}
for p in paras:
    cs = {wcolour(r) for r in p.runs if r.text.strip()}
    if p.text.strip() and len(cs) == 1: WC[nz(p.text)] = next(iter(cs))
hexrgb = lambda h: 'rgb(%d, %d, %d)' % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
fails = []; n = 0
for t, col in G['heads']:
    w = WC.get(nz(t))
    if w and re.fullmatch(r'[0-9A-F]{6}', w) and w not in ('000000',):
        n += 1
        if any(nz(t).startswith(nz(x_)) for x_ in SET.get('RES_SPLIT_ITEM', [])) and col == 'rgb(238, 0, 0)': continue   # 22 Oct 2026 (5.5, user: "Busy Bee Montessori Center" a red name line): the page setting makes it a red source name
        if col != hexrgb(w): fails.append('"%s" is %s, Word #%s' % (t[:40], col, w))
out('B headings', fails, n)

# C formatting
# C formatting, letter by letter: Word's letters (title and the settings' DROP left out) lined up with the page's; every
# Word letter in italic, bold or underline must be so on the page, and no page letter bold or italic that Word has plain
import difflib
def _fieldlink(r):   # 21 Oct: is this run the shown text of a Word HYPERLINK field?
    p_ = r.getparent(); depth = 0; inst = ''
    for x in p_.iter(qn('w:r')):
        if x is r: return depth > 0 and 'HYPERLINK' in inst
        fc = x.find(qn('w:fldChar'))
        if fc is not None:
            t_ = fc.get(qn('w:fldCharType'))
            if t_ == 'begin': depth += 1; inst = ''
            elif t_ == 'end': depth = max(0, depth - 1)
        it_ = x.find(qn('w:instrText'))
        if it_ is not None: inst += it_.text or ''
    return False
CSTY = {}
for st_ in D.styles:
    try:
        if st_.type == 2: CSTY[st_.style_id] = (1 if st_.font.italic else 0) + (2 if st_.font.bold else 0) + (4 if st_.font.underline else 0)
    except Exception: pass
WS_, WF = [], []
first = True
for p in paras:
    if not p.text.strip(): continue
    if first: first = False; continue
    if any(p.text.strip().startswith(t) for t in SET.get('DROP', [])): continue
    for r in p._p.iter(qn('w:r')):
        hl_ = r.getparent()
        if ''.join(x.text or '' for x in r.iter(qn('w:t'))).strip() in ('PDF', 'MP4') and _fieldlink(r): continue   # 21 Oct: a field link (5.3 "Supplemental Videos")
        if hl_.tag == qn('w:hyperlink') and ''.join(x.text or '' for x in hl_.iter(qn('w:t'))).strip() in ('PDF', 'MP4'): continue   # shown as the site's badge, not as text
        rp = r.find(qn('w:rPr'))
        on = lambda tag, off: rp is not None and rp.find(qn(tag)) is not None and rp.find(qn(tag)).get(qn('w:val')) not in off
        v = (1 if on('w:i', ('0', 'false')) else 0) + (2 if on('w:b', ('0', 'false')) else 0) + (4 if on('w:u', ('none', None)) else 0)
        rs_ = rp.find(qn('w:rStyle')) if rp is not None else None   # Word's character style (5.3: "Emphasis" is italic)
        if rs_ is not None and rs_.get(qn('w:val')) in CSTY:   # the character style's italic/bold/underline, unless the run sets its own (5.4: a Hyperlink run with underline none)
            sv = CSTY[rs_.get(qn('w:val'))]
            for bit, tag in ((1, 'w:i'), (2, 'w:b'), (4, 'w:u')):
                if rp.find(qn(tag)) is None: v |= sv & bit
        for ch in ''.join(x.text or '' for x in r.iter(qn('w:t'))):
            if ch.isspace(): continue
            WS_.append(ch); WF.append(v)
PT, PF = G['chars'][0], [int(x, 16) for x in G['chars'][1]]   # bit 8: the letter is in a label (micro-label)
WT = ''.join(WS_).replace('–', '-').replace('—', '-')
bad = []
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, WT, PT, autojunk=False).get_opcodes():
    if op != 'equal': continue
    for k in range(i2 - i1):
        wv, pv = WF[i1 + k], PF[j1 + k]
        lost = [nm for bit, nm in ((1, 'italic'), (2, 'bold'), (4, 'underline')) if wv & bit and not pv & bit and not (bit == 2 and pv & 8 and SET.get('LABELS_AS_TEMPLATE'))]   # 21 Oct (5.3, user 11:16 "correct ... so your page follows the template"): labels regular as the template sets them
        added = [nm for bit, nm in ((1, 'italic'), (2, 'bold')) if pv & bit and not wv & bit]
        if lost or added: bad.append((i1 + k, ', '.join(['%s lost' % x for x in lost] + ['%s added' % x for x in added])))
if SET.get('FORMAT_EDITS'):   # 21 Oct 19:38 (5.3, user: "change from italics to bold"): words whose formatting the user changed from Word's are allowed their new formatting
    _fe = set()
    for t_ in SET['FORMAT_EDITS']:
        c_ = ''.join(ch for ch in t_ if not ch.isspace() and ch not in '‘’“”"\'')
        _wq = [(i_, ch) for i_, ch in enumerate(WT) if ch not in '‘’“”"\'']   # 22 Oct 2026 (5.5 "teacher's guide"): Word's letters without quotation marks, each with its place
        _ws = ''.join(ch for _, ch in _wq)
        for m_ in re.finditer(re.escape(c_), _ws): _fe.update(range(_wq[m_.start()][0] - 1, _wq[m_.end() - 1][0] + 2))
    bad = [(pos, what) for pos, what in bad if pos not in _fe]
groups = []
for pos, what in bad:
    if groups and pos - groups[-1][1] <= 1 and groups[-1][2] == what: groups[-1][1] = pos
    else: groups.append([pos, pos, what])
fails_c = ['%s: "%s" (in "...%s...")' % (w, WT[a:b + 1][:30], WT[max(0, a - 15):b + 16]) for a, b, w in groups]
out('C formatting (letter by letter)', fails_c, len(WT))

# D dividers
fails = []
page_rules = G['rules']; pdf_rules = [t for _, _, t in thin]
if SET.get('NO_DIVIDER_BEFORE'):   # 21 Oct: lines the page setting leaves out before headings of those Word colours
    _cols = [c_ for c_ in SET['NO_DIVIDER_BEFORE'] if re.fullmatch(r'[0-9A-F]{6}', c_)]; _txts = [nz(c_) for c_ in SET['NO_DIVIDER_BEFORE'] if c_ not in _cols]   # 21 Oct 13:34: a Word colour, or a heading's own words
    pdf_rules = [t for t in pdf_rules if not (any(k_.startswith(nz(t)[:18]) and v_ in _cols for k_, v_ in WC.items()) or any(x_[:min(len(x_), len(nz(t)))] == nz(t)[:min(len(x_), len(nz(t)))] and min(len(x_), len(nz(t))) >= 12 for x_ in _txts))]
if len(page_rules) != len(pdf_rules): fails.append('page has %d beige lines, PDF %d' % (len(page_rules), len(pdf_rules)))
for k, t in enumerate(pdf_rules[:len(page_rules)]):
    _a, _b = nz(page_rules[k])[:20], nz(t)[:20]; _n = min(len(_a), len(_b))   # 21 Oct: "Managing Colleagues" is 18 letters - compare the shorter
    if _n < 5 or _a[:_n] != _b[:_n]: fails.append('line %d: page puts it before "%s", PDF before "%s"' % (k + 1, page_rules[k][:35], t[:35]))
# 20 Oct 22:1x: lines a page setting places (DIVIDERS_BEFORE) are checked against the setting: one before each heading of that colour after the first, nowhere else
if SET.get('DIVIDERS_BEFORE'):
    _stop = next((i for i, p_ in enumerate(paras) if SET.get('RES_FROM') and p_.text.strip() == SET['RES_FROM']), len(paras))
    _isnum = lambda p_: p_._p.pPr is not None and p_._p.pPr.find(qn('w:numPr')) is not None
    want_ = [nz(p_.text) for p_ in paras[:_stop] if p_.text.strip() and not _isnum(p_) and WC.get(nz(p_.text)) == SET['DIVIDERS_BEFORE'] and len(p_.text.strip()) < 120][1:]   # 20 Oct 22:5x: headings only (not list lines, not the Resources titles)
    got_ = [nz(x) for x in G.get('setrules', [])]
    if len(got_) != len(want_) or any(not g.startswith(w[:20]) for g, w in zip(got_, want_)):   # 20 Oct 22:5x: a short heading (Circle Time) is matched by its start
        fails.append('setting lines before %s, wanted before %s' % (G.get('setrules'), want_))
elif SET.get('RULE_BEFORE'):   # 22 Oct 2026 (5.5, user: "divider 30/30 above"): lines the page setting places before the blocks it names, nowhere else
    got_ = [nz(x) for x in G.get('setrules', [])]; want_ = [nz(x) for x in SET['RULE_BEFORE']]
    if len(got_) != len(want_) or any(not g.startswith(w[:20]) for g, w in zip(got_, want_)):
        fails.append('setting lines before %s, wanted before %s' % (G.get('setrules'), SET['RULE_BEFORE']))
elif G.get('setrules'): fails.append('setting lines with no setting: %s' % G['setrules'])
if SET.get('RES_DIVIDERS'):   # 20 Oct 23:54: one line between each pair of Resources entries, none elsewhere
    n_, k_, all_ = G.get('resrules', [0, 0, 0])
    if SET['RES_DIVIDERS'] == 'all':   # 22 Oct 2026 (5.5, user: "divider 30/30 for red headings in resources"): a line above every entry, the first too
        if not (k_ == max(0, n_ - 1) and all_ == n_): fails.append('Resources: %d entries, %d lines between them, %d in all (want a line above each, %d)' % (n_, k_, all_, n_))
    elif not (k_ == all_ == max(0, n_ - 1)): fails.append('Resources: %d entries, %d lines between them, %d in all (want %d)' % (n_, k_, all_, max(0, n_ - 1)))
out('D dividers', fails, max(len(page_rules), len(pdf_rules)) + len(G.get('setrules', [])) + G.get('resrules', [0, 0, 0])[2])   # 21 Oct: the count includes the lines the settings place

# E overlaps
fails = []
for w in (1280, 768, 390): fails += ['%d: %s' % (w, x) for x in G['over%d' % w]]
out('E overlaps (photos loading late)', fails, 3)

# F lists
def fmt(k, cls):
    if 'mm-lroman' in cls or 'mm-uroman' in cls:
        v, o = k, ''
        for val, sym in ((1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')):
            while v >= val: o += sym; v -= val
        return o if 'mm-lroman' in cls else o.upper()
    if 'mm-mk-alpha-paren' in cls: return chr(96 + k)   # 20 Oct 23:2x: markers set by the page settings (LIST_MARKERS)
    if 'mm-lalpha' in cls: return chr(96 + k)
    if 'mm-ualpha' in cls: return chr(64 + k)
    return str(k)
pdflines = []   # (text, page, x0, y0, x1) in reading order
for pi_, pg in enumerate(pdf):
    for b_ in pg.get_text('dict')['blocks']:
        for l in b_.get('lines', []): pdflines.append((''.join(s['text'] for s in l['spans']), pi_, l['bbox'][0], l['bbox'][1], l['bbox'][2]))
NUM = re.compile(r'\s*([0-9]+|[ivxlcdm]+|[IVXLCDM]+|[a-zA-Z])[.)]')
fails = []; at = 0
for num, cls, t in G['lis']:
    k = nz(t)[:40]
    if not k: continue
    hit = next((i for i in range(at, len(pdflines)) if nz(pdflines[i][0]).startswith(k[:25]) or k[:25] in nz(pdflines[i][0])), None)   # in order: the next PDF line with this text
    if hit is None: continue
    at = hit + 1; ln, pn, x0, y0, x1 = pdflines[hit]
    m = NUM.match(ln)
    if not m:   # Word's own numbering: the PDF writes the number as a line of its own, level with the text, to its left
        lab = [x for x in pdflines if x[1] == pn and abs(x[3] - y0) < 3 and x[4] <= x0 + 1 and NUM.fullmatch(x[0].strip() + ('' if x[0].strip()[-1:] in '.)' else '.'))]
        m = NUM.match(lab[-1][0]) if lab else None
    if m is None: fails.append('"%s": page %s., the PDF shows no number' % (t[:35], fmt(num, cls)))
    elif cls == 'mm-mk-alpha-paren' and SET.get('LIST_MARKERS'):
        pass   # 20 Oct 23:2x: the page settings set a) b) c) here (LIST_MARKERS); the letter is checked by its count
    elif m.group(1).lower() != fmt(num, cls).lower(): fails.append('"%s": page %s., PDF %s' % (t[:35], fmt(num, cls), m.group(1)))
# 21 Oct (proof: renaming the a) b) c) class passed F, because those lines match no PDF line and were skipped): a list the
# settings mark (LIST_MARKERS) must carry those markers on the page
for _start, _kind in SET.get('LIST_MARKERS', {}).items():
    _its = [x for x in G['lis'] if x[2].startswith(_start)]
    if not _its: fails.append('LIST_MARKERS: no list item starts "%s"' % _start)
    elif any(x[1] != 'mm-mk-' + _kind for x in _its): fails.append('LIST_MARKERS: "%s" does not show %s markers' % (_start, _kind))
out('F lists', fails, len(G['lis']))

# G tab gaps
out('G tab gaps', G['tabs'], 1)

# I space runs
out('I space runs (Word lines things up with spaces)', G['gaps'], len(GAPS))

def _pdfwords(pg):   # the word PDF inside a web link (link boxes overlap the next line, so the word, not the box)
    lr = [ln['from'] for ln in pg.get_links() if ln.get('uri')]
    return [w for w in pg.get_text('words') if w[4] in ('PDF', 'MP4') and any(r.x0 <= (w[0] + w[2]) / 2 <= r.x1 and r.y0 <= (w[1] + w[3]) / 2 <= r.y1 for r in lr)]
# J PDF badges - every PDF link has a badge, on the PDF's line, with the PDF's place (data-tabx); badges on neighbouring
# lines in one column at 1280 and 768 (within 1px); a badge on its own line at the margin; none closer than 23px to its text
fails = []; bd = G['badges']
pw = []
for pg in pdf:
    mg = min((w[0] for w in pg.get_text('words')), default=0)
    pw += [(pg.number, w[1], round(w[0] - mg, 1)) for w in _pdfwords(pg)]
pw = [x[2] for x in sorted(pw)]
_wpdf = sum(1 for h_ in D.element.body.iter(qn('w:hyperlink')) if ''.join(t_.text or '' for t_ in h_.iter(qn('w:t'))).strip() in ('PDF', 'MP4'))   # 21 Oct 2026 (5.5): Word's own PDF links - the PDF made from Word lost 2 of them
if len(bd) != len(pw) and len(bd) != _wpdf: fails.append('page has %d PDF badges, the PDF %d PDF links, Word %d' % (len(bd), len(pw), _wpdf))
for k_, (x, want) in enumerate(zip(bd, pw) if any(x[0] for x in bd) and not SET.get('PDF_COLUMN') else []):   # PDF places: pages whose badges carry them (a Word list part)
    if x[0] is None or abs(float(x[0]) - want) > 0.5: fails.append('badge %d ("%s") has PDF place %s, the PDF %.1f' % (k_ + 1, x[4][:30], x[0], want))
for w in (1280, 768):   # 20 Oct (your rule): badges on neighbouring lines stand in one column
    for g in G.get('bgrp%d' % w, []):
        if len(g) > 1 and max(x[0] for x in g) - min(x[0] for x in g) > 1:
            fails.append('%d: badges from "%s" to "%s" not in one column (%d-%dpx)' % (w, g[0][1], g[-1][1], min(x[0] for x in g), max(x[0] for x in g)))
for w in (1280, 768, 390):   # every width: a badge on a line of its own starts at the margin; beside its text, 24 or more from it
    for own, left, gap, t in G.get('bown%d' % w, []):
        if own and abs(left) > 1: fails.append('%d: badge on its own line %dpx in from the margin: "%s"' % (w, left, t))
        if not own and gap is not None and gap < 23: fails.append('%d: badge %dpx from its text: "%s"' % (w, gap, t))
if SET.get('PDF_COLUMN') == 'longest':   # 21 Oct 12:2x (user, 5.2): "One column, 24 px after longest" - the column stands 24 after the longest line
    _g = [x[1] - x[2] for x in bd if x[2] is not None]
    if not _g or abs(min(_g) - 24) > 1: fails.append('PDF_COLUMN: the closest badge is %s px after its text, wanted 24' % (round(min(_g), 1) if _g else None))
    if any(x[0] for x in bd): fails.append('PDF_COLUMN: badges still carry the PDF place (data-tabx)')
out('J PDF badges', fails, len(bd))

# H words
r = json.load(open(os.path.join(os.path.dirname(PV), 'report.json')))
def UK(a):   # the UK spellings the site rules allow: only these exact changes pass
    w = a
    for us, uk in ((r'(?<!\bs)(?<!\bpr)(?<!\bse)(?<!caps)(?<!\bmaz)iz(e|ed|es|ing|ation|ations)\b', r'is\1'),
                   (r'\b((?i:behavi|col|fav|hon|lab|neighb|hum|flav|harb|rum|endeav|vap|savi|arm|od|val|vig|rig|splend|parl|tum))or(s|ed|ing|ite|ites|ful|al)?\b', r'\1our\2'),
                   (r'\bprogram(s?)\b', r'programme\1'), (r'\bProgram(s?)\b', r'Programme\1'),
                   (r'enroll(ment|ments)\b', r'enrol\1'), (r'practic(ed|ing)\b', r'practis\1'), (r'\b(grovel|model)ing\b', r'\1ling')):
        w = re.sub(us, uk, w)
    return w
def SITE(a, b):
    a = re.sub(r'\blead guide\b', 'Lead Guide', a, flags=re.I)
    for o_, n_ in SET.get('TEXT_EDITS', []): a = a.replace(o_.rstrip('.'), n_.rstrip('.'))
    if any(a and a in o_ and b in n_ and o_[::-1].replace(a[::-1], b[::-1], 1)[::-1] == n_ for o_, n_ in SET.get('TEXT_EDITS', [])): return True   # 21 Oct: the changed piece alone ("Mon" -> "Montessori classes.")
    if any(a and a in o_ and b in n_ and o_.find(a) == n_.find(b) and len(o_) == len(n_) for o_, n_ in SET.get('TEXT_EDITS', [])): return True   # 21 Oct 19:38 (5.3, user: single quotation marks): one of several changed pieces, at the same place in the user's old and new wording
    if (a, b) in [(o_, n_) for o_, n_ in SET.get('TEXT_EDITS', [])] or any(a in o_ and b in n_ and a.replace(';', ':') == b for o_, n_ in SET.get('TEXT_EDITS', [])): return True   # 20 Oct 22:10 (user): 'Lead Guide' always capitalised
    c = a.replace(' / ', '/').replace(' /', '/').replace('/ ', '/').replace('–', '-').replace('—', '-')
    if c.lower() == b.lower() and re.search(r'lead', c, re.I): return True   # Lead Guide capitalised (user)
    return b in (c, UK(c), UK(a))
dropped = lambda o, a, b: o == 'delete' and any(a.startswith(t) for t in SET.get('DROP', []))   # left out by the page settings (DROP)
# 21 Oct 2026 (5.5 "a. Sweep & Scan"): a label Word numbers itself shows Word's number, as the PDF does - the number is not in Word's text
def _labnums():
    out_ = []; cnt = {}
    try: nmx = D.part.numbering_part.element
    except Exception: return out_
    fmts = {}
    for an in nmx.findall(qn('w:abstractNum')):
        for lv in an.findall(qn('w:lvl')):
            nf = lv.find(qn('w:numFmt')); fmts[(an.get(qn('w:abstractNumId')), lv.get(qn('w:ilvl')))] = nf.get(qn('w:val')) if nf is not None else 'decimal'
    nm = {n.get(qn('w:numId')): n.find(qn('w:abstractNumId')).get(qn('w:val')) for n in nmx.findall(qn('w:num'))}
    for q in paras:
        t = q.text.strip(); pPr = q._p.pPr; np_ = pPr.find(qn('w:numPr')) if pPr is not None else None
        if not t or np_ is None or np_.find(qn('w:numId')) is None: continue
        vis = [r for r in q.runs if r.text.strip()]
        if not vis or len(t) >= 70 or re.search(r'[.;,]$', t) or sum(len(r.text.strip()) for r in vis if r.bold) / max(1, sum(len(r.text.strip()) for r in vis)) <= 0.9: continue
        nid = np_.find(qn('w:numId')).get(qn('w:val')); il = np_.find(qn('w:ilvl')).get(qn('w:val')) if np_.find(qn('w:ilvl')) is not None else '0'
        cnt[nid] = cnt.get(nid, 0) + 1; k = cnt[nid]; fm = fmts.get((nm.get(nid), il), 'decimal')
        out_.append((chr(96 + k) if fm == 'lowerLetter' else chr(64 + k) if fm == 'upperLetter' else str(k)) + '.')
    return out_
_LN = _labnums(); _LN2 = list(_LN)
def labnum(o, a, b):
    if o == 'insert' and a == '' and b in _LN: _LN.remove(b); return True
    return False
# an attribution Word sets as a list line with a dash bullet, straight after a quotation, shows its dash as text: allowed once each
def _dash_cites():
    try: nmx = D.part.numbering_part.element
    except Exception: return 0
    lvl = {}
    for an in nmx.findall(qn('w:abstractNum')):
        aid = an.get(qn('w:abstractNumId'))
        for lv in an.findall(qn('w:lvl')):
            t = lv.find(qn('w:lvlText')); lvl[(aid, lv.get(qn('w:ilvl')))] = t.get(qn('w:val')) if t is not None else ''
    nm = {n.get(qn('w:numId')): n.find(qn('w:abstractNumId')).get(qn('w:val')) for n in nmx.findall(qn('w:num'))}
    k = 0; prev = None
    for q in paras:
        if not q.text.strip(): continue
        pPr = q._p.pPr; np_ = pPr.find(qn('w:numPr')) if pPr is not None else None
        if np_ is not None and np_.find(qn('w:numId')) is not None:
            a_ = nm.get(np_.find(qn('w:numId')).get(qn('w:val'))); il = np_.find(qn('w:ilvl')).get(qn('w:val')) if np_.find(qn('w:ilvl')) is not None else '0'
            if lvl.get((a_, il), '') in ('-', '–', '‐') and prev is not None and sum(len(r.text) for r in prev.runs if r.italic) > 0.5 * max(1, len(prev.text)): k += 1
        prev = q
    return k
_dc = [_dash_cites()]
def dashok(o, a, b):
    if o == 'insert' and a == '' and b == '-' and _dc[0] > 0: _dc[0] -= 1; return True
    return False
def _period(o, a, b):   # the full stop may come with a wording change the user made (TEXT_EDITS)
    for o_, n_ in SET.get('TEXT_EDITS', []): a = a.replace(o_, n_)
    return SET.get('ENTRY_PERIOD') and o == 'replace' and b == a.rstrip() + '.'   # 21 Oct 12:21 (user): a full stop after each school
fails = ['%s: "%s" -> "%s"' % (o, a[:40], b[:40]) for o, a, b in r['text_differences_word_vs_page'] if not SITE(a, b) and not dropped(o, a, b) and not dashok(o, a, b) and not _period(o, a, b) and not labnum(o, a, b)]
out('H words (site rules left out)', fails, len(r['text_differences_word_vs_page']))
# H2 words, from the page itself (20 Oct 21:4x: H reads the build's report, so a page changed after the build got past it) -
# every letter of Word (title and DROP left out; badges' PDF/MP4 left out) against every letter the page shows, after the site's
# rules are applied to Word's text: short dashes, UK spellings, spaces round slashes (letters only, so spacing does not count)
_dc_left = [_dash_cites()]
WT2 = re.sub(r'leadguide', 'LeadGuide', ''.join(WS_), flags=re.I)
WT2 = re.sub(r'(grovel|model)ing', r'\1ling', WT2)   # UK spellings (site rule)
for o_, n_ in SET.get('TEXT_EDITS', []): WT2 = WT2.replace(re.sub(r'\s', '', o_), re.sub(r'\s', '', n_))   # wording the user changed   # 20 Oct 22:10 (user): 'Lead Guide' always capitalised
for a_, b_ in (('–', '-'), ('—', '-')): WT2 = WT2.replace(a_, b_)
uk_words = []
fails = []
sm = difflib.SequenceMatcher(None, WT2, PT, autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal': continue
    a_, b_ = WT2[max(0, i1 - 12):i2 + 12], PT[max(0, j1 - 12):j2 + 12]
    if UK(a_) == b_ or (op == 'replace' and UK(WT2[max(0, i1 - 30):i2 + 30]).replace(' ', '') == PT[max(0, j1 - 30):j2 + 30]): continue
    if op == 'replace' and re.fullmatch(r'z+', WT2[i1:i2]) and re.fullmatch(r's+', PT[j1:j2]): continue   # -ize -> -ise (site rule)
    if op == 'insert' and PT[j1:j2] in ('u',) and re.search(r'o$', WT2[:i1]): continue
    if op == 'insert' and PT[j1:j2] == 'l' and re.search(r'(grovel|model)$', WT2[:i1], re.I): continue   # grovelling, modelling (UK)                     # -or -> -our (site rule)
    if op == 'insert' and PT[j1:j2] == 'me' and WT2[:i1].lower().endswith('program'): continue          # program -> programme (site rule)
    if op == 'insert' and PT[j1:j2] == '.' and SET.get('ENTRY_PERIOD'): continue   # 21 Oct 12:21 (user): a full stop after each school
    if op == 'insert' and PT[j1:j2] == '-' and _dc_left[0] > 0: _dc_left[0] -= 1; continue                    # dash shown before a Word dash-bullet attribution
    if op == 'insert' and PT[j1:j2] in _LN2: _LN2.remove(PT[j1:j2]); continue   # 21 Oct 2026 (5.5): Word's own number on a label, as the PDF shows it
    if op == 'replace' and WT2[i1:i2] == 'c' and PT[j1:j2] == 's' and re.search(r'practi$', WT2[:i1], re.I): continue   # 21 Oct 2026 (5.5): practiced -> practised (site rule) where no word boundary follows in the letters-only text
    fails.append('%s: Word "%s" -> page "%s" (in "...%s...")' % (op, WT2[i1:i2][:30], PT[j1:j2][:30], PT[max(0, j1 - 20):j2 + 20]))
out('H2 words from the page (letters, site rules allowed)', fails, len(WT2))

# K list indents (1280): every list's marker and the start of its text against Word's indent for its first item (1px tolerance)
_nx = zw.read('word/numbering.xml').decode('utf-8') if 'word/numbering.xml' in zw.namelist() else ''
_nm = dict(re.findall(r'<w:num w:numId="(\d+)"[^>]*>.*?<w:abstractNumId w:val="(\d+)"/>', _nx, re.S))
def _lvl(nid):
    m_ = re.search(r'<w:abstractNum [^>]*w:abstractNumId="%s".*?</w:abstractNum>' % _nm.get(nid, '-1'), _nx, re.S)
    lv = re.search(r'<w:lvl w:ilvl="0".*?</w:lvl>', m_.group(0), re.S) if m_ else None
    g = lambda k: int((re.search(r'<w:ind [^>]*w:%s="(\d+)"' % k, lv.group(0)) or [0, 0])[1]) if lv else 0
    return g('left'), g('hanging'), g('firstLine')
fails = []; n = 0
for txt, mk, tx, mkr in G.get('lists', []):
    k_ = nz(txt)[:30]
    q = next((p for p in paras if p.text.strip() and nz(p.text)[:30] and k_.startswith(nz(p.text)[:min(30, len(nz(p.text)))])), None)
    if q is None or q._p.pPr is None or q._p.pPr.find(qn('w:numPr')) is None: continue
    pPr = q._p.pPr; L, Hh, F = _lvl(pPr.find(qn('w:numPr')).find(qn('w:numId')).get(qn('w:val')))
    ind = pPr.find(qn('w:ind'))
    if ind is not None:
        if ind.get(qn('w:left')) is not None: L = int(ind.get(qn('w:left')))
        if ind.get(qn('w:hanging')) is not None: Hh, F = int(ind.get(qn('w:hanging'))), 0
        if ind.get(qn('w:firstLine')) is not None: F, Hh = int(ind.get(qn('w:firstLine'))), 0
    wm, wt = ((L + F) / 15, ((L + F) // 720 + 1) * 720 / 15) if F else ((L - Hh) / 15, L / 15)
    nid_ = pPr.find(qn('w:numPr')).find(qn('w:numId')).get(qn('w:val')); am_ = re.search(r'<w:abstractNum [^>]*w:abstractNumId="%s".*?</w:abstractNum>' % _nm.get(nid_, '-1'), _nx, re.S)
    jc_ = re.search(r'<w:lvl w:ilvl="0".*?<w:lvlJc w:val="(\w+)"', am_.group(0), re.S) if am_ else None
    if jc_ and jc_.group(1) == 'right': mk = mkr   # a right-aligned Word number: its right edge is at the marker position
    _il = pPr.find(qn('w:numPr')).find(qn('w:ilvl')); _il = _il.get(qn('w:val')) if _il is not None else '0'   # 21 Oct 2026 (5.5): the line's own list level (a dash line at level 2 of a numbered list)
    fm_ = re.search(r'<w:lvl w:ilvl="%s".*?<w:numFmt w:val="(\w+)"' % _il, am_.group(0), re.S) if am_ else None
    if fm_ and fm_.group(1) == 'bullet':   # 21 Oct 2026 (user, preferences 21 Oct: "text margin, then a space of 24, then the dash, then a space of 24, then the word - at every width"): a dash list against that rule, not Word's indent
        n += 1
        if abs(mk - 24) > 1 or abs(tx - (mkr + 24)) > 1: fails.append('"%s": dash at %.1f, word at %.1f; the rule: dash at 24, word 24 after the dash (%.1f)' % (txt[:35], mk, tx, mkr + 24))
        continue
    if SET.get('OL_AT_MARGIN') and fm_ and fm_.group(1) != 'bullet' and not (jc_ and jc_.group(1) == 'right'): wm, wt = 0.0, wt - wm   # 21 Oct 18:4x (user rule 20 Oct: "numbered lists always start at the left margin"): the list moved left, Word's number-to-text gap kept
    if fm_ and fm_.group(1) != 'bullet' and not (jc_ and jc_.group(1) == 'right'):   # 22 Oct 2026 04:05 (user, the A/B question: "Numbered lists: 30"): the number at the margin, the text 30 from it
        n += 1
        if abs(mk) > 1 or abs(tx - 30) > 1: fails.append('"%s": number at %.1f, text at %.1f; the rule: number at 0, text at 30' % (txt[:35], mk, tx))
        continue
    n += 1
    if abs(mk - wm) > 1 or abs(tx - wt) > 1: fails.append('"%s": page marker %.1f, text %.1f; Word %.1f, %.1f' % (txt[:35], mk, tx, wm, wt))
out('K list indents (Word)', fails, n)

# P photos beside text: top level with the top of the first line's letters (or centred on the text, mm-mid) at 1280 and 768
fails = []; n = 0
for w in (1280, 768):
    for nm_, kind, off, t in G.get('float%d' % w, []):
        n += 1
        if abs(off) > 1: fails.append('%d: %s (%s, beside "%s") off by %.1fpx' % (w, nm_, kind, t, off))
out('P photo tops beside text', fails, n)
# S slash breaks (21 Oct, user: "Allow breaks after "/""): every slash between two letters in the page text may break - a <wbr> follows it
from bs4 import BeautifulSoup as _BS
_sp = _BS(open(os.path.join(PV, 'index.html'), encoding='utf-8').read(), 'html.parser'); _m = _sp.find('main') or _sp
fails = []; n = 0
for _t in _m.find_all(string=True):
    if _t.parent.name in ('script', 'style') or re.search(r'https?:|www\.', str(_t)): continue
    for _x in re.finditer(r'(?<=\w)/(?=\w)', str(_t)): n += 1; fails.append('no break after "/" in "%s"' % str(_t)[max(0, _x.start() - 20):_x.end() + 20])
    if re.search(r'\w/$', str(_t)):
        n += 1; _nx = _t.next_sibling
        if not (getattr(_nx, 'name', None) == 'wbr'): fails.append('no break after "/" in "%s"' % str(_t)[-30:])
out('S slash breaks', fails, n)
# T copy spaces (21 Oct, 4th check): a label or typed number ends in a no-break space, so copied text keeps the space ("Classroom Flow Traffic", "2. How")
fails = []; n = 0
for _x in _m.select('span.mm-lab, span.mm-n'):
    n += 1
    if not _x.get_text().endswith(' '): fails.append('no space kept after "%s"' % _x.get_text()[:30])
out('T copy spaces after labels and numbers', fails, n)
print('\nALL PASS' if not any(res.values()) else '\nFAILURES: ' + ', '.join(k for k, v in res.items() if v))
