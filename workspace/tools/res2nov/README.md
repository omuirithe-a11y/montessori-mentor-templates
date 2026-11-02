# Helper scripts from 2 Nov 2026 (Resources pages 8.0, 8.1, 8.3, 8.4)
Copied from the 2 Nov chat's local folder /home/claude/res80 (not kept between chats). Paths inside them point to /home/claude/res80 and /home/claude/mm; change the build folder names before use.
- build-8.3.sh, build-8.4.sh: build a Resources page from its Word file and PDF (8.3/8.4 had no faces: --no-blur; 8.2 has faces - use the blurred images from the faces rounds instead).
- all-nolive-8.3-example.sh: every check for a NEW page (no live version): code check against Word, run_checks.sh (122 widths, height, lines, placement, speed), place v2, lines_v2 at 8 widths, format against Word, then screenshots (shots.py).
- all-live-8.1-example.sh + more_checks-8.1.sh: the same for a page WITH a live version (format against live, side-by-side screenshots vslive.py).
- runall6.sh: runs each build's all.sh one page after another (nothing beside a check).
- gates.sh: the send_gate.sh / send_gate_nolive.sh commands used.
- shots.py: screenshots of a build at set widths. layout_compare.py, longtask_trace.py, profile_scroll.py: earlier diagnosis tools.
- probes/: gaps.js (letters-to-letters gap between two texts at 1440, 768, 390: node gaps.js <build dir> preview '<json pairs>'), gaps2.js, atop.js (image top vs first line), ov.js (overlaps), col.js (badge columns), lines81.js, crop.js, probe.js, tk.js; g.py and v.py (2 Nov 21:4x: measure heading gaps and take ORDINARY window screenshots - the full-page captures of vslive.py can show more space around headings than a reader sees, e.g. 8.1 68/47 against 52/37).
