# Resources Code Template change, 3 Nov 2026 - mm-res-3nov-a (two lists side by side)

Owner's agreement, 3 Nov 12:45, word for word: "I agree to change the Resources Code Template so that two lists marked as a pair stand side by side in two equal columns at 641 px and wider, and one under the other at 640 px and narrower, on 8.2 Books of Interest and every page built from this template"

Change: one style block added before </head>, id mm-res-3nov-a:
  @media (min-width:641px){main .mm-pair{display:grid !important;grid-template-columns:1fr 1fr;column-gap:48px;align-items:start}}
  main .mm-pair > div > :first-child{margin-top:0 !important}
Template fingerprint: before 38fd0f9b (sha256 38fd0f9b14ea9266...), after cf017c93. Code checks (tools/strip_compare.py, tools/v8/strip_compare.py, tools/v8/strip_compare_nolive.py) updated to the new fingerprint.
Effect on other pages: only elements with class mm-pair are touched. No live page copy and no other page settings file in this workspace uses the class (grep at the 12:50 review: the only other match is "mm-pairend" in live/resources/index.html, a different class that .mm-pair does not select). Used by: pages/books-of-interest.py (Required Reading / Recommended Reading).
Commit: to be made once, with the 8.2 page, before the page is sent (lesson 43).

## Addition, 03 Nov 13:27 (under the same 12:45 agreement)
Build 5's separate review found the right column's heading ("Recommended Reading") standing below the whole left column at 641 px and wider: mm-letter-gaps-js measured its 40 px space from the lowest text above it on the page, which is the end of the left column, and set that as an inline !important margin (565.63 px at 1440).
Change: in mm-letter-gaps-js run(), the first line of a pair's right column is not measured while the pair is a grid; after the pass it takes the left column's first-line margin, so both start level. At 640 px and narrower (one under the other) the usual rule applies.
Fingerprint cf017c93 -> ea554a07. Quick test on build 6: both headings at the same top at 641 (1102), 1024 (947), 1440 (910); one under the other at 390 and 640.

## Second addition, 03 Nov 13:38 (same agreement)
Build 6's separate review: the headings were level, but the right column's entries still started below the left list - each line of the right column was spaced from the lowest text above it, the end of the left column.
Change: mm-letter-gaps-js lastBase() skips the left column's text when measuring for a line in the right column of a pair standing side by side (display grid). Fingerprint ea554a07 -> 7e182c67.
Quick test on build 7, tops of the first four lines, left | right: 641: 1102,1154,1243,1331 | the same; 768: 1006,1058,1146,1197 | the same; 1024 and 1440 the same both sides; 390 and 640 one under the other; 1440 -> 390 -> 1440 by resizing: level again.

## Third addition, 03 Nov 14:34 (lesson 32: one script per margin)
The style rule "main .mm-pair > div > :first-child{margin-top:0 !important}" is removed: the first line of each column has its space above set by mm-letter-gaps-js only. Fingerprint 7e182c67 -> f07114f0. Quick test on build 8: the pair's line tops identical to build 7 at 390, 640, 641, 768, 1024, 1440 and after resizing 1440 -> 390 -> 1440.

## Second template change, 03 Nov 15:04 (owner 15:02, "yes" to: "add a rule to the Resources Code Template so that the four Forest Bluff entries with Discussion Guide links are set flush left instead of justified")
Added to style mm-res-3nov-a: html body main p.mm-left{text-align:left !important}. Used on 8.2 only, on the four Forest Bluff entries that hold the Discussion Guide links (pages/books-of-interest.py). Fingerprint f07114f0 -> d1c2db87. Quick test on build 9: the four entries flush left at 960 and 1440; every Discussion Guide link on one line at 390, 768 and 1440; the pair unchanged.
