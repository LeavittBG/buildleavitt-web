"""The Expressionist II - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 4 (brochure page 5, image xref 29), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only; the optional bath keeps its tub/shower and its vanity.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 29
K, PXFT = 370.4, 29.6
DROP = [(362, 108, 428, 184), (158, 149, 238, 225), (150, 426, 450, 503)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 394, 145, 'OPT.\nW.I.C.', None, name_pt=4.6)
    bhelp.vlabel(c, 196, 187, 'OPT.\nBATH', None, name_pt=4.6)
    bhelp.vlabel(c, 300, 463, 'OPTIONAL BEDROOM 4', '14\'-11" × 15\'-11"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
