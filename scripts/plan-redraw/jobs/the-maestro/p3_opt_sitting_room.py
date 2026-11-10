"""The Maestro - SECOND FLOOR OPTIONS: OPTIONAL SITTING ROOM (brochure page 3, image xref 22,
1060x738 px placed at 945.8 dpi, 46.1 px/ft). Walls, windows and linework traced; lettering
re-set. The name sits in the half of the room east of the cathedral ridge line, as printed."""
import blib as B
import bhelp

PAGE, XREF = 3, 22
K, PXFT = 945.8, 46.1
DROP = [(610, 162, 790, 444), (535, 195, 570, 452)]


def after(c):
    bhelp.vlabel(c, 703, 322, 'OPTIONAL\nSITTING\nROOM', '11\'-1" × 9\'-0"', name_pt=3.8, sub_pt=3.3)
    B.small(c, 552, 323, 'CATHEDRAL CEILING', size=2.6, color=B.OPT, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
