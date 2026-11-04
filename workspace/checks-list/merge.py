#!/usr/bin/env python3
"""Merge the extracted rows into REQUIRED-CHECKS draft (jsonl + txt) and a readable HTML page grouped by topic."""
import json, glob, html, re, sys, os
D = os.path.dirname(os.path.abspath(__file__))
SRC = [('A', 'rows-prefs.jsonl', 'Your saved preferences'), ('B', 'rows-declog.jsonl', 'Decisions log (to 3 Nov)'),
       ('C', 'rows-declog3.jsonl', 'Decisions log 3-5 Nov and handover'), ('D', 'rows-lessons-templates.jsonl', 'Lessons Learned and template notes'),
       ('E', 'rows-mine.jsonl', 'START-HERE, MASTER-DECISIONS, check documents')]
TOPICS = [('Faces and images of children', r'face|blur|child'),
          ('Gate, delivery and upload', r'gate|zip|upload|deliver|hostinger|copy protection|folder|public_html'),
          ('Columns and layout', r'column|layout|side by side|two-column|grid'),
          ('Images: size, placement, rows, captions', r'image|photo|caption|row of|crop|turn|rotat|mask'),
          ('Spacing and gaps', r'spac|gap| px |above|below|letters to letters|margin'),
          ('Headings, labels, lists, quotations, tables', r'heading|label|list|bullet|number|quotation|table|indent|tab'),
          ('Colours, lines and dividers', r'colou?r|blue|red|green|beige|divider|line under|underline|#'),
          ('Text: wording, spelling, fonts, alignment', r'word|spell|typo|font|justif|align|italic|bold|dash|uk english'),
          ('Hero, menu, contents box, footer', r'hero|menu|contents|footer|title|address'),
          ('Phones and tablets', r'phone|tablet|390|640|830|swipe'),
          ('How checks are run', r'check|review|agent|width|screenshot|measure|test')]
def topic(x):
    s = (x.get('item', '') + ' ' + x.get('quote', '')).lower()
    for t, p in TOPICS:
        if re.search(p, s): return t
    return 'Other'
rows = []; seen = {}
for pre, fn, label in SRC:
    p = os.path.join(D, fn.replace('.jsonl', '.v.jsonl'))
    if not os.path.exists(p): p = os.path.join(D, fn)
    if not os.path.exists(p): print('MISSING', fn); continue
    n = 0
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if not line: continue
        try: x = json.loads(line)
        except Exception as e: print('BAD LINE', fn, line[:80]); continue
        if x.get('drop') == 'remove': continue
        qk = re.sub(r'\s+', ' ', x.get('quote', '')).strip().lower()
        if qk and qk in seen and x.get('item', '')[:40] == seen[qk]: continue
        seen[qk] = x.get('item', '')[:40]
        n += 1; x['id'] = '%s%03d' % (pre, n); x['from'] = label; x['topic'] = topic(x) if x.get('drop') != 'builder' else 'BUILDER'; rows.append(x)
    print(fn, n)
cur = [x for x in rows if x.get('status', 'current') == 'current' and x.get('drop') != 'builder']
bld = [x for x in rows if x.get('drop') == 'builder']
print('rows', len(rows), 'current', len(cur))
with open(os.path.join(D, 'REQUIRED-CHECKS-draft.jsonl'), 'w', encoding='utf-8') as f:
    for x in rows: f.write(json.dumps(x, ensure_ascii=False) + '\n')
with open(os.path.join(D, 'REQUIRED-CHECKS-draft.txt'), 'w', encoding='utf-8') as f:
    f.write('# REQUIRED-CHECKS (DRAFT, not in effect until the owner agrees) - id | status | applies_to | check | widths | pass | item | source | quote\n')
    for x in rows:
        f.write(' | '.join(str(x.get(k, '')).replace('\n', ' ') for k in ('id', 'status', 'applies_to', 'check', 'widths', 'pass', 'item', 'source', 'quote')) + '\n')
# page
order = [t for t, _ in TOPICS] + ['Other']
def rowhtml(x):
    ck = x.get('check', '')
    kind = 'new' if ck.startswith('new') else ('eye' if ck.startswith('eye') else 'have')
    lab = {'new': 'check to write', 'eye': 'by eye (agent)', 'have': 'check exists'}[kind]
    note = ('<p class="src">Note: %s</p>' % esc(x['note'])) if x.get('note') else ''
    return ('<article class="row"><div class="top"><span class="id">%s</span><span class="tag %s">%s</span><span class="ap">%s</span></div>'
            '<p class="item">%s</p><blockquote>%s</blockquote><p class="src">%s%s</p>%s</article>' % (
        esc(x['id']), kind, lab, esc(x.get('applies_to', '')), esc(x.get('item', '')), esc(x.get('quote', '')), esc(x.get('source', '')),
        (' &middot; ' + esc(x.get('date'))) if x.get('date') else '', note))
def esc(s): return html.escape(str(s or ''))
out = []
for t in order:
    g = [x for x in cur if x['topic'] == t]
    if not g: continue
    out.append('<section><h2>%s <span class="n">%d</span></h2>' % (esc(t), len(g)))
    for x in g: out.append(rowhtml(x))
    out.append('</section>')
if bld:
    out.append('<section><h2>Settings I made myself, with no decision of yours <span class="n">%d</span></h2><p class="lead">These are in the templates or tools, but the records show they were my own choice, not your words. They are not rules until you keep them; each needs your yes or no.</p>' % len(bld))
    for x in bld: out.append(rowhtml(x))
    out.append('</section>')
sup = [x for x in rows if x.get('status') == 'superseded']
counts = dict(have=sum(1 for x in cur if not x.get('check', '').startswith(('new', 'eye'))), new=sum(1 for x in cur if x.get('check', '').startswith('new')), eye=sum(1 for x in cur if x.get('check', '').startswith('eye')))
page = open(os.path.join(D, 'page-template.html'), encoding='utf-8').read()
page = page.replace('{{BODY}}', '\n'.join(out)).replace('{{N}}', str(len(cur))).replace('{{SUP}}', str(len(sup))) \
           .replace('{{HAVE}}', str(counts['have'])).replace('{{NEW}}', str(counts['new'])).replace('{{EYE}}', str(counts['eye'])).replace('{{BLD}}', str(len(bld)))
open(os.path.join(D, 'page', 'index.html'), 'w', encoding='utf-8').write(page)
print('page written', counts)
