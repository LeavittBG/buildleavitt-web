"""The Illustrator - SECOND FLOOR OPTIONS, "ELEVATION D" (page 5, xref 32), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered (labels where printed); no modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 5, 32
B.K, B.PXFT = 444.6, 32.3
TEXT = [(134, 0, 400, 94), (616, 50, 841, 145), (1049, 74, 1321, 170)]
WIN_DROP = []

def after(c):
    bhelp.vlabel(c, 270, 47, 'BEDROOM 3', '12\'-10" × 11\'-10"')
    bhelp.vlabel(c, 728, 98, 'OPEN TO\nFOYER BELOW')
    bhelp.vlabel(c, 1185, 122, 'BEDROOM 2', '12\'-10" × 16\'-10"')


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
