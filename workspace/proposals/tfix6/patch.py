"""Proposed Essay Code Template changes after the build 25 review (6 Nov), NOT agreed yet.
usage: patch.py <in.html> <out.html> [T1,T2,T5]
T1 (review fault 9): the spacing script lays out Word's columns (.mm-wcols2/.mm-cols3) as columns whenever the page shows
    them side by side (two or more grid columns), not only above 830 px - at 641-830 the second column started where the
    first ended.
T2 (review fault 11): at 641-830 px, a caption above an image in a swipe row stands in the flow above its image, as at
    640 and narrower - it stood outside the row and the row's scrolling cut it off.
T6 (review fault 5): the letter-gap script still spaces a line that has a floated image beside it (only an image standing in the flow above the line makes it step aside).\nT5 (review fault 6): class mm-ind104: a block Word indents 78 pt (104 px) starts 104 px in, at 641 px and wider; none on
    phones (as mm-tab1).
"""
import sys
src, out = sys.argv[1], sys.argv[2]
which = set((sys.argv[3] if len(sys.argv) > 3 else 'T1,T2,T5').split(','))
s = open(src, encoding='utf-8').read()
E = []
if 'T1' in which:
    E += [("if ((cl.contains('mm-cols3') || cl.contains('mm-wcols2')) && ph) {",
           "if ((cl.contains('mm-cols3') || cl.contains('mm-wcols2')) && !mcols(c)) {"),
          ("if ((cl.contains('mm-wcols2') || cl.contains('mm-cols3')) && !ph) {",
           "if ((cl.contains('mm-wcols2') || cl.contains('mm-cols3')) && mcols(c)) {"),
          ("    var main = document.querySelector('main'), ph = phone(), items = [], floats = [];",
           "    var main = document.querySelector('main'), ph = phone(), items = [], floats = [];\n"
           "    /* 6 Nov 2026 (proposed, b25 review fault 9): Word's columns are spaced as columns whenever the page shows them side by side (641-830 too), not only above 830 */\n"
           "    var mcols = function(c){ return getComputedStyle(c).gridTemplateColumns.trim().split(/\\s+/).length > 1; };")]
if 'T2' in which or 'T5' in which:
    css = ''
    if 'T2' in which:
        css += ('/* 6 Nov 2026 (proposed, b25 review fault 11): at 641-830 px a caption above an image in a swipe row stands above its image in the flow, as at 640 and narrower (it stood outside the row, which cut it off) */'
                '@media (min-width:641px) and (max-width:830px){html body main .mm-row figure.mm-cf{display:flex;flex-direction:column;justify-content:flex-end}html body main .mm-row figure.mm-cf>.mm-cap:not(.mm-cap-below){position:static !important;transform:none !important;left:auto !important;width:auto !important;white-space:normal !important;text-align:center;margin:0 0 6px !important}}')
    if 'T5' in which:
        css += ('/* 6 Nov 2026 (proposed, b25 review fault 6): a block Word indents 78 pt starts 104 px in, at 641 px and wider; none on phones, as mm-tab1 */'
                'html body main .mm-ind104{margin-left:104px !important}@media (max-width:640px){html body main .mm-ind104{margin-left:0 !important}}')
    E += [('<style id="mm-fix3-5nov">', '<style id="mm-review25-6nov">' + css + '</style>\n<style id="mm-fix3-5nov">')]
if 'T6' in which:
    E += [("function(p){if(el.contains(p))return false;var r=p.getBoundingClientRect();",
           "function(p){if(el.contains(p))return false;var fl=p.closest('.mm-float');if(fl&&getComputedStyle(fl).cssFloat!=='none')return false;   /* 6 Nov 2026 (proposed, b25 review fault 5): an image floated beside the line is not one standing in the flow above it - the letter gap is set as for every other line (list lines beside an image were left to the spacing script, unevenly spaced) */var r=p.getBoundingClientRect();")]
if 'T4' in which:
    # her 5 Nov 09:16 agreement ("images beside text move under the text only when the text would be narrower than 200 px,
    # at 641 px and wider") was put into the template only above 830 px: at 641-830 every image beside text still stood
    # above or below it (the 19 Oct swipe rule). T4 carries the agreement down to 641 px: sets and floats beside text keep
    # the desktop layout at 641-830; swipe rows (images not beside text) stay as they are
    blk_old = """  .mm-set{display:block}
  .mm-set .mm-text{width:auto !important;max-width:none !important}
  .mm-set .mm-imgs,.mm-row{display:flex;"""
    blk_new = """  .mm-row{display:flex;"""
    E += [(blk_old, blk_new),
          ("  .mm-set .mm-imgs::-webkit-scrollbar,.mm-row::-webkit-scrollbar{display:none}", "  .mm-row::-webkit-scrollbar{display:none}"),
          ("  .mm-set.mm-col .mm-imgs .pim{height:70px !important}\n", ""),
          ("  .mm-imgs .pim{height:calc(var(--hp,180) * 1px) !important}\n", "  .mm-imgs .pim{height:calc(var(--hp,180) * 1px) !important}\n}\n@media (min-width:641px) and (max-width:830px){   /* proposed T4: images beside text take the size the layout gives them (as above 830) */\n  html body main .mm-set .mm-imgs .pim{height:calc(var(--mh,153) * 1px) !important}\n}\n@media (max-width:830px){\n"),
          ("  .mm-float, .mm-float.mm-left{float:none;margin:12px 0}\n", ""),
          ("  .mm-dots{display:flex;justify-content:center;gap:6px;margin:8px 0 4px}",
           "  .mm-dots{display:flex;justify-content:center;gap:6px;margin:8px 0 4px}\n}\n@media (max-width:640px){   /* 6 Nov 2026 (proposed T4; her 5 Nov 09:16 agreement): images beside text stand under it only at 640 and narrower (above 640: only when the text would be narrower than 200 px) */\n  .mm-set{display:block}\n  .mm-set .mm-text{width:auto !important;max-width:none !important}\n  .mm-set .mm-imgs{display:flex;justify-content:flex-start !important;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px;margin:12px 0 0 !important;scrollbar-width:none}\n  .mm-set .mm-imgs::-webkit-scrollbar{display:none}\n  .mm-set.mm-col .mm-imgs .pim{height:70px !important}\n  .mm-float, .mm-float.mm-left{float:none;margin:12px 0}"),
          ("@media (min-width:641px) and (max-width:830px){html body main .mm-pdf-r,html body main .mm-pdf-l{float:none !important;clear:both !important}html body main .mm-pdf-r{margin-left:auto !important;margin-right:0 !important}html body main .mm-pdf-l{margin-left:0 !important;margin-right:auto !important}html body main .mm-pdfsp{display:none !important}}",
           "/* 6 Nov 2026 (proposed T4): the 641-830 rule above is withdrawn - images the PDF puts beside text stand beside it at 641 px and wider (her 5 Nov 09:16 agreement) */"),
          ("@media (min-width:641px) and (max-width:830px){html body main .mm-imgs .pim{height:calc(min(var(--hp,180), 200) * 1px) !important}html body main .mm-set.mm-intro .mm-imgs .pim{height:200px !important}html body main .mm-set.mm-col .mm-imgs .pim{height:calc(min(var(--hp,180), 200) * 1px) !important}}",
           "@media (min-width:641px) and (max-width:830px){html body main .mm-row .pim{height:calc(min(var(--hp,180), 200) * 1px) !important}}   /* 6 Nov 2026 (proposed T4): at 641-830 only swipe rows; images beside text take their desktop size */"),
          ("@media (min-width:831px){\n  .mm-set.mm-stack{display:block}", "@media (min-width:641px){   /* proposed T4: from 641 px (was 831) */\n  .mm-set.mm-stack{display:block}"),
          ("      if (phone()) return;\n      if (s.classList.contains('mm-intro')) {", "      if (phone640()) return;   /* 6 Nov 2026 (proposed T4): beside text down to 641 px */\n      if (s.classList.contains('mm-intro')) {"),
          ("    if (phone()) return;\n    var col = document.querySelector('main#content') || document.querySelector('main'), lim = 200;", "    if (phone640()) return;\n    var col = document.querySelector('main#content') || document.querySelector('main'), lim = 200;"),
          ("    var main = document.querySelector('main'), ph = phone(), items = [], floats = [];", "    var main = document.querySelector('main'), ph = phone(), pb = phone640(), items = [], floats = [];   /* pb (proposed T4): images beside text stand in the column only at 640 and narrower */"),
          ("if (cl.contains('mm-pdf-r') || cl.contains('mm-pdf-l')) { if (ph) add(c, 'row', tgt, set); return; }", "if (cl.contains('mm-pdf-r') || cl.contains('mm-pdf-l')) { if (pb) add(c, 'row', tgt, set); return; }"),
          ("if (cl.contains('mm-float')) { if (ph) add(c, 'row', tgt, set); else floats.push(c.querySelector('.pim')); return; }", "if (cl.contains('mm-float')) { if (pb) add(c, 'row', tgt, set); else floats.push(c.querySelector('.pim')); return; }"),
          ("            if (ph || getComputedStyle(c).display === 'block') add(c.querySelector('.mm-imgs'), 'strip', null, c); }", "            if (pb || getComputedStyle(c).display === 'block') add(c.querySelector('.mm-imgs'), 'strip', null, c); }"),
          ("if (ph && a.type === 'row' && a.el.classList && a.el.classList.contains('mm-float')", "if (pb && a.type === 'row' && a.el.classList && a.el.classList.contains('mm-float')"),
          ("P = items.map(function(it){ return it.set && !ph ? photos(it.set) : null; })", "P = items.map(function(it){ return it.set && !pb ? photos(it.set) : null; })"),
          ("      if (!ph) {   // photos beside text never closer than 32px", "      if (!pb) {   // photos beside text never closer than 32px")]
for a, b in E:
    n = s.count(a)
    if n != 1: sys.exit('NOT FOUND ONCE (%d): %s' % (n, a[:80]))
    s = s.replace(a, b)
open(out, 'w', encoding='utf-8').write(s)
print('patched', sorted(which), len(E), 'edits ->', out)
