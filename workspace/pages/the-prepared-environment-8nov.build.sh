#!/bin/bash
# Build command for The Prepared Environment (2.2.0) rebuilt from the new Word file of 8 Nov 2026 (owner "B"). Usage: bash pages/the-prepared-environment-8nov.build.sh bN
# Word: Drive 1yFwpuu62d2RwSjHTDQxG1bBAHUW9HxyU (1158244863 bytes, modified 2026-11-07T23:59:25Z); PDF: 1wxirPhGCniYmSMiPOpdesrtMZnmP-xuA (111704977 bytes)
# Hero: Drive 1bvdKFBNPGIelgwcMv2-IPQZaG3E_7SlR prepared-environment-hero.jpg (faces already blurred, 18 Oct)
set -e
cd /home/claude/mm
B=${1:?build name, e.g. b1}
export DECISIONS_SHEET=/home/claude/pe2/decisions.md
export PAGE_SLUG=the-prepared-environment
bash tools/build_guard.sh /home/claude/pe2/build "$B" || exit 3; export MM_GUARD_DONE="$B"
[ "$B" = try ] && rm -rf /home/claude/pe2/build/try   # 8 Nov 2026: a trial build replaces the last trial
python3 tools/build_page.py --docx ${PE_DOCX:-/home/claude/pe2/src9/2.2.0-v2.docx} --pdf ${PE_PDF:-/home/claude/pe2/src10/2.2.0.pdf} --template essay --title "The Prepared Environment" --folder the-prepared-environment --menu-from /home/claude/tpl/livenow/the-prepared-environment/index.html --settings pages/the-prepared-environment-8nov.py --photos /home/claude/pe2/build/the-prepared-environment/faces/photos-final --hero /home/claude/pe2/src/hero/prepared-environment-hero.jpg --hero-pos "center 22%" --section-href /essential-elements/ --out /home/claude/pe2/build/$B > /home/claude/pe2/build/$B.log 2>&1
tail -3 /home/claude/pe2/build/$B.log
