"""The Novel - FIRST FLOOR OPTIONS, "OPTIONAL CONSERVATORY" (page 3, xref 20), redrawn clean.
Placed at 412.4 dpi, 37.95 px/ft. Traced walls, windows, doors and fireplace; lettering re-set as
printed. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
B.K, B.PXFT = 412.4, 37.95
TEXT = [(102, 362, 138, 648), (352, 466, 682, 501), (312, 642, 722, 688), (400, 688, 640, 736)]


def after(c):
    bhelp.vlabel(c, 517, 688, 'OPTIONAL CONSERVATORY', '13\'-6" × 21\'-1"')
    B.small(c, 517, 486, 'OPTIONAL CATHEDRAL CEILING', size=3.4, color=B.OPT)
    B.small(c, 120, 505, 'OPTIONAL GAS FIREPLACE', size=3.2, color=B.OPT, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 412.4, after=after, drop=TEXT, auto_text=False)
