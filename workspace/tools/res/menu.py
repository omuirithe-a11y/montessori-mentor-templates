"""THE FULL MENU (5 Oct 2026, chat 12 - the user's list 1__Menu.docx and answers).
One source for the menu of every page: the data (MENU, PANELS, LIVE), the header HTML, the menu's extra CSS and script.
Rules (the user's words in quotes):
- the top bar keeps the one-word names ("I used the one word names for reasons of space, so lets go with them");
- no numbers ("don't show");
- Curriculum: each Resources page under its curriculum entry ("the answer is B");
- every entry is shown; one without a page yet is plain text, not a link ("The answer is A") - an entry becomes a link
  when its address is added to LIVE;
- Independence and Infant/Toddler - 0 to 3 are each ONE page (their PDFs go on that page, not in the menu);
- The History of Education: the user's four names, Comenius and Locke moved to Predecessors ("A ... agreed").
PANELS[m] = columns; a column = groups; a group = entries. '*Name' = the group's leading page (bold); '#Name' = a heading that is not a page."""
import html as H

SITE = 'Montessori Mentor'
MENU = ['Home', 'Essential Elements', 'Curriculum', 'Play', 'Administration', 'Parents', 'Education', 'Resources']
PANELS = {
 'Home': [[['Montessori Mentor', 'Why This Website?', 'Aun Aprendo', 'A Montessori Journey']],          # 5 Oct 2026 (chats 12, 14): the audience card's ten entries in its order ("yes"); 4 / 3 / 3 is Claude's choice, shown in preview 1 of the card. 7 Oct (chat 22): "1. Menu.docx" does not name 'Montessori Mentor' - KEPT, it is the live home page at /; put to the user.
          [['The History of Montessori Education', 'Biography', 'Timeline']],
          [['The First Casa dei Bambini', 'The Story of San Lorenzo', 'Glossary']]],
 'Essential Elements': [
          [['*Essential Elements', 'Essential Elements Resources'],
           ['*The Role of The Adult', 'The Role of The Adult Resources', 'The Role of the Assistant', 'Developing Responsibility', "Montessori's Advice to Teachers"]],
          [['*The Prepared Environment', 'Essential Characteristics - Theory', 'The Prepared Environment Resources', 'The Outdoor Environment', 'Anji Play'],
           ['*Mixed-Age Groups', 'Mixed-Age Groups Resources']],
          [['*The Uninterrupted Three-Hour Cycle', 'The Uninterrupted Three-Hour Cycle Resources'],
           ['*The Montessori Materials', 'The Montessori Materials Resources', 'The Montessori Materials Sourcing']]],
 # 7 Oct 2026 (chat 22), "1. Menu.docx": the seven curriculum names take their full titles; the Resources entry is
 # "Curriculum Resources"; "Developing Responsibility" is new under Practical Life; the English resources drop the
 # "English " prefix, 6 reads "Writing" and 7 "Articles, Books and Research".
 'Curriculum': [
          [['*The Montessori Curriculum', 'Scope and Sequence', 'Curriculum Resources'],
           ['*The Practical Life Curriculum', 'Developing Responsibility', 'Practical Life Resources'],
           ['*The Sensorial Curriculum', 'Sensorial Resources']],
          [['*The Culture Curriculum', 'Culture Resources'],
           ['*The Mathematics Curriculum', 'Mathematics Resources']],
          [['*The English Curriculum', 'Resources 1 - Montessori', 'Resources 2 - Oral Language', 'Resources 3 - Keys to Literacy',
            'Resources 4 - Reading', 'Resources 5 - The Pink, Blue and Green Series', 'Resources 6 - Writing', 'Resources 7 - Articles, Books and Research']]],
 # 7 Oct 2026 (chat 22): 'Play' (the section's audience card) leads the panel; the document does not name 'Types of
 # Play' (KEPT - the live essay), "Children's Outdoor Bill of Rights" or 'Mud Day' (both GONE, as the document has it).
 'Play': [[['*Play', 'Types of Play', 'Play Resources'], ['Outdoor Play: Varieties', 'Outdoor Play: Spaces and Resources'], ['Loose Parts']],
          [['Nature Play', 'Nature Play Spaces', 'Natural Playgrounds', 'Nature Play Resources', 'Forest School Lessons']],
          [['Junk Playgrounds History', 'Adventure Playgrounds']]],
 'Administration': [
          [['Staff', 'School Handbook', 'Classroom Management', 'Beginning of the year for Teachers', 'Observations for Teachers']],
          [['Lesson Planning', 'Montessori For All Lesson Planning', 'Checklists and Record Keeping', 'Assessment', 'Studies of Montessori Assessment']],
          [['Admissions', 'Observations for Parents', 'Progress Reports', 'Parent-Teacher Conferences', 'Children’s Portfolio']]],
 # 7 Oct 2026 (chat 22): 'Parent Resources' is new and leads the panel; the five page names take the document's wording.
 'Parents': [[['*Parent Resources'],
           ['Traditional v’s Montessori', 'Montessori at Home: Environment and Materials', 'Montessori at Home: Activities']],
          [['Independence', 'Infant and Toddler: Birth to 3']],
          [['Elementary: 6 to 12', 'The Silent Journey']]],
 # 23 Oct 2026 (user): 'Friedrich Fröbel' (was 'Froëbel').
 # 7 Oct 2026 (chat 22): 'The History of Education' is new and leads the panel; Comenius and Locke move from
 # Predecessors to Foundations (SUPERSEDES the "A ... agreed" of 5 Oct, chat 12).
 'Education': [
          [['*The History of Education'],
           ['#Foundations', 'The Roots of Montessori', 'Active Learning', 'Constructivism', 'John Amos Comenius', 'John Locke']],
          [['#Predecessors', 'Jean-Jacques Rousseau', 'Johann Pestalozzi', 'Friedrich Fröbel', 'Jean Marc Itard', 'Édouard Séguin']],
          [['#Contemporaries', 'John Dewey', 'Rudolf Steiner', 'Lev Vygotsky', 'Jean Piaget', 'A.S. Neill', 'Célestin Freinet']],
          [['#Modern Voices', 'Caleb Gattegno', 'Jerome Bruner', 'Haim G. Ginott', 'John Holt', 'MIT Guidelines on Learning']]],
 # 7 Oct 2026 (chat 22): 'Resources' is new and leads the panel.
 'Resources': [[['*Resources', 'Books by Montessori', 'Books by others', 'Resources and Links']]],
}
# A page that stands over all the columns of its panel (5 Oct: "there is an Administration page, an overview of this section. You choose how and where").
OVER = {'Administration': ['*Administration']}
# The pages that exist. (section, entry) -> address. Add a line here when a page goes live.
LIVE = {
 ('Home', 'Montessori Mentor'): '/',                      # from the card's upload: the Home AUDIENCE CARD (5 Oct 2026, chats 12, 14)
 ('Home', 'Why This Website?'): '/why-this-website/',   # the essay that was the home page ("The address ... /why-this-website/ ... Yes"; its name: "Why This Website?")
 ('Play', 'Play'): '/play/',                            # 7 Oct 2026 (chat 20): the Play AUDIENCE CARD; the document names it at the head of the Play panel (chat 22)
 ('Play', 'Types of Play'): '/play-varieties-and-characteristics/',   # 5 Oct 2026 (chat 13): 4.1 renamed and moved by the user; renamed "Types of Play" 7 Oct (chat 20)
 ('Curriculum', 'The Montessori Curriculum'): '/the-montessori-curriculum/',
 ('Curriculum', 'Scope and Sequence'): '/montessori-scope-and-sequence/',
 ('Curriculum', 'Curriculum Resources'): '/curriculum-scope-and-sequence-resources/',
 ('Curriculum', 'The Practical Life Curriculum'): '/the-practical-life-curriculum-2/',
 ('Curriculum', 'Practical Life Resources'): '/practical-life-resources/',
 ('Curriculum', 'The Sensorial Curriculum'): '/the-sensorial-curriculum/',
 ('Curriculum', 'Sensorial Resources'): '/sensorial-resources/',
 ('Curriculum', 'The Culture Curriculum'): '/the-culture-curriculum/',
 ('Curriculum', 'Culture Resources'): '/culture-resources/',
 ('Curriculum', 'The Mathematics Curriculum'): '/the-mathematics-curriculum/',
 ('Curriculum', 'Mathematics Resources'): '/mathematics-resources/',
}
# The top bar: a name is a link only when the section's own page exists.
TOP = {'Home': '/', 'Curriculum': '/the-montessori-curriculum/', 'Play': '/play/'}

CHEV = ('<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
        '<path d="M2.5 4.5 6 8l3.5-3.5"></path></svg>')
BURGER = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
          '<path d="M4 7h16M4 12h16M4 17h16"></path></svg>')

def section_of(url):
    for (m, t), u in LIVE.items():
        if u == url: return m
    return None

def header(current_url=None, active=None):
    """The whole header. current_url: this page's address (its entry and its section are marked); active: the section, when no address."""
    active = active or section_of(current_url)
    items = []
    for m in MENU:
        cur = ' aria-current="page"' if m == active else ''
        pid = 'p-' + ''.join(c for c in m.lower() if c.isalnum())
        cols = ''
        for col in ([[OVER[m]]] if m in OVER else []) + PANELS[m]:
            over = ' over' if (m in OVER and col == [OVER[m]]) else ''
            grps = ''
            for g in col:
                lis = ''
                for t in g:
                    kind = t[0] if t[0] in '*#' else ''
                    name = t.lstrip('*#')
                    if kind == '#':
                        lis += f'<li class="hd"><span>{H.escape(name)}</span></li>'; continue
                    cls = ' class="lead"' if kind == '*' else ''
                    u = LIVE.get((m, name))
                    if u:
                        here = ' aria-current="page"' if u == current_url else ''
                        lis += f'<li{cls}><a href="{u}"{here}>{H.escape(name)}</a></li>'
                    else:
                        lis += f'<li{cls}><span class="np">{H.escape(name)}</span></li>'
                grps += f'<ul class="grp">{lis}</ul>'
            cols += f'<div class="pcol{over}">{grps}</div>'
        top = (f'<a class="top" href="{TOP[m]}"{cur}>{H.escape(m)}</a>' if m in TOP
               else f'<a class="top np-top"{cur}>{H.escape(m)}</a>')
        cat = ' cat' if m in CATEGORY_PANELS else ''
        items.append(f'<li class="has-panel">{top}'
                     f'<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="{pid}" aria-label="Show the {H.escape(m)} pages">{CHEV}</button>'
                     f'<div class="panel{cat}" id="{pid}"><div class="panel-in c{len(PANELS[m])}">{cols}</div></div></li>')
    return ('<a class="skip" href="#content">Skip to the essay</a>'
            '<header class="site-head"><div class="site-head-in">'
            f'<a class="site-name" href="/">{SITE}</a>'
            f'<nav class="site-nav" id="site-nav" aria-label="Main"><ul class="menu">{"".join(items)}</ul></nav>'
            '<div class="site-tools"><button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open the menu">'
            f'{BURGER}</button></div></div></header>')

# Added after the page's own menu CSS (it overrides the three-column grid of groups and the old Curriculum placements).
# 7 Oct 2026 (chat 23): ONE SOURCE for the menu's blue - the site's blue heading colour as qa/settled_record.json
# records it ("the blue heading 20px #0432FF"). qa/menu_style_check.py imports MENU_BLUE from here; nothing holds a
# second copy of it.
MENU_BLUE = '#0432FF'
# 8 Oct 2026 - your answers to the two menu questions of 7 Oct (chat 23):
#   #73 "C" - on the phone (960px and under) the category titles are light blue #8FC6FF (the navy band hides #0432FF);
#   #74 "the three only" - the blue goes on the category titles of Essential Elements, Education and Curriculum only;
#       the other panels' leading entries keep the ordinary text colour.
MENU_PHONE_BLUE = '#8FC6FF'
CATEGORY_PANELS = ('Essential Elements', 'Education', 'Curriculum')
# The extra space between one category (group) and the next, desktop and phone alike (8 Oct 2026) - the one copy.
CAT_GAP = 22
# The phone's entries carry 7px above and below instead of the desktop's 8px, so the phone adds 2px more to give the
# same space letter to letter between one category and the next: 38px on both (measured 8 Oct on a copy of 3.1).
CAT_GAP_PHONE = CAT_GAP + 2

MENU_CSS = r"""
/* 6 Oct 2026 (chat 15), the user: "delete the lines from every panel in every menu" - no thin lines under the entries of ANY panel (5 Oct, chat 14: the Home panel only). */
.menu .panel li{border-bottom:0 !important}
/* THE FULL MENU (5 Oct 2026): columns of groups; a page that exists is a blue link, one not yet made is plain text */
.panel-in.c1{grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr)}
.panel-in.c4{grid-template-columns:repeat(4,minmax(0,1fr));gap:26px 40px}
.panel-in > .pcol{min-width:0;display:flex;flex-direction:column;gap:__CAT_GAP__px}
.panel-in > .pcol.over{grid-column:1 / -1;margin-bottom:-12px}
.grp a,.grp a[aria-current="page"]{color:var(--ink)}
.grp a:hover{text-decoration:underline;text-underline-offset:3px}
.grp .np,.grp .hd span{display:block;padding:8px 0;font-family:var(--serif);font-size:17px;line-height:1.3;color:var(--ink);cursor:default}
/* 7 Oct 2026 (chat 23), the user: "Essential Elements, education and curriculum have categories in their menus.
   The title of each category to be in blue. no bold to be used anywhere". A CATEGORY TITLE is a group's leading
   entry (li.lead) or a heading that is not a page (li.hd); it is now the site's blue, and NOTHING in the menu is
   bold. SUPERSEDES "no blue - ONE text colour in every panel, bold leads and headings" (5 Oct 2026, chat 12).
   Checked by qa/menu_style_check.py (MN3) in the gate, which reads the blue from MENU_BLUE below. */
.grp li.lead a,.grp li.lead .np,.grp li.hd span{color:var(--ink)}
.panel.cat .grp li.lead a,.panel.cat .grp li.lead .np,.panel.cat .grp li.hd span{color:__BLUE__}
.menu,.menu .top,.menu a,.menu span,.grp,.grp li,.grp li.lead a,.grp li.lead .np,.grp li.hd span{font-weight:400}
.menu .top.np-top{cursor:default}
.menu .top.np-top:hover{color:#fff}
@media (min-width:961px) and (max-width:1279px){   /* eight names, each with its arrow, on one line down to 961px */
  .site-head-in{padding:0 24px;gap:14px}
  .menu{gap:10px}
  .sub-toggle{width:16px}
}
@media (min-width:961px) and (max-width:1023px){
  .site-head-in{padding:0 18px;gap:12px}
  .menu{gap:7px}
  .menu .top{font-size:16px}
}
@media (max-width:960px){
  .panel-in > .pcol{display:block}
  .panel-in > .pcol.over{margin-bottom:0}
  /* 8 Oct 2026, the user: "Menu: on a desktop there is a space between categories. add this space on phones" -
     the same gap as the desktop's between one group and the next, including where one column's groups end and the
     next column's begin (on the phone the columns stand one under another). */
  .panel-in .grp + .grp,.panel-in > .pcol + .pcol{margin-top:__CAT_GAP_PHONE__px}
  .grp a,.grp .np{color:#E7EEF5}
  .grp li.lead a,.grp li.lead .np,.grp li.hd span{color:#fff}
  .panel.cat .grp li.lead a,.panel.cat .grp li.lead .np,.panel.cat .grp li.hd span{color:__PHONE_BLUE__}
  .grp .np,.grp .hd span{font-size:17px;padding:7px 0}
  .menu .top.np-top{cursor:pointer}
}
"""
MENU_CSS = MENU_CSS.replace('__CAT_GAP_PHONE__', str(CAT_GAP_PHONE)).replace('__CAT_GAP__', str(CAT_GAP)).replace('__BLUE__', MENU_BLUE).replace('__PHONE_BLUE__', MENU_PHONE_BLUE)

# A top name that is not a link opens its panel (phones: the name is the larger target).
MENU_JS_EXTRA = ("(function(){[].forEach.call(document.querySelectorAll('.menu .top.np-top'),function(a){a.addEventListener('click',function(e){"
                 "var t=a.parentNode.querySelector('.sub-toggle');if(t){e.stopPropagation();t.click();}});});})();")

def names():
    return [(m, t.lstrip('*#'), t[0] if t[0] in '*#' else '') for m in MENU for col in ([[OVER[m]]] if m in OVER else []) + PANELS[m] for g in col for t in g]

if __name__ == '__main__':
    import collections
    n = names(); c = collections.Counter(m for m, t, k in n if k != '#')
    print('entries (pages) per section:', dict(c), 'total', sum(c.values()), '| links', len(LIVE), '| headings', sum(1 for x in n if x[2] == '#'))
