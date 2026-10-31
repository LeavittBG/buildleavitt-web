"""The Craftsman - OPTIONAL BAY (brochure page 2, image xref 15, 629x138 px at 682.0 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 2, 15
K, PXFT = 682.0, 46.2


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, bands=False)
