# The Prepared Environment - owner's edits, 8 Nov 2026 evening (on the One Spacing Preview), her words
1. One spacing rule: 30 between every block and the next, at every width (preview: "This page is mostly fine").
2. "dividers: 30/30 is a better number. use the for every divider"
3. "all dividers to be the same colour" (all are #D9C9AB)
4. "add a divider above every blue sub-heading"
5. "the elemnets in the table of contents: leave them colouyred black in the table, but make them red on the page."
6. "'Furniture Dimensions' - add this as a red heading above 'Rows of the Shelves'"
7. "make the spacing for quotations the same 29.7" (phones: 28.05, as paragraphs)
8. "add a divider between the contents and the introduction"
9. "Make 'Furniture - Purchasing' one line"
10. "remove the dividers between the red headings and blue sub-headings"
11. "These photos need to be fixed" (Shelf Length, images 19 and 20): side by side beside the text, as in her PDF
12. Before/After: "the 2 photos in the first pair and the 2 photos in the second pair need to be closer together, with a bigger gap between the pairs" - the template's own data-gaps="0.4,2.2,0.4" on that row
13. Image 152: "is this photo 120 high?" / "it looks too big" - it is 120 high (172 wide) at 1280; 180 at 641-830. Not changed yet - her answer wanted
14. Madonna: "make the background match the colour of the page so it doesn't stand out" - white corners cut away (round)
15. "no further edits"
16. "image 152 - delete it"
17. quotations: "I\x27ve changed my mind. I like that number" - quotation lines 36 apart (as before), not 29.7
18. "make the space of 40 above and below quotations"
19. red headings: "add that line under the red headings ... match the distance" - 1 px line in the heading colour, 16 below the letters

## Later edits (8 Nov), all in the One Spacing Preview (version 10)
- "make that number 40 under the hero and above the footer" - hero to "Table of contents" 40; last line (baseline or image bottom) to the blue footer band 40.
- "add an introduction to the prepared environment, with the line under it, but do not add introduction to the table of contents" - red heading "Introduction" (with the red heading line) after the divider below the contents; not in the table of contents.
- "finished." - no more edits; version 10 of the preview is the approved look.

## Sent 8 Nov 2026: the-prepared-environment-UPLOAD.zip (05447856), GATE PASSED (tools/v8/send_gate_pe.sh)
- Page = approved preview v10 + copy protection + full-size images (pages/pe-final/make_final.py from b8's zip); no new build.
- Spacing: pages/pe-final/mm-one-spacing.js (one rule; template spacing writes to those blocks ignored; side photos levelled; each run under 50 ms).
- Fixes found by the checks: side photos at 641-830 not level (fixed); busy stretches while scrolling (fixed); chairs table 31 px sideways at 320-360 (smaller cell padding at 640 and below).
- Reviewer's 5 items, all as in the approved preview: 390 Shelf Length photos stacked; 390 Mats photo small; 390 Windows photo gap; 390 chairs table wraps; 641/768 swipe strips start right of the text.

## 9 Nov 2026, owner: "One last change. the Essential Elements menu is wrong. This is the correct one." (screenshot)
Essential Elements panel, three columns:
1. Essential Elements / Essential Elements Resources | Mixed-Age Groups / Mixed-Age Groups Resources | The Three-Hour Cycle / The Three-Hour Cycle Resources
2. The Role of The Adult / The Role of The Adult Resources / The Role of the Assistant | The Montessori Materials / The Montessori Materials Resources / The Montessori Materials Sourcing
3. The Prepared Environment / The Prepared Environment Resources / Essential Characteristics / The Outdoor Environment / Anji Play
Removed: Developing Responsibility, Montessori's Advice to Teachers (from this panel only; Developing Responsibility stays under Curriculum). Unpublished pages stay as plain text.
Done on this page only; the template menu (other pages) still has the old panel.
- 9 Nov, owner: "I want to change them all" - all 42 live pages downloaded; Essential Elements panel replaced on each (nothing else differs, byte for byte); menu items checked on 41 pages at 1440 and 390; essential-elements-menu-41-pages.zip sent; both templates updated (GitHub d122be5); strip_compare_nolive pins the new templates. The Prepared Environment re-gated: GATE PASSED c431a226.
