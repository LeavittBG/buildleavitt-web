"""The Illustrator - SECOND FLOOR OPTIONS, "OPTIONAL BUDDY BATH" (page 5, xref 28), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered; the buddy bath keeps its tub/shower and vanity."""
import blib as B
import bhelp

PAGE, XREF = 5, 28
B.K, B.PXFT = 444.6, 32.3
TEXT = [(169, 172, 283, 267), (302, 302, 338, 376)]
WIN_DROP = [(70, 240, 125, 300)]

def after(c):
    bhelp.vlabel(c, 222, 220, 'BUDDY\nBATH')
    B.small(c, 320, 339, 'LINEN', size=3.6, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
