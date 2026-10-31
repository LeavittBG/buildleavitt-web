"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL CONSERVATORY (page 3, xref 23; 482 dpi,
37.8 px/ft). Traced; re-lettered."""
import blib as B, bhelp

PAGE, XREF = 3, 23
B.K = 482.0
SKIP = [(270, 490, 315, 520), (820, 110, 860, 205)]   # window mark, opt. window lines
TEXT = [(100, 365, 140, 645), (334, 641, 745, 738), (375, 469, 702, 504)]                          # "OPTIONAL GAS FIREPLACE", turned


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 539, 690, 'OPTIONAL\nCONSERVATORY', '13\'-6" × 21\'-1"')
    B.small(c, 539, 487, 'OPTIONAL CATHEDRAL CEILING', size=3.6, color=o)
    B.small(c, 121, 505, 'OPTIONAL GAS FIREPLACE', size=3.4, color=o, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 482.0, after=after, drop=TEXT, auto_text=False)
