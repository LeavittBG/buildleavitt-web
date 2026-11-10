"""The Daydreamer - BASEMENT OPTIONS: 4' AREAWAY (page 6, xref 34). The same picture as The
Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_32.py, compared pixel by pixel), placed at 389.4 dpi, so it is
drawn by that job with every traced line taken from this image."""
import os
import blib as B, bhelp

PAGE, XREF = 6, 34
B.K = 389.4
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_32.py')


def draw(c, img):
    bhelp.reuse(c, img, SRC)
