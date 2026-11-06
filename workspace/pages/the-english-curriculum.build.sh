#!/bin/bash
# Build command for The English Curriculum (3.5.0), Essay Code Template. Usage: bash pages/the-english-curriculum.build.sh bN
# Sources downloaded from Google Drive (her 6:53 5 Nov update), size checked against Drive on 5 Nov 17:2x:
#   Word: 3.5.0 The English Curriculum.docx - Drive file id: 1BHTkC40TdBeQwNSXMAhos2iVMnZ9ZgvC (396121581 bytes, modified 2026-11-04T22:49:15Z)
#         https://drive.google.com/file/d/1BHTkC40TdBeQwNSXMAhos2iVMnZ9ZgvC/view
#   PDF:  3.5.0 The English Curriculum.pdf  - Drive file id: 175BpC3SJGCX9zedGRUNZwAjd2PwLaunx (63648019 bytes, modified 2026-11-04T22:50:49Z)
#         https://drive.google.com/file/d/175BpC3SJGCX9zedGRUNZwAjd2PwLaunx/view
#   Local copies in /home/claude/eng35/src (Word sha256 36a76415..., PDF 4e44885a...)
# Faces: final images after her 09:31 round 1 answer and 10:04 round 2 "approved", pixel check build-35/faces/pixel-check-after-answer.json
set -e
cd /home/claude/mm
B=${1:?build name, e.g. b22}
bash tools/build_guard.sh build-35 "$B" || exit 3; export MM_GUARD_DONE="$B"   # 6 Nov 2026 (owner 08:01): one build per check round
python3 tools/build_page.py --docx "/home/claude/eng35/src/3.5.0 The English Curriculum.docx" --pdf "/home/claude/eng35/src/3.5.0 The English Curriculum.pdf" --template essay --title "The English Curriculum" --folder the-english-curriculum --menu-from /home/claude/eng35/live/picture-books/index.html --settings pages/the-english-curriculum.py --photos /home/claude/mm/build-35/faces/photos-final --hero /home/claude/eng35/src/hero/english-hero-original.jpg --section-href /the-montessori-curriculum/ --out build-35/$B > build-35/$B.log 2>&1
tail -1 build-35/$B.log
