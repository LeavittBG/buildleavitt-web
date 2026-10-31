"""The Illustrator - SECOND FLOOR OPTIONS, "OPTIONAL LOFT" (page 5, xref 27), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Traced and re-lettered; no modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 5, 27
B.K, B.PXFT = 444.6, 32.3
TEXT = [(205, 236, 462, 332)]
WIN_DROP = []

def after(c):
    bhelp.vlabel(c, 333, 284, 'OPTIONAL LOFT', '12\'-3" × 10\'-10"')


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=None, drop=TEXT + [], win_drop=WIN_DROP,
                 auto_text=False)
