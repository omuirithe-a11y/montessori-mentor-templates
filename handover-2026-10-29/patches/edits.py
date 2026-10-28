"""Essay template edits, 27 Oct (owner 19:01 "fix them all"). apply(text) -> text; each old string must occur exactly once."""
N = '27 Oct 2026 (owner, 19:01: fix them all)'
EDITS = [
 ('1 no contents box without entries',
  '.toc-wrap{max-width:1100px;margin:0 auto;padding:26px 0 36px}',
  '.toc-wrap{max-width:1100px;margin:0 auto;padding:26px 0 36px}\n.toc-wrap:not(:has(li)){display:none}   /* %s: no "Table of contents" box when it has no entries */' % N),
 ('2 current page in the menu marked and underlined',
  '<script id="mm-menu-js">',
  '<script id="mm-current-js">/* %s; her rule: the current page is underlined): the menu link to this page, and the top name of its group, get aria-current="page", which the menu styles .menu .top[aria-current] and .grp a[aria-current] underline. A page may also carry the mark in its menu markup. */(function(){var p=location.pathname.replace(/index\\.html$/,\'\');[].forEach.call(document.querySelectorAll(\'.menu a[href]\'),function(a){if(a.getAttribute(\'href\')!==p)return;a.setAttribute(\'aria-current\',\'page\');var li=a.closest(\'.has-panel\'),t=li&&li.querySelector(\':scope > .top\');if(t&&t!==a)t.setAttribute(\'aria-current\',\'page\');});})();</script><script id="mm-menu-js">' % N.replace(')', '')),
]
def apply(s, only=None):
    for name, old, new in EDITS:
        if only is not None and name.split()[0] not in only: continue
        assert s.count(old) == 1, 'edit %s: found %d times' % (name, s.count(old))
        s = s.replace(old, new)
    return s

COLS = ['0432FF', '00B050', 'EE0000', '7030A0', 'FB0207', '0000FF', '2CC171', 'ED2AFB', 'FBEF32', '66CCFF', 'CC66FF', 'FFFFFF', '996633',
        'FF0000', 'FFDD60', '008F00', 'FF9300', '521B93', 'FF3FFF', '945200', '797979']
CSS = ('<style id="mm-owner-27oct">/* ' + N + ' */\n'
 '/* 3: a caption sits clear of its image - its letters\' box stood 1px into the image above it */\n'
 'html body main .mm-cap{padding-top:2px}\n'
 '/* 4: two photos in one figure (a pair with one caption) stand side by side, 24 apart at the row height of 170, as one photo of the row */\n'
 'html body main figure.ph > div:not(.pim):has(> .pim + .pim){display:flex;align-items:flex-start}\n'
 'html body main figure.ph > div:not(.pim) > .pim{flex:none}\n'
 'html body main figure.ph > div:not(.pim) > .pim + .pim{margin-left:calc(var(--mh,153) * 24px / 170)}\n'
 '/* 7, 8, 9, 13, 15: words in their Word colour, inside text too (material names, labels, colour words, list items, captions, key lines, names). Orange Word text stays the ink colour, and so does black. */\n'
 + ''.join('html body main .mm-hc-%s:not(h2){color:#%s !important}\n' % (c, c) for c in COLS) +
 '/* 14: every name line is blue, 20px, regular - also one with no beige line straight above it */\n'
 'html body main p.mm-name{color:#0432FF !important;font-weight:400 !important}\n'
 'html body main p.mm-name:not(.mm-gl):not(.mm-cap){font-size:20px !important}\n'
 '/* 16: a heading bold in Word is bold */\n'
 'html body main h2[data-notred]{font-weight:700 !important}\n'
 '/* 17: the green heading - 20px (19 on phones), regular, no line under it */\n'
 'html body main h2.mm-hc-00B050{color:#00B050 !important;font-size:20px !important;font-weight:400 !important;border-bottom:0 !important;padding-bottom:0 !important}\n'
 '@media (max-width:640px){html body main h2.mm-hc-00B050{font-size:19px !important}}\n'
 '</style>')
SHAPE = ('<script id="mm-shape-js">/* ' + N + ', 10, 11, 18: the page shows a photo turned (data-rot) and cut (data-crop) as Word did, as the lightbox already does; '
 'a numbered list that continues (start) goes on from that number */(function(){'
 "[].forEach.call(document.querySelectorAll('main img.doc-img[data-rot],main img.doc-img[data-crop]'),function(im){var p=im.parentElement;if(!p||!p.classList.contains('pim')||im.closest('.mm-pdf'))return;"
 "var rot=((+im.getAttribute('data-rot')||0)%360+360)%360,c=(im.getAttribute('data-crop')||'0,0,0,0').split(',').map(Number);if(c.length!==4||c.some(isNaN))c=[0,0,0,0];if(rot%180)c=[0,0,0,0];"
 "if(!rot&&!c.some(function(x){return x>0;}))return;var W=+im.getAttribute('width'),H=+im.getAttribute('height');if(!W||!H)return;"
 "var cw=1-c[0]-c[2],ch=1-c[1]-c[3],dw=W*cw,dh=H*ch;if(rot%180){var t=dw;dw=dh;dh=t;}var ar=dw/dh,st=p.getAttribute('style')||'';"
 "p.setAttribute('style',(/aspect-ratio:\\s*[0-9.]+/.test(st)?st.replace(/aspect-ratio:\\s*[0-9.]+/,'aspect-ratio:'+ar.toFixed(5)):st+';aspect-ratio:'+ar.toFixed(5)).replace(/^;/,''));"
 "p.style.setProperty('overflow','hidden','important');var s=function(k,v){im.style.setProperty(k,v,'important');};s('position','absolute');s('max-width','none');s('max-height','none');s('object-fit','fill');"
 "if(rot%180){s('left','50%');s('top','50%');s('width',(100/ar).toFixed(4)+'%');s('height',(100*ar).toFixed(4)+'%');s('transform','translate(-50%,-50%) rotate('+rot+'deg)');}"
 "else{s('width',(100/cw).toFixed(4)+'%');s('height',(100/ch).toFixed(4)+'%');s('left',(-100*c[0]/cw).toFixed(4)+'%');s('top',(-100*c[1]/ch).toFixed(4)+'%');s('transform',rot===180?'rotate(180deg)':'none');}});"
 "[].forEach.call(document.querySelectorAll('main ol[start]'),function(o){var n=parseInt(o.getAttribute('start'),10);if(!isNaN(n))o.style.setProperty('counter-reset','mmn '+(n-1),'important');});"
 '})();</script>')
EDITS += [
 ('4a row: a figure holding a pair counts both photos',
  "var m = /aspect-ratio:\\s*([0-9.]+)/.exec(f.querySelector('.pim').getAttribute('style') || ''); return m ? parseFloat(m[1]) : 1; }); }",
  "var ps = q('.pim', f), s = 0; ps.forEach(function(p){ var m = /aspect-ratio:\\s*([0-9.]+)/.exec(p.getAttribute('style') || ''); s += m ? parseFloat(m[1]) : 1; }); return s + (ps.length - 1) * 24 / 170; }); }   // %s (4): a pair in one figure is as wide as both photos and the 24 between them" % N),
 ('4b side photo never lifted into the text above it',
  "var base = s2.getBoundingClientRect().top, mt = parseFloat(getComputedStyle(f).marginTop) || 0, want = k0[2] + h;",
  "var base = s2.getBoundingClientRect().top, mt = parseFloat(getComputedStyle(f).marginTop) || 0, want = k0[2] + h;\n        var pv0 = s2.previousElementSibling, ik0 = pv0 ? ink(pv0) : null, pb0 = ik0 ? ik0[3] : -1e9; want = Math.max(want, Math.min(k0[2], pb0 + 30));   // %s (4): centred on its text, but never into the text above - at most level with its own first line, or 30 below the letters above" % N),
 ('6 phones: a side photo standing alone keeps 16 to the text after it, as to the text before it',
  "      if (rowText && a.type === 'row'",
  "      if (ph && a.type === 'row' && a.el.classList && a.el.classList.contains('mm-float') && (b.type === 'text' || b.type === 'li')) return 16;   // %s (6): a photo beside text that stands alone on a phone or tablet: 16 below it, as above it (it is not a row: the 64 after rows is not for it)\n      if (rowText && a.type === 'row'" % N),
 ('10 11 18 shapes and list numbers', '</main><aside class="mc-band">', '</main>' + SHAPE + '<aside class="mc-band">'),
 ('3 7 8 9 13 14 15 16 17 css', '</script></body>', '</script>' + CSS + '</body>'),
]
EDITS += [
 ('20 a line space is not measured across a photo standing in the flow',
  "function run0(){[].forEach.call(document.querySelectorAll('main [data-gap]'),function(el){var want=",
  "function run0(){[].forEach.call(document.querySelectorAll('main [data-gap]'),function(el){var pv=tgt(el).previousElementSibling;while(pv&&pv.classList.contains('mm-fspacer'))pv=pv.previousElementSibling;if(pv&&pv.querySelector('.pim')&&getComputedStyle(pv).float==='none'&&getComputedStyle(pv).display!=='contents')return;var a0=lastBase(el),b0=firstTop(el),er=el.getBoundingClientRect();if(a0!==null&&b0!==null&&[].some.call(document.querySelectorAll('main .pim'),function(p){if(el.contains(p))return false;var r=p.getBoundingClientRect();return r.height>0&&r.top<Math.max(a0,b0)&&r.bottom>Math.min(a0,b0)&&r.left<er.right&&r.right>er.left;}))return;   /* %s (20): a photo stands in the flow just above (on phones a PDF-placed photo or a side photo): the space is the page's own from the photo - measured from the text above the photo it pulled the line up over the photo; so also when any photo stands between the text above and this line, as the phone layout of a set does */var want=" % N),
]
EDITS += [
 ('4c a row ends at the foot of its captions',
  "if (it.type === 'row' || it.type === 'strip') { var p = q('.pim', it.el).map(function(x){ return x.getBoundingClientRect().bottom; });",
  "if (it.type === 'row' || it.type === 'strip') { var p = q('.pim, .mm-cap', it.el).map(function(x){ return x.getBoundingClientRect().bottom; });   /* %s (3, 4, 6): a row - or a photo standing alone on a phone - ends at the foot of its captions, so the text after it is measured from them, not run under them */" % N),
]
EDITS += [
 ('4d the 40 under a row of photos is taken from the foot of its captions',
  "      var b = edge0(rw); if (b === null) return;",
  "      var b = edge0(rw); if (b === null) return; q('.mm-cap', rw).forEach(function(c){ var cr = c.getBoundingClientRect(); if (cr.height && cr.bottom > b) b = cr.bottom; });   // %s (4): captions under the photos are part of the row - the text was pulled up under them" % N),
]
EDITS += [
 ('21 data-centre-lines "p" and "all" understood, never an error',
  "if (cl) { var ps = q('.mm-text > p', s), ab = cl.split('-').map(Number), k1 = ink(ps[ab[0] - 1]), k2 = ink(ps[ab[1] - 1]);",
  "if (cl) { var ps = q('.mm-text > p', s), ab = cl.split('-').map(Number), e1 = null, e2 = null;   // %s (21): \"p\" - centred on its paragraphs (first to last), \"all\" - on the whole text, \"a-b\" - between paragraphs a and b; any other value is left alone (it stopped the layout with an error)\n            if (cl === 'p') { e1 = ps[0]; e2 = ps[ps.length - 1]; } else if (cl === 'all') { e1 = tx.firstElementChild; e2 = tx.lastElementChild; } else if (ab.length === 2 && !ab.some(isNaN)) { e1 = ps[ab[0] - 1]; e2 = ps[ab[1] - 1]; }\n            var k1 = e1 ? ink(e1) : null, k2 = e2 ? ink(e2) : null;" % N),
]
EDITS += [
 ('22 a data-step never puts a line over the line above it',
  "        return parseFloat(dstep) * U - lm(a.el)[0]; }",
  "        var tr = function(el, last){ var r = document.createRange(), w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n, v = null; while ((n = w.nextNode())) { if (!n.nodeValue.trim()) continue; r.selectNodeContents(n); Array.prototype.forEach.call(r.getClientRects(), function(x){ if (x.width < 1 || x.height < 5) return; v = v === null ? (last ? x.bottom : x.top) : (last ? Math.max(v, x.bottom) : Math.min(v, x.top)); }); } return v; };\n"
  "        var ra = tr(a.el, true), rb = tr(b.el, false), floor = (ra !== null && rb !== null) ? (ra - bot(a)) + (top(b) - rb) + 1 : 0;   // %s (22): the step is from the page's own line height (29.7, the live page had 37.2) - under a taller line (a name line, a label) it put the next line's letters over it; the space is never less than keeps the two lines' letter boxes 1px apart\n"
  "        return Math.max(parseFloat(dstep) * U - lm(a.el)[0], floor); }" % N),
]
EDITS += [
 ('23a a photo the PDF puts beside text stands in the column from 641 to 830, as the engine spaces it there',
  "html body main .mm-cap{padding-top:2px}\n",
  "html body main .mm-cap{padding-top:2px}\n/* 23: from 641 to 830 the spacing engine (phone(): 830 and narrower) spaces a photo the PDF puts beside text as a block in the column, as at 640 and narrower and as every other photo at these widths (the 24 Oct rule), but the styles still floated it beside the text: each pass pushed the text below the photo and the photo followed its line down - 950px of empty page above the Mathematics introduction, text run over photos and their captions. It now stands in the column at its PDF size, at its own side. */\n@media (min-width:641px) and (max-width:830px){html body main .mm-pdf-r,html body main .mm-pdf-l{float:none !important;clear:both !important}html body main .mm-pdf-r{margin-left:auto !important;margin-right:0 !important}html body main .mm-pdf-l{margin-left:0 !important;margin-right:auto !important}html body main .mm-pdfsp{display:none !important}}\n"),
 ('23b captions over a row of photos never run into the text above',
  "var a = items[m - 1], b = items[m], w = want(a, b); if (w === null || done.has(b.target)) continue;",
  "var a = items[m - 1], b = items[m], w = want(a, b); if (w === null || done.has(b.target)) continue;\n      if (!phone640() && b.el.classList && b.el.classList.contains('mm-pdf-row') && a.type !== 'row') { var cq = q('.mm-cap:not(.mm-cap-below)', b.el).map(function(x){ return x.getBoundingClientRect(); }).filter(function(x){ return x.height > 0; }), pq = q('.pim', b.el).map(function(x){ return x.getBoundingClientRect().top; }); if (cq.length && pq.length) w = Math.max(w, Math.min.apply(null, pq) - Math.min.apply(null, cq.map(function(x){ return x.top; })) + 1); }   // %s (23): the space is measured to the photos, so captions set over them (Unprepared / Prepared, Addition Snake Game) ran into the last line above at 641 to 830 (at 640 and narrower they stand in the flow); never less than keeps the captions' box 1px below that line's letters" % N),
]
EDITS += [
 ('24 a photo strip ends at the foot of its figcaptions too',
  "if (it.type === 'row' || it.type === 'strip') { var p = q('.pim, .mm-cap', it.el).map(function(x){ return x.getBoundingClientRect().bottom; });",
  "if (it.type === 'row' || it.type === 'strip') { var p = q('.pim, .mm-cap, figcaption', it.el).map(function(x){ return x.getBoundingClientRect().bottom; });   /* %s (24): captions written as figcaption (The Sensorial Curriculum's sets) count too - on phones and tablets the label after a set was run over \"Presentation complete\" */" % N),
 ('25 a photo cut as Word did stays inside its own box',
  "else{s('width',(100/cw).toFixed(4)+'%');",
  "else if(window.CSS&&CSS.supports&&CSS.supports('object-view-box','inset(1% 1% 1% 1%)')){s('width','100%');s('height','100%');s('left','0');s('top','0');s('object-view-box','inset('+[c[1],c[2],c[3],c[0]].map(function(x){return (100*x).toFixed(4)+'%';}).join(' ')+')');s('transform',rot===180?'rotate(180deg)':'none');}   /* " + N + " (25): the cut is made inside the photo's own box (object-view-box), so the photo never reaches past its box into the photo beside it; browsers without it keep the enlarged photo clipped by its box (below) */\n else{s('width',(100/cw).toFixed(4)+'%');"),
]
EDITS += [
 ('26 phones: a photo in a cell grid is never shown wider than 400',
  "html body main .mm-cap{padding-top:2px}\n",
  "html body main .mm-cap{padding-top:2px}\n/* 26: at 640 and narrower a photo in a grid of cells (.mm-g2c, Mathematics Group 5) took the whole column - 592 wide at 640, over 120% of its 360-wide file; it is at most 400 wide, centred */\n@media (max-width:640px){html body main .mm-g2c .pim{max-width:min(100%,400px) !important;margin-left:auto !important;margin-right:auto !important}}\n"),
]
EDITS += [
 ('27 a set whose photos stand under its text ends at the foot of its photos',
  "if (ph) add(c.querySelector('.mm-imgs'), 'strip', null, c); }",
  "if (ph || getComputedStyle(c).display === 'block') add(c.querySelector('.mm-imgs'), 'strip', null, c); }   // %s (27): a set whose photos are too wide to stand beside its text has them under the text (the 24 Oct rule, display block) at any width, not only on phones - the next block was spaced from its text and drawn over its photos (The Sensorial Curriculum, Drawers 5-6, Blue Triangles, 1024 and wider)" % N),
 ('28 the intro photo is the height of its paragraph, within the check limit',
  "for (var i = 0; i < 12; i++) { setH(im, h); var t = tx.getBoundingClientRect().height; if (Math.abs(t - h) < 0.5) break; h = t; }",
  "var hx = Math.min(200, 0.45 * W / Math.max(0.01, sum(a)));   // %s (28): never taller than 200 nor wider than 45%% of the column - at 831 the paragraph grew as the photo widened and the photo followed it, 2802 px wide\n        for (var i = 0; i < 12; i++) { h = Math.min(h, hx); setH(im, h); var t = tx.getBoundingClientRect().height; if (Math.abs(Math.min(t, hx) - h) < 0.5) break; h = t; }" % N),
]
EDITS += [
 ('29a a margin that moves nothing is not taken further',
  "      } else b.target.style.setProperty('margin-top', need.toFixed(2) + 'px', 'important');",
  "      } else { var gq = T[m] - B[m - 1], pq = b.target.__mmPq;   /* %s (29): a margin that moved nothing (the line held where it is by a photo beside it) is not taken further - each pass pulled the line under Aims 12px higher until a photo moved and it ran over Aims (The Mathematics Curriculum, Teen Beads and Boards, 831) */\n        if (pq && cur < pq.cur - 0.5 && Math.abs(gq - pq.gap) < 0.5) b.target.__mmFl = pq.cur;\n        if (b.target.__mmFl !== undefined) need = Math.max(need, b.target.__mmFl);\n        b.target.__mmPq = {cur: cur, gap: gq};\n        b.target.style.setProperty('margin-top', need.toFixed(2) + 'px', 'important'); }" % N),
 ('29b the guard starts again with each fresh layout',
  "if (fresh) {   // the first pass of a layout starts from nothing",
  "if (fresh) items.forEach(function(it){ delete it.target.__mmPq; delete it.target.__mmFl; });   // %s (29)\n    if (fresh) {   // the first pass of a layout starts from nothing" % N),
 ('30 sets beside text are fitted again once the floats have settled',
  "wrapFloats(); spaceTable(false); wrapFloats(); floatsAboveHeadings(); }",
  "wrapFloats(); spaceTable(false); wrapFloats(); floatsAboveHeadings(); sets(); spaceTable(false); wrapFloats(); }   /* %s (30): a set of photos beside text is fitted again at the width it has once the floats above have settled - fitted while wider, its photos ran 17px over its text (The Culture Curriculum, Sandpaper Globe, 1080-1110) */" % N),
]
EDITS += [
 ('31 open-and-close lists (album contents) as on the live Culture page',
  "html body main blockquote.pullquote p > span:first-child > .mm-t:first-child{display:none !important}</style>",
  "html body main blockquote.pullquote p > span:first-child > .mm-t:first-child{display:none !important}</style><style id=\"mm-albums-css\">/* %s (31): the open-and-close album lists, styled as on the live Culture page (its own page style, 27 Oct copy) - the cleaning had removed them: 23 beige 1px lines, the red +/- markers, 3 columns */main .mm-albums-c{margin:0;margin-left:24px !important}main .mm-albums-c details.mm-centre{border-bottom:1px solid #D9C9AB;padding:10px 0}main .mm-albums-c summary{cursor:pointer;color:#EE0000;font-size:18px;list-style:none;margin-left:0}main .mm-albums-c summary::marker{color:#EE0000}main .mm-albums-c summary::-webkit-details-marker{display:none}main .mm-albums-c summary::before{content:\"+\";display:inline-block;width:22px;font-weight:400;color:#EE0000}main .mm-albums-c details[open]>summary::before{content:\"\\2212\"}main .mm-albums-c details.mm-megd summary{color:#2B2B2B}main .mm-albums-c .mm-cbody{column-count:3;column-gap:40px;padding:14px 0 6px}main .mm-albums-c .mm-cbody>*{break-inside:avoid;margin:0 0 11px !important}main .mm-albums-c .mm-cbody>.micro-label{break-after:avoid;margin:6px 0 11px !important}main .mm-albums-c .mm-cbody>.micro-label:first-child{margin-top:0 !important}@media (max-width:640px){main .mm-albums-c .mm-cbody{column-count:1}main .mm-albums-c{margin-left:0 !important}}\n/* %s (32): a black heading (cw-white) has no line under it, as on the live pages - the blue line under every heading (19 Oct rule) put one under black headings on The Culture Curriculum and The Mathematics Curriculum */html body main h2.cw-white{border-bottom:0 !important;padding-bottom:0 !important}</style>" % (N, N)),
]
EDITS += [
 ('33 a line space is measured from the text above it in its own column, never from text beside it or inside a closed section',
  "while((n=w.nextNode())){if(el.contains(n))break;if(!(el.compareDocumentPosition(n)&Node.DOCUMENT_POSITION_PRECEDING))continue;if(!ok(n))continue;var l=lineOf(n,true);if(l)best=best===null?l.b:Math.max(best,l.b);}",
  "var er=el.getBoundingClientRect(),rg=document.createRange();while((n=w.nextNode())){if(el.contains(n))break;if(!(el.compareDocumentPosition(n)&Node.DOCUMENT_POSITION_PRECEDING))continue;if(!ok(n))continue;var pd=n.parentElement.closest('details');if(pd&&!pd.open&&!n.parentElement.closest('summary'))continue;rg.selectNodeContents(n);var qs=[].filter.call(rg.getClientRects(),function(q){return q.height>=5&&q.width>=1;});if(!qs.length)continue;var lq=qs[qs.length-1];if(lq.right<=er.left+1||lq.left>=er.right-1)continue;var l=lineOf(n,true);if(l)best=best===null?l.b:Math.max(best,l.b);}   /* %s (33): only text above this line in its own column counts - text in the column beside it, or hidden in a closed section, pulled the line down further on every pass (Culture albums: 139 013 px; Sensorial \"Materials\": 547 322 px, below the footer) */" % N),
]
EDITS += [
 ('33b the albums keep their own line spaces (their style sets them, as live)',
  "[].forEach.call(document.querySelectorAll('main [data-gap]'),function(el){var pv=tgt(el).previousElementSibling;",
  "[].forEach.call(document.querySelectorAll('main [data-gap]'),function(el){if(el.closest('.mm-cbody'))return;   /* %s (33b): inside an album's columns the album style sets the spaces, as on the live Culture page */var pv=tgt(el).previousElementSibling;" % N),
 ('34 a bold label at the top of a column is not spaced from the column beside it',
  "      if (!pv) { var sc = l.parentElement && l.parentElement.previousElementSibling; pv = sc && sc.lastElementChild; }\n      if (pv && pv.classList.contains('beige-rule'))",
  "      if (!pv) { var sc = l.parentElement && l.parentElement.previousElementSibling; pv = sc && sc.lastElementChild; }\n      if (pv) { var la = l.getBoundingClientRect(), pa = pv.getBoundingClientRect(); if (pa.right <= la.left + 1 || pa.left >= la.right - 1) return; }   // %s (34): the text before it stands in the column beside it, not above it - the label was pushed below the end of that column (Mathematics, the three periods: a staircase; Culture albums)\n      if (pv && pv.classList.contains('beige-rule'))" % N),
]
EDITS += [
 ('35 photos beside text are measured where they stand before they are centred on their lines',
  "function photos(set){ var p = q('.pim', set.querySelector('.mm-imgs')).map(function(x){ return x.getBoundingClientRect(); }); return [Math.min.apply(null, p.map(function(x){ return x.top; })), Math.max.apply(null, p.map(function(x){ return x.bottom; }))]; }",
  "function photos(set){ var mi = set.querySelector('.mm-imgs'), off = parseFloat(mi.style.top) || 0, p = q('.pim', mi).map(function(x){ return x.getBoundingClientRect(); }); return [Math.min.apply(null, p.map(function(x){ return x.top; })) - off, Math.max.apply(null, p.map(function(x){ return x.bottom; })) - off]; }   // %s (35): measured without the shift that centres them on their lines (data-vc) - with it, each spacing pass pushed the set down and the centring pulled the photos back up, without end (The Sensorial Curriculum, Touch Tablets: 547 322 px, below the footer)" % N),
]
EDITS += [
 ('36 the Culture page layouts the cleaning had dropped: number column, introduction list, opposite forms, tab gaps, list indents, lines that do not wrap',
  "<style id=\"mm-albums-css\">",
  "<style id=\"mm-culture-live-css\">/* %s (36): the Culture page's own layouts, as on the live page (27 Oct copy), which the cleaning had dropped */main p.mm-num,main .micro-label.mm-num{display:grid;grid-template-columns:44px 1fr}main p.mm-cols3{grid-template-columns:repeat(3,max-content);column-gap:72px}main .mm-introlist{display:grid;grid-template-columns:1fr 1fr;column-gap:40px;margin:0 0 0 48px}main .mm-introlist p{margin:0 0 11px !important;display:grid;grid-template-columns:30px 1fr}main .mm-introlist p.mm-il1{margin-left:30px !important}main .mm-introlist p.mm-il2{margin-left:60px !important}main p.mm-off{margin-left:48px !important}main .mm-tabgap{display:inline-block;width:2em}main ul.mm-lvl1{margin-left:48px !important}main .mm-set ol.mm-nooff{margin-left:0 !important;padding-left:0 !important;list-style-position:inside}@media (min-width:641px){main .mm-set[data-nowrap] .mm-text li,main .mm-set[data-nowrap] .mm-text p{white-space:nowrap;text-align:left !important}}@media (max-width:640px){main p.mm-cols3{grid-template-columns:1fr}main .mm-introlist{grid-template-columns:1fr;margin-left:0}main p.mm-off{margin-left:0 !important}}</style><style id=\"mm-albums-css\">" % N),
]
EDITS += [
 ('37 words hidden in a closed section are not measured',
  "      var sv = n.nodeValue; if (!sv.trim() || (n.parentElement.closest && n.parentElement.closest('.mm-pdf,a.pdf'))) continue;",
  "      var sv = n.nodeValue; if (!sv.trim() || (n.parentElement.closest && n.parentElement.closest('.mm-pdf,a.pdf'))) continue;\n      var dz = n.parentElement.closest && n.parentElement.closest('details'); if (dz && !dz.open && !n.parentElement.closest('summary')) continue;   // %s (37): words inside a closed section are not on the screen - measured, they put 465 px of empty page above \"Artistic Expression\" (The Culture Curriculum)" % N),
]
EDITS += [
 ('38 the Sensorial page layouts the cleaning had dropped: material-name lines, reference and touch tables, the formula line, the visual list',
  "<style id=\"mm-culture-live-css\">",
  "<style id=\"mm-sensorial-live-css\">/* %s (38): as on the live Sensorial page (27 Oct copy), which the cleaning had dropped */html body main h3.material-name{margin-top:20px !important;padding-top:0 !important;border-top:0 !important;margin-bottom:20px !important}html body main h3.material-name::before{content:\"\";display:block;height:2px;background:#D9C9AB;margin-bottom:var(--mm-below,20px)}html body main h3.material-name.dm-blue::before{background:transparent !important}html body main h3.material-name.dm-blue{color:#0432FF !important}main .ref-table{border-top:0 !important;margin-top:0 !important;margin-bottom:0 !important}main .ref-row{position:relative;padding:0 !important;border-bottom:0 !important;margin:30px 0 10px !important}main .ref-table:not(.touch-table)>.ref-row:first-child::before{content:\"\";position:absolute;left:0;right:0;top:-17px;border-top:1px solid var(--rule)}main .ref-table:not(.touch-table)>.ref-row:last-child::after{content:\"\";position:absolute;left:0;right:0;bottom:-17px;border-top:1px solid var(--rule)}main .ref-label{flex:0 0 150px;font-weight:700;color:var(--ink)}main .touch-table,main .touch-table .ref-row{border:0 !important}main .touch-table .ref-row{display:grid;grid-template-columns:minmax(180px,26%%) minmax(110px,14%%) 1fr;gap:0 18px}main .touch-table>.ref-row:nth-child(n+2){margin-bottom:20px !important}main .touch-table>.ref-row:nth-child(n+3){margin-top:20px !important}main .touch-table .ref-row:not(.touch-head) .ref-label{color:#EE0000 !important;font-weight:400 !important}main hr.formula-divider{border:0 !important}@media (min-width:641px){main #visual-list{grid-template-columns:1fr 1fr 1fr;grid-template-rows:repeat(5,auto);max-width:820px}main #visual-list > div:nth-child(5n+1){margin-top:0 !important}}@media (max-width:640px){main .ref-row{flex-direction:column;gap:4px}main .ref-label{flex:none}main .touch-table .ref-row{grid-template-columns:1fr 1fr}main .touch-table .ref-desc{grid-column:1 / -1}}</style><style id=\"mm-culture-live-css\">" % N),
 ('39 a set whose text would be squeezed under 200 px stands its photos under the text, as on the live Sensorial page (computers and tablets)',
  "floatsAboveHeadings(); sets(); spaceTable(false); wrapFloats(); }",
  "floatsAboveHeadings(); sets(); stackNarrow(); spaceTable(false); wrapFloats(); }\n    function stackNarrow(){   // %s (39): as the live Sensorial page (16 Oct, option C): text squeezed under 200 px -> the photos stand under the text, centred\n      q('main .mm-set').forEach(function(s){ s.classList.remove('mm-stack'); if (phone() || s.classList.contains('mm-intro') || s.classList.contains('mm-formula') || s.hasAttribute('data-h')) return;\n        var tx = s.querySelector('.mm-text'), im = s.querySelector('.mm-imgs'); if (!tx || !im || tx.getBoundingClientRect().width >= 200) return;\n        var a = shapes(im), W = s.clientWidth, G = GAP * (a.length - 1), p0 = im.querySelector('.pim'), H = (p0 && parseFloat(p0.style.getPropertyValue('--mh'))) || STD;\n        s.classList.add('mm-stack'); s.style.setProperty('display', 'block'); tx.style.width = ''; tx.style.maxWidth = ''; im.style.position = ''; im.style.top = ''; im.style.justifyContent = 'center'; setH(im, Math.min(H, (W - G) / sum(a)));\n        var k = ink(tx), t = Math.min.apply(null, q('.pim', im).map(function(x){ return x.getBoundingClientRect().top; })); im.style.marginTop = (k && isFinite(t)) ? Math.max(0, 48 - (t - k[3])).toFixed(2) + 'px' : '48px'; }); }" % N),
]
EDITS += [
 ('40 photos are centred on the named lines of their own text',
  "      var line = function(t){ return q('main p').filter(function(p){ return p.textContent.indexOf(t) >= 0; })[0]; };",
  "      var line = function(t){ var own = q('p', s).filter(function(p){ return p.textContent.indexOf(t) >= 0; }); return own.length ? own[0] : q('main p').filter(function(p){ return p.textContent.indexOf(t) >= 0; })[0]; };   // %s (40): the line is looked for in the set's own text first - \"Preparation for writing.\" is in several sets, and the first one on the page put the Touch Tablets photos 9 000 px above their text, over the Binomial Cube photos" % N),
]
EDITS += [
 ('41 the Sensorial Extensions photos stand one under another, as on live',
  "main hr.formula-divider{border:0 !important}",
  "main hr.formula-divider{border:0 !important}main .mm-float.ext-float{clear:right}" ),
]
