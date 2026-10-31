"""The Daydreamer - SECOND FLOOR OPTIONS: OPTIONAL BATH (page 4, xref 28; 735 dpi, 37.8 px/ft).
A secondary bath: it keeps its tub/shower, and its sink is already in a vanity. Traced; lettering
re-set."""
import blib as B, bhelp

PAGE, XREF = 4, 28
B.K = 735.1
TEXT = [(263, 128, 357, 172), (432, 170, 525, 261), (212, 390, 446, 486), (821, 140, 929, 179),
        (1194, 140, 1302, 179), (542, 350, 650, 389)]


def after(c):
    B.small(c, 310, 150, 'MECH.', size=3.8, weight=700)
    bhelp.vlabel(c, 478, 216, 'OPT.\nBATH', name_pt=4.0)
    bhelp.vlabel(c, 302, 438, 'BEDROOM 2', '12\'-0" × 13\'-4"')
    for x, y in ((875, 159), (1248, 159), (596, 369)):
        B.small(c, x, y, 'W.I.C.', size=3.6)


def draw(c, img):
    bhelp.simple(c, img, 735.1, after=after, drop=TEXT, auto_text=False)
