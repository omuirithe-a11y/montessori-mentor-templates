"""log_time_check.py <repo copy of the log> <working copy of the log> (S9, owner 7 Nov "implement all of these changes"):
refuses (exit 3) when a line added to a decisions log starts with a time later than the clock - '- D Mon HH:MM' or 'HH:Mx'
(x counted as 0). Times are Asia/Shanghai, the log's own."""
import sys, re, datetime, os
old = set(open(sys.argv[1]).read().splitlines()) if os.path.exists(sys.argv[1]) else set()
now = datetime.datetime.now()
MON = {m: i for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 1)}
bad = []
for l in open(sys.argv[2]).read().splitlines():
    if l in old: continue
    m = re.match(r'^- (\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* (\d{1,2}):(\d)([0-9x])', l)
    if not m: continue
    d, mo, hh, m1, m2 = int(m.group(1)), MON[m.group(2)], int(m.group(3)), int(m.group(4)), m.group(5)
    try: t = datetime.datetime(now.year, mo, d, hh, m1 * 10 + (0 if m2 == 'x' else int(m2)))
    except ValueError: bad.append(l[:80]); continue
    if t > now + datetime.timedelta(minutes=1): bad.append(l[:80])
if bad:
    print('COMMIT REFUSED: log line(s) with a time later than the clock (%s): %s' % (now.strftime('%d %b %H:%M'), ' | '.join(bad))); sys.exit(3)
