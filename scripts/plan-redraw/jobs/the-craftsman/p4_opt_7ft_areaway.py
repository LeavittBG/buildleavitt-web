"""The Craftsman - OPTIONAL 7' AREAWAY (brochure page 4, image xref 25, 635x851 px at 705.6 dpi).
Option drawing: traced walls and linework, foundation band filled, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 4, 25
K, PXFT = 705.6, 46.2

DROP = [(254, 296, 300, 352), (368, 768, 634, 820)]
STAIR = [(100, 10, 500, 700)]


def labels(c):
    B.small(c, 277, 324, 'UP', size=4.4, rotate=-90)
    B.small(c, 501, 793, 'OPT. PATIO DOOR', size=3.8, color=B.OPT)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, band_drop=STAIR, after=labels)
