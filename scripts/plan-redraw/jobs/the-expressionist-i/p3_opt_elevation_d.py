"""The Expressionist I - FIRST FLOOR OPTIONS: ELEVATION D (brochure page 3, image xref 20), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. The front wall for Elevation D; traced and re-lettered only. The room names cut by the
frame at the top are set again in the same place, so the frame cuts them the same way.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 20
K, PXFT = 370.4, 32.1

TEXT = [(130, 0, 330, 76), (578, 70, 674, 108), (835, 108, 1032, 188), (478, 217, 652, 253)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 230, 38, 'DINING ROOM', '13\'-6" × 15\'-4"')
    L(c, 626, 89, 'FOYER', name_pt=5.2)
    L(c, 929, 147, 'LIVING ROOM', '13\'-5" × 15\'-5"')
    L(c, 565, 235, 'CONC. PORCH', name_pt=4.8)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False, win_drop=[(1305, 280, 1355, 345)])
