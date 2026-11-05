"""image_sizes.py <package.zip>   (29 Oct 2026 v5) - a REPORT, never a fault: the owner decides image sizes.
For every large image the page opens on a click (data-full), its longest side, and how many are under 1600 px (the most Hostinger
sends phones) and under 2900 px (the most it sends computers; both measured 25 Oct, confirmed by the owner 29 Oct).
It cannot compare with the owner's originals: they are not in the package."""
import sys, zipfile, re, io
from PIL import Image
z = zipfile.ZipFile(sys.argv[1]); slug = z.namelist()[0].split('/')[0]
s = z.read(slug + '/index.html').decode('utf-8'); full = list(dict.fromkeys(re.findall(r'data-full="([^"]+)"', s)))
rows = []
for f in full:
    try: w, h = Image.open(io.BytesIO(z.read(slug + '/' + f))).size; rows.append((f, max(w, h), w, h))
    except KeyError: rows.append((f, 0, 0, 0))
u16 = [r for r in rows if r[1] < 1600]; u29 = [r for r in rows if r[1] < 2900]
print('image sizes: %d large images; %d under 1600 px long side, %d under 2900 px; smallest %d px; missing %d' % (len(rows), len(u16), len(u29), min([r[1] for r in rows] or [0]), sum(1 for r in rows if r[1] == 0)))
print('  under 1600: ' + ', '.join('%s %dx%d' % (r[0].split('/')[-1], r[2], r[3]) for r in u16[:60]))
