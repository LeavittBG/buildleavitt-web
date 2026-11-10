"""The Maestro - BASEMENT OPTIONS: walkout door (brochure page 5, image xref 29, placed at 446.4 dpi).

The same picture as The Craftsman's (jobs/the-craftsman/p4_opt_walkout_door.py) and The Entrepreneur's /
The Impressionist's copies of it (mean pixel difference under 4 of 255), so that job runs on this
image through bhelp.reuse_k, at this page's 446.4 dpi so its lettering prints at the same size as
the rest of this brochure. Every traced line comes from this picture. No modernising needed.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 5, 29
K, PXFT = 446.4, 46.2
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-craftsman', 'p4_opt_walkout_door.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse_k(c, img, SRC, K, dx=-1, dy=0)
    B.K, B.PXFT = K, PXFT
