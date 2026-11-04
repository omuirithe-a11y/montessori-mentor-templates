# The English Curriculum: changes to correct the mistakes of 4-5 Nov (5 Nov 05:2x; owner 05:14 and 05:16)

Items marked NEW were added at 05:16 ("analyse and edit this list for elements that have been missed"), after a separate checker's pass.

## 1. The review brief, rewritten
- The Word file and the PDF decide what is on the page and where: columns, rows of images, where each image stands, captions, the kind of each line, indents and tabs, alignment, line breaks, bullets and numbers, tables, beige lines.
- The template decides sizes, spacing, fonts, colours, menu, footer, and the style of each element.
- A difference from the PDF is excused only by quoting the owner's written rule. "The template does it" is not a reason.
- The reviewer goes through the PDF page by page, beside the same part of the page.
- NEW: the brief quotes her placement rule: placement follows the PDF roughly, sizes follow the template. Columns, which images share a row, beside or above, and which side must match; exact positions inside the template's sizes need not.
- A new separate review after every build that changes the page, not only the final one.
- Its report lists every item no check covers, each marked checked or not checked.
- Before use, a second agent checks the brief against the owner's rules and the sources.
- NEW: the brief gives the reviewer only the build, the template, the Word file, the PDF and the rules - no notes from the builder on what to expect or excuse (lesson 35).
- NEW: the brief names the build by its folder and fingerprint, and the reviewer confirms both before starting.

## 2. New checks (each proven on a build with the fault and one without; added to the gate between runs, never while a check runs)
- Columns: text columns on each PDF page against the page at the computer width. Must fail on build 7 (Spoken Language lists).
- Lines against Word: each paragraph's kind, alignment, indent and tabs, bullets or numbers, line breaks; tables.
- Size, font and line height: every line against the template's figures for its kind.
- Images against the PDF: order, which share a row, beside or above and which side, captions, where each copy of a repeated image goes.
- NEW: each image also against the PDF for crop, turn, white background masked, and sharpness.
- NEW: where each image sits in the order of the text (after which paragraph), not only the order of the images among themselves.
- Contents box: entries against the PDF's headings, in order, none missing, none extra, no duplicates.
- Beige lines: every PDF line on the page, none added.
- Colour of things that are not words, against the template (beige lines #D9C9AB).
- NEW: no transparent or invisible lines in the code, and nothing added that is not in Word or the PDF.
- NEW: list indents (numbered and dash lists) and the gaps around underlined phrases on their own line, at the figures her rules set.
- Quotations: italic, the name under them.
- Hero: the 18:14 image (sha256 97e3f429), shown whole; title "The English Curriculum".
- NEW: page title and address /the-english-curriculum/.
- Links: each goes where Word's link goes; the check fails the gate.
- Phone rules: text left-aligned; image groups as swipe rows, each image stopping in the middle of the screen; a row that fits stays still, centred, with no dots.
- NEW: text justified at 641 px and wider.
- NEW: tablet width (641-830) rules checked as well as phone and computer.
- Site menu: this page in the menu of every other page - checked on the live site after her upload; it cannot be checked before.
- Contents links land on their headings; the image viewer opens.
- NEW: faces - every image file in the build is the released blurred copy (fingerprint matched against the faces data); no unblurred image reaches a build or preview.

## 3. Wider checks
- Spacing at all 13 widths on every build; also gaps between columns, image to caption, lines inside a paragraph.
- Bold, italic, underline and colour at every width.
- Height, placement and menu clicks at every width.
- Overlaps while images are still loading.
- Screenshots at the 13 spacing widths and every band edge, each looked at beside the PDF; the other widths by the automatic checks.
- Speed check repeated.
- Every existing check tested on this page with a planted fault before its result is trusted.
- NEW: every new check also run on one finished Essay page, to prove it does not fail a correct page (lesson 10).

## 4. Open results gone through, not left (NEW)
- NEW: the format check's differences against Word (288 on build 4): each one fixed or matched to a written rule.
- NEW: the code check's word differences (part 5): each one gone through the same way.
- NEW: build 9, started by the interrupted command: its state checked before anything is built on it.

## 5. How I work
- Every check on every build; time saved only by removing repeated work.
- Typos and US spellings corrected on every build at once (her spellings: "judgemental", "maths", "Lead Guide"); short dashes only, no spaces around a slash; names, published titles and quoted words stay as written.
- NEW: copy and paste work in the preview; copy protection only in the package for publishing.
- Records searched before asking; one question at a time.
- Faces rounds and the pixel check in full before any image with children is used.
- NEW: the preview republished, with its images, at every build, before it is named (lesson 66).
- NEW: every agent watched from its start; its result read before it is stopped (lessons 37, 38).
- NEW: no check script changed while it runs; a changed check is a new version with a new fingerprint (lessons 11, 39).
- NEW: other browser work stopped while the final build is checked (lesson 15).
- NEW: every reply through the message checker; the hourly lessons review kept.
- NEW: every fix swept 1 px at a time across every width before it goes to review (lesson 68).
- NEW: no "passed" without quoting the check's last line from its file, build by build (lesson 69).
- NEW: gaps she set by name built into the spacing check before the page runs (lesson 70).
- NEW: "pushed" or "saved" said only after comparing with GitHub's copy (lesson 48).
- NEW: long checks resume from saved results; free disk space checked and old test builds deleted (lessons 18, 41).

## 6. Then the page
- Lists in two columns, as in the PDF, in the template's two-column style.
- Letter Bingo pairs side by side; the Writing Stages image beside its list.
- The spacing faults; then everything the new checks and the new review find.
- NEW: the speed fault (the template's letter-gap script walks the whole page for every line): a fix shown in a preview; made only after her written agreement sentence stating the change, the widths and the pages; then every page built from the Essay template given a quick look and re-tested before the commit (lessons 6, 33).
- NEW: the final build: every check, the change list, send_gate_nolive.sh ending GATE PASSED (the gate for a page with no live version, settled 3 Nov), push with fingerprints, handover, START-HERE versions line.

- NEW: delivery: the folder name for public_html and one zip; never images downloaded from the live site; her original images as a numbered download after publishing (lesson 51).

## 7. Records
- Owner's messages from 04:51 on, and these changes, in the decisions log; new lessons in Lessons Learned; pushed to GitHub, copies in the Project.

## Cannot be done here
- Safari and Firefox: this workspace has only Chrome's engine.

## Already covered, so not added
- Footer, contents box label, menu, hero (no rotation): the code check requires them identical to the template.
- Side images level with the first line: the placement check (TOP).
- Word colours (blue, red, orange as black): the format check against Word.
