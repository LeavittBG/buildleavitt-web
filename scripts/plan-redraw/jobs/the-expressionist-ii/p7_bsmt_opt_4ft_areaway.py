"""The Expressionist II - BASEMENT OPTIONS: OPTIONAL 4' AREAWAY (brochure page 7, image xref 39), redrawn clean.

370.4 dpi, 29.6 px/ft. Traced (foundation band in the light concrete fill, as on the basement)
and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 39
K, PXFT = 370.4, 29.6
DROP = [(162, 190, 232, 231)]


def before(c):
    for x in (180.0, 210.0):                    # tread lines under the old lettering
        c.line(x, 190, x, 231, 0.95, color=B.NAVY)


def after(c):
    o = B.OPT
    B.arrow(c, [(228, 198), (166, 198)])
    B.small(c, 205, 214, 'UP', size=3.6, bg='#ffffff')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    # no concrete fill here: the band finder reads the gaps between treads as foundation
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after, bands=False)
