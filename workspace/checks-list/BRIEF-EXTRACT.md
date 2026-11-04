# Brief: extract every page rule into rows for tools/REQUIRED-CHECKS.txt (5 Nov 2026)

The owner agreed (5 Nov 05:48) that every check a Montessori Mentor page must pass will be listed in one file, each row with its source quoted word for word, and that the gates will require every row. Your job: read your assigned source IN FULL and write one row for every rule in it that says how a page must look, be built, be checked or be delivered. Nothing in the list may be the builder's own idea: every row must quote the owner's words, a lesson, or a template note.

## What counts
- How a page looks at any width: layout, columns, images (size, placement, rows, captions, crop, turn, white masking), spacing (gaps, in letters-to-letters terms where given), fonts and sizes, colours (words and non-words), lines/dividers, headings, labels, lists (bullets, numbers, indents), tables, quotations, contents box, hero, menu, footer, phone/tablet rules, alignment (justified/left), spelling (UK English, typos), dashes, links.
- How a page is built: from which template, from which source (Word/PDF/live), title/address rules, what is copied or left out.
- How a page is checked: which checks, at which widths, on which build, by whom (script or separate agent), what counts as a pass.
- How it is delivered: gate, zips, folders, copy protection, faces rounds before images with children, original images download, after-upload checks.
- Do NOT include rules only about how Claude writes messages to the owner (those belong to the message-check brief) unless they also govern the page.

## Superseded rules
Later decisions override earlier ones. If a rule was later changed, withdrawn, reopened or replaced, still write the row but set "status" to "superseded" and name what replaced it in "superseded_by". Only the newest wording is "current". Page-specific rules (one page only) get applies_to "page:<slug>".

## Existing checks you can map a rule to (inventory)
- code check: /home/claude/mm/tools/v8/strip_compare.py (live pages) and strip_compare_nolive.py (no live page): page code vs template, words vs live/Word, links, images, menu, copy protection.
- format check: /home/claude/mm/tools/v8/format_check_word.py (vs Word, 1440 and 390) / tools-v5-fixA/format_check.py (vs live): bold, italic, underline, colour of words; words and images seen.
- 122 widths: tools-v5-fixA/visual_check.py via vfast.py: oversized images, squeezed text, enlarged images, sideways scroll, text over text/image, image over image/footer, images not loaded, hero loads, menu panels open/close (17 widths), errors.
- height: tools-v5-fixA/stable.py (1440, 390): height steady after load/scroll/albums; largest margin.
- lines through text: /home/claude/mm/tools/lines_v2.py (8 widths).
- placement: /home/claude/mm/tools/v8/place_check.py (COLUMN, TOP, GAP 30/30, ROWS).
- spacing vs PDF: /home/claude/mm/tools/spacecheck.py (13 widths; together/apart from Word+PDF, sizes from template).
- speed: tools-v5-fixA/speed_check.py (busy stretches <=50 ms, clicks <=1.0 s).
- heading gap: /home/claude/mm/tools/v8/heading_gap.py.
- screenshot review: a separate agent looks at screenshots against live or the PDF ("eye").
- faces: blur method v22 tools, sheet checks and pixel check by separate agents ("eye" + scripts).
If no existing check covers the rule, set check to "new". If only a person/agent looking can judge it, set check to "eye".

## Output
Write JSON lines (one JSON object per line) to the output file named in your task. Fields:
{"item": "<the rule in plain words, one line>", "quote": "<the source's exact words>", "source": "<file and line number, or date/time entry>", "date": "<date and time of the owner's words if given>", "applies_to": "all | essay | resources | live | nolive | page:<slug>", "check": "existing:<script> | new | eye", "widths": "<widths or 'all'>", "pass": "<what counts as a pass, from the rule>", "status": "current | superseded", "superseded_by": "<source of the replacing rule, or empty>"}
Quote exactly; never paraphrase inside "quote". One rule per row; split compound rules. When unsure whether something is a rule, include it and add "unsure": true.
At the end, print a one-paragraph summary: rows written, current vs superseded, and anything you could not read. Change no other file.
