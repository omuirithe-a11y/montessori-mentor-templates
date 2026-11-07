# Separate review - The English Curriculum (3.5.0), build 38, against the owner's PDF (after the fast round)

- Time: Fri 6 Nov 2026 16:34-16:40 CST (from `date`), after "FAST CHECKS PASSED 16:31:55" in checks2/SUMMARY.txt and "screenshots ready 16:34:23" in /home/claude/eng35/chain38.log (no "fast round stopped").
- Build folder: /home/claude/mm/build-35/b38
- Zip: /home/claude/mm/build-35/b38/the-english-curriculum.zip, sha256 d91ba5ac23103e0b8959f306a5fc8f08c13a8547d1092e068d30b34ac4494d37 (from `sha256sum`; matches "d91ba5ac23103e0b" in SUMMARY.txt). 328 files. The zip's index.html (sha256 e2d752b1...) is byte-identical to hostinger/the-english-curriculum/index.html.
- Compared: page code against build 37's (split at tags). The only change is in the script `mm-float-captop-31oct`: (1) a side image followed by a list is now levelled with the list's first item (as with a paragraph); (2) an image may also move up, so long as its margin stays 0 or more. Nothing else in the page changed (no words, images or styles).
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 37's, then the full pages stitched and matched row by row and in 40-row windows (left and right halves apart), and every changed part looked at by eye.
- PDF render /home/claude/eng35/review31/pdf/p10.png (the I-Spy list and its image). Every file in checks2/ read (see H).
- NOT checked: menu panels; links not clicked; swipe rows not swiped; widths other than 1440/768/390 by eye (others only through the checks); unchanged parts not re-read against the PDF (words and format unchanged, see H); full-size images and faces records; the long checks (more_checks.sh long, run_checks.sh), which have not run yet. No browser and no check script run. No file changed except this report.

## The intended change - image 052 beside "I-Spy, Sandpaper Letters ..."
- 1440 (part09): image moved up 8 px (top 443 -> 435). The capitals of "I-Spy" start at row 435: now exactly level. Before it sat 8 px low.
- 768 (part11): image moved down 7 px (top 624 -> 631). The capitals of "I-Spy" start at row 631: now exactly level. Before it stood 7 px high. Because the image is taller than the list, the quotation and everything below it moved down 7-8 px with it (gap image -> quotation unchanged, 39 px); a pure shift, nothing else moved relative to its neighbours.
- 390: pixel-identical to build 37 (side images are not floated on phones).
- PDF p10: the image's top is level with "1. I-Spy" - the page now follows it.

## Every other side image
- 1440: below part09 y603 everything moved up 0-1 px (sub-pixel; the list -> quotation gap went 41.5 -> 41.0 in space.txt). In every 40-row window, text and images moved by the same amount (within 1 px rounding); no side image moved relative to its text. Looked at by eye: part12 (image rows), part13 (Pinning image, Metal Insets row), part17 (Object Box, Action Cards, Grammar images), part18 (Word Study images) - the same as build 37.
- 768: everything after image 052 moved down 7-8 px together; where the left and right halves differ it is by 1 px only (sub-pixel rounding: part19 3.x number table, part20 label columns, part23 Word Study) - looked at by eye, no image moved for the worse.
- 390: no change anywhere.

## Faults

### A contents box
None (part01 identical at all three widths).

### B headings and text
None. No word changed.

### C bold/italic/colour
None. format-word.txt identical to build 37's.

### D images and their placement
None. Image 052 is now level with "I-Spy" at 1440 and 768 (was 8 px low / 7 px high); no other image moved relative to its text.

### E lists and tables
None.

### F spacing and lines
None. space.txt: "RESULT: SPACING OK", no FAULT line, 45 AGREED lines (as in build 37); only page gaps changed by 0.5 px (sub-pixel), all still "OK".

### G phone/tablet only
None counted.

Template items awaiting the owner (listed, not counted), unchanged apart from the shift:
- 390 Writing Stages list split by the writing-strip image (390 pixel-identical to build 37).
- 390 tab-set lists (Reading Analysis / Symbol Boxes) misaligned.
- 390 gaps lost where Word's columns join (AGREED in space.txt).
- Word Study label list justified at 768 (w768-part23, shift only).

### H the automatic checks' findings
- strip-nolive.txt: "ALL CHECKS OK (parts 1-4 and 8)", identical to build 37's. Confirmed. (SUMMARY.txt shows a first refusal at 16:20:27 - "no proof on a deliberately broken copy" - then a clean re-run at 16:21:05 that passed.)
- static.txt: STATIC PASS; only the template clone HEAD line differs from build 37's.
- format-word.txt: 74 differences / 48 allowed - identical to build 37's.
- col.txt COLUMNS OK; text: TEXT PASS, corrections.txt and doubts.txt identical to build 37's (paths aside).
- style.txt: 4712 FAULT lines (build 37: 4709), every one "D066/E054 ... margin-top written by 2 scripts", the allowed kind (AF001). The 3 new lines are image 052's float at 641, 768 and 830 - now written by the levelling script, as the change intends. Not page faults. Beige lines shown 10 (template 10) at every width.
- tablet.txt TABLET PASS; widths13.txt every width ok; wrap-early.txt WRAP PASS; space.txt SPACING OK.
- gate-early.txt: GATE FAILED only on its three INTEGRITY FAULT order lines (this review, more_checks.sh long, run_checks.sh not yet run) and the gate rows that rest on them - not the page.
- Build log /home/claude/eng35/build-b38.log: no WARNING lines. report.json WARNING lines identical to build 37's.

## Build 37 on build 38
| b37 | Item | On b38? |
|---|---|---|
| - | 0 faults in build 37's review | Nothing new found |
| - | image 052 8 px below "I-Spy" at 1440, 7 px above at 768 | Fixed (level) |

FAULTS: 0
