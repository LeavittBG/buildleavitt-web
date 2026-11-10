"""The Maestro - FIRST FLOOR OPTIONS: OPTIONAL BAY (brochure page 2, image xref 17,
627x136 px placed at 658.2 dpi). Walls and windows traced; no lettering, nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 2, 17
K, PXFT = 658.2, 46.1


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, auto_text=False)
