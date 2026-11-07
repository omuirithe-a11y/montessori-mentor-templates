# Separate review - The English Curriculum (3.5.0), build 32, against the owner's PDF

- Time: Fri 6 Nov 2026 11:16 CST (from `date`)
- Build folder: /home/claude/mm/build-35/b32
- Zip: /home/claude/mm/build-35/b32/the-english-curriculum.zip, sha256 8f14ab732a4afce4430faabd546f2bae9d08a28078dfacfe7dfa11554e6afaaf (from `sha256sum`; matches the "8f14ab732a4afce4" in checks2/SUMMARY.txt)
- Compared: page code preview/index.html (also line by line against build 31's page code: the only changes are the AMI list titles, the beige line before the Spoken Language shelf image, five word corrections, and two gaps); every screenshot part w1440-part01..21, w768-part01..26, w390-part01..38; the PDF p1-p23 as rendered by the previous reviewer in /home/claude/eng35/review31/pdf/ (present, so not rendered again); the Word file (python-docx: words, tabs, indents, spacing); checks2/ (SUMMARY.txt, format-word.txt every line, strip-nolive.txt sections 5 and 6 compared with build 31's, static.txt, col.txt, text/, style.txt); build log /home/claude/eng35/build-b32.log; report.json (keys only); the previous review /home/claude/mm/build-35/b31/REVIEW.md.
- Measurements: pixel rows/columns read from the screenshots with PIL (no browser, no check script run).
- NOT checked: menu panels (not opened in the screenshots); links not clicked; swipe rows not swiped (only the first images visible); widths other than 1440/768/390; full-size images and faces records (not part of this brief); the checks that had not run when I finished (see H).
- No file changed except this report.

## Words and her rules (not faults)
- Corrections seen (for her to confirm): characterized/civilization(s)/colorful/memorizing/organizing/recognize/tyrannize -> UK forms; practice/practicing (verbs) -> practise/practising, the noun "practice" kept; "instills" -> "instils"; new in this build: "a quarter an hour" -> "a quarter of an hour", "help child learn" -> "help the child learn", "gaining an understanding the perspective" -> "an understanding of the perspective", "so they game doesn't" -> "so the game doesn't", "a sense of the how extensive" -> "a sense of how extensive" (strip-nolive section 5 and format-word.txt show exactly these five plus "instils"; screenshots w768-part03, part05, part06, part09, w1440-part16). – and — -> "-"; spaces round slashes removed. "tyrannized" inside the Montessori Method quotation kept (quoted words).
- Quotations: "being able write" (Secret of Childhood, w1440-part15), "the 'the writer,'" (Absorbent Mind) and "[,,,]" (Frierson) are inside quotations - quoted words stay.
- Question for her (not counted, as in build 31): the sequence list keeps "Puzzle Words（Sight Words）" with full-width brackets (w1440-part17, w768-part21, w390-part30) while the caption's bracket was corrected.
- Grammar for her to judge (not counted): "them miming the action" (PDF p19, w1440-part17), "as good or better than an adult", "an interest on I-Spy", "many of adults", "are fundamental principle", "along the word they precede", "Below are the list", "the following are the list", "pair of quotes neatly encapsulate", "give a sense".
- "motor"/"intellect" bold italic in Word show italic regular in the quotation: her quotation rule as written (as flagged in build 31).

## Faults

### A contents box
None. Six entries in two columns as PDF p1 (w1440-part01, w768-part01, w390-part01).

### B headings and text
1. Typos in her own text still uncorrected (her 27 Oct rule):
   - "so they unconsciously they absorb the shapes of the letters" (Word paragraph 294, PDF p8; w768-part09, w390-part14) - one "they" too many ("so they unconsciously absorb").
   - "Cards of a contrasting colour with the title's 'singular' and 'plural'." and "... with the title's 'masculine' and 'feminine'." (Word 683 and 685, PDF p21; w1440-part18, w768-part23, w390-part34) - "titles" (plural, no apostrophe).
   Neither is in text/corrections.txt or text/doubts.txt; TEXT PASS does not catch them.

### C bold/italic/colour
No fault. AMI list titles blue; section headings red; Pink/Blue/Green words in their colours; "Preparation of the hand" bold as PDF p12.

### D images and their placement
No fault at 1440. Image rows, sides and order as build 31 (no image code changed except the beige line moved above the Spoken Language shelf float).

### E lists and tables
2. (Build 31 fault 4, still there.) PDF p16-p17 "Kate Millie's Supplemental Language Album - Reading" (w1440-part15). In the PDF it stands at the top of p17 after an empty Word paragraph as the title of the 3.1-3.17 list. On the page at 1440 it follows "Definition Stages" at the list's own pitch: line tops 853 and 885, 32 px, the same as every item above it (Object Box 1 ... Definition Stages, 32 px each), so it still reads as an eleventh item of the AMI reading list. The code is unchanged from build 31 (`<p data-gap="29">` straight after the float holding the image grid). At 768 (w768-part19) and 390 (w390-part27) the image grid stands between them, so it is not seen there.

### F spacing and lines
No counted fault. Build 31 fault 5 is fixed: "“I Spy ... containing the sounds ....”" -> "What the child is doing here" is now 41 px at 768 (w768-part08, rows 73 -> 114) and at 1440; "Reading:" -> "Decoding:" 41 px at 1440 (w1440-part15, rows 442 -> 483) and 768.

Not counted (template spacing awaiting her, or not clearly different from the PDF):
- AMI list (PDF p2) at 1440: Sound Game -> Keys to Literacy 41 px, Movable Alphabet -> Writing Stages 42, Continuation of Commands -> Word Study 42, Word Study -> Reading Analysis 60 (the empty Word paragraph 100) - now as the PDF. Title -> first item: Keys to Literacy -> Sandpaper Letters 32, Function of Words -> Symbol Box 32, but Writing Stages -> Metal Insets 35-36 and Word Study -> Word Study 36 (code `data-gap="24"` on the latter two); Word has 0 after all four titles. A 4 px difference, listed only.
- Beige line to heading after a quotation's attribution 11-12 px, elsewhere about 44 px (as build 31; the PDF also varies).
- Blue Language Materials column 2-5 px higher than the Pink and Green columns (w1440-part16, w768-part20) - as build 31.
- Beige lines: none through or touching letters at 1440, 768 or 390.

### G phone/tablet only
3. 390, Writing Stages list (PDF p15; w390-part25). The tall writing-strip image (image 112), which stands beside the right column at 1440 and 768, stands at 390 between "Writing Copies" and "Capitals", splitting the eleven-item list in two with a 180 px image in the middle. The code puts the image float at the start of Word's second column, so when the columns join it lands mid-list. The PDF list is one block with the image beside it; on the phone the image should stand before or after the whole list. The same mechanism puts the grammar-symbols box between "Noun" and "Article" (w390-part33), which at least falls between two separate entries.
4. 390, the tab-set lists of Reading Analysis and the Symbol Boxes (PDF p21-p22; w390-part36, part37). Word's tab columns break on the phone: "2 very large red circles verb" has only a word space before "verb" while "subject"/"object" below stand at x 264; "1 blue triangle  adjunct" starts at x 216 but "1 black triangle  noun in" at x 264; wrapped lines go back to the left margin (x 24) under the 72 px indent ("the verb", "apposition", "that? what is it that?", "what?", "with whom? with what?" ...), and the Series 2 lines b.-e. wrap to x 24 under the letters ("object.", "objects.", "variety of subjects and objects."). At 1440 and 768 (w768-part25) these lists are aligned as the PDF. No phone rule covers misaligned columns.

Template, awaiting the owner (not counted):
- Build 31 fault 7 - still there: 768 reading-presentations image grid stands centred under the list, not beside it (w768-part19).
- Build 31 fault 8 - still there: 768 justified lines in Word's narrow columns open wide word gaps (w768-part04 "Sorting Middle Sounds Using Pictures Of 2", "Matching Objects to Pictures and/or to"; part14 "Develop a left to right mental", "Practise left to right muscular"; part17 "Pencils: coloured and lead (triangular", "Capital Letters, Periods, Commas, and"; part19/20 "Cursive and Print Letter", "Consonant Blends", "Phonetic Picture and", "Phonogram Matching", "Phonogram Rhyming", "Large Pink Picture Word", "L.M.A. Blue Object Word", "Large Blue Picture Word", "Phonogram Sandpaper").
- Build 31 fault 9 - still there: 390 column joins lose the gap (w390-part29 "Blue Sentence Cards" -> "Green Language Materials" at the list pitch, while "Pink Secret Box" -> "Blue Language Materials" is about 60 px; w390-part30 sequence list "Blue Series" -> "Action Cards 2" tighter than the other items).

Not counted at 390: images beside text standing above or under it (Storytelling, Materials, I-Spy list, Word Study cards, Grammar image): phone rule; text left-aligned, swipe rows with dots: phone rules.

### H the automatic checks' findings
- Build log: two lines ("build guard: b31's round stopped at a fault - fix every fault found, then build b32", "zip: build-35/b32/the-english-curriculum.zip"). No WARNING lines.
- SUMMARY (read at 11:16): code against template and Word PASS; static PASS; format (Word) first stopped at "FAULT: width 1440: insert: Word "" -> page "of"" (11:01:04), then the second fast stage at 11:04:54 lists it as "kept (passed 11:01:03)" - the summary marks a step passed whose own first run says FAULT. By eye the "of"/"the" inserts and the "the" delete are her typo corrections (confirmed, see the corrections list), not faults. format-word.txt also files "they -> the" under the UK-spelling rule A023 - the change is right, the rule label is wrong.
- format-word.txt: every other line confirmed as her rules (quotation bold italic -> italic; "Writing - Abstract" Heading bold -> template heading; "Contents" -> "contents"; full-width bracket in the caption). Colour pairs match her colour rules.
- strip-nolive.txt sections 5 and 6: identical to build 31's except the six corrections above. RESULT ALL CHECKS OK.
- col.txt COLUMNS OK; text TEXT PASS (does not catch fault 1).
- style.txt STYLE FAULT (4693), stopped the run at 11:09:37: 4682 D066 lines (the same count as build 31, code-level, nothing to confirm by eye) and 11 new E041 lines "beige line before 'This is a photo of the Spoken Language shelf' ... found before it: div.mm-float" (all 11 widths). Rejected by eye: the line now stands straight before the float that holds the shelf image beside that paragraph, full width at 1440 (w1440-part04), 768 (w768-part04 row 1364, x 40-727) and 390 (w390-part07), as the PDF p4/p5. The checker expects the line next to the paragraph itself.
- Steps NOT finished when I finished (the run stopped at style): tablet, widths13, wrap-early, space, full (122 widths), height, lines, place, speed and anything later. Their findings are not in this review.

## Build 31 faults on build 32
| b31 | Fault | On b32? |
|---|---|---|
| 1 | AMI list titles: Writing Stages, Word Study, Reading Analysis coded as headings, uneven gaps | Fixed - all `<p class="mm-hc-0432FF">`; 41/42/42 px, Reading Analysis 60 px (w1440-part02, w768-part02) |
| 2 | five typos uncorrected | Fixed - all five corrected (other typos remain: new fault 1) |
| 3 | "instills" | Fixed - "instils" (w768-part06, w390-part09) |
| 4 | Kate Millie title at the list pitch | Still there - fault 2 |
| 5 | I-Spy -> What the child, Reading: -> Decoding: gaps lost | Fixed - 41 px |
| 6 | 768 beige line after the Kate Millie Spoken Language list only 416 px | Fixed - x 40-727 (w768-part04 row 1364) |
| 7 | 768 reading grid under its list | Still there - template, awaiting the owner |
| 8 | 768 justified narrow column lists | Still there - template, awaiting the owner |
| 9 | 390 column-join gaps lost | Still there - template, awaiting the owner |

FAULTS: 4
