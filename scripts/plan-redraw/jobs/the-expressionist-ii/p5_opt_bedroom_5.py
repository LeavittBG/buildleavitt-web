"""The Expressionist II - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 5 (brochure page 5, image xref 31), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only; the optional bath keeps its tub/shower and its vanity.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 31
K, PXFT = 370.4, 29.6
DROP = [(200, 281, 492, 358), (260, 562, 339, 638), (478, 602, 550, 674), (103, 765, 137, 791)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 346, 318, 'OPTIONAL BEDROOM 5', '17\'-9" × 15\'-9"')
    bhelp.vlabel(c, 300, 600, 'OPT.\nBATH', None, name_pt=4.6)
    bhelp.vlabel(c, 513, 638, 'OPT.\nW.I.C.', None, name_pt=4.6)
    B.small(c, 120, 778, 'UP', size=3.4, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
