"""The Expressionist II - SECOND FLOOR OPTIONS: ELEVATION D (brochure page 5, image xref 30), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 30
K, PXFT = 370.4, 29.6
DROP = [(120, 0, 325, 80), (815, 60, 1045, 140)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 220, 38, 'BEDROOM 3', '13\'-1" × 15\'-4"')
    bhelp.vlabel(c, 925, 98, 'BEDROOM 2', '12\'-9" × 17\'-3"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
