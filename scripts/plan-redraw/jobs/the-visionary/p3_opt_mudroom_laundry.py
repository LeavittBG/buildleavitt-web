"""The Visionary - FIRST FLOOR OPTIONS: OPTIONAL MUDROOM AND LAUNDRY (brochure page 3, image xref 20, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed.
No bench or desk here; nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
DROP = [(773, 0, 898, 36), (510, 160, 880, 260), (165, 335, 370, 385), (480, 490, 835, 612)]


def after(c):
    B.small(c, 834, 17, 'PANTRY', size=3.6)
    bhelp.vlabel(c, 660, 222, 'OPTIONAL MUDROOM', '14\'-11" × 6\'-0"')
    bhelp.vlabel(c, 272, 360, 'LAUNDRY', name_pt=4.8)
    bhelp.vlabel(c, 657, 552, 'TWO-CAR GARAGE', '21\'-8" × 28\'-8"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
