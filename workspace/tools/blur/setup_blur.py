"""Set up a chat for the agreed blur method (claude/BLUR-METHOD-26-oct.md version 22, agreed 26 Oct 2026 13:47, item 1).
Written 26 Oct 2026 on the owner's instruction, 14:03: "fix all of these now".

    python3 setup_blur.py [--mm /home/claude/mm]

The workspace is wiped between chats, so every chat needs the same libraries, models and tools again. This checks each
one, installs or downloads what it can, and checks every fingerprint against the one the method names. It prints READY
or STOP, so nothing runs on a wrong file.

What it does by itself: pip install mediapipe 0.10.32 and retina-face 0.0.19; download face_landmarker.task and
selfie_multiclass_256x256.tflite from Google's model store; check all three fingerprints (the two models and yunet.onnx).
What it cannot do (no network for these, or they need Claude's own tools): copy claude/workspace from the Project, and
fetch yunet.onnx from Drive or the records repository. It names those and stops, instead of leaving a half-set-up chat.
"""
import sys, os, json, subprocess, hashlib, urllib.request

MM = '/home/claude/mm'
for i, a in enumerate(sys.argv):
    if a == '--mm' and i + 1 < len(sys.argv): MM = os.path.abspath(sys.argv[i + 1])
BLUR = os.path.join(MM, 'blur2')

# every fingerprint the method names (item 1), plus yunet.onnx as read from the workspace on 26 Oct 01:5x
MODELS = [
    (os.path.join(MM, 'models', 'face_landmarker.task'),
     'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task',
     '64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff'),
    (os.path.join(BLUR, 'models', 'selfie_multiclass_256x256.tflite'),
     'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite',
     'c6748b1253a99067ef71f7e26ca71096cd449baefa8f101900ea23016507e0e0'),
    (os.path.join(MM, 'faces', 'yunet.onnx'), None,
     '8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4'),
]
PIP = [('mediapipe', '0.10.32'), ('retina-face', '0.0.19')]
TOOLS = ['method.py', 'method_sheet.py', 'method_check.py', 'changed.py', 'grid.py', 'page.py']

stops, notes = [], []


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def version(pkg):
    try:
        from importlib.metadata import version as v
        return v(pkg)
    except Exception:
        return None


print('Set-up for the agreed blur method, version 22. Workspace: ' + MM)

for pkg, want in PIP:
    got = version(pkg)
    if got == want:
        print('  %-14s %s  already installed' % (pkg, got)); continue
    print('  %-14s %s -> installing %s' % (pkg, got or 'not installed', want), flush=True)
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', '%s==%s' % (pkg, want)])
    got = version(pkg)
    if r.returncode or got != want:
        stops.append('%s is %s, not %s. Install it by hand: pip install --break-system-packages %s==%s' % (pkg, got or 'missing', want, pkg, want))
    else:
        print('  %-14s %s  installed' % (pkg, got))

for path, url, want in MODELS:
    name = os.path.basename(path)
    if not os.path.exists(path) and url:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print('  %-34s downloading' % name, flush=True)
        try:
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            if os.path.exists(path): os.remove(path)
            stops.append('%s could not be downloaded (%s). Its address is in README "Faces".' % (name, e))
            continue
    if not os.path.exists(path):
        stops.append('%s is missing and cannot be downloaded here: %s.\n      yunet.onnx comes from the Drive folder "faces-tools" (tools/fetch_drive.py 1v60o1zyUb64nL0gIVnMYLjIeF8x46EB8) or from the records repository, faces_template/yunet.onnx (README step 4).' % (name, path))
        continue
    got = sha(path)
    if got != want:
        stops.append('%s differs from the model the method names.\n      file: %s\n      its SHA-256: %s\n      needed:      %s' % (name, path, got, want))
    else:
        print('  %-34s fingerprint correct' % name)

missing = [t for t in TOOLS if not os.path.exists(os.path.join(BLUR, t))]
if missing:
    stops.append('blur tools missing from %s: %s.\n      Claude copies claude/workspace/tools/blur/ from the Project into that folder (README "Faces").' % (BLUR, ', '.join(missing)))
else:
    print('  %-34s all present' % 'blur tools')

if not os.path.exists(os.path.join(MM, 'w220', 'tools', 'faces.py')) and not os.path.exists(os.path.join(MM, 'ws', 'tools', 'faces.py')):
    stops.append('tools/faces.py is missing (it does the YuNet steps, method items 4-5). Claude copies claude/workspace/ from the Project.')

print()
if stops:
    print('STOP - %d thing%s to settle before any blur runs:' % (len(stops), '' if len(stops) == 1 else 's'))
    for s in stops: print('  - ' + s)
    sys.exit(1)
print('READY. Every library, model and tool is present with the fingerprint the method names.')
print('Next, for a page: python3 %s new <name> --docx <Word file>' % os.path.join(BLUR, 'page.py'))
