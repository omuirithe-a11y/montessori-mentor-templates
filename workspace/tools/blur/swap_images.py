"""Put blurred images into a page that is already live, without rebuilding it from Word.
Written 26 Oct 2026 on the owner's instruction, 14:03: "fix all of these now" (there was no tool for this, and no locks).

    python3 swap_images.py <set.json> --faces <build/<address>/faces> --page <page folder>
                           --places <place list> [--out <folder>] [--zip]

<place list>: which blurred image goes to which image number on the page, as "<image in the set>=<page number>",
separated by commas - for example "image1.jpg=007,image2.jpg=015". Or --places <file.json> holding the same as
{"image1.jpg": "007", ...}. The page's own numbering is what Hostinger shows (images/007.jpg).

<page folder> is a copy of the live page (index.html and its images folder). The tool never writes into it: it copies
it to <out> (the default is <page folder>-swapped) and changes only the images named, writing both sizes the page uses -
images/NNN.jpg (full size, long side at most 2400, quality 92) and images/NNN-480.jpg (quality 88), exactly as
build_page.py writes them.

It refuses unless the same three things the builder needs are in the faces folder (the owner's Project instructions:
round 1 sheet, her answer, blur, round 2 sheet, her answer, a separate agent's pixel check, then build):
  review2.json "final"            - her last answer, word for word, with the sheet it answers and the agent's check
  sheet-check-final.json          - the separate agent's passed check of that sheet
  pixel-check-after-answer.json   - a separate agent's pixel check of the final images, made AFTER her answer
                                    (--waived "<her words, with the time>" if she has set that check aside for this page;
                                     her words are recorded in the swap record, and nothing is treated as a pass)
With --zip it also writes <out>.zip for upload. It prints exactly which files changed, so the change can be checked.
"""
import sys, os, json, shutil, hashlib
from PIL import Image

if len(sys.argv) < 2: raise SystemExit(__doc__)
S = json.load(open(sys.argv[1]))
opt = {}
k = 2
while k < len(sys.argv):
    if sys.argv[k] == '--zip': opt['zip'] = True; k += 1; continue
    if not sys.argv[k].startswith('--') or k + 1 >= len(sys.argv): raise SystemExit('STOP: bad argument: ' + sys.argv[k])
    opt[sys.argv[k][2:]] = sys.argv[k + 1]; k += 2


def die(m): raise SystemExit('STOP: ' + m)


fdir = os.path.abspath(opt.get('faces') or die('--faces <build/<address>/faces> is needed'))
page = os.path.abspath(opt.get('page') or die('--page <page folder> is needed'))
places_arg = opt.get('places') or die('--places "<image>=<number>,..." or --places <file.json> is needed')
out = os.path.abspath(opt.get('out', page.rstrip('/') + '-swapped'))

# --- the locks, the same three the builder uses ---
r2 = os.path.join(fdir, 'review2.json')
if not os.path.exists(r2): die('no review2.json in ' + fdir)
F = json.load(open(r2)).get('final') or die('review2.json has no "final" (her last answer). Make it with: page.py handoff')
if not str(F.get('words', '')).strip(): die('review2.json "final" holds no words of hers.')
sc = os.path.join(fdir, 'sheet-check-final.json')
if not os.path.exists(sc): die('no sheet-check-final.json in %s - the separate agent\'s passed check of the sheet she answered.' % fdir)
if not json.load(open(sc)).get('pass'): die('sheet-check-final.json does not record a pass.')
pc = os.path.join(fdir, 'pixel-check-after-answer.json')
# 26 Oct 2026 14:13: the owner can set this check aside for a page, in her own words. --waived records what she said;
# it is never written by Claude and never stands in for a pass. Without either, nothing is swapped.
if opt.get('waived'):
    P = {'pass': None, 'time': '', 'waived_by_the_owner': opt['waived']}
    print('NOTE: the separate agent\'s pixel check was set aside by the owner - "%s"' % opt['waived'])
else:
    if not os.path.exists(pc):
        die('no pixel-check-after-answer.json in %s.\n      Her Project instructions put a separate agent\'s pixel check after her\n      answer and before anything is built. Nothing is swapped until it is there,\n      or until she sets it aside in her own words: --waived "<her words, with the time>"' % fdir)
    P = json.load(open(pc))
    if not P.get('pass'): die('pixel-check-after-answer.json does not record a pass.')
    if str(P.get('time', ''))[:16] <= str(F.get('answered', ''))[:16]:
        die('the pixel check (%s) is not later than her answer (%s). It has to be made after it.' % (P.get('time'), F.get('answered')))

# --- which image goes where ---
if places_arg.endswith('.json') and os.path.exists(places_arg):
    PL = {k2: str(v) for k2, v in json.load(open(places_arg)).items()}
else:
    PL = {}
    for bit in places_arg.split(','):
        if '=' not in bit: die('--places wants "<image in the set>=<page number>", not "%s"' % bit)
        a, b = bit.split('=', 1); PL[a.strip()] = b.strip()
if not PL: die('--places named nothing')

src_dir = os.path.join(fdir, 'photos-final')
if not os.path.isdir(src_dir): die('no photos-final in %s (make it with: page.py handoff)' % fdir)
idx = os.path.join(page, 'index.html')
if not os.path.exists(idx): die('no index.html in ' + page)
html = open(idx, encoding='utf-8').read()

for img_name, num in PL.items():
    if not os.path.exists(os.path.join(src_dir, img_name)):
        die('%s is not in %s. The images with a face to blur are: %s' % (img_name, src_dir, ', '.join(sorted(os.listdir(src_dir))[:12])))
    if 'images/%s.jpg' % num not in html:
        die('the page does not use images/%s.jpg (from "%s"). Check the number against the page.' % (num, img_name))

if os.path.exists(out): shutil.rmtree(out)
shutil.copytree(page, out)
os.makedirs(os.path.join(out, 'images'), exist_ok=True)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


print('From %s\n  into a copy of %s\n  at %s\n' % (src_dir, page, out))
print('Her answer: "%s" (%s)\nSheet check: pass. Pixel check after her answer: %s\n' % (F['words'], F.get('answered', ''), ('set aside by her - "%s"' % opt['waived']) if opt.get('waived') else ('pass (%s)' % P.get('time', ''))))
done = []
for img_name, num in sorted(PL.items(), key=lambda kv: kv[1]):
    im = Image.open(os.path.join(src_dir, img_name)).convert('RGB')
    big = im.copy(); big.thumbnail((2400, 2400))
    bp = os.path.join(out, 'images', '%s.jpg' % num); big.save(bp, quality=92)
    sm = im.copy(); sm.thumbnail((480, 10000))
    sp = os.path.join(out, 'images', '%s-480.jpg' % num); sm.save(sp, quality=88)
    done.append((num, img_name, im.size, big.size, sm.size, sha(bp)[:16], sha(sp)[:16]))
    print('  %s.jpg  <- %-16s  %dx%d -> full %dx%d, small %dx%d' % (num, img_name, im.size[0], im.size[1], big.size[0], big.size[1], sm.size[0], sm.size[1]))

rec = {'made': 'blur2/swap_images.py, 26 Oct 2026 or later', 'from': src_dir, 'page': page, 'out': out,
       'her_answer': F, 'sheet_check': sc, 'pixel_check': P,
       'images': [{'page_number': d[0], 'from': d[1], 'full_sha256_16': d[5], 'small_sha256_16': d[6]} for d in done]}
json.dump(rec, open(os.path.join(out, 'swap-record.json'), 'w'), indent=1, ensure_ascii=False)
print('\n%d images changed, both sizes each. Nothing else in the page was touched (index.html unchanged).' % len(done))
print('Record: ' + os.path.join(out, 'swap-record.json'))

if opt.get('zip'):
    z = shutil.make_archive(out, 'zip', out)
    print('Upload file: ' + z)
print('\nNEXT: a separate agent checks the changed page, then it goes to the owner. Nothing is uploaded without her go.')
