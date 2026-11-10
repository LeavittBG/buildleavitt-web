"""The Visionary - FIRST FLOOR OPTIONS: OPTIONAL SUNROOM (brochure page 3, image xref 24, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 3, 24
DROP = [(140, 200, 520, 320), (618, 100, 662, 335), (135, 515, 475, 630)]


def after(c):
    bhelp.vlabel(c, 327, 258, 'OPTIONAL SUNROOM', '12\'-11" × 10\'-4"')
    B.small(c, 637, 217, 'OPT. PATIO DOOR', size=3.8, color=B.OPT, rotate=-90)
    bhelp.vlabel(c, 305, 577, 'BREAKFAST NOOK', '9\'-10" × 15\'-2"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
