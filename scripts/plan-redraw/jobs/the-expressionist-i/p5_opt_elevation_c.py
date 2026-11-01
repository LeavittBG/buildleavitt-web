"""The Expressionist I - SECOND FLOOR OPTIONS: ELEVATION C (brochure page 5, image xref 31), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. The front wall for Elevation C; traced and re-lettered only.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 31
K, PXFT = 370.4, 32.1

TEXT = [(134, 21, 318, 101), (830, 24, 1018, 104)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 226, 61, 'BEDROOM 3', '13\'-1" × 17\'-4"')
    L(c, 925, 64, 'BEDROOM 2', '12\'-9" × 15\'-3"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
