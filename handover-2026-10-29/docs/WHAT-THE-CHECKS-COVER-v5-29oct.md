# What the checks cover, and what they do not (version 5, 29 Oct 2026 07:3x)

Version 5 adds section 'Changes on 28-29 Oct' at the end. Sections 1-6 below are version 4 (28 Oct 14:4x), unchanged; where they conflict with the new section, the new section wins.


## How this was made

**Read in full, line by line, between 14:10 and 14:30:** the check scripts in /home/claude/reports/checks-v14/:
- strip_compare.py, 217 lines;
- format_check.py, 48 lines;
- visual_check.py, 102 lines;
- live_match.py, 14 lines.

Line numbers below are in these scripts.

**The templates were not read line by line.** A program pulled their classes, settings, variables and breakpoints out of their styles and scripts. The class lists were then pulled out a second time with a different pattern that also reads names inside double quotes, and both gave the same lists.

What the program cannot find: a name a script builds up while the page runs, such as `'mm-hc-' + colour`. The lists in sections 3 to 5 are therefore complete for names written out in the templates, and not otherwise.

**Templates used:**
- Essay Code Template.html, GitHub commit 02f147a (sha256 0b3d3850);
- Resources Code Template.html, commit ddce8cb (sha256 138b5e0c).

**Which template each page is built on.** This was confirmed at 14:2x by comparing each package's template code with each version on GitHub: every one is an exact match.

| Page | Template version |
|---|---|
| Biography, Aun Aprendo, The Practical Life Curriculum | Essay, commit 575b25b (sha256 e47b1b0e) |
| A Montessori Journey | Essay, commit ae040de (sha256 2e4f029f) |
| The Mathematics Curriculum, The Culture Curriculum, The Sensorial Curriculum | Essay, commit 02f147a (sha256 0b3d3850) |
| Sensorial Resources, The Role of the Adult – Resources | Resources, commit ddce8cb (sha256 138b5e0c) |

The class lists below are from the newest versions. The styled classes of the three Essay versions were compared:
- ae040de has the same classes as 02f147a;
- 575b25b has one fewer, mm-pdfsp.

Their settings, variables and named scripts were also compared at 14:4x. Versions 575b25b and ae040de have exactly the same settings, variables and named scripts as 02f147a. The differences are inside the script code itself: template changes 23-30, which add 6 to 12 lines.

**Which check versions each delivered page passed.** The code check was run again at 14:4x on all seven delivered packages, each against its own template version. All seven read "ALL CHECKS OK (parts 1-4 and 8)". The outputs are in /tmp/claude-0/-home-claude/457824cb-7342-52d8-8229-8cd580a6aa46/scratchpad/recheck/.

| Page (package) | Code check, run again 14:4x | On-screen check |
|---|---|---|
| A Montessori Journey (38225171) | checks-v12 | visual_check sha256 68026417, 122 widths, "every width ok"; file final-checks/a-montessori-journey-38225171-visual-full.txt |
| Aun Aprendo (97b8de20) | checks-v11 | sha256 68026417, 122 widths, "every width ok"; final-checks/aun-aprendo-97b8de20-visual-full.txt |
| Biography (43051826) | checks-v11 | sha256 68026417, 122 widths, "every width ok"; final-checks/biography-43051826-visual-full.txt |
| The Practical Life Curriculum (4c59a98b) | checks-v11 | sha256 68026417, 122 widths, "every width ok"; final-checks/the-practical-life-curriculum-2-4c59a98b-visual-full.txt |
| The Mathematics Curriculum (8bae404f) | checks-v14 | sha256 68026417, 122 widths, the known faults only; final-checks/the-mathematics-curriculum-8bae404f-visual-full.txt |
| Sensorial Resources (80a8b076) | checks-v14 (on 27 Oct: checks-v9) | sha256 68026417, "every width ok"; independent-checks/sensorial-resources-80a8b07652a2-visual-v9.txt |
| The Role of the Adult – Resources (f5e6ea1e) | checks-v14 (on 27 Oct: checks-v9) | sha256 68026417, "every width ok"; independent-checks/the-role-of-the-adult-resources-f5e6ea1edaad-visual-v9.txt |

The on-screen check script is the same file, sha256 68026417, in checks-v7 to checks-v14. checks-v11, -v12 and -v14 differ only in which Essay template fingerprint the code check expects. checks-v9's code check is a different file (sha256 2d8c1433, against e210778f for v14), so the two Resources pages were also run on v14, and passed.

**Before 14:4x**, no saved code check output existed for the delivered Practical Life package (4c59a98b), the one with the corrected image descriptions. The earlier outputs found were for older packages. It passes now.

**Format check outputs:** only these were found:
- Sensorial Resources, "266 differences", in coordinator-checks/;
- The Role of the Adult – Resources, "20 differences", in coordinator-checks/;
- A Montessori Journey, "10 differences", in final-checks/code-and-format/t2e4f/journey-format.txt, run on the build before its descriptions were corrected.

Whether every one of those differences is an allowed change has not been checked again today.

## 1. What each check does

### Code check (strip_compare.py)

| What | Lines | Compared with |
|---|---|---|
| Everything outside the content area is identical to the template: head code, all styles and scripts, header, menu markup, contents box, hero, footer, image viewer. Excepted (lines 34-40): the page title, the hero title text, the hero image name, the contents entries, the menu entries. | 53-55 | template |
| Copy protection: present once and in place | 57-60 | fixed file |
| Menu entries: only the template's tags, attributes and classes; links go to the same pages as live | 93-98, 128-135 | template, live |
| **Inside the content:** every class and data- setting is a name the template code *mentions* (lines 63, 111, 114). It does **not** check that it is the right element, or that its value is right. | 102-118 | template (names only) |
| Classes the template uses only for the page frame are not allowed inside the content, and neither are ids the template already has | 100-105 | template |
| Inside the content: no script, style, link, iframe, object, embed, form, input, meta, base or svg | 64, 109 | fixed list |
| Inline styles are not allowed inside the content, with three exceptions: a variable the template reads (list in section 5), aspect-ratio on an image box, and PDF-placed image boxes, which must equal live | 119-127 | template, live |
| The content area's own settings equal the template's | 142-143 | template |
| Every word, including the page title, hero title and contents entries' text; every content link's text and destination; every content image, in order | 145-159 | live |
| Image descriptions are listed; names in them that are not in the page text are flagged | 160-168 | page text |
| Image files that differ from live are listed, not failed | 169-176 | live |
| The hero is images/hero.jpg; every file the page names exists; image shapes match their files (within 1%) | 177-206 | files |

### Format check (format_check.py)

| What | Lines | Widths |
|---|---|---|
| Each word **inside the content area only**: colour, italic or upright, bold (weight 600 or more) or regular, underline | 17-22, 41-46 | **1440 and 390 only** |
| Which words can be seen, and which images can be seen (by file name, in order), inside the content area | 23, 36-40 | 1440 and 390 |

It compares with **live**, never with the template. The page title, hero, menu, contents box and footer are outside its scope.

### On-screen check (visual_check.py)

It runs at 122 widths (line 23), one page load each, plus one window narrowed from 1280 to 390 (lines 96-99). At each width it counts:
- images in the content taller than the larger of 200 px and their set's own height plus 2 px, from 641 px up (line 60);
- paragraphs of more than 60 characters narrower than max(260 px, 0.35 × the content width), from 641 px up (line 58). Inline elements are skipped, and so is text inside table cells or list items unless it is the list item itself;
- images in the content shown more than 20% wider than their file (line 61);
- sideways scrolling of the whole page (line 62);
- text over text, inside the content area only, between elements that hold text of their own, ignoring an element inside another (lines 40, 47-49);
- text over a content image, image over image, and content image over the footer band (lines 50-53);
- content and hero images that have not loaded (line 54);
- whether the hero image loads (lines 55-56);
- whether each menu panel opens and closes when its button is clicked, at 17 widths only (lines 24, 64-75);
- console errors, page errors, failed requests and responses of 400 or more (lines 84-87).

Nothing overlapping in the header, hero or footer is looked for.

It compares with nothing: it only counts faults. Its limits, checked against the templates at 14:4x:
- **Narrow column, 260 px / 0.35:** taken from the templates. Essay 02f147a line 883 and Resources ddce8cb line 915 say `Math.max(260, 0.35 * W)`. The script cites Essay line 878 and Resources line 914; the lines have moved as the template grew.

  There is one difference. In the template, W is the width of the image set. In the check, it is the width of the whole content area.
- **Image height, 200 px:** not from the templates. The templates' image heights stop at 170 (Essay line 838, `ROW = 170`; Resources line 874, `ROW = 168`). 200 is the check's own allowance above that, which I set.
- **Enlarged by 20%** and **more than 60 characters:** the check's own numbers, which I set.

Before measuring, it makes every image load at once and scrolls to the bottom and back (line 89). A fault that shows only while a visitor scrolls and images arrive one by one is therefore usually missed. The 831 px Aims overlap on Mathematics was missed this way, and was caught only by a second agent's repeat runs. Phone emulation is used at 640 px and narrower.

### After upload (live_match.py)

Every file on the live site is byte-identical to the package. It does not look at the page.

## 2. Covered as code: the page frame

These are the classes the templates use outside the content area. Code check part 1 requires their code to be identical to the template.
- **Essay, 38 classes:** beige-rule c4 cat grp has-panel hd hero icon-btn lb-counter lb-nav lb-next lb-prev lead lightbox mc-band mc-by menu menu-btn np panel panel-in pcol site-foot site-foot-in site-head site-head-in site-name site-nav site-tools skip sub-toggle toc toc-grid toc-groups toc-label toc-rule-wrap toc-wrap top
- **Resources, 36 classes:** c4 cat grp has-panel hd hero icon-btn lb-counter lb-nav lb-next lb-prev lead lightbox mc-band mc-by menu menu-btn mm-toc3 np panel panel-in pcol site-foot site-foot-in site-head site-head-in site-name site-nav site-tools skip sub-toggle toc toc-grid toc-label toc-wrap top

Not covered, even in the frame:
- how the frame looks on screen;
- the formatting of the page title, hero title, menu text, contents entries and footer text (the format check reads the content area only);
- the hero image itself, beyond its name and that it loads;
- the image viewer, which is never opened;
- the contents entries' link destinations: their text is compared, their destinations are not.

## 3. Not covered: the content elements

For every class below, the only check is that its name appears in the template code (code check, line 111). No check confirms:
- that it is the element live used — live's beige `mm-line` became the grey `formula-divider` on A Montessori Journey, and both names are in the template, so it passed;
- or that it looks the way the template sets it: colour, thickness, size, spacing, alignment, position.

The words inside these elements are checked: their text, plus colour, bold, italic and underline at 1440 and 390.

**Essay, 167 styled classes:** article beside-photo blindfold-label c1 callout callout-label centred colophon cw-white doc-img formula-divider formula-head formula-table formula-wrap g grp-first grp-last grp-mid hero-sub lb-frame lbl-blue lbl-bold lead-rule material-name materials-table mc-1-1 mc-1-2 mc-1-3 mc-2-1 mc-2-2 mc-3-1 md meta micro-label mm-area mm-arrow mm-attr mm-bda mm-cabar mm-cabar-bar mm-cabar-ends mm-cabar-plain mm-cabar-tick mm-cabar-ticks mm-cap mm-cap-below mm-caprow mm-cf mm-col mm-cols2 mm-cols3 mm-contain mm-cset mm-ctr mm-dots mm-float mm-flow mm-formula mm-g2 mm-g2c mm-g2col mm-gl mm-gl-bq mm-hang mm-hc-0000FF mm-hc-008F00 mm-hc-00B050 mm-hc-0432FF mm-hc-2CC171 mm-hc-521B93 mm-hc-66CCFF mm-hc-7030A0 mm-hc-797979 mm-hc-945200 mm-hc-996633 mm-hc-CC66FF mm-hc-ED2AFB mm-hc-EE0000 mm-hc-FB0207 mm-hc-FBEF32 mm-hc-FF0000 mm-hc-FF3FFF mm-hc-FF9300 mm-hc-FFDD60 mm-hc-FFFFFF mm-hs mm-imgs mm-inner mm-intro mm-just mm-left mm-lineabove mm-name mm-noind mm-noline mm-notes mm-one mm-pcap mm-pdf mm-pdf-l mm-pdf-r mm-pdf-row mm-pdff mm-pdfflow mm-pdfin mm-pdfsp mm-pf mm-pfig mm-ph11 mm-ph26 mm-poem-ctr mm-pspacer mm-pwrap mm-red mm-row mm-set mm-sub mm-t mm-tab1 mm-tabcol mm-table mm-table-wrap mm-tabtail mm-text mm-toc3 mm-tocline mm-trio mm-wc mm-wcol mm-wcol2 mm-wcols2 mq np-top on op open over page-h2 pdf ph pim preview-grid preview-line pullquote py ref-desc ref-label ref-row ref-table res-item res-title rule section sense seq-line sub sub-label swatch tight-bottom tight-top title-block toc-area toc-col1 toc-num total touch-head touch-table

**Essay, 11 more classes used only by its scripts (no style of their own):** mm-br mm-fspacer mm-l2 mm-lstart mm-org-rule mm-tabpart mm-tabrow mm-tabstops mm-tiles mm-twocap res-entry

**Resources, 126 styled classes:** article beige-rule blindfold-label c1 callout callout-label centred colophon cw-white doc-img formula-divider formula-head formula-table formula-wrap g grp-first grp-last grp-mid hero-sub lb-frame material-name materials-table mc-1-1 mc-1-2 mc-1-3 mc-2-1 mc-2-2 mc-3-1 md meta micro-label mm-ami mm-attr mm-besidepdf mm-blue mm-cap mm-col mm-dots mm-figcap mm-fitlines mm-float mm-formula mm-fspacer mm-gl mm-hanglab mm-hc-00B050 mm-hc-EE0000 mm-hc-FF0000 mm-imgs mm-ink mm-inner mm-intro mm-lab mm-lalpha mm-left mm-licont mm-lroman mm-lsp mm-mk-alpha-paren mm-msfloat mm-n mm-numline mm-org-rule mm-pairend mm-poem-ctr mm-row mm-rowleft mm-set mm-sub mm-sugar mm-t mm-t2 mm-t3 mm-tab mm-tab1 mm-table mm-table-wrap mm-text mm-trio mm-ualpha mm-under mm-uroman mm-w mm-wi mm-wr mq np-top on op open over page-h2 pdf pdf-date ph pim preview-grid preview-line pullquote py q-ref ref-desc ref-row ref-table res-book res-desc res-entry res-item res-item-line res-label res-link res-src res-title rule section sense seq-line sub sub-label swatch tight-bottom tight-top title-block toc-groups toc-num total

**Resources, 11 more classes used only by its scripts:** mm-bbr mm-br mm-l2 mm-lstart mm-mid mm-pfig mm-pspacer mm-pwrap mm-tabrow mm-twocap mm-ul

Some of these names (on, open, over, mm-one, mm-lstart and others) are states or markers the scripts switch on and off, not elements a page is built from. They are listed because they are names the templates use.

## 4. Not covered: the template's settings

For each setting, only its **name** is checked (code check, line 114). Its **value** is never compared with live or with the template. The exceptions are data-h, data-scale, data-column, data-match, data-likerows, data-gaps, data-hscale, data-row-h, data-crop, data-rot and data-w: their values are listed for the owner, not judged (line 115).

These lists include the settings the scripts read under a script name (dataset.…), which the first version of this list missed: data-gpx, data-row-above, data-ga-photos, data-after, data-between, data-bottom, data-deftab, data-fit-text, data-ntab, data-tabstops, data-wrap and data-tw.

**Essay, 73 settings:** data-above data-above-from data-after data-align data-at data-between data-bottom data-cap data-centre-lines data-clear data-cols data-column data-crop data-deftab data-fgap data-first data-fit data-fit-text data-foot data-full data-ga data-ga-photos data-gap data-gap-phone data-gaps data-gb data-gpx data-grid data-h data-hmatch data-hscale data-last data-layout data-left data-level data-likerows data-line data-linemid data-match data-nocentre data-notred data-ntab data-pair data-purpose data-rot data-row-above data-row-h data-rows data-scale data-space data-space-desk data-space-head-after data-space-head-before data-space-head-line data-space-lines data-space-phone data-space-row-text data-spacing data-src-step data-step data-tabs data-tabstops data-top data-topline data-trim data-under data-valign data-vc-lower data-vc-upper data-vgap data-want data-word-bold data-wrap

**Resources, 55 settings:** data-above data-above-from data-align data-at data-bottom-on data-centre-lines data-cols data-column data-crop data-fgap data-fill-gap data-fit data-foot data-full data-gap data-gaps data-grid data-h data-height data-hmatch data-hscale data-layout data-level data-likerows data-match data-pair data-pdf-column data-pdf-group data-ph-pad data-phone-gaps data-purpose data-res-pdf-column data-rot data-row-h data-rows data-rule-gap data-rule-gap-below data-scale data-space data-space-head-after data-space-head-before data-space-head-line data-space-lines data-space-row-text data-spacing data-tabx data-tw data-under data-valign data-vc-lower data-vc-upper data-vgap data-want data-word-bold data-wrap

(data-full is the name of an image's full-size file, and data-layout is set by the template itself. Both are listed because the templates use the names.)

## 5. Variables and breakpoints

**Colour and size variables set by the templates.** Their values are covered by code check part 1.
- Essay: --active --bar --bar-line --bg --card --display --gutter --head --heading --ink --line --link --material --mh --navy --page --paper --paper-alt --quiet --rule --sans --serif --tint --title
- Resources: the same list without --mh.

**Variables a page may set in an inline style inside the content**, because the template reads them (code check, line 126). Their values are not checked.
- Essay: --active --bg --display --g2gap --gl --gutter --h --hang --head --heading --hp --hw --ind --ink --line --link --ly --material --mh --n --navy --page --paper --quiet --rule --serif --tint --title
- Resources: --active --arR --bg --display --gutter --head --heading --hp --ink --line --link --material --mh --navy --page --paper --quiet --rule --sans --serif --tint --title --wm --wt

This means a page could set, for example, `--ink` or `--rule` on one block and change its colour, and the code check would pass it.

**Breakpoints (both templates):** 640/641, 830/831, 960/961, 1023, 1099, 1180, 1279.
- The on-screen check runs on both sides of each one.
- The format check runs at 1440 and 390 only, so it covers two of the eight width bands.

## 6. What no check looks at

1. **Anything with no words and no image:** lines, dividers, rules, borders, empty boxes. A line that changes colour, or disappears, passes every check. This happened on A Montessori Journey, where 15 beige lines became grey, and on Biography, where 2 lines were removed.
2. **Spacing between blocks:** paragraphs, headings, labels, lists, quotations, image rows, dividers.
3. **Text, beyond the four word properties:** font, size, line height, alignment (centred, justified, left), indents, letter spacing, highlight and background colours.
4. **List bullets and numbers.** Checked in both templates' styles:
   - bullets are drawn by the style, as a "‐" mark (`ul li::before`);
   - numbers are drawn by the style (`list-style: decimal`, and a counter for numbered lists that continue).

   Neither is text in the page, so no check compares them.
5. **Tables:** borders, shading, column widths, alignment.
6. **Image placement:** beside the text, in a row, at its PDF position, captions above or below. Image size is checked only for "too tall" and "enlarged too much". Crop and rotation values are listed, not compared.
7. **Colours of anything that is not a word:** heading lines, backgrounds of boxes and panels, quotation boxes.
8. **Word formatting at any width other than 1440 and 390**, and anywhere outside the content area.
9. **Faults that appear only while a visitor scrolls**, before every image has loaded (see the on-screen check above).
10. **Behaviour:** the image viewer, swiping on phones, contents links jumping to their heading, hover.
11. **Browsers other than Chromium:** Safari and Firefox are never tested.
12. **The template itself, on screen:** no check compares how a page looks with how the template sets it. The format check compares words with live; the code check compares code.

## 7. Corrections

**To my 14:07 answer:**
- I said the header, menu, footer and footer band were "tested for opening and closing only". Wrong: their code is checked to be identical to the template (code check, line 53). How they look on screen is not checked.
- I said "I haven't confirmed whether any check compares where each link goes". The content links' destinations are compared with live (code check, lines 150, 158). The contents box links' destinations are not.
- I listed only the Essay template; the Resources template is now listed too.
- I gave about 70 of 205 classes; all are listed now.

**To version 1 of this document (14:12):**
- It said the templates were "read in full". They were not; their names were pulled out by a program (see "How this was made").
- It missed 22 classes used only by the scripts, and 12 settings the scripts read under a script name.
- It said only "--mh and a few other variables" may be set inline. The full lists are in section 5; they include --ink and --rule, which change colours.
- It did not say that the format check reads only the content area.
- It did not say that the on-screen check makes all images load at once, and so misses faults that appear while a visitor scrolls.
- It did not say which template version each page is built on.
- It said list bullets and numbers are "not text" without having checked the styles. They have now been checked (section 6, item 4).

**To version 2 of this document (14:2x):**
- It said visual_check.py lines 1-79 had been read "this morning". That earlier read cut every line off at 400 characters, so it was not a full read. All 102 lines have now been read in full.
- It said the on-screen check's limits were "numbers I chose". The script records them as the templates' own numbers, with template line references; this is now stated, along with the fact that the template lines have not been opened today to confirm it.
- It did not say that the on-screen check looks for overlaps only inside the content area, or which elements its narrow-column and text-over-text tests skip.
- The template version for each page came from my notes, not from the packages. It has now been confirmed by exact code comparison.
- It did not say which check versions each delivered page passed, or where those results are. A table has now been added.
- The class lists came from one pattern only. A second pattern has now been run, also reading names in double quotes, and it gave the same lists.

**To version 3 of this document (14:3x):**
- The check-version table was written from my notes, not from saved outputs. The saved outputs do not record which check version produced them, and one delivered package, Practical Life 4c59a98b, had no saved code check output at all. All seven have now been run again, each against its own template version, and all pass.
- It said the Resources pages "passed checks-v9" without giving Sensorial Resources' result. Its on-screen result is "every width ok", and both Resources pages now also pass the code check on v14.
- It pointed to format check outputs without saying which pages have them. Only three were found, and their differences have not been checked again.
- It said the template lines behind the limits had not been opened. They have now been opened. One limit (260 px / 0.35) is the template's, at slightly different lines. The other limits (200 px, 20%, 60 characters) are the check's own.
- It said the scripts and settings had not been compared across template versions. They have now been compared: settings, variables and named scripts are the same; the script code differs by template changes 23-30.
- It still does not, and cannot honestly, say that the templates were read line by line. Each is about 2,200 lines, many of them several thousand characters long, and their names were pulled out by program.

## Changes on 28-29 Oct (version 5)

### Checks added since version 4, and what each covers
| Check | Tool | What it covers | Run by |
|---|---|---|---|
| Height and margins | scratchpad/elist/stable.py | main's height at 1 s, 4 s, after scrolling the whole page in 800 px steps, after opening and closing every album; the largest margin-top in main | send_gate.sh (1440 and 390, required) |
| Album toggle | stable.py ("closed again") | the page returns to its load height after albums are opened and closed (Culture's 28 Oct fault) | send_gate.sh (required since 28 Oct 22:0x) |
| Full check, every width | checks-v*/visual_check.py through tools/vfast.py | the same checks as before at all 122 widths; the runner no longer changes what is checked | send_gate.sh requires 122 widths and the narrowing line |
| Fault filter | tools/faults_allowed.py | each FAULT line item by item: allowed only if every item it names is allowed and every other count is 0 | send_gate.sh |
| Lines through text | chk-sen3/tools/lines.py (written by a checker) | borders, hr and thin ::before/::after lines that fall through a line of text | the separate checker only - NOT in the gate |
| Screenshots against live | the separate checker | what a reader sees: overlaps, lines through text, gaps, missing images | the separate checker only |

### What is still NOT covered (known gaps)
- The send gate does not run the lines-through-text check or look at screenshots. On 29 Oct the beige lines through text (14 places at 700 px, 20 at 1440 px) passed the full check and the gate; only the checker's screenshots found them. Until it is added to the gate, every page needs the checker's lines and screenshot steps.
- Line colours and which elements have lines are compared with live (lines3.py, the checker), not with the template's own rules.
- Height is checked at 1440 and 390 only.
- visual_check measures after loading all images at once; faults that appear only while a visitor scrolls are seen only by stable.py's scroll step (1440, 390).
- The checks cannot tell whether a difference from live is correct; settled rules are listed in AGENT-BRIEF-STANDARD.md.

### Order (from 29 Oct)
On the FIRST build of a page, before any fix: code check, full check (band edges first), height check, format check, lines-through-text check, screenshots against live. Fix all faults found; then the same again on the final build; then send_gate.sh; then commit the template; then send.
