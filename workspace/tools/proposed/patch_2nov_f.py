"""2 Nov 2026 (owner 17:20): "I agree to change the Resources Code Template so that, at 640 px and narrower, the PDF badges at the
end of a blue title line stay on the same line as the title's last word, on 8.1 Books by Montessori, 8.2 Books of Interest,
8.3 Picture Books, 8.4 Websites and every page built from this template."
At 640 px and narrower each title line (.res-item) ending in PDF badges gets a no-wrap span (span.mm-tkeep) holding a copy of the
last word before the badges (of the title, or of a year after it) (in the title's own elements, so its colour, italic and link stay) and the badges; the rest of the title keeps
the other words. Above 640 px everything is put back exactly as it was, before the badge-column script measures (it runs 300 ms
after a resize; this runs at once)."""
import sys
CSS = ('<style id="mm-res-2nov-f">/* 2 Nov 2026 (owner 17:20): at 640 px and narrower a title line\'s PDF badges stay on the line of the title\'s last word */'
       '@media (max-width:640px){html body main .res-item .mm-tkeep{white-space:nowrap;display:inline}'
       'html body main .res-item .mm-tkeep > .res-title{display:inline !important}'
       'html body main .res-item .mm-tkeep > .meta{display:inline !important}'
       'html body main .res-item .mm-tkeep > a.pdf,html body main .res-item .mm-tkeep > .meta > a.pdf{margin-left:24px !important;display:inline !important}}</style>')
JS = r'''<script id="mm-res-2nov-f-js">
/* 2 Nov 2026 (owner 17:20): at 640 px and narrower the PDF badges at the end of a blue title line stay on the same line as the
   title's last word (span.mm-tkeep, no wrap); above 640 px the line is put back as built */
(function(){
  var done=[];
  function isBadge(e){if(!e)return false;if(e.matches('a.pdf'))return true;
    return e.matches('.meta')&&e.children.length===1&&e.firstElementChild.matches('a.pdf')&&e.textContent.trim()===e.firstElementChild.textContent.trim();}
  function undo(){while(done.length){var d=done.pop();
      d.badges.forEach(function(b,i){d.marks[i].parentNode.replaceChild(b,d.marks[i]);});
      d.keep.parentNode.removeChild(d.keep);d.text.nodeValue=d.orig;}}
  function make(it){
    var bs=[],e=it.lastElementChild;while(isBadge(e)){bs.unshift(e);e=e.previousElementSibling;}
    if(!bs.length||!e||!e.matches('.res-title,.meta'))return;   /* the words before the badges: the title, or a year after it (.meta, 8.1) */
    var title=e,w=document.createTreeWalker(title,NodeFilter.SHOW_TEXT),n,last=null;while((n=w.nextNode())){if(n.nodeValue.trim())last=n;}
    if(!last)return;
    var v=last.nodeValue,t=v.replace(/\s+$/,''),k=t.search(/\S+$/);if(k<0)return;
    var word=t.slice(k),rest=v.slice(0,k);
    /* the last word in copies of the title's own elements (colour, italic, link) */
    var chain=[],p=last.parentNode;while(p&&p!==title){chain.unshift(p);p=p.parentNode;}
    var root=title.cloneNode(false),cur=root;chain.forEach(function(x){var c=x.cloneNode(false);cur.appendChild(c);cur=c;});cur.appendChild(document.createTextNode(word));
    var keep=document.createElement('span');keep.className='mm-tkeep';keep.appendChild(root);
    bs.forEach(function(b){b.style.removeProperty('margin-left');var a=b.querySelector('a.pdf');if(a)a.style.removeProperty('margin-left');});   /* the column place set above 640 px is not kept */
    var marks=bs.map(function(b){var m=document.createComment('mm-tkeep');b.parentNode.insertBefore(m,b);keep.appendChild(document.createTextNode(' '));keep.appendChild(b);return m;});
    title.parentNode.insertBefore(keep,title.nextSibling);
    var d={text:last,orig:v,keep:keep,badges:bs,marks:marks};last.nodeValue=rest;done.push(d);}
  function run(){undo();if(window.innerWidth>640)return;[].forEach.call(document.querySelectorAll('main .res-item'),make);}
  window.__mmTitleKeep=run;
  run();
  document.addEventListener('DOMContentLoaded',run);
  window.addEventListener('resize',run);
})();
</script>'''
def patch(s):
    assert s.count('</head>') == 1 and s.count('</body>') == 1 and 'mm-res-2nov-f' not in s
    return s.replace('</head>', CSS + '</head>').replace('</body>', JS + '</body>')
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
