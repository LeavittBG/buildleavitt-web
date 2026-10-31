"""The Craftsman - OPTIONAL SUNROOM (brochure page 2, image xref 13, 1131x723 px at 682.0 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 2, 13
K, PXFT = 682.0, 46.2

DROP = [(380, 166, 559, 218), (328, 222, 602, 280), (640, 112, 678, 398), (1038, 128, 1076, 362),
        (407, 613, 572, 664), (328, 668, 642, 723), (726, 552, 949, 604), (784, 610, 892, 661)]


def labels(c):
    # The cathedral ridge runs down the middle of the sunroom, so the name is centred in the
    # half to the left of it, as printed.
    B.label(c, 462, 240, 'SUNROOM', '15\'-6" × 9\'-8"')
    B.small(c, 660, 267, 'CATHEDRAL CEILING', size=3.8, color=B.OPT, rotate=-90)
    B.small(c, 1057, 245, 'OPT. PATIO DOOR', size=3.8, color=B.OPT, rotate=-90)
    B.label(c, 488, 668, 'KITCHEN', '19\'-10" × 13\'-10"')
    B.label(c, 837, 606, 'BREAKFAST\nNOOK')


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    bhelp.vignette(c, img, drop=DROP, after=labels, bands=False)
