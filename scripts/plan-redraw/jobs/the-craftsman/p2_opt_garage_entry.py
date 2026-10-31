"""The Craftsman - OPTIONAL GARAGE ENTRY THROUGH LAUNDRY (brochure page 2, image xref 14, 680x502 px at 681.9 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 2, 14
K, PXFT = 681.9, 46.2

DROP = [(200, 148, 378, 200)]


def labels(c):
    B.label(c, 289, 174, 'LAUNDRY', name_pt=5.6)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, after=labels, bands=False)
