"""29 Oct 2026 template change (owner's "General" document, 29 Oct 07:55; "go" 08:45):
 1. Menu: the menu lines of the 25 Oct font-size block (mm-type-25oct) removed, so the menu returns to its earlier sizes.
 2. Table of contents: lines up with the text at 641-1179 px (it touched the screen edge).
Usage: python3 edit29.py <in.html> <out.html>   (prints what it changed; stops if an expected line is missing or doubled)"""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
log = []
MENU = ['html body .menu .top{font-size:18px !important}\n',
        'html body .grp a,html body .grp .np,html body .grp .hd span{font-size:18px !important}\n',
        'html body .menu .top{font-size:17px !important}\n',
        'html body .grp a,html body .grp .np,html body .grp .hd span{font-size:17px !important}\n',
        '@media (min-width:961px) and (max-width:1099px){html body .site-head-in{padding-left:16px !important;padding-right:16px !important}html body .menu{gap:2px !important}html body .menu .sub-toggle{width:13px !important;min-width:13px !important;padding:0 !important;margin-left:1px !important}}\n']
import re
# a menu line: the menu bar names, the panel entries, or the 961-1099 squeeze (gaps 2, toggles 13) - in the 25 Oct block and,
# where a page repeats the block in its own settings (The Prepared Environment's mm-page), there too
LINE = re.compile(r'^(?:html body \.menu \.top\{font-size:\d+px !important\}'
                  r'|html body \.grp a,html body \.grp \.np,html body \.grp \.hd span\{font-size:\d+px !important\}'
                  r'|@media \(min-width:961px\) and \(max-width:1099px\)\{html body \.site-head-in\{padding-left:16px !important;padding-right:16px !important\}html body \.menu\{gap:2px !important\}html body \.menu \.sub-toggle\{[^}]*\}\})[^\n]*\n', re.M)
if 'id="mm-type-25oct"' in t:
    for sid in ('mm-type-25oct', 'mm-page'):
        m = re.search(r'<style id="%s">.*?</style>' % sid, t, re.S)
        if not m: continue
        blk, k = LINE.subn('', m.group(0))
        if sid == 'mm-type-25oct' and k != 5: sys.exit('STOP: %s: %d menu lines in the 25 Oct block, 5 expected' % (src, k))
        if k: t = t[:m.start()] + blk + t[m.end():]; log.append('%s: %d menu lines removed' % (sid, k))
    if re.search(r'\.menu \.top\{font-size:\d+px !important|\.menu\{gap:2px', t): sys.exit('STOP: %s: a menu size line is left' % src)
    t = t.replace('<style id="mm-type-25oct">/* 25 Oct 2026 (owner, 24 Oct 16:15 and 16:2x): font sizes */',
                  '<style id="mm-type-25oct">/* 25 Oct 2026 (owner, 24 Oct 16:15 and 16:2x): font sizes. 29 Oct 2026 (owner, "General": "Return it to the previous size across all pages and change the template"): the menu lines removed - the menu keeps the template\'s own sizes (17px, 16px at 961-1279, phones 18px; panel entries 17px) and gaps */', 1)
else:
    log.append('menu: no 25 Oct block - unchanged')
TOC = ('<style id="mm-toc-align">/* 29 Oct 2026 (owner, \"General\": the contents \"needs to align with the text below\"): '
       'at 641-1179 the contents start at the text margin (they touched the screen edge); wider, unchanged */'
       '@media (min-width:641px){.toc-wrap{max-width:calc(1100px + 2 * var(--gutter));padding-left:var(--gutter);padding-right:var(--gutter)}}'
       '/* a contents entry that runs onto two lines is not spread to the full width (Culture at 768: wide word gaps) */'
       'html body .toc-wrap li,html body .toc-wrap a{text-align:left !important;text-align-last:auto !important}</style>')
if 'id="mm-toc-align"' in t: sys.exit('STOP: already has mm-toc-align')
if t.count('</head>') != 1: sys.exit('STOP: </head> found %d times' % t.count('</head>'))
t = t.replace('</head>', TOC + '</head>', 1); log.append('contents: mm-toc-align added')
open(dst, 'w', encoding='utf-8').write(t)
print(src.split('/')[-1], '|', '; '.join(log))
