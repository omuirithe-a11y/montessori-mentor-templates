"""2 Nov 2026 (owner 16:22, queued, 8.4): "Table of contents to have two columns, not three and to match the layout of the PDF" - in the
Resources template's three-column contents box, a page that fills only two columns (its third column empty) shows two equal columns
at 641 px and wider; phones keep one column."""
import sys
CSS = ('<style id="mm-res-2nov-e">/* 2 Nov 2026 (owner 16:22): a contents box with only two columns filled shows two equal columns (641 px and wider) */'
       '@media (min-width:641px){.toc .toc-grid.mm-toc3:has(> ul:empty){grid-template-columns:1fr 1fr}}.toc .toc-grid.mm-toc3 > ul:empty{display:none}</style>')
def patch(s):
    assert s.count('</head>') == 1 and 'mm-res-2nov-e' not in s; return s.replace('</head>', CSS + '</head>')
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
