"""The Innovator - FIRST FLOOR OPTIONS: OPTIONAL BEDROOM 3 (brochure page 3, image xref 20,
687x962 px placed at 471.5 dpi, 46.1 px/ft). Traced, re-lettered as printed, name centred in the
room; nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
K, PXFT = 471.5, 46.1
DROP = [(130, 158, 280, 210), (38, 308, 112, 418), (78, 428, 497, 538)]


def labels(c):
    bhelp.vlabel(c, 300, 525, 'OPTIONAL BEDROOM 3', '11\'-5" × 15\'-8"')
    B.small(c, 205, 184, 'CLOSET', size=4.0)
    B.small(c, 55, 363, 'OPT.', size=3.4, color=B.OPT, rotate=-90)
    B.small(c, 92, 363, 'WINDOW', size=3.4, color=B.OPT, rotate=-90)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, auto_text=False, drop=DROP, after=labels)
