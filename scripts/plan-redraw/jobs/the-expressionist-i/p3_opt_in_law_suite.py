"""The Expressionist I - FIRST FLOOR OPTIONS: OPTIONAL IN-LAW SUITE (brochure page 3, image xref 23), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. Traced and re-lettered only. The optional bath keeps its tub/shower, and its sink is already
in a vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 23
K, PXFT = 370.4, 32.1

TEXT = [(225, 130, 305, 212), (104, 174, 181, 252), (75, 450, 388, 527)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 265, 172, 'OPT.\nW.I.C.', name_pt=4.8)
    L(c, 140, 213, 'OPT.\nBATH', name_pt=4.8)
    L(c, 231, 488, 'OPTIONAL IN-LAW SUITE', '13\'-6" × 15\'-11"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
