"""The Expressionist II - FIRST FLOOR OPTIONS: ELEVATION C (brochure page 3, image xref 21), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 21
K, PXFT = 370.4, 29.6
DROP = [(815, 0, 1045, 80), (586, 33, 672, 71), (120, 78, 325, 158), (478, 178, 654, 216)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 927, 38, 'LIVING ROOM', '13\'-5" × 13\'-5"')
    bhelp.vlabel(c, 632, 52, 'FOYER', None)
    bhelp.vlabel(c, 220, 116, 'DINING ROOM', '13\'-6" × 17\'-4"')
    bhelp.vlabel(c, 565, 197, 'CONC. PORCH', None)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False,
                 win_drop=[(1300, 220, 1360, 340)])   # porch column, not a window
