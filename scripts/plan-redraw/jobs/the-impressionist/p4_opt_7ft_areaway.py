"""The Impressionist - OPTIONAL 7' AREAWAY (brochure page 4, image xref 21), redrawn clean.

The same picture as The Craftsman's (jobs/the-craftsman/p4_opt_7ft_areaway.py), within 1 px
(mean pixel difference about 6 of 255), placed here at 712.0 dpi. That job runs on this image via
bhelp.reuse, so every traced line comes from this picture. No modernising needed.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 4, 21
K, PXFT = 712.0, 46.2
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-craftsman', 'p4_opt_7ft_areaway.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse(c, img, SRC, dx=0, dy=0, drop_text=('PATIO',))
    B.small(c, 486, 793, 'OPT. PATIO DOOR', size=3.4, color=B.OPT)   # smaller: the bold face ran off the frame
    B.K, B.PXFT = K, PXFT          # the reused job sets its own placement dpi
