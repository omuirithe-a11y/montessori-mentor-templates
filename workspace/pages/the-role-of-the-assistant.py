# 2.1.2 The Role of the Assistant - settings (22 Oct 2026)
# User 22 Oct 21:58: the Essay Code Template; no Resources-template part; the hero of The Role of the Adult; faces blurred.
# Faces: the user's answer to the round 1 sheet, 22 Oct 22:05 (faces/review.json).

# 22 Oct 2026 23:15: the user updated the Word file and PDF in Drive; Word renamed the photos (same pictures) - names here are the new ones
# (faces/rename-23.json: new name <- old name; blurred copies in faces/photos-23)
# user rule 21 Oct ("every photo on every page includes a description"): each photo described from the photo itself  [REPLACED 28 Oct: no descriptions]
# 23 Oct 2026 11:4x: the user's new Word file (20 photos, Drive 09:23). The 8 photos kept from 22 Oct keep their descriptions
# (matched by picture); the 4 removed photos' descriptions are dropped; the 12 new photos are described from the photos themselves
ALT_TEXT = {}   # 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere

# 22 Oct 2026 23:16 (user, queued): "remove the table of contents"
NO_TOC = True

# 23 Oct 2026 09:47: the phone left-align rule set here at 07:24 is now in both templates (mm-phone-left, user: "I agree to these changes to the Essay Template and the Resources Template")

# 22 Oct 2026 23:33 (user: "fix the page" - the differences from the Essay Code Template, 23:31 answer)
CSS = """
/* the Word file's green heading ("Resources", #00B050) in Word's green - the Essay template has no green
   heading style, so it was drawn blue and the template's blue-heading spacing (Item 7, which measures from the last line of
   text and skips the photo row between) pulled the Resources section 442px up over the last photo row */
/* 22 Oct 2026 23:46: drawn as 5.3's green "Resources" heading (the user's approved look for a green Resources heading) */
html body main h2.mm-hc-00B050{color:#00B050 !important;border-bottom:2px solid #00B050 !important;padding-bottom:8px !important;font-size:20px !important;font-weight:400 !important}
"""

# 22 Oct 2026 23:45 (user: "one comma"): Word's "By Maria Montessori, , first published" with one comma
TEXT_EDITS = [('Montessori,, first', 'Montessori, first'),
              # 23 Oct 2026 12:40 (user: "correct the three typos"):
              ('and it they want to chat', 'and if they want to chat'),
              ('this one from is Mater Amoris', 'this one is from Mater Amoris'),
              ('“new teacher”.“', '“new teacher”.”')]   # 23 Oct 2026: the "Resources" heading rename (22 Oct 23:57) is now in the Word file itself

# 22 Oct 2026 23:49 (user: "A"): headings Word links keep Word's underline (no setting needed - the build keeps it)

# 22 Oct 2026 23:58 (user): "Line 1: Working With Your Assistant [PDF] / Line 2: By M. Shannon Helfrich, a concise, actionable playbook etc"
BLOCK_HTML = [
 ('Working With Your Assistant', '<span class="mm-wcol" style="color:#0432FF">Working With Your Assistant</span><a class="pdf" href="https://montessoridigital.org/file/1927/download?token=cqxOK9Gm" rel="noopener" target="_blank">PDF</a>', None),
 ('A concise, actionable playbook', 'By M. Shannon Helfrich, a concise, actionable playbook for building a respectful, effective guide-assistant team, stressing collaboration, mutual respect, and purposeful role definition in order to preserve child independence, leverage the assistant’s strengths, and create a warm, consistent environment for children.', None),
]

# 23 Oct 2026 00:00 (user): "Resources section: dividers 30/30 between the elements" - a beige line before each element after the first
RULE_BEFORE = ['Working With Your Assistant', 'Montessori Assistant Job Description', 'The Role of the Montessori Assistant in the Intangible Environment', 'The New Mistress']
# the two blue headings after a beige line: the template's Item 7 (40 under the text above, measured past the line) put them 1-6 below
# the line; a space of their own (data-space) keeps Item 7 off them, so the line's own 30 below holds
SPACE_SET = [('The Role of the Montessori Assistant in the Intangible Environment', 30, None)]
# with the beige lines, the template's short-lines list rule took the Job Description entry's one-line description as a list line
# (20.4 under its title, baseline to capitals); the same 29.4 as the other two entries' descriptions
GAPS = [('There are many variations of this document', 29.4, None), ('By Maria Montessori', 29.4, None), ('“In 1998 at the AMI', 29.4, None)]   # 00:26 (user "yes"): the heading entry's description as far below as the other four   # 00:18: the New Mistress entry too, now a title line

# 23 Oct 2026 00:18 (user): "The New Mistress move the pdf so it is alongside the title, as it is in the others"
# 23 Oct 2026: PDF_TO_TITLE removed - the Word file now has The New Mistress's PDF on its title line, and the build makes the badge from it
