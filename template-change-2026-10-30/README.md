# Essay Code Template change - 30 Oct 2026 (Asia/Shanghai)

Owner's words: 09:20 "add them to the template and test the template on its own ... yes. do this"; 11:21 "keep the rule and commit the template".

Template before: commit 533f0c5, sha256 de0725464cd9c9c9...
Template after: sha256 3ebaef3a0922e9ea... (full diff: essay-template.diff)

## The changes (copied from the live The Role of the Adult, 29 Oct)
1. Contents alignment (mm-toc-align): already in the template, unchanged.
2. Font sizes: style mm-type-29oct (byte-identical to live).
3. Image above its quotation below 440px: style mm-quote-image-29oct (byte-identical to live).
4. Quotation-line edits in glInk() and glTopline(): (a) an image standing in the text starts at 0 like a row; (b) 30px from the
   last line's baseline to an image standing above its text; (c) a quotation opening with such an image takes the 40px image
   space; (d) such a quotation is measured from its image; (e) glTopline skips an image that is not floating. The template's own
   23 Oct rules kept (owner 11:21 "keep the rule": at 640px and narrower an image inside a quotation is measured from its top).
5. 30px above/below images standing above their text: script mm-image-gap-29oct (byte-identical to live).
6. Fix A: an image that loads re-spaces the page only if the page's size changed (byte-identical to live).
7. mm-photo40: the line that set 40px BELOW an image standing after a quotation removed - it fought change 5 (owner 29 Oct
   12:12 "they should all have a gap of 30"): measured 46px at 830 and 45px at 390/320 before, 30px after, as live.

## Checks (files in this folder)
- Speed (speed_check.py, Aun Aprendo build): old template FAULT (busy stretches 24 at 1440, 59 at 390; longest 286 ms);
  new template OK (none; clicks 0.75-0.83 s).
- Full check, 122 widths (vfast.py, visual_check sha256 68026417): Aun Aprendo build and a test page of The Role of the Adult's
  content in the new template - every width ok, narrowing 1280->390 sideways 0.
- Height (stable.py) at 1440 and 390: steady on both test pages; largest margin 48px.
- Lines through text (lines.py) at 320, 390, 430, 641, 700, 830, 1024, 1440: 0 on both test pages.
- Stacked images 020, 028, 034, 046: 30 above / 30 below at 830, 641, 430, 390, 320 - the same as live.
- Separate agent (had not seen the work): PASS - changes 2-7 present and correct, nothing else changed. One difference from
  live: image 023 at 440-640px sits 45/40.5px below the line above (live 36.3/31.5) because the 23 Oct rule is kept; no overlap.
  Not checked by it: Firefox/Safari, resizing, the template's other differences from the live page.
- Code check (strip_compare.py): the build tool's own additions fail it identically on old and new template (not a template effect).

The test page of The Role of the Adult was a local test only; the live page is unchanged.
