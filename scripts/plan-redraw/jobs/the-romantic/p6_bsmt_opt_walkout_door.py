"""The Romantic - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 6, image xref 28), redrawn clean.

Source raster placed at 370.3 dpi, 46.2 px/ft like the basement. Traced and re-lettered only
(labels where they were printed), with the light concrete fill in the foundation lines.
"""
import blib as B
import bhelp

PAGE, XREF = 6, 28
K, PXFT = 370.3, 46.2

TEXT = [(146, 2, 380, 40)]
BAND_DROP = []


def labels(c):
    B.small(c, 263, 22, 'OPT. PATIO DOOR', size=3.8, color=B.OPT)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT + BAND_DROP, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
