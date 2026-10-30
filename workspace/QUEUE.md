# Montessori Mentor work queue (read by the mm-gate mod)
# "- [ ]" open: the turn cannot end while one is open. "- [x]" done. "- [waiting: ...]" needs the user.

- [x] Gate: all 14 checks proved on 5.4; tools/gate.py 5.4 -> GATE PASS (21 Oct 11:5x)
- [x] 5.4: the gated build is identical to published v12 (compared 21 Oct 11:5x) - no republish needed
- [waiting: 5.3 - Word file and PDF fetched from Drive 21 Oct 11:42; the user to say when to build it (earlier: "5.5 and 5.3 still to do later"); its photos need faces blurred first]
- [waiting: 5.5 - Word file and PDF fetched from Drive 21 Oct 11:42; the user to say when to build it]
- [x] 5.4 finished (user 15:14 "is finished zip"): zip sent 15:1x, gated build 54ad53f13c7b = preview v15; folder beginning-of-the-year-for-teachers
- [x] 5.1 rebuilt (user 15:13 "yes"): "Office" 40 above (template rule), gate PASS 5a68c81037b0, preview v7; the live Staff page still has the old build until a new zip is uploaded
- [x] 5.1/5.2 phone footer: user "choose the option that works" - 35.2 for pages ending in text, 40 for pages ending in a photo (check_page.py); 5.1 gate PASS (21 Oct 14:0x)
- [x] 5.4 name-card drawing from the original Word file at full resolution (the PDF inside image1.emf, 400 dpi), the child's photos blurred inside it; gate PASS, preview v13 (21 Oct 14:2x)
- [x] 5.4 dashes (user 14:09 "correct the dashes", "that's the only edit. go"): the 14 dashes Word writes against a word get a space each side (DASH_SPACES); "second- and third-year" kept; gate PASS, preview v13
- [x] 5.1 and 5.2 gated again with the merged tools (21 Oct 14:2x): 5.1 PASS, same file as before (84d5f6abb149); 5.2 PASS, page identical to published v7 apart from the artifact wrapper
- [waiting: mm-gate - replace the end-of-turn rule (skipped by cc-plugin-sec-default) with a "start a new turn when QUEUE.md has open work" rule; needs the user to write "unlock gate"; do it only on the user's "go" (21 Oct 12:20)]
- [x] 5.5 queued edits 1-17 made (user 12:07 "you go ahead", no gate - user 12:07 "B"); preview v3 published 12:32 (https://claude.ai/artifact/GZ1WLXygkAB8LSXF9WNJBa). Was: [waiting: 5.5 queued edits (user 22 Oct 11:28-11:56, "Queue the following edits. Make no changes"), to be made only on the user's "go":
  1. "The aim of a faculty observation" -> "The Aim of a Faculty Observation", styled like the other blue headings
  2. 40 above (letters to letters) each numbered bold line: Observe daily / Daily reflect and objectively review / Maintain records regularly / Prepare individual and/or class plans and goals / Focused Observations
  3. 25 under every blue heading (letters to letters), including Week 1 and The Aim of a Faculty Observation
  4. intro line ends "...the two next examples, excerpted from 'The Bloomsbury Handbook of Montessori Education', Chapter 22, *Assessment in Montessori Education*, by Susan Zoll, Laura Saylor, and Arya Ansari:"
  5. Patell quotation: at the margin, no first-line indent, justified, body line spacing; ends "...development." (Patell, Hilla. 2016. *Observation*. The NAMTA Journal 41 (252))" - the separate "- Patell..." line goes
  6. "As a physician..." quotation: at the margin, no first-line indent, justified, body line spacing (ends "as necessary". (Montessori 2012)")
  7. delete the "Both quotes are from The Bloomsbury Handbook..." paragraph
  8. intro line to "To minimise bias...": the space above each block = the paragraph spacing
  9. everything under "Montessori Teacher-Training Observations": body-text line spacing, not quotation spacing ("yourselves." (Montessori 2013, 20)" keeps the full stop inside - user 11:43 "inside")
  10. "The National Center for Montessori in the Public Sector" heading blue (25 under, edit 3); the Resources source name stays red
  11. "Post-Observation Discussions" blue (25 under)
  12. all six Dartmouth College PDF badges in one column, 24 after the longest badged title (431.6 from the margin at 1280); phones: 24 after each title
  13. Berk and Toronto badges in one column (414.8 at 1280)
  14. both Teachstone badges in one column (456.2 at 1280)
  15. move the "Journal of Educational Supervision" entry to directly above "The Froebel Trust"
  16. one column for the badges of Learning Journals, Arda Arikan, Maryellen Weimer, Yale-NUS, Montessori in Action (536.8 at 1280)
  17. Busy Bee PDF badge back to the blue of every other badge (outline and letters)
  Only the groups the user shows share a PDF column (user 11:55). Open question: the user has not yet answered whether a full-page look at 1280 and 390 plus a separate-agent review is added after the gate]
- [x] 5.5 third queue, edits 1-9 made (user 12:52 "go"); preview v4 published 13:00 (https://claude.ai/artifact/GZ1WLXygkAB8LSXF9WNJBa); edit 8 also gives "Observe daily" 20 under "Essential Practices for Class" (the later instruction). Was:
  1. the NCMPS picture (image1.jpg, beside "NCMPS have developed a selection...") 100 high (now 72.4 at 1280); its bottom stays level with the bottom of the letters of "...all of the important elements." (already settled: BOTTOM_ON, user 22 Oct "Bottom of image = bottom of ... important elements"), so its top moves up
  2. "I ‘ve used their" -> "I’ve used their" (Word has a space and an opening quote; user 12:37 "I've")
  3. the quotation "“Observations of children engaged in activities..." at the margin, no first-line indent (now 48, Word's), as edits 5 and 6 of 11:28-11:56 for the other quotations (user 12:40 "already settled")
  4. "Sweep & Scan" and "Regular Intervals" not bold, still underlined (user 12:41 "NOT BOLD UNDERLINED"); the letters "a." and "b." not bold either (user 12:43)
  5. "Purpose" (the line "Purpose - To practice observing children...") not bold, its " -" too (they are one bold run) (user 12:43)
  6. "Classroom Observation Practices" in the centred line "MH and WHQ Classroom Observation Practices  Beginning March 1, 2022": text colour, not blue (user 12:44)
  7. "MH and WHQ Classroom Observation Practices" underlined (the words before the tab; "Beginning March 1, 2022" not) (user 12:44)
  8. every bold line 40 above / 20 below, letters to letters (user 12:48 "all bold: 40/20"): Essential Practices for Class; Notes on keeping an observation journal; General Guidelines to consider; Some questions you might start with (bold, its ":" plain as Word); Peer Evaluation and Self-Evaluation (replacing their 30/15 from the first batch). Not a. Sweep & Scan / b. Regular Intervals (not bold after edit 4)
  9. the Journal of Educational Supervision and The Froebel Trust PDF badges in one column, 24 after the longer title (740.3 from the margin at 1280; the Froebel badge moves from 701.9) - as the other groups the user showed (user 12:48, screenshot)]
- [x] 5.1, 5.2, 5.4: finished, left as they are - no rebuild on the updated Resources template (user 22 Oct 14:20)
- [waiting: 5.3 - being finished in another chat; note claude/NOTE-5.3-22-oct.md (user 14:20)]
