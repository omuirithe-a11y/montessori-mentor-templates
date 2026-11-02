"""2 Nov 2026 (owner 16:08, queued): "There needs to be clearer separation between each section, so for example Hornbooks shouldn't be so close
to the '101 Great Picture Books for Preschoolers'. Make it the same as the spacing between 20 Wonderful Picture Books and Cruise Into
Kindergarten" + "On all pages and in the template": a green heading with no beige line straight above it stands 51 px (letters to letters)
below the text above - the gap between two entries (measured 51 at 1440 on 8.3 build 11; Hornbooks 21.7)."""
import sys
OLD = "      set(next(h),25);});\n"
NEW = ("      set(next(h),25);});\n"
       "    /* 2 Nov 2026 (owner 16:08): a green heading with no beige line straight above it stands 51 below the text above, as one entry below the next */\n"
       "    [].forEach.call(m.querySelectorAll('h2.mm-hc-00B050'),function(h){if(h.closest('.res-entry'))return;\n"
       "      var s=h.parentElement&&h.parentElement.tagName==='SECTION'&&h.parentElement.firstElementChild===h?h.parentElement:h,pv=s.previousElementSibling;\n"
       "      if(!pv)return;var lp=pv.tagName==='SECTION'?pv.lastElementChild:pv;if(!rule(lp))set(h,51);});\n")
def patch(s):
    assert s.count(OLD) == 1; return s.replace(OLD, NEW)
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read(); open(sys.argv[2], 'w', encoding='utf-8').write(patch(s))
