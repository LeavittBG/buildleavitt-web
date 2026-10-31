"""The Draftsman - BASEMENT OPTIONS, "OPTIONAL 4' AREAWAY" (page 6, xref 33).
The same drawing as The Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_32.py; mean pixel difference
about 2 of 255, no offset), so that job runs on this brochure's own picture. 420.9 dpi."""
import os
import blib as B
import bhelp

PAGE, XREF = 6, 33
B.K, B.PXFT = 420.9, 38.0
JOB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_32.py')


def draw(c, img):
    bhelp.reuse(c, img, JOB)
