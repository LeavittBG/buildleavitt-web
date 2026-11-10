"""The Illustrator - FIRST FLOOR OPTIONS, "ELEVATION B" (page 3, xref 23), redrawn clean.
Placed at 370.4 dpi, 32.3 px/ft like the first floor. Traced walls, windows, doors and porch;
lettering re-set as printed (an option drawing shows part of the house, so labels stay where they
were printed). No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 23
B.K, B.PXFT = 370.4, 32.3
TEXT = [(802, 2, 991, 44), (843, 50, 949, 90), (222, 30, 468, 126), (1137, 48, 1394, 144), (696, 232, 917, 281)]
WIN_DROP = []


def after(c):
    bhelp.vlabel(c, 896, 46, 'TWO-STORY\nFOYER')
    bhelp.vlabel(c, 345, 78, 'LIVING ROOM', '12\'-10" × 13\'-9"')
    bhelp.vlabel(c, 1266, 96, 'DINING ROOM', '12\'-10" × 15\'-10"')
    bhelp.vlabel(c, 806, 256, 'CONC. PORCH', name_pt=4.8)


def draw(c, img):
    bhelp.simple(c, img, 370.4, after=after, drop=TEXT, win_drop=WIN_DROP, auto_text=False)
