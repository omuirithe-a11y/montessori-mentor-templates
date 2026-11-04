"""Preview photos for The English Curriculum (owner 4 Nov 18:08 "yes" to a preview build from the round 1 blurred images, as for 8.2 on 3 Nov):
copies each blurred image (blur2/m_eng/images/<stem>.jpg) under its Word media name, exactly as page.py handoff does for photos-final
(the EXIF turn undone where the original is stored unturned; images with no face to blur left out so the build uses the original).
usage: python3 preview_photos.py <set.json> <out folder>"""
import sys, os, json, shutil
from PIL import Image
S = json.load(open(sys.argv[1])); dst = sys.argv[2]
faces = json.load(open(os.path.join(S['out'], 'faces.json')))
if os.path.exists(dst): shutil.rmtree(dst)
os.makedirs(dst); rec = []; n = 0
for img_name, v in sorted(faces.items(), key=lambda kv: int(kv[1].get('no', 0))):
    if not any(not f.get('skipped') for f in v.get('faces', [])): rec.append([img_name, 'no face to blur - the original is used']); continue
    src = os.path.join(S['out'], 'images', os.path.splitext(img_name)[0] + '.jpg')
    if not os.path.exists(src): raise SystemExit('STOP: blurred image missing: ' + src)
    bl = Image.open(src).convert('RGB'); o = Image.open(os.path.join(S['media'], img_name)).getexif().get(274, 1); note = 'blurred (round 1 run)'
    if o in (3, 6, 8): bl = bl.transpose({3: Image.ROTATE_180, 6: Image.ROTATE_90, 8: Image.ROTATE_270}[o]); note += ', EXIF turn undone'
    ext = os.path.splitext(img_name)[1].lower()
    bl.save(os.path.join(dst, img_name), 'PNG' if ext == '.png' else 'JPEG', **({} if ext == '.png' else {'quality': 95})); rec.append([img_name, note]); n += 1
json.dump(rec, open(dst + '.json', 'w'), indent=0); print('preview photos:', n, 'blurred images copied to', dst)
