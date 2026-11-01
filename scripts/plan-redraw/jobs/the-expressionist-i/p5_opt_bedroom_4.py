"""The Expressionist I - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 4 (brochure page 5, image xref 32), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only. The optional bath keeps its tub, and its sink is already in a
vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 32
K, PXFT = 370.4, 32.1

TEXT = [(240, 143, 326, 224), (520, 304, 812, 382), (210, 468, 294, 547)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 283, 184, 'OPT.\nBATH', name_pt=4.8)
    L(c, 667, 343, 'OPTIONAL BEDROOM 4', '16\'-10" × 17\'-4"')
    L(c, 250, 508, 'OPT.\nW.I.C.', name_pt=4.8)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
