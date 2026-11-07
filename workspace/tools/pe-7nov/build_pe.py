# build_pe.py <live index.html> <out folder>: The Prepared Environment, the owner's 7 Nov edits (queue/edits.txt), each with a count check
import sys, re, os, shutil
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf-8').read()
log = []
def rep(old, new, n=1, label=''):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('FAIL %s: found %d, expected %d: %r' % (label, c, n, old[:120]))
    s = s.replace(old, new); log.append('OK %s (%d)' % (label, c))
NOTE = '7 Nov 2026 (owner)'
# --- dividers (edits 1,3,7,9,10,11,16,17,18,19,20,23,24): a beige line at the end of the section above, 40 above and 40 below
DIV = {  # section id: (space above the line, space below the line) - figures set so each measures 40/40 (letters to line)
 'my-experience-preparing-environments': (35, 40), 'furniture-purchasing': (40, 39), 'mats-quantity': (40, 40),
 'layout-of-the-shelves-tables-and-chairs': (40, 39), 'mathematics-area': (40, 39), 'language-area': (35, 40),
 'layout-of-the-tables': (40, 39), 'book-corner': (40, 39), 'bathroom': (40, 39), 'mirrors': (40, 40),
 'sharing-table': (35, 39), 'storage-and-other-admin': (35, 39), 'windows': (40, 39)}
# phones (640 and narrower) take their own figures so the line also measures 40/40 there (measured at 390)
PH_A = {'my-experience-preparing-environments': 39, 'language-area': 39, 'sharing-table': 39}
PH_B_SAME = ('mats-quantity', 'language-area')
for sid, (a, b) in DIV.items():
    pa = PH_A.get(sid, a); pb = b if sid in PH_B_SAME else b + 1
    old = '</section><section class="section" id="%s"><h2 class="mm-hc-0432FF">' % sid
    rep(old, '<p class="mm-gl" data-space="%d" data-space-desk="%d" data-space-phone="%d"> </p></section><section class="section" id="%s"><h2 class="mm-hc-0432FF" data-space="%d" data-space-desk="%d" data-space-phone="%d">' % (a, a, pa, sid, b, b, pb), 1, 'divider above ' + sid)
# --- edit 25: the 20 Oct rule "no lines round quotations" deleted: no hiding, and the engine's quotation-line pass leaves dividers to their own figures
rep("html body main p.mm-gl.mm-gl-bq,html body main p.mm-gl:has(+ blockquote.pullquote),html body main blockquote.pullquote + p.mm-gl{height:0 !important;min-height:0 !important;background:none !important;line-height:0 !important;font-size:0 !important}", "/* 7 Nov 2026 (owner: \"delete that rule and ignore that old rule\"): the 20 Oct rule hiding lines next to quotations removed */", 1, 'edit 25 css')
rep("      if (!bqA && !bqB) return;\n      g.classList.add('mm-gl-bq');", "      if (!bqA && !bqB) return;\n      if (bqA) { var bl = (function(e){ var w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT), n, last = null; while ((n = w.nextNode())) if (n.nodeValue.trim()) last = n; if (!last) return null; var z = document.createElement('span'); z.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline'; last.parentNode.insertBefore(z, last.nextSibling); var y = z.getBoundingClientRect().top; z.parentNode.removeChild(z); return y; })(pv);\n        if (bl !== null) for (var k0 = 0; k0 < 4; k0++) { var d0 = 40 - (g.getBoundingClientRect().top - bl); if (Math.abs(d0) < 0.2) break; g.style.setProperty('margin-top', ((parseFloat(getComputedStyle(g).marginTop) || 0) + d0).toFixed(2) + 'px', 'important'); } }\n      return;   /* 7 Nov 2026 (owner: \"delete that rule and ignore that old rule\" - no lines round quotations; \"When I write 'divider' I always mean 40/40\"): a divider straight after a quotation stands 40 below the quotation's last line, measured from the line its letters stand on, at every width */\n      g.classList.add('mm-gl-bq');", 1, 'edit 25 engine')
# --- edits 2 and 13: heading words (heading and contents entry; link names kept)
rep('My experience preparing environments', 'My Experience Preparing Environments', 2, 'edit 2')
rep('Layout of the shelves, tables, and chairs', 'Layout of the Furniture', 2, 'edit 13')
# --- edit 4: the two dash lists in Furniture - purchasing without dashes
rep('<p>Some alternatives:</p><ul>', '<p>Some alternatives:</p><ul class="mm-nodash">', 1, 'edit 4a')
rep('prices are a fraction of what you’ll pay in the west:</p><ul>', 'prices are a fraction of what you’ll pay in the west:</p><ul class="mm-nodash">', 1, 'edit 4b')
# --- edit 26: those two lists at the left margin, and the page's paragraph space (29) between their items
def _li(m): return m.group(1) + m.group(2).replace('<li>', '<li data-space="23">') + '</ul>'
s, n26 = re.subn(r'(<ul class="mm-nodash">)(.*?)</ul>', _li, s, flags=re.S); assert n26 == 2; log.append('OK edit 26 items (%d lists)' % n26)
rep('<li data-space="23">In the British Isles', '<li data-space="26">In the British Isles', 1, 'edit 26 (the item above ends with no letter below the line)')
# --- edit 12: the stray full stop
rep('<p>.</p></section><section class="section" id="sensorial-and-language-areas">', '</section><section class="section" id="sensorial-and-language-areas">', 1, 'edit 12')
# --- edit 14: Sensorial and Language Areas: heading gone, its text and images under the shelf-height paragraph
i = s.find('<section class="section" id="sensorial-and-language-areas">'); j = s.find('</section>', i) + len('</section>')
sec = s[i:j]; body = sec[len('<section class="section" id="sensorial-and-language-areas"><h2 class="mm-hc-0432FF">Sensorial and Language Areas</h2>'):-len('</section>')]
assert sec.startswith('<section class="section" id="sensorial-and-language-areas"><h2 class="mm-hc-0432FF">Sensorial and Language Areas</h2>')
s = s[:i] + s[j:]
rep('who are quite a bit taller so it’s important to factor in which material will be on each shelf. More about this below.</p></section>', 'who are quite a bit taller so it’s important to factor in which material will be on each shelf. More about this below.</p>' + body.replace('<p>The materials are commonly', '<p data-space="%s">The materials are commonly' % os.environ.get('PSP','28'), 1) + '</section>', 1, 'edit 14 move')   # data-space 19: the page's usual 29 between paragraphs (the paragraph above ends with no letter below the line)
rep('<li><a href="#sensorial-and-language-areas">Sensorial and Language Areas</a></li>', '', 1, 'edit 14 contents')
# --- edit 15: the two row labels
rep('<p>First row: classes I’ve visited. Second row: classes I’ve prepared.</p><div class="mm-row" data-above="40" data-level="28">', '<p>Classes I’ve visited</p><div class="mm-row" data-above="40" data-level="28">', 1, 'edit 15a')
k = s.find('<p>Classes I’ve visited</p>'); k2 = s.find('<div class="mm-row" data-above="40" data-level="28">', k + 60)
assert k2 > 0 and s[k2-12:k2] == '</div></div>'
s = s[:k2] + '<p>Classes I’ve prepared</p>' + s[k2:].replace('<div class="mm-row" data-above="40" data-level="28">', '<div class="mm-row" data-above="40" data-level="28">', 1); log.append('OK edit 15b')
# --- edit 22: the Madonna 200 high
rep('<div class="mm-float"><div class="mm-imgs"><figure class="ph portrait" style="--h:180;--hg:180;--hp:180;--ar:0.97556"><div class="pim" style="aspect-ratio:0.97556"><img alt="Raphael', '<div class="mm-float mm-h200"><div class="mm-imgs"><figure class="ph portrait" style="--h:180;--hg:180;--hp:180;--ar:0.97556"><div class="pim" style="aspect-ratio:0.97556"><img alt="Raphael', 1, 'edit 22')
# --- edit 21: under the Madonna heading the space of the other headings (quotation's own figure)
rep("          var d = T - (it - ib); if (Math.abs(d) < 0.2) break;\n          b.style.setProperty('margin-top'", "          var d = ((h2 && p0 !== pv) ? HQ : T) - (it - ib); if (Math.abs(d) < 0.2) break;   /* 7 Nov 2026 (owner: 'reduce the space under this so it is the same as under the other blue headings'): a quotation beside an image straight under a heading stands as far below it as text does under the other headings */\n          b.style.setProperty('margin-top'", 1, 'edit 21')
# --- edit 8 (rows): images in a row 150 high
rep('var STD = 153, MIN = 106, ROW = 170,', 'var STD = 153, MIN = 106, ROW = 150,', 1, 'edit 8 rows')
# --- edit 5: side images: top level with the top of the letters of the first line beside them - every side image placed by the engine's glTopline (21 Oct rule), which may now also lift an image (it only lowered them)
n5 = s.count('<div class="mm-float')
s = s.replace('<div class="mm-float"', '<div class="mm-float" data-topline=""').replace('<div class="mm-float mm-h200"', '<div class="mm-float mm-h200" data-topline="%s"' % os.environ.get('MOFF', '-1.3')); log.append('OK edit 5 data-topline (%d)' % n5)
rep("        f.style.setProperty('margin-top', (Math.max(0, (parseFloat(getComputedStyle(f).marginTop) || 0) + d)).toFixed(2) + 'px', 'important');", "        f.style.setProperty('margin-top', ((parseFloat(getComputedStyle(f).marginTop) || 0) + d).toFixed(2) + 'px', 'important');   /* 7 Nov 2026 (owner: \"top of photo = top of line of text\"): an image may also move up to the first line */", 1, 'edit 5 lift')
rep("      for (var k = 0; k < 4; k++) {\n        var it = glInkTop(p), d = it - pim.getBoundingClientRect().top;", "      var off = parseFloat(f.getAttribute('data-topline')) || 0;   /* 7 Nov 2026: a quotation's opening mark stands above its capitals - data-topline gives the distance */\n      for (var k = 0; k < 4; k++) {\n        var it = glInkTop(p), d = it + off - pim.getBoundingClientRect().top;", 1, 'edit 5 offset')
# --- edit 27 (faults the placement check found at 830 and narrower, live as well): images standing above their text - the text 30 below (owner 29 Oct 12:12 "they should all have a gap of 30")
rep('<main ', '<main data-space-row-text="30" ', 1, 'edit 27 rows of one')
rep("  function skip(e, dir){ while (e && (e.classList.contains('mm-gl')", "  var cv40 = document.createElement('canvas').getContext('2d');\n  function capTop(el){ var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), t; while ((t = w.nextNode())) { if (!t.nodeValue.trim()) continue; var rg = document.createRange(), i = t.nodeValue.search(/\\S/); rg.setStart(t, i); rg.setEnd(t, i + 1); var q = rg.getClientRects()[0]; if (!q) continue; var st = getComputedStyle(t.parentElement); cv40.font = st.fontStyle + ' ' + st.fontWeight + ' ' + st.fontSize + ' ' + st.fontFamily; var mm = cv40.measureText('H'); return q.top + (q.height - (mm.fontBoundingBoxAscent + mm.fontBoundingBoxDescent)) / 2 + mm.fontBoundingBoxAscent - mm.actualBoundingBoxAscent; } return null; }   /* 7 Nov 2026: the top of the capitals of the first line */\n  function skip(e, dir){ while (e && (e.classList.contains('mm-gl')", 1, 'edit 27 capitals')
rep("if (b !== null && !nx.classList.contains('mm-float') && !nx.classList.contains('mm-row')) { var h = b - p.getBoundingClientRect().bottom; if (Math.abs(h - P) > 0.5) set(nx, 'margin-top', px(nx, 'margin-top') + P - h); }", "if (b !== null && !nx.classList.contains('mm-float') && !nx.classList.contains('mm-row')) { b = capTop(nx); var h = b - p.getBoundingClientRect().bottom; if (Math.abs(h - 30) > 0.3) set(nx, 'margin-top', px(nx, 'margin-top') + 30 - h); }   /* 7 Nov 2026: 30 to the top of the capitals, the owner's 29 Oct rule (was 40 to the letters, 24 Oct) */", 1, 'edit 27 photo after a quotation')
i9 = s.find('data-full="images/009.jpg"'); a9 = s.rfind('<div class="mm-float" data-topline=""', 0, i9); assert a9 > 0 and i9 - a9 < 400
s = s[:a9] + '<div class="mm-float" data-topline="" data-space="13"' + s[a9 + len('<div class="mm-float" data-topline=""'):]; log.append('OK edit 27 image 009: 30 below the text above it at 830 and narrower')
rep('<blockquote class="pullquote beside-photo"><p>“Above the blackboards', '<blockquote class="pullquote beside-photo" data-space="29.7"><p>“Above the blackboards', 1, 'edit 27 the quotation 30 below the Madonna at 830 and narrower')
# --- edit 28 (fault the full check found at 490-640, live as well: side images shown wider than their file): where a larger file exists the browser takes it (srcset); where the file is the largest there is, the image is never shown wider than it
from PIL import Image as _I
_dir = os.path.join(os.path.dirname(os.path.abspath(SRC)), 'images')
for n in ('001', '009', '014', '031', '151', '179', '195'):
    small = 'src="images/%s-480.jpg"' % n; assert s.count(small) == 1, n
    w1 = _I.open(os.path.join(_dir, n + '-480.jpg')).size[0]; w2 = _I.open(os.path.join(_dir, n + '.jpg')).size[0]
    if w2 > w1: s = s.replace(small, small + ' srcset="images/%s-480.jpg %dw, images/%s.jpg %dw" sizes="(max-width:640px) 100vw, 480px"' % (n, w1, n, w2)); log.append('OK edit 28 %s larger file %d' % (n, w2))
    else:
        i = s.find(small); a = s.rfind('<div class="pim" style="', 0, i); assert i - a < 600
        s = s[:a] + '<div class="pim" style="--mw:%dpx;' % w1 + s[a + len('<div class="pim" style="'):]; log.append('OK edit 28 %s at most %d wide' % (n, w1))
# --- edit 6: the chairs table - every gap between its columns half of the gap the page gave it, at every computer width (one script owns these spaces)
JS6 = """<script id="mm-table-half-7nov">/* 7 Nov 2026 (owner: "make this table less than full-width. maybe reduce the space between the comlumns by 50%"): above 640 the gap after each column is half the gap the page's full-width table had at that width */(function(){function run(){[].forEach.call(document.querySelectorAll('main table.mm-table'),function(t){var cells=[].slice.call(t.querySelectorAll('tr'));t.style.removeProperty('width');cells.forEach(function(r){[].forEach.call(r.children,function(c){c.style.removeProperty('padding-right');});});if(window.innerWidth<=640)return;var rows=[].slice.call(t.querySelectorAll('tbody tr')),n=0;rows.forEach(function(r){n=Math.max(n,r.children.length);});var R=[],L=[],g=document.createRange();for(var i=0;i<n;i++){R.push(-1e9);L.push(1e9);}rows.forEach(function(r){[].forEach.call(r.children,function(c,i){if(!c.textContent.trim())return;g.selectNodeContents(c);[].forEach.call(g.getClientRects(),function(q){R[i]=Math.max(R[i],q.right);L[i]=Math.min(L[i],q.left);});});});var gaps=[];for(var j=1;j<n;j++)gaps.push(L[j]-R[j-1]);t.style.setProperty('width','auto','important');[].forEach.call(t.querySelectorAll('tr'),function(r){[].forEach.call(r.children,function(c,i){var cs=parseInt(c.getAttribute('colspan')||'1',10);if(cs>1||i>=n-1)return;c.style.setProperty('padding-right',Math.max(0,gaps[i]/2).toFixed(2)+'px','important');});});});}addEventListener('load',run);addEventListener('resize',function(){clearTimeout(run.t);run.t=setTimeout(run,300);});run();})();</script>"""
rep('</body>', JS6 + '</body>', 1, 'edit 6 script')
# --- page settings CSS (edits 4, 6, 8, 22)
css = '''
/* 7 Nov 2026 (owner: "I want photos in a row to be be 150 and beside text to be 120", "every page"; "this pho is an exception. make it 200 high") */
@media (min-width:831px){html body main .section .mm-float .pim{height:120px !important;width:auto !important}html body main .section .mm-float.mm-h200 .pim{height:200px !important}}
/* 7 Nov 2026 (owner: "remove the dashes, so this is a non dashed list") */
html body main ul.mm-nodash li::before{content:none !important}
/* 7 Nov 2026 (the full check: side images shown wider than their file at 490-640) */
@media (max-width:640px){html body main .section .mm-float .pim[style*="--mw"]{max-width:var(--mw) !important}}
/* 7 Nov 2026 (owner: "align to the left margin") */
html body main ul.mm-nodash{padding-left:0 !important;margin-left:0 !important}html body main ul.mm-nodash li{margin-left:0 !important;padding-left:0 !important}
'''
i = s.find('<style id="mm-page">'); j = s.find('</style>', i); s = s[:j] + css + s[j:]; log.append('OK page css')
s = s.replace('? HQ :', '? %s :' % os.environ.get('HQ', '20'))
os.makedirs(OUT, exist_ok=True)
src_dir = os.path.dirname(os.path.abspath(SRC))
if not os.path.exists(os.path.join(OUT, 'images')): shutil.copytree(os.path.join(src_dir, 'images'), os.path.join(OUT, 'images'))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
print('\n'.join(log)); print('BUILT', len(s))
