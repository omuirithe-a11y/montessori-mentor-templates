import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
rep('<h2 class="mm-hc-0432FF centred" data-gap="48">Matching first sounds','<h2 class="mm-hc-0432FF centred" data-gap="48" data-mma="50" data-mmb="25">Matching first sounds')
rep('<h2 class="mm-hc-0432FF centred" data-gap="48">Letter + first sound','<h2 class="mm-hc-0432FF centred" data-gap="48" data-mma="50" data-mmb="25">Letter + first sound')
rep('<p class="mm-twocap mm-hc-0432FF">','<p class="mm-twocap mm-hc-0432FF" data-mma="50" data-mmb="25">')
rep('<p class="centred mm-hc-0432FF">A sample of some useless','<p class="centred mm-hc-0432FF" data-mma="50">A sample of some useless')
open(f,'w').write(s);print('b4 ok')
