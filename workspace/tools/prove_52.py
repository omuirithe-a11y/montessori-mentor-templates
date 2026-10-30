#!/usr/bin/env python3
"""Proofs on 5.2 for the checks 5.4 cannot prove (21 Oct 2026): 5.4 has no PDF badges, and 5.4's word breakers look for
"consumables". The faults put in here are 5.2's own; recording works exactly as tools/prove_all.py (it is called).
  python3 tools/prove_52.py J H H2"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prove_all as P

P.BREAK.update({
    'J': ('the first PDF badge moved 40 px out of its column', P.first(r'<a class="pdf"', '<a class="pdf" style="transform:translateX(40px)"')),
    'H2': ('a word misspelt on the page', P.first(r'Saskatoon', 'Saskatooon')),
    # H: prove_all's own breaker (a misspelt word added to the build's report) works on any page
})

if __name__ == '__main__':
    sys.exit(0 if P.main('5.2', sys.argv[1:] or ['J', 'H', 'H2']) else 1)
