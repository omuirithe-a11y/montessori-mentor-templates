# Separate check of the round 1 faces sheet, The English Curriculum (3.5.0), 4 Nov 2026

You have not seen this work being made. Check it as items 20-23 of the blur method (version 22) require, and report. You change no file except the two named under "Write" at the end. Do not run anything that rewrites the sheet, the masks, the images or faces.json.

## Files (all under /home/claude/mm/blur2/m_eng/ unless a full path is given)
- The sheet: eng-sheet.html (NOT CHECKED banner on). Its file name must not change.
- faces.json: every face by image (key = Word media name) with "no" (the sheet's image number), "tag" (no-letter), "box", "crop", "full_width"; a left face has "skipped" with its reason.
- check-measure.json: the measurements already run (counts, byte-identity of every embedded image, changed share inside each blurred area, feather reach, changed pixels beyond reach per image, left faces changed). Read its "fails" and "reports" lists and judge each one at full size - a "fail" there is not a fail of the sheet until you have looked.
- images/<stem>.jpg: the full result images. The originals: /home/claude/mm/blur2/m_eng/media/ (the Word media).
- masks/<tag>.png: each blurred area (channel 0 = 50% line, channel 1 = 10% line). crops/, whole-sheet/: the files embedded in the sheet.
- The rules for which faces are left: faces/by_rule.json (41 faces: adults, printed/historical images, objects, no eye showing), faces/keep_unblurred.json (the owner's no-blur images: every face on them is left by her words), sets/eng.json "undecided" (11 faces blurred and named at the top of the sheet for her to rule on), faces/extra_faces.json (10 hand-added), faces/adjust_faces.json.
- The maker's by-eye notes, for reference only after you have formed your own view: /home/claude/eng35/review/notes.jsonl.
- An example of the report wanted, from another page: /home/claude/eng35/example-check.md.

## What to do, in four parts
1. Counts and byte-identity (item 20): embedded images all byte-identical to a file; faces.json counts (blurred / left / images with faces / left off) against the sheet's own line and against by_rule + keep + undecided; every result image the same size as its original. Say the figures you read.
2. Item 21 measures on the full result images: every entry in check-measure.json "fails" and "reports" looked at enlarged, original beside result, and judged: JPEG noise and rounding pass; spill onto hair, a neighbour or an object fails; a left face changed fails unless within a neighbour's feather and judged harmless; any adult or by-rule face blurred fails.
3. Item 22 by eye at full size: every flagged face, every hand-added face, every undecided face, the 10 smallest faces and 30 faces at random (say the seed) - the blur must hide the features (eyes, nose, mouth) with a soft edge; a soft lip bump is allowed.
4. Whole images for missed faces: look at every one of the 165 images whole (the 121 result images and the 44 left off, from media/), enlarge any doubtful spot, and name any child's face with an eye showing that is not lettered. Backs of heads, ears or cheeks with no eye, faces hidden behind objects, printed pictures, and adults are not missed faces. Adults must be left; say where you checked them.

## Write
- /home/claude/mm/blur2/m_eng/sheet-check.json: {"pass": true|false, "when": "<clock time from `date`>", "sheet": "eng-sheet.html", "parts": {"counts and byte-identity": true|false, "item 21 measures": true|false, "item 22 by eye": true|false, "whole images for missed faces": true|false}, "time": "<clock time>", "summary": "<one line>", "sheet_sha256": "<sha256 of eng-sheet.html>", "faces_blurred": N, "faces_left": N, "missed": [...], "failed": [...], "notes": "..."}. pass is true only if nothing failed and no face was missed.
- /home/claude/mm/blur2/m_eng/sheet-check-report.md: the report, in the shape of the example, with a "For the owner" section for anything she should know (numbered by the sheet's image numbers), a "Could not check" line, and the last line "PASS" or "FAIL: <what>".

Rules: every time from `date`, never typed ahead; every figure from a file or a command you ran; say "image", never "photo"; plain words; no claims beyond what you looked at.

## Check v2 (4 Nov 20:2x)
A first check (v1, /home/claude/eng35/sheet-check-v1-report.md) failed the sheet: faces missed on images 136, 31 and 130, and 57-e wrongly left. The sheet was remade with those four blurred (now 281 blurred, 50 left). Do the whole check again as above, and in part 3 look at 136-b, 31-g, 130-c and 57-e in particular. Write your report with "v2" in its title.

## Check v3 (4 Nov 21:2x)
Check v2 (/home/claude/eng35/sheet-check-v2-report.md) failed the sheet: a face missed on image 141 (the boy at the far right of the group at the back) and 123-g wrongly left as "not a face". Both are now blurred (141-d was a finder's face wrongly ruled a printed picture; 123-g's rule withdrawn). The sheet now has 283 blurred, 48 left (41 by rule, 7 by the owner's words). Do the whole check again as above; in part 3 look at 141-d and 123-g in particular, and in part 4 look again at every image whole - two checks have each found faces the one before missed. Write your report with "v3" in its title.
