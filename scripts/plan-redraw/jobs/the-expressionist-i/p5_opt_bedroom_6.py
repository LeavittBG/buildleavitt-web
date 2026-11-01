"""The Expressionist I - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 6 (brochure page 5, image xref 30), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only. The optional bath keeps its tub, and its sink is already in a
vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 30
K, PXFT = 370.4, 32.1

TEXT = [(205, 280, 488, 355), (255, 560, 342, 640), (465, 600, 558, 674), (102, 764, 138, 792)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 346, 318, 'OPTIONAL BEDROOM 6', '17\'-9" × 15\'-9"')
    L(c, 300, 602, 'OPT.\nBATH', name_pt=4.8)
    L(c, 512, 640, 'OPT.\nW.I.C.', name_pt=4.8)
    S(c, 120, 778, 'UP', size=3.8, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
