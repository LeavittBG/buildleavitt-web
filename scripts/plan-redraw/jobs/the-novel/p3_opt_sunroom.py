"""The Novel - FIRST FLOOR OPTIONS, "OPTIONAL SUNROOM" (page 3, xref 22), redrawn clean.
Placed at 412.4 dpi, 37.95 px/ft. Traced walls, windows, patio doors, column and the kitchen corner;
lettering re-set as printed. No modernising needed (the kitchen counter shown is the perimeter run)."""
import blib as B
import bhelp

PAGE, XREF = 3, 22
B.K, B.PXFT = 412.4, 37.95
TEXT = [(340, 224, 660, 274), (385, 274, 612, 322)]


def after(c):
    bhelp.vlabel(c, 500, 272, 'OPTIONAL SUNROOM', '19\'-9" × 11\'-6"')


def draw(c, img):
    bhelp.simple(c, img, 412.4, after=after, drop=TEXT, auto_text=False)
