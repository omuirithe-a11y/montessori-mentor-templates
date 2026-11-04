# Review of The English Curriculum (3.5.0), build 1, against the owner's PDF - 4 Nov 2026

You are a separate reviewer who has not seen the page being made. Compare the built page with the owner's Word/PDF, section by section, and write every fault you find. Change no file except the report named at the end. Do not run the build or any check script; everything you need is on disk.

## What to compare
- The owner's source: /home/claude/eng35/src/3.5.0 The English Curriculum.pdf (23 pages, rendered to /home/claude/eng35/pdfpng/p01.png-p23.png) and the Word file /home/claude/eng35/src/3.5.0 The English Curriculum.docx (read its text with python-docx if you need the words).
- The page: /home/claude/mm/build-35/b1/preview/index.html (the page code) and its full-page screenshots in /home/claude/mm/build-35/b1/shots/: w1440-part01..35.png (computer), w768-part01..36.png (tablet), w390-part01..37.png (phone). Each part is 1400 px of the page from top to bottom. Look at every part at 1440; at 768 and 390 look at every part too, but report only what differs from 1440 (phone rules differ: text left-aligned, groups of images as swipe rows).
- The automatic checks' outputs, in /home/claude/mm/build-35/b1/checks/: code-word.txt (code against the template and words against Word), format-word-v2.txt (bold/italic/underline/colour against Word - use v2, not format-word.txt), place-v2.txt (image placement), lines_v2.txt, full.txt (122 widths: overlaps, oversized, squeezed), height.txt, speed.txt, space.txt (spacing against the PDF - made for the Resources template; on this Essay page most of its "faults" are the template's own spacing, so use it only to spot something odd). Read every line of code-word.txt sections 5 and 6 and of format-word-v2.txt; each real difference is a fault unless a rule below explains it.
- The build log /home/claude/mm/build-35/b1.log (its WARNING lines name things the build could not place).

## The owner's rules (her words, summarised; a difference that follows a rule is NOT a fault - say so where it matters)
- The page is built from the Essay Code Template (/home/claude/mm/templates/Essay Code Template.html): layout, spacing, font sizes, menu and footer come from the template, not from the PDF. Computer font sizes: hero title 40, "Table of contents" label 20, contents entries 18, headings 18, paragraphs and lists 18, quotations 18, captions 16, footer 15.
- The Word title line ("The English Language Curriculum") is replaced by the hero title "The English Curriculum" - not a fault.
- UK English everywhere in her own text (characterised, practising, colourful, organising); names, published titles and quoted words stay as written. Typos in the Word are corrected on the page (her 27 Oct rule) - list each correction you see so it can be confirmed.
- Short dashes only, no spaces around a slash ("and/or", "Cards/Nomenclature") - the page may differ from Word here by rule.
- Orange text in Word shows as ordinary black on the page. Blue text (#0432FF) in Word marks names of materials/activities, red (#EE0000) marks names/headings; both keep their colour on the page. Links are blue.
- Quotations: the template sets them italic (Word's bold italic becomes italic regular) with the attribution line under them - not a fault.
- Images: resized to fit, never cropped; placement follows the PDF roughly, sizes follow the template; images of objects on a white background have the white masked; side images top level with the first line of text beside them; on phones groups of images are swipe rows.
- Image descriptions (alt text) are not needed (her 28 Oct rule) - empty descriptions are not a fault.
- The contents box lists the page's headings (the template fills it) - but report duplicates, entries that are not headings in the PDF, and headings missing from it.
- Every beige line, every heading, every list, every table, every image row, every quotation in the PDF must be on the page in the same order with the same words; nothing added that the PDF does not have (no extra lines or elements).

## What to write
/home/claude/mm/build-35/b1/REVIEW.md, in this shape:
- a heading with the time (from `date`), what was compared and what was NOT checked;
- then the faults, numbered from 1, grouped by kind (A contents box, B headings and text, C bold/italic/colour, D images and their placement, E lists and tables, F spacing and lines, G phone/tablet only, H the automatic checks' findings you confirmed or rejected), each with: where (PDF page and the words nearby; the screenshot part), what the PDF/Word shows, what the page shows, and which rule applies if any;
- for each WARNING in the build log and each FAULT line of the checks, say whether you confirm it by eye;
- a last line "FAULTS: N".
Plain words. Say "image", never "photo". Every claim from something you looked at; mark anything you did not check.
