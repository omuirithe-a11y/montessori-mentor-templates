"""Fetch a Drive file by its id, any size (20 Oct 2026). The Drive tool stops at 10 MB; this does not.
  python3 tools/fetch_drive.py <file id> <out path>
Find the id with the Drive tool's search (search_files); the file must be the user's own."""
import sys, subprocess, os
fid, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
r = subprocess.run(['curl', '-sSL', '-o', out, '-w', '%{http_code} %{size_download}',
                    'https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t' % fid], capture_output=True, text=True)
print(out, r.stdout, r.stderr.strip())
head = open(out, 'rb').read(5)
if head.startswith(b'<'): sys.exit('not a file - Drive returned a web page (file not shared to this link, or wrong id)')
