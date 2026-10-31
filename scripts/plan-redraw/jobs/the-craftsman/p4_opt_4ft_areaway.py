"""The Craftsman - OPTIONAL 4' AREAWAY (brochure page 4, image xref 23, 606x852 px at 706.0 dpi).
Option drawing: traced walls and linework, foundation band filled, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 4, 23
K, PXFT = 706.0, 46.2

DROP = [(255, 296, 301, 352)]
STAIR = [(200, 20, 395, 700)]


def labels(c):
    B.small(c, 278, 324, 'UP', size=4.4, rotate=-90)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, band_drop=STAIR, after=labels)
