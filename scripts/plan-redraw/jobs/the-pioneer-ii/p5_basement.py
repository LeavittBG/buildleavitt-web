"""The Pioneer II - page 5, image xref 28: the same picture moved (0, -76) px as The Pioneer I's
jobs/the-pioneer-i/p5_bsmt.py (measured pixel for pixel), so it is drawn by that job, with every
traced line taken from this image. Its modernisations are The Pioneer I's."""
import os
import bhelp

PAGE, XREF = 5, 28
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p5_bsmt.py')


def draw(c, img):
    bhelp.reuse(c, img, SRC, dx=0, dy=-76, drop_text=('FAMILY ROOM EXTENSION',))
