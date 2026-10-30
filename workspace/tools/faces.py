"""Faces for one page - 26 Oct 2026: the blur is the AGREED METHOD, claude/BLUR-METHOD-26-oct.md version 22 (SHA-256
1dc672e9f65e077e5e290ecf57cc30154848ce52501e8faba7c501a4405cb684; the owner's words 26 Oct 13:47: "I agree to
BLUR-METHOD-26-oct.md version 22 (attached)"), run with the tools in claude/workspace/tools/blur/ (method.py blur | sheet,
method_sheet.py, method_check.py, changed.py, grid.py, sets/<set>.json). The v8 blur of this file (eyes, nose and lips only)
was REJECTED by the owner on 25 Oct 20:23 and its commands here - sheet, blurfull, after, release, blur - now REFUSE
(26 Oct 2026, the owner 13:48: "update all immediately, replacing v8 with the attached file").
Still used from this file (method items 2, 4-6): detect and pass2 (YuNet, thresholds 0.72/0.88 and 0.45/0.6 at scales 1,
1.5, 2), pageorder, save and restore. The Drive "faces-tools" pack and blur_faces.py stay retired (yunet.onnx excepted).
The process (the owner's Project instructions, which come first): round 1 sheet, her answer, blur, round 2 sheet, her
answer, a separate agent's pixel check, then build.

History: rewritten 21 Oct 2026 from the faces pack in Drive folder "faces-tools":
find_faces.py, detect_lm.py, pass2.py, blur_faces.py, run_faces.py; the user's rules of 22-30 Sept). The 20 Oct version
of this file drew a plain oval and did NOT do v7 (user, 21 Oct 21:06: "correct this before doing anything else").

  python3 tools/faces.py detect <word.docx> <out>   working copies (long side 1600, panoramas 2400) of every Word photo in
                                                    <out>/work; faces found on each photo turned upright and both ways
                                                    sideways, with eyes, nose and mouth points -> <out>/detections.json
  python3 tools/faces.py pass2 <word.docx> <out>    the second, more sensitive pass (standard since 30 Sept): candidates
                                                    the first pass missed -> <out>/pass2.json and <out>/pass2-sheet.jpg.
                                                    Every candidate is checked by eye; real faces go into extra_faces.json
  python3 tools/faces.py sheet <word.docx> <out> [photo numbers]
                                                    round 1 sheet <out>/round1.html: only photos where blurring is in
                                                    question; red = to blur, orange = added by hand, grey = left by a rule
                                                    or by an earlier answer (reason shown). Under each photo, each face to
                                                    blur and each face kept by an earlier answer, large: the original with
                                                    its blur oval beside how it will look (full-size original, blur_local)
  python3 tools/faces.py blurfull <word.docx> <out> [photo numbers] the blur -> <out>/photos-full/<word name> (pass this folder to
                                                    build_page.py --photos). Refuses unless by_rule.json carries "_checked"
                                                    and review.json holds the user's answer to the current round 1 sheet
  python3 tools/faces.py after <word.docx> <out> <photo numbers | all>
                                                    round 2 sheet <out>/round2.html: only the images the user's answer
                                                    changed (or all, when a change touches every blur), as they now are,
                                                    with the same large pairs; "what changed" lines from <out>/notes.json
                                                    {"round2": [...]} (and {"round1": [...]} for round 1)
  python3 tools/faces.py pageorder <word.docx> <out> <built page index.html>
                                                    the page photo number of each Word photo -> <out>/page_order.json
                                                    (shown on the sheets beside the Word number)
  python3 tools/faces.py save <word.docx> <out> <file.json>
                                                    every choice for this page in one file (faces with their points, faces
                                                    added by hand, moved boxes, hand-placed points, rule decisions, earlier
                                                    answers, the user's words, sheet notes) - saved to the Project at
                                                    claude/workspace/faces-data/<page>.json after every round
  python3 tools/faces.py restore <word.docx> <out> <file.json>
                                                    the reverse: working copies remade from the Word file, the choices
                                                    written back, so any sheet can be made again in a later chat
  python3 tools/faces.py blur ...                   RETIRED 23 Oct 2026 (blur on 1600-pixel copies): refuses, use blurfull

Tested 21 Oct 2026: blur_image gives the same pixels as the Drive pack's blur_faces.py v7 on the same photo and faces
(0 pixels differ); every command run on a test Word file (a face found upright and sideways, with eye and mouth points).
Tested 23 Oct 2026 (15:4x) on 5.3 Classroom Management: detect gives the same boxes as the 22 Oct record (0.0px); sheet,
blurfull, after, save and restore run on its saved choices (see claude/workspace/faces-data/5.3-faces.json).

Who is blurred (26-28 Sept): only children photographed in the classroom. Never adults, blindfolded children, historical
photos, photos freely available online (printed pictures on cards and charts count), drawings, or "faces" on objects.
Each face a rule leaves is entered in <out>/by_rule.json ({"<image no>": {"<letter>": "<reason>"}, "_checked": true})
after checking EVERY face by eye on the whole photo; such faces are not put to the user.
The user's answer: keep_unblurred.json ({"<image no>": "<letters>"}), extra_faces.json ({"<image no>": [{"box":
[x0,y0,x1,y1], "lm": null|points, "lm_by_hand": bool}]}; added faces take the letters after the detected ones),
adjust_faces.json ({"<image no>": {"<letter>": [x0,y0,x1,y1]}}), review.json ({"date": ..., "sheet": "round1.html",
"words": "<the user's words>"}), review2.json (the same for round2.html; build_page.py refuses without it).
A photo the user does not comment on stays as it is. Date stamps stay visible; watermarks are never removed without the
user's word. Photos already blurred in Word are blurred again (harmless). Originals are never altered.
Photo numbers are Word's order of pictures, a line picture taller than 6 pixels included (2.1.2: image1.png is #1).

25 Oct 2026 (user 10:02, "too broad ... it needs to be precise"): v8 - per face only the area face_region gives: the
MediaPipe mesh outline of the eyes (with upper lids), nose and lips; else a rounded shape round the five points; else
tight_oval for a face with no points. Never forehead, hairline, ears, chin or neck. Strength follows the eye distance.
23 Oct 2026 (user): blur on copies of the FULL-SIZE originals only (command blurfull -> photos-full), centred on the eyes,
nose and mouth (blur_local); printed photos never blurred. The v7 description below is kept for its strengths; its
"whole face, hairline to jaw" oval is REPLACED by blur_local's oval.
v7 (blur_faces.py, 26 Sept): the whole face, up to the ears but not over them, hairline to jaw, not hair or neck - the
detector's face box as an oval turned with the face's angle (from the eyes); soft Gaussian, 7.7% of the face width,
ceiling 11px on the 1600px working copy; eyes and mouth a second layer at x1.45, ceiling 16px; feather 10% of the face
width. A face with no eye and mouth points (added by hand, profile) gets the even blur only and is listed in the report.

Sheets (23 Oct 2026, user 13:13-13:15: the sheet must let the user judge every face): each photo whole, faces drawn as
their blur ovals and lettered, turned as Word turns it; under it each face large (340px), its label above the pair,
original with its oval on the left, the blurred face on the right. Before a sheet is sent: pick faces at random and check
that you can tell whether the eyes, nose and mouth are blurred; then a separate agent checks it.
"""
import sys, os, io, json, zipfile, re, math, base64, html as _html
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont
Image.MAX_IMAGE_PIXELS = None
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(WS, 'faces', 'yunet.onnx')
L = list('abcdefghijklmnopqrstuvwxyz') + ['a' + c for c in 'abcdefghijklmnopqrstuvwxyz']
V7 = dict(fe=0.10, s=0.077, cap=11.0, feat=1.45, featcap=16.0)
H = _html.escape

# ------------------------------------------------------------------ photos (Word order) and working copies
def photos(docx):
    z = zipfile.ZipFile(docx)
    doc = z.read('word/document.xml').decode('utf8'); rels = z.read('word/_rels/document.xml.rels').decode('utf8')
    R = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels)) | {k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)}
    order = []
    for rid in re.findall(r'r:(?:embed|id)="(rId\d+)"', doc):
        t = R.get(rid, '')
        if t.startswith('media/') and t not in order: order.append(t)
    out = []
    # 24 Oct 2026 (2.2.0: 214 pictures, 1.1 GB - every picture held open at once ran out of memory): each picture is
    # written to <docx>.media/ once and opened from there only when used (LazyIm); the pictures themselves are unchanged
    md = docx + '.media'; os.makedirs(md, exist_ok=True)
    for t in order:
        fp = os.path.join(md, os.path.basename(t))
        try:
            if not os.path.exists(fp):
                with z.open('word/' + t) as src_, open(fp, 'wb') as dst_:
                    while True:
                        b_ = src_.read(1 << 22)
                        if not b_: break
                        dst_.write(b_)
            im = LazyIm(fp)
        except Exception: continue
        if im.height <= 6 or im.width <= 6: continue   # line pictures
        out.append((os.path.basename(t), im))
    return out

class LazyIm:
    """A picture opened from disk each time it is used, so no more than one is held in memory."""
    def __init__(self, path):
        self.path = path
        with Image.open(path) as i: i.load(); self.size = i.size; self.mode = i.mode; self.format = i.format; self.info = dict(i.info)
        self.width, self.height = self.size
    def __getattr__(self, k):
        im = Image.open(self.path); im.load(); return getattr(im, k)

def word_turns(docx):   # 22 Oct 2026: how Word turns each photo on the page (a:xfrm rot, 60000ths of a degree) -> quarter turns clockwise
    z = zipfile.ZipFile(docx); doc = z.read('word/document.xml').decode('utf8'); rels = z.read('word/_rels/document.xml.rels').decode('utf8')
    R = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels)) | {k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)}
    out = {}
    for d in re.findall(r'<w:drawing>.*?</w:drawing>', doc, re.S):
        m = re.search(r'r:embed="(rId\d+)"', d); r = re.search(r'<a:xfrm[^>]*\brot="(-?\d+)"', d)
        if m and r: out[os.path.basename(R.get(m.group(1), ''))] = round(int(r.group(1)) / 5400000) % 4
    return out

def working_copy(out, name, im):   # find_faces.py: long side 1600, panoramas (wider than 2:1) 2400
    p = os.path.join(out, 'work', name); os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        cap = 2400 if im.width / im.height > 2 else 1600; rgb = im.convert('RGB')
        if max(im.size) > cap:
            k = cap / max(im.size); rgb = rgb.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        if name.lower().endswith('.png'): rgb.save(p, 'PNG', optimize=True)
        else: rgb.save(p, 'JPEG', quality=92)
    return p

# ------------------------------------------------------------------ detection (find_faces.py + detect_lm.py)
_det = None
def _detector():
    global _det
    if _det is None: _det = cv2.FaceDetectorYN.create(MODEL, '', (320, 320), 0.3, 0.3, 5000)
    return _det
def unrot(X, Y, k, ww, hh):   # np.rot90 (ccw) k times: a point in the turned picture -> the original
    cw, ch = ww, hh
    for _ in range(k): X, Y = (ch - 1 - Y), X; cw, ch = ch, cw
    return X, Y
def detect(bgr, thr0=0.72, thr1=0.88, extra_scales=False):
    det = _detector(); found = []
    for k in (0, 1, 3):   # upright, and both ways sideways (stricter)
        r = np.rot90(bgr, k).copy(); hh, ww = r.shape[:2]
        scales = (1.0, 2.0) if max(hh, ww) <= 1200 else (1.0,)
        if extra_scales: scales = (1.0, 1.5, 2.0)
        for sc in scales:
            rr = cv2.resize(r, (int(ww * sc), int(hh * sc))) if sc != 1 else r
            det.setInputSize((rr.shape[1], rr.shape[0])); _, faces = det.detect(rr)
            if faces is None: continue
            for f in faces:
                score = float(f[-1])
                if score < (thr0 if k == 0 else thr1): continue
                fx, fy, fw, fh = f[0] / sc, f[1] / sc, f[2] / sc, f[3] / sc
                xs, ys = [], []
                for (px, py) in [(fx, fy), (fx + fw, fy), (fx, fy + fh), (fx + fw, fy + fh)]:
                    X, Y = unrot(px, py, k, ww, hh); xs.append(X); ys.append(Y)
                lm = [unrot(f[4 + 2 * j] / sc, f[5 + 2 * j] / sc, k, ww, hh) for j in range(5)]
                found.append([min(xs), min(ys), max(xs), max(ys), score, [[float(a), float(b)] for a, b in lm]])
    found.sort(key=lambda b: -b[4]); keep = []
    for b in found:   # overlapping boxes merged, the best kept
        if all(max(0, min(b[2], k2[2]) - max(b[0], k2[0])) * max(0, min(b[3], k2[3]) - max(b[1], k2[1]))
               <= 0.3 * min((b[2] - b[0]) * (b[3] - b[1]), (k2[2] - k2[0]) * (k2[3] - k2[1])) for k2 in keep):
            keep.append(b)
    return keep
def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1])); i = ix * iy
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-9)
def ov(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return ix * iy / max(1, min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])))
def in_box(bgr, box):   # eyes and mouth for a face added by hand: the detector again on that area, enlarged, lower threshold
    H_, W = bgr.shape[:2]; x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    X0, Y0, X1, Y1 = int(max(0, x0 - w)), int(max(0, y0 - h)), int(min(W, x1 + w)), int(min(H_, y1 + h))
    crop = bgr[Y0:Y1, X0:X1]; s = max(1.0, 320 / max(crop.shape[:2])); crop = cv2.resize(crop, (int(crop.shape[1] * s), int(crop.shape[0] * s)))
    best = None
    for b in detect(crop, 0.3, 0.5, extra_scales=True):
        bb = [X0 + b[0] / s, Y0 + b[1] / s, X0 + b[2] / s, Y0 + b[3] / s]
        if iou(bb, box) > 0.2 and (best is None or b[4] > best[0]): best = (b[4], [[X0 + p[0] / s, Y0 + p[1] / s] for p in b[5]])
    return best[1] if best else None
def bgr_of(p): return cv2.cvtColor(np.asarray(Image.open(p).convert('RGB')), cv2.COLOR_RGB2BGR)

# ------------------------------------------------------------------ lists
def jl(out, name, default):
    p = os.path.join(out, name); return json.load(open(p)) if os.path.exists(p) else default
class HandPts(list):   # 25 Oct 2026 (round 1 checks: 22e, 22c, 12i, 14e, 9d): points placed by hand are the authority - the
    pass               # blur uses the rounded shape round them (plus the point circles), never the face mesh, which overruled them
def _hp(src, pts): return HandPts(pts) if isinstance(src, HandPts) else pts
def faces_of(out, D, n):
    """Every face of a photo, lettered: detected ones first, then added ones -> [(letter, box, lm, added)]."""
    v = D[n]; no = str(v['no']); EX = jl(out, 'extra_faces.json', {}); ADJ = jl(out, 'adjust_faces.json', {})
    PTS = jl(out, 'hand_points.json', {})   # 28 Sept rule: wrong eye and mouth points are placed by hand, never the even blur instead
    fs = [(L[k], ADJ.get(no, {}).get(L[k], f[:4]), (HandPts(PTS[no][L[k]]) if PTS.get(no, {}).get(L[k]) else (v.get('landmarks') or [None] * 99)[k]), False) for k, f in enumerate(v['faces'])]
    fs += [(L[len(v['faces']) + j], ADJ.get(no, {}).get(L[len(v['faces']) + j], e['box']), (HandPts(e['lm']) if e.get('lm') else None), True) for j, e in enumerate(EX.get(no, []))]
    return fs
def kept_of(KEEP, no): return set(re.findall(r'a?[a-z]', KEEP.get(no, '')))   # 24 Oct 2026: write letters with commas ("a,b,c") - "ab" reads as the one face ab (after z)

# ------------------------------------------------------------------ v7 blur (blur_faces.py, unchanged numbers)
def ellipse_mask(size, ell, feather):
    cx, cy, a, b, ang = ell
    side = int(2 * max(a, b) + 6 * feather + 6); big = Image.new('L', (side, side), 0); d = ImageDraw.Draw(big)
    c = side / 2; d.ellipse((c - a, c - b, c + a, c + b), fill=255)
    big = big.rotate(-ang, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(feather))
    m = Image.new('L', size, 0); m.paste(big, (int(cx - c), int(cy - c))); return m
def blur_image(src_path, faces, dst_path, V=V7):   # the 26 Sept v7 blur (whole face box) - kept for reference only; no command uses it since 23 Oct 2026
    base = Image.open(src_path).convert('RGB'); layers = []
    for box, lm in faces:
        x0, y0, x1, y1 = box; w = x1 - x0; h = y1 - y0
        r = min(V['cap'], max(1.5, w * V['s'])); ang = 0.0
        if lm:
            (lx, ly), (rx, ry) = lm[0], lm[1]; ang = math.degrees(math.atan2(ry - ly, rx - lx))
        layers.append((r, ellipse_mask(base.size, (x0 + w / 2, y0 + h / 2, 0.5 * w, 0.5 * h, ang), feather=max(2, V['fe'] * w))))
        if lm:
            (lx, ly), (rx, ry), (nx, ny), (mlx, mly), (mrx, mry) = lm
            e = max(math.hypot(rx - lx, ry - ly), 0.38 * w); rf = min(V['featcap'], r * V['feat'])
            em = ellipse_mask(base.size, ((lx + rx) / 2, (ly + ry) / 2, 0.95 * e, 0.36 * e, ang), feather=max(2, 0.12 * e))
            mw = max(math.hypot(mrx - mlx, mry - mly), 0.5 * e)
            mm = ellipse_mask(base.size, ((mlx + mrx) / 2, (mly + mry) / 2, 0.8 * mw, 0.34 * e, ang), feather=max(2, 0.12 * e))
            layers.append((rf, Image.fromarray(np.maximum(np.asarray(em), np.asarray(mm)))))
    res = base
    for r, m in sorted(layers, key=lambda t: t[0]):   # lightest first
        bl = res.filter(ImageFilter.GaussianBlur(r)).filter(ImageFilter.GaussianBlur(r * 0.5))
        res = Image.composite(bl, res, m)
    if dst_path.lower().endswith('.png'): res.save(dst_path, 'PNG', optimize=True)
    else: res.save(dst_path, 'JPEG', quality=92)

# 25 Oct 2026 (user 10:02, v8): v8 tight blur (25 Oct 2026, user 10:02: "the blurring needs to be localised, centred on the eyes nose and mouth ... a massive
# blur that covers the forehead neck ears etc. it's too broad. it needs to be precise"): one oval hugging the eyes, nose and
# mouth - from just above the eyebrows to just below the lower lip, and across the eyes' outer corners - not forehead, ears,
# chin or neck. Strong blur inside, short feather.
def tight_oval(box, lm):
    x0, y0, x1, y1 = box; w = x1 - x0; h = y1 - y0
    if not lm: return (x0 + w / 2, y0 + 0.56 * h, 0.34 * w, 0.30 * h, 0.0), 0.6 * w / 1.6
    (lx, ly), (rx, ry), (nx, ny), (mlx, mly), (mrx, mry) = lm
    ang = math.degrees(math.atan2(ry - ly, rx - lx)); t = math.radians(ang)
    e = max(math.hypot(rx - lx, ry - ly), 0.28 * w)
    ex, ey = (lx + rx) / 2, (ly + ry) / 2; mx, my = (mlx + mrx) / 2, (mly + mry) / 2
    d = max(math.hypot(mx - ex, my - ey), 0.75 * e)        # eyes to mouth
    ux, uy = (ex - mx) / d, (ey - my) / d                  # unit step from mouth towards eyes
    cx, cy = (ex + mx) / 2 + 0.08 * e * ux, (ey + my) / 2 + 0.08 * e * uy   # a little towards the eyes: eyelids and brows covered, chin not
    a = 0.76 * e; b = d / 2 + 0.34 * e                     # eyebrows to lower lip; across the eyes' outer corners
    # every point (incl. a side-view nose) inside 0.8 of the edge
    k = 1.0
    for px, py in lm:
        dx, dy = px - cx, py - cy; u = dx * math.cos(t) + dy * math.sin(t); v = -dx * math.sin(t) + dy * math.cos(t)
        k = max(k, math.sqrt((u / a) ** 2 + (v / b) ** 2) / 0.9)
    return (cx, cy, a * k, b * k, ang), e
def oval_of(box, lm):   # the oval drawn on the sheets = the oval blurred
    return tight_oval(box, lm)[0]
def oval_points(ell, k=1.0, n=72):   # the oval as a polygon, scaled by k (for drawing on a resized picture)
    cx, cy, a, b, ang = ell; t = math.radians(ang)
    return [((cx + a * math.cos(u) * math.cos(t) - b * math.sin(u) * math.sin(t)) * k,
             (cy + a * math.cos(u) * math.sin(t) + b * math.sin(u) * math.cos(t)) * k) for u in [2 * math.pi * i / n for i in range(n)]]
# 25 Oct 2026 (user 10:02 "it needs to be precise"; the 5-point oval missed eyes or mouths on 11 of 26 faces): the blurred area
# comes from MediaPipe's face mesh (478 points) where it finds the face - the outline of both eyes with their lids, the
# nose and the lips, joined, with the upper lids (0.22 x the eye-to-eye distance above the eyes) and widened by 0.18 x that distance - never forehead, ears, chin or
# neck. Where the mesh finds nothing, or disagrees with the face's own eye and mouth points (a wrong face), the tight oval
# (tight_oval) on the five points is used. Model: models/face_landmarker.task (MediaPipe, float16 v1; see README).
_MESH = None
_ME_L = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]; _ME_R = [263,249,390,373,374,380,381,382,362,398,384,385,386,387,388,466]
_MN = [1,2,98,327,4,5,195,197,6]; _MLIP = [61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185]
def _mesh():
    global _MESH
    if _MESH is None:
        # 25 Oct 2026 (user 13:07, "guarantee that all of these steps are used every time"): no precise face points, no blur -
        # a missing library or model stops the run instead of falling back quietly to the rougher five-point shape
        try:
            import mediapipe as mp
            from mediapipe.tasks import python as mpt
            from mediapipe.tasks.python import vision
        except Exception as ex:
            raise SystemExit('STOP: mediapipe is not installed (%s). Install it as README "Added 25 Oct 2026" says, then run again.' % ex)
        if getattr(mp, '__version__', '') != '0.10.32':   # 25 Oct 2026: the version every precise blur was made and measured with
            raise SystemExit('STOP: mediapipe %s installed; 0.10.32 needed (README "Added 25 Oct 2026").' % getattr(mp, '__version__', '?'))
        mp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'face_landmarker.task')
        if not os.path.exists(mp_path): mp_path = '/home/claude/mm/models/face_landmarker.task'
        if not os.path.exists(mp_path):
            raise SystemExit('STOP: models/face_landmarker.task is missing. Download it as README "Added 25 Oct 2026" says, then run again.')
        o = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=mp_path), num_faces=3,
                                         min_face_detection_confidence=0.3, min_face_presence_confidence=0.3)
        _MESH = (mp, vision.FaceLandmarker.create_from_options(o))
    return _MESH
_REG = {}
class _Hand(Exception): pass
def face_region(img, box, lm):
    """('mesh', polygon, e) or ('oval', ellipse, e) - the area to blur for one face, in img's coordinates."""
    key = (id(img), img.size, tuple(round(c, 1) for c in box), tuple(tuple(round(c, 1) for c in q) for q in lm) if lm else None, isinstance(lm, HandPts))
    if key in _REG: return _REG[key]
    ell, e5 = tight_oval(box, lm); res = ('oval', ell, e5)
    if (box[2] - box[0]) < 0.0125 * img.size[0] and lm:   # 25 Oct 2026 14:45 (user: "tiny faces: B"): a face narrower than 1.25% of the image keeps
        # to its eyes, nose and mouth - the rounded shape round its five points - with a blur twice as strong (2 x the eye distance passed on)
        import cv2
        (lx, ly), (rx, ry) = lm[0], lm[1]; e_ = max(math.hypot(rx - lx, ry - ly), 0.28 * (box[2] - box[0]), 2.0); cir = []
        for j_, (px_, py_) in enumerate(lm):
            rr = 0.55 * e_ if j_ < 2 else (0.36 * e_ if j_ == 2 else 0.42 * e_)
            cir += [(px_ + rr * math.cos(t), py_ + rr * math.sin(t)) for t in [2 * math.pi * i / 20 for i in range(20)]]
        _REG[key] = ('mesh', [tuple(q) for q in cv2.convexHull(np.array(cir, dtype=np.float32)).reshape(-1, 2)], 2 * e_); return _REG[key]
    if (box[2] - box[0]) < 0.0125 * img.size[0]:   # a tiny face with no points: its whole box (25 Oct 2026, round 2 check: 2d)
        _REG[key] = ('oval', ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 0.55 * (box[2] - box[0]), 0.55 * (box[3] - box[1]), 0.0), max(e5, 0.3 * (box[2] - box[0]))); return _REG[key]
    if lm:   # 25 Oct (4a, head bent): the 5 points' own outline - a rounded shape round each eye, the nose and the mouth corners -
        # instead of an oval turned to the eye line, which grew over chin and neck when the face is tilted or foreshortened
        import cv2
        (lx, ly), (rx, ry) = lm[0], lm[1]; x0_, y0_, x1_, y1_ = box
        hp_ = isinstance(lm, HandPts)   # 25 Oct 16:1x (Word12 check: hand-placed faces 1.4-1.8 x the mesh area): hand-placed points are
        # exact, so their rounded shape is drawn closer - eye distance at least 0.22 (not 0.28) of the box width, circles 0.8 of the size
        e_ = max(math.hypot(rx - lx, ry - ly), (0.22 if hp_ else 0.28) * (x1_ - x0_), 2.0)
        cir = []
        for j_, (px_, py_) in enumerate(lm):
            rr = (0.8 if hp_ else 1.0) * (0.55 * e_ if j_ < 2 else (0.36 * e_ if j_ == 2 else 0.42 * e_))   # 25 Oct (check: 7a lip, 5a eye corner left)
            cir += [(px_ + rr * math.cos(t), py_ + rr * math.sin(t)) for t in [2 * math.pi * i / 20 for i in range(20)]]
        hull = cv2.convexHull(np.array(cir, dtype=np.float32)).reshape(-1, 2)
        res = ('mesh', [tuple(q) for q in hull], e_)
    try:
        if isinstance(lm, HandPts): raise _Hand()   # hand-placed points: the rounded shape round them, not the mesh
        mp, LM = _mesh(); x0, y0, x1, y1 = box; S = max(x1 - x0, y1 - y0) * 2.6; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        L, T = cx - S / 2, cy - S / 2
        crop = img.crop((int(L), int(T), int(L + S), int(T + S))).convert('RGB').resize((480, 480))
        r = LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(crop).copy()))
        if r.face_landmarks:
            f = min(r.face_landmarks, key=lambda q: (q[1].x - 0.5) ** 2 + (q[1].y - 0.5) ** 2)
            P = lambda ids: np.array([(L + f[i].x * S * (int(L + S) - int(L)) / S, T + f[i].y * S * (int(T + S) - int(T)) / S) for i in ids])
            le, rr, no_, li = P(_ME_L), P(_ME_R), P(_MN), P(_MLIP)
            e = float(np.hypot(*(le.mean(0) - rr.mean(0))))
            pts = np.vstack([le, rr, no_, li]); e = max(e, 0.45 * float(np.ptp(pts[:, 0])), 2.0)
            ok = x0 - 0.2 * (x1 - x0) <= no_[0][0] <= x1 + 0.2 * (x1 - x0) and y0 - 0.2 * (y1 - y0) <= no_[0][1] <= y1 + 0.2 * (y1 - y0)
            if ok and lm:   # agrees with the face's own points (else it is another face, or a wrong fit)
                (lx, ly), (rx, ry), _n, (mlx, mly), (mrx, mry) = lm
                e_lm = max(math.hypot(rx - lx, ry - ly), 0.28 * (x1 - x0))
                de = math.hypot((lx + rx) / 2 - (le.mean(0)[0] + rr.mean(0)[0]) / 2, (ly + ry) / 2 - (le.mean(0)[1] + rr.mean(0)[1]) / 2)
                dm = math.hypot((mlx + mrx) / 2 - li.mean(0)[0], (mly + mry) / 2 - li.mean(0)[1])
                ok = de < 0.6 * e_lm and dm < 0.6 * e_lm
            if ok:
                import cv2
                dv0 = (li.mean(0) - (le.mean(0) + rr.mean(0)) / 2); dv0 = dv0 / max(1e-6, float(np.hypot(*dv0)))
                pts = np.vstack([pts, le - dv0 * 0.22 * e, rr - dv0 * 0.22 * e])   # 25 Oct (check: 11a, 8a eyes at the top edge): the upper lids too
                hull = cv2.convexHull(pts.astype(np.float32)).reshape(-1, 2); c = hull.mean(0); g = 0.18 * e
                poly = [c + (q - c) * (1 + g / max(1e-6, float(np.hypot(*(q - c))))) for q in hull]
                # 25 Oct (check: chin covered on 6a, 11a): nothing lower than 0.10 x eye distance below the lowest lip point
                dv = (li.mean(0) - (le.mean(0) + rr.mean(0)) / 2); dv = dv / max(1e-6, float(np.hypot(*dv)))
                lim = max(float(np.dot(q - c, dv)) for q in li) + 0.10 * e
                poly = [tuple(q - dv * max(0.0, float(np.dot(q - c, dv)) - lim)) for q in poly]
                if lm and res[0] == 'mesh':   # 25 Oct 2026 (round 2 check: 70d, 118a, 139a, 143d): the face's own eye, nose and mouth
                    # points (detector's or placed by hand) are always inside - the mesh outline is joined with the rounded shape round them
                    # (14:3x: small circles round the points only - 0.25 x the eye distance - not the whole rounded shape, which grew
                    # 109 of 262 areas by over 25%)
                    _pc = [(px_ + 0.25 * e * math.cos(t_), py_ + 0.25 * e * math.sin(t_)) for px_, py_ in lm for t_ in [2 * math.pi * i / 16 for i in range(16)]]
                    hull2 = cv2.convexHull(np.array(list(poly) + _pc, dtype=np.float32)).reshape(-1, 2)
                    poly = [tuple(q) for q in hull2]
                res = ('mesh', poly, e)
    except _Hand:
        pass
    except Exception as ex:
        print('  mesh not used:', ex)
    _REG[key] = res; return res
def region_points(img, box, lm, k=1.0):   # the outline of the blurred area, scaled by k (for drawing)
    kind, g, e = face_region(img, box, lm)
    return [(x * k, y * k) for x, y in g] if kind == 'mesh' else oval_points(g, k)
def region_mask(img, box, lm):
    kind, g, e = face_region(img, box, lm); fe = max(1.5, 0.07 * e)
    if kind == 'oval': return ellipse_mask(img.size, g, feather=fe), e
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon(g, fill=255)
    return m.filter(ImageFilter.GaussianBlur(fe)), e
def blur_local(src_path, faces, dst_path, V=V7):
    """25 Oct 2026 (v8, user 10:02 "it needs to be precise"): per face, only the area face_region gives - the mesh outline of the
    eyes with upper lids, nose and lips; else the rounded shape round the five points; else tight_oval - strong blur inside, short feather. Replaces the 23-24 Oct oval with its eye/nose/mouth second layer, which
    spread over forehead, ears, chin and neck. V is kept for callers; the strength now follows the eye distance.
    src_path may be a path or a PIL image; dst_path None returns the image instead of saving it."""
    base = (src_path if isinstance(src_path, Image.Image) else Image.open(src_path)).convert('RGB'); res = base
    for box, lm in faces:
        m, e = region_mask(base, box, lm)   # 25 Oct: the mesh outline of eyes, nose and lips where found, else the tight oval
        r = max(2.5, 0.26 * e)
        bl = res.filter(ImageFilter.GaussianBlur(r)).filter(ImageFilter.GaussianBlur(r * 0.6))
        res = Image.composite(bl, res, m)
    if dst_path is None: return res
    if dst_path.lower().endswith('.png'): res.save(dst_path, 'PNG', optimize=True)
    else: res.save(dst_path, 'JPEG', quality=92)

def full_faces(out, n, faces, ORIG):
    """Boxes and points of the given faces (working-copy scale) moved to the full-size original, and the scaled strengths."""
    wk = Image.open(os.path.join(out, 'work', n)); im = ORIG[n]; k = im.width / wk.width
    fs = [([float(c) * k for c in f[1]], _hp(f[2], [[float(x) * k, float(y) * k] for x, y in f[2]]) if f[2] else None) for f in faces]
    V = dict(V7); V['cap'] *= k; V['featcap'] *= k
    return im.convert('RGB'), fs, V, k
def blurred_full(out, n, faces, ORIG):   # the full-size original with these faces blurred, in memory (nothing saved)
    im, fs, V, k = full_faces(out, n, faces, ORIG)
    return (blur_local(im, fs, None, V) if fs else im), k

# ------------------------------------------------------------------ sheets
try: FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
except Exception: FONT = ImageFont.load_default()
try: FONT_BIG = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception: FONT_BIG = FONT
RED, ORANGE, GREEN, GREY = (220, 20, 20), (230, 120, 0), (10, 140, 40), (150, 150, 150)
def b64(im, q=85):
    bb = io.BytesIO(); im.convert('RGB').save(bb, 'JPEG', quality=q); return base64.b64encode(bb.getvalue()).decode()
def turned(im, k):   # a quarter turn clockwise k times, as Word shows the photo
    for _ in range(k % 4): im = im.rotate(-90, expand=True)
    return im
def card_img(img, boxes, s, turns=0, font=FONT):
    """The whole photo at scale s: each face drawn as its blur oval (oval_of), the picture turned as Word turns it, the
    letters placed upright at the top-left of each oval after turning (22-23 Oct 2026)."""
    t = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))))
    dd = ImageDraw.Draw(t); bs = []
    for e_ in boxes:
        letter, box, colour = e_[0], e_[1], e_[2]; lm = e_[4] if len(e_) > 4 else None
        pts = region_points(img, box, lm, s); dd.polygon(pts, outline=colour, width=3)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; bs.append((letter, [min(xs), min(ys), max(xs), max(ys)], colour))
    for _ in range(turns % 4):
        h_ = t.height; t = t.rotate(-90, expand=True)
        bs = [(l, [h_ - b[3], b[0], h_ - b[1], b[2]], c) for (l, b, c) in bs]
    d = ImageDraw.Draw(t)
    for (letter, b, colour) in bs:
        d.text((b[0] + 2, max(0, b[1] - (font.size + 6 if hasattr(font, 'size') else 22))), letter, fill=colour, font=font, stroke_width=3, stroke_fill=(255, 255, 255))
    return t
def card(img, boxes, s, turns=0):   # the same, as base64 (kept for callers of the 22 Oct version)
    bb = io.BytesIO(); card_img(img, boxes, s, turns).save(bb, 'JPEG', quality=82); return base64.b64encode(bb.getvalue()).decode()

def face_box(f, k, size=None):   # the square around a face on the full-size original that its close-up shows
    x0, y0, x1, y1 = [c * k for c in f[1]]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; r = max(x1 - x0, y1 - y0) * 1.4
    if size:   # 23 Oct 2026 (5.3 test, 5d): kept inside the photo - a square past the edge showed a black band
        W, H_ = size; r = min(r, W / 2, H_ / 2); cx = min(max(cx, r), W - r); cy = min(max(cy, r), H_ - r)
    return (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
def pair_html(no, f, why, orig, after, k, turns, after_label, cls, blurred=True):
    """One face, large: the label above, the original with its blur oval (white) on the left, the other picture on the right."""
    box = face_box(f, k, orig.size); S = 340
    oc = orig.crop(box).resize((S, S)); sc = S / (box[2] - box[0])
    rp = region_points(orig, [c * k for c in f[1]], _hp(f[2], [[x * k, y * k] for x, y in f[2]]) if f[2] else None, sc)
    ImageDraw.Draw(oc).polygon([(x - box[0] * sc, y - box[1] * sc) for x, y in rp], outline=(255, 255, 255), width=2)
    ac = after.crop(box).resize((S, S))
    return ('<div class="face"><h3>Image %s, face %s <span class="%s">(%s)</span></h3><div class="pair">'
            '<figure><img src="data:image/jpeg;base64,%s" alt="Image %s face %s, original"><figcaption>%s</figcaption></figure>'
            '<figure><img src="data:image/jpeg;base64,%s" alt="Image %s face %s, %s"><figcaption>%s</figcaption></figure></div></div>'
            % (no, f[0], cls, H(why), b64(turned(oc, turns)), no, f[0], 'Original - white outline = the area blurred' if blurred else 'Original - white outline = the area that would be blurred (not blurred)',
               b64(turned(ac, turns)), no, f[0], H(after_label.lower()), H(after_label)))
CSS = ('body{margin:0;font-family:Georgia,serif;background:#F5EEE3;color:#2B2B2B}header{background:#1E4D7B;color:#fff;padding:20px 24px}'
       'header h1{margin:0 0 8px;font-weight:500;font-size:26px}header p{line-height:1.5;max-width:900px;margin:8px 0}'
       'section{padding:24px;border-bottom:3px solid #D9C9AB}h2{color:#0432FF;font-weight:500;margin:0 0 12px}'
       'img.whole{display:block;max-width:100%;height:auto;margin-bottom:6px}.note{font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;max-width:900px}'
       '.face{margin:22px 0}.face h3{margin:0 0 6px;font-size:20px;font-weight:600}.face h3 span{font-weight:400;font-size:16px}'
       '.pair{display:flex;gap:16px;flex-wrap:wrap}.pair figure{margin:0}.pair img{display:block;width:340px;max-width:44vw;height:auto;border:1px solid #bbb}'
       'figcaption{font-family:Helvetica,Arial,sans-serif;font-size:14px;padding-top:3px}'
       '.r{color:#c01010}.o{color:#b85c00}.g{color:#666}.n{color:#0a7a2a}.test{background:#8a1c1c;color:#fff;padding:12px 24px;font-family:Helvetica,Arial,sans-serif;font-size:18px}'
       '.hp{display:flex;gap:16px;flex-wrap:wrap}.hp figure{margin:0;width:340px;max-width:44vw}.hp img{display:block;width:100%;height:auto;border:1px solid #bbb}'
       '@media (max-width:640px){section{padding:16px}.pair img{width:100%;max-width:100%}.pair figure,.hp figure{width:100%;max-width:100%}}')
def sheet_page(title, head_html, sections, test=None):
    t = ('<div class="test">%s</div>' % H(test)) if test else ''
    # 25 Oct 2026 (round 1 sheets reached the user before any check): every sheet opens with this banner; only
    # 'faces.py release' takes it off, and only after a separate agent's passed check is recorded (sheet-check.json)
    t += '<div class="test" id="mm-unchecked">NOT CHECKED YET - please do not answer this sheet. A separate check comes first; you will be sent the checked sheet.</div>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><style>%s</style></head><body>%s<header><h1>%s</h1>%s</header>%s</body></html>'
            % (H(title), CSS, t, H(title), head_html, ''.join(sections)))
def page_no(out, n):
    po = jl(out, 'page_order.json', {}); return (' - page image %03d' % po[n]) if n in po else ''
def test_label(): return os.environ.get('FACES_TEST') or None   # a test run: the sheet says so at the top
def reply_line(examples):   # a test sheet asks for no answer (independent check, 23 Oct)
    return '<p><b>Test sheet: no answer is needed.</b></p>' if test_label() else '<p><b>Reply</b> by image number and face letter, e.g. %s.</p>' % examples

def hand_point_cards(out, D, n, f, k_, ORIG, turns):
    """28 Sept rule: a face whose points were placed by hand is shown in close-up - the points, the blur with the detector's
    points (not used) and with the hand-placed points (used). 23 Oct 2026: the current blur (blur_local) on the full-size
    original, turned as Word turns the photo."""
    v = D[n]; no = str(v['no']); det_lm = (v.get('landmarks') or [None] * 99)[L.index(f[0])] if L.index(f[0]) < len(v['faces']) else None
    COLS = [(255, 0, 0), (0, 0, 255), (255, 200, 0), (255, 0, 255), (0, 230, 230)]
    im, _, V, k = full_faces(out, n, [], ORIG); box = face_box(f, k, im.size); pad = int((box[2] - box[0]) * 0.5)
    big = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    crop = im.crop(big); S = 340; sc = S / (box[2] - box[0])
    def local(lm):   # the blur on a piece of the full-size original around the face (the same pixels as the whole photo there)
        fb = [[c * k - (big[0] if i % 2 == 0 else big[1]) for i, c in enumerate(f[1])]]
        lmb = _hp(lm, [[x * k - big[0], y * k - big[1]] for x, y in lm]) if lm else None
        r = blur_local(crop, [(fb[0], lmb)], None, V)
        return r.crop((box[0] - big[0], box[1] - big[1], box[2] - big[0], box[3] - big[1])).resize((S, S))
    pts = im.crop(box).resize((S, S)); d = ImageDraw.Draw(pts)
    for i, (px, py) in enumerate(f[2]):
        X, Y = (px * k - box[0]) * sc, (py * k - box[1]) * sc; d.ellipse((X - 6, Y - 6, X + 6, Y + 6), fill=COLS[i])
    out_ = ['<div class="face"><h3>Image %s, face %s: its eye, nose and mouth points, placed by hand <span>(the same face as above)</span></h3><div class="hp">' % (no, f[0])]
    out_.append('<figure><img src="data:image/jpeg;base64,%s" alt="Image %s face %s, the points"><figcaption><b>The points used:</b> red and blue eyes, yellow nose, pink and turquoise mouth. The blurred area is placed over them.</figcaption></figure>' % (b64(turned(pts, turns)), no, f[0]))
    if det_lm:
        out_.append('<figure><img src="data:image/jpeg;base64,%s" alt="Image %s face %s, blurred with the detector points"><figcaption>Blurred with the detector\'s points (not used)</figcaption></figure>' % (b64(turned(local(det_lm), turns)), no, f[0]))
    out_.append('<figure><img src="data:image/jpeg;base64,%s" alt="Image %s face %s, blurred with the hand-placed points"><figcaption><b>Blurred with the hand-placed points (used)</b></figcaption></figure>' % (b64(turned(local(f[2]), turns)), no, f[0]))
    out_.append('</div></div>')
    return ''.join(out_)

def photo_section(out, D, n, docx, ORIG, TURN, BY, KEEP, mode, ASK=None):
    """One photo on a sheet. mode 'r1': the original, faces to blur shown as they will look (blurred in memory);
    mode 'r2': the full-size blurred copy from photos-full."""
    v = D[n]; no = str(v['no']); fs = faces_of(out, D, n); rule = BY.get(no, {}); kept = kept_of(KEEP, no); tk = TURN.get(n, 0)
    blur_fs = [f for f in fs if f[0] not in rule and f[0] not in kept]
    orig = ORIG[n].convert('RGB'); wk = Image.open(os.path.join(out, 'work', n)); k = orig.width / wk.width
    if mode == 'r1':
        after, _ = blurred_full(out, n, blur_fs, ORIG); top = orig; after_label = 'How it will look'
    else:
        pf = os.path.join(out, 'photos-full', n)
        after = Image.open(pf).convert('RGB') if os.path.exists(pf) else orig; top = after; after_label = 'On the page'
    def colour(f):
        if f[0] in rule or f[0] in kept: return GREY
        if f[3]: return ORANGE if mode == 'r1' else GREEN
        return RED
    s = 1100 / max(top.size)
    boxes = [(f[0], [c * k for c in f[1]], colour(f), '', [[x * k, y * k] for x, y in f[2]] if f[2] else None) for f in fs]
    whole = card_img(top, boxes, s, tk, FONT_BIG)
    if mode == 'r1':
        key = 'Red = to blur. Orange = a face added by hand, to blur. Grey = not blurred.'
    else:
        key = 'Red = blurred. Green = added by hand and blurred. Grey = not blurred.'
    left = '; '.join('%s (%s)' % (l, r) for l, r in rule.items())
    note = key + (' Left by a standing rule: %s.' % left if left else '') + ((' <b>I cannot decide: %s.</b> Red: blurred unless you say otherwise.' % H(ASK[no])) if ASK and no in ASK else '')
    even = [f[0] for f in blur_fs if not f[2]]
    if even: note += ' No eye and mouth points (even oval blur): %s.' % ', '.join(even)
    rows = []
    for f in fs:
        if f[0] in rule: continue
        if f[0] in kept: why, cls = 'NOT blurred - your earlier answer', 'g'
        else: why, cls = ('to blur' if mode == 'r1' else 'blurred') + (' - added by hand' if f[3] else ''), ('o' if mode == 'r1' else 'n') if f[3] else 'r'
        rows.append(pair_html(no, f, why, orig, after, k, tk, after_label, cls, f[0] not in kept))
    PTS = jl(out, 'hand_points.json', {})
    for f in fs:
        if f[0] not in rule and PTS.get(no, {}).get(f[0]): rows.append(hand_point_cards(out, D, n, f, k, ORIG, tk))
    return ('<section><h2>Word image %s%s</h2><img class="whole" src="data:image/jpeg;base64,%s" alt="Word image %s, faces outlined">'
            '<p class="note">%s</p>%s</section>' % (no, page_no(out, n), b64(whole, 80), no, note, ''.join(rows))), len(blur_fs)

def main():
    cmd, docx, out = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True)
    DP = os.path.join(out, 'detections.json')
    if cmd in ('sheet', 'blurfull', 'after', 'release'):   # 26 Oct 2026: the v8 blur is rejected - the agreed method v22 replaces it
        sys.exit('Refused: "%s" is the rejected v8 blur. Use the agreed method (claude/BLUR-METHOD-26-oct.md version 22) with tools/blur/method.py, method_sheet.py and method_check.py - see START-HERE "Faces".' % cmd)
    if cmd == 'blur':   # 23 Oct 2026 (user 12:39: "Always blur copies of full size original photos only")
        sys.exit('Refused: the blur on 1600-pixel working copies is retired (23 Oct 2026). Use: faces.py blurfull <word.docx> <out> -> <out>/photos-full')
    ps = photos(docx)
    if cmd == 'detect':
        D = {}
        for i, (n, im) in enumerate(ps, 1):
            p = working_copy(out, n, im); fs = detect(bgr_of(p))
            D[n] = dict(no=i, size=list(Image.open(p).size), faces=[[round(float(x), 1) for x in f[:4]] + [round(float(f[4]), 3)] for f in fs],
                        landmarks=[f[5] for f in fs])
        json.dump(D, open(DP, 'w'), indent=1)
        print(len(ps), 'photos,', sum(1 for v in D.values() if v['faces']), 'with faces,', sum(len(v['faces']) for v in D.values()), 'faces ->', DP)
    elif cmd == 'pass2':
        D = json.load(open(DP)); P = {}; tiles = []
        for n, v in D.items():
            p = os.path.join(out, 'work', n); keep = []
            for b in detect(bgr_of(p), 0.45, 0.6, extra_scales=True):
                if all(ov(b, f) < 0.3 for f in v['faces']) and all(ov(b, k) < 0.3 for k in keep): keep.append([round(float(x), 1) for x in b[:5]])
            if keep:
                P[str(v['no'])] = keep; im = Image.open(p).convert('RGB')
                for j, b in enumerate(keep):
                    w, h = b[2] - b[0], b[3] - b[1]
                    c = im.crop((max(0, b[0] - w), max(0, b[1] - h), b[2] + w, b[3] + h)).resize((160, 160))
                    ImageDraw.Draw(c).text((4, 4), '%s-%d' % (v['no'], j + 1), fill=(255, 0, 0), font=FONT, stroke_width=2, stroke_fill=(255, 255, 255)); tiles.append(c)
        json.dump(P, open(os.path.join(out, 'pass2.json'), 'w'), indent=1)
        if tiles:
            cols = 8; sh = Image.new('RGB', (cols * 165, ((len(tiles) + cols - 1) // cols) * 165), 'white')
            for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * 165, (i // cols) * 165))
            sh.save(os.path.join(out, 'pass2-sheet.jpg'), quality=88)
        print('second pass:', sum(len(x) for x in P.values()), 'candidates in', len(P), 'photos -> check each by eye; real faces into extra_faces.json')
    elif cmd == 'sheet':   # round 1 (23 Oct 2026: the large pairs of the 13:2x 2.1.2 sheet, for round 1 too)
        D = json.load(open(DP)); BY = {k: v for k, v in jl(out, 'by_rule.json', {}).items() if not k.startswith('_')}
        KEEP = jl(out, 'keep_unblurred.json', {}); ASK = jl(out, 'ask.json', {}); TURN = word_turns(docx); ORIG = dict(ps)
        only = set(sys.argv[4:]); secs = []; left = []; nred = 0
        for n, v in D.items():
            no = str(v['no']); fs = faces_of(out, D, n)
            if only and no not in only: continue
            if not fs: left.append('%s (no faces)' % no); continue
            grey = lambda f: f[0] in BY.get(no, {}) or f[0] in kept_of(KEEP, no)
            why = lambda f: BY[no][f[0]] if f[0] in BY.get(no, {}) else 'your earlier answer: not blurred'
            if not [f for f in fs if not grey(f)] and not only:
                left.append('%s (%s)' % (no, '; '.join(sorted(set(why(f) for f in fs))))); continue
            sec, nb = photo_section(out, D, n, docx, ORIG, TURN, BY, KEEP, 'r1', ASK); secs.append(sec); nred += nb
        top = ''.join('<p><b>I cannot decide - image %s:</b> %s. Red: blurred unless you say otherwise.</p>' % (k, H(ASK[k])) for k in sorted(ASK, key=int))
        notes = jl(out, 'notes.json', {}).get('round1', []) + jl(out, 'checks.json', {}).get('sheet_notes', [])
        head = (top + '<p>Each image whole, every face drawn as the outline of the area that will be blurred. Under it, each face large: the original on the left, how it will look on the right (blurred on a copy of the full-size original; nothing is saved until you answer).</p>'
                '<p>%d images on this sheet, %d faces to blur. Left off this sheet: %s.</p>' % (len(secs), nred, ', '.join(left) or 'none')
                + ''.join('<p>%s</p>' % x for x in notes)
                + '<p>Check that every child\'s eyes, nose and mouth are blurred, and that nothing else is.</p>' + reply_line('"No blurring: 3b 7a", "Blur: 9c", or "No changes"'))
        p = os.path.join(out, 'round1.html'); open(p, 'w').write(sheet_page('Faces, first round - ' + os.path.splitext(os.path.basename(docx))[0], head, secs, test_label()))
        print(len(secs), 'photos on the sheet,', nred, 'faces to blur ->', p)
    elif cmd == 'blurfull':   # 23 Oct 2026 (user 12:39: "Always blur copies of full size original photos only"): the chosen faces
        # drawn on a copy of the FULL-SIZE Word original -> <out>/photos-full/<word name>. Boxes, points and every v7 radius
        # scaled from the working copy by (original width / working-copy width), so the look is the same.
        BYF = jl(out, 'by_rule.json', {})
        if not BYF.get('_checked'): sys.exit('Refused: by_rule.json lacks "_checked".')
        if not os.path.exists(os.path.join(out, 'review.json')): sys.exit("Refused: no review.json (the user's answer).")
        rv = jl(out, 'review.json', {}); r1 = os.path.join(out, 'round1.html')   # 23 Oct 2026: the check the retired 'blur' made - the answer must be to the round 1 sheet as it now stands
        if os.path.exists(r1) and (rv.get('sheet') != 'round1.html' or os.path.getmtime(os.path.join(out, 'review.json')) < os.path.getmtime(r1)):
            sys.exit('Refused: review.json does not hold the answer to the current round 1 sheet ("sheet": "round1.html", recorded after the sheet was made).')
        D = json.load(open(DP)); BY = {k: v for k, v in BYF.items() if not k.startswith('_')}; KEEP = jl(out, 'keep_unblurred.json', {})
        ORIG = dict(ps); pd = os.path.join(out, 'photos-full'); os.makedirs(pd, exist_ok=True); done = 0
        only = set(sys.argv[4:])   # 24 Oct 2026: optional image numbers - redo only those (the rest stay as they are)
        for n, v in D.items():
            no = str(v['no'])
            if only and no not in only: continue
            skip = set(BY.get(no, {})) | kept_of(KEEP, no)
            fs = [f for f in faces_of(out, D, n) if f[0] not in skip]
            for f in fs:
                if not f[2]: print('  #%s%s no points - oval on the lower-middle of the box' % (no, f[0]))
            dst = os.path.join(pd, n)
            if fs:
                im, ffs, V, k = full_faces(out, n, fs, ORIG)
                src = os.path.join(out, 'orig-' + n + '.png'); im.save(src, 'PNG')   # lossless copy of the original's pixels (no camera tag, as the working copies)
                blur_local(src, ffs, dst, V); done += 1; os.remove(src)   # 23 Oct 12:40: centred on eyes, nose and mouth
            elif os.path.exists(dst): os.remove(dst)
        print('photos blurred on full-size copies (v8 precise: eyes, nose, lips only):', done, '->', pd)
    elif cmd == 'after':   # round 2 (23 Oct 2026: the large pairs, as the 2.1.2 sheet of 13:2x)
        D = json.load(open(DP)); BY = {k: v for k, v in jl(out, 'by_rule.json', {}).items() if not k.startswith('_')}
        KEEP = jl(out, 'keep_unblurred.json', {}); TURN = word_turns(docx); ORIG = dict(ps)
        only = set(sys.argv[4:]); every = 'all' in only; secs = []; nb_ = 0; left = []
        for n, v in D.items():
            no = str(v['no']); fs_ = faces_of(out, D, n)
            if not every and no not in only: continue
            if every and not [f for f in fs_ if f[0] not in BY.get(no, {})]:
                left.append('%s (%s)' % (no, '; '.join('%s: %s' % (l, r) for l, r in BY.get(no, {}).items()) if fs_ else 'no faces')); continue
            sec, nb = photo_section(out, D, n, docx, ORIG, TURN, BY, KEEP, 'r2'); secs.append(sec); nb_ += nb
        notes = jl(out, 'notes.json', {}).get('round2', [])
        head = (''.join('<p>%s</p>' % x for x in notes)
                + '<p>%s, as they will be on the page: blurred on copies of the full-size originals, each blur centred on the eyes, nose and mouth. Under each image, every child\'s face: the original on the left, the page on the right. %d blurred faces.</p>'
                % ('Every image with a face that is blurred or kept by your answer' if every else 'Only the images your answer changed', nb_)
                + ('<p>Left off this sheet: %s.</p>' % H(', '.join(left)) if left else '')
                + '<p>Check that every child\'s eyes, nose and mouth are blurred, and that nothing else is.</p>' + reply_line('"No blurring: 3b", "Blur: 9c", or "No changes"'))
        p = os.path.join(out, 'round2.html'); open(p, 'w').write(sheet_page('Faces, second round - ' + os.path.splitext(os.path.basename(docx))[0], head, secs, test_label()))
        print(len(secs), 'photos,', nb_, 'blurred faces ->', p)
    elif cmd == 'pageorder':   # the page photo number of each Word photo, from a built page (data-name, in page order)
        names = re.findall(r'data-name="([^"]+)"', open(sys.argv[4], encoding='utf-8').read()); po = {}
        for nm in names:
            if nm not in po: po[nm] = len(po) + 1
        json.dump(po, open(os.path.join(out, 'page_order.json'), 'w'), indent=1); print(len(po), 'photos on the page ->', os.path.join(out, 'page_order.json'))
    elif cmd == 'release':   # 25 Oct 2026: faces.py release <word.docx> <out> round1|round2 - the banner comes off only after a passed check
        nm = (sys.argv[4] if len(sys.argv) > 4 else 'round1') + '.html'; sp = os.path.join(out, nm); sc = os.path.join(out, 'sheet-check.json')
        if not os.path.exists(sc): sys.exit('Refused: no sheet-check.json (a separate agent checks the sheet first).')
        j = jl(out, 'sheet-check.json', {})
        if j.get('sheet') != nm or j.get('pass') is not True or os.path.getmtime(sc) < os.path.getmtime(sp):
            sys.exit('Refused: sheet-check.json does not record a passed check of %s made after the sheet.' % nm)
        st = os.stat(sp); h = open(sp).read()
        h2 = re.sub(r'<div class="test" id="mm-unchecked">.*?</div>', '', h, count=1)
        open(sp, 'w').write(h2); os.utime(sp, (st.st_atime, st.st_mtime))   # the sheet keeps its time, so the check still counts as after it
        print('released %s (%s)' % (sp, 'banner removed' if h2 != h else 'no banner found'))
    elif cmd == 'save':   # every choice for the page in one file, for claude/workspace/faces-data/
        rec = {'word_file': os.path.basename(docx), 'word_bytes': os.path.getsize(docx)}
        for f_ in ('detections.json', 'extra_faces.json', 'adjust_faces.json', 'hand_points.json', 'by_rule.json', 'keep_unblurred.json',
                   'ask.json', 'review.json', 'review2.json', 'checks.json', 'notes.json', 'page_order.json', 'pass2.json'):
            if os.path.exists(os.path.join(out, f_)): rec[f_] = json.load(open(os.path.join(out, f_)))
        json.dump(rec, open(sys.argv[4], 'w'), indent=1, ensure_ascii=False); print('saved', sorted(k for k in rec if k.endswith('.json')), '->', sys.argv[4])
    elif cmd == 'restore':   # the reverse of save: working copies from the Word file, the choices written back
        rec = json.load(open(sys.argv[4]))
        if rec.get('word_bytes') and rec['word_bytes'] != os.path.getsize(docx): print('WARNING: the Word file is not the size recorded (%s, now %s) - check the photos are the same' % (rec['word_bytes'], os.path.getsize(docx)))
        for n, im in ps: working_copy(out, n, im)
        for k_, v_ in rec.items():
            if k_.endswith('.json'): json.dump(v_, open(os.path.join(out, k_), 'w'), indent=1, ensure_ascii=False)
        print('restored', sorted(k for k in rec if k.endswith('.json')), '->', out)
    else:
        sys.exit('unknown command: ' + cmd)

if __name__ == '__main__':
    main()
