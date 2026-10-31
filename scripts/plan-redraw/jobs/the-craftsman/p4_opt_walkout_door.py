"""The Craftsman - DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 4, image xref 24, 607x211 px at 706.0 dpi).
Option drawing: traced walls and linework, foundation band filled, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 4, 24
K, PXFT = 706.0, 46.2

DROP = [(186, 2, 420, 40)]


def labels(c):
    B.small(c, 303, 21, 'OPT. PATIO DOOR', size=3.8, color=B.OPT)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, after=labels)
