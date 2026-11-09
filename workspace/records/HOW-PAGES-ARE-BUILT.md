# How pages are built (from 9 Nov 2026)

The owner, 9 Nov 2026: "The most important thing to do now is to preserve this way of building pages." Before that, 8 Nov: "finished. this process is much quicker than 46 builds", and "yes - this page being built using the preview you just created is the priority. nothingmust be allowed to prevent that from happeing or even slow that from happening".

This replaces every earlier build order: claude/BUILD-ORDER.md, the fast and long rounds (check_round.sh), the 860-check and 524-row lists, build_guard's questions and the gate plans. Where START-HERE.md or any other file says otherwise, this file wins.

First used for The Prepared Environment, 8-9 Nov 2026: GATE PASSED c431a226, after one evening of edits on a live preview. The page had been through 8 builds before this method.

## The method

1. **One preview, from the Word file.** Build the page once with tools/build_page.py (Word file + Essay or Resources Code Template, faces first for images with children). Take out the copy protection and publish it as a preview artifact. That preview is the working copy from here on. Don't build again for edits.

2. **She edits on the live preview.**
   - Each edit she gives is made straight away in the preview's index.html, and the preview is republished, so she always sees the result.
   - Every question about something visible comes with the preview open.
   - Answers are terse: just the number ("The space between those two paragraphs is 29"). Don't explain measuring methods, and don't quote phone figures.
   - Her words for each edit are written down at once in records/<page>-EDITS.md.

3. **One spacing rule (the script mm-one-spacing.js).** It is put in the preview at the start and does all the vertical spacing:
   - 30 between blocks, measured from the bottom of the text (its baseline) or image above to the top of the capitals or image below;
   - 40 above and below quotations;
   - 40 from the hero to "Table of contents";
   - 40 from the last line to the blue footer;
   - the red-heading line 16 below the letters;
   - side photos level with the top of the capitals of the first line beside them.

   The template's own spacing scripts are not allowed to change those blocks (their writes are ignored), so the page doesn't jump after it opens. The script reruns only when the page's height changes, and each run takes under 50 ms.
   The tool is in workspace/pages/pe-final/mm-one-spacing.js, with its check onecheck.js.

4. **When she says "finished", the page is the preview.** There is no new build. tools: pages/pe-final/make_final.py takes the last build's zip (full-size images) and replaces its index.html with the approved preview. It puts the copy protection back exactly where it was and leaves out any image she deleted. Then it proves the round trip: the zip's page with the protection taken out equals the approved preview.

5. **The checks: once, one at a time, with nothing else running beside them.** Two processors: a second browser job at the same time made the speed check fail on 9 Nov.
   - Code check (strip_compare_nolive.py). The preview's new lines are added to the page's allowed list (tools/allowed/<page>-code.txt), with her words.
   - Format against the Word file (format_check_word.py). Her edits are the only new differences.
   - 122 widths (vfast.py), height (stable.py at 1440 and 390), placement (v8/place_check.py), speed (speed_check.py).
   - The one-spacing check at all 122 widths (onecheck.js): every gap, the side photos, hero, footer and red lines, no sideways scroll, nothing moving after 0.6 s.
   - Lines through text (lines_v2.py, 8 widths).
   - A separate agent compares screenshots of the final page with the approved preview at 1440, 1024, 768, 641 and 390.

   A fault the checks find is fixed in the page and the checks run again. The ones found on 8-9 Nov were: side photos not level, busy stretches while scrolling, and the chairs table pushing the page sideways at 320-360.

6. **The gate, then send.** tools/v8/send_gate_pe.sh is send_gate_nolive.sh with the PDF spacing part replaced by the one-spacing check. Its placement exception (an image above a quotation at 40) is her quotation rule. GATE PASSED, then send the UPLOAD zip with one line of context.

## Menu changes on every page (9 Nov 2026)
Changing the menu on every page is a separate job and needs no page build:
1. Download every live page's index.html (the hrefs in the home page's menu) into menu9/live.
2. Replace only the panel that changed. Byte-compare each page with live outside that panel: 0 differences.
3. Check the panel's items on every page at 1440 and 390 (menu9/mcheck.js; open the panel by a script click).
4. Zip index.html only, one folder per page, with the home page at the root.
5. Change the same panel in both Code Templates on GitHub, and re-pin strip_compare_nolive.py to the new template sha256.

## Lessons from 8-9 Nov
- Don't run two browser checks at once.
- Don't move or rename a checks folder while a run is still writing to it.
- A check that runs late can't be trusted on its own. The preview's own faults only show up in the checks, so the checks still run in full on the final page.
- Every time-dependent result is measured twice before it is believed.
- The template's spacing scripts rewrite margins about 29,000 times in the 9 seconds after the page opens. The one spacing rule exists for that reason. Don't add spacing fixes to those scripts.
