"""The Expressionist I - BASEMENT OPTIONS: OPTIONAL DEN WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY ABOVE (brochure page 7, image xref 37), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only, with the light concrete fill in the foundation lines.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 37
K, PXFT = 370.4, 32.1

TEXT = [(330, 362, 562, 452)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 452, 405, 'OPT. DEN', '12\'-7" × 19\'-11"')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
