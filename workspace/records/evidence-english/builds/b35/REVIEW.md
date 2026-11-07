# Separate review - The English Curriculum (3.5.0), build 35, against the owner's PDF

- Time: Fri 6 Nov 2026 12:21-12:23 CST (from `date`)
- Build folder: /home/claude/mm/build-35/b35
- Zip: /home/claude/mm/build-35/b35/the-english-curriculum.zip, sha256 5349c18970cad8f745a148bc25362c95159c70e66ee9cd859a7b3d8124011c4d (from `sha256sum`; matches "5349c18970cad8f7" in checks2/SUMMARY.txt). The zip's index.html is the same as hostinger/the-english-curriculum/index.html; it differs from preview/index.html only by the copy-protection blocks (`mm-protect` style and `mm-protect-js` script), as in earlier builds.
- Compared: page code preview/index.html line by line against build 34's. The only change is one line, the style `mm-wcols-left-6nov`: build 34 `main .mm-wcols2 p{text-align:left !important}`; build 35 `main .mm-wcols2 p,main .mm-wcols2 li,main .mm-cols3 p,main .mm-cols3 li{text-align:left !important}` (comment names the owner's 11:59 and 12:15 agreements). hostinger copies of b34 and b35 differ only by the same line. report.json against build 34's: only the b35 paths. Build log /home/claude/eng35/build-b35.log. checks2/ (every file there). Previous review b34/REVIEW.md.
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 34's. Changed: 1440 parts 01, 10, 11, 17, 18, 19, 20, 21; 768 parts 14, 17, 20; 390 none (all 38 parts pixel-identical to build 34). Every changed place looked at by eye at full size (b34 and b35 crops side by side).
  - The 1440 changes are text-edge smoothing only: largest grey-level difference 17-74 of 255, at most a few hundred pixels per part, no shift (part01: menu, hero title and "Table of contents" over the hero image; parts 10-21: single pixel rows on letter edges, e.g. part20 Symbol Box 2 lists). Nothing moved; the text looks the same by eye.
  - The 768 changes are exactly the lines named in build 34's faults (see E and G).
- NOT checked: menu panels; links not clicked; swipe rows not swiped; widths other than 1440/768/390; PDF pages not re-read against unchanged parts (the words are unchanged from build 34: code and format checks identical, see H); full-size images and faces records; the browser check steps that had not finished (see H). No browser and no check script run.
- No file changed except this report.

## Words and her rules (not faults)
- Corrections seen (for her to confirm): unchanged from build 34's review (format-word.txt is word for word the same as build 34's: 74 differences, 48 allowed).
- 104 px indent for Word's 78 pt blocks at 641 px and wider: the Object Box 1 / Action Cards 2 sequence list parts (w1440-part16, w768-part21) are pixel-identical to build 34, where it measured about 105 px and 103 px. Right.
- UK spelling: no word changed in this build; "Practise left to right muscular orientation", "coloured", "colours" as before (w768-part14, part17).

## Faults

### A contents box
None. w1440-part01 changes are edge smoothing only; six entries as before.

### B headings and text
None. No word changed.

### C bold/italic/colour
None new (format check identical to build 34's).

### D images and their placement
None. No image moved at any width.

### E lists and tables
None.
- Build 34 fault 1 (bulleted lines in Word's two-column lists justified at 768): FIXED. w768-part14 (PDF p13, Preparation of the mind / of the hand): "Develop a left to right mental / orientation" and "Practise left to right muscular / orientation" now with ordinary word spaces, ragged right. w768-part17 (PDF p15, How Parents Can Help): "Pencils: coloured and lead (triangular / are best)" the same. The new style covers `li` inside `mm-wcols2`.

### F spacing and lines
None counted. No line moved (no shift in any part); beige lines as build 34.

### G phone/tablet only
None counted.
- Build 34 fault 2 (three-column Pink / Blue / Green list justified at 768): FIXED. w768-part20 (PDF p17): "Phonogram Sandpaper / Letters", "L.M.A. Blue Object Word / Box", "Large Pink Picture Word / Card", "Large Blue Picture Word / Card" now with ordinary word spaces, left-aligned. Covered by the owner's 12:15 agreement (`mm-cols3` in the new style).

Template items awaiting the owner (listed, not counted), all still present (390 is pixel-identical to build 34; 768 part23 unchanged):
- 390 Writing Stages list split by the writing-strip image between "Writing Copies" and "Capitals" (w390-part25).
- 390 tab-set lists of Reading Analysis / Symbol Boxes misaligned (w390-part36, part37, part38).
- 390 gaps lost where Word's columns join ("Blue Sentence Cards" -> "Green Language Materials", "Blue Series" -> "Action Cards 2", w390-part29, part30).
- The spacing check's UNEVEN lines: the spacing check has not run on this build (see H), so no list.
- The Word Study label list beside the cards image justified in a narrow column at 768 (w768-part23, "Two sets of cards, the first set with / masculine words, ..."): unchanged; it is not in `mm-wcols2` or `mm-cols3`, so the new style does not reach it.

### H the automatic checks' findings
- Code against template and Word (strip-nolive.txt): "ALL CHECKS OK (parts 1-4 and 8)"; the file is identical to build 34's apart from the build path. Confirmed.
- Static: STATIC PASS. Format (Word): 74 differences / 48 allowed, identical to build 34's file; all her typo corrections as before. Columns: COLUMNS OK. Text: TEXT PASS.
- Style: running when read (style.log at 12:22:53: widths 320, 390 and 640 done, each "beige lines shown 10 (template render 10)" and 430 faults, 1290 in all, all D066/E054 "margin-top written by 2 scripts" - the same template-script kind as build 34's 4664, no visible fault behind them; not confirmed as page faults). No "text-align left vs justify" lines so far (those widths are under 641); whether the 1400 such lines of build 34 are gone at 641-1920 is not yet known.
- Steps NOT finished when SUMMARY.txt was last read (12:22:53): style (in progress, widths 320, 390, 640 done; 641-1920 not yet), and not started: tablet, widths13, wrap-early, space, full (122 widths), height, lines, place, speed and everything after style. Their findings are not in this review.
- Build log: two lines ("build guard: b34's round stopped at a fault and b34 has its review - fix every fault found, then build b35", "zip: build-35/b35/the-english-curriculum.zip"). No WARNING lines.
- report.json: against build 34's only the b35 paths; the 10 WARNING lines (6 "mostly white edge", 4 "heading not found in Word (kept as built)") word for word as before; nothing new to confirm.

## Build 34 faults on build 35
| b34 | Fault | On b35? |
|---|---|---|
| 1 | bulleted lines in two-column lists justified at 768 | Fixed - w768-part14, part17 left-aligned |
| 2 | three-column Pink/Blue/Green list justified at 768 | Fixed - w768-part20 left-aligned |

FAULTS: 0
