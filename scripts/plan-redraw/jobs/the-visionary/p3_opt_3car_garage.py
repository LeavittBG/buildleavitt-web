"""The Visionary - FIRST FLOOR OPTIONS: OPTIONAL 3 CAR GARAGE (brochure page 3, image xref 21, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 3, 21
DROP = [(0, 788, 335, 902)]


def after(c):
    bhelp.vlabel(c, 133, 842, 'THREE-CAR GARAGE', '21\'-8" × 38\'-8"', name_pt=4.4, sub_pt=3.9)


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
