import sys
f=sys.argv[1]
s=open(f).read()
old="var GG=(B[i].matches('p.mm-gl')||B[i-1].matches('p.mm-gl'))?GT:((B[i].matches('blockquote')||B[i-1].matches('blockquote'))?40:(isHead(B[i-1])?G:GT));"
assert s.count(old)==1
s=s.replace(old,"var GG=gap(B[i-1],B[i]);")
anchor="function blocks(){"
fn=("/* 11 Nov 2026 (owner): quotations 30 above and 30 below (\"30/30\"); 40 above and 40 below images (\"I've changed my mind about the spacing above/below photos: make it 40/40\", every page); "
"a gap she set for one block (data-mma above it / data-mmb below it) wins */"
"function imgOnly(e){if(!e.querySelector('.pim')||e.matches('.mm-set'))return false;var t='';var w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),n;while((n=w.nextNode())){if(n.parentElement.closest('.mm-cap,.mm-pcap,.mm-caprow'))continue;t+=n.nodeValue;}return !t.trim();}"
"function gap(a,b){var v=b.getAttribute('data-mma');if(v)return +v;v=a.getAttribute('data-mmb');if(v)return +v;if(a.matches('p.mm-gl')||b.matches('p.mm-gl'))return GT;if(a.matches('blockquote')||b.matches('blockquote'))return GT;if(isHead(a))return G;if(imgOnly(a)||imgOnly(b))return 40;return GT;}")
assert s.count(anchor)==1
s=s.replace(anchor,fn+anchor)
old2="if(e.matches('p.mm-hanglab')){var nx=e.nextElementSibling;while(nx&&(nx.matches('.mm-float')||!nx.textContent.trim()))nx=nx.nextElementSibling;return !!(nx&&/^[a-z]\\.\\s/.test(nx.textContent.trim()));}"
assert s.count(old2)==1
s=s.replace(old2,"if(e.matches('p.mm-hanglab'))return /^Series\\s/.test(e.textContent.trim())||(function(){var nx=e.nextElementSibling;while(nx&&(nx.matches('.mm-float')||!nx.textContent.trim()))nx=nx.nextElementSibling;return !!(nx&&/^[a-z]\\.\\s/.test(nx.textContent.trim()));})();/* 11 Nov (owner, E: \"Series 3, 4 and 5 - 24\") */")
open(f,'w').write(s);print('b0 ok')
s=open(f).read()
a="if(window.MutationObserver){var mo=new MutationObserver(function(){if(!mine)soon(80);});var obs=function(){var m1=document.querySelector('main');if(m1)mo.observe(m1,{attributes:true,attributeFilter:['style','class'],subtree:true});};"
assert s.count(a)==1
b="if(window.MutationObserver){var mo=new MutationObserver(function(rs){if(mine)return;/* 11 Nov: only a real change counts - a script that writes back the value an element already had (or changes it and back) does not run the rule again, which had two scripts waking each other for ever */var first=new Map();rs.forEach(function(r){var k=r.target;if(!first.has(k))first.set(k,{});var o=first.get(k);if(!(r.attributeName in o))o[r.attributeName]=r.oldValue;});var real=false;first.forEach(function(o,t){for(var a in o){if((t.getAttribute(a)||'')!==(o[a]||''))real=true;}});if(real)soon(80);});var obs=function(){var m1=document.querySelector('main');if(m1)mo.observe(m1,{attributes:true,attributeOldValue:true,attributeFilter:['style','class'],subtree:true});};"
s=s.replace(a,b);open(f,'w').write(s);print('b0b ok')
