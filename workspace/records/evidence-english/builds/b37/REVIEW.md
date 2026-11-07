# Separate review - The English Curriculum (3.5.0), build 37, against the owner's PDF (after the fast round)

- Time: Fri 6 Nov 2026 15:09-15:11 CST (from `date`), after "FAST CHECKS PASSED 15:08:36" in checks2/SUMMARY.txt. This replaces the review written at 15:01, before the round finished.
- Build folder: /home/claude/mm/build-35/b37
- Zip: /home/claude/mm/build-35/b37/the-english-curriculum.zip, sha256 303e01d4928b2e634584441cbbd1e90a444c2ed83da3526b8d3e99312190bfc9 (from `sha256sum`; matches "303e01d4928b2e63" in SUMMARY.txt, FAST-PASSED and fast.log, and the full hash in widths13.txt and gate-early.txt). 328 files. The zip's index.html is byte-identical to hostinger/the-english-curriculum/index.html (sha256 4a94d51d...).
- Compared: page code against build 36's (split at tags): the only change is two list items, "Follow the Muriel Dwyer approach." and "Follow the Pink, Blue and Green series.", `data-gap` 25 -> 20. Every file in checks2/ read (list in H). PDF render /home/claude/eng35/review31/pdf/p18.png for the changed list. Build log /home/claude/eng35/build-b37.log.
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 36's, then the full pages stitched and matched row by row.
  - 1440: identical down to part16 y 1203; from there item 2 is build 36's moved up 5 px and everything from item 3 to the end moved up 10 px; no row left unmatched. part21 647 -> 637 px.
  - 768: same from part20 y 1180; part26 801 -> 791 px. No row unmatched.
  - 390: same from part30 y 436 (some rows move 9 px - one-pixel rounding); part38 820 -> 810 px. Rows matching neither shift: part01 y 20-345 (contents box, edge smoothing, largest grey difference 49), part18 y 1186-1203 and part20 y 253-268 (edge smoothing, 30), part31 y 364-452 (a few single rows in the Blue Series image set, rounding).
  - Looked at by eye, build 36 and 37 side by side: the changed list at 1440 (part16), 768 (part20), 390 (part30); 390 part31 (Blue Series set and its dots, "Early Readers"). They look right; nothing else moved relative to its neighbours.
- NOT checked: menu panels; links not clicked; swipe rows not swiped; widths other than 1440/768/390 by eye (640 only through space.txt); unchanged parts not re-read against the PDF (words and format unchanged, see H); full-size images and faces records; the long checks (more_checks.sh long, run_checks.sh: 122 widths, height, lines, place, speed), which have not run yet. No browser and no check script run. No file changed except this report.

## Words and her rules (not faults)
- Corrections (for her to confirm), from checks2/text/corrections.txt, same as build 36: characterised, civilisation(s), colourful, memorising, organising, practising x3, recognise, tyrannise (UK, A023/A108); instils, practise x3, Practise, "they -> the", "title's -> titles" x2 (page settings); long dashes -> short (5); spaces round "/" removed (7).
- The list's new gaps follow the PDF (p18: items about 32 px apart in the rendering, "together").

## Faults

### A contents box
None (1440/768 part01 identical; 390 part01 edge smoothing only).

### B headings and text
None. No word changed.

### C bold/italic/colour
None. format-word.txt identical to build 36's; the Muriel Dwyer link still blue and underlined at all three widths.

### D images and their placement
None. Every image below the list moved with its text (pure shift).

### E lists and tables
None. The three "Follow ..." items now stand 32 px apart at 1440, 768 and 390 (were 37), the page's usual together gap.

### F spacing and lines
None. space.txt (13 widths + 1279/1180/1023/960 bands) ends "RESULT: SPACING OK": no FAULT line left; build 36's 29 FAULTS are gone - the 13 "UNEVEN" lines (now every together gap at 1440 is 32 px except 630 -> 631 at 36.2, a pair in the owner's allowed file, T2) and the 4 "Follow ..." lines (now "OK together", 32 px at 640/390) are fixed by the change; the 12 image/divider lines at 640/390 are now AGREED. All 45 AGREED lines are pairs listed in tools/allowed/the-english-curriculum-space.txt (I matched each one): 627 -> 628, 628 -> 630, 630 -> 631 (T2 / gap above an image), and the phone-layout pairs 183, 219, 243, 319, 373, 455, 490, 594, 619, 645, 654, 663, 681, 683, 685. One line went from AGREED to "OK apart" (1180, 628 -> 630) - better, not a fault.

### G phone/tablet only
None counted.

Template items awaiting the owner (listed, not counted), all unchanged apart from the shift:
- 390 Writing Stages list split by the writing-strip image (w390-part25, pixel-identical to build 36).
- 390 tab-set lists (Reading Analysis / Symbol Boxes) misaligned (w390-part36-38, shift only).
- 390 gaps lost where Word's columns join ("Blue Sentence Cards" -> "Green Language Materials", "Blue Series" -> "Action Cards 2"; AGREED in space.txt).
- Word Study label list justified at 768 (w768-part23, shift only).

### H the automatic checks' findings
- strip-nolive.txt (code against template and Word): "ALL CHECKS OK (parts 1-4 and 8)", identical to build 36's apart from paths. Confirmed.
- static.txt: STATIC PASS (only the template clone HEAD line differs from build 36's; template sha256 unchanged, 64/64 template blocks unchanged).
- format-word.txt: 74 differences / 48 allowed - byte-identical to build 36's (paths aside).
- col.txt: COLUMNS OK. text.log / text/: TEXT PASS, corrections and doubts identical to build 36's.
- style.txt (= style.log, finished): 4709 FAULT lines, every one "FAULT D066/E054 ... margin-top written by 2 scripts" (430/430/430/431/433/433/425/425/424/424/424 at the 11 widths, sums to 4709); "beige lines shown 10 (template render 10)" at every width. Only the allowed D066/E054 kind (gate allowance AF001); no other rule. Not page faults.
- tablet.txt: TABLET PASS (641-830). widths13.txt: every width ok (0 oversized, squeezed, overlaps, sideways; hero ok; menus 8 panels, no faults), package hash = the zip's. wrap-early.txt: WRAP PASS (320-1920 step 40). space.log/space.txt: SPACING OK (see F).
- gate-early.txt (15:08:39): its three INTEGRITY FAULT order lines are about steps still to come (this review, more_checks.sh long, run_checks.sh), not the page.
- Build log: no WARNING lines. report.json WARNING lines unchanged from build 36 (6 "mostly white edge", 4 "heading not found in Word").

## Build 36 on build 37
| b36 | Item | On b37? |
|---|---|---|
| - | 0 faults in build 36's review | Nothing new found |
| space check | together gaps uneven (32, 37), 13 widths | Fixed (SPACING OK) |
| space check | 610 -> 611, 611 -> 612 apart on the page at 640/390 | Fixed (OK together, 32 px; seen at 390) |
| space check | 12 image/divider lines at 640/390 | AGREED by the owner's allowed file |

FAULTS: 0
