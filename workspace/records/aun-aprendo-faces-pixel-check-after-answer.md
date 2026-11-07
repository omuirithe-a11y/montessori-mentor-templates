# Aun Aprendo faces: pixel check after the owner's last answer

Checker: a separate agent that had not seen this work. Agreed blur method version 22, item 7 ("a separate agent's pixel check of the final images").
Time of check: 2026-11-07 14:54 Shanghai time (from `TZ=Asia/Shanghai date`).
Owner's answers: round 1 "approved", round 2 "yes", both 2026-11-07 14:48 Shanghai time (as given in the brief).

## What I looked at

- Final images: /home/claude/aun/build/faces/photos-final/ (37 images). photos-final.json lists 61 images: 37 "blurred", 24 used as they are.
- Originals: /home/claude/mm/blur2/m_aun7/media/. Blurred images the sheet showed: /home/claude/mm/blur2/m_aun7/images/. Faces: faces.json (363 faces: 226 blurred, 137 left by rule). Masks: masks/<tag>.png (226 masks).
- My scripts and work images: /home/claude/aun/pixel/work/ (an.py, meas.py, sheets.py, sheet-00.png to sheet-08.png, zoom-*.png, ub-*.png, z*.png; figures in an.json and meas.json).

## 1. Same picture, same size, equal to the sheet's blurred image

- Final, original and sheet image are the same size for all 37 (an.json "sizes").
- Final against the sheet's blurred image (images/): the largest pixel difference in any image is 19 of 255. The largest average difference is 1.24. That is JPEG re-save noise.
- image40.JPG: the final is 4000 x 3000 and is stored unturned, as Word stores it. The sheet showed it turned upright: the sheet's whole image matches images/image40.jpg turned 90 degrees clockwise (average difference 3.5). media/image40.JPG differs from the Word file's image40.JPG in 2 bytes, both 5019136 bytes long. The Word file's copy carries turn tag 6. The final carries no tags at all.

## 2. Faces (226 of 226)

- **By eye, 103 faces.** Each one shown as the original next to the final at full size, enlarged (sheet-00.png to sheet-08.png):
  - all 41 faces under 60 px wide, which includes 15-k, 18-d and 29-i;
  - the hand-added faces 16-g and 42-f, plus 40-a, 16-b, 16-f and 20-b;
  - 40 faces picked at random with seed 20261107 (Python random.sample);
  - 16 more faces that my measure flagged (detail kept above 0.45 of the original, or the blur covering less than 0.8 of the box centre).
  I also looked closer, with more of the image around them, at 29-h, 19-f, 36-c and 52-g. In every one of the 103 the eyes, nose and mouth are hidden. Where the original shows a back or side of a head (for example 23-p, 29-h, 51-f), the face part that shows is blurred.
- **Measured, the other 123.** In the centre of each full-size box, the final changed by at least 5.3 levels on average against the original. The detail left was at most 0.45 of the original's, and the blurred area covered at least 0.85 of the box centre. All 123 are within the range of the faces I looked at by eye and found hidden.
- 19-f: the blue eye patch and the glasses frame still show as colour, but no eye, nose or mouth shows.

## 3. Outside the blurred areas

I compared final and original everywhere more than 12 px away from any mask. The largest single-pixel difference in any image is 45. The largest difference after smoothing over 9 x 9 px is 16.7 (image21). The largest average difference is 2.56. I looked at where the biggest smoothed changes are: the ceiling light in image21, the shirt edges in image8, plus image56, image57 and image37. They are JPEG noise on sharp edges and bright detail. Nothing in the picture changed there.

## 4. The 24 unblurred images

All 24 sha256 values in /home/claude/aun/unblurred-list.json match the files in media/. I looked at each one whole, and enlarged every person in the background: image54 (an adult in a visor, and a child in yellow seen from behind through a net), image55 (the bus seats), image14 (the street), image10 (the diners) and image12 (the shop doorway). In none of them does a child's face show with an eye visible. The faces they do show are adults or printed pictures, and faces.json lists those as "skipped".

## The sheet file

The checked sheet's sha256 was 59e02ffe.... The file /home/claude/aun/aun-round1.html now has sha256 bd75f2745fce0d5445196c30ffc1e82bed6bdd6ce8504dc69dcea0b839bf8787. It was last written at 05:57:43 UTC. Its check is recorded at 05:57:09 UTC (sheet-check-final.json) and its report was written at 05:57:26 UTC. That fits the method's release step, which takes off the NOT CHECKED banner after the check passes: the banner is no longer in the file. All 287 images inside it are still byte-identical to the working files (59 in whole-sheet/, 226 in crops/, 2 in left-off/). So what the owner saw is what I checked against.

## For the owner

- All 37 blurred images on the page match the sheet you approved. In every one of the 226 blurred faces, the eyes, nose and mouth are hidden. Nothing else in those images changed.
- None of the 24 images used as they are shows a child's face with an eye showing.
- image40 (the girl lying down) is stored on its side, as Word holds it, and has no turn tag. When the page is built it must be turned upright, as the sheet showed it. Otherwise it will show on its side.

## Could not check

Could not check: nothing in the brief. I did not open the page in a browser, as told, so how image40 shows on the built page is for the build check.

PASS
