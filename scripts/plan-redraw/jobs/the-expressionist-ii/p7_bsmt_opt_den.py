"""The Expressionist II - BASEMENT OPTIONS: OPTIONAL DEN WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY ABOVE (brochure page 7, image xref 38), redrawn clean.

370.4 dpi, 29.6 px/ft. Traced (foundation band in the light concrete fill, as on the basement)
and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 38
K, PXFT = 370.4, 29.6
DROP = [(345, 366, 565, 449)]


def before(c):
    pass


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 455, 407, 'OPT. DEN', '12\'-7" × 19\'-11"')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    # thin furring walls traced solid, as on the basement plan
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after,
                   add=[bhelp.thin_walls(img, drop=DROP)])
