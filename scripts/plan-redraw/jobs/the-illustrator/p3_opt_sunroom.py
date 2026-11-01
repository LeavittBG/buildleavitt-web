"""The Illustrator - FIRST FLOOR OPTIONS, "OPTIONAL SUNROOM" (page 3, xref 22), redrawn clean.
Placed at 370.4 dpi, 32.3 px/ft like the first floor. Traced walls, windows, doors and porch;
lettering re-set as printed (an option drawing shows part of the house, so labels stay where they
were printed). No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 22
B.K, B.PXFT = 370.4, 32.3
TEXT = [(175, 118, 392, 262), (525, 112, 560, 308), (163, 421, 355, 514)]
WIN_DROP = []


def after(c):
    bhelp.vlabel(c, 283, 190, 'OPTIONAL\nSUNROOM', '10\'-6" × 9\'-6"')
    B.small(c, 542, 210, 'OPT. PATIO DOOR', size=3.6, color=B.OPT, rotate=-90)
    bhelp.vlabel(c, 259, 468, 'BREAKFAST\nNOOK')


def draw(c, img):
    bhelp.simple(c, img, 370.4, after=after, drop=TEXT, win_drop=WIN_DROP, auto_text=False)
