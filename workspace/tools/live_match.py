#!/usr/bin/env python3
"""After the owner uploads (27 Oct 2026, 14:3x). usage: python3 live_match.py <the package .zip that was handed over>
Downloads the live page and every file the package holds from montessorimentor.co.uk (a plain fetch returns the true file)
and proves each is byte-identical to the package. Any difference means the upload or the server is not what was checked."""
import sys, zipfile, hashlib, subprocess, tempfile, os
z = zipfile.ZipFile(sys.argv[1]); names = [n for n in z.namelist() if not n.endswith('/')]
slug = names[0].split('/')[0]; tmp = tempfile.mkdtemp(prefix='lm-'); bad = 0
import atexit, shutil; atexit.register(shutil.rmtree, tmp, True)   # v7: the unpacked copy is deleted when the check ends (copies filled the disk on 27 Oct)
for n in names:
    rel = n[len(slug) + 1:]; url = 'https://montessorimentor.co.uk/%s/%s' % (slug, '' if rel == 'index.html' else rel)
    out = os.path.join(tmp, 'f'); r = subprocess.run(['curl', '-sS', '--retry', '2', '-o', out, '-w', '%{http_code}', url], capture_output=True, text=True)
    want = hashlib.sha256(z.read(n)).hexdigest(); got = hashlib.sha256(open(out, 'rb').read()).hexdigest() if r.stdout == '200' else r.stdout
    if got != want: bad += 1; print('DIFFERS %s: live %s, package %s' % (rel, got[:16], want[:16]))
print('RESULT: %d of %d files identical to the package on the live site' % (len(names) - bad, len(names)))
