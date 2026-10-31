"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL ENTRY FROM GARAGE HALL" (page 3, xref 19).
Placed at 490 dpi. Linework only (no lettering); traced clean, nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 19
B.K, B.PXFT = 490.0, 38.0


def draw(c, img):
    bhelp.simple(c, img, 490.0, auto_text=False, win_drop=[(40, 90, 90, 260)])
