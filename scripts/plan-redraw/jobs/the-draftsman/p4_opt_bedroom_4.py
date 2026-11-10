"""The Draftsman - SECOND FLOOR OPTIONS, "OPTIONAL BEDROOM 4" (page 4, xref 29), 669.6 dpi."""
import blib as B
import bhelp

PAGE, XREF = 4, 29
B.K, B.PXFT = 669.6, 38.0
WIN_DROP = [(150, 630, 190, 690)]


def after(c):
    bhelp.vlabel(c, 370, 320, 'OPTIONAL BEDROOM 4', '13\'-4" × 14\'-1"', name_pt=4.2, sub_pt=3.6)
    B.small(c, 556, 530, 'OPT. CLOSET', size=2.9, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 669.6, after=after, auto_text=False, win_drop=WIN_DROP,
                 drop=[(194, 272, 546, 368), (534, 432, 578, 628)])
