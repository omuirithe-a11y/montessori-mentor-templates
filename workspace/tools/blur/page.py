"""One command per page for the agreed blur method (claude/BLUR-METHOD-26-oct.md version 22, agreed 26 Oct 2026 13:47).
Written 26 Oct 2026 on the owner's instruction, 14:00: "fix these now" (the two tool faults: no single command per page,
and fixed model folders).

Before this, each page needed a set file written by hand and five commands in two folders. Now:

  python3 page.py new <name> --docx <Word file> [--faces <dir>] [--out <dir>] [--media <dir>]
                             [--prev <faces.json>] [--data <faces-data.json>]
  python3 page.py new <name> --match <match.json> [--faces <dir>] [--out <dir>]
        writes sets/<name>.json (folders, Word file, empty answers), making the faces folder, unpacking the Word
        file's images, and restoring the page's saved choices from <faces-data.json> if it was worked on before.
        --match is for images the owner uploaded that are in no Word file (they were matched to their places by hand
        until now): a JSON file {"<place on the page>": {"file": "<full path>"}, ...} as hires/amj-final.json and
        aun-final.json are written. Each image is copied to the set's media folder as image<place>.<ext>, and
        <out>/places.json records which uploaded file each one is, so the sheets and the build can name its place.

  python3 page.py find <name>
        method items 4-5: faces.py detect and pass2 (YuNet), then method.py detect (RetinaFace). Then it STOPS:
        items 6-8 are Claude's own eye - every face on the whole image, adults and rules, missed faces, hand points,
        and the RetinaFace candidates in <out>/candidates.jpg.

  python3 page.py sheet <name> "<title>" [<file.html>]
        method items 9-21: method.py blur, method_sheet.py (NOT CHECKED banner on), method_check.py. Then it STOPS:
        a SEPARATE agent has to check the sheet (items 20-23) before anyone sees it.

  python3 page.py release <name> <file.html>
        method item 39: the banner comes off only when that agent has written its pass for every part of it.

  python3 page.py handoff <name> --faces <build/<address>/faces> [--answer <key in review2.json>]
        the hand-off to the builder, which was done by one-off scripts until now: the blurred images copied under the
        names the page uses, a turn undone where the original is stored unturned, images with no face to blur left out,
        and the three files the builder's locks need (review2.json "final" from her recorded answer, sheet-check-final.json
        from the agent's pass, and the record photos-final.json). It writes no answer of its own and refuses without hers.

Every step prints what it did and what must happen next, so no step is skipped by accident. Each underlying tool is
run as its own command, so the method's own stops (missing model, missing library, no answer recorded) still apply.
The models are found by method.py from any folder (MM_LMK_MODEL / MM_SEG_MODEL, or beside the tools).
"""
import sys, os, json, subprocess, zipfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SETS = os.path.join(HERE, 'sets')
FACES_PY = os.path.join(os.path.dirname(HERE), 'w220', 'tools', 'faces.py')
for _c in (FACES_PY, os.path.join(os.path.dirname(HERE), 'ws', 'tools', 'faces.py'),
           os.path.join(os.path.dirname(HERE), 'tools', 'faces.py')):
    if os.path.exists(_c): FACES_PY = _c; break


def die(msg):
    raise SystemExit('STOP: ' + msg)


def set_path(name):
    p = os.path.join(SETS, name + '.json')
    if not os.path.exists(p):
        have = sorted(f[:-5] for f in os.listdir(SETS) if f.endswith('.json')) if os.path.isdir(SETS) else []
        die('no set called "%s" (%s). Make it with: page.py new %s --docx <Word file>\n  sets here: %s'
            % (name, p, name, ', '.join(have) or 'none'))
    return p


def load(name):
    return json.load(open(set_path(name)))


def run(args, what):
    print('\n--- %s\n    %s' % (what, ' '.join(args)), flush=True)
    r = subprocess.run([sys.executable] + args)
    if r.returncode:
        die('%s failed (exit %d). Nothing after it was run.' % (what, r.returncode))


def cmd_new(argv):
    if not argv: die('page.py new <name> --docx <Word file> [--faces <dir>] [--out <dir>] [--media <dir>] [--prev <faces.json>] [--data <faces-data.json>]')
    name = argv[0]; opt = {}
    k = 1
    while k < len(argv):
        if not argv[k].startswith('--') or k + 1 >= len(argv): die('bad argument: ' + argv[k])
        opt[argv[k][2:]] = argv[k + 1]; k += 2
    docx, match = opt.get('docx'), opt.get('match')
    if not docx and not match: die('--docx <Word file>, or --match <match.json> for uploaded images that are in no Word file')
    if docx and not os.path.exists(docx): die('Word file not found: ' + docx)
    if match and not os.path.exists(match): die('match file not found: ' + match)
    out = os.path.abspath(opt.get('out', os.path.join(HERE, 'm_' + name)))
    faces = os.path.abspath(opt.get('faces', os.path.join(out, 'faces')))
    media = os.path.abspath(opt.get('media', os.path.join(out, 'media')))
    os.makedirs(faces, exist_ok=True); os.makedirs(out, exist_ok=True)
    places = None
    if match:   # uploaded images, numbered by their place on the page (method item 3 assumes a Word file; these are not in one)
        os.makedirs(media, exist_ok=True); M = json.load(open(match)); places = {}
        for place, rec in sorted(M.items(), key=lambda kv: int(kv[0])):
            src_f = rec['file'] if isinstance(rec, dict) else rec
            if not os.path.exists(src_f): die('the match file names a file that is not here: ' + src_f)
            img = 'image%s%s' % (place, os.path.splitext(src_f)[1].lower())   # not "name" - that is the set's own name
            shutil.copyfile(src_f, os.path.join(media, img))
            places[img] = {'place': int(place), 'from': os.path.abspath(src_f)}
        json.dump(places, open(os.path.join(out, 'places.json'), 'w'), indent=1)
        print('%d uploaded images copied -> %s (places in %s)' % (len(places), media, os.path.join(out, 'places.json')))
    elif not opt.get('media'):   # the Word file's images, full size, exactly as stored (method item 14: never altered)
        os.makedirs(media, exist_ok=True); n = 0
        with zipfile.ZipFile(docx) as z:
            for m in z.namelist():
                if m.startswith('word/media/'):
                    with z.open(m) as f, open(os.path.join(media, os.path.basename(m)), 'wb') as g:
                        shutil.copyfileobj(f, g); n += 1
        print('%d images unpacked from the Word file -> %s' % (n, media))
    S = {'src': faces, 'work': os.path.join(faces, 'work'), 'media': media, 'out': out,
         'docx': os.path.abspath(docx) if docx else '',
         'answers': {}, 'candidates_ok': [],
         'made': '26 Oct 2026 or later, by page.py new - the agreed method version 22'}
    if places: S['match'] = os.path.abspath(match); S['places'] = os.path.join(out, 'places.json')
    if opt.get('prev'): S['prev'] = os.path.abspath(opt['prev'])
    os.makedirs(SETS, exist_ok=True)
    p = os.path.join(SETS, name + '.json')
    if os.path.exists(p): die('%s already exists. Delete it yourself if you mean to start this page again (its answers and hand fixes are in it).' % p)
    json.dump(S, open(p, 'w'), indent=1)
    print('set file written: ' + p)
    if opt.get('data'):
        if not os.path.exists(opt['data']): die('faces data file not found: ' + opt['data'])
        run([FACES_PY, 'restore', S['docx'], faces, os.path.abspath(opt['data'])], 'faces.py restore (the page\'s saved choices)')
    print('\nNEXT: python3 page.py find %s' % name)


def cmd_find(name):
    S = load(name)
    docx = S.get('docx')
    if not docx:   # a set made from a match file: faces.py needs a Word file, so one is made holding the images in place order
        docx = os.path.join(S['out'], 'images.docx')
        if not os.path.exists(docx):
            try:
                from docx import Document
                from docx.shared import Cm
            except Exception:
                die('python-docx is needed to put the uploaded images in place order for faces.py: pip install --break-system-packages python-docx')
            from PIL import Image
            P = json.load(open(S['places']))
            tmp = os.path.join(S['out'], 'for-docx'); os.makedirs(tmp, exist_ok=True)
            d = Document()
            for nm in sorted(P, key=lambda k: P[k]['place']):
                # 26 Oct 2026: python-docx reads JPEG markers strictly and refused some of her uploaded images
                # (the whole Culture Curriculum set), so each one is re-saved as a plain JPEG for this stand-in file only.
                # The originals are never touched and the blur runs on them, not on these copies.
                c = os.path.join(tmp, os.path.splitext(nm)[0] + '.jpg')
                Image.open(os.path.join(S['media'], nm)).convert('RGB').save(c, 'JPEG', quality=95)
                d.add_picture(c, width=Cm(10)); d.add_paragraph(nm)
            d.save(docx)
            print('%d uploaded images put in place order -> %s (for the face finding only; the blur is on the uploaded files themselves)' % (len(P), docx))
        S['docx'] = docx; json.dump(S, open(set_path(name), 'w'), indent=1)
    run([FACES_PY, 'detect', docx, S['src']], 'faces.py detect (YuNet, working copies) - method item 4')
    run([FACES_PY, 'pass2', docx, S['src']], 'faces.py pass2 (the more sensitive pass) - method item 5')
    if S.get('places'):
        # 26 Oct 2026: the stand-in Word file renumbers the images (image1.jpg, image2.jpg ...), so the faces would be
        # recorded under names that are not in the media folder and the blur would not find them. They are put back to
        # the real names here, by the place order the stand-in file was written in.
        P = json.load(open(S['places']))
        real = sorted(P, key=lambda k: P[k]['place'])
        det_p = os.path.join(S['src'], 'detections.json'); D = json.load(open(det_p))
        order = sorted(D, key=lambda k: D[k]['no'])
        if len(order) != len(real): die('the stand-in Word file holds %d images but the set has %d' % (len(order), len(real)))
        work = os.path.join(S['src'], 'work')
        newD = {}
        for old_n, new_n in zip(order, real):
            a, b = os.path.join(work, old_n), os.path.join(work, new_n)
            if os.path.exists(a) and a != b:
                if os.path.exists(b): os.remove(b)
                os.rename(a, b)
            newD[new_n] = D[old_n]
        json.dump(newD, open(det_p, 'w'), indent=1)
        print('the %d faces records put back to the page names (%s ... %s)' % (len(real), real[0], real[-1]))
    run([os.path.join(HERE, 'method.py'), 'detect', set_path(name)], 'method.py detect (RetinaFace) - method item 5')
    print('''
STOPPED HERE, as the method says. Items 6-8 are Claude's own eye, not code:
  - every face looked at on the whole image;
  - adults and the other rules into %s/by_rule.json, each with its reason, then "_checked": true;
  - missed faces into extra_faces.json; wrong points into hand_points.json; a box missing the eyes or mouth into adjust_faces.json;
  - the RetinaFace candidates in %s/candidates.jpg judged one by one; the ones that are faces go in the set file's
    "candidates_ok"; a face that cannot be decided is blurred and named at the top of the sheet.
NEXT, after that: python3 page.py sheet %s "<title>"''' % (S['src'], S['out'], name))


def cmd_sheet(name, title, dst=None):
    S = load(name)
    byr = os.path.join(S['src'], 'by_rule.json')
    if not (os.path.exists(byr) and json.load(open(byr)).get('_checked')):
        die('by_rule.json has no "_checked": true (method item 7). Every face is looked at by eye before the blur runs.')
    dst = dst or os.path.join(S['out'], name + '-sheet.html')
    run([os.path.join(HERE, 'method.py'), 'blur', set_path(name)], 'method.py blur (the area and the blur) - method items 9-14')
    run([os.path.join(HERE, 'method_sheet.py'), set_path(name), title, dst], 'method_sheet.py (the sheet, NOT CHECKED banner on) - items 16-19')
    run([os.path.join(HERE, 'method_check.py'), set_path(name), dst], 'method_check.py (the measurements for the checker) - items 20-21')
    print('''
STOPPED HERE, as the method says. The sheet is %s, with its NOT CHECKED banner on.
A SEPARATE agent that has not seen the work now checks it (items 20-23) and saves its report in the Project.
Only when it has written its pass: python3 page.py release %s %s
Then the sheet goes to the owner with its reports, and nothing else happens until she answers.''' % (dst, name, dst))


def cmd_handoff(name, argv):
    """The hand-off to the builder (method item 27 and the locks added 26 Oct). Written 26 Oct 2026 on the owner's
    instruction, 14:03; until then this was done with a one-off script each time."""
    from PIL import Image
    S = load(name); opt = {}
    k = 0
    while k < len(argv):
        if not argv[k].startswith('--') or k + 1 >= len(argv): die('bad argument: ' + argv[k])
        opt[argv[k][2:]] = argv[k + 1]; k += 2
    fdir = opt.get('faces') or die('page.py handoff <name> --faces <build/<address>/faces> [--answer <key>]')
    fdir = os.path.abspath(fdir)
    if not os.path.isdir(fdir): die('faces folder not found: ' + fdir)
    r2p = os.path.join(fdir, 'review2.json')
    if not os.path.exists(r2p):
        die("no review2.json in %s - the owner's answer is recorded there, word for word, before anything is built." % fdir)
    R = json.load(open(r2p))
    key = opt.get('answer')
    if not key:
        cands = [a for a, v in R.items() if isinstance(v, dict) and str(v.get('answer', v.get('words', ''))).strip()]
        if 'final' in R: key = 'final'
        elif len(cands) == 1: key = cands[0]
        else: die('review2.json holds %d recorded answers (%s). Name the one she last gave: --answer <key>'
                  % (len(cands), ', '.join(cands) or 'none'))
    ans = R.get(key) or die('review2.json has no "%s"' % key)
    words = str(ans.get('words', ans.get('answer', ''))).strip()
    if not words:
        die('"%s" in review2.json holds no words of hers. The build locks need her answer as she wrote it.' % key)
    ckp = os.path.join(S['out'], 'sheet-check.json')
    if not os.path.exists(ckp):
        die('no sheet-check.json in %s - a separate agent has not recorded a passed check of the sheet she answered.' % S['out'])
    CK = json.load(open(ckp))
    if not CK.get('pass'): die('sheet-check.json does not record a pass.')
    faces = json.load(open(os.path.join(S['out'], 'faces.json')))
    dst = os.path.join(fdir, 'photos-final')
    if os.path.exists(dst): shutil.rmtree(dst)
    os.makedirs(dst)
    rec, blurred, turned = [], 0, 0
    for img_name, v in sorted(faces.items(), key=lambda kv: int(kv[1].get('no', 0))):
        if not any(not f.get('skipped') for f in v.get('faces', [])):
            rec.append([img_name, 'no face to blur - the original is used as it is']); continue
        src_img = os.path.join(S['out'], 'images', os.path.splitext(img_name)[0] + '.jpg')
        if not os.path.exists(src_img):
            die('the blurred image is missing: %s. Run page.py sheet %s first.' % (src_img, name))
        orig = os.path.join(S['media'], img_name)
        if not os.path.exists(orig): die('the original is missing: ' + orig)
        bl = Image.open(src_img).convert('RGB')
        o = Image.open(orig).getexif().get(274, 1)
        note = 'blurred'
        if o in (3, 6, 8):   # the original is stored unturned and carries its turn in its EXIF; the page applies that turn
            bl = bl.transpose({3: Image.ROTATE_180, 6: Image.ROTATE_90, 8: Image.ROTATE_270}[o]); turned += 1
            note += ', the EXIF turn undone so the page turns it once'
        ext = os.path.splitext(img_name)[1].lower()
        bl.save(os.path.join(dst, img_name), 'PNG' if ext == '.png' else 'JPEG',
                **({} if ext == '.png' else {'quality': 95}))
        rec.append([img_name, note]); blurred += 1
    json.dump(rec, open(dst + '.json', 'w'), indent=0)
    R['final'] = {'answered': ans.get('answered', ''), 'sheet': ans.get('sheet', ''), 'words': words,
                  'check': '%s pass %s' % (ckp, CK.get('time', '')),
                  'source': '%s -> faces/photos-final (page names; the EXIF turn undone where the original is stored unturned)'
                            % os.path.join(S['out'], 'images'),
                  'recorded': 'by page.py handoff, from review2.json "%s" - her words, unchanged' % key}
    json.dump(R, open(r2p, 'w'), indent=1, ensure_ascii=False)
    shutil.copyfile(ckp, os.path.join(fdir, 'sheet-check-final.json'))
    print('%d blurred images -> %s (%d turned back); %d images left out with no face to blur'
          % (blurred, dst, turned, len(rec) - blurred))
    print('review2.json "final" written from her answer "%s" (key: %s); sheet-check-final.json copied.'
          % (words[:60], key))
    print('\nSTILL NEEDED before an upload zip can be made (the owner\'s Project instructions): a SEPARATE agent\'s pixel'
          '\ncheck of these final images, made AFTER her answer, recorded as\n  %s'
          '\nThen: build_page.py ... --photos %s' % (os.path.join(fdir, 'pixel-check-after-answer.json'), dst))


def cmd_release(name, dst):
    run([os.path.join(HERE, 'method_sheet.py'), 'release', set_path(name), dst], 'method_sheet.py release - method item 39')
    print('\nNEXT: send the sheet and every check report to the owner; record her answer word for word; map it to actions by method item 15.')


def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    c = sys.argv[1]
    if c == 'new': cmd_new(sys.argv[2:])
    elif c == 'find': cmd_find(sys.argv[2])
    elif c == 'sheet':
        if len(sys.argv) < 4: die('page.py sheet <name> "<title>" [<file.html>]')
        cmd_sheet(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif c == 'handoff':
        if len(sys.argv) < 3: die('page.py handoff <name> --faces <build/<address>/faces> [--answer <key>]')
        cmd_handoff(sys.argv[2], sys.argv[3:])
    elif c == 'release':
        if len(sys.argv) < 4: die('page.py release <name> <file.html>')
        cmd_release(sys.argv[2], sys.argv[3])
    else: raise SystemExit(__doc__)


main()
