(S)=>{
 const m=document.querySelector('main'),Y=y=>y+scrollY;
 const cv=document.createElement('canvas').getContext('2d');
 const vis=e=>{if(!e)return false;const c=getComputedStyle(e),r=e.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&r.width>0&&r.height>0;};
 const inkTop=el=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n,v=null,line=null;const r=document.createRange();
  while((n=w.nextNode())){if(!n.nodeValue.trim())continue;const pe=n.parentElement;if(!pe||pe.closest('a.pdf,.mm-float'))continue;const c=getComputedStyle(pe);if(c.display==='none')continue;
   cv.font=c.fontStyle+' '+c.fontWeight+' '+c.fontSize+' '+c.fontFamily;const fm=cv.measureText('Hg'),s=n.nodeValue;
   for(let i=0;i<s.length;i++){if(!s[i].trim())continue;r.setStart(n,i);r.setEnd(n,i+1);const b=r.getClientRects()[0];if(!b||!b.width)continue;if(line===null)line=b.top;if(b.top>line+2)return v===null?null:Y(v);
    const base=b.top+(b.height-(fm.fontBoundingBoxAscent+fm.fontBoundingBoxDescent))/2+fm.fontBoundingBoxAscent,y=base-cv.measureText(s[i]).actualBoundingBoxAscent;v=v===null?y:Math.min(v,y);}}
  return v===null?null:Y(v);};
 const lines=el=>{const tops=new Set();const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;const r=document.createRange();while((n=w.nextNode())){if(!n.nodeValue.trim())continue;r.selectNodeContents(n);for(const q of r.getClientRects())if(q.width>1)tops.add(Math.round(q.top));}return tops.size;};
 const P=m.querySelector('section > p')||m.querySelector('p');const pr=P.getBoundingClientRect();const X0=pr.left,X1=pr.right;
 const o={};
 // L1 numbered lists: where each number starts, from the text margin
 o.olMarkers=[...m.querySelectorAll('ol')].filter(vis).map(ol=>{const li=ol.querySelector(':scope>li');const b=getComputedStyle(li,'::before');let x;
   if(b.content&&b.content!=='none'&&b.content!=='normal')x=li.getBoundingClientRect().left+parseFloat(b.left||0);else x=li.getBoundingClientRect().left-(getComputedStyle(ol).listStylePosition==='outside'?parseFloat(getComputedStyle(li).paddingLeft):0);
   return [li.textContent.trim().slice(0,30),Math.round((x-X0)*10)/10];});
 // T1 justified: every wrapped paragraph and list line
 const blocks=[...m.querySelectorAll('p, li')].filter(e=>vis(e)&&!e.closest('blockquote,figure,.mm-float,.mc-band')&&!e.classList.contains('centred')&&!e.querySelector('p,ul,ol')&&e.textContent.trim().length>0);
 const wrapped=blocks.filter(e=>lines(e)>1);o.wrapped=wrapped.length;
 o.notJustified=wrapped.filter(e=>getComputedStyle(e).textAlign!=='justify').map(e=>[e.textContent.trim().slice(0,40),getComputedStyle(e).textAlign]);
 // T4 short dashes only
 o.dashes=[];{const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode()))if(/[–—]/.test(n.nodeValue))o.dashes.push(n.nodeValue.trim().slice(0,40));}
 // B1 beige line colour; B2 invisible lines
 const gls=[...document.querySelectorAll('main .beige-rule, main p.mm-gl, .toc-rule-wrap .beige-rule, hr')];
 o.lineColours=gls.filter(g=>vis(g)&&g.getBoundingClientRect().width>100).map(g=>getComputedStyle(g).backgroundColor);
 o.invisible=gls.filter(g=>{const c=getComputedStyle(g),r=g.getBoundingClientRect();return c.display!=='none'&&r.width>0&&(c.visibility==='hidden'||c.opacity==='0'||c.backgroundColor==='rgba(0, 0, 0, 0)')}).map(g=>g.className||g.tagName);
 [...document.querySelectorAll('body *')].forEach(e=>{const c=getComputedStyle(e);if(c.display==='none')return;['Top','Bottom'].forEach(s=>{if(parseFloat(c['border'+s+'Width'])>0&&c['border'+s+'Style']!=='none'&&c['border'+s+'Color']==='rgba(0, 0, 0, 0)')o.invisible.push(e.tagName+'.'+(e.className||'')+' border-'+s.toLowerCase()+' transparent');});});
 // Q1, Q2 quotations and attributions
 o.quotes=[...m.querySelectorAll('blockquote')].filter(vis).map(bq=>{const ps=[...bq.querySelectorAll('p')].filter(p=>!p.querySelector('cite')&&p.textContent.trim());const p=ps[0]||bq;const c=getComputedStyle(p);
   const last=ps.length?ps[ps.length-1].getBoundingClientRect().bottom:bq.getBoundingClientRect().top;
   return {t:p.textContent.trim().slice(0,30),fs:parseFloat(c.fontSize),lh:parseFloat(c.lineHeight),style:c.fontStyle,
    cites:[...bq.querySelectorAll('cite')].map(ct=>{const cc=getComputedStyle(ct);return {t:ct.textContent.trim().slice(0,30),fs:parseFloat(cc.fontSize),style:cc.fontStyle,ownLine:ct.getBoundingClientRect().top>=last-1};})};});
 // N1 name lines
 o.nameLines=[...m.querySelectorAll('p.mm-name')].filter(n=>vis(n)&&n.previousElementSibling&&n.previousElementSibling.matches('p.mm-gl')).map(n=>{const g=n.previousElementSibling.getBoundingClientRect(),r=n.getBoundingClientRect();return {t:n.textContent.trim().slice(0,30),x0:r.left,x1:r.right,lineBottom:Y(g.bottom)};});
 // F1-F4 footer
 const band=document.querySelector('.mc-band');
 if(band){const bc=getComputedStyle(band),q=band;const words=[];if(q){const w=document.createTreeWalker(q,NodeFilter.SHOW_TEXT);let n;const r=document.createRange();while((n=w.nextNode())){if(n.parentElement.closest('.mc-by'))continue;const re=/\S+/g;let mm;while((mm=re.exec(n.nodeValue))){r.setStart(n,mm.index);r.setEnd(n,mm.index+mm[0].length);const b=r.getClientRects()[0];if(b)words.push([Math.round(b.top),mm[0]]);}}}
   const L=[];words.forEach(([t,wd])=>{if(!L.length||Math.abs(L[L.length-1][0]-t)>3)L.push([t,wd]);else L[L.length-1][1]+=' '+wd;});const lt=L.map(x=>x[1]);
   const ci=lt.findIndex(x=>x.endsWith('confess that,')),pi=lt.findIndex(x=>x.includes('It was as if'));const ok=ci>=0&&(lt[ci+1]||'').startsWith('while my efforts')&&pi>ci&&(lt[pi].startsWith('It was as if')?(lt[pi-1]||'').endsWith('prostrated me.'):/me\. It was as if/.test(lt[pi]));   /* 20 Oct rule: breaks after "confess that," and "prostrated me."; where a line does not fit, its overflow words go on with "It was as if..." (21 Oct: a line too long for the width wraps where it must) */
   const foot=document.querySelector('.site-foot');const fk=foot?[...foot.querySelectorAll('*')].filter(e=>e.children.length===0&&e.textContent.trim()):[];
   const _ib=Math.max(-1e9,...[...document.querySelectorAll('main img')].map(i=>{const r=i.getBoundingClientRect();return r.height>4?r.bottom:-1e9;}));let _tb=-1e9;{const w2=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT),rg=document.createRange();let n2;while((n2=w2.nextNode())){if(!n2.nodeValue.trim())continue;rg.selectNodeContents(n2);for(const q of rg.getClientRects())if(q.width)_tb=Math.max(_tb,q.bottom);}}
   o.footer={endsPhoto:_ib>_tb,x0:X0,x1:X1,bandTop:Y(band.getBoundingClientRect().top),bg:bc.backgroundColor,pt:parseFloat(bc.paddingTop),pb:parseFloat(bc.paddingBottom),lines:lt,breaksOk:ok,
    strip:fk.map(e=>e.textContent.trim()),stripCol:fk[0]?getComputedStyle(fk[0]).color:null,stripFs:fk[0]?parseFloat(getComputedStyle(fk[0]).fontSize):null};}
 else o.footer=null;
 // M2-M4 menu
 const nav=document.querySelector('#site-nav')||document.querySelector('header nav');
 const mlink=[...document.querySelectorAll('#site-nav a, .panel a')];
 o.menu={lined:mlink.filter(a=>{const c=getComputedStyle(a);return a.getAttribute('aria-current')!=='page'&&(parseFloat(c.borderBottomWidth)>0&&c.borderBottomStyle!=='none'&&c.borderBottomColor!=='rgba(0, 0, 0, 0)'||c.textDecorationLine.includes('underline'));}).map(a=>a.textContent.trim().slice(0,25)),
  panelBg:document.querySelector('.panel')?getComputedStyle(document.querySelector('.panel')).backgroundColor:null,own:[]};
 document.querySelectorAll('.panel').forEach(pn=>{const top=pn.parentElement&&pn.parentElement.querySelector('.top');const href=top&&top.getAttribute('href');const nm=top?top.textContent.trim():'';
   if(!['Administration','The History of Education','Parent Resources','Resources','Parents','Education'].some(x=>nm.startsWith(x)))return;   /* SETTLED 18 Oct names these four pages */
   if(href&&[...pn.querySelectorAll('a')].some(a=>a.getAttribute('href')===href))o.menu.own.push('the "'+nm+'" panel lists its own page');});
 const adm=[...document.querySelectorAll('.top')].find(t=>t.textContent.trim().startsWith('Administration'));
 if(adm){const pn=adm.parentElement.querySelector('.panel');if(pn){const subs=[...pn.querySelectorAll('h3,h4,.grp-h,.sub,.label,strong,b,.grp > span')].map(e=>e.textContent.trim());['Teachers','Children','Parents'].forEach(s=>{const e=[...pn.querySelectorAll('*')].find(x=>x.children.length===0&&x.textContent.trim()===s);if(!e)o.menu.own.push('Administration panel has no "'+s+'" sub-heading');else{const c=getComputedStyle(e);if(parseInt(c.fontWeight)>=600)o.menu.own.push('"'+s+'" is bold');}});}}
 // M5 blues outside the menu
 const isBlue=c=>{const v=(c.match(/\d+/g)||[]).map(Number);return v.length>=3&&v[2]>v[0]+40&&v[2]>v[1]+20&&(v.length<4||v[3]>0);};
 const ok_=['rgb(4, 50, 255)','rgb(30, 77, 123)','rgb(5, 99, 193)'];const seen={};
 [...document.querySelectorAll('body *')].filter(e=>!e.closest('#site-nav,.panel,header,script,style')).forEach(e=>{const c=getComputedStyle(e);[['color',c.color],['background',c.backgroundColor]].forEach(([k,v])=>{if(isBlue(v)&&!ok_.includes(v)&&!seen[v]&&(k!=='color'||e.textContent.trim()))seen[v]=(e.className||e.tagName)+' '+k;});});
 o.blues=Object.entries(seen);
 o.heroRotates=!!document.querySelector('.hero .mm-hs');
 o.noAlt=[...m.querySelectorAll('img')].filter(i=>!(i.getAttribute('alt')||'').trim()).map(i=>i.getAttribute('data-name')||i.src.slice(-30));
 o.headings=[...m.querySelectorAll('h2')].filter(vis).map(h=>{const c=getComputedStyle(h);return {t:h.textContent.trim().slice(0,30),colour:c.color,fs:parseFloat(c.fontSize),border:parseFloat(c.borderBottomWidth)};});
 o.toc=vis(document.querySelector('nav.toc-wrap'));
 o.linkColours=[...m.querySelectorAll('a:not(.pdf)')].filter(vis).filter(a=>!a.closest('h3.material-name')).map(a=>[a.textContent.trim().slice(0,30),getComputedStyle(a).color]);
 o.linkTargets=[...m.querySelectorAll('a')].map(a=>[a.textContent.trim(),a.getAttribute('href')]);
 o.underlinedLabels=[...m.querySelectorAll('.micro-label')].filter(e=>getComputedStyle(e).textDecorationLine.includes('underline')).map(e=>e.textContent.trim());
 // gaps the page settings set (pixels are measured in Python; here only where to look)
 const gp=[];const find=st=>[...m.querySelectorAll('p,h2,h3,div.micro-label')].find(e=>e.textContent.trim().startsWith(st));
 const prevBlock=e=>{let p=e.previousElementSibling;while(p&&(!vis(p)||p.matches('.mm-float,script,style')))p=p.previousElementSibling;if(!p){const s=e.closest('section');if(s&&s.firstElementChild===e){let q=s.previousElementSibling;while(q&&!vis(q))q=q.previousElementSibling;return q&&q.matches('section')?q.lastElementChild:q;}}return p;};
 const nextBlock=e=>{let n=e.nextElementSibling;while(n&&!vis(n))n=n.nextElementSibling;if(!n){const s=e.closest('section');let q=s&&s.nextElementSibling;while(q&&!vis(q))q=q.nextElementSibling;return q&&q.matches('section')?q.firstElementChild:q;}return n;};
 /* 21 Oct 19:4x: SPACE_SET (a block's own figures, over SPACE_AFTER/SPACE_ABOVE), HEAD_AFTER, and the standing rule for underlined lines (40 above / 15 below, user 21 Oct) */
 const ph=innerWidth<=640,fig=v=>Array.isArray(v)?(ph?v[1]:v[0]):v,ov=new Set();
 const exact=t=>[...m.querySelectorAll('p,div,h2,h3')].filter(e=>e.textContent.trim()===t&&!e.querySelector('p,div'));
 const at=(what,e,want)=>{const r=e.getBoundingClientRect();gp.push({what:what,x0:X0,x1:X1,aBottom:Y(r.top)-0.5,bTop:Y(r.top),want:want});};
 (S.spaceSet||[]).forEach(([t,a,b])=>{const e=exact(t)[0];if(!e){gp.push({what:'SPACE_SET block not found: '+t,missing:1});return;}
   if(a!==null&&a!==undefined){ov.add(e);at('above "'+t.slice(0,22)+'"',e,fig(a));}
   if(b!==null&&b!==undefined){const n=nextBlock(e);if(n){ov.add(n);at('under "'+t.slice(0,22)+'"',n,fig(b));}}});
 Object.entries(S.headAfter||{}).forEach(([c,px])=>{m.querySelectorAll('h2.mm-hc-'+c).forEach(h=>{const n=nextBlock(h);if(n){ov.add(n);at('under heading "'+h.textContent.trim().slice(0,22)+'"',n,px);}});});
 [...m.querySelectorAll('.micro-label')].filter(e=>getComputedStyle(e).textDecorationLine.includes('underline')).forEach(e=>{ov.add(e);at('above underlined "'+e.textContent.trim().slice(0,22)+'"',e,40);const n=nextBlock(e);if(n){ov.add(n);at('under underlined "'+e.textContent.trim().slice(0,22)+'"',n,15);}});
 (S.spaceAfter||[]).forEach(([lab,px])=>{[...m.querySelectorAll('p')].filter(p=>p.textContent.trim().startsWith(lab)).forEach(p=>{const n=nextBlock(p);if(n&&!ov.has(n))gp.push({what:'under "'+p.textContent.trim().slice(0,22)+'"',x0:X0,x1:X1,aBottom:Y(n.getBoundingClientRect().top)-0.5,bTop:Y(n.getBoundingClientRect().top),want:px});});});
 (S.spaceAbove||[]).forEach(([st,px])=>{[...m.querySelectorAll('p')].filter(p=>p.textContent.trim().startsWith(st)&&!ov.has(p)).forEach(p=>{gp.push({what:'above "'+p.textContent.trim().slice(0,22)+'"',x0:X0,x1:X1,aBottom:Y(p.getBoundingClientRect().top)-0.5,bTop:Y(p.getBoundingClientRect().top),want:px});});});
 Object.entries(S.dividers||{}).forEach(([st,[a,b]])=>{const h=find(st);if(!h)return;const s=h.closest('section');const g=(s&&s.firstElementChild===h?s.previousElementSibling:h.previousElementSibling);if(!g||!g.matches('p.mm-gl'))return;const gr=g.getBoundingClientRect();
   gp.push({what:'above the beige line before "'+st.slice(0,22)+'"',x0:X0,x1:X1,aBottom:Y(gr.top)-0.5,bTop:Y(gr.top),want:a});
   gp.push({what:'from that line to "'+st.slice(0,22)+'"',x0:X0,x1:X1,aBottom:Y(gr.bottom)-0.5,bTop:Y(gr.bottom)+0.5,want:b});});   /* line edge to the heading's letters (the heading's box can reach above the line) */
 o.gaps=gp;
 o.redStarts=[...m.querySelectorAll('.res-entry p.res-desc')].filter(p=>{const f=[...p.childNodes].find(c=>!(c.nodeType===3&&!c.nodeValue.trim()));return f&&f.nodeType===1&&f.tagName==='SPAN'&&/rgb\((238|255), 0, 0\)/.test(getComputedStyle(f).color);}).map(p=>p.textContent.trim().slice(0,50));   /* 21 Oct 20:52: a red name starting a description is a separate source */
 o.redStarts=[...m.querySelectorAll('.res-entry p.res-desc')].filter(p=>{const f=[...p.childNodes].find(c=>!(c.nodeType===3&&!c.nodeValue.trim()));return f&&f.nodeType===1&&f.tagName==='SPAN'&&/rgb\((238|255), 0, 0\)/.test(getComputedStyle(f).color);}).map(p=>p.textContent.trim().slice(0,50));   /* 21 Oct 20:52: a red name starting a description is a separate source */
 // S10 the Resources section, against the live page's figures
 o.res=[];
 [...document.querySelectorAll('main section:has(> .res-entry)')].forEach(rs=>{const h=rs.querySelector(':scope > h2'),ents=[...rs.querySelectorAll(':scope > .res-entry')];const cov=[...rs.querySelectorAll('.mm-float .pim')].map(p=>p.getBoundingClientRect());
   const xr=e=>{const r=e.getBoundingClientRect();let x1=r.right;cov.forEach(c=>{if(c.left>r.left+50)x1=Math.min(x1,c.left-4);});return [r.left,x1];};
   if(ents[0]&&h&&h.tagName==='H2'&&parseFloat(getComputedStyle(h).borderBottomWidth)>0){const [a,b]=xr(ents[0]);o.res.push({kind:'head',what:'green line to "'+ents[0].textContent.trim().slice(0,18)+'"',x0:a,x1:b,aBottom:Y(h.getBoundingClientRect().bottom)-1,bTop:Y(h.getBoundingClientRect().bottom)+0.5});}
   ents.forEach((e,i)=>{const nm=e.querySelector(':scope > h3'),nx=nm&&nm.nextElementSibling;const [a,b]=xr(e);
     if(nm&&nx&&vis(nx))o.res.push({kind:'name',what:'"'+nm.textContent.trim().slice(0,18)+'" to its first line',x0:a,x1:b,aBottom:Y(nx.getBoundingClientRect().top)-0.5,bTop:Y(nx.getBoundingClientRect().top)});
     if(i>0&&e.previousElementSibling&&e.previousElementSibling.classList.contains('mm-org-rule')){const g=e.previousElementSibling.getBoundingClientRect();o.res.push({kind:'line',what:'line to "'+e.textContent.trim().slice(0,18)+'"',x0:a,x1:b,aBottom:Y(g.top)-0.5,bTop:Y(g.top),want:30});o.res.push({kind:'line',what:'line to "'+e.textContent.trim().slice(0,18)+'" below',x0:a,x1:b,aBottom:Y(g.bottom)-0.5,bTop:Y(g.bottom)+0.5,want:30});return;}   /* 21 Oct 19:39-19:40 (user: a beige line between entries, 30/30): measured against 30, not the live page's entry figure */
     if(i>0){const pv=ents[i-1],last=[...pv.children].filter(x=>!x.classList.contains('mm-float')&&x.textContent.trim()).pop();
       if(last&&!last.querySelector('a.pdf')&&last.classList.contains('res-desc')&&nm)o.res.push({kind:'entry',what:'entry to "'+nm.textContent.trim().slice(0,18)+'"',x0:a,x1:b,aBottom:Y(e.getBoundingClientRect().top)-0.5,bTop:Y(e.getBoundingClientRect().top)});}});});
 // P3 photos beside text
 o.floatTops=[...m.querySelectorAll('.mm-float')].filter(vis).map(f=>{const pim=f.querySelector('.pim');if(!pim||getComputedStyle(f).cssFloat==='none')return null;const host=f.closest('.res-entry')||f.nextElementSibling;const t=host?inkTop(host):null;return t===null?null:[host.textContent.trim().slice(0,25),Math.round((Y(pim.getBoundingClientRect().top)-t)*10)/10];}).filter(x=>x);
 // P4 photo rows on phones
 o.rows=[...m.querySelectorAll('.mm-row')].map((r,i)=>{const n=r.nextElementSibling,dots=n&&n.classList.contains('mm-dots')?n:null;const figs=[...r.querySelectorAll('figure')];
   return {i:i+1,photos:figs.length,overflows:r.scrollWidth>r.clientWidth+1,scrolls:/(auto|scroll)/.test(getComputedStyle(r).overflowX),dots:dots?dots.children.length:0,dotsShown:dots?vis(dots):false,snapCentre:figs.length>0&&figs.every(f=>/center/.test(getComputedStyle(f).scrollSnapAlign))};}).filter(r=>r.photos>1);
 o.coloured=[];{const w=document.createTreeWalker(m,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){if(!n.nodeValue.trim())continue;o.coloured.push([n.nodeValue.trim().slice(0,80),getComputedStyle(n.parentElement).color]);}}
 o.imgNames={};m.querySelectorAll('img[data-name]').forEach(i=>{o.imgNames[i.getAttribute('data-name')]=i.getAttribute('data-full');});
 return o;}
