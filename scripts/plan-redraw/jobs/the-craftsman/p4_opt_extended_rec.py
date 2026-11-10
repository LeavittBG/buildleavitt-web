"""The Craftsman - EXTENDED REC ROOM WITH OPTIONAL SUNROOM ABOVE (brochure page 4, image xref 26, 2322x582 px at 706.0 dpi).
Option drawing: traced walls and linework, foundation band filled, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 4, 26
K, PXFT = 706.0, 46.2


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img)
