"""The Draftsman - BASEMENT OPTIONS, "OPTIONAL 7' AREAWAY" (page 6, xref 37).
The same drawing as The Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_34.py) moved 1 px left, so
that job runs on this brochure's own picture. 420.9 dpi."""
import os
import blib as B
import bhelp

PAGE, XREF = 6, 37
B.K, B.PXFT = 420.9, 38.0
JOB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_34.py')


def draw(c, img):
    bhelp.reuse(c, img, JOB, dx=-1)
