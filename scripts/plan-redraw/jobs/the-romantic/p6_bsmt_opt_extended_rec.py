"""The Romantic - BASEMENT OPTIONS: EXTENDED REC ROOM WITH OPTIONAL SUNROOM ABOVE (brochure page 6, image xref 29), redrawn clean.

Source raster placed at 370.3 dpi, 46.2 px/ft like the basement. Traced and re-lettered only
(labels where they were printed), with the light concrete fill in the foundation lines.
"""
import blib as B
import bhelp

PAGE, XREF = 6, 29
K, PXFT = 370.3, 46.2

TEXT = [(462, 586, 770, 644), (1546, 576, 1854, 694)]
BAND_DROP = [(1120, 500, 1260, 640), (150, 462, 372, 530), (1490, 462, 1925, 530)]  # stair-free; windows stay white


def labels(c):
    bhelp.vlabel(c, 616, 615, 'OPT. REC ROOM')
    bhelp.vlabel(c, 1700, 635, 'OPT. DEN', '12\'-0" × 13\'-5"')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls = B.trace(img)[0]
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT + BAND_DROP, after=labels,
                   before=lambda c: B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY))
