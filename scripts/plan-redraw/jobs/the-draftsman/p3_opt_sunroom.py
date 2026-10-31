"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL SUNROOM" (page 3, xref 24), 490 dpi.
Traced clean and re-lettered; the kitchen corner it shows is unchanged on the first floor."""
import blib as B
import bhelp

PAGE, XREF = 3, 24
B.K, B.PXFT = 490.0, 38.0


def after(c):
    bhelp.vlabel(c, 529, 593, 'OPTIONAL SUNROOM', '21\'-8" × 13\'-1"')
    B.small(c, 517, 119, 'OPTIONAL GAS FIREPLACE', size=3.4)


def draw(c, img):
    bhelp.simple(c, img, 490.0, after=after, auto_text=False, win_drop=[(35, 0, 85, 45), (35, 245, 85, 295)], 
                 drop=[(378, 100, 656, 138), (370, 545, 688, 642)])
