# Workspace - where each file came from (30 Oct 2026)

This folder is the exact copy of the working files. A new chat copies it with
`git clone https://github.com/omuirithe-a11y/montessori-mentor-templates` and proves every file with
`cd montessori-mentor-templates/workspace && sha256sum -c FINGERPRINTS.txt` (every line must say OK).
The Project's claude/workspace/ copies can only be read back as text, so they cannot be proved this way.
The templates (Essay, Resources, org-rule) are not copied here: the master copies are at the top of this repository.

## Sources
- 74 files: workspace-74-2026-10-30.zip, made by another chat from its copies (last changed 27 Oct 10:27-10:34);
  every file matched the zip's own fingerprint list.
- tools/format_check.py, live_match.py, strip_compare.py, visual_check.py: from this repository's tools-v5
  (handover-2026-10-29-evening). live_match.py differs from the Project text only at line 8.
- templates/copy-protection.html: typed from the Project; sha256 0d180ad6... is the one strip_compare.py expects.
- faces/yunet.onnx: from Drive (232,589 bytes, sha256 8f2383e4...).
- Changed or new 30 Oct:
  - tools/build_page.py: --shown-width, --no-blur <record>, large copies up to 2900 px (owner 30 Oct "Up to 2900 px - yes").
    The copy before the change matched the Project at 24 places.
  - pages/aun-aprendo.py: new. The 9 image descriptions written 30 Oct were removed (owner 28 Oct: descriptions "are not
    necessary anymore"). Whether the 52 copied from the live page stay is the owner's open question.
  - records/aun-aprendo-no-blur.json: the no-blur record (owner 29 Oct 10:25, agreed 30 Oct 09:24).
  - check-tools-v6-test/strip_compare.py: TEST copy of tools-v5's strip_compare.py, only the template pin changed to the
    30 Oct Essay template (3ebaef3a...). Not an agreed tool.

## Compared with the Project's text (30 Oct)
- tools/pages/frame.html: byte-identical (the Project handed over the file itself).
- tools/drawings.py, tools/menu_sync.py, tools/fetch_drive.py: identical (Project text typed out and compared).
- tools/convert_curriculum.py: identical except two invisible characters (a zero-width space, a no-break space on line
  157) that cannot be seen in the Project text; taken as the local ones.
- Every other file: NOT compared with the Project.

## Added 30 Oct, after 11:54 ("implement all 8")
- tools/run_checks.sh: runs the first-build checks with the tools-v5 tools unchanged - the 122 widths, the height and lines
  through text side by side, then the speed check alone. Tested 11:56-12:01 on the Aun Aprendo build b1 with 2 widths for
  the 122-width part: every part ran and gave the same figures as the separate runs of 10:33-10:53 (height 4711 / 7241).
- QUICK-START.md: the quick start prepared for the top of claude/START-HERE.md (not yet in START-HERE).
- 12:1x: tools/build_page.py - NAME_LINES page setting: named lines become the template's name line (p.mm-name) with the
  template's beige line before each, as on the live page. pages/aun-aprendo.py - NAME_LINES (the nine group names) and
  NO_TOC. Measured on build b2 against the live page at 1440, 830 and 390: all nine lines the same colour, size, beige line
  and gaps as live.
- 12:3x: tools/build_page.py - a page with no headings keeps the template's own empty contents box (the template hides it),
  as on the live Aun Aprendo page; removing it had changed the template's code (code check part 1). pages/aun-aprendo.py -
  NO_TOC taken out again. Build b3: code check part 1 down to the one added style block (mm-wrap).
- 12:1x-12:3x: build_page.py - dash joining dropped (owner 12:18 "drop it like the live page"); the build's own labels the
  template never reads left out (data-name except for CENTRE_ON, landscape/portrait, --ar/--hg); the mm-wrap style only when
  the page has something it styles; no image descriptions (owner 28 Oct; 12:26 "yes"). extra_checks.py check V and
  rule_checks.py's description check removed; rules.json X4 and TO-ADD item 10 updated; the four page settings with
  descriptions emptied (Prepared Environment, Role of the Assistant, Classroom Management, Observations).
  check-tools-v6-test/strip_compare.py also lists any image with a description (none allowed since 28 Oct).
- records/START-HERE-30oct.md: the copy of claude/START-HERE.md as written to the Project on 30 Oct 12:2x (shortened, quick start).
