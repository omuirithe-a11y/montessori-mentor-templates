"""2 Nov 2026 proposed Resources Code Template changes (for the owner's one agreement); applies to the template or to a page built from it."""
import sys
CSS = ('<style id="mm-res-2nov">/* 2 Nov 2026 (owner\'s agreement): in a red source line, words Word sets black stay black (span.mm-ink) and a link Word leaves '
       'in its link colour is a link (a.mm-link); a PDF badge in running text keeps to the word before it (span.mm-keep); at 640 px and narrower an image '
       'beside text is never wider than the text column (its height comes down with it) */'
       'main .res-entry h3.material-name .mm-ink{color:#000 !important}'
       'main .res-entry h3.material-name a.mm-link,main .res-entry h3.material-name a.mm-link *{color:#0432FF !important}'
       'main .mm-keep{white-space:nowrap}'
       '@media (max-width:640px){main .mm-float .pim{height:auto !important;width:auto !important;max-height:150px;max-width:100%}}</style>')
REPL = [
 ("function under(e){for(var x=e;x&&x.tagName!=='MAIN';x=x.parentElement){if(getComputedStyle(x).textDecorationLine.indexOf('underline')>=0)return true;}return false;}",
  "function under(e){for(var x=e;x&&x.tagName!=='MAIN';x=x.parentElement){if(x.tagName==='A')continue;/* 2 Nov 2026 (owner's agreement): a link's own underline is not Word's underline - a line that is wholly a link is not spaced as an underlined phrase */if(getComputedStyle(x).textDecorationLine.indexOf('underline')>=0)return true;}return false;}"),
 ("    [].forEach.call(m.querySelectorAll('ol>li'),function(li){",
  "    /* 2 Nov 2026 (owner's agreement): an entry that starts with plain text (no source line) stands as far below the entry above as an entry with a source line, 51 letters to letters */\n    [].forEach.call(m.querySelectorAll('.res-entry + .res-entry > p:first-child'),function(p){set(p,51);});\n    [].forEach.call(m.querySelectorAll('ol>li'),function(li){"),
]
def patch(s):
    for a, b in REPL:
        assert s.count(a) == 1, a[:50]; s = s.replace(a, b)
    assert s.count('</head>') == 1; return s.replace('</head>', CSS + '</head>')
if __name__ == '__main__':
    f = sys.argv[1]; s = open(f, encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
