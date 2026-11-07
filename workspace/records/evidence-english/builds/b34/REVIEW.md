# Separate review - The English Curriculum (3.5.0), build 34, against the owner's PDF

- Time: Fri 6 Nov 2026 12:05-12:14 CST (from `date`)
- Build folder: /home/claude/mm/build-35/b34
- Zip: /home/claude/mm/build-35/b34/the-english-curriculum.zip, sha256 40c3f895b80e7c69a5fab31a88a8007510c63aeb175718882684d83e29486345 (from `sha256sum`; matches "40c3f895b80e7c69" in checks2/SUMMARY.txt)
- Compared: page code preview/index.html line by line against build 33's. The only changes: (a) build 33's `<style id="mm-page">` (mm-gl-full) is gone, replaced by `<style id="mm-wcols-left-6nov">main .mm-wcols2 p{text-align:left !important}</style>`; (b) the beige line before the Spoken Language shelf paragraph is back before the image float (`<p class="mm-gl">`, no mm-gl-full); (c) "with the title's" -> "with the titles" twice; (d) two `mm-grid3` lines in the set-sizing script (rows of three sized as one row of three); (e) the line-gap script now gives a line its own gap after a set whose text reaches lower than its images. (a), (d) and (e) are in the template /home/claude/mm/templates/Essay Code Template.html (saved 11:59; the code check confirms all 64 template script/style blocks unchanged). PDF (5 Nov, /home/claude/eng35/review31/pdf/ p15, p16 looked at); Word colours of the Reading headings (python-docx); checks2/ (all files there); build log /home/claude/eng35/build-b34.log; report.json (diffed with build 33's); previous reviews b33/REVIEW.md and b32/REVIEW.md.
- Screenshots: every part (w1440-part01..21, w768-part01..26, w390-part01..38) compared by pixel with build 33's and looked at by eye as contact sheets (1440 at 55 %, 768 at 60 %, 390 at 75 %). Where things moved I worked out the vertical shift along the whole page (PIL) and looked at every place it changes, at full size: 1440 part02 ("Dr. Angeline Lillard" after the classroom-photos set, 4 px up), part15 (Kate Millie title), part17 (quotation after the Grammar set, 9 px up); 768 part02, part14, part17, part19 (reading images), part20, part21 ("Action Cards - Set 1" after the Object Box 1 set, 5 px down), part22 (quotation after Grammar); 390 part07 (shelf line), part27 (reading images, Kate Millie title). 390 parts 01-06 are pixel-identical to build 33; 390 changes only by the 9 px at part07, then content identical.
- NOT checked: menu panels; links not clicked; swipe rows not swiped; widths other than 1440/768/390; full-size images and faces records; every check step after "style" (the run stopped there, see H). No browser and no check script run.
- No file changed except this report.

## Words and her rules (not faults)
- Corrections seen (for her to confirm): as in build 32/33's reviews, plus new in this build: "with the title's 'singular'" and "with the title's 'masculine'" -> "with the titles ..." (her 27 Oct typo rule; w1440-part18, w768-part23, w390-part34; code lines with `with the titles ‘<em>singular’</em>` and `‘<em>masculine’</em>`). Note: format-word.txt lists these two under rule A023 ("UK English") - the right rule is her 27 Oct typo rule; label only, the page is right.
- Quotations keep their own words, as before. Question for her (not counted, as before): "Puzzle Words（Sight Words）" full-width brackets. Grammar for her to judge (not counted, as before): the list in build 33's review.
- 104 px indent (her rule for Word's 78 pt blocks at 641 px and wider): the Object Box 1 / Action Cards 2 sequence list measures about 105 px at 1440 (w1440-part16) and about 103 px at 768 (w768-part21). Right.
- Word's green (00B050) headings show red/blue on the page (e.g. "Reading", PDF p16 green, w1440-part15 red): unchanged from earlier builds, listed by the format check as colour pairs and not counted by any earlier review; not counted here.

## Faults

### A contents box
None. Six entries as PDF p1 (w1440-part01 pixel-identical to build 33).

### B headings and text
None. Build 33 fault 1 ("title's" x2) is fixed.

### C bold/italic/colour
None new.

### D images and their placement
None counted.
- Spoken Language shelf image (build 33 fault 2): fixed. 390 (w390-part07): "Consonant Blends Sound Card" -> beige line (full width, x 24-366) -> shelf image -> "This is a photo ...", as the PDF. 1440 (w1440-part04) and 768 (w768-part04): line full width above the image and paragraph.
- Reading images in rows of three (new rule): 1440 (w1440-part15) beside the list, as before; 768 (w768-part19) now beside the list, two rows of three, list column about 213 px wide (not under 200 px, so beside is right). At 768 the image rows are centred in their column (about 76 px free to the right), at 1440 they reach the right edge; the PDF (p16) has them centred beside the list, so not a fault. 390 (w390-part27): a swipe row under the list, unchanged from build 33.

### E lists and tables
1. Lines in Word's two-column lists are still justified when they wrap, at 768 (new rule: "lines in Word's two-column lists are left-aligned at every width"). The new style only reaches paragraphs (`main .mm-wcols2 p{text-align:left !important}`), not bulleted list lines (`li`) inside `mm-wcols2`. Seen:
   - w768-part14 (PDF p13, Preparation of the mind / of the hand): "Develop   a   left   to   right   mental / orientation" and "Practise   left   to   right   muscular / orientation" spread with wide word gaps.
   - w768-part17 (PDF p15, How Parents Can Help): "Pencils:  coloured  and  lead  (triangular / are best)" spread the same way.
   The paragraph-type two-column lists (Spoken Language tables of contents, Kate Millie lists, Writing Stages, Handwriting, the 3.1-3.17 list) are left-aligned at 768 - right. The style check agrees: its 1400 "left vs justify" lines are all on `p` elements; none on these `li`.
- Kate Millie's Supplemental Language Album - Reading (build 32 fault 2, new rule): now stands apart. 1440 (w1440-part15): "Definition Stages" -> Kate Millie title 42 px (list pitch 31-32 px), title -> "3.1" 41 px; build 33 had 31-33 px. 768 (w768-part19): about 42 px. 390 (w390-part27): clear gap below the swipe row, unchanged. Fixed.
- Same rule elsewhere, looked at and right: "Dr. Angeline Lillard ..." after the classroom-photos set (1440 part02, 768 part02; now Word's 20 pt gap, 4-7 px less); "Action Cards - Set 1" after the Object Box 1 set (768 part21, 5 px more); the "Experience has shown us ..." quotation after the Grammar set (1440 part17: last line -> quotation 41 px, as every other paragraph -> quotation, e.g. w1440-part04 40 px; build 33 had 50 px).

### F spacing and lines
No counted fault. Beige lines: none through or touching letters in any part looked at; style check: "beige lines shown 10 (template render 10)" at every width, and build 32's E041 beige-line fault is gone.

### G phone/tablet only
2. 768 three-column lists still justified with wide word gaps (build 31 fault 8 named this part; the 11:59 agreement covers only Word's two-column lists, so this list is outside it). w768-part20 (PDF p17, Pink / Blue / Green Language Materials, class `mm-cols3`): "Phonogram          Sandpaper / Letters", "L.M.A.   Blue   Object   Word / Box", "Large   Pink   Picture   Word / Card", "Large   Blue   Picture   Word / Card". If she means the left-aligned exception for all of Word's column lists, the same fix covers this; if not, it stays a fault of the template's justified text in narrow columns.

Not counted, for her to look at: the Word Study label list beside the cards image at 768 (w768-part23, "Two sets of cards, the first set with / masculine words, ...") is justified in a narrow column with wide gaps; same in build 33, not reported before, and it is not a column list.

Template, awaiting the owner (not counted), all still there:
- 390 Writing Stages list split by the writing-strip image between "Writing Copies" and "Capitals" (w390-part25).
- 390 tab-set lists of Reading Analysis / Symbol Boxes misaligned ("2 very large red circles verb" with only a word space; "8 medium orange circles / extensions of / the verb", "1 black triangle / noun in / apposition" wrapping to the left margin) (w390-part36, part37, part38).
- 390 gaps lost where Word's columns join ("Blue Sentence Cards" -> "Green Language Materials", "Blue Series" -> "Action Cards 2", w390-part29, part30).
- The spacing check's UNEVEN lines: the spacing check did not run on this build (see H), so no list.

### H the automatic checks' findings
- Code against template and Word (strip-nolive.txt): "ALL CHECKS OK (parts 1-4 and 8)". Build 33 fault 3 (page-made `mm-page` style and class `mm-gl-full`) is gone - confirmed in the code. Section 5 now shows the two "title's -> titles" corrections; otherwise as build 33.
- Static: STATIC PASS (template sha256 e4c2d51f..., same as the GitHub clone).
- Format (Word): 74 differences / 48 allowed; against build 32's file only the "they" deletion and the two "titles" corrections are new - all her typo corrections, confirmed.
- Columns: COLUMNS OK. Text: TEXT PASS (corrections.txt adds "title's -> titles" x2; doubts.txt unchanged).
- Style: STYLE FAULT (6109), and the run STOPPED there at 12:10:11. By kind:
  - 1400 x D122/E015 "text-align left vs justify" (641-1920 px; 1208 `p`, 136 `p.mm-hanglab`, 56 `p.mm-hc-0432FF`, all inside `mm-wcols2`): rejected as page faults - this is the owner's agreed 11:59 exception; the style check has not been told about it yet, so it will keep stopping the run until it is.
  - 4664 x D066/E054 "margin-top written by 2 scripts" (template scripts: the base script, mm-letter-gaps-js, mm-float-captop-31oct, mm-image-gap-29oct, mm-photo40): the same kind and nearly the same count as build 32 (4637); no visible fault behind them in the screenshots; not confirmed as page faults.
  - Nothing else.
- Steps NOT finished (not run at all, SUMMARY.txt read at 12:13): tablet, widths13, wrap-early, space, full (122 widths), height, lines, place, speed and everything after style. Their findings are not in this review.
- Build log: two lines ("build guard: b33's round stopped at a fault - fix every fault found, then build b34", "zip: build-35/b34/the-english-curriculum.zip"). No WARNING lines.
- report.json: against build 33's only the text-edit lines ("changed by the user (2 found)", "with the title's ‘ -> with the titles ‘"), "image moved after the beige line before it (review b31 fault 6)" in place of the mm-gl-full line, and the b34 paths. The 10 WARNING lines (6 "mostly white edge", 4 "heading not found in Word (kept as built)") are word for word as before; nothing new to confirm.

## Build 33 faults on build 34
| b33 | Fault | On b34? |
|---|---|---|
| 1 | "title's" x2 (her typo rule) | Fixed - "titles" in code and on all three widths |
| 2 | 390 shelf image above its beige line | Fixed - line, then image, then paragraph; line full width at 1440, 768, 390 |
| 3 | code check: page-made style `mm-page` / class `mm-gl-full` | Fixed - code check ALL CHECKS OK |

Earlier template items: build 32 fault 2 (Kate Millie title at the list pitch) fixed; build 31 fault 7 (768 reading images under the list) fixed; build 31 fault 8 (768 justified narrow-column lists) fixed for two-column paragraph lists, still there for bulleted two-column lists (fault 1) and the three-column list (fault 2); build 32 faults 3, 4 and build 31 fault 9 still awaiting the owner (G).

FAULTS: 2
