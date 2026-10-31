"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL IN-LAW SUITE (page 3, xref 24). The same
picture as The Pioneer I's in-law suite (jobs/the-pioneer-i/p3_first_opt_20.py), placed at 482 dpi,
so it is drawn by that job with every traced line taken from this image. Its bath keeps the tub."""
import os
import blib as B, bhelp

PAGE, XREF = 3, 24
B.K = 482.0
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p3_first_opt_20.py')


def draw(c, img):
    bhelp.reuse(c, img, SRC)
