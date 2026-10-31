"""The Poet - SECOND FLOOR: OPTIONAL DORMER vignette (image xref 22).
Traced walls and windows; lettering re-set."""
import blib as B, bhelp

PAGE, XREF = 4, 22
B.K, B.PXFT = 421.7, 38.0
TEXT = [(163, 122, 387, 217)]


def after(c):
    B.label(c, 270, 170, 'OPT. DORMER', '8\'-5" × 5\'-5"', name_pt=5.6)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, bands=False, after=after)
