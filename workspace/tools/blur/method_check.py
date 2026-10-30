"""Measurements for the separate agent's check (items 20-21, 25): counts; every embedded image byte-identical to its file (crops and whole-sheet
renders); on the full result images, against a q92 recompression of the original: every blurred face changed inside its area; every left face
unchanged (a left face within a blurred area's feather reach is reported, not failed); nothing changed further than 0.3 w (0.63 w for a feather-0.2
face) from each area's 50% line, measured from the saved masks; and the distance from each area's 50% line to its 10% line (the feather's reach).
usage: python3 method_check.py <set.json> <sheet.html> -> prints JSON and writes <out>/check-measure.json"""
import sys, os, json, re, base64, cv2, numpy as np, hashlib
S = json.load(open(sys.argv[1])); SHEET = sys.argv[2]; OUT = S['out']; res = json.load(open(os.path.join(OUT, 'faces.json')))
html = open(SHEET).read()
embedded = re.findall(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', html)
files = {}
for d in ('crops', 'whole-sheet'):
    for p in os.listdir(os.path.join(OUT, d)): files[hashlib.sha256(open(os.path.join(OUT, d, p), 'rb').read()).hexdigest()] = d + '/' + p
emb = [hashlib.sha256(base64.b64decode(e)).hexdigest() for e in embedded]
report = {'sheet': SHEET, 'embedded_images': len(embedded), 'byte_identical_to_a_file': sum(1 for h in emb if h in files), 'not_matching_any_file': sum(1 for h in emb if h not in files),
          'faces_blurred': sum(1 for v in res.values() for f in v['faces'] if 'skipped' not in f), 'faces_left': sum(1 for v in res.values() for f in v['faces'] if 'skipped' in f),
          'images_with_faces': sum(1 for v in res.values() if v['faces']), 'images_left_off': sum(1 for v in res.values() if not v['faces']), 'faces': {}, 'fails': [], 'reports': []}
ANS = S.get('answers', {})
for name, v in res.items():
    if not v['faces']: continue
    orig = cv2.imread(os.path.join(S['media'], name)); out = cv2.imread(os.path.join(OUT, 'images', name.rsplit('.', 1)[0] + '.jpg'))
    ok, enc = cv2.imencode('.jpg', orig, [cv2.IMWRITE_JPEG_QUALITY, 92]); q92 = cv2.imdecode(enc, 1)
    noise = np.abs(q92.astype(np.int16) - orig.astype(np.int16)).max(axis=2)
    diff = np.abs(out.astype(np.int16) - orig.astype(np.int16)).max(axis=2)
    changed = diff > np.maximum(noise + 2, 6)
    H, W = orig.shape[:2]; allowed = np.zeros((H, W), np.uint8); reach_union = np.zeros((H, W), np.uint8)
    for f in v['faces']:
        if 'skipped' in f: continue
        m = cv2.imread(os.path.join(OUT, 'masks', f['tag'] + '.png')); X0, Y0, X1, Y1 = f['crop']; w = f['full_width']
        m50 = m[..., 0]; m10 = m[..., 1]
        ed = ANS.get(f['tag'], {}); reach = max(0.3, round(ed.get('grow', 0.03) + 3 * ed.get('feather', 0.08), 3))   # item 21: grow + 3 x feather (0.27 -> 0.3 by default; 0.63 for feather 0.2; 0.50 for grow 0.08 + feather 0.14)
        r = int(round(reach * w)); grown = cv2.dilate(m50, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
        allowed[Y0:Y1, X0:X1] = np.maximum(allowed[Y0:Y1, X0:X1], grown); reach_union[Y0:Y1, X0:X1] = np.maximum(reach_union[Y0:Y1, X0:X1], m10)
        # the feather's reach: farthest 10%-line pixel from the 50% line, in units of w
        dt = cv2.distanceTransform(255 - m50, cv2.DIST_L2, 5); far = float(dt[m10 > 0].max()) / w if (m10 > 0).any() else 0.0
        inside = changed[Y0:Y1, X0:X1][m50 > 0]; share = float(inside.mean()) if inside.size else 0.0
        report['faces'][f['tag']] = {'changed_share_inside_area': round(share, 3), 'feather_reach_w': round(far, 3), 'reach_limit_w': reach}
        if share < 0.6: report['fails'].append((f['tag'], 'blurred face changed on only %.0f%% of its area' % (100 * share)))
        if far > 0.2 and reach <= 0.3: report['reports'].append((f['tag'], 'feather reach %.2f w (expected about 0.13)' % far))
    outside = int((changed & (allowed == 0)).sum())
    report['faces']['image %s' % v['no']] = {'changed_pixels_beyond_reach': outside}
    if outside > 0: report['fails'].append(('image %s' % v['no'], 'changed pixels further than the allowed reach from every area: %d' % outside))
    for f in v['faces']:
        if 'skipped' not in f: continue
        sc = v.get('scale', 1); x0, y0, x1, y1 = [c * sc for c in f['box']]
        box = changed[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)]; share = float(box.mean()) if box.size else 0.0
        near = reach_union[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)].any()
        report['faces'][f['tag']] = {'left': True, 'changed_share_in_box': round(share, 3), 'within_a_blurred_areas_feather': bool(near)}
        if share > 0.02: (report['reports'] if near else report['fails']).append((f['tag'], 'left face changed on %.0f%% of its box%s' % (100 * share, ' - within a neighbour\'s feather, reported not failed' if near else '')))
json.dump(report, open(os.path.join(OUT, 'check-measure.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in report.items() if k != 'faces'}, indent=1))
