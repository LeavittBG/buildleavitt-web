"""The Illustrator - SECOND FLOOR OPTIONS, "OPTIONAL BEDROOM 5" (page 5, xref 34), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered; no modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 5, 34
B.K, B.PXFT = 444.6, 32.3
TEXT = [(175, 202, 523, 298), (358, 439, 553, 469)]
WIN_DROP = []

def after(c):
    bhelp.vlabel(c, 349, 250, 'OPTIONAL BEDROOM 5', '12\'-3" × 8\'-6"')
    B.small(c, 455, 454, 'OPTIONAL CLOSET', size=3.6)


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
