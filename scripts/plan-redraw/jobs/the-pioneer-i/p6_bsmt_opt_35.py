"""The Pioneer I - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 6, image
xref 35, 499x173 px, 438 dpi). Traced walls, slider and swing lines; concrete foundation band;
lettering re-set in Roboto Condensed."""
import sys
import blib as B, bhelp

PAGE, XREF = 6, 35
IMG = None   # set by draw()
TEXT = [(152, 2, 348, 31)]


def after(c):
    B.small(c, 250, 18, 'OPT. PATIO DOOR', size=3.8, color=B.OPT)


def _draw(c):
    bhelp.vignette(c, IMG, drop=TEXT, after=after)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
