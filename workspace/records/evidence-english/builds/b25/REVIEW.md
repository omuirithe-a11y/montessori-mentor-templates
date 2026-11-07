# Separate review - The English Curriculum, build 25

- Time: Fri 6 Nov 2026 05:44 CST (from `date`)
- Build folder: /home/claude/mm/build-35/b25
- Zip: /home/claude/mm/build-35/b25/the-english-curriculum.zip, sha256 c5dddc16146add8c758da9e5ceca61eeb80da81e6b4c36998f6529ee37316164 (confirmed, starts c5dddc16146add8c)
- Compared: page code preview/index.html; full-page screenshots w1440-part01-21, w768-part01-31, w390-part01-33 (all looked at); the PDF "3.5.0 The English Curriculum.pdf" p1-p23 (rendered again at 90 and 200 dpi to read small text); the Word file (python-docx, every word, every paragraph's colour/bold/italic/indent); the Essay Code Template; tools/REQUIRED-CHECKS.txt eye rows (/home/claude/eng35/eye-rows-b25-full.txt, 143 rows); her rules (memory preferences.md, records/DECISIONS-LOG.md, records/DECISIONS-LOG-3-nov.md).
- Live comparison: not applicable (this page has no live version).
- No check output was used in place of looking. No file changed except this report.

## Words (Word file against the page, every word)
All words of the Word file are on the page, in order. The only differences, each excused by her written rule:
- UK spellings (characterised, practise, civilisation, recognise, tyrannise, colourful, memorising, organising): preferences "always UK English on the site" (13 Oct) and "USE BRITISH ENGLISH IN ALL INSTANCES" (26 Oct). Spellings inside quotations kept ("tyrannized" in the Montessori Method quotation) per her 26 Oct 15:57 words "do not change ... words inside a quotation".
- – and — shown as "-": preferences "short dashes only, everywhere on the site".
- Spaces round slashes removed ("me/choose", "Art/Drawing/Colouring", "language/bilingualism"): preferences "no spaces around a slash".
- "Table of Contents" shown as "Table of contents": preferences "the label above the contents list reads 'Table of contents'".
- Full-width bracket in the caption "Puzzle Words (aka Sight Words)": row AF002, her 6 Nov 00:19 agreement "the corrected full-width bracket".
- The dashes before attributions ("- Maria Montessori") are Word's list dashes, shown in the PDF (p9, p11, p12...).
- Word's duplicate text-box copies (Run/Hug, the Perugia caption) appear once on the page, as in the PDF.

## Faults (grouped by PDF page)

1. PDF p1/p3 - contents box and "Spoken Language" heading (code: index.html; w1440-part01, part02). The contents entry "Spoken Language" links to `id="toc-spoken"`, which is on the red list title "Spoken Language" above "Nomenclature Cards" (Word paragraph 171, PDF p4), not on the section heading "Spoken Language" (Word paragraph 124, PDF p3). That section heading stays green while the other five contents headings are red. Her rule 1 Nov 10:01: "Headings are all words in the table of contents ... On the page they need to be red" - the contents heading should be the PDF p3 one, in red.
2. PDF p2 - AMI list titles (w1440-part01, part02). "Spoken Language" (left column top), "Reading Stages" (right column top) and "Function of Words" are blue in the Word file (colour 0000FF, paragraphs 43, 78, 89) and in the PDF; the page shows them black (`<p data-space="29">Spoken Language</p>`, `<p data-space="20">Reading Stages</p>`, `<p data-gap="20">Function of Words</p>`). The PDF also has a blank space before "Keys to Literacy" and before "Function of Words" (as before "Writing Stages" and "Word Study"); the page has none (Sound Game to Keys to Literacy 27 px, smaller than the 32 px between list lines).
3. PDF p4 - attribution "- Maria Montessori, The 1946 London Lectures, p. 77." (w1440-part03). On the page it starts 95 px in (x 245), where every other attribution starts 48 px in (x 198). In the PDF it stands nearer the margin than the others (about 18 px in, against 45 px for the p5 attribution). No rule excuses it.
4. PDF p6 - beige line through text (w1440-part05, pixel rows 696-697). At 1440 the beige line after the Peace Table paragraph runs through the tops of the letters of "In the environments I have prepared, ..." (55 and 40 dark letter pixels on the two line rows). Not at 768 or 390.
5. PDF p10, p15, p18 - uneven gaps inside lists (1440). PDF p10 list: item 3 to item 4 is 28 px on the page, the others 33 (w1440-part09). PDF p15 Writing Stages second column: "Punctuation" to "Written Question Game" 26 px, others 32 (part14). PDF p18 Pink Language Materials: "Pink Booklet" - "Puzzle Words" - "Pink Phrase Cards" 32 px, the others 41 (part16). The PDF shows each list evenly spaced.
6. PDF p18 - "I use a mixture ... sequence of presentations:" list (w1440-part16/17). Word paragraphs 615-619 have a left indent of 1560 twips (about 104 px) and the PDF shows both columns indented (first column at about 1.3 in from the margin); the page starts the first column at the margin.
7. PDF p19 - Grammar image caption (w1440-part17; w390 sheet part28; w768 part25). The PDF puts "Maria Montessori, 1950, Perugia." under the image; the page puts it above the image at every width.
8. PDF p22 - Reading Analysis lettered lines a.-e. (w1440-part19). Word paragraphs 719-727 have a first-line indent of 720 twips (48 px) and the PDF shows "a." indented; the page puts "a." at the margin (x 150), text at 198.
9. PDF p2, p3, p4, p12, p15, p16, p17, p18, p20 - Word's columns at 768 (w768 parts 01-27). At 768 every two- and three-column list staircases: the second column starts only where the first column ends (e.g. "Reading Stages ... Continuation of Commands" starts beside the end of "Presentation and Storage of Work"; "Expansion of Oral Language", "Sorting Middle Sounds...", "Alphabet Books...", "make continuous strokes", "Preparation of the hand", "Crayons", "Upper and Lowercase Letters", "Writing Practice Series - The Alphabet", "3.10...", "Blue/Green Language Materials", "Action Cards 2", "Preposition"). The PDF has the columns side by side and level. Row D331: "the second column starts level with the first"; her 5 Nov 13:38 agreement ("a list that opens a column of Word's columns starts level with the other columns"). In the narrow columns the justified list lines also open wide word gaps ("Consonant      Blends", "Phonogram      Sandpaper").
10. PDF p3, p5, p10, p14, p16, p18, p19, p20, p21 - images beside text at 768 (w768 parts 03-27). At 768 the images the PDF puts beside the text on the right (Language area pair, Spoken Language shelf, Storytelling, Materials, I-Spy list image, Pinning, the reading-list grid, Object Box 1 pair, Grammar image, grammar-symbols box, Word Study cards) stand above or below the text, at the left or centred; the grammar-symbols box stands between "Noun" and "Article". The text beside them would be over 300 px wide. Her 5 Nov 09:16 agreement: "images beside text move under the text only when the text would be narrower than 200 px, at 641 px and wider".
11. PDF p19 - captions of the row "The Blue Series / The Green Series / Action Cards - Set 2 / Puzzle Words (aka Sight Words)" at 768 (w768-part25, zoomed). The swipe row shows the images with no captions above them; at 1440 and 390 the captions show.

Checked and excused (not faults): section headings "Writing - Abstract", "Writing - Concrete", "Reading", "Grammar" green in Word/PDF, red on the page - her 1 Nov 10:01 rule quoted in fault 1. Orange quotation text black on the page - preferences "orange text in Word always shows as regular black on the page". "Synonyms" in the label column though the PDF has no gap - her 5 Nov 04:37 agreement (label column "for lines made of a label and its text"). "Letter Bingo" titles on two lines at 768/390 - row B120. Two-column grids level at 1440 - her 5 Nov 13:38 agreement. Image sizes (e.g. the Writing Stages strip, 27 x 120 px, beside the columns as in PDF p15) - preferences "placement follows the source PDF roughly, sizes follow the template" (row A011).

## Kinds of check (summary)
| Kind | Result |
|---|---|
| words | checked - all present; differences excused (above) |
| headings / kinds of line | checked - faults 1, 2 |
| columns | checked - 1440 level; fault 9 at 768 |
| image groups / rows | checked - every row's count matches the PDF at 1440 |
| image side / position | checked - faults 7, 10 |
| which image is in each place | checked - matches the PDF at 1440 |
| captions | checked - faults 7, 11 |
| line breaks | checked at 1440 against the PDF; no forced break missing (Fourth/Fifth Stage quotes on own lines, Writing Tray on own line) |
| bullets / numbers | checked - dashes and numbers as the PDF; numbering continues |
| indents / tabs | checked - faults 3, 6, 8 |
| alignment by width band | checked - justified at 1440 and 768, left at 390; centred captions/titles centred at 1440 |
| beige lines | checked - same places as the PDF (p4, p5, p6 x3, p9 x2, p10, p13 x2); fault 4 |
| together / apart / blank lines | checked - faults 2, 5 |
| contents box | checked - entries/columns as PDF p1; fault 1 (link target) |
| bold / italic / underline / colour | checked - fault 2 (colour); others match the Word file/PDF |
| hero and title | checked - hero image with "The English Curriculum" at 1440/768/390 |
| template sizes, spacing, fonts, colours | checked by eye only (not measured) |
| menu and footer | checked - menu bar and footer "© 2026 Montessori Mentor", band quote in three lines; menu panels not opened (NOT checked) |
| links | checked by eye - all PDF links present and blue/underlined as Word; not clicked |
| images of children blurred | checked - by eye and the records (rows A067, C008) |
| phone layout (390) | checked - fault 7 also at 390 |
| tablet layout (768) | checked - faults 9, 10, 11 |

## Eye rows (all 143 rows of /home/claude/eng35/eye-rows-b25-full.txt)
| Row | Result | What I looked at |
|---|---|---|
| A007 | checked | object images (grammar symbols box, Reading Analysis material, word cards) at 1440/768/390: no white surround on the beige page; the word-card images are white cards, as in the PDF p21 |
| A008 | checked | every image row at 1440 compared with the PDF thumbnails p3-p22: each shows the same whole frame as the PDF |
| A009 | checked | no image on the page is cut more than the PDF shows (compared at 1440 with PDF p3-p22) |
| A015 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A025 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A026 | checked | this report: every claim names the screenshot, PDF page, Word paragraph or file it came from |
| A029 | NOT checked | needs her image-review answers, not given to me |
| A039 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A040 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A055 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A056 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A067 | checked | records /home/claude/mm/build-35/faces/review2.json (round 1 words 5 Nov 09:31, round 2 "approved" 10:04) and pixel-check-after-answer.json ("pass": true, 104 images); by eye every classroom child face in the 1440/768/390 screenshots is blurred |
| A068 | checked | by eye: adults (e.g. Early Readers image 149, Sandpaper Letters image of the guide) and the historical images (Montessori with child, Perugia 1950) are not blurred |
| A069 | checked | review2.json: round1_words (her 5 Nov 09:31 answer) and round2 words "approved" 5 Nov 10:04 |
| A071 | checked | nothing required; images have alt="" in the code, which the rule allows |
| A073 | checked | whole page looked at 1440 (21 parts), 768 (31 parts), 390 (33 parts) beside PDF p1-p23, section by section; faults are listed above |
| A080 | NOT checked | no published/live page for this build (task: no live version); only screenshots given |
| A082 | checked | each image row at 1440 compared with the PDF for content, order, shape, crop and turn: all match (positions/captions faults listed separately) |
| A084 | NOT checked | needs her messages, not given to me |
| A085 | checked | this report: evidence given for each claim; the rest marked NOT checked |
| A086 | checked | this report is the separate agent check (its result is FAULTS: 11, see B061) |
| A089 | NOT checked | no published page |
| A093 | NOT checked | the full-size originals and blurred copies were not compared by me |
| A095 | NOT checked | not looked for image by image |
| A096 | NOT checked | faces sheets not given to me |
| A099 | checked | by eye at screenshot size: every blurred face is covered, soft-edged, of even strength (1440 parts 05-17, 390 parts) |
| A100 | checked | records: round 1 answer 5 Nov 09:31, round 2 "approved" 10:04, pixel check pass 10:33 (pixel-check-after-answer.json), all before build 25 (changes.txt, 6 Nov 02:5x) |
| A101 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A104 | checked | by eye: blurred faces still read as faces, not blank patches (e.g. 1440 part06, part07) |
| A105 | NOT checked | faces sheets not given to me |
| A106 | checked | by eye: no adult face blurred (Early Readers, Sandpaper Letters, Notes images) |
| A114 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A116 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A221 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A223 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A224 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| A234 | NOT checked | about the Parents pages, not this page |
| B013 | checked | contents box at 1440/768/390: two columns of three entries, same order as PDF p1 (link-target fault listed as fault 1, row D195) |
| B022 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B023 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B055 | checked | FAULT - screenshots compared with the PDF: 11 differences (faults 1-11) |
| B061 | checked | FAULT - this review at 1440, 768, 390 finds 11 faults |
| B072 | checked | crops compared with PDF thumbnails at 1440: same crops |
| B085 | checked | no open-and-close album lists on this page (none in the code, none in the screenshots) |
| B087 | checked | no album lists on this page |
| B095 | NOT checked | faces sheets and their checks not given to me |
| B104 | checked | by eye every classroom child face blurred in all three widths; records as A067 |
| B107 | checked | one-line quotations (Dickens, part09; Montessori p.96, part11) start 48 in at 1440 |
| B108 | checked | pixel-check-after-answer.json "pass": true, 5 Nov 10:33 |
| B111 | NOT checked | no failed pixel check in the records given |
| B113 | NOT checked | byte comparison not made by me |
| B114 | NOT checked | faces pages not given to me |
| B120 | checked | Letter Bingo: learning / teaching at 768 and 390: each on its own line at the left edge (w768-part13 area) |
| B132 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B152 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B166 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B180 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B181 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| B205 | checked | FAULT - eye part: screenshots at 1440/768/390 show faults 1-11 |
| B206 | NOT checked | faces sheets not given to me |
| B207 | NOT checked | faces sheets not given to me |
| B209 | NOT checked | not looked at full size |
| C005 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| C006 | NOT checked | faces sheets not given to me |
| C008 | checked | pixel-check-after-answer.json: pass true, faults [] (104 images, 267 blurred faces) |
| C088 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| C110 | checked | FAULT - differences from the Word/PDF not covered by her written rules: faults 1-11 |
| C112 | checked | the brief tools/briefs/REVIEW-BRIEF-STANDARD.md says "The template ... never excuses" column/row/side/order differences |
| D004 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D005 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D006 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D011 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D012 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D013 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D019 | checked | screenshots looked at for 1440, 768 and 390 (all parts) |
| D020 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D022 | NOT checked | check outputs not given to me |
| D030 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D041 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D044 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D045 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D056 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D060 | checked | FAULT - fault 4: beige line through the tops of "In the environments I have prepared..." at 1440 (w1440-part05, rows 696-697) |
| D062 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D063 | NOT checked | screenshots reviewed by me; whether a new check exists per missed kind is not mine to see |
| D069 | checked | my brief gave only the build, template, Word/PDF, rules, checks list |
| D070 | checked | this report lists every row NOT checked |
| D075 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D077 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D093 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D094 | checked | the line fault (D060) was confirmed by looking at the pixels, w1440-part05 rows 696-697 |
| D098 | checked | FAULT - this independent check is done and is not READY (11 faults) |
| D099 | NOT checked | no preview link given to me |
| D107 | checked | as B120 |
| D109 | checked | no tables on this page (0 <table> in the code; label lines use the hanging-label style) |
| D114 | NOT checked | swiping not possible in still screenshots; the first image of each swipe row stands in the middle at 768/390 |
| D121 | NOT checked | menu panels not opened in the screenshots |
| D123 | checked | no border round any quotation at 1440/768/390 |
| D126 | checked | as B107 |
| D130 | checked | quotation first lines 48 in at 1440 (e.g. part08, part11); the template has no paragraph first-line indent and the PDF shows none |
| D134 | checked | black bold headings (Presentations, Sentences, Circles, Arrows, Chart 1/2, Aims, Age) have no line under them |
| D138 | checked | label column used for Phoneme/Grapheme, Reading:/Decoding:, Noun/Article/Verb, Number...Word Families, Series 1-5 at 1440 |
| D140 | checked | Notes list numbering 1, 2, 3, 4, 5, 6 continues across the image rows (1440 parts 06-07); no turned image differs from the PDF |
| D155 | checked | FAULT - faults 7 and 10: Grammar caption above its image; at 768 images beside text moved above/below the text |
| D170 | checked | each attribution follows its quotation with no extra gap at 1440 |
| D195 | checked | FAULT - fault 1: the contents entry "Spoken Language" jumps to the list title on PDF p4, not to the section heading on PDF p3 |
| D197 | checked | numbered lists at 1440: number at the margin, text about 24-25 px after it (Peace Table, Notes, I-Spy list) |
| D199 | checked | footer quotation at 1440 in three lines; at 390 no word stands alone |
| D206 | checked | as D130 |
| D219 | checked | no pair-over-single image group on this page |
| D294 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D295 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D297 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D298 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D300 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D301 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D312 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D313 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D314 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D315 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D317 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| D320 | NOT checked | grid gaps not measured |
| D322 | checked | column lists read downward (first column then second) at 1440, as the PDF |
| D325 | checked | no image visibly trimmed against the PDF |
| D326 | checked | no quotation stands beside an image in the PDF |
| D329 | NOT checked | which images carry data-fit=width not checked |
| D330 | checked | FAULT - at 768 the image grid beside the reading-presentations list (PDF p16) stands below the list (w768 sheet 19, third part); at 1440 it is beside the list |
| D331 | checked | FAULT - fault 9: at 768 every Word column grid staircases (second/third column starts where the first ends) |
| D334 | checked | at 1440 no empty band beside a margin image (Materials, Storytelling, Pinning); at 768 see fault 10 |
| D340 | NOT checked | not measured |
| D342 | NOT checked | not measured |
| D344 | NOT checked | not measured |
| E007 | checked | this report has the table |
| E009 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| E010 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| E011 | checked | FAULT - review result is not "NO UNLISTED FAULTS SEEN": 11 faults |
| E013 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| E020 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| E021 | checked | review2.json final "approved" and pixel-check-after-answer.json pass |
| E033 | checked | this report says "image"; the page text is unaffected by the rule |
| E034 | NOT checked | a process step of the main session, not visible on the page or in the files given to me |
| E035 | checked | 390 screenshots: one column, swipe rows with dots, text left-aligned; no phone-only fault beyond the all-width faults 1-8 |
| E052 | checked | no material-name headings (h3.material-name) on this page |

FAULTS: 11
NOT CHECKED: 80
