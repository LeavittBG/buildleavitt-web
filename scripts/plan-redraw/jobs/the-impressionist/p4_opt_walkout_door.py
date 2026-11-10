"""The Impressionist - DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 4, image xref 22), redrawn clean.

The same picture as The Craftsman's (jobs/the-craftsman/p4_opt_walkout_door.py), shifted by (-1, 0) px
(mean pixel difference about 10 of 255), placed here at 711.6 dpi. That job runs on this image via
bhelp.reuse, so every traced line comes from this picture. No modernising needed.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 4, 22
K, PXFT = 711.6, 46.2
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-craftsman', 'p4_opt_walkout_door.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse(c, img, SRC, dx=-1, dy=0)
    B.K, B.PXFT = K, PXFT          # the reused job sets its own placement dpi
