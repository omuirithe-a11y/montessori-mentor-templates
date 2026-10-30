# 20 Oct 2026: Administration pages on the Resources template; headings 18, no line (user, 15:00), in their Word colour; Resources heading green as the template
import os
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-common.css')).read()
# 22 Oct 2026: the NCMPS sheet and the Leuven Scale chart are placed beside their text by the build itself, from the PDF (was BESIDE)
# Day 4: "child to do so?" is its own Word paragraph; the PDF shows it as the second line of the bullet above
JOIN = ['child to do so?']

# the Resources part as the Resources template's entries (red source, blue italic title, PDF badges, description)
RES_FROM = 'Resources'

# 21 Oct 2026 (as Word and the PDF): Motivation / Concentration / Social development - the labels in one column, their text
# lined up after them (Word's tabs), the lines 24px in from the margin (Word: left indent 360 twips = 24px)
# 22 Oct 2026: the label column is now found from Word by the build (was ALIGN_LABELS)
# CSS += 'main p.mm-hanglab{margin-left:24px !important}'   # 22 Oct 2026 edit 5 (user: "start the labels on the margin"): the 24 in from the margin dropped
LABEL_COL = '185px'   # 22 Oct 2026 edit 5 (user, queued): the text column at 185, wrapped lines at 185 (computers; phones: label then text, as before)
# 21 Oct 2026 (user's rule 21 Oct 13:4x: phones take the mean of the live pages - 35.2 from the last letters to the footer band
# for a page that ends in text; banner to first letters 42, the page check's settled phone figure): the template's own phone
# footer script spaces from the line box and gives 33 here, where the last entries have the Resources template's taller lines
PHONE_GAPS = (42, 35.2)
# 20 Oct 2026 (user rule: "numbered lists always start at the left margin") - the number-to-text gap is the open A/B
# question from the 5.3 chat, not decided here
OL_AT_MARGIN = True   # user rule, 20 Oct 2026

# 21 Oct 2026 (user rule: "every photo on every page includes a description (alt text), from now on"): words from the pictures
ALT_TEXT = {   # user rule 21 Oct (photo descriptions); words from the pictures themselves
 'image1.jpg': 'The NCMPS rubric sheet, Observing in the Prepared Environment, a form with rows of criteria and tick boxes',
 'image2.png': 'The Leuven Scale chart: five levels of involvement, from extremely low to extremely high, with descriptions, key indicators and examples',
}

# gaps the user approved (the gap check U skips them), by the start of the line above the gap:
U_ALLOWED = [   # user 22 Oct 04:06 ("NCMPS picture ... 128.6 ... - ok") and 04:07 ("Word's 12pt space after a line ... 14 on the page for each 6pt in Word - ok")
 'NCMPS have developed a selection', 'Social development', 'MH and WHQ Classroom Observation',
]

TITLE = 'Observations - Faculty'   # user 22 Oct 04:08 "Hero title: \"Observations - Faculty\"." - Word's own title line (the menu entry stays "Observations for Teachers")

# ===== 22 Oct 2026: the user's 20 queued edits (queued 09:31-10:1x, "do it" 10:24) =====
BODY_END = ['res-extra.html', 'letter-gaps.html']   # edits 2 and 18 (res-extra), the spaces letters to letters (letter-gaps)
# edit 1 (user: "change all of these to 20", "B"): 20 under these headings and bold lines, letters to letters ("Week 1" keeps 40 above "Day 1")
GAPS = [(h_, None, 20) for h_ in [
 'Observing the Physical Environment', 'Observing Children', 'The Leuven Scale', 'Observing my own class',
 'Classroom Observation and Planning Expectations', 'Montessori Teacher-Training Observations', 'Week 2', 'Week 3',
 'Qualities of an Effective Peer Classroom Observation',
 'The National Center for Montessori in the Public Sector', 'Faculty-to-Faculty Observations', 'Post-Observation Discussions',
 'a. Sweep & Scan', 'b. Regular Intervals', ]]
GAPS += [
 ('For what it\u2019s worth', 30),                               # edit 12 (user: "space 30 above")
 ('Unfortunately, I haven\u2019t recorded', None, 30),           # edit 16 (user: "space 30 below")
]
RULE_GAP = 30   # user 22 Oct 10:55: "switch them to exactly 30/30 letters to letters"; 10:56 "only the letters" - every beige line on this page
BOTTOM_ON = {'image1.jpg': 'important elements'}   # edit 2 (user: "Bottom of image = bottom of ... important elements")
TEXT_EDITS = [
 ('all of the important elements,', 'all of the important elements.'),                           # edit 3
 ('adjust the environment as necessary. ', 'adjust the environment as necessary\u201d. '),        # edit 8 (user: "environment as necessary\". (Montessori 2012)")
 ('accomplish in yourselves\u201d', 'accomplish in yourselves.\u201d'),                           # edit 9 (user: "accomplish in yourselves.\u201d (Montessori 2013, 20)")
 ('(Montessori 2013, 20).', '(Montessori 2013, 20)'),                                           # edit 9
]
# edit 4 (user: "Correct these attributions including adding the correct offset"): each on its own line, 48 in, the title in italics
BLOCK_HTML = [
 ('Retrieved from https://www.structural-learning.com', '- Paul Main, <em>Leuven Scale: A teacher\'s guide</em>. (2021)', 'padding-left:48px !important;text-indent:0 !important'),
 ('- \u2018Bringing the Montessori Approach', '- Barbara Isaacs, <em>Bringing the Montessori Approach to your Early Years Practice</em>. (2007)', 'padding-left:48px !important;text-indent:0 !important'),
]
TEXT_EDITS += [(' - Main, P (2021, November 03). Leuven Scale: A teacher\'s guide.', ''),   # user: edit 4, the attribution moved to its own line (above)
 ('Retrieved from https://www.structural-learning.com/post/leuven-scale-a-teachers-guide', "- Paul Main, Leuven Scale: A teacher's guide. (2021)"),   # user: edit 4 (the line itself is set by BLOCK_HTML; this tells the word checks)
 ('- \u2018Bringing the Montessori Approach to your Early Years Practice\u2019, Barbara Isaacs.', '- Barbara Isaacs, Bringing the Montessori Approach to your Early Years Practice. (2007)')]   # user: edit 4, as above
LABEL_LETTER = [('a. Sweep & Scan', 'a.'), ('b. Regular Intervals', 'b.')]   # edit 6 (user: "offset lettered lists as dashes are offset")
NO_BOLD = ['as it happens', 'are', 'signed', 'group activities']   # user: edits 13 ("no bold in this text") and 14 ("no bold")
FORMAT_EDITS = NO_BOLD + ["Leuven Scale: A teacher's guide", 'Bringing the Montessori Approach to your Early Years Practice']   # the formatting check allows these changes from Word
RULE_BEFORE = ['Careful, systematic, rigorous', 'Faculty-to-Faculty Observations']   # edits 11 and 15 (user: "divider 30/30 above")
RES_DIVIDERS = 'all'   # edit 19 (user: "divider 30/30 for red headings in resources only") - the first entry too
RES_SPLIT_ITEM = ['Busy Bee Montessori Center']   # edit 20 (user: "correct this", Busy Bee a red name line with its PDF badge)
PLAIN_COLOUR = ["Valerie Polakow"]   # user: edit 20, "Valerie Polakow" in the text colour
CSS += """
/* edit 6: the letter 24 in from the margin, its words 24 after it; the paragraphs under it at the margin */
html body main .micro-label.mm-lettered{padding-left:24px !important}
/* edit 7 (user: "do not offset these quotations"): no side offset; first line 48 as Word; the attribution 48 */
:root body main blockquote.pullquote{margin-left:0 !important;margin-right:0 !important}
:root body main blockquote.pullquote p{text-indent:48px !important;padding-left:0 !important}
:root body main blockquote.pullquote cite{padding-left:48px !important;text-indent:0 !important}
/* edit 20: a badge on a name line stands 24 after the name */
html body main h3.res-src a.pdf{margin-left:24px}
"""

# ===== 22 Oct 2026: the user's second queue (11:28-11:56, "Queue the following edits"; built on the user's "go ahead" 12:07) =====
MAKE_HEADING = [('The aim of a faculty observation', '0432FF', 'The Aim of a Faculty Observation')]   # q1: title case, a blue heading
HEAD_COLOUR = {'The National Center for Montessori in the Public Sector': '0432FF', 'Post-Observation Discussions': '0432FF'}   # q10, q11 (the Resources source name stays red)
HEAD_GAP = {'0432FF': 25}   # q3: 25 under every blue heading, letters to letters (Week 1 and the Aim included)
GAP_LI = [(w_, 40) for w_ in ['Observe daily', 'Daily reflect and objectively review', 'Maintain records regularly',
                               'Prepare individual and', 'Focused Observations']]   # q2: 40 above each numbered bold line; "Observe daily" 40 too (user 13:18 "make the space above bold items the same")
BLOCK_HTML += [('There\u2019s a great deal of literature on the topic of observation',
  'There\u2019s a great deal of literature on the topic of observation, a lot of it along the lines of the two next examples, excerpted from \u2018The Bloomsbury Handbook of Montessori Education\u2019, Chapter 22, <em>Assessment in Montessori Education</em>, by Susan Zoll, Laura Saylor, and Arya Ansari:', None),   # q4
 ('Both quotes are from', None, None)]   # q7: deleted
UNQUOTE = [('\u201cMontessori teacher education', 'cite'),   # q5: at the margin, body text; the Patell line after it in brackets
           ('\u201cAs a physician and a scientist', None)]    # q6: at the margin, body text
MOVE_ENTRY_BEFORE = [('Journal of Educational Supervision', 'The Froebel Trust')]   # q15
PDF_GROUPS = [['Gina Peterson', 'Dartmouth College', 'Ronald A. Berk', 'The Centre For Teaching Support', 'A. M. Joosten', 'Teachstone'],   # user 13:37: one column from "Observation And Assessment In Early Childhood Education" to "What To Expect When You're About To Be Observed?"
              ['Learning Journals', 'Arda Arikan', 'Maryellen Weimer', 'Yale-NUS', 'Montessori in Action']]   # q12, q13, q14, q16
CSS += """
/* q17: the Busy Bee badge in the blue of every other badge (letters and outline) */
html body main h3.res-src a.pdf{color:#0563C1 !important;border-color:#0563C1 !important}
html body main h3.res-src a.pdf:hover{color:#fff !important}
/* q5, q6: the two quotations as body text at the margin, italic as Word */
html body main p.mm-unq{font-style:italic !important;text-indent:0 !important;margin-left:0 !important;padding-left:0 !important}
"""

# ===== 22 Oct 2026: the user's third queue (12:37-12:48), built on the user's "go" 12:52 =====
IMG_FILL_GAP = {'image1.jpg': 30}   # e1 (user 12:37 "make that image 100 high", 13:17 "164.1 high"; 13:40 "fill the space above, 30 below the line above" - every width, its bottom on the "important elements" line)
TEXT_EDITS += [('I \u2018ve used their', 'I\u2019ve used their')]   # e2 (user 12:37 "I've"; Word has a space and an opening quote)
NO_FIRST_INDENT = ['\u201cObservations of children engaged']   # e3 (user 12:40: at the margin, as the other quotations, edits 5 and 6)
NO_BOLD += ['Purpose -']   # e5 (user 12:43 "Purpose - not bold")
LATE_HTML = [('MH and WHQ Classroom Observation Practices',
  '<u>MH and WHQ Classroom Observation Practices</u><span class="mm-t">\u2409</span>Beginning March 1, 2022')]   # e6 (user 12:44 "not blue"), e7 (user 12:44 "underline")
GAPS += [(w_, 40, 40) for w_ in ['Essential Practices for Class', 'Notes on keeping an observation journal', 'General Guidelines to consider',
                                 'Some questions you might start with', 'Peer Evaluation', 'Self-Evaluation']]   # e8 (user 12:48 "all bold: 40/20"; Peer/Self were 30/15; 13:35 "Space under the bold lines = 40")
PDF_GROUPS += [['Journal of Educational Supervision', 'The Froebel Trust']]   # e9 (user 12:48, screenshot)
CSS += """
/* e4 (user 12:41-12:43): a. Sweep & Scan, b. Regular Intervals not bold, letters included; still underlined */
html body main .micro-label.mm-lettered,html body main .micro-label.mm-lettered *{font-weight:400 !important}
"""
HEAD_ABOVE = {'0432FF': 40}   # user 13:30 "Space above the blue lines, outside Resources = 30"; 14:00 "change all to 40/25" (25 below: HEAD_GAP)
TEXT_EDITS += [('To practice observing', 'To practise observing')]   # site rule: UK English (the verb), preferences 13 Oct
GAPS += [('a. Sweep & Scan', 40, None), ('b. Regular Intervals', 40, None),   # site rule 21 Oct: underlined lines 40 above / 15 below (their 20 below: user, first batch)
         ('Day 1', None, 15), ('Day 2 and 3', 40, 15), ('Day 4', 40, 15)]    # (Day 1's above is the 25 under "Week 1": user edit 3)
