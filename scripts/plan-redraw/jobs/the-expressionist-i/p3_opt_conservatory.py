"""The Expressionist I - FIRST FLOOR OPTIONS: OPTIONAL CONSERVATORY (brochure page 3, image xref 21), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only; labels stay where they were printed.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 21
K, PXFT = 370.4, 32.1

TEXT = [(280, 372, 543, 401), (249, 509, 575, 545), (290, 544, 500, 586), (82, 290, 112, 510)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    S(c, 411, 386, 'OPTIONAL CATHEDRAL CEILING', size=4.0, color=B.OPT)
    L(c, 411, 545, 'OPTIONAL CONSERVATORY', '13\'-6" × 21\'-1"')
    S(c, 97, 400, 'OPTIONAL GAS FIREPLACE', size=3.8, color=B.OPT, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
