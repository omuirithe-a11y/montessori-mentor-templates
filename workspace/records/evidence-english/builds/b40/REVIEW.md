# Separate review - The English Curriculum (3.5.0), build 40, against build 39 (after the fast round)

- Time: Fri 6 Nov 2026 19:59-20:01 CST (from `date`), after "FAST-PASSED" in checks2 and "screenshots ready 19:58:51" in /home/claude/eng35/chain40.log (no "fast round stopped").
- Build folder: /home/claude/mm/build-35/b40
- Zip: /home/claude/mm/build-35/b40/the-english-curriculum.zip, sha256 44d8c51b3d5f0b704fc2475e1cde811111634ce727906829bc3c387839c79d32 (from `sha256sum`; matches "44d8c51b3d5f0b70" in checks2/SUMMARY.txt). 328 files.
- Compared: preview/ files against build 39's by sha256: only index.html differs. Its only change: two CSS lines added in the `@media (max-width:830px)` block (`.mm-dots span` 6x6 px round, colour --rule; `.mm-dots span.on` colour --ink). Before, the spans were sized only in the 640 block, so at 641-830 the dots box was there but empty. The dots script (`dots()`, runs when width is 830 or less) is unchanged. No words, images or other styles changed. Template: static.txt shows the template sha256 c0b6a91d... -> b8bfedec... and clone HEAD 21432c8 "Template: swipe dots drawn at 641-830" - the same change in the template.
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 39's; every changed part looked at by eye.
- NOT checked: PDF renders in /home/claude/eng35/review31/pdf/ not re-read (no words or images changed, so nothing new to compare with the PDF); widths 641-830 other than 768 by eye (no screenshots); swipe rows not swiped, so the lit dot moving was not seen; menu panels; links; full-size images and faces records; the long round (not run yet). No browser and no check script run. No file changed except this report.

## The intended change
- 1440: all 21 parts pixel-identical to build 39. As intended.
- 390: all 38 parts pixel-identical to build 39. As intended.
- 768: 14 parts changed (06, 07, 08, 09, 10, 11, 12, 13, 15, 16, 18, 20, 21, 24), and in each the changed area is only a 6 px high strip of dots (28 strips, x 351-417), nothing else. Looked at by eye: each strip is a row of small round dots (first one dark, the rest light) about 8 px under a row of images that runs off the right edge (scrolls sideways); the number of dots matches the row's images (3 to 6). Rows: Reading area (6 dots), I-Spy rows (p7-p9), Sandpaper Letters (p10-p11), first sounds/letters (p12), Letter Bingo, blending (p12), p13, drawings and easels (p15), cutting/punch-pin (p16), Sandpaper/writing rows (p16, p18), Writing Stages scripts (p18), Blue/Green Series (p20), Bob Books (p21), Hole/Whole and Tide/Tied (p24).
- I also looked for any image row at 768 that touches the right edge without dots: every other block found is a single image beside text, a list image, a table image or the same row seen across a part boundary. No scrolling row without dots seen.
- Page height: no dot row added height (the dots box already had its place). w768-part26 is 798 px high (build 39: 797); its first 797 rows are identical and the extra row is beige footer background - the 1 px build 39 lost comes back (sub-pixel rounding). Not a fault.
- Observation, not counted: at 768 the dots are centred on the text column (centre about x 384), while most rows start to the right (x about 240-320), so the dots sit under the left half of the row rather than its middle. This is the same rule as on phones (`justify-content:center` on the dots box); on phones the rows fill the width so it does not show. For the owner to say if she wants them centred under the row.

## Faults

### A contents box
None (part01 identical at all three widths).

### B headings and text
None. No word changed; text: TEXT PASS, corrections.txt and doubts.txt identical apart from paths.

### C bold/italic/colour
None. format-word.txt identical to build 39's.

### D images and their placement
None. Only dots changed (see above).

### E lists and tables
None.

### F spacing and lines
None. space.txt identical to build 39's apart from the temp path ("RESULT: SPACING OK").

### G phone/tablet only
None counted.

Template items awaiting the owner (listed, not counted), unchanged (390 pixel-identical; w768-part23 identical):
- 390 Writing Stages list split by the writing-strip image.
- 390 tab-set lists (Reading Analysis / Symbol Boxes) misaligned.
- 390 gaps lost where Word's columns join.
- Word Study label list justified at 768 (w768-part23).

### H the automatic checks' findings
- strip-nolive.txt: ALL CHECKS OK (parts 1-4 and 8); only the zip path differs. Confirmed.
- static.txt: STATIC PASS; differs only in zip path, template sha256 and clone HEAD (the dots change, above).
- format-word.txt: identical (74 differences / 48 allowed).
- col.txt COLUMNS OK (only server log times differ). tablet.txt TABLET PASS (641/680/720/768/800/830). widths13.txt every width ok. wrap-early.txt identical (WRAP PASS).
- style.txt: 4704 FAULT lines (build 39: 4713), all "D066/E054 ... margin-top written by 2 scripts", the allowed kind (AF001). Beige lines shown 10 (template 10) at every width. Not page faults.
- images.txt: IMAGES PASS, 43 groups, 0 faults at every width; header still "heights only (a proof run)"; swipe/late/viewer parts left to the long round (images-2.txt missing).
- gate-early.txt: the same 40 FAULT rows as build 39's (A013, A034, A035, A046, A047, A088, B007, ... E050); all are order/missing-result rows (this review, run_checks.sh, more_checks.sh long, images-2.txt) or rows resting on them, and A046/A047/B040 list template commits without a word-for-word agreement entry - now also 21432c8 (this dots change, which cites "owner's standing agreement" without a time). A gate/records item for the main session, not a page fault.
- Build log /home/claude/eng35/build-b40.log: no WARNING lines. report.json WARNING lines identical to build 39's.

## Build 39 on build 40
| b39 | Item | On b40? |
|---|---|---|
| - | 0 faults in build 39's review | Nothing new found |

FAULTS: 0
