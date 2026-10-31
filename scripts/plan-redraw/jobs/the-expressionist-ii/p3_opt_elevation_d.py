"""The Expressionist II - FIRST FLOOR OPTIONS: ELEVATION D (brochure page 3, image xref 20), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 20
K, PXFT = 370.4, 29.6
DROP = [(120, 0, 325, 78), (586, 70, 672, 108), (815, 110, 1045, 190), (478, 216, 654, 254)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 222, 38, 'DINING ROOM', '13\'-6" × 15\'-4"')
    bhelp.vlabel(c, 633, 89, 'FOYER', None)
    bhelp.vlabel(c, 927, 147, 'LIVING ROOM', '13\'-5" × 15\'-5"')
    bhelp.vlabel(c, 565, 235, 'CONC. PORCH', None)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False,
                 win_drop=[(1300, 220, 1360, 340)])   # porch column, not a window
