# Brief: separate check of the REQUIRED-CHECKS draft rows (5 Nov 2026)

You have not seen these rows being made. The rows were extracted from the owner's records by other agents following /home/claude/eng35/list/BRIEF-EXTRACT.md (read it first). The owner will read the list and agree to it; every row must quote its source exactly, and no rule in the sources may be missing.

For your assigned rows file and source:
1. QUOTES: check every row's "quote" appears word for word in the named source (at the named line where given). Write each failure with the exact correct text.
2. STATUS: check rows marked current are not replaced by a later rule in any of the sources you can read (later owner words win), and rows marked superseded really were replaced. List each wrong status with the replacing source.
3. MISSING: read the source IN FULL and list every rule about how a page looks, is built, checked or delivered that has no row. Give each as a ready JSON row in the brief's format.
4. WRONG ROWS: rows that are not rules (status notes, message-only rules, the builder's own words presented as the owner's) - list them with the reason.

Write your findings as JSON lines to the output file named in your task: {"kind": "quote|status|missing|wrong", "row": "<the row's item text, or empty for missing>", "fix": "<exact fix>", "evidence": "<source and line>"} and for "missing" add "newrow": {...}. End with a one-paragraph summary printed to your reply: counts of each kind, and what you could not check. Change no other file.
