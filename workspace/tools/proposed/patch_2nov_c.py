"""2 Nov 2026 (owner 16:04, queued): "The spacing beneath underlined words is too small: match the spacing that is under the other elements,
such as that under 'The Federation of Children's Book Groups'. etc Change this on all pages and in the template" - an underlined line
(p.mm-ul) to the letters below: 21 (as a name line to its next line, measured 21-21.3 at 1440 on 8.3 build 11), not 15. Two scripts set it:
mm-kind-gaps-js (data-gap on the next block) and mm-ul-gap-js (from the underline); both changed; measured after the build."""
import sys
REPL = [("else if(share(e,under)>=0.9){set(e,40);set(next(e),15);}", "else if(share(e,under)>=0.9){set(e,40);set(next(e),21);}   /* 2 Nov 2026 (owner 16:04): 21 below, as under a name line (was 15) */"),
        ("E=eff+15-(nt-bt);", "E=eff+18.3-(nt-bt);")]
def patch(s):
    for a, b in REPL:
        assert s.count(a) == 1, a; s = s.replace(a, b)
    return s
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
