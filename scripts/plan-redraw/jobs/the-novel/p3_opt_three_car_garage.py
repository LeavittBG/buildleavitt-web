"""The Novel - FIRST FLOOR OPTIONS, "OPTIONAL 3 CAR GARAGE" (page 3, xref 19), redrawn clean.
Placed at 412.4 dpi, 37.95 px/ft like the first floor. Traced walls, door and garage-door line;
lettering re-set as printed. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 19
B.K, B.PXFT = 412.4, 37.95
TEXT = [(0, 805, 330, 902)]


def after(c):
    bhelp.vlabel(c, 165, 855, 'THREE-CAR GARAGE', '21\'-7" × 27\'-10"')


def draw(c, img):
    bhelp.simple(c, img, 412.4, after=after, drop=TEXT, auto_text=False)
