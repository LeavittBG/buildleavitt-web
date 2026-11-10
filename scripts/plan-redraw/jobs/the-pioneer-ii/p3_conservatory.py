"""The Pioneer II - page 3, image xref 19: the same picture as The Pioneer I's
jobs/the-pioneer-i/p3_first_opt_19.py (measured pixel for pixel), so it is drawn by that job, with every
traced line taken from this image. Its modernisations are The Pioneer I's."""
import os
import bhelp

PAGE, XREF = 3, 19
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p3_first_opt_19.py')


def draw(c, img):
    bhelp.reuse(c, img, SRC, dx=0, dy=0, drop_text=())
