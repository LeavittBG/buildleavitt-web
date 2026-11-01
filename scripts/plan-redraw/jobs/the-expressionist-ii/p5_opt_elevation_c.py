"""The Expressionist II - SECOND FLOOR OPTIONS: ELEVATION C (brochure page 5, image xref 28), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 28
K, PXFT = 370.4, 29.6
DROP = [(120, 23, 325, 103), (815, 26, 1045, 105)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 220, 61, 'BEDROOM 3', '13\'-1" × 17\'-4"')
    bhelp.vlabel(c, 925, 63, 'BEDROOM 2', '12\'-9" × 15\'-3"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
