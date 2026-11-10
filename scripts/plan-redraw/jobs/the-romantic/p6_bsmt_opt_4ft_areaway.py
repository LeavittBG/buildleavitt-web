"""The Romantic - BASEMENT OPTIONS: OPTIONAL 4' AREAWAY (brochure page 6, image xref 26), redrawn clean.

Source raster placed at 370.3 dpi, 46.2 px/ft like the basement. Traced and re-lettered only
(labels where they were printed), with the light concrete fill in the foundation lines.
"""
import blib as B
import bhelp

PAGE, XREF = 6, 26
K, PXFT = 370.3, 46.2

TEXT = [(214, 296, 258, 348)]
BAND_DROP = [(120, 0, 330, 690)]


def labels(c):
    B.small(c, 236, 322, 'UP', size=4.2, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT + BAND_DROP, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
