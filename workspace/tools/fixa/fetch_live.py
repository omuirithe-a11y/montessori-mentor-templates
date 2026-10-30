#!/usr/bin/env python3
"""fetch_live.py <slug> <out dir>   (30 Oct 2026)
Downloads the live page's index.html byte for byte, and every image it names (src, data-full, url(...)) into <out dir>/<slug>/.
The images are FOR CHECKING ONLY: Hostinger sends re-compressed copies (Aun Aprendo 057.jpg: 975,999 bytes uploaded, 720,736
sent back, 30 Oct 16:1x), so they are never uploaded. Prints the counts and fails if any file is missing."""
import sys, os, re, urllib.request
slug, out = sys.argv[1], sys.argv[2]; base = 'https://montessorimentor.co.uk/%s/' % slug; d = os.path.join(out, slug)
os.makedirs(d, exist_ok=True)
get = lambda u, acc: urllib.request.urlopen(urllib.request.Request(u, headers={'Accept': acc, 'Cache-Control': 'no-cache'}), timeout=90).read()
html = get(base, 'text/html'); s = html.decode('utf-8')
if not s.rstrip().endswith('</html>'): sys.exit('index.html incomplete')
if get(base, 'text/html') != html: sys.exit('two downloads of index.html differ')
open(os.path.join(d, 'index.html'), 'wb').write(html)
refs = sorted(set(re.findall(r'(?:src|data-full)="(images/[^"]+)"', s) + re.findall(r"url\(['\"]?(images/[^)'\"]+)", s)))
miss = []
from concurrent.futures import ThreadPoolExecutor
def one(r):
    p = os.path.join(d, r); os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and os.path.getsize(p) > 0: return None   # kept from an earlier, stopped run
    try: open(p + '.part', 'wb').write(get(base + r, 'image/jpeg')); os.replace(p + '.part', p); return None
    except Exception as e: return (r, str(e)[:60])
with ThreadPoolExecutor(8) as ex: miss = [m for m in ex.map(one, refs) if m]   # 30 Oct 16:2x: 8 downloads at once (network, not processors)
print('%s: index.html %d bytes (two downloads identical), %d images named, %d downloaded' % (slug, len(html), len(refs), len(refs) - len(miss)))
if miss: print('MISSING:', miss); sys.exit(1)
