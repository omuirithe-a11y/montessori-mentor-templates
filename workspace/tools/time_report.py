"""time_report.py <builds folder> <page slug>  (7 Nov 2026, owner "implement all of these changes", S10)
Where the time went, per build, from the files: the build log's time (file modification time), each check stage's start and
end (checks2/SUMMARY.txt and checks/SUMMARY.txt lines, dated by the summary file's own date), the review report's time,
and the cause the build guard recorded (records/build-causes-<page>.txt). Prints one line per build and the totals."""
import sys, os, re, glob, datetime
D, page = sys.argv[1], sys.argv[2]
causes = {}
cf = '/home/claude/mm/records/build-causes-%s.txt' % page
if os.path.exists(cf):
    for l in open(cf):
        f = [x.strip() for x in l.split('|')]
        if len(f) >= 3: causes[f[1]] = f[2].replace('cause: ', '')
def times(p):
    if not os.path.exists(p): return []
    day = datetime.datetime.fromtimestamp(os.path.getmtime(p)).date(); out = []
    for l in open(p, errors='replace'):
        for t in re.findall(r'\b(\d\d:\d\d:\d\d)\b', l): out.append(datetime.datetime.combine(day, datetime.time.fromisoformat(t)))
    # a summary that crosses midnight: times that fall before the first are the next day
    fixed = []
    for t in out:
        if fixed and t < fixed[0] - datetime.timedelta(hours=1): t += datetime.timedelta(days=1)
        fixed.append(t)
    return fixed
def span(ts): return (min(ts), max(ts)) if ts else (None, None)
rows, tot = [], {'fast': 0, 'long': 0}
for b in sorted(glob.glob(os.path.join(D, 'b[0-9]*')), key=lambda x: int(re.sub(r'\D', '', os.path.basename(x)) or 0)):
    n = os.path.basename(b)
    if not os.path.isdir(b): continue
    lg = os.path.join(D, n + '.log'); bt = datetime.datetime.fromtimestamp(os.path.getmtime(lg)) if os.path.exists(lg) else None
    f0, f1 = span(times(os.path.join(b, 'checks2', 'SUMMARY.txt'))); l0, l1 = span(times(os.path.join(b, 'checks', 'SUMMARY.txt')))
    rv = os.path.join(b, 'REVIEW.md'); rt = datetime.datetime.fromtimestamp(os.path.getmtime(rv)) if os.path.exists(rv) else None
    fm = (f1 - f0).total_seconds() / 60 if f0 else 0; lm = (l1 - l0).total_seconds() / 60 if l0 else 0
    tot['fast'] += fm; tot['long'] += lm
    rows.append('%s | built %s | checks2 %s-%s (%.0f min) | checks %s-%s (%.0f min) | review %s | cause: %s' % (
        n, bt.strftime('%d %b %H:%M') if bt else '?', f0.strftime('%H:%M') if f0 else '-', f1.strftime('%H:%M') if f1 else '-', fm,
        l0.strftime('%H:%M') if l0 else '-', l1.strftime('%H:%M') if l1 else '-', lm, rt.strftime('%d %b %H:%M') if rt else '-', causes.get(n, 'not recorded')))
print('\n'.join(rows))
print('totals: fast/early-stage checks %.1f h, long checks %.1f h, over %d builds (builds whose folders were cleared show only what remains)' % (tot['fast'] / 60, tot['long'] / 60, len(rows)))
