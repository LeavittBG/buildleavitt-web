"""The Expressionist II - FIRST FLOOR OPTIONS: OPTIONAL CONSERVATORY (brochure page 3, image xref 24), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 24
K, PXFT = 370.4, 29.6
DROP = [(280, 371, 543, 402), (249, 508, 575, 583), (82, 290, 111, 511)]


def after(c):
    o = B.OPT
    B.small(c, 411, 387, 'OPTIONAL CATHEDRAL CEILING', size=3.4, color=o)
    bhelp.vlabel(c, 412, 545, 'OPTIONAL CONSERVATORY', '13\'-6" × 21\'-1"')
    B.small(c, 96, 400, 'OPTIONAL GAS FIREPLACE', size=3.2, color=o, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
