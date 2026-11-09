"""make_final.py <b8 zip> <approved page index.html (fin)> <out zip>
8 Nov 2026 (owner: "this page being built using the preview you just created is the priority"): the upload zip = b8's zip (the same Word file, photos and
template) with its index.html replaced by the approved One Spacing Preview page (version 10, with the one spacing script), copy protection put back
exactly where b8 had it, and image 152's files left out (owner: "image 152 - delete it")."""
import sys,zipfile,re
zi=zipfile.ZipFile(sys.argv[1]);fin=open(sys.argv[2],encoding='utf-8').read();out=sys.argv[3]
name=[n for n in zi.namelist() if n.endswith('/index.html')][0];old=zi.read(name).decode('utf-8')
for pat in (r'<style id="mm-protect">.*?</style>',r'<script id="mm-protect-js">.*?</script>'):
    m=re.search(pat,old,re.S);pre=old[max(0,m.start()-300):m.start()];post=old[m.end():m.end()+300]
    if fin.count(pre)==1:i=fin.index(pre)+len(pre)
    else:assert fin.count(post)==1,('context not found once',pat);i=fin.index(post)
    fin=fin[:i]+m.group(0)+fin[i:]
assert 'images/152' not in fin
zo=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED);skipped=[]
for i in zi.infolist():
    if re.search(r'/images/152(-\d+)?\.(jpg|webp|png)$',i.filename):skipped.append(i.filename);continue
    zo.writestr(i,fin.encode('utf-8') if i.filename==name else zi.read(i))
zo.close();print('index replaced; protection blocks put back: 2; left out:',skipped)
