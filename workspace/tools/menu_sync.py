"""24 Oct 2026: give a page the live site's menu (<nav> ... </nav>) taken from a live page, with this page's own entry
made a link and marked as the current page, and "The Prepared Environment" made a link (it goes live with 2.2.0).
usage: menu_sync.py <live page index.html> <folder name> <page index.html>..."""
import re, sys
src, folder, pages = sys.argv[1], sys.argv[2], sys.argv[3:]
def nav(s):
    i = s.find('<nav'); j = s.find('</nav>', i) + 6; assert i >= 0 and j > 6; return i, j
L = open(src, encoding='utf-8').read(); i, j = nav(L); N = L[i:j]
N = re.sub(r' aria-current="page"', '', N)
PE = '<li class="lead"><span class="np">The Prepared Environment</span></li>'
if PE in N: N = N.replace(PE, '<li class="lead"><a href="/the-prepared-environment/">The Prepared Environment</a></li>')
for p in pages:
    s = open(p, encoding='utf-8').read(); a, b = nav(s); old = s[a:b]
    cur = re.findall(r'<a class="top" href="(/[^"]*)" aria-current="page"', old)
    n = N
    for c in cur: n = n.replace('<a class="top" href="%s"' % c, '<a class="top" href="%s" aria-current="page"' % c, 1)
    k = n.count('href="/%s/">' % folder)
    n = n.replace('href="/%s/">' % folder, 'href="/%s/" aria-current="page">' % folder)
    s = s[:a] + n + s[b:]; open(p, 'w', encoding='utf-8').write(s)
    print(p, 'section marked:', cur, '| own entry marked:', k, '| prepared env link:', n.count('href="/the-prepared-environment/"'))
