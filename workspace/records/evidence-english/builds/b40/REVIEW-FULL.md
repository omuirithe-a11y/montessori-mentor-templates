# Full separate review - The English Curriculum (3.5.0), build 40, zip sha256 44d8c51b3d5f0b704fc2475e1cde811111634ce727906829bc3c387839c79d32

- Time: Fri 6 Nov 2026 22:24-22:39 CST (from `date`).
- Build folder: /home/claude/mm/build-35/b40
- Zip: /home/claude/mm/build-35/b40/the-english-curriculum.zip, sha256 44d8c51b3d5f0b704fc2475e1cde811111634ce727906829bc3c387839c79d32 (from `sha256sum`; starts 44d8c51b3d5f0b70 as asked).
- Brief followed: /home/claude/mm/tools/briefs/REVIEW-BRIEF-STANDARD.md; the owner's rules from /home/claude/mm/tools/briefs/ENG-REVIEW-BRIEF.md ("The owner's rules").
- Compared: the owner's PDF p1-p23 (/home/claude/eng35/review31/pdf/p01..p23.png) page by page beside the 1440 screenshots (w1440-part01..21), then the same parts at 768 (w768-part01..26) and 390 (w390-part01..38); the Word file word by word (python-docx, all 536 non-empty paragraphs, against the text of preview/index.html <main>), plus Word colours, tabs and indents where the page differed; the page code (headings, colour classes, image structure); the template /home/claude/mm/templates/Essay Code Template.html (rules for quotations, lists, green/red headings); tools/REQUIRED-CHECKS.txt rows; tools/ALLOWED-FAULTS.txt and tools/allowed/the-english-curriculum-space.txt and the-english-curriculum-format-word.txt; the delta review b40/REVIEW.md and the last full review b32/REVIEW.md for context only.
- Measurements: pixel rows/columns read from the screenshots with PIL. No browser, no build, no check script run. No file changed except this report.
- NOT checked: widths other than 1440, 768, 390 (no screenshots); menu panels (not opened); links not clicked; swipe rows not swiped (only the first images and the dots seen); tab order and any other browser action; the live/published page (not uploaded); full-size images and the faces records; image heights not measured against their text (D329, D342, D344); the check outputs (not used in place of looking).

## Words and her rules (not faults)
- Word against page, word by word: the only differences are her rules - UK spelling (characterised, civilisation(s), colourful, memorising, organising, recognise, tyrannise; practise/practising for the verb), "instills" -> "instils", the typo corrections "a quarter of an hour", "help the child learn", "an understanding of the perspective", "so the game", "so they unconsciously absorb", "a sense of how extensive", "with the titles" (twice) (her 27 Oct rule "correct all typos"); the full-width bracket in "Puzzle Words (aka Sight Words)" (AF002); "- " before every attribution (template quotation style); the Word title line replaced by the hero title "The English Curriculum"; spaces round slashes removed ("Art/Drawing/Colouring", "language/bilingualism"). "Run", "Hug" and "Maria Montessori, 1950, Perugia." are Word text-box captions, shown as captions, as in the PDF p19. Quoted words kept ("tyrannized", "being able write", "[,,,]").
- Colours: Word's green headings Spoken Language, Writing - Abstract, Writing - Concrete, Reading, Grammar (PDF p3, p9, p12, p17, p19) are red on the page: her rule 1 Nov 10:01 "Headings are all words in the table of contents. In the table the headings are black. On the page they need to be red" (DECISIONS-LOG.md line 96). Orange quotations are black italic (her rule). Pink/Blue/Green words in their colours (w1440-part16; w768-part10 "blue/pink/green").
- Spacing differences on the allowed list are not counted (tools/allowed/the-english-curriculum-space.txt, "owner 6 Nov 13:49 (b): template rule ..." and "phone layout follows the template (owner 21 Oct rule "no questions about phones")").

## Faults

### PDF p6-p7 (The Sound Game, First / Second / Third Stage)
1. The tab before the "I Spy" quotation inside the stage lines is lost. Word paragraphs 246, 251, 254 have "... the beginning sound: \t\t"I Spy with my little eye, something beginning with ...."", "... the ending sound. \t"I Spy ..." and "... the middle sound.\t"I Spy ..."; the PDF (p6 First stage, p7 Second and Third Stage) shows the quotation pushed right to a tab stop, a wide gap after "sound:" / "sound.". The page shows only a word space or two (code: `sound:<em>  "I Spy with my little eye, something <u>beginning</u> with ...."</em>`), so the quotation runs straight on: w1440-part06/07, w768-part07 ("always identifying the beginning sound: "I Spy with my little eye..."), w390-part11/12. No owner rule I found covers a tab inside a line (D130 covers only Word's tab before a quotation's first line). If she accepts it, it is one wording item; listed so she can say.

### Not counted - template items awaiting her (as in the earlier reviews; seen again on this build)
- 390: Writing Stages list split by the writing-strip image between "Writing Copies" and "Capitals" (w390-part25); PDF p16 has the image beside one list.
- 390: Symbol Box tab lists - "2 very large red circles verb" with only a space before "verb", other labels at their column, wrapped lines back at the left margin ("the verb", "apposition", "that? what is it that?") (w390-part34, part37); Phoneme/Grapheme lines lose their column (w390-part13).
- 390: gaps where Word's columns join (e.g. "Blue Series" -> "Action Cards 2", w390-part30).
- 768: Word Study label lines justified with wide gaps ("Two sets of cards, one set with words in", w768-part23); Article/Verb text in a narrow justified column beside the grammar box (w768-part22).
- 768: swipe dots centred on the text column, not under the row (w768-part06 and others).

### Checked and found as the PDF (no fault)
- PDF p1: contents box (six entries, two columns), first paragraph. p2: AMI list in two columns, blue titles; "Reading Analysis" after a gap. p3-p4: Language-area image pair beside the text, Lillard quotation, Spoken Language lists in two columns, Time-consuming/Unnecessary, Enrichment/Expansion columns, the two alternative album lists in two columns, beige line before the shelf paragraph, shelf image beside it. p5-p6: beige lines above Circle Time, The Peace Table, after "of the adults in the room.", above The Sound Game; Storytelling image beside its text; Book Corner row of 6; Materials image beside its text; Sound Game rows of 5. p7-p8: Notes 1-6 with rows of 5/5/4/5/5 images; dash list under 6. p8-p9: Writing - Abstract, Phonemes/Phoneme/Grapheme label lines, row of 3. p9-p10: beige line, Keys to Literacy, Sandpaper Letters (graphemes), row of 4, quotation, row of 5. p10-p11: beige line, The Moveable Alphabets, numbered 1-5 with the image beside it, Dickens quotation, beige line, Reinforcement of Letters, centred "Matching first sounds..." row of 5, centred "Letter + first sound..." row of 6, Letter Bingo: learning | teaching side by side over their pairs (1440). p11-p12: Moveable Alphabets rows of 6 and 5; Writing - Concrete dictionary line; Wikipedia quotation; 1-3; dash lists in two columns; Preparation of the mind / of the hand in two columns ("Preparation of the hand" bold, as the PDF). p13-p14: beige lines above Art/Drawing/Colouring and above Cutting; drawings rows of 6, centred caption, two rows of 5; Cutting row of 5; Pinning image beside its text and row of 5; Metal Insets row of 6. p15-p16: How Parents Can Help two-column dash list; Writing Stages two columns with the strip image beside them; Handwriting two columns; row of 6; Kate Millie list in two columns; rows of 5 and 5. p17: Reading/Decoding label lines; reading list with the 3+3 grid beside it; "Kate Millie's Supplemental Language Album - Reading" now 41 px below "Definition Stages" (rows 548 -> 589 in w1440-part15; the list pitch is 32), so it no longer reads as an eleventh item; 3.1-3.17 in two columns. p17-p18: Phonetic Reading, Pink/Blue/Green Series lines in colour, row of 4, Pink/Blue/Green Language Materials in three columns (tops level, rows 627-629), Montessori Reading Systems 1-3, sequence in two columns, Object Box 1 ----> The Pink Series. bold with its two images beside. p19: Action Cards - Set 1 with Run / cards / Hug and captions beside; captions The Blue Series / The Green Series / Action Cards - Set 2 / Puzzle Words (aka Sight Words) over their images in one row; Early Readers row of 5; Grammar with the Montessori image and caption beside; two quotations. p20: Functions of Words, Noun/Article/Verb/Adjective with the symbols box beside; Presentations in two columns; quotation. p21: Word Study labels with the three card images beside; Hole/Whole... two rows of three card sets; Homophones, weakly. p22-p23: Reading Analysis, Sentences, Series 1-5 with a.-e., tray image beside; Symbol Box 1/2 tab columns (aligned at 1440 and 768); Arrows, Chart 1/2, Writing Tray., Aims, Age. Footer and hero as the template.
- 768: text justified, side images beside text where they fit, groups as swipe rows with dots. 390: text left-aligned, images above/below their text, groups as swipe rows with dots, one column for Word's columns.

## Eye rows (all 143 rows of /home/claude/eng35/b40-eye-rows-full.txt)

Rows marked FAULT (B055, B061, C110) all rest on fault 1; they are not extra faults.

| Row | Result | What I looked at / why not |
|---|---|---|
| A007 | checked | object images on beige: grammar-symbols box (w1440-part18), Reading Analysis tray (part19), Materials objects (w768-part07) have no white box round them; the white of the word cards, Hole/Whole cards and Puzzle Words grid is part of those cards, as in the PDF |
| A008 | checked | every image compared in shape with the PDF at 1440 (PDF p3-p21 beside w1440-part02..20): no image seen cut short; shapes match the PDF images at screenshot scale |
| A009 | checked | no image seen cropped against the PDF (same check as A008) |
| A015 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A025 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A026 | checked | this report: each claim names the screenshot/PDF page/code looked at; the rest marked NOT checked |
| A029 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A039 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A040 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A055 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A056 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A067 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A068 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A069 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A071 | checked | alt="" on the images (preview/index.html); her 28 Oct rule says descriptions are not needed - not a fault |
| A073 | checked | every section at 1440 (w1440-part01..21), 768 (w768-part01..26) and 390 (w390-part01..38) seen beside PDF p1-p23 |
| A080 | NOT checked | after upload: needs the published page opened in Chrome |
| A082 | checked | each image row compared with the PDF for content, order, shape, crop, turn at 1440 (e.g. Book Corner 6, Sound Game rows of 5, Sandpaper 4, Moveable Alphabet 6, Early Readers 5, Hole/Whole 6 cards): match |
| A084 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A085 | checked | this report gives evidence (file and place) for each claim; the rest marked NOT checked |
| A086 | checked | this is a separate agent's full check of build 40 (I did not make the page) |
| A089 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A093 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A095 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A096 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A099 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A100 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A101 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A104 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A105 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| A106 | NOT checked | adults seen unblurred at screenshot scale (Montessori archive images, the man in Early Readers and Notes images), but full-size images not looked at |
| A114 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A116 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A221 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A223 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A224 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| A234 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B013 | checked | contents box: six entries in two columns, Spoken Language/Writing - Abstract/Keys to Literacy | Writing - Concrete/Reading Stages/Grammar, as PDF p1 (w1440-part01, w768-part01, w390-part01 one column) |
| B022 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B023 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B055 | FAULT | one difference from the PDF not covered by a rule: fault 1 |
| B061 | FAULT | separate review at 1440, 768, 390 found fault 1 |
| B072 | checked | no image cropped in the PDF differently from the page (same look as A008) |
| B085 | checked | AMI list titles (Spoken Language, Keys to Literacy, Writing Stages, Reading Stages, Function of Words, Word Study, Reading Analysis) blue and at the text's left edge at 1440/768/390 (w1440-part02, w768-part01, w390-part01..02) |
| B087 | checked | no beige line under the album entries (w1440-part02, w768-part01) |
| B095 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B104 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B107 | checked | one-line quotations start about 48 px in at 1440 ("A necessary condition..." w1440-part11; "I Spy ... containing the sound" w768-part07) |
| B108 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B111 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B113 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B114 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B120 | checked | 768: "Letter Bingo: learning" and "Letter Bingo: teaching" each on its own line at the left edge above their row (w768-part12); 390 same (w390-part17) |
| B132 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B152 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B166 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B180 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B181 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| B205 | NOT checked | row text empty in the list (no check described); nothing to look at |
| B206 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B207 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| B209 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| C005 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| C006 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| C008 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| C088 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| C110 | FAULT | fault 1 is a difference from Word/PDF with no written rule |
| C112 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D004 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D005 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D006 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D011 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D012 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D013 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D019 | checked | screenshots looked at at every width given (1440, 768, 390); other widths have no screenshots - see NOT CHECKED in the heading |
| D020 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D022 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D030 | NOT checked | needs loading the page with late images in a browser |
| D041 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D044 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D045 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D056 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D060 | NOT checked | needs the lines check run at 8 widths; by eye at 1440/768/390 no beige line through text seen |
| D062 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D063 | checked | screenshots at 1440, 768, 390 reviewed by eye in full (this report); new checks for missed kinds are for the main session |
| D069 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D070 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D075 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D077 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D093 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D094 | NOT checked | needs the check outputs at 8 widths |
| D098 | NOT checked | READY of the independent check is the main session's record |
| D099 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D107 | checked | as B120 (w768-part12, w390-part17) |
| D109 | checked | no table (Word has 0 tables; page has none); nothing to compare |
| D114 | NOT checked | browser action: swipe rows not swiped (screenshots show only the first images) |
| D121 | NOT checked | menu panel not opened in the screenshots (browser action) |
| D123 | checked | no line round any quotation at 1440/768/390 |
| D126 | checked | as B107 |
| D130 | checked | quotation first lines start 48 in (e.g. "Now the hand can be prepared" w768-part10, "The so-called free drawing" w768-part14); Word's extra tab before quotations not shown |
| D134 | checked | black headings (Presentations, Sentences, Circles, Arrows, Chart 1, Aims, Age) have no line under them (w1440-part18..21) |
| D138 | checked | label lines (Noun/Article/Verb/Adjective, Word Study labels, Series 1-5, Reading:/Decoding:, Phoneme/Grapheme) in a label column at 1440 and 768 (w1440-part18..19, w768-part19, part22, part23) |
| D140 | checked | no image turned or cropped differently from Word (as A082); numbered lists: Notes 1-6 continue 1..6 across the image rows (w768-part07..09), as the PDF |
| D155 | checked | images beside text float where the PDF has them (Language area pair, shelf, Storytelling, Materials, I-Spy list, Pinning, Writing Stages strip, Object Box pair, Action Cards, Grammar image, grammar box, word cards, tray); rows between paragraphs as the PDF (1440 parts 02-20 beside PDF p3-p21) |
| D170 | checked | each attribution follows its quotation's last line with no extra gap (all quotations at 1440 and 768) |
| D195 | checked | contents box as B013 |
| D197 | checked | numbered lists: number at the left margin, text after it (Peace Table 1-3, Notes, sequence 1-5, three key points, reading systems 1-3) at 1440/768/390 |
| D199 | checked | footer quotation: 1440 three lines with "It was as if..." starting line 3 (w1440-part21); 768 "prostrated me. It was as if..." on line 3, no word alone (w768-part26); 390 no word standing alone (w390-part38) |
| D206 | checked | quotations not offset (left edge = text edge); first lines 48 (as D130) |
| D219 | NOT checked | no pair of two upper images over one lower image on this page; nothing to compare |
| D294 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D295 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D297 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D298 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D300 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D301 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D312 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D313 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D314 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D315 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D317 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| D320 | checked | reading-presentations grid of 3+3 beside its list (w1440-part15) spaced closely, as the template |
| D322 | checked | column lists read down then next column (AMI list, Kate Millie 3.1-3.17, Writing Stages, Handwriting, Pink/Blue/Green) at 1440 and 768 |
| D325 | checked | no image visibly trimmed against the PDF |
| D326 | checked | the PDF has no quotation with an image beside it; quotations stand full width as in the PDF |
| D329 | NOT checked | no single image marked data-fit=width identified by eye; not measured |
| D330 | checked | reading grid (3+3) beside its 10-line list at 1440, vertically about centred on the list (w1440-part15 grid rows 264-528 beside list 252-560) |
| D331 | checked | Word's columns level at the top (Pink/Blue/Green column first lines within 2 px, w1440-part16 rows 627-629; AMI list; Enrichment/Expansion); next block below the longest column; on phones one column (w390-part04, part29) |
| D334 | checked | text beside margin images wraps round them, no empty band (Storytelling, Materials, Pinning, Object Box 1, Action Cards at 1440 and 768) |
| D340 | checked | lines above side images run full width (e.g. I-Spy list above, w1440-part09) |
| D342 | NOT checked | side-image heights not measured against their text blocks |
| D344 | NOT checked | not measured |
| E007 | checked | this report has the table |
| E009 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| E010 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| E011 | NOT checked | needs the check results (code vs template, format) - not given to me |
| E013 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| E020 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| E021 | NOT checked | faces records and full-size images not part of this review (screenshots only; at screenshot scale the children's faces seen are blurred) |
| E033 | checked | this report says image throughout (the page's own text "photo" is hers) |
| E034 | NOT checked | process or record row: about how the work was done (chat, records, delivery), not visible on the built page or its screenshots |
| E035 | checked | 390 screenshots w390-part01..38 looked at: each element present in phone form; template items awaiting her listed (not counted) |
| E052 | checked | no beige line through text at 1440/768/390 (lines above Circle Time, Peace Table, Book Corner, Sound Game, Keys to Literacy, Moveable Alphabets, Reinforcement, Art/Drawing, Cutting all clear of letters) |

FAULTS: 1
NOT CHECKED: 97
