"""The Visionary - SECOND FLOOR OPTIONS: ELEVATION C (brochure page 5, image xref 30, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 5, 30
DROP = [(155, 0, 410, 100), (580, 0, 808, 92), (1005, 0, 1258, 100)]


def after(c):
    L, S = bhelp.vlabel, B.small
    L(c, 281, 45, 'BEDROOM 3', '12\'-5" × 14\'-0"')
    L(c, 694, 44, 'OPEN TO\nFOYER BELOW', name_pt=4.8)
    L(c, 1131, 45, 'BEDROOM 2', '12\'-3" × 14\'-6"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
