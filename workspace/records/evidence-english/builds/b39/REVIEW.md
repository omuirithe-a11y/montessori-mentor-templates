# Separate review - The English Curriculum (3.5.0), build 39, against build 38 and the owner's PDF (after the fast round)

- Time: Fri 6 Nov 2026 18:30-18:33 CST (from `date`), after "FAST CHECKS PASSED 18:28:00" in checks2/SUMMARY.txt and "screenshots ready 18:30:26" in /home/claude/eng35/chain39.log (no "fast round stopped").
- Build folder: /home/claude/mm/build-35/b39
- Zip: /home/claude/mm/build-35/b39/the-english-curriculum.zip, sha256 293cf352283f51e6cc823e7844761b8a2b5ca4124a15058ca8ed09538733ecec (from `sha256sum`; matches "293cf352283f51e6" in SUMMARY.txt). 328 files.
- Compared: page code against build 38's. The only change is in the image-sizing script: (1) a fixed-size group (`data-h`, class mm-col) that drops under its text gets height 180 px from 641 to 830 px wide (was its own height H0); (2) a group that stacks under its text (mm-stack) gets H = 180 from 641 to 830 px. Both still capped by the column width ((W - G) / sum of ratios), so "as wide as the column allows". No words, images or styles changed.
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 38's; every changed part looked at by eye.
- NOT checked: widths 641-830 other than 768 by eye (no screenshots there; the change there is known only through the checks, see H); PDF renders not re-read (no part at 1440/768/390 changed, so nothing new to compare); menu panels; links not clicked; swipe rows not swiped; full-size images and faces records; the long checks (more_checks.sh long, run_checks.sh), not run yet. No browser and no check script run. No file changed except this report.

## The intended change
- 1440: all 21 parts pixel-identical to build 38. As intended.
- 390: all 38 parts pixel-identical to build 38. As intended.
- 768: parts 01-25 pixel-identical; part26 is 797 px high instead of 798 - its first 797 rows are identical, only the last row of the footer background (beige) is gone, i.e. the page ends 1 px shorter. Looked at by eye (quotation band, footer, "Back to top"): the same as build 38. A sub-pixel rounding of the page height, not a visible change; the groups at 768 still stand beside their text. Not a fault.
- 641-830: space.txt shows the change at 641: a new "image to image" row (Definition Stages -> Kate Millie's Supplemental Language Al..., 24.0 px, OK) - a group now dropping under its text at 180 px. images.txt: 43 groups measured, 0 faults at 641, 650 ... 830; tablet.txt TABLET PASS at 641/680/720/768/800/830. Not seen by eye.

## Faults

### A contents box
None (part01 identical at all three widths).

### B headings and text
None. No word changed.

### C bold/italic/colour
None. format-word.txt identical to build 38's.

### D images and their placement
None at 1440, 768, 390 (pixel-identical). 641-830 not seen by eye (checks pass).

### E lists and tables
None.

### F spacing and lines
None. space.txt: "RESULT: SPACING OK", 45 AGREED lines (as build 38). Other differences: "41.0"/"41" print form only; "Notes -> What I've described" at 640 and 390 reads 36.0 (build 38: 35.2) - this value has swung 35.2/36.0 across builds 30-39 with no page change, and the 390 screenshots are pixel-identical, so it is measuring noise, not a page change.

### G phone/tablet only
None counted.

Template items awaiting the owner (listed, not counted), unchanged (390 and 768 pixel-identical to build 38):
- 390 Writing Stages list split by the writing-strip image.
- 390 tab-set lists (Reading Analysis / Symbol Boxes) misaligned.
- 390 gaps lost where Word's columns join.
- Word Study label list justified at 768 (w768-part23).

### H the automatic checks' findings
- strip-nolive.txt: ALL CHECKS OK (parts 1-4 and 8); only the zip path differs from build 38's. Confirmed.
- static.txt: STATIC PASS. Differs from build 38 in the template sha256 (03e939d4... -> c0b6a91d..., same in /home/claude/mm/templates and the GitHub clone) and the clone HEAD (71260c7e -> 0e9d2b89): the template itself was updated (SUMMARY.txt: "template changed"). Noted, not a page fault.
- format-word.txt: identical to build 38's (74 differences / 48 allowed).
- col.txt COLUMNS OK (only server log times differ); text: TEXT PASS, corrections.txt and doubts.txt identical apart from paths.
- style.txt: 4713 FAULT lines (build 38: 4712), every one "D066/E054 ... margin-top written by 2 scripts", the allowed kind (AF001); differences are extra margin values at 1024 from the letter-gaps script. Not page faults. Beige lines shown 10 (template 10) at every width.
- images.txt: IMAGES PASS, 43 groups, 0 faults at every one of the 122 widths. Note its header: "PARTS RUN: heights only (a proof run - not a full check)"; swipe, late-loading and viewer parts are left to the long round (gate-early lists images-2.txt missing).
- tablet.txt TABLET PASS; widths13.txt every width ok; wrap-early.txt identical (WRAP PASS); space.txt SPACING OK.
- gate-early.txt: integrity faults 3, all "order" lines (this review, run_checks.sh, more_checks.sh long not yet run) and the rows resting on them (A013/A034/A035 waiting for images-2.txt) - not the page.
- Build log /home/claude/eng35/build-b39.log: no WARNING lines. report.json WARNING lines identical to build 38's.

## Build 38 on build 39
| b38 | Item | On b39? |
|---|---|---|
| - | 0 faults in build 38's review | Nothing new found |

FAULTS: 0
