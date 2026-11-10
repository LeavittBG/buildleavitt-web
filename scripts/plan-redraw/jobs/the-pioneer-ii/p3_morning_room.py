"""The Pioneer II - page 3, image xref 21: the same picture moved (-1, 0) px as The Pioneer I's
jobs/the-pioneer-i/p3_first_opt_23.py (measured pixel for pixel), so it is drawn by that job, with every
traced line taken from this image. Its modernisations are The Pioneer I's."""
import os
import bhelp

PAGE, XREF = 3, 21
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p3_first_opt_23.py')


def draw(c, img):
    bhelp.reuse(c, img, SRC, dx=-1, dy=0, drop_text=())
