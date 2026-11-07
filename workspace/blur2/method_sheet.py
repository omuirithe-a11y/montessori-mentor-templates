"""The sheet of items 16-17 for one set: every face once - each image whole with the blurred areas drawn (red 50% line) and lettered, turned as
Word turns it; under it each blurred face large, original (white outline of the area, yellow mesh outline where found) beside the result; grey
for faces left by rule or by the owner's answer; faces without a mesh marked; the count of images left off; the NOT CHECKED banner (item 19).
usage: python3 method_sheet.py <set.json> <title> <dst.html>            make the sheet (banner on)
       python3 method_sheet.py release <set.json> <sheet.html>          remove the banner, only if <out>/sheet-check.json records a pass
                                                                         by a separate agent made after the sheet (item 23)"""
import sys, os, json, base64, time
if sys.argv[1] == 'release':
    S = json.load(open(sys.argv[2])); sheet = sys.argv[3]; ck = os.path.join(S['out'], 'sheet-check.json')
    if not os.path.exists(ck): raise SystemExit('REFUSED: no sheet-check.json - a separate agent has not recorded a passed check')
    c = json.load(open(ck))
    if not c.get('pass') or os.path.getmtime(ck) < os.path.getmtime(sheet) or c.get('sheet') != os.path.basename(sheet): raise SystemExit('REFUSED: sheet-check.json is not a pass for this sheet made after it')
    # 26 Oct 2026 (the owner 14:03, "fix all of these now"): until now this checked only that the newest pass named the
    # sheet - a sheet checked in parts could be released on one part's pass. The set file names its parts in
    # "parts_expected"; every one of them must be recorded as passed in sheet-check.json "parts", which is either a list
    # of names or {name: true}. With no parts_expected, at least one part must be named, and it is printed.
    want = S.get('parts_expected') or []
    got = c.get('parts') or []
    have = set(got) if isinstance(got, (list, tuple)) else {k for k, v in got.items() if v}
    named = lambda w: any(w == h or w in str(h) for h in have)
    if want:
        missing = [w for w in want if not named(w)]
        if missing: raise SystemExit('REFUSED: the check records no pass for %d part%s of this sheet: %s\n  passed: %s\n  (the set file names its parts in "parts_expected")' % (len(missing), '' if len(missing)==1 else 's', ', '.join(missing), ', '.join(sorted(map(str, have))) or 'none'))
    elif not have:
        raise SystemExit('REFUSED: sheet-check.json names no part it checked ("parts"). Every part of the sheet is checked before it is released (method item 39).')
    print('parts passed: ' + ', '.join(sorted(map(str, have))))
    h = open(sheet).read(); b = '<div id="mm-unchecked">NOT CHECKED YET - a separate agent has not yet checked this sheet - please do not answer</div>'
    if b not in h: raise SystemExit('nothing to release')
    open(sheet, 'w').write(h.replace(b, '<div id="mm-checked" style="background:#2a6;color:#fff;padding:8px">Checked by a separate agent at %s - %s</div>' % (c.get('time', '?'), c.get('summary', 'passed'))))
    print('released', sheet); sys.exit()
S = json.load(open(sys.argv[1])); TITLE = sys.argv[2]; DST = sys.argv[3]; OUT = S['out']
res = json.load(open(os.path.join(OUT, 'faces.json')))
PAGE = {}
po = os.path.join(S['src'], 'page_order.json')
if os.path.exists(po):
    try:
        p = json.load(open(po)); PAGE = {str(k): v for k, v in (p.items() if isinstance(p, dict) else {})}
    except Exception: PAGE = {}
def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
rows = []; n_bl = 0; n_left = 0; n_img = 0; no_mesh = []; refused = []; answered = []; fixed = []; show = []; left_off = []
for name, v in sorted(res.items(), key=lambda kv: int(kv[1]['no'] or 0)):
    if not v['faces']: left_off.append(str(v['no'])); continue
    n_img += 1
    pg = (' &middot; page image %s' % PAGE[str(v['no'])]) if str(v['no']) in PAGE else ''
    rows.append('<h2>Image %s <span class="g">(%s%s)</span></h2><img class="w" src="%s">' % (v['no'], name, pg, b64(os.path.join(OUT, 'whole-sheet', name.rsplit('.', 1)[0] + '.jpg'))))
    for f in v['faces']:
        tag = f['tag']; letter = tag.split('-', 1)[1]
        if 'skipped' in f:
            n_left += 1
            if f['skipped'].startswith('REFUSED'): refused.append(tag)
            rows.append('<div class="s"><b>%s</b> &middot; %d px wide &middot; %s</div>' % (letter, round(f['width']), f['skipped'])); continue
        n_bl += 1; notes = f.get('notes', []); mesh = notes[0] if notes else ''
        if mesh.startswith('no mesh') or 'failed' in mesh: no_mesh.append(tag)
        ans = [x for x in notes if x.startswith('your answer')]
        if ans: answered.append(tag)
        hf = [x for x in notes if x.startswith('hand fix after the check')]
        if hf: fixed.append(tag)
        if any('shown to you' in x or 'show to the owner' in x for x in notes): show.append(tag)
        flags = []
        has_oval = any(x.startswith('oval') for x in notes)
        if any(x.startswith('labels not used') for x in notes): flags.append('<b class="r">area = the oval alone (hand fix after the check)</b>')
        elif mesh.startswith('no mesh'): flags.append('<b class="r">no mesh on this face: area = skin labels%s</b>' % (' + oval' if has_oval else ''))
        elif 'failed' in mesh: flags.append('<b class="r">mesh found but not on this face: area = skin labels%s</b>' % (' + oval' if has_oval else ''))
        else: flags.append(mesh + ' outline (yellow) + skin labels' + (' + oval' if has_oval else ''))
        flags += [x for x in notes if x.startswith('cut back') or x.startswith('labels cut') or 'shown to you' in x or 'show to the owner' in x]
        rf = [x for x in notes if x.startswith('RetinaFace')]
        rows.append('<div class="f"><img src="%s"><div class="t"><b>%s</b> &middot; %d px wide on the original &middot; %s%s%s</div></div>' % (
            b64(os.path.join(OUT, 'crops', tag + '.jpg')), letter, round(f.get('full_width', f['width'])), ' &middot; '.join(flags),
            (('<br><i>%s</i>' % ans[0]) if ans else '') + (('<br><i>%s</i>' % hf[0]) if hf else ''), ('<br><span class="g">%s</span>' % rf[0]) if rf else ''))
# 7 Nov 2026 (owner "implement all of these changes", S2b): the images with no face found are SHOWN too (they used to be only
# counted - page image 109 of The English Curriculum was never shown, and had a child's face), each whole, from the working copy
if left_off:
    from PIL import Image as _I
    os.makedirs(os.path.join(OUT, 'left-off'), exist_ok=True)
    rows.append('<h2>Images with no face found (%d) - please look at each for any child\'s face the finders missed</h2>' % len(left_off))
    for name, v in sorted(res.items(), key=lambda kv: int(kv[1]['no'] or 0)):
        if v['faces']: continue
        src = os.path.join(S['work'], name); dst = os.path.join(OUT, 'left-off', name.rsplit('.', 1)[0] + '.jpg')
        try:
            im = _I.open(src).convert('RGB'); im.thumbnail((900, 900)); im.save(dst, quality=85)
        except Exception as e:
            rows.append('<div class="s"><b class="r">Image %s (%s): could not be shown (%s)</b></div>' % (v['no'], name, e)); continue
        pg = (' &middot; page image %s' % PAGE[str(v['no'])]) if str(v['no']) in PAGE else ''
        rows.append('<div class="f"><div class="t"><b>Image %s</b> <span class="g">(%s%s) - no face found</span></div><img src="%s" style="max-width:450px"></div>' % (v['no'], name, pg, b64(dst)))
html = '''<!doctype html><html><head><meta charset="utf-8"><title>%s</title><style>
body{font-family:Georgia,serif;margin:20px;background:#f6f1e7;color:#222}h1{font-size:22px}h2{font-size:17px;margin:26px 0 8px;border-top:1px solid #c9bda3;padding-top:10px}.g{color:#777;font-weight:normal}
.w{display:block;max-width:100%%;border:1px solid #bbb;margin-bottom:8px}.f{margin:6px 0 14px}.f img{display:block;max-width:100%%;border:1px solid #bbb}.t{font-size:13px;margin-top:3px}.r{color:#b00}#mm-unchecked{background:#b00;color:#fff;padding:10px;font-size:16px}
.s{font-size:13px;color:#555;margin:4px 0 8px}.k{background:#fff;padding:10px 14px;border:1px solid #c9bda3;font-size:14px}</style></head><body>
<div id="mm-unchecked">NOT CHECKED YET - a separate agent has not yet checked this sheet - please do not answer</div>
<h1>%s</h1>
<div class="k">The method of BLUR-METHOD-26-oct.md version 22 (26 Oct 10:1x), run on the full-size originals: the face mesh's outline, with the face-skin labels filling gaps within 0.06 of the face width of it (the labels near the nose and mouth where they lie outside the outline) and a disc round each eye, nose and mouth point that lies on the face (where there is no mesh, the one patch of labels that holds the nose, within the face box grown a tenth sideways and a tenth down, a quarter up), an oval centred on the eyes, nose and mouth only where those cover under half the face box (0.84 of the box wide, kept inside the box and within 0.06 of the face width of the outline round the labels and the eyes, nose and mouth), edge grown 0.03 and feathered 0.08 of the face width, Gaussian blur 0.12 x the face width. Nothing from the 25 Oct trial's blur is kept; your answers are.<br>
Each image whole, turned as on the page, with every blurred area outlined in red and lettered (grey boxes = faces left); then each blurred face large: <b>original</b> with the white outline of the blurred area and the yellow mesh outline where the mesh was found &middot; <b>result</b>. %d faces blurred on %d images; %d faces left (listed in grey with the reason); %d images with no face found are shown whole at the end%s.<br>
Faces without a mesh (area = skin labels, with an oval where they covered under half the box), %d: %s.<br>
Faces where your 25 Oct answer was applied, %d: %s.%s%s<br>
Faces I adjusted by hand after a separate check found a fault (not your answers), %d: %s.<br>
Faces I could not decide (red unless you say otherwise): %s. Answer by number and letter as before (e.g. "not covering enough 8d; no blurring 2c; no changes").</div>
%s
<p class="g">Made %s.</p>
</body></html>''' % (TITLE, TITLE, n_bl, n_img, n_left, len(left_off), (' (images %s)' % ', '.join(left_off)) if left_off else '', len(no_mesh), ', '.join(no_mesh) or 'none', len(answered), ', '.join(answered) or 'none',
    (' <b class="r">Shown to you for a decision (the mesh was found but failed its position tests, or a re-fit changed nothing): %s.</b>' % ', '.join(show)) if show else '',
    (' <b class="r">Refused (no eye, nose and mouth points - hand points needed): %s.</b>' % ', '.join(refused)) if refused else '', len(fixed), ', '.join(fixed) or 'none', ', '.join(S.get('undecided', [])) or 'none', ''.join(rows), time.strftime('%d %b %Y %H:%M:%S'))
open(DST, 'w').write(html); print('sheet', DST, 'blurred', n_bl, 'left', n_left, 'images', n_img, 'left off', len(left_off), 'no-mesh', len(no_mesh), 'bytes', len(html))
