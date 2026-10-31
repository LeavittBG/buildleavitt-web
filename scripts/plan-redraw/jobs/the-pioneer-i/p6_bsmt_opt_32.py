"""The Pioneer I - BASEMENT OPTIONS: OPTIONAL 4' AREAWAY (brochure page 6, image xref 32,
499x699 px, 438 dpi). Traced walls, stair, door and linework; concrete fill in the areaway walls
and the house foundation; UP arrow re-set in Roboto Condensed."""
import sys
import blib as B, bhelp

PAGE, XREF = 6, 32
IMG = None   # set by draw()
TEXT = [(205, 222, 256, 310)]
STAIR = [(176, 25, 325, 462), (180, 462, 322, 568)]


def after(c):
    for y in (226, 264, 302.5):                 # tread lines under the erased UP lettering
        c.rect(204, y - 2, 53, 4, sw=0, fill=B.NAVY)
    B.arrow(c, [(249, 300), (249, 230)], w=0.45)
    B.small(c, 231, 245, 'UP', size=4.0, rotate=-90)


def _draw(c):
    bhelp.vignette(c, IMG, drop=TEXT, band_drop=STAIR, after=after)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
