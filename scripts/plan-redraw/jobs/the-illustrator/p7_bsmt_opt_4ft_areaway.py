"""The Illustrator - BASEMENT OPTIONS, "OPTIONAL 4' AREAWAY" (page 7, xref 40).
The same drawing as The Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_32.py; offset dx=0), so that job runs
on this brochure's own picture. Placed at 370.4 dpi."""
import os
import blib as B
import bhelp

PAGE, XREF = 7, 40
B.K, B.PXFT = 370.4, 37.8
JOB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_32.py')


def draw(c, img):
    bhelp.reuse(c, img, JOB, dx=0)
