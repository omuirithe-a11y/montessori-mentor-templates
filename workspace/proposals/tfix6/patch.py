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
for a, b in E:
    n = s.count(a)
    if n != 1: sys.exit('NOT FOUND ONCE (%d): %s' % (n, a[:80]))
    s = s.replace(a, b)
open(out, 'w', encoding='utf-8').write(s)
print('patched', sorted(which), len(E), 'edits ->', out)
