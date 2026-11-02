"""2 Nov 2026 (g corrected 19:2x: top margin 15 px so the letter's top is level with the top of the first line's capitals, the owner's 20 Oct rule, as at 641 px and wider; 8.3 build 17 review), three Resources Code Template changes, each agreed by the owner in writing:
g (18:23): a decorative first letter that begins a paragraph (class mm-initial, set in the page's settings) stays beside its text,
   50 px wide, at 390-640 px (text beside it at least 260 px); below 390 above the text as now; above 640 unchanged.
h (question 3, answer A at 18:23; sentence agreed at 18:2x): text not justified at 641-830 px, as on phones; 640 and narrower
   unchanged; wider than 830 justified as now.
i (question 4, answer A at 18:23; sentence agreed at 18:2x): at 640 px and narrower no extra gap in a contents box where one
   column ends and the next begins; wider than 640 unchanged."""
import sys
G = ('<style id="mm-res-2nov-g">/* 2 Nov 2026 (owner 18:23): a decorative first letter (span-free: the float marked mm-initial) beside its text, 50 px, at 390-640 px */'
     '@media (min-width:390px) and (max-width:640px){html body main .mm-float.mm-initial{float:left !important;clear:left !important;margin:15px 32px 4px 0 !important;width:50px !important}'
     'html body main .mm-float.mm-initial .pim{width:50px !important;height:auto !important;max-height:none !important}}</style>')
H = ('<style id="mm-res-2nov-h">/* 2 Nov 2026 (owner, question 3 A): at 641-830 px text is not justified, as on phones (the same list as mm-phone-left) */'
     '@media (min-width:641px) and (max-width:830px){:root body main li,:root body main ul>li,:root body main ol>li,:root body main.article p:not(.centred):not(.mm-poem-ctr):not(.mm-cap):not(.mc-by):not(blockquote p),:root body main .mm-bda span,:root body main blockquote.pullquote.mm-just>p{text-align:left !important}}</style>')
I = ('<style id="mm-res-2nov-i">/* 2 Nov 2026 (owner, question 4 A): at 640 px and narrower no extra gap where one contents column ends and the next begins */'
     '@media (max-width:640px){html body .toc .toc-grid{row-gap:0 !important}}</style>')
def patch(s, parts='ghi'):
    assert s.count('</head>') == 1
    add = ''.join({'g': G, 'h': H, 'i': I}[p] for p in parts)
    for k in ('mm-res-2nov-g', 'mm-res-2nov-h', 'mm-res-2nov-i'): assert k not in s
    return s.replace('</head>', add + '</head>')
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s, sys.argv[3] if len(sys.argv) > 3 else 'ghi'))
