"""The Innovator - FIRST FLOOR OPTIONS: OPTIONAL BAY (brochure page 3, image xref 21, 471.2 dpi).

The same picture as The Maestro's bay (jobs/the-maestro/p2_opt_bay.py, mean difference 1.5 of
255), run on this image through bhelp.reuse_k at this page's dpi. No lettering; nothing to modernise.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 3, 21
K, PXFT = 471.2, 46.1
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-maestro', 'p2_opt_bay.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse_k(c, img, SRC, K)
    B.K, B.PXFT = K, PXFT
