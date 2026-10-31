"""The Expressionist II - BASEMENT OPTIONS: OPTIONAL 7' AREAWAY (brochure page 7, image xref 36), redrawn clean.

370.4 dpi, 29.6 px/ft. Traced (foundation band in the light concrete fill, as on the basement)
and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 36
K, PXFT = 370.4, 29.6
DROP = [(505, 2, 533, 152), (162, 176, 232, 219)]


def before(c):
    for x in (180.5, 210.5):                    # tread lines under the old lettering
        c.line(x, 176, x, 219, 0.95, color=B.NAVY)


def after(c):
    o = B.OPT
    B.small(c, 519, 77, 'OPT. PATIO DOOR', size=3.2, color=o, rotate=-90)
    B.arrow(c, [(228, 190), (166, 190)])
    B.small(c, 205, 205, 'UP', size=3.6, bg='#ffffff')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    # no concrete fill here: the band finder reads the gaps between treads as foundation
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after, bands=False)
