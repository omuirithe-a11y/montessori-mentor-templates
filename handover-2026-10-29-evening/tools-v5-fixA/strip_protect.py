"""strip_protect.py <candidate.zip> <out.zip>: the owner's editing copy - removes only the copy-protection style and script blocks."""
import sys,zipfile,re
zi=zipfile.ZipFile(sys.argv[1]);zo=zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED)
for i in zi.infolist():
    d=zi.read(i)
    if i.filename.endswith('/index.html'):
        s=d.decode('utf-8');n0=len(s)
        s,a=re.subn(r'<style id="mm-protect">.*?</style>','',s,flags=re.S)
        s,b=re.subn(r'<script id="mm-protect-js">.*?</script>','',s,flags=re.S)
        assert a==1 and b==1,(a,b);print('removed',n0-len(s),'chars');d=s.encode('utf-8')
    zo.writestr(i,d)
zo.close()
