"""The Craftsman - WINDOW WITH ELEVATION B (brochure page 3, image xref 21, 465x227 px at 461.2 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 3, 21
K, PXFT = 461.2, 46.2

DROP = [(98, 145, 367, 184)]


def labels(c):
    B.small(c, 232, 165, 'WINDOW W/ ELEV. B', size=3.8, color=B.OPT)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, after=labels, bands=False)
