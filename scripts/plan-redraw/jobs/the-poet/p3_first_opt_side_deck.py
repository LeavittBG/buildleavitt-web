"""The Poet - FIRST FLOOR OPTIONS: OPTIONAL SIDE DECK (image xref 18).
Traced walls, door and deck outline; lettering re-set."""
import blib as B, bhelp

PAGE, XREF = 3, 18
B.K, B.PXFT = 421.7, 38.0
TEXT = [(156, 157, 200, 410)]


def after(c):
    B.label(c, 179, 283, 'OPTIONAL DECK', name_pt=5.0, rotate=-90)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, bands=False, after=after)
