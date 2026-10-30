"""Item 18 helper: faces whose pixels changed between <out>/images.before-v<N> and <out>/images, within each face's full_box grown 0.3 w.
usage: python3 changed.py <set.json> <N>  -> <out>/changed-v<N>.json"""
import sys, os, json, numpy as np, cv2
S = json.load(open(sys.argv[1])); N = sys.argv[2]; O = S['out']; r = json.load(open(os.path.join(O, 'faces.json'))); out = []
for name, v in r.items():
    jn = name.rsplit('.', 1)[0] + '.jpg'; a, b = os.path.join(O, 'images.before-v' + N, jn), os.path.join(O, 'images', jn)   # results are saved as <stem>.jpg
    if not os.path.exists(b): continue
    B = cv2.imread(b); A = cv2.imread(a) if os.path.exists(a) else None
    for f in v['faces']:
        if 'skipped' in f or 'full_box' not in f: continue
        if A is None or A.shape != B.shape: out.append(f['tag']); continue
        x0, y0, x1, y1 = f['full_box']; g = 0.3 * (x1 - x0); H, W = B.shape[:2]
        X0, Y0, X1, Y1 = int(max(0, x0 - g)), int(max(0, y0 - g)), int(min(W, x1 + g)), int(min(H, y1 + g))
        if (np.abs(A[Y0:Y1, X0:X1].astype(int) - B[Y0:Y1, X0:X1].astype(int)).max(axis=2) > 12).any(): out.append(f['tag'])
json.dump(out, open(os.path.join(O, 'changed-v%s.json' % N), 'w')); print(len(out), out[:40])
