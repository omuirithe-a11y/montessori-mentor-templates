#!/usr/bin/env python3
"""Apply the separate verifiers' findings to the rows files (writes rows-*.v.jsonl beside each), then dedupe by quote.
quote -> replace quote; status -> set status/superseded_by (partial -> keep current, add 'note'); wrong -> 'drop'
(builder-sourced: kept in a separate 'builder' list for the owner); missing -> new row."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
PAIRS = {'verify-prefs.jsonl': ['rows-prefs.jsonl'], 'verify-declog.jsonl': ['rows-declog.jsonl', 'rows-declog3.jsonl'],
         'verify-lessons.jsonl': ['rows-lessons-templates.jsonl']}
def load(fn): return [json.loads(l) for l in open(os.path.join(D, fn), encoding='utf-8') if l.strip()]
log = []
for vf, rfs in PAIRS.items():
    if not os.path.exists(os.path.join(D, vf)): print('no', vf); continue
    rows = {rf: load(rf) for rf in rfs}
    for f in load(vf):
        key = (f.get('row') or '').strip()
        hits = [(rf, r) for rf in rfs for r in rows[rf] if key and r.get('item', '').strip()[:60] == key[:60]]
        k, fix = f.get('kind'), f.get('fix', '')
        if k == 'missing':
            nr = f.get('newrow')
            if nr: nr.setdefault('status', 'current'); nr['added_by_check'] = vf; rows[rfs[0]].append(nr); log.append(('add', nr.get('item', '')[:70]))
            continue
        if not hits: log.append(('NO MATCH', k, key[:70])); continue
        for rf, r in hits:
            if k == 'quote':
                m = re.search(r'set source to "([^"]+)"', fix)
                if m: r['source'] = m.group(1); log.append(('source', key[:60]))
                else: r['quote_fix'] = fix; r['note'] = (r.get('note', '') + ' QUOTE: ' + fix).strip(); log.append(('quote-note', key[:60]))
            elif k == 'status':
                lf = fix.lower()
                if 'in part' in lf or 'partial' in lf or 'only in part' in lf or 'narrow' in lf or 'add note' in lf:
                    r['note'] = (r.get('note', '') + ' ' + fix).strip(); log.append(('partial', key[:60]))
                elif '-> current' in lf or 'recommend current' in lf:
                    r['status'] = 'current'; r['superseded_by'] = ''; r['note'] = fix; log.append(('current', key[:60]))
                elif 'superseded' in lf:
                    r['status'] = 'superseded'; r['superseded_by'] = fix; log.append(('superseded', key[:60]))
                else:
                    r['note'] = fix; log.append(('status-note', key[:60]))
            elif k == 'wrong':
                lf = fix.lower()
                r['drop'] = 'builder' if ('builder' in lf or 'no owner decision' in lf) else 'remove'
                r['drop_reason'] = fix; log.append(('drop-' + r['drop'], key[:60]))
    for rf in rfs:
        with open(os.path.join(D, rf.replace('.jsonl', '.v.jsonl')), 'w', encoding='utf-8') as o:
            for r in rows[rf]: o.write(json.dumps(r, ensure_ascii=False) + '\n')
for x in log: print(*x)
print('findings applied:', len(log), 'no match:', sum(1 for x in log if x[0] == 'NO MATCH'))
