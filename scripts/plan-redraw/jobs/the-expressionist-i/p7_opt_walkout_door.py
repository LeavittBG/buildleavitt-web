"""The Expressionist I - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 7, image xref 39), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 39
K, PXFT = 370.4, 32.1

TEXT = [(0, 118, 32, 276)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    S(c, 16, 197, 'OPT. PATIO DOOR', size=3.6, color=B.OPT, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
