"""The Expressionist II - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 7, image xref 35), redrawn clean.

370.4 dpi, 29.6 px/ft. Traced (foundation band in the light concrete fill, as on the basement)
and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 35
K, PXFT = 370.4, 29.6
DROP = [(0, 116, 31, 276)]


def before(c):
    pass


def after(c):
    o = B.OPT
    B.small(c, 15, 196, 'OPT. PATIO DOOR', size=3.2, color=o, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after)
