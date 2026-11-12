import sys
f=sys.argv[1]
s=open(f).read()
old="function gap(a,b){var v=b.getAttribute('data-mma');if(v)return +v;v=a.getAttribute('data-mmb');if(v)return +v;if(a.matches('p.mm-gl')||b.matches('p.mm-gl'))return GT;if(a.matches('blockquote')||b.matches('blockquote'))return GT;if(isHead(a))return G;if(imgOnly(a)||imgOnly(b))return 40;return GT;}"
assert s.count(old)==1
new=("/* 12 Nov 2026 (owner): 50 above red headings (\"make it 50 on this page and in the template\"); quotations 40 above and below (\"make it 40/40\", page and template); "
     "40 above blue headings after text, a quotation or images (\"Make it 40 after text or a quotation, same as 40 after images\"); "
     "18 after a blue sub-heading before lines of text (\"make the space after blue sub-headings before lines of text 18 on this page and on the template\") */"
     "function blueEl(e){var t=e.matches('.mm-hc-0432FF')?e:e.querySelector('.mm-hc-0432FF');if(!t)return false;var w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),n;while((n=w.nextNode())){if(n.nodeValue.trim())return getComputedStyle(n.parentElement).color==='rgb(4, 50, 255)';}return false;}"
     "function redH(e){return e.matches('h2.mm-hc-EE0000');}"
     "function gap(a,b){var v=b.getAttribute('data-mma');if(v)return +v;v=a.getAttribute('data-mmb');if(v)return +v;if(a.matches('p.mm-gl')||b.matches('p.mm-gl'))return GT;if(redH(b))return 50;if(a.matches('blockquote')||b.matches('blockquote'))return 40;"
     "if(isHead(a)){if(blueEl(a)&&!isHead(b)&&!imgOnly(b)&&!b.matches('.mm-row'))return 18;return G;}if(imgOnly(a)||imgOnly(b))return 40;if(isHead(b)&&blueEl(b))return 40;return GT;}")
s=s.replace(old,new)
open(f,'w').write(s);print('b17 ok')
