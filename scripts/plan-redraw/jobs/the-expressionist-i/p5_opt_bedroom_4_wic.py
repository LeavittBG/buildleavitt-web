"""The Expressionist I - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 4 WITH OPTIONAL EXTENDED W.I.C. (brochure page 5, image xref 29), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only. The optional bath keeps its tub, and its sink is already in a
vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 29
K, PXFT = 370.4, 32.1

TEXT = [(235, 147, 314, 224), (424, 306, 703, 384), (560, 732, 645, 808), (560, 1056, 645, 1132)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 273, 186, 'OPT.\nBATH', name_pt=4.8)
    L(c, 563, 345, 'OPTIONAL BEDROOM 4', '24\'-11" × 17\'-4"')
    L(c, 602, 770, 'OPT.\nW.I.C.', name_pt=4.8)
    L(c, 602, 1094, 'OPT.\nW.I.C.', name_pt=4.8)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
