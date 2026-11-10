"""The Expressionist I - SECOND FLOOR OPTIONS: ELEVATION D (brochure page 5, image xref 28), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. The front wall for Elevation D; traced and re-lettered only. The room name cut by the frame
at the top is set again in the same place, so the frame cuts it the same way.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 28
K, PXFT = 370.4, 32.1

TEXT = [(130, 0, 320, 76), (830, 58, 1018, 136)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 226, 38, 'BEDROOM 3', '13\'-1" × 15\'-4"')
    L(c, 925, 97, 'BEDROOM 2', '12\'-9" × 17\'-3"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False)
