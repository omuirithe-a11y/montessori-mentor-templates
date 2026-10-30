# Essay Code Template change - 30 Oct 2026, 12:5x-13:1x (Asia/Shanghai)

Owner's words: 12:50 "yes" (an image beside text never runs past the text column); 13:05 "yes" (an image beside text starts
level with the top of the capitals of its paragraph's first line, on every page built from the template).
Template before: 3ebaef3a (commit 13175ad). After: 25b728e6.

1. Script mm-fit-column-30oct (before </body>): an image beside text wider than its column is shrunk to the column's width,
   keeping its shape. Aun Aprendo's 2:1 Beckett image ran 18 px past the text at 390; now it ends at the column edge, shape 2.0.
2. wrapFloats(): the image's top is placed level with the top of the capitals of its paragraph's first line (her rule of
   20 Oct, "side photos always align with the first line of the text"); it was centred on the paragraph (30 Sept, 27 Oct).

Tests:
- Aun Aprendo build b6: 122 widths every width ok; height steady 1440 and 390; lines through text 0 at 8 widths; speed OK;
  code check ALL CHECKS OK; image tops 0 px from the first line's capitals at 1047-1920.
- The Role of the Adult's content in the template: 122 widths every width ok; height steady; lines 0; image tops within
  0.7 px. Speed FAULT (busy stretches up to 242 ms while scrolling; clicks 0.77-0.78 s). The same content in the 13175ad
  template also fails (up to 1,963 ms at 390), so the fault is not from these two changes; it is open, next after Aun Aprendo.
