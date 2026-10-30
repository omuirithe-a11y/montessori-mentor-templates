"""The list of Montessori Mentor pages with images: which have children, where each one has got to, and the owner's words.
Written 26 Oct 2026 on the owner's instruction, 14:03: "fix all of these now" (there was no such list - a chat had to
read the handover and guess).

    python3 pages.py                      the list, as a table
    python3 pages.py <page>               one page in full, with the owner's words
    python3 pages.py waiting              only the pages waiting for her answer
    python3 pages.py todo                 only the pages not finished
    python3 pages.py set <page> <field> <value>       change one field (and record when it changed)

The list is blur2/pages.json, saved in the Project at claude/workspace/tools/blur/pages.json. Fields:
    children   yes | no | not checked      whether any image on it has a child's face to blur
    images     how many images are being changed
    state      a step of the agreed method: new, finding, round1-sent, round1-answered, blurred, round2-sent,
               round2-answered, pixel-checked, on-page, page-checked, sent, uploaded, live-checked, no-blur-needed
    words      the owner's own words about this page, as she wrote them, with the time
    set        the set name in blur2/sets/, where its answers and hand fixes live
    note       anything else that matters

Only her own words go in "words" - nothing is written there that she did not say.
"""
import sys, os, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pages.json')
ORDER = ['new', 'finding', 'round1-sent', 'round1-answered', 'blurred', 'round2-sent', 'round2-answered',
         'pixel-checked', 'on-page', 'page-checked', 'sent', 'uploaded', 'live-checked', 'no-blur-needed']
DONE = ('uploaded', 'live-checked', 'no-blur-needed')
WAIT = ('round1-sent', 'round2-sent', 'sent')

if not os.path.exists(P):
    raise SystemExit('STOP: %s is missing. It is saved in the Project at claude/workspace/tools/blur/pages.json.' % P)
D = json.load(open(P))


def show_one(name, r):
    print('\n%s' % name)
    for k in ('children', 'images', 'state', 'set', 'note', 'words', 'changed'):
        if r.get(k) not in (None, ''):
            print('  %-9s %s' % (k, r[k]))


def table(rows):
    if not rows:
        print('none'); return
    w = max(len(n) for n in rows)
    print('%-*s  %-11s  %6s  %-17s  %s' % (w, 'page', 'children', 'images', 'state', 'the owner\'s words'))
    print('-' * (w + 60))
    for n in sorted(rows, key=lambda x: (ORDER.index(rows[x].get('state', 'new')) if rows[x].get('state') in ORDER else 99, x)):
        r = rows[n]
        print('%-*s  %-11s  %6s  %-17s  %s' % (w, n, r.get('children', '?'), r.get('images', ''), r.get('state', '?'),
                                               (r.get('words') or '')[:46]))
    print('\n%d pages: %d finished, %d waiting for her answer, %d in hand.'
          % (len(rows), sum(1 for r in rows.values() if r.get('state') in DONE),
             sum(1 for r in rows.values() if r.get('state') in WAIT),
             sum(1 for r in rows.values() if r.get('state') not in DONE and r.get('state') not in WAIT)))


a = sys.argv[1:]
if not a:
    table(D)
elif a[0] == 'waiting':
    table({n: r for n, r in D.items() if r.get('state') in WAIT})
elif a[0] == 'todo':
    table({n: r for n, r in D.items() if r.get('state') not in DONE})
elif a[0] == 'set':
    if len(a) < 4: raise SystemExit('STOP: pages.py set <page> <field> <value>')
    name, field, value = a[1], a[2], ' '.join(a[3:])
    if name not in D: raise SystemExit('STOP: no page called "%s". The pages are: %s' % (name, ', '.join(sorted(D))))
    if field == 'state' and value not in ORDER:
        raise SystemExit('STOP: "%s" is not a step. The steps are: %s' % (value, ', '.join(ORDER)))
    D[name][field] = value
    D[name]['changed'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    json.dump(D, open(P, 'w'), indent=1, ensure_ascii=False)
    show_one(name, D[name])
    print('\n(saved; save %s to the Project too)' % P)
elif a[0] in D:
    show_one(a[0], D[a[0]])
else:
    raise SystemExit('STOP: no page called "%s". The pages are: %s' % (a[0], ', '.join(sorted(D))))
