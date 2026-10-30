"""Word's vector drawings (EMF/WMF) as pictures (22 Oct 2026, user: "do all of this").

The image library here can recognise EMF/WMF but cannot draw them, so the converter stopped on them (5.4, 20 Oct) and
faces.py skipped them (a child in such a drawing was never checked). This makes a working copy of the Word file in which
every EMF/WMF picture is replaced by a PNG of the same drawing, under the SAME name (so page settings that name the
picture, e.g. 'image1.emf', still find it). The original Word file is never changed.

  1. a picture embedded inside the drawing (a PDF, as on 5.4's name cards; else a PNG or JPEG) is taken out:
     a PDF is drawn at 400 dpi, its first page;
  2. otherwise LibreOffice draws the drawing itself.

  python3 tools/drawings.py <word.docx> <out.docx>      prints what was replaced
"""
import io, os, re, shutil, subprocess, sys, tempfile, zipfile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

VECTOR = ('.emf', '.wmf', '.emz', '.wmz')

def _embedded(blob):
    """A picture stored inside the drawing, or None."""
    i = blob.find(b'%PDF-')
    if i >= 0:
        j = blob.rfind(b'%%EOF')
        if j > i:
            import fitz
            try:
                d = fitz.open(stream=blob[i:j + 5], filetype='pdf')
                pm = d[0].get_pixmap(dpi=400, alpha=False)
                return pm.tobytes('png'), 'the PDF inside it, drawn at 400 dpi'
            except Exception:
                pass
    for sig, end, kind in ((b'\x89PNG\r\n\x1a\n', b'IEND\xaeB`\x82', 'PNG'), (b'\xff\xd8\xff', b'\xff\xd9', 'JPEG')):
        i = blob.find(sig)
        if i >= 0:
            j = blob.rfind(end)
            if j > i:
                try:
                    im = Image.open(io.BytesIO(blob[i:j + len(end)])); im.load()
                    if im.width > 50 and im.height > 50:
                        b = io.BytesIO(); im.convert('RGB').save(b, 'PNG'); return b.getvalue(), 'the %s inside it' % kind
                except Exception:
                    pass
    return None

def _render(name, blob):
    """LibreOffice draws the drawing itself."""
    with tempfile.TemporaryDirectory() as t:
        src = os.path.join(t, os.path.basename(name)); open(src, 'wb').write(blob)
        subprocess.run(['soffice', '--headless', '--convert-to', 'png', '--outdir', t, src], capture_output=True, timeout=240)
        png = os.path.splitext(src)[0] + '.png'
        if os.path.exists(png) and os.path.getsize(png) > 0:
            return open(png, 'rb').read(), 'drawn by LibreOffice'
    return None

def _trim(png):
    """White page margins round the drawing cut off (5.4: the embedded PDF page has a white foot); None if all white."""
    im = Image.open(io.BytesIO(png)).convert('RGB')
    from PIL import ImageChops
    box = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 8 else 0).getbbox()
    if not box: return None
    pad = 4; box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    b = io.BytesIO(); im.crop(box).save(b, 'PNG'); return b.getvalue()

def picture(name, blob):
    """(png bytes, how) for one drawing, or (None, reason)."""
    if name.lower().endswith(('.emz', '.wmz')):
        import gzip
        try: blob = gzip.decompress(blob)
        except Exception: pass
    for get in (_embedded, lambda b: _render(name, b)):
        r = get(blob)
        if r:
            png = _trim(r[0])
            if png: return png, r[1] + ', white margins trimmed'
    # 22 Oct 2026: LibreOffice drew 5.4's drawing as a blank page - a blank result is not accepted
    return None, 'WARNING: could not be drawn (left as it is - the page build and the faces step will report it)'

def prepare(docx, out):
    """Copy docx to out with every EMF/WMF picture replaced by a PNG of it (same name). Returns [(name, how)]."""
    done = []
    with zipfile.ZipFile(docx) as zi:
        vec = [n for n in zi.namelist() if n.startswith('word/media/') and n.lower().endswith(VECTOR)]
        if not vec:
            if os.path.abspath(docx) != os.path.abspath(out): shutil.copy(docx, out)
            return done
        tmp = out + '.part'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = zi.read(it.filename)
                if it.filename in vec:
                    png, how = picture(it.filename, data)
                    if png: data = png
                    done.append((it.filename.split('/')[-1], how))
                zo.writestr(it, data)
    os.replace(tmp, out)
    return done

if __name__ == '__main__':
    for n, how in prepare(sys.argv[1], sys.argv[2]): print(n, '-', how)
