"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL OWNER'S BATH FIREPLACE" (page 3, xref 25).
Placed at 490 dpi. Linework only; traced clean, nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 25
B.K, B.PXFT = 490.0, 38.0


def draw(c, img):
    bhelp.simple(c, img, 490.0, auto_text=False)
