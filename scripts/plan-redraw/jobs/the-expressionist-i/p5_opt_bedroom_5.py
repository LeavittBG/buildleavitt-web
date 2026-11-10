"""The Expressionist I - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 5 (brochure page 5, image xref 27), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only. The optional bath keeps its tub, and its sink is already in a
vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 27
K, PXFT = 370.4, 32.1

TEXT = [(355, 105, 440, 180), (155, 148, 238, 225), (160, 425, 445, 502)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 395, 142, 'OPT.\nW.I.C.', name_pt=4.8)
    L(c, 196, 187, 'OPT.\nBATH', name_pt=4.8)
    L(c, 302, 463, 'OPTIONAL BEDROOM 5', '14\'-11" × 15\'-11"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
