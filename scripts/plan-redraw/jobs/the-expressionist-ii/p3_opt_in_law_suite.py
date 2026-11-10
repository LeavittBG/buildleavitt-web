"""The Expressionist II - FIRST FLOOR OPTIONS: OPTIONAL IN-LAW SUITE (brochure page 3, image xref 22), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only; the optional bath keeps its tub/shower and its vanity.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 22
K, PXFT = 370.4, 29.6
DROP = [(236, 135, 302, 210), (102, 175, 182, 252), (70, 450, 392, 528)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 268, 172, 'OPT.\nW.I.C.', None, name_pt=4.6)
    bhelp.vlabel(c, 140, 213, 'OPT.\nBATH', None, name_pt=4.6)
    bhelp.vlabel(c, 231, 488, 'OPTIONAL\nIN-LAW SUITE', '13\'-6" × 15\'-11"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
