"""The Craftsman - OPTIONAL SUNROOM (brochure page 2, image xref 13, 1131x723 px at 682.0 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 2, 13
K, PXFT = 682.0, 46.2

DROP = [(380, 166, 559, 218), (339, 225, 595, 277), (641, 155, 677, 380), (1038, 128, 1076, 362),
        (407, 613, 572, 664), (340, 671, 635, 723), (726, 552, 949, 604), (784, 610, 892, 661)]


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
