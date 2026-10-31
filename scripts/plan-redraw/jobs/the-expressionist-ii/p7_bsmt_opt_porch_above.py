"""The Expressionist II - BASEMENT OPTIONS: OPTIONAL PORCH ABOVE (brochure page 7, image xref 37), redrawn clean.

370.4 dpi, 29.6 px/ft. Traced (foundation band in the light concrete fill, as on the basement)
and re-lettered only; the bath fixtures at its edge are the optional bath, which keeps its fixtures.
"""
import blib as B
import bhelp

PAGE, XREF = 7, 37
K, PXFT = 370.4, 29.6
DROP = [(392, 148, 697, 186), (285, 268, 340, 323)]


def before(c):
    c.circle(312, 295, 23, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    o = B.OPT
    B.small(c, 545, 167, 'OPTIONAL PORCH ABOVE', size=3.8)
    B.small(c, 312, 288, 'EJEC.', size=2.6)
    B.small(c, 312, 303, 'PIT', size=2.6)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    # thin furring walls traced solid, as on the basement plan
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after,
                   add=[bhelp.thin_walls(img, drop=DROP)])
