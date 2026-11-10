"""The Expressionist I - BASEMENT OPTIONS: OPTIONAL 4' AREAWAY (brochure page 7, image xref 38), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only, with the light concrete fill in the foundation lines.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 38
K, PXFT = 370.4, 32.1

TEXT = [(175, 185, 227, 226)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    S(c, 200, 210, 'UP', size=4.2)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
