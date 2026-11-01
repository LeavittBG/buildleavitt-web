"""The Novel - FIRST FLOOR OPTIONS, "OPTIONAL IN-LAW SUITE" (page 3, xref 21), redrawn clean.
Placed at 412.4 dpi, 37.95 px/ft. Traced walls, windows, doors and the optional bath (it keeps its
tub/shower; its sink is already in a vanity). Lettering re-set as printed."""
import blib as B
import bhelp

PAGE, XREF = 3, 21
B.K, B.PXFT = 412.4, 37.95
TEXT = [(138, 195, 232, 290), (378, 142, 472, 240), (86, 543, 478, 592), (160, 590, 396, 640)]


def after(c):
    bhelp.vlabel(c, 185, 242, 'OPT.\nBATH', name_pt=4.4)
    bhelp.vlabel(c, 422, 190, 'OPT.\nW.I.C.', name_pt=4.4)
    bhelp.vlabel(c, 281, 590, 'OPTIONAL IN-LAW SUITE', '13\'-6" × 15\'-5"')


def draw(c, img):
    bhelp.simple(c, img, 412.4, after=after, drop=TEXT, auto_text=False)
