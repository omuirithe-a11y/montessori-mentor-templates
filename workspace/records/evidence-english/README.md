# Evidence pack - The English Curriculum (3.5.0), for an independent analysis of the whole process (made 7 Nov 2026)

The owner asked for an analysis of the entire process (4-7 Nov 2026, builds 1-42) and of what could have been done differently,
run as option C: TWO separate agents, each writing the analysis alone from these files, then set side by side - where they agree
the finding is solid; where they differ the evidence is unclear and is marked so. The agents must not be given any analysis
written by the assistant who built the page (its lists in SOLUTIONS-7-nov.md and in the transcript are evidence of what it said,
not conclusions to adopt).

## Sources, most independent first
| File | What it shows | Limits |
|---|---|---|
| builds/<bN>/ | per build: checks_SUMMARY.txt (run_checks.sh), checks2_SUMMARY.txt (more_checks.sh), checks2_gate-early.txt (the gate's early run), gate-full.txt, REVIEW*.md (separate reviews), changes.txt; builds/<bN>.log = build logs | written by the scripts and separate agents; builds 21-27 from archives; builds 31, 33, 36: records LOST (their archive copy failed when the folders were cleared on 6 Nov); builds 1-17 not here (see ENG-CHANGES-5-nov.md) |
| git-log.txt | every commit since 4 Nov with time and message (templates, checks, settings, log) | only what was committed; times in the repo's time zone (CST) |
| agent-reports/ | separate agents' reports: faces sheet and pixel checks; the critique of the assistant's solutions list (7 Nov) | reviews of builds are in builds/<bN>/REVIEW*.md |
| transcript.txt | the chat, word for word: OWNER = her messages, CLAUDE = the assistant's replies, with UTC times (CST = UTC+8) | only from 6 Nov 20:21 CST; the first entry is a summary the assistant wrote at a context reset, NOT her words |
| BUILD-ORDER.md, LESSONS-LEARNED-27-29-oct.md | what was meant to happen (rules, lessons) | rules, not events |
| DECISIONS-LOG-3-nov.md, DECISIONS-LOG.md | the fullest account: events, her words quoted, hourly reviews | WRITTEN BY THE ASSISTANT - check every claim against the sources above |
| time-report.txt | hours per check stage per build (tools/time_report.py) | only builds whose summaries survive; no build causes before 7 Nov |
| check-proofs.json | each check script version and the planted fault that proved it | - |
| SOLUTIONS-7-nov.md, ENG-CHANGES-5-nov.md | the assistant's list of mistakes and fixes (evidence of what it proposed); the change list for builds 1-17 | the assistant's own writing |

## Brief for each of the two agents (give each the same, separately)
You have not seen this work. From the files in this folder only, write an analysis of how The English Curriculum page was built
(4-7 Nov 2026, 42 builds): (1) a timeline of the builds with what each was for and what stopped it, from builds/ and git-log.txt;
(2) where the time went, in hours where the files allow, and the causes of the rebuilds; (3) every mistake or pattern that cost
time, each with its evidence (file and line) and how much time it cost, ranked; (4) for each, what should have been done instead
and at what point it could have been caught; (5) what the owner was told that the files show was not true at the time. Treat the
decisions log and the assistant's replies as claims to verify, not as facts. Mark anything you could not verify. Plain words;
"image", never "photo". Write your report as analysis-<A or B>.md.
