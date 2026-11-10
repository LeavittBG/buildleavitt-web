"""The Maestro - FIRST FLOOR OPTIONS: OPTIONAL MORNING ROOM (brochure page 2, image xref 14,
715x786 px placed at 658.2 dpi, 46.1 px/ft). Walls, windows and linework traced; lettering re-set.
The name sits in the half of the room east of the cathedral ridge line, as printed."""
import blib as B
import bhelp

PAGE, XREF = 2, 14
K, PXFT = 658.2, 46.1
DROP = [(455, 67, 633, 345), (55, 220, 92, 447), (366, 216, 396, 473)]


def after(c):
    bhelp.vlabel(c, 541, 340, 'OPTIONAL\nMORNING\nROOM', '12\'-0" × 13\'-6"', name_pt=4.4, sub_pt=3.8)
    B.small(c, 381, 345, 'CATHEDRAL CEILING', size=3.0, color=B.OPT, rotate=-90)
    B.small(c, 73, 333, 'OPT. PATIO DOOR', size=3.0, color=B.OPT, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
