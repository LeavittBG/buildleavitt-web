"""The Expressionist I - FIRST FLOOR OPTIONS: ELEVATION C (brochure page 3, image xref 22), redrawn clean.

Source raster placed at 370.4 dpi, about 32.1 px/ft, the same scale as the main floors. The front wall for Elevation C; traced and re-lettered only. The room name cut by the
frame at the top is set again in the same place, so the frame cuts it the same way.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 22
K, PXFT = 370.4, 32.1

TEXT = [(835, 0, 1022, 76), (578, 33, 674, 70), (130, 78, 330, 156), (478, 179, 652, 215)]


def labels(c):
    L, S = bhelp.vlabel, B.small
    L(c, 929, 38, 'LIVING ROOM', '13\'-5" × 13\'-5"')
    L(c, 626, 52, 'FOYER', name_pt=5.2)
    L(c, 229, 116, 'DINING ROOM', '13\'-6" × 17\'-4"')
    L(c, 565, 197, 'CONC. PORCH', name_pt=4.8)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=labels, drop=TEXT, auto_text=False, win_drop=[(1305, 215, 1355, 280)])
