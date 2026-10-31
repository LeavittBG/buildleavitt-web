"""The Impressionist - OPTIONAL 4' AREAWAY (brochure page 4, image xref 19), redrawn clean.

The same picture as The Craftsman's (jobs/the-craftsman/p4_opt_4ft_areaway.py), shifted by (0, -1) px
(mean pixel difference about 5 of 255), placed here at 711.8 dpi. That job runs on this image via
bhelp.reuse, so every traced line comes from this picture. No modernising needed.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 4, 19
K, PXFT = 711.8, 46.2
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-craftsman', 'p4_opt_4ft_areaway.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse(c, img, SRC, dx=0, dy=-1)
    B.K, B.PXFT = K, PXFT          # the reused job sets its own placement dpi
