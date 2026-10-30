# 5.3 Classroom Management - settings (21 Oct 2026, rebuilt on the Essay Code Template)
# User, 21 Oct 10:07: headings "A" - the Essay Code Template's own headings (blue, 22px, blue line; phones 20).
# User, 21 Oct 10:08: the Resources part "A" - on this page, in the Resources template's style (red source, blue italic
#   title, PDF badges, description), under its green heading.
# User, 21 Oct 10:11: the cut-off sentence ends "disputes in Montessori classes." (the Word file in Drive is unchanged).
import os
_here = os.path.dirname(os.path.abspath(__file__))   # not a page setting: this file's folder, to read admin-common.css (the template's red-heading lines)
# admin-common.css without its first line (the 18px no-line heading rule of 20 Oct 15:00, replaced by the user's "A")
# 21 Oct (user: "correct each of them to follow the template"): only its red-heading colour lines are kept (sanctioned "Red headings: keep");
#   its photo-beside-text height 150 and italic lines are dropped - the template's own rules apply
_admin = '\n'.join(l for l in open(os.path.join(_here, 'admin-common.css')).read().split('\n')[1:] if 'mm-hc-' in l)   # labels regular, as the template sets them

# the Resources part as the Resources template's entries
RES_FROM = 'Resources'

# 21 Oct 12:19 (user "correct all faults"): the text after each label in one column, wrapped lines under the text, as the PDF
# 22 Oct 2026: the label column is now found from Word by the build (was ALIGN_LABELS = ['Responsibility:', 'Right:'])

# lists at Word's own indents (the rule set on 5.4, 20 Oct 21:3x, "fix them"; checked by K)
WORD_LIST_INDENT = True

# 20 Oct 2026 (user, preferences): "numbered lists always start at the left margin" - each numbered list moved left so its numbers stand at the margin
OL_AT_MARGIN = True

# the book cover beside its entry starts level with the first line beside it (the Essay template's glTopline)
FLOAT_TOPLINE = True

TEXT_EDITS = []   # user 21 Oct 10:11 ("disputes in Montessori classes."): 22 Oct 2026 the Word file in Drive now has the whole sentence, so the change is no longer needed (it added "classes." twice)

# the PDF badges on neighbouring lines stand in one column (the Resources template's rule, 20 Oct 19:1x)
BODY_END = ['pdf-column.html', 'res-live.html']   # swipe-middle.html is in the templates from 22 Oct 2026   # res-live: user 21 Oct 13:40 "use culture resources live page to build the resources section" - its live figures

# The Resources part: the Resources template's look, only inside the section under the green "Resources" heading
_R = 'html body main section:has(> h2.mm-hc-00B050)'
_res = '''
{R} > h2{{color:#00B050 !important;border-bottom:2px solid #00B050 !important;padding-bottom:8px !important;font-size:20px !important;font-weight:400 !important}}
{R} .res-entry{{margin:0 0 8px}}
{R} .res-entry h3.material-name{{font-family:var(--serif);font-size:18px !important;font-weight:400 !important;color:#EE0000;border-top:0;padding-top:0;margin:32px 0 0 !important}}
{R} .res-entry h3.material-name a{{color:#EE0000 !important}}
{R} .res-item{{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:24px;row-gap:4px;margin:4px 0}}
{R} .res-item .res-title,{R} .res-item .res-title em{{font-style:normal !important;color:#0432FF}}   /* as Word and as the Resources template shows it (its main *{{font-style:normal}} wins) */
{R} .res-item .res-title a,{R} a:not(.pdf),{R} a:not(.pdf) *{{color:#0432FF !important}}
{R} .res-desc{{margin:4px 0 !important;color:#000}}
{R} .res-item .meta{{color:#000;font-size:18px}}
{R} a.pdf,{R} span.pdf{{display:inline-block;vertical-align:.12em;font-family:var(--sans,sans-serif);font-size:11px;font-weight:400;letter-spacing:.06em;line-height:1;padding:4px 6px;border:1.5px solid #0563C1;border-radius:2px;color:#0563C1 !important;text-decoration:none}}
{R} a.pdf:hover{{background:#0563C1;color:#fff !important}}
{R} p a.pdf{{margin-left:24px}}
@media (max-width:640px){{{R} > h2{{font-size:19px !important}}{R} .res-entry h3.material-name,{R} .res-desc,{R} .res-item .meta{{font-size:17px !important}}}}
'''.format(R=_R)

CSS = _admin + _res

# Word's near-black greys (#1A1A1A, #222222) shown in the template's text colour
GREYS_TO_INK = True

# 21 Oct 11:25 (user "go" on the queued edits):
# 19 "The blue headings such as Why and When to Interrupt Children - remove the lines, reduce font size to 20"; user 21 Oct 20:49 "sub-headings 18" and 20:51 "red headings 18" (all widths 18) (template steps 22 -> 20 on phones; here 20 -> 18)
# 22 "Red headings: keep. remove the divider above and the blue line beneath"
CSS += """
html body main h2.mm-hc-0432FF,html body main .section h2.mm-hc-0432FF{font-size:18px !important;border-bottom:0 !important;padding-bottom:0 !important}
html body main h2.mm-hc-EE0000,html body main h2.mm-hc-FF0000,html body main .section h2.mm-hc-EE0000,html body main .section h2.mm-hc-FF0000{border-bottom:0 !important;padding-bottom:0 !important}
@media (max-width:640px){html body main h2.mm-hc-0432FF,html body main .section h2.mm-hc-0432FF{font-size:18px !important}}
"""
NO_DIVIDER_BEFORE = ['00B050']   # user 21 Oct 11:25 no divider above the red headings; 13:34 lines back above the other two; 19:38 "remove the divider above Resources" (its heading is Word's green 00B050)
# 20 "Space under each 'Right' = 40"
SPACE_AFTER = [('Right:', 40)]   # user 21 Oct: "Space under each 'Right' = 40"
# 21 the template's "3 or more short lines are a list (14)" rule does not fit the Responsibility/Right pairs or the lines after
#    them: the line after each Responsibility and the paragraph after "Source." take the template's paragraph space, 23
SPACE_ABOVE = [('Right:', 23), ('There is a great deal of wisdom', 23)]

# 21 Oct 11:28 (user): "Delete the table of contents"
NO_TOC = True

# 21 Oct 12:19 (user "correct all faults"):
RES_ENTRIES_EQUAL = True      # the same space above every Resources entry (was tight from the seventh)
# EVEN_LIST_STEP not used: the engine measures letters to letters (user, 10:49), so the template's data-step cannot even the lines out
# 21 Oct 11:16 (user: "correct each of the unsanctioned divergences so your page follows the template"): labels regular, as the
# template sets them (Word has them bold) - the letter-by-letter check allows it on this page
LABELS_AS_TEMPLATE = True

# 21 Oct 13:40 (user "also execute the list of queued edits"):
UNDERLINE_LABELS = ['Discipline Problems', 'Dismissal', 'Monticello Montessori General Classroom Expectations']   # user 13:29, 13:32: underline
LINK_TEXT = [('Monticello Montessori', 'https://mmlions.org/')]   # user 13:31-13:32: a link to the school, the template's blue
SPACE_ABOVE += [('Any child can do a work', 23), ('Once again, these rules', 30)]   # user 13:33: 23 below the Monticello label ("a"); 30 above "Once again"
DIVIDER_SPACE = {'Managing children who are not yet normalised': (30, 30), 'Managing children who need help': (30, 30), 'Managing Colleagues': (30, 30)}   # user 13:34: "divider 30/30 above"; 20:45 the same above "Managing children who are not yet normalised"
CSS += """
html body main .micro-label.mm-ulab{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
html body main h2.mm-hc-EE0000,html body main h2.mm-hc-FF0000,html body main .section h2.mm-hc-EE0000,html body main .section h2.mm-hc-FF0000{font-size:18px !important}
@media (max-width:640px){html body main h2.mm-hc-EE0000,html body main h2.mm-hc-FF0000,html body main .section h2.mm-hc-EE0000,html body main .section h2.mm-hc-FF0000{font-size:18px !important}}
"""   # user 13:29/13:32 underline (the template's underline offset 3px); 13:35 "make the red headings 20" (phones 18, as the blue)
# 21 Oct (the 5.3 faces step in this chat, Claude by eye; 5d and 8b added by eye; photo 10, the book cover, not blurred) - the faces
# blurred on this page, which the faces check (rule P2) holds the page to; the user has not yet been shown this list
FACES_BLUR = ['1a', '1b', '1c', '1d', '2a', '2b', '3a', '3b', '4a', '4b', '5a', '5b', '5c', '5d', '8a', '9a']   # user 22 Oct 14:57: 6a and 8b not blurred ("none of those children need to be blurred")

# 21 Oct 2026 18:3x (START-HERE finishing list 7, "photo descriptions"): each photo described for screen readers, from the photo itself  [REPLACED 28 Oct: no descriptions]
ALT_TEXT = {}   # 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere

# 21 Oct 2026 18:4x (user: "fix the faults on the page"), the user's standing rules for every page, where the Essay template differs:
CSS += """
/* 22 Oct 2026: numbered list items justified, the menu line and swipe centring are now in the templates (user: "do all of this", "B") */
"""

# 21 Oct 2026 18:4x (user: "fix the faults on the page"; the Essay template is not changed without "I agree to these changes to the Essay Template"):
# the beige line's own space measured from the letters of the line above, not its line box (390: 34.5 above the line before "Managing Colleagues", want 30)
# 22 Oct 2026: the beige-line spacing fix (user 21 Oct 18:11) is now in the Essay template
PAGE_CODE_REPLACE = []

# 21 Oct 2026 (user 13:4x: phones take the mean of the live pages): at 390, banner to the first letters 42 and the last letters to the footer band 35.2
PHONE_GAPS = (42, 35.2)

# user 21 Oct 19:26-19:41 (queued, "go" 19:43), spaces letters to letters:
SPACE_SET_21_OCT = [
 ('Source.', 20, 40),   # 19:27 "20/40"
 ('Discipline Problems', 40, 15), ('Dismissal', 40, 15), ('Monticello Montessori General Classroom Expectations', 40, 15),   # user rule 21 Oct: underlined lines 40 above / 15 below; 19:32 "15"
 ('\u2018One-up, one-down\u2019', (52, 54)), ('\u201cMy child, my problem.\u201d', (52, 54)),   # user 19:38 "double the space above both": 26 at 1280, 27 at 390 measured 19:4x
]
HEAD_GAP = {'0432FF': 15}   # user 19:36: "15" under the blue sub-headings
RES_DIVIDERS = True   # user 19:39-19:40: "divider between each element in resources", "30/30"
DROP_PHOTOS = ['image12.jpeg']   # user 19:39: "delete the positive discipline photo"
TEXT_EDITS = TEXT_EDITS + [('\u201cMy child, my problem.\u201d', '\u2018My child, my problem.\u2019')]   # user 19:38: "use '' and not \"\""
PAGE_CODE_REPLACE = PAGE_CODE_REPLACE + [   # user 19:38: "change from italics to bold"
 ('<em>\u2018One-up, one-down\u2019 </em>', '<strong class="mm-bold">\u2018One-up, one-down\u2019 </strong>'),
 ('<em>\u2018My child, my problem.\u2019 </em>', '<strong class="mm-bold">\u2018My child, my problem.\u2019 </strong>')]
FORMAT_EDITS = ['\u2018One-up, one-down\u2019', '\u2018My child, my problem.\u2019']   # user 19:38: bold, not Word's italic (the formatting check allows these two)
CSS += """
/* user 21 Oct 19:38: these two labels bold (the template sets labels regular) */
:root body main .micro-label strong.mm-bold{font-weight:700 !important}
"""
# 22 Oct 2026: the underline-position fix (user 21 Oct 19:31-19:32) is now in the Essay template

# ===== 22 Oct 2026 (the Essay template now has the 5.5 spacing, letters to letters - user 14:24 "I agree to these changes to the Essay Template"):
# the user's 21 Oct figures above, held letters to letters (baseline above to the top of the capitals below) by letter-gaps, as every 22 Oct figure;
# the Essay engine's data-space measured from the tails of the letters above and gave 5-6 more. Later settings win, as before (SPACE_SET over SPACE_ABOVE).
SPACE_ABOVE = [x_ for x_ in SPACE_ABOVE if x_[0] != 'Right:']   # "Right:" lines: GAPS_EACH below
SPACE_AFTER = []                                                # "Space under each 'Right' = 40": GAPS_EACH below
GAPS = [('Once again, these rules', 30)]   # user 13:33: 30 above "Once again". The 21 Oct 23 above "There is a great deal of wisdom" and "Any child can do a work" are not carried over: the user's later figures set those spaces (19:27 40 below "Source."; 19:32 15 below the Monticello label)
GAPS += [tuple(x_) + (None,) * (3 - len(x_)) for x_ in SPACE_SET_21_OCT]   # Source. 20/40; the three underlined labels 40/15; 'One-up' and 'My child' 52 (phones 54)
GAPS_EACH = [('Right:', 23, 40)]                                # 23 above each "Right:" (the 21 Oct setting), 40 under it (user 21 Oct)
SPACE_ABOVE = []
CSS += """
/* 22 Oct 2026: "The teacher should intervene before..." starts with a tab in Word (no indent): Word shows its text at 48, as the
   other quotations' first lines. The template's first-line 48 plus the tab put it at 96; the tab alone takes it to 48 */
:root body main blockquote.pullquote p.mm-form{text-indent:0 !important}
:root body main blockquote.pullquote:has(> p.mm-form) cite:has(> .mm-t:first-child){padding-left:0 !important}   /* its attribution starts with a tab too: at 48, as the others */
"""
CSS += """
/* 22 Oct 2026: the three underlined labels stay regular weight, as the user reviewed them on 21 Oct (underline added 13:29-13:32 to the
   regular labels) - the Essay template's new "Word's black bold labels stay bold" does not apply to them; underlined lines are not bold
   (5.5, user 12:41 "NOT BOLD UNDERLINED") */
:root body main .micro-label.mm-ulab{font-weight:400 !important}
"""
GAPS += [('Materials for Trainers', 40), ('Supporting Materials', 40)]   # user 21 Oct 19:41: a bold line inside an entry 40 above - letters to letters (res-live measured it from the PDF badge's bottom: 47 / 45.7)
CSS += """
/* 22 Oct 2026: a Resources title line ending in a PDF or MP4 badge is not justified - with its last word kept beside the badge on
   phones, justifying it spread the words across the line (Resources template style, user 21 Oct 10:08 "A": its title lines are not justified) */
html body main p.res-desc:has(> span.mm-bj, > a.pdf){text-align:left !important}
"""
