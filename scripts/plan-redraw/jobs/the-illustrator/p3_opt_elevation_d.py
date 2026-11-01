"""The Illustrator - FIRST FLOOR OPTIONS, "ELEVATION D" (page 3, xref 20), redrawn clean.
Placed at 370.4 dpi, 32.3 px/ft like the first floor. Traced walls, windows, doors and porch;
lettering re-set as printed (an option drawing shows part of the house, so labels stay where they
were printed). No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
B.K, B.PXFT = 370.4, 32.3
TEXT = [(222, 0, 468, 95), (802, 46, 991, 88), (843, 94, 949, 134), (1137, 92, 1394, 190), (696, 238, 917, 287)]
WIN_DROP = []


def after(c):
    bhelp.vlabel(c, 345, 46, 'LIVING ROOM', '12\'-10" × 12\'-9"')
    bhelp.vlabel(c, 896, 90, 'TWO-STORY\nFOYER')
    bhelp.vlabel(c, 1266, 140, 'DINING ROOM', '12\'-10" × 16\'-10"')
    bhelp.vlabel(c, 806, 262, 'CONC. PORCH', name_pt=4.8)


def draw(c, img):
    bhelp.simple(c, img, 370.4, after=after, drop=TEXT, win_drop=WIN_DROP, auto_text=False)
