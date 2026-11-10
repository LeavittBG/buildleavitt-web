"""The Illustrator - SECOND FLOOR OPTIONS, "ELEVATION B" (page 5, xref 29), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered (labels where printed); no modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 5, 29
B.K, B.PXFT = 444.6, 32.3
TEXT = [(616, 0, 841, 94), (134, 23, 406, 119), (1049, 23, 1321, 119)]
WIN_DROP = []

def after(c):
    bhelp.vlabel(c, 728, 47, 'OPEN TO\nFOYER BELOW')
    bhelp.vlabel(c, 270, 71, 'BEDROOM 3', '12\'-10" × 12\'-10"')
    bhelp.vlabel(c, 1185, 71, 'BEDROOM 2', '12\'-10" × 15\'-10"')


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
