#!/bin/bash
# more_checks.sh <build dir> <out dir>  (5 Nov 2026, owner 09:27 "this work is too slow make it faster. read and implement lessonslearned")
# The checks run_checks.sh does not run, one after another with nothing else beside them (lessons 15, 40): the Word format
# check, the column check, the text, code, style and wrap checks. Every check runs; nothing skipped (lesson 44).
set -u; B=$(cd "$1" && pwd); O=$2; mkdir -p "$O"; O=$(cd "$O" && pwd); M=/home/claude/mm; S=/home/claude/eng35/src
DOCX="$S/3.5.0 The English Curriculum.docx"; PDF="$S/3.5.0 The English Curriculum.pdf"; Z=$(ls $B/*CHECK-ONLY.zip | head -1); P=$B/preview
echo "start $(date +%H:%M:%S)" > $O/SUMMARY.txt
python3 $M/tools/v8/format_check_word.py "$Z" "$DOCX" > $O/format-word.txt 2>&1; echo "format (Word): $(tail -1 $O/format-word.txt)" >> $O/SUMMARY.txt
python3 $M/tools/col_check.py "$PDF" "$P" > $O/col.txt 2>&1; echo "columns: $(grep -E 'COLUMNS' $O/col.txt | tail -1)" >> $O/SUMMARY.txt
python3 $M/tools/text_rules.py "$P" "$DOCX" $O/text --settings $M/pages/the-english-curriculum.py > $O/text.log 2>&1; echo "text: $(tail -2 $O/text.log | head -1)" >> $O/SUMMARY.txt
python3 $M/tools/static_code.py "$Z" "$M/templates/Essay Code Template.html" $O/static.txt > $O/static.log 2>&1; echo "code (static): $(tail -2 $O/static.txt | head -1)" >> $O/SUMMARY.txt
python3 $M/tools/style_rules.py "$P" "$M/templates/Essay Code Template.html" $O/style.txt > $O/style.log 2>&1; echo "style: $(tail -2 $O/style.txt | head -1)" >> $O/SUMMARY.txt
python3 $M/tools/images_behaviour.py "$P" $O/images.txt full > $O/images.log 2>&1; echo "images: $(tail -2 $O/images.txt | head -1)" >> $O/SUMMARY.txt
python3 $M/tools/wrap_sweep.py "$P" "$DOCX" $O/wrap.txt 320 1920 1 > $O/wrap.log 2>&1; echo "wrap (1 px, 320-1920): $(tail -2 $O/wrap.txt | head -1)" >> $O/SUMMARY.txt
echo "end $(date +%H:%M:%S)" >> $O/SUMMARY.txt; cat $O/SUMMARY.txt
