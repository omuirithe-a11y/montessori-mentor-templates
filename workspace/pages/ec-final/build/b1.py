import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
j=s.find('<p data-gap="20">Dr. Angeline Lillard'); k=s.find('</p>',j)
lill=s[j+len('<p data-gap="20">'):k]
s=s[:j]+s[k+4:]
rep('which ones.</p>','which ones. '+lill+'</p>')
rep('<p class="mm-hc-0432FF" data-gap="48">Read','<p class="mm-hc-0432FF" data-gap="29">Read')
rep('<p data-gap="29">Here’s another option','<p data-gap="29" data-mma="40">Here’s another option')
rep('<h2 class="mm-hc-0432FF" data-gap="48">Symbol Box 1</h2>','<h2 class="mm-hc-0432FF" data-gap="48" data-mma="40">Symbol Box 1</h2>')
rep('<h2 class="mm-hc-0432FF" data-gap="48">Symbol Box 2</h2>','<h2 class="mm-hc-0432FF" data-gap="48" data-mma="40">Symbol Box 2</h2>')
rep('<p data-gap="29"><span class="mm-hc-EE0000">Sandpaper Letters </span>(graphemes)</p>','<p data-gap="29" data-mma="40"><span class="mm-hc-0432FF">Sandpaper Letters</span> (graphemes)</p>')
rep('<h2 class="mm-hc-0432FF" data-space="48"><strong>Preparation of the hand</strong></h2>','<h2 class="mm-hc-0432FF" data-space="48">Preparation of the hand</h2>')
ARW='<span class="mm-arw" aria-hidden="true"></span><span class="mm-vh"> to </span>'
rep('<p data-gap="29"><strong>Object Box 1 ----&gt; The Pink Series.</strong></p>','<p data-gap="29">Object Box 1 '+ARW+' The Pink Series.</p>')
rep('<p data-gap="29">Phonemes ----------&gt; graphemes.</p>','<p data-gap="29">Phonemes '+ARW+' graphemes.</p>')
rep('<span class="mm-lab"><span class="mm-hc-0432FF">Reading</span>:\xa0</span>','<span class="mm-lab">Reading:\xa0</span>')
rep('<span class="mm-lab"><span class="mm-hc-0432FF">Decoding</span>:\xa0</span>','<span class="mm-lab">Decoding:\xa0</span>')
rep('<p data-gap="29"><span class="mm-hc-0432FF">Adjective </span>A medium blue triangle','<p class="mm-hanglab" data-gap="29"><span class="mm-lab"><span class="mm-hc-0432FF">Adjective</span> </span>A medium blue triangle')
n=[0]
def k(m):
    n[0]+=1; return m.group(0).replace('class="mm-hanglab"','class="mm-hanglab mm-knum"')
s=re.sub(r'<p class="mm-hanglab"[^>]*><span class="mm-lab">3\.\d+[ \xa0]</span>',k,s)
assert n[0]==17,n
open(f,'w').write(s);print('b1 ok')
