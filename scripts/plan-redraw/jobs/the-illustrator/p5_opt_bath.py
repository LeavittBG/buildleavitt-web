"""The Illustrator - SECOND FLOOR OPTIONS, "OPTIONAL BATH" (page 5, xref 33), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered; the optional bath keeps its tub/shower and vanity."""
import blib as B
import bhelp

PAGE, XREF = 5, 33
B.K, B.PXFT = 444.6, 32.3
TEXT = [(282, 214, 380, 310), (7, 376, 256, 470)]
WIN_DROP = []

def after(c):
    bhelp.vlabel(c, 331, 262, 'OPT.\nBATH')
    bhelp.vlabel(c, 131, 423, 'BEDROOM 2', '12\'-10" × 14\'-10"')


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
