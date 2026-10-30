"""The blur method of claude/BLUR-METHOD-26-oct.md, version 22 - AGREED by the owner 26 Oct 2026 13:47 (its text was written for version 20; version 21's hand cuts and added areas are applied from the set files, and version 22 added only the working rules of section K). This tool does items 4-19 for one set:
  python3 method.py detect <set.json>     RetinaFace upright and both ways sideways on the working copies (0.9), plus the 0.5
                                           candidates -> <out>/rf.json and <out>/candidates.jpg (for Claude's eye, item 5)
  python3 method.py blur <set.json>       faces merged, the area and blur on the full-size originals -> <out>/images, crops, faces.json
  python3 method.py sheet <set.json> <title> <dst.html>
<set.json>: {"src": faces dir (detections.json, extra_faces.json, hand_points.json, adjust_faces.json, by_rule.json, keep_unblurred.json),
             "work": working copies dir, "media": full-size originals dir, "out": out dir, "docx": Word file (turns), "prev": previous
             faces.json whose letters are kept, "answers": the owner's answers mapped to actions (item 15), "candidates_ok": [tags kept]}
No quiet fallback (item 1): a missing library, model or file, or a detector failing on an image, stops the run."""
import sys, os, json, time, re, string, math
import numpy as np, cv2
from PIL import Image
import mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
from retinaface import RetinaFace
assert mp.__version__ == '0.10.32', 'STOP: mediapipe %s installed; 0.10.32 needed' % mp.__version__
# 26 Oct 2026 (the owner 14:00: "fix these now"): the two models are no longer looked for at two fixed paths - the tool
# ran only from /home/claude/mm. Each is looked for in this order, and the first file found is used:
#   1. the environment variable MM_LMK_MODEL / MM_SEG_MODEL (a full path), 2. <this file's folder>/models/<name>,
#   3. <this file's folder>/../models/<name>, 4. /home/claude/mm/blur2/models/<name>, 5. /home/claude/mm/models/<name>.
# Whichever is found, its SHA-256 must equal the one the method names (item 1), so a wrong file anywhere still stops the run.
import hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_SHA = {'face_landmarker.task': '64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff',
             'selfie_multiclass_256x256.tflite': 'c6748b1253a99067ef71f7e26ca71096cd449baefa8f101900ea23016507e0e0'}
def _model(name, env):
    tried = []
    for c in ([os.environ[env]] if os.environ.get(env) else []) + [
            os.path.join(HERE, 'models', name), os.path.join(os.path.dirname(HERE), 'models', name),
            '/home/claude/mm/blur2/models/' + name, '/home/claude/mm/models/' + name]:
        if c in tried: continue
        tried.append(c)
        if os.path.exists(c):
            got = hashlib.sha256(open(c, 'rb').read()).hexdigest()
            if got != MODEL_SHA[name]:
                raise SystemExit('STOP: %s differs from the model the method names (item 1).\n  file:     %s\n  its SHA-256: %s\n  needed:      %s' % (name, c, got, MODEL_SHA[name]))
            return c
    raise SystemExit('STOP: model missing: %s. Looked in:\n  %s\nSet %s to its full path, or put it in one of those folders (README "Faces", method item 1).' % (name, '\n  '.join(tried), env))
LMK_MODEL = _model('face_landmarker.task', 'MM_LMK_MODEL')
SEG_MODEL = _model('selfie_multiclass_256x256.tflite', 'MM_SEG_MODEL')
import retinaface
assert getattr(retinaface, '__version__', '0.0.19') in ('0.0.19',), 'STOP: retina-face version'
OVAL36 = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
GROW, FEATHER, SIGMA = 0.03, 0.08, 0.12          # items 11 and 13 (outward distance, Gaussian sigma, blur sigma), all x the face width
OVAL_HX, OVAL_HY = 0.42, 0.56                     # item 10 half-axes (v18: 0.42 w - at 0.5 w the oval took the ear on profiles, whose points sit at the front of the box)
MERGE = 0.3                                       # item 5: overlap > 0.3 of the smaller box = one face
L = list(string.ascii_lowercase) + ['a' + c for c in string.ascii_lowercase] + ['b' + c for c in string.ascii_lowercase]

def jl(p, d=None):
    return json.load(open(p)) if os.path.exists(p) else d
def overlap_small(a, b):   # intersection as a share of the smaller box (faces.py's rule)
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return ix * iy / max(1.0, min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])))
def unrot_pt(x, y, k, ww, hh):   # a point in np.rot90(img, k) back to the upright image (ww, hh = rotated image size)
    if k == 0: return x, y
    if k == 1: return hh - 1 - y, x      # np.rot90 once (counter-clockwise): r[i, j] = img[j, W-1-i]
    if k == 3: return y, ww - 1 - x      # three times (clockwise): r[i, j] = img[H-1-j, i]
    raise ValueError(k)
def rf_detect_all(path):
    """RetinaFace at 0.5 on the upright image and both ways sideways; each box back in upright coordinates with score and 5 points."""
    img = cv2.imread(path); H, W = img.shape[:2]; found = []
    for k in (0, 1, 3):
        r = np.ascontiguousarray(np.rot90(img, k)); hh, ww = r.shape[:2]
        rf = RetinaFace.detect_faces(r, threshold=0.5)          # raises on failure: no quiet fallback
        if not isinstance(rf, dict): continue
        for v in rf.values():
            x0, y0, x1, y1 = v['facial_area']; pts = [v['landmarks'][n] for n in ('right_eye', 'left_eye', 'nose', 'mouth_right', 'mouth_left')]
            cs = [unrot_pt(px, py, k, ww, hh) for px, py in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
            xs = [c[0] for c in cs]; ys = [c[1] for c in cs]
            lm = [list(map(float, unrot_pt(px, py, k, ww, hh))) for px, py in pts]
            if k:  # after turning back, the eye order may swap; order the points left eye, right eye by x
                e = sorted(lm[:2], key=lambda p: p[0]); mth = sorted(lm[3:], key=lambda p: p[0]); lm = [e[0], e[1], lm[2], mth[0], mth[1]]
            else:
                e = sorted(lm[:2], key=lambda p: p[0]); mth = sorted(lm[3:], key=lambda p: p[0]); lm = [e[0], e[1], lm[2], mth[0], mth[1]]
            found.append({'box': [float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys))], 'score': float(v['score']), 'lm': lm, 'turn': k})
    found.sort(key=lambda f: (f['turn'] != 0, -f['score'])); keep = []   # upright detections first: their points are the better ones
    for f in found:
        if all(overlap_small(f['box'], g['box']) <= MERGE for g in keep): keep.append(f)
    return keep, (W, H)

def cmd_detect(S):
    out = S['out']; os.makedirs(out, exist_ok=True); det = jl(os.path.join(S['src'], 'detections.json')); assert det, 'STOP: detections.json missing'
    rf = jl(os.path.join(out, 'rf.json'), {}); t0 = time.time(); n = 0
    for name, rec in sorted(det.items(), key=lambda kv: int(kv[1].get('no', 0))):
        if name in rf: continue
        p = os.path.join(S['work'], name)
        if not os.path.exists(p): raise SystemExit('STOP: working copy missing: ' + p)
        faces, size = rf_detect_all(p); rf[name] = {'no': rec.get('no'), 'faces': faces, 'size': size}; n += 1
        json.dump(rf, open(os.path.join(out, 'rf.json'), 'w'))
        print('%3d %-14s rf %2d (>=0.9: %d)  %.0fs' % (n, name, len(faces), sum(1 for f in faces if f['score'] >= 0.9), time.time() - t0), flush=True)
    print('detect done', n, 'images')

def load_faces(S, name, rec, rf_rec, prev):
    """Item 5: YuNet (inherited detections.json, with hand points and adjusted boxes), hand-added faces, RetinaFace >= 0.9 merged, then the
    0.5 candidates Claude has accepted (S['candidates_ok']). Letters: detections, extras, RetinaFace-only in the previous run's order
    (kept from prev faces.json by box match), then new faces."""
    no = str(rec.get('no')); HP = jl(os.path.join(S['src'], 'hand_points.json'), {}).get(no, {}); ADJ = jl(os.path.join(S['src'], 'adjust_faces.json'), {}).get(no, {})
    extra = jl(os.path.join(S['src'], 'extra_faces.json'), {}).get(no, [])
    faces = []
    for k, f in enumerate(rec['faces']):
        lm = rec.get('landmarks', [None] * len(rec['faces']))[k]
        faces.append({'box': ADJ.get(L[k], f[:4]), 'score': f[4] if len(f) > 4 else None, 'lm': HP.get(L[k], lm), 'src': 'yunet' + ('+hand points' if L[k] in HP else ''), 'letter': L[k]})
    for j, e in enumerate(extra):
        le = L[len(rec['faces']) + j]; faces.append({'box': ADJ.get(le, e['box']), 'score': None, 'lm': HP.get(le, e.get('lm')), 'src': 'hand', 'letter': le})
    for f in faces:
        if f['lm'] is not None: f['lm'] = [[float(a), float(b)] for a, b in f['lm']]
    rfaces = [f for f in rf_rec['faces'] if f['score'] >= 0.9] if rf_rec else []
    for f in rfaces:
        hit = [g for g in faces if overlap_small(f['box'], g['box']) > MERGE]
        if hit:
            g = hit[0]; g['src'] += '+retinaface'; g['rf_lm'] = f['lm']
            if g['lm'] is None: g['lm'] = f['lm']; g['src'] += ' (RetinaFace points)'
        else: faces.append({'box': f['box'], 'score': f['score'], 'lm': f['lm'], 'src': 'retinaface', 'letter': None, 'rf': f})
    # the 0.5 candidates Claude accepted by eye (item 5, second pass)
    for f in (rf_rec['faces'] if rf_rec else []):
        if f['score'] >= 0.9: continue
        tag = '%s@%d,%d' % (no, int(f['box'][0]), int(f['box'][1]))
        if tag in S.get('candidates_ok', []) and all(overlap_small(f['box'], g['box']) <= MERGE for g in faces):
            faces.append({'box': f['box'], 'score': f['score'], 'lm': f['lm'], 'src': 'retinaface second pass (%.2f)' % f['score'], 'letter': None, 'rf': f})
    # letters for the unlettered: the previous run's letter where the box matches, else the next free letter
    used = {f['letter'] for f in faces if f['letter']}; pv = (prev or {}).get(name, {}).get('faces', [])
    for f in faces:
        if f['letter']: continue
        for p in pv:
            pl = p['tag'].split('-', 1)[1]
            if pl not in used and overlap_small(f['box'], p['box']) > 0.5: f['letter'] = pl; used.add(pl); break
    nxt = max([L.index(l) for l in used] + [-1]) + 1
    for f in faces:
        if not f['letter']: f['letter'] = L[nxt]; used.add(L[nxt]); nxt += 1
    faces.sort(key=lambda f: L.index(f['letter']))
    return faces

def area_for(full, fbox, lm, w, h, lmk, seg, edit, log):
    """Items 9-11 on the full-size original. Returns the feathered weight (float32, crop size), crop bounds, notes."""
    H, W = full.shape[:2]; x0, y0, x1, y1 = fbox; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; s = max(w, h) * 1.6
    X0, Y0 = int(max(0, cx - s)), int(max(0, cy - s)); X1, Y1 = int(min(W, cx + s)), int(min(H, cy + s)); crop = full[Y0:Y1, X0:X1]
    up = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_CUBIC); rgb = cv2.cvtColor(up, cv2.COLOR_BGR2RGB)
    sx, sy = (X1 - X0) / 512, (Y1 - Y0) / 512
    gx, gy = 0.25 * w, 0.25 * h; bx0, by0, bx1, by1 = x0 - gx, y0 - gy, x1 + gx, y1 + gy      # the box grown a quarter (width / height)
    # (a) the mesh outline
    mesh = None; mesh_note = 'no mesh'
    rr = lmk.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    if rr.face_landmarks:
        pts = rr.face_landmarks[0]; P = np.array([[pts[k].x * 512 * sx + X0, pts[k].y * 512 * sy + Y0] for k in OVAL36], np.float32)
        c = P.mean(0); ok_c = bx0 <= c[0] <= bx1 and by0 <= c[1] <= by1
        if lm is not None:
            le, ri, no_, ml, mr = lm; e_lm = max(math.hypot(ri[0] - le[0], ri[1] - le[1]), 0.28 * w)
            eye_mid_m = ((pts[33].x + pts[263].x) * 256 * sx + X0, (pts[33].y + pts[263].y) * 256 * sy + Y0)
            mouth_m = ((pts[61].x + pts[291].x) * 256 * sx + X0, (pts[61].y + pts[291].y) * 256 * sy + Y0)
            de = math.hypot(eye_mid_m[0] - (le[0] + ri[0]) / 2, eye_mid_m[1] - (le[1] + ri[1]) / 2); dm = math.hypot(mouth_m[0] - (ml[0] + mr[0]) / 2, mouth_m[1] - (ml[1] + mr[1]) / 2)
            ok_p = de < 0.6 * e_lm and dm < 0.6 * e_lm
        else: ok_p = True
        if ok_c and ok_p: mesh = P; mesh_note = 'mesh'
        else: mesh_note = 'mesh found but failed the position tests (%s)' % ('centre' if not ok_c else 'eyes/mouth')
    if mesh is not None and edit.get('refit'):   # item 15 "not covering enough" with a mesh: re-fit on a crop 2.2 x the box each side, the larger outline kept
        s2 = max(w, h) * 2.2; A0, B0 = int(max(0, cx - s2)), int(max(0, cy - s2)); A1, B1 = int(min(W, cx + s2)), int(min(H, cy + s2))
        up2 = cv2.resize(full[B0:B1, A0:A1], (512, 512), interpolation=cv2.INTER_CUBIC); r2 = lmk.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(up2, cv2.COLOR_BGR2RGB)))
        if r2.face_landmarks:
            p2 = r2.face_landmarks[0]; P2 = np.array([[p2[k].x * (A1 - A0) + A0, p2[k].y * (B1 - B0) + B0] for k in OVAL36], np.float32)
            c2 = P2.mean(0)
            if bx0 <= c2[0] <= bx1 and by0 <= c2[1] <= by1 and cv2.contourArea(P2) > cv2.contourArea(mesh): mesh = P2; mesh_note = 'mesh (re-fitted, larger)'
            else: mesh_note = 'mesh (re-fit no larger - show to the owner)'
        else: mesh_note = 'mesh (re-fit found nothing - show to the owner)'
    # (b) the skin labels, inside the quarter-grown box
    cat = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)).category_mask.numpy_view()[..., 0]
    skin = cv2.resize((cat == 3).astype(np.uint8) * 255, (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_NEAREST)
    # v14 (item 9b): the labels are kept to the box grown a tenth of its width sideways, a quarter of its height up and a tenth down (not a quarter all
    # round - that let ears, necks and a neighbour's ear in), and to the one connected patch that holds the nose point (or the largest patch in the box)
    lx0, ly0, lx1, ly1 = x0 - 0.1 * w, y0 - 0.25 * h, x1 + 0.1 * w, y1 + 0.1 * h
    boxm = np.zeros_like(skin); boxm[max(0, int(ly0 - Y0)):max(0, int(ly1 - Y0)), max(0, int(lx0 - X0)):max(0, int(lx1 - X0))] = 255; skin = cv2.bitwise_and(skin, boxm)
    ncomp, lab, stats, _ = cv2.connectedComponentsWithStats((skin > 127).astype(np.uint8), 8)
    if ncomp > 1:
        pick = 0
        if lm is not None:
            nx, ny = int(lm[2][0] - X0), int(lm[2][1] - Y0)
            if 0 <= ny < lab.shape[0] and 0 <= nx < lab.shape[1] and lab[ny, nx] > 0: pick = lab[ny, nx]
        if pick == 0: pick = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        skin = ((lab == pick).astype(np.uint8) * 255)
    area = np.zeros_like(skin)
    if mesh is not None:   # where the mesh is found, the labels only fill gaps within 0.06 w of its outline, never beyond -
        cv2.fillPoly(area, [np.round(mesh - [X0, Y0]).astype(np.int32)], 255); gm = max(1, int(round(0.06 * w)))
        near = cv2.dilate(area, np.ones((2 * gm + 1, 2 * gm + 1), np.uint8)); band = cv2.bitwise_and(skin, near)
        # - unless the nose point or the mouth centre lies outside the mesh outline (a poor fit on a tilted face): then the whole labels patch is used (v15)
        if lm is not None:
            le, ri, no_, ml, mr = lm; mc = ((ml[0] + mr[0]) / 2, (ml[1] + mr[1]) / 2); poly = np.round(mesh - [X0, Y0]).astype(np.int32)
            inside = lambda p: cv2.pointPolygonTest(poly, (float(p[0] - X0), float(p[1] - Y0)), False) >= 0
            if not (inside(no_) and inside(mc)):   # v16: not the whole patch (that took ears on tilted heads) - the labels within 0.25 w of the nose and of the mouth centre
                nm = np.zeros_like(skin); rr_ = max(2, int(round(0.25 * w)))
                cv2.circle(nm, (int(no_[0] - X0), int(no_[1] - Y0)), rr_, 255, -1); cv2.circle(nm, (int(mc[0] - X0), int(mc[1] - Y0)), rr_, 255, -1)
                band = cv2.bitwise_or(band, cv2.bitwise_and(skin, nm)); notes_extra = 'nose or mouth outside the mesh outline: the labels within 0.25 w of them added'
            else: notes_extra = None
        else: notes_extra = None
        area = cv2.bitwise_or(area, band)
    else:   # v17: no mesh - the labels only within 0.3 w of the five points (the whole patch took ears on profiles)
        if lm is not None:
            nearp = np.zeros_like(skin); rp = max(2, int(round(0.3 * w)))
            for p in lm: cv2.circle(nearp, (int(p[0] - X0), int(p[1] - Y0)), rp, 255, -1)
            area = cv2.bitwise_and(skin, nearp); notes_extra = 'labels within 0.3 w of the five points'
        else: area = skin.copy(); notes_extra = None
    if lm is not None:   # (c) v16: a disc of 0.1 w round each of the five points that lies on face skin (a label) or inside the mesh - a detector's
        rd = max(2, int(round(0.1 * w))); on_mesh = np.zeros_like(skin)   # nose point in the air beyond a profile's nose tip gets no disc
        if mesh is not None: cv2.fillPoly(on_mesh, [np.round(mesh - [X0, Y0]).astype(np.int32)], 255)
        for p in lm:
            px, py = int(p[0] - X0), int(p[1] - Y0)
            if 0 <= py < skin.shape[0] and 0 <= px < skin.shape[1] and (skin[py, px] > 0 or on_mesh[py, px] > 0): cv2.circle(area, (px, py), rd, 255, -1)
    cover = float((area > 127).sum()) / max(1.0, w * h); notes = [mesh_note, 'cover %.2f' % cover] + ([notes_extra] if notes_extra else [])
    if mesh is None and 'failed' in mesh_note and (edit.get('refit') or edit.get('add_oval')): edit = dict(edit, add_oval=False, show='mesh found but failed the position tests - shown to you, nothing changed')
    if edit.get('oval_only'):   # hand fix after a check: the labels found belong to a neighbour or miss the face - the item 10 oval alone, inside the box
        area = np.zeros_like(area); notes.append('labels not used (hand fix): the oval alone')
    oval = np.zeros_like(area); use_oval = cover < 0.5 or (edit.get('add_oval') and mesh is None) or edit.get('oval_only')   # item 15: the oval is added only where there is no mesh
    if use_oval:   # item 10: centred midway between the eye midpoint and the mouth centre of the five points; not grown
        if lm is None: raise SystemExit('STOP: face without points needs an oval - place hand points first')
        le, ri, no_, ml, mr = lm; ocx = ((le[0] + ri[0]) / 2 + (ml[0] + mr[0]) / 2) / 2; ocy = ((le[1] + ri[1]) / 2 + (ml[1] + mr[1]) / 2) / 2
        sc = edit.get('oval_scale', 1.0)
        cv2.ellipse(oval, (int(ocx - X0), int(ocy - Y0)), (int(OVAL_HX * w * sc), int(OVAL_HY * h * sc)), 0, 0, 360, 255, -1); notes.append('oval' + (' x%.2f' % sc if sc != 1 else ''))
        ob = np.zeros_like(oval); ob[max(0, int(y0 - 0.1 * h - Y0)):max(0, int(y1 + 0.1 * h - Y0)), max(0, int(x0 - X0)):max(0, int(x1 - X0))] = 255
        oval = cv2.bitwise_and(oval, ob)   # v19: the oval kept inside the box sideways and 0.1 of the height up and down
        # v20: the oval is kept within the outline round the labels, the discs and the five points (their convex hull), grown 0.06 w (0.12 w where
        # the labels cover under a tenth of the box). v19 kept it within 0.1 w of the labels alone, which cut the face into patches where the labels
        # are sparse (17-a, 36-c, 31-n, 78-j, 7-h, 20-w); the hull spans the eyes, nose and mouth, and on a profile ends 0.06 w past the nose tip.
        if not edit.get('oval_only'):
          pts = [(int(round(p[0] - X0)), int(round(p[1] - Y0))) for p in lm]
          ys, xs = np.nonzero(area); allp = np.array(pts + list(zip(xs[::7].tolist(), ys[::7].tolist())), np.int32)
          hull = np.zeros_like(area); cv2.fillConvexPoly(hull, cv2.convexHull(allp), 255)
          gl = max(2, int(round((0.06 if cover >= 0.1 else 0.12) * w))); hull = cv2.dilate(hull, np.ones((2 * gl + 1, 2 * gl + 1), np.uint8))
          oval = cv2.bitwise_and(oval, hull); notes.append('oval kept within %.2f w of the hull of the labels and the five points' % (0.06 if cover >= 0.1 else 0.12))
    if edit.get('mesh_only') and mesh is not None:   # item 15 "hair, ear or neck": cut back to the mesh outline, no oval
        area = np.zeros_like(area); cv2.fillPoly(area, [np.round(mesh - [X0, Y0]).astype(np.int32)], 255); oval[:] = 0; notes.append('cut back to the mesh outline')
    elif edit.get('mesh_only'):   # item 15: no mesh - the labels cut back to the box (ungrown); the oval, if any, stays
        bm = np.zeros_like(area); bm[max(0, int(y0 - Y0)):max(0, int(y1 - Y0)), max(0, int(x0 - X0)):max(0, int(x1 - X0))] = 255; area = cv2.bitwise_and(area, bm); notes.append('labels cut back to the box (no mesh)')
    for ab in edit.get('add', []):   # hand fix after a check: a rectangle of the face the area missed (working-copy coordinates), added to the area
        k_ = edit.get('_scale', 1.0); ax0, ay0, ax1, ay1 = [int(round(v * k_)) for v in ab]
        area[max(0, ay0 - Y0):max(0, ay1 - Y0), max(0, ax0 - X0):max(0, ax1 - X0)] = 255; notes.append('hand area added')
    for cb in edit.get('cut', []):   # item 15: hand-drawn cut rectangles (working-copy coordinates, scaled here by 'scale'), removed from the area and the oval
        k_ = edit.get('_scale', 1.0); cx0, cy0, cx1, cy1 = [int(round(v * k_)) for v in cb]
        area[max(0, cy0 - Y0):max(0, cy1 - Y0), max(0, cx0 - X0):max(0, cx1 - X0)] = 0; oval[max(0, cy0 - Y0):max(0, cy1 - Y0), max(0, cx0 - X0):max(0, cx1 - X0)] = 0; notes.append('hand cut applied')
    g = max(1, int(round(edit.get('grow', GROW) * w))); grown = cv2.dilate(area, np.ones((2 * g + 1, 2 * g + 1), np.uint8))   # outward distance GROW x w (a per-face 'grow' edit allowed, stated on the sheet)
    m = cv2.bitwise_or(grown, oval)
    fe = max(1.0, edit.get('feather', FEATHER) * w); mf = cv2.GaussianBlur(m, (0, 0), fe).astype(np.float32) / 255
    if edit.get('show'): notes.append(edit['show'])
    return mf, (X0, Y0, X1, Y1), notes, area, oval, mesh

def word_turns(docx):   # how Word turns each image on the page (a:xfrm rot) -> quarter turns clockwise (from tools/faces.py)
    import zipfile
    z = zipfile.ZipFile(docx); doc = z.read('word/document.xml').decode('utf8'); rels = z.read('word/_rels/document.xml.rels').decode('utf8')
    R = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels)) | {k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)}
    out = {}
    for d in re.findall(r'<w:drawing>.*?</w:drawing>', doc, re.S):
        m = re.search(r'r:embed="(rId\d+)"', d); r = re.search(r'<a:xfrm[^>]*\brot="(-?\d+)"', d)
        if m and r: out[os.path.basename(R.get(m.group(1), ''))] = round(int(r.group(1)) / 5400000) % 4
    return out

def cmd_blur(S):
    out = S['out']; [os.makedirs(os.path.join(out, d), exist_ok=True) for d in ('images', 'crops', 'whole', 'whole-sheet', 'masks')]
    S['_turns'] = word_turns(S['docx']) if S.get('docx') and os.path.exists(S['docx']) else {}
    det = jl(os.path.join(S['src'], 'detections.json')); rfj = jl(os.path.join(out, 'rf.json')); assert rfj, 'STOP: run detect first'
    BYALL = jl(os.path.join(S['src'], 'by_rule.json'), {})
    if not BYALL.get('_checked'): raise SystemExit('STOP: by_rule.json has no "_checked": true - every face must be looked at first (item 7)')
    BY = {k: v for k, v in BYALL.items() if not k.startswith('_')}; KEEP = jl(os.path.join(S['src'], 'keep_unblurred.json'), {})
    ANS = S.get('answers', {}); prev = jl(S['prev']) if S.get('prev') else {}
    be = os.path.join(S['src'], 'blur_edits.json')
    if os.path.exists(be) and not os.path.exists(be + '.25oct-trial'): os.rename(be, be + '.25oct-trial')   # the trial's per-face parameters are discarded (item 15)
    json.dump({'method': 'BLUR-METHOD-26-oct.md v12', 'answers': ANS, 'source': S.get('answers_source', '')}, open(be, 'w'), indent=1)
    lmk = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpp.BaseOptions(model_asset_path=LMK_MODEL), num_faces=1, min_face_detection_confidence=0.2))
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=SEG_MODEL), output_category_mask=True))
    res = {}; t0 = time.time(); n = 0; refused = []
    for d in ('crops', 'masks'):
        for p in os.listdir(os.path.join(out, d)): os.remove(os.path.join(out, d, p))   # no stale files from an earlier run
    for name, rec in sorted(det.items(), key=lambda kv: int(kv[1].get('no', 0))):
        no = str(rec.get('no')); wk = os.path.join(S['work'], name); md = os.path.join(S['media'], name)
        if not os.path.exists(md): raise SystemExit('STOP: full-size original missing: ' + md)
        faces = load_faces(S, name, rec, rfj.get(name), prev)
        if not faces: res[name] = {'no': no, 'faces': [], 'left_off': 'no face found'}; continue
        wkim = Image.open(wk); full = cv2.imread(md)
        if full is None: raise SystemExit('STOP: cannot read ' + md)
        K = full.shape[1] / wkim.width; Hf, Wf = full.shape[:2]
        kept = set(re.findall(r'b?a?[a-z]', KEEP.get(no, ''))) if isinstance(KEEP.get(no, ''), str) else set(KEEP.get(no, []))
        outim = full.copy(); rows = []; pend = []
        for f in faces:
            tag = '%s-%s' % (no, f['letter']); edit = dict(ANS.get(tag, {}), _scale=full.shape[1] / wkim.width)
            if f['letter'] in BY.get(no, {}):
                rows.append({'tag': tag, 'box': f['box'], 'width': round(f['box'][2] - f['box'][0], 1), 'src': f['src'], 'skipped': 'left unblurred by rule: ' + BY[no][f['letter']]}); continue
            if f['letter'] in kept or edit.get('keep'):
                rows.append({'tag': tag, 'box': f['box'], 'width': round(f['box'][2] - f['box'][0], 1), 'src': f['src'], 'skipped': 'left unblurred by your answer'}); continue
            fb = [v * K for v in f['box']]; lm = [[a * K, b * K] for a, b in f['lm']] if f['lm'] else None
            if lm is None: refused.append(tag); rows.append({'tag': tag, 'box': f['box'], 'width': round(f['box'][2] - f['box'][0], 1), 'src': f['src'], 'skipped': 'REFUSED: no eye, nose and mouth points - hand points needed'}); continue
            w = fb[2] - fb[0]; h = fb[3] - fb[1]
            mf, (X0, Y0, X1, Y1), notes, area, oval, mesh = area_for(full, fb, lm, w, h, lmk, seg, edit, None)
            if f.get('rf_lm') and f['lm'] and 'hand' not in f['src']:
                def ordered(p): e = sorted(p[:2], key=lambda q: q[0]); m_ = sorted(p[3:], key=lambda q: q[0]); return [e[0], e[1], p[2], m_[0], m_[1]]
                gap = max(math.hypot(a[0] * K - b[0] * K, a[1] * K - b[1] * K) for a, b in zip(ordered(f['lm']), ordered(f['rf_lm']))) / w
                if gap > 0.1: notes.append('RetinaFace points differ from YuNet by %.2f w' % gap)
            base = outim[Y0:Y1, X0:X1]; sg = max(1.0, edit.get('sigma', SIGMA) * w); bl = cv2.GaussianBlur(base, (0, 0), sg)
            outim[Y0:Y1, X0:X1] = (bl * mf[..., None] + base * (1 - mf[..., None])).astype(np.uint8)
            if tag in ANS:   # only entries in the set file; _scale is internal. Fixes made after a check are not the owner's answers
                nt = ANS[tag].get('note', str(ANS[tag])); parts = [x.strip() for x in nt.split(' | ')]
                own = [x for x in parts if not x.startswith('check')]; chk = [x for x in parts if x.startswith('check')]
                if own: notes.append('your answer: ' + ' | '.join(own))
                if chk: notes.append('hand fix after the check: ' + ' | '.join(chk))
            rows.append({'tag': tag, 'box': [round(v, 1) for v in f['box']], 'full_box': [round(v, 1) for v in fb], 'width': round(f['box'][2] - f['box'][0], 1), 'full_width': round(w, 1), 'src': f['src'], 'notes': notes, 'crop': [X0, Y0, X1, Y1]})
            pend.append((tag, fb, (X0, Y0, X1, Y1), mf, area, oval, mesh))
        cv2.imwrite(os.path.join(out, 'images', name.rsplit('.', 1)[0] + '.jpg'), outim, [cv2.IMWRITE_JPEG_QUALITY, 92])
        for tag, fb, (X0, Y0, X1, Y1), mf, area, oval, mesh in pend:   # crops from the finished image: original | result, 2.6 x the box
            cx, cy = (fb[0] + fb[2]) / 2, (fb[1] + fb[3]) / 2; Sx = max(fb[2] - fb[0], fb[3] - fb[1]) * 1.3
            a0, b0 = int(max(0, cx - Sx)), int(max(0, cy - Sx)); a1, b1 = int(min(Wf, cx + Sx)), int(min(Hf, cy + Sx))
            o = full[b0:b1, a0:a1].copy(); r = outim[b0:b1, a0:a1].copy(); side = 400
            # the area's outline on the original tile (white) - the 50% line of the feathered weight
            wm = np.zeros((Hf, Wf), np.uint8); wm[Y0:Y1, X0:X1] = (mf > 0.5).astype(np.uint8) * 255
            cs, _ = cv2.findContours(wm[b0:b1, a0:a1], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(o, cs, -1, (255, 255, 255), max(1, int(0.012 * (fb[2] - fb[0]))))
            if mesh is not None: cv2.polylines(o, [np.round(mesh - [a0, b0]).astype(np.int32)], True, (0, 220, 255), max(1, int(0.006 * (fb[2] - fb[0]))))   # the mesh outline in yellow
            cv2.imwrite(os.path.join(out, 'masks', tag + '.png'), np.dstack([(mf > 0.5).astype(np.uint8) * 255, (mf > 0.1).astype(np.uint8) * 255, (mf > 0.01).astype(np.uint8) * 255]))
            def sq(im):   # scaled to fit, padded (not stretched) to a square
                hh, ww = im.shape[:2]; k = side / max(hh, ww); im = cv2.resize(im, (max(1, int(ww * k)), max(1, int(hh * k))), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC)
                pad = np.full((side, side, 3), 200, np.uint8); pad[:im.shape[0], :im.shape[1]] = im; return pad
            tile = np.hstack([sq(o), sq(r)]); cv2.imwrite(os.path.join(out, 'crops', tag + '.jpg'), tile, [cv2.IMWRITE_JPEG_QUALITY, 88])
        # the whole image, small, with the areas drawn and lettered (for the sheet)
        sm = cv2.resize(full, (wkim.width, wkim.height)); kk = wkim.width / Wf
        for tag, fb, (X0, Y0, X1, Y1), mf, area, oval, mesh in pend:   # the blurred areas (50% line) drawn in red on the whole image
            wm = np.zeros((Hf, Wf), np.uint8); wm[Y0:Y1, X0:X1] = (mf > 0.5).astype(np.uint8) * 255; wm = cv2.resize(wm, (wkim.width, wkim.height), interpolation=cv2.INTER_NEAREST)
            cs, _ = cv2.findContours(wm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(sm, cs, -1, (0, 0, 220), 2)
        for r_ in rows:
            x0, y0, x1, y1 = [int(v) for v in r_['box']]; col = (160, 160, 160) if 'skipped' in r_ else (0, 0, 220)
            if 'skipped' in r_: cv2.rectangle(sm, (x0, y0), (x1, y1), col, 2)
            cv2.putText(sm, r_['tag'].split('-', 1)[1], (x0, max(12, y0 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, col, 2)
        cv2.imwrite(os.path.join(out, 'whole', name.rsplit('.', 1)[0] + '.jpg'), sm, [cv2.IMWRITE_JPEG_QUALITY, 80])
        sh = sm
        for _ in range(S.get('_turns', {}).get(name, 0)): sh = cv2.rotate(sh, cv2.ROTATE_90_CLOCKWISE)   # turned as Word turns it (item 16)
        if sh.shape[1] > 900: sh = cv2.resize(sh, (900, int(sh.shape[0] * 900 / sh.shape[1])), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(out, 'whole-sheet', name.rsplit('.', 1)[0] + '.jpg'), sh, [cv2.IMWRITE_JPEG_QUALITY, 75])
        res[name] = {'no': no, 'faces': rows, 'scale': K}; n += 1
        json.dump(res, open(os.path.join(out, 'faces.json'), 'w'), indent=1)
        print('%3d %-14s faces %2d blurred %2d  %.0fs' % (n, name, len(rows), sum(1 for r_ in rows if 'skipped' not in r_), time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(out, 'faces.json'), 'w'), indent=1)
    print('blur done', n, 'images; refused (no points):', refused)

def cmd_candidates(S):
    """A sheet of the 0.5-0.9 RetinaFace candidates not overlapping a known face, for Claude to judge by eye (item 5)."""
    out = S['out']; det = jl(os.path.join(S['src'], 'detections.json')); rfj = jl(os.path.join(out, 'rf.json')); tiles = []; tags = []
    for name, rec in sorted(det.items(), key=lambda kv: int(kv[1].get('no', 0))):
        no = str(rec.get('no')); faces = load_faces(dict(S, candidates_ok=[]), name, rec, rfj.get(name), None); img = None
        for f in rfj.get(name, {}).get('faces', []):
            if f['score'] >= 0.9 or any(overlap_small(f['box'], g['box']) > MERGE for g in faces): continue
            if img is None: img = cv2.imread(os.path.join(S['work'], name))
            x0, y0, x1, y1 = f['box']; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; s = max(x1 - x0, y1 - y0) * 1.5
            a0, b0 = int(max(0, cx - s)), int(max(0, cy - s)); a1, b1 = int(min(img.shape[1], cx + s)), int(min(img.shape[0], cy + s))
            t = cv2.resize(img[b0:b1, a0:a1], (200, 200)); cv2.rectangle(t, (int((x0 - a0) * 200 / (a1 - a0)), int((y0 - b0) * 200 / (b1 - b0))), (int((x1 - a0) * 200 / (a1 - a0)), int((y1 - b0) * 200 / (b1 - b0))), (0, 0, 255), 1)
            tag = '%s@%d,%d' % (no, int(x0), int(y0)); cv2.putText(t, '%s %.2f' % (tag, f['score']), (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1); tiles.append(t); tags.append(tag)
    if not tiles: print('no candidates'); json.dump([], open(os.path.join(out, 'candidates.json'), 'w')); return
    cols = 8; rowsn = math.ceil(len(tiles) / cols); sheet = np.zeros((rowsn * 200, cols * 200, 3), np.uint8)
    for i, t in enumerate(tiles): sheet[(i // cols) * 200:(i // cols + 1) * 200, (i % cols) * 200:(i % cols + 1) * 200] = t
    cv2.imwrite(os.path.join(out, 'candidates.jpg'), sheet, [cv2.IMWRITE_JPEG_QUALITY, 85]); json.dump(tags, open(os.path.join(out, 'candidates.json'), 'w'))
    print('candidates', len(tags), '->', os.path.join(out, 'candidates.jpg'))

if __name__ == '__main__':
    cmd = sys.argv[1]; S = json.load(open(sys.argv[2]))
    {'detect': cmd_detect, 'blur': cmd_blur, 'candidates': cmd_candidates}[cmd](S)
