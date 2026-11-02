"""2 Nov 2026 (owner 13:30, question 1: "37"): every paragraph of the text area has the descriptions' line spacing - 37.2 px on computers, 36 px at 640 px and narrower."""
import sys
CSS = ('<style id="mm-res-2nov-b">/* 2 Nov 2026 (owner 13:30, "37"): paragraphs not under a name or title have the line spacing of the descriptions '
       '(Word double-spaces both): 37.2 px, 36 px at 640 px and narrower; quotations keep their own */'
       'main .section p:not(.res-desc):not(blockquote p){line-height:37.2px}'
       '@media (max-width:640px){main .section p:not(.res-desc):not(blockquote p){line-height:36px}}</style>')
def patch(s):
    assert s.count('</head>') == 1 and 'mm-res-2nov-b' not in s; return s.replace('</head>', CSS + '</head>')
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
