"""Montessori Mentor site shell, in the Practical Life design.
Everything shared by the three page templates lives here: design tokens, header,
hero, contents box, footer, and the base typography. Change a token once and
every page follows on the next build."""
import base64, html as H

SITE = 'Montessori Mentor'
MENU = ['Home', 'Essential Elements', 'Curriculum', 'Play', 'Administration', 'Parents', 'Education', 'Resources']
# Dropdown panels: one group per main essay; the essay first, then its companion and Resources pages (21 Sept, from the live site)
PANELS = {
 'Home': [['Montessori Mentor', 'Aun Aprendo', 'A Montessori Journey', 'The History, Philosophy, and Legacy of Montessori Education'],   # THE NEW MENU (4 Oct 2026, chat 10: your list 1.1-1.10)
          ['Biography', 'Timeline of Montessori’s Life', 'The First Casa dei Bambini'],
          ['The Story of San Lorenzo', 'Glossary']],
 'Essential Elements': [['Essential Elements', 'Essential Elements Resources'],
          ['The Role of the Adult', 'The Role of the Assistant', 'Developing Responsibility', 'Some Words of Advice to Teachers', 'The Role of the Adult Resources'],
          ['The Prepared Environment', 'Essential Characteristics Theory', 'The Prepared Outdoor Environment', 'Anji Play', 'The Prepared Environment Resources'],
          ['The Uninterrupted Three-Hour Cycle', 'The Uninterrupted Three-Hour Cycle Resources'],
          ['Mixed-Age Groups', 'Mixed-Age Groups Resources'],
          ['The Montessori Materials', 'The Montessori Materials Sourcing', 'The Montessori Materials Resources']],
 'Curriculum': [['The Montessori Curriculum', 'Montessori Scope and Sequence', 'Montessori Scope and Sequence: Curriculum Resources'],
          ['The Practical Life Curriculum', 'Practical Life Resources'],
          ['The Sensorial Curriculum', 'Sensorial Resources']],
}
GROUPED = {'Essential Elements', 'Curriculum'}
# Where each page lives (22 Sept): the live WordPress pages, plus the new pages. A dropdown entry with no page yet is left out.
URLS = {
 "Montessori Mentor": "/",
 "Home": "/",
 "Essential Elements": "/essential-elements/",
 "Curriculum": "/curriculum/",
 "The Practical Life Curriculum": "/the-practical-life-curriculum-2/",
 "Play": "/play/",
 "Administration": "/administration/",
 "Parents": "/parents/",
 "Education": "/education/",
 "Resources": "/resources/",
 "Essential Elements Resources": "/essential-elements-resources/",
 "The Role of the Adult": "/the-role-of-the-adult/",
 "The Role of the Assistant": "/the-role-of-the-assistant/",
 "Developing Responsibility": "/developing-responsibility/",
 "Some Words of Advice to Teachers": "/some-words-of-advice-to-teachers/",
 "The Role of the Adult Resources": "/the-role-of-the-adult-resources/",
 "The Prepared Environment": "/the-prepared-environment/",
 "Essential Characteristics Theory": "/essential-characteristics-theory/",
 "The Prepared Outdoor Environment": "/the-prepared-outdoor-environment/",
 "Anji Play": "/anji-play/",
 "The Prepared Environment Resources": "/the-prepared-environment-resources/",
 "The Uninterrupted Three-Hour Cycle": "/the-uninterrupted-three-hour-cycle/",
 "The Uninterrupted Three-Hour Cycle Resources": "/the-uninterrupted-three-hour-cycle-resources/",
 "Mixed-Age Groups": "/mixed-age-groups/",
 "Mixed-Age Groups Resources": "/mixed-age-groups-resources/",
 "The Montessori Materials": "/the-montessori-materials/",
 "The Montessori Materials Sourcing": "/the-montessori-materials-sourcing/",
 "The Montessori Materials Resources": "/the-montessori-materials-resources/",
 "Montessori Mentor": "/",
 "Aun Aprendo": "/aun-aprendo/",
 "A Montessori Journey": "/a-montessori-journey/",
 "The History, Philosophy, and Legacy of Montessori Education": "/the-history-philosophy-and-legacy-of-montessori-education/",
 "Biography": "/biography/",
 "Timeline of Montessori's Life": "/timeline-of-montessoris-life/",
 "The First Casa dei Bambini": "/the-first-casa-dei-bambini/",
 "The Story of San Lorenzo": "/the-story-of-san-lorenzo/",
 "Glossary": "/glossary/",
 "The Montessori Curriculum": "/curriculum/",
 "The Sensorial Curriculum": "/the-sensorial-curriculum/",
 "Sensorial Resources": "/sensorial-resources/",
 "Timeline of Montessori’s Life": "/timeline-of-montessoris-life/",
}
SEARCH_READY = False   # the search button appears once site search (Pagefind) is set up   # first page of each group is a main essay (shown a little stronger)
FONTS = ('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500'
         '&family=Vollkorn:ital,wght@0,400;0,500;1,400&display=swap')

# Contents-number colours, in the order of the Practical Life page (7th added for pages with seven groups)
GROUP = ['#1E4D9B', '#2A6F6A', '#9C2F1F', '#4A7C59', '#6B3D6E', '#B07D2A', '#5B6B7A']

CSS = r"""
:root{
  --paper:#FFFFFF; --paper-alt:#F3F3F1; --line:#E6E6E4;
  --ink:#2B2B2B; --quiet:#6B6B6B; --link:#4A5560;
  --head:#0432FF; --navy:#1E4D7B;   /* 23 Sept: headings in the blue the person uses in Word */ --bar:#FBF8F3; --bar-line:#DED6C8; --active:#B5613E;
  --serif:'EB Garamond',Georgia,serif; --display:'Vollkorn',Georgia,serif;
  --sans:Helvetica,'Helvetica Neue',Arial,sans-serif;
  --page:1220px; --gutter:40px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:calc(76px + env(safe-area-inset-top,0px))}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.65;
  padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
a{color:var(--head)}
a:focus-visible,button:focus-visible{outline:2px solid var(--active);outline-offset:3px}
.skip{position:absolute;left:-9999px;top:0}
.skip:focus{left:12px;top:12px;z-index:50;background:#fff;padding:8px 12px}

/* ---------- header: menu bar A4 (navy, all serif) ---------- */
.site-head{position:sticky;top:env(safe-area-inset-top,0px);z-index:40;background:var(--navy)}
.site-head-in{max-width:1280px;margin:0 auto;height:76px;padding:0 40px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.site-name{font-family:var(--display);font-size:25px;font-weight:500;color:#fff;text-decoration:none;white-space:nowrap}
.menu{list-style:none;margin:0;padding:0;display:flex;align-items:center;gap:22px}
.menu > li{position:static;display:flex;align-items:center;height:76px}
.menu .top{font-family:var(--serif);font-size:17px;color:#fff;text-decoration:none;padding:6px 0;border-bottom:1.5px solid transparent;white-space:nowrap}
.menu .top:hover{color:#DCE6F0}
.menu .top[aria-current="page"]{border-bottom-color:#fff}
.sub-toggle{width:22px;height:30px;margin-left:1px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:none;border:0;color:#fff;cursor:pointer;opacity:.85}
.panel{display:none;position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 14px 28px rgba(20,30,40,.14)}
.has-panel:focus-within > .panel,.has-panel.open > .panel{display:block}
.has-panel.open > .sub-toggle svg{transform:rotate(180deg)}
.panel-in{max-width:1280px;margin:0 auto;padding:26px 40px 30px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 48px}
.grp{list-style:none;margin:0;padding:0}
.grp li{border-bottom:1px solid var(--line)}
.grp li:last-child{border-bottom:0}
.grp a{display:block;padding:8px 0;font-family:var(--serif);font-size:17px;line-height:1.3;color:var(--ink);text-decoration:none}
.grp a:hover{color:var(--head)}
.grp li.lead a{color:var(--head);font-weight:600}
.grp a[aria-current="page"]{color:var(--head);text-decoration:underline;text-underline-offset:3px}
.icon-btn{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;background:none;border:0;color:#fff;cursor:pointer;border-radius:22px}
.icon-btn:hover{background:rgba(255,255,255,.1)}
.menu-btn{display:none}
.site-tools{display:flex;align-items:center;gap:2px}
.site-head a:focus-visible,.site-head button:focus-visible{outline:2px solid #fff;outline-offset:3px}

/* ---------- hero (Practical Life page) ---------- */
.hero{position:relative;margin:10px 10px 0;min-height:400px;display:flex;align-items:flex-end;padding:0 8% 40px;
  background-color:#2A2420;background-size:cover;background-position:center}
.hero::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(105deg,rgba(15,12,9,.72) 0%,rgba(15,12,9,.55) 34%,rgba(15,12,9,.12) 62%,rgba(15,12,9,0) 80%)}
.hero h1{position:relative;z-index:1;margin:0;max-width:760px;font-family:var(--display);font-weight:500;font-size:40px;line-height:1.2;color:#fff;
  text-shadow:0 1px 12px rgba(0,0,0,.4)}
.hero h1 span{display:block}
.hero h1 .sub{font-size:26px;margin-top:6px}

/* ---------- contents box ---------- */
.toc-wrap{max-width:1100px;margin:0 auto;padding:26px 0 36px}
.toc-label{margin:0 0 14px;font-family:var(--serif);font-weight:500;font-size:24px;color:var(--head)}
.toc-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 40px}
.toc ul{list-style:none;margin:0;padding:0}
.toc li{margin:0 0 10px}
.toc a{font-size:19px;line-height:1.35;color:var(--link);text-decoration:none;border-bottom:1px solid transparent}
.toc a:hover{color:var(--head);border-bottom-color:var(--head)}
.toc-groups a{display:flex;align-items:baseline;gap:8px}
.toc-num{flex:0 0 22px;font-weight:600;font-size:17px;color:var(--ink);font-variant-numeric:tabular-nums}

/* ---------- footer ---------- */
.site-foot{border-top:1px solid var(--line);margin-top:24px}
.site-foot-in{max-width:var(--page);margin:0 auto;padding:32px var(--gutter) 48px;display:flex;justify-content:space-between;align-items:center;gap:16px;
  font-size:15px;color:var(--quiet)}
.site-foot a{color:var(--quiet)}

/* ---------- shared essay typography (all three templates) ---------- */
.page-h2{font-family:var(--serif);font-weight:500;font-size:24px;line-height:1.2;color:var(--head);
  margin:40px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--head)}
blockquote.mq{margin:24px 38px;padding:0;font-family:var(--display);font-weight:400;font-style:italic;font-size:17px;line-height:1.65}
blockquote.mq strong{font-weight:400}
blockquote.mq p{margin:0 0 8px;text-indent:48px}
blockquote.mq cite{display:block;font-style:normal;margin-top:6px;padding-left:48px}

@media (max-width:1180px){
  .menu{gap:15px}
  .site-head-in{padding:0 24px}
  .menu .top{font-size:16px}
}
@media (max-width:960px){
  .site-head-in{height:60px;padding:0 8px 0 18px}
  .site-name{font-size:21px}
  .menu-btn{display:inline-flex}
  .site-nav{display:none;position:absolute;left:0;right:0;top:60px;background:var(--navy);max-height:calc(100vh - 60px);overflow-y:auto;
    padding:4px 18px 16px;box-shadow:0 12px 24px rgba(0,0,0,.18)}
  .site-nav.open{display:block}
  .menu{display:block}
  .menu > li{display:flex;flex-wrap:wrap;align-items:center;height:auto;border-bottom:1px solid rgba(255,255,255,.2)}
  .menu .top{flex:1 1 auto;font-size:18px;padding:13px 0;border-bottom:0}
  .menu .top[aria-current="page"]{text-decoration:underline;text-underline-offset:4px}
  .sub-toggle{width:44px;height:44px}
  .has-panel:focus-within > .panel{display:none}
  .has-panel.open > .panel{display:block}
  
  .has-panel.open > .sub-toggle svg{transform:rotate(180deg)}
  .panel{position:static;flex:0 0 100%;background:transparent;border:0;box-shadow:none}
  .panel-in{display:block;padding:0 0 10px 14px}
  .grp{margin-bottom:6px}
  .grp li{border-bottom:0}
  .grp a{color:#E7EEF5;font-size:17px;padding:7px 0}
  .grp li.lead a{color:#fff}
  .grp a[aria-current="page"]{color:#fff}
  html{scroll-padding-top:calc(64px + env(safe-area-inset-top,0px))}
}
@media (max-width:640px){
  .hero{margin:0;min-height:240px;padding:0 24px 24px}
  .hero h1{font-size:28px}
  .hero h1 .sub{font-size:19px}
  .toc-wrap{padding:22px 24px 26px}
  .toc-grid{grid-template-columns:1fr}
  .toc-label{font-size:22px}
  .toc a{font-size:18px}
  .site-foot-in{flex-direction:column;align-items:flex-start;padding:28px 24px 40px}
  blockquote.mq{margin:20px 0}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
"""

SEARCH = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
          '<circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>')
BURGER = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
          '<path d="M4 7h16M4 12h16M4 17h16"></path></svg>')

CHEV = ('<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
        '<path d="M2.5 4.5 6 8l3.5-3.5"></path></svg>')

def header(active, current=None):
    """THE FULL MENU (5 Oct 2026, chat 12): the header is made by site/menu.py - MENU, PANELS and LIVE there are the menu;
    the MENU / PANELS / URLS above are the old menu, kept as a record only. After a page is built, site/apply_menu.py marks its own entry."""
    import menu
    return menu.header(None, active)

def hero(img_path, lines):
    b = open(img_path, 'rb').read(); mime = 'image/png' if img_path.endswith('.png') else 'image/jpeg'
    uri = f'data:{mime};base64,' + base64.b64encode(b).decode()
    spans = ''.join(f'<span{" class=\"sub\"" if k else ""}>{l}</span>' for k, l in enumerate(lines))
    return (f'<div class="hero" style="background-image:url(\'{uri}\')">'
            f'<h1>{spans}</h1></div>')

def toc(left, right):
    """left: [(id, text)], right: [(id, text)] numbered with the group colours."""
    L = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in left)
    R = ''.join(f'<li><a href="#{i}"><span class="toc-num">{k + 1}</span>{t}</a></li>'
                for k, (i, t) in enumerate(right))
    return (f'<nav class="toc-wrap toc" aria-label="Contents"><p class="toc-label">Table of contents</p><div class="toc-grid">'
            f'<ul class="toc-essays">{L}</ul>' + (f'<ul class="toc-groups">{R}</ul>' if right else '<ul></ul>') + '</div></nav>')

def footer():
    return (f'<footer class="site-foot"><div class="site-foot-in"><span>\u00a9 2026 {SITE}</span>'
            f'<a href="#top">Back to top</a></div></footer>')

MENU_JS = r"""
(function(){var b=document.querySelector('.menu-btn'),n=document.getElementById('site-nav');if(!n)return;
if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Close the menu':'Open the menu');});
var items=[].slice.call(n.querySelectorAll('.has-panel'));
function closeAll(ex){items.forEach(function(li){if(li!==ex){li.classList.remove('open');var t=li.querySelector('.sub-toggle');if(t)t.setAttribute('aria-expanded','false');}});}
items.forEach(function(li){var t=li.querySelector('.sub-toggle');t.addEventListener('click',function(e){e.stopPropagation();var o=!li.classList.contains('open');closeAll(li);li.classList.toggle('open',o);t.setAttribute('aria-expanded',o?'true':'false');});});
document.addEventListener('click',function(e){if(!n.contains(e.target))closeAll();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();if(document.activeElement&&n.contains(document.activeElement))document.activeElement.blur();}});})();
"""

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import menu as _menu
CSS = CSS + _menu.MENU_CSS
MENU_JS = MENU_JS + _menu.MENU_JS_EXTRA

def head(title, extra_css=''):
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{H.escape(title)} | {SITE}</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="{FONTS}">\n'
            f'<style>{CSS}{extra_css}</style>\n</head>\n')
