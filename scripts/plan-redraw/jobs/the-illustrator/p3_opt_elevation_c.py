"""The Illustrator - FIRST FLOOR OPTIONS, "ELEVATION C" (page 3, xref 21), redrawn clean.
Placed at 370.4 dpi, 32.3 px/ft like the first floor. Traced walls, windows, doors and porch;
lettering re-set as printed (an option drawing shows part of the house, so labels stay where they
were printed). No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 21
B.K, B.PXFT = 370.4, 32.3
TEXT = [(1137, 11, 1394, 108), (802, 41, 991, 83), (843, 89, 949, 129), (222, 70, 468, 166), (918, 233, 1138, 282)]
WIN_DROP = [(1460, 330, 1505, 375)]


def after(c):
    bhelp.vlabel(c, 1266, 58, 'DINING ROOM', '12\'-10" × 14\'-10"')
    bhelp.vlabel(c, 896, 85, 'TWO-STORY\nFOYER')
    bhelp.vlabel(c, 345, 118, 'LIVING ROOM', '12\'-10" × 14\'-9"')
    bhelp.vlabel(c, 1028, 257, 'CONC. PORCH', name_pt=4.8)


def draw(c, img):
    bhelp.simple(c, img, 370.4, after=after, drop=TEXT, win_drop=WIN_DROP, auto_text=False)
