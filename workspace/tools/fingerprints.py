#!/usr/bin/env python3
"""fingerprints.py <record|check|show> <page slug>   (8 Nov 2026, owner "built the three", item 3)
The fingerprints of everything a page's builds are judged by: both code templates, the builder, the page's own settings are NOT
included (they change with every fix), every check script and runner (tools/*.py, tools/*.sh, tools/v8/*.py, tools/v8/*.sh),
the rules list (tools/REQUIRED-CHECKS.json) and the allowed lists are left out.
  record: writes records/fingerprints/<page>.txt (made at the page's first build, or with the owner's words in the decisions log)
  check:  exit 0 if nothing changed; else prints each changed file and the combined fingerprint, exit 3. A change is accepted when
          a decisions-log line holds "FINGERPRINT <page> <combined, 16 characters>" and "OWNER" (her words for that change).
"""
import sys, os, glob, hashlib, re
M = '/home/claude/mm'
mode, page = sys.argv[1:3]
def files():
    L = [os.path.join(M, 'templates', 'Essay Code Template.html'), os.path.join(M, 'templates', 'Resources Code Template.html')]
    for pat in ('tools/*.py', 'tools/*.sh', 'tools/v8/*.py', 'tools/v8/*.sh'):
        L += glob.glob(os.path.join(M, pat))
    # the page's own allowed lists are NOT included: like the settings, they change with the page's fixes (8 Nov: including them
    # would have refused every trial that names one of her choices)
    return sorted(set(f for f in L if os.path.isfile(f) and '/_' not in f))
def sha(f): return hashlib.sha256(open(f, 'rb').read()).hexdigest()
now = {os.path.relpath(f, M): sha(f) for f in files()}
comb = hashlib.sha256(''.join('%s %s\n' % kv for kv in sorted(now.items())).encode()).hexdigest()
rec = os.path.join(M, 'records', 'fingerprints', page + '.txt')
if mode == 'show': print(comb[:16]); sys.exit(0)
if mode == 'record':
    os.makedirs(os.path.dirname(rec), exist_ok=True)
    open(rec, 'w').write('combined %s\n' % comb + ''.join('%s %s\n' % (v, k) for k, v in sorted(now.items())))
    print('fingerprints recorded for %s: %d files, combined %s' % (page, len(now), comb[:16])); sys.exit(0)
if not os.path.exists(rec): print('FINGERPRINTS: no record for %s (records/fingerprints/%s.txt) - run: tools/fingerprints.py record %s' % (page, page, page)); sys.exit(3)
old = {}
for l in open(rec):
    p_ = l.rstrip('\n').split(' ', 1)   # paths may hold spaces (the templates)
    if len(p_) == 2 and p_[0] != 'combined': old[p_[1]] = p_[0]
ch = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
if not ch: print('fingerprints: unchanged since the record (%d files)' % len(now)); sys.exit(0)
logs = ''.join(open(f, encoding='utf-8', errors='replace').read() for f in glob.glob(os.path.join(M, 'records', 'DECISIONS-LOG*.md')))
ok = any(('FINGERPRINT %s %s' % (page, comb[:16])) in l and 'OWNER' in l for l in logs.splitlines())
print('FINGERPRINTS CHANGED since the record for %s (combined now %s): %s' % (page, comb[:16], ', '.join(ch[:30])))
if ok: print('accepted: the decisions log holds the owner\'s words for FINGERPRINT %s %s' % (page, comb[:16])); sys.exit(0)
print('a change to the template or the checks mid-page needs the owner\'s words: a decisions-log line with "FINGERPRINT %s %s" and OWNER' % (page, comb[:16])); sys.exit(3)
