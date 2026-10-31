"""The Entrepreneur - OPTIONAL THREE CAR GARAGE (brochure page 3, image xref 18), redrawn clean.

Source raster 1176x1914 px placed at 532 dpi; 46.2 px/ft (inside 21'-9" = 1011 px). Traced walls,
windows and linework; lettering re-set. No modernising needed: the entry steps, doors and the
butler's pantry are as on the first floor, and there is no garage-entry bench.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 18
K, PXFT = 532.0, 46.2

TEXT = [(410, 950, 812, 1065)]
WIN_DROP = [(760, 110, 960, 150)]


def labels(c):
    B.label(c, 628, 1000, 'THREE-CAR GARAGE', '21\'-9" × 37\'-10"')


def draw(c, img):
    B.PXFT = PXFT
    c.K = K
    bhelp.simple(c, img, K, after=labels, drop=TEXT, win_drop=WIN_DROP, auto_text=False)
