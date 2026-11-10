"""The Innovator - BASEMENT OPTIONS: 4' areaway (brochure page 5, image xref 27, placed at 711.8 dpi).

The same picture as The Craftsman's (jobs/the-craftsman/p4_opt_4ft_areaway.py), so that job runs on this image
through bhelp.reuse_k at this page's dpi; every traced line comes from this picture. Nothing to
modernise.
"""
import os
import blib as B
import bhelp

PAGE, XREF = 5, 27
K, PXFT = 711.8, 46.2
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-craftsman', 'p4_opt_4ft_areaway.py')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.reuse_k(c, img, SRC, K, dx=-1, dy=-1)
    B.K, B.PXFT = K, PXFT
