#!/usr/bin/env python3
"""Proofs on 5.1 (21 Oct 2026) for the checks 5.4 cannot prove: D (5.4's dividers are page-setting lines; 5.1 has Word's
own), I (5.1 has a run of spaces Word uses to line things up), and the page check's phone footer for a page that ends in a
photo. The faults put in here are 5.1's own; recording works exactly as tools/prove_all.py (it is called).
  python3 tools/prove_51.py D I PAGE"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prove_all as P

P.BREAK.update({
    'D': ('the first beige line removed', P.first(r'<div class="beige-rule mm-org-rule"></div>', '')),
    'I': ('the run of spaces after "Shortlist:" made one space', P.first(r'<span class="mm-t">(  ?){3,}</span>', ' ')),
    'PAGE': ('the footer script set to 60 on phones (the photo 20 px further from the band)', P.first(r'G=ph\?40:60', 'G=ph?60:60')),
})

if __name__ == '__main__':
    sys.exit(0 if P.main('5.1', sys.argv[1:] or ['D', 'I', 'PAGE']) else 1)
