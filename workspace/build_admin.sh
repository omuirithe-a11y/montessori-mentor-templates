
# usage: bash build_admin.sh [5.1 5.3 ...]   (no numbers: all five)
# 23 Oct 2026: 5.3 Classroom Management has been built on the ESSAY template since 21 Oct 2026, not the Resources template
# shown below; the exact Essay build command was not recorded (lost when the 22-23 Oct chat was condensed). A command that
# rebuilt it for testing on 23 Oct: --template essay --docx <5.3.docx> --pdf <5.3.pdf> --title "Classroom Management"
# --folder classroom-management --menu "Classroom Management" --hero heroes/administration.jpg --section-href /administration/
# --photos <5.3 blurred photos> --settings pages/classroom-management.py  (the PDF and section link are not checked against the live build)
PAGES="$*"; w(){ case " ${PAGES:-5.1 5.2 5.3 5.4 5.5} " in *" $1 "*) echo "== $1"; return 0;; esac; return 1; }
S=/home/claude/admin/src; F=/home/claude/admin/faces
b(){ timeout 600 python3 tools/build_page.py --template resources --no-toc --hero heroes/administration.jpg --section-href /administration/ "$@" 2>&1 | grep -E "WARNING|DIFFER|^photo|zip:|Error|Traceback|failed" ; }
w 5.1 && b --docx $S/5.1.docx --title "Staff" --folder staff --menu "Staff" --settings pages/staff.py --photos build/staff/faces/photos
w 5.2 && b --docx $S/5.2.docx --title "School Handbook" --folder school-handbook --menu "School Handbook" --settings pages/school-handbook.py
w 5.3 && echo "5.3 is on the Essay template - see the note at the top; not built by this script"
w 5.4 && b --docx $S/5.4-work.docx --pdf $S/5.4.pdf --title "Beginning of the Year - Teachers" --folder beginning-of-the-year-for-teachers --menu "Beginning of the year for Teachers" --settings pages/beginning-of-the-year-for-teachers.py --photos $F/5.4/photos
w 5.5 && b --docx $S/5.5.docx --title "Observations for Teachers" --folder observations-for-teachers --menu "Observations for Teachers" --settings pages/observations-for-teachers.py
