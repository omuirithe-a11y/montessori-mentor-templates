import sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# speed (owner's plan, step 4 - the one measured run): after the page has loaded, two template scripts ran again during scrolling for 0.16 s and 1.1 s
rep("function run(){var bd=document.querySelector('.mc-band'),m=document.querySelector('main');if(!bd||!m)return;",
    "function run(){return;/* 11 Nov 2026: the page's one spacing rule sets the gap above the blue band (40, the approved One Spacing Preview); this older script measured every word on the page (1.1 s, the busy stretch while scrolling) */var bd=document.querySelector('.mc-band'),m=document.querySelector('main');if(!bd||!m)return;")
rep("window.addEventListener('load',function(){setTimeout(run,700);setTimeout(run,1800);setTimeout(run,3000);if(document.fonts)document.fonts.ready.then(function(){setTimeout(run,300);});});",
    "function runIf(){var r=document.querySelector('main').getBoundingClientRect(),m=run.sz;if(m&&Math.abs(r.width-m[0])<=1&&Math.abs(r.height-m[1])<=1)return;run();}/* 11 Nov 2026: after loading, the gaps are measured again only if the page's size changed (each measuring kept the page busy 0.16 s while scrolling) */\n  window.addEventListener('load',function(){setTimeout(runIf,700);setTimeout(runIf,1800);setTimeout(runIf,3000);if(document.fonts)document.fonts.ready.then(function(){setTimeout(runIf,300);});});")
open(f,'w').write(s);print('b11 ok')
