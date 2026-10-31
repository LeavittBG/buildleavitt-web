"""The Innovator - FIRST FLOOR OPTIONS: ELEVATION C (brochure page 3, image xref 18, 2406x574 px
placed at 471.3 dpi, 46.1 px/ft). Traced and re-lettered as printed; nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 18
K, PXFT = 471.3, 46.1
DROP = [(95, 2, 505, 172), (1025, 55, 1325, 172), (595, 245, 875, 305), (1735, 345, 2115, 465)]


def labels(c):
    V, S = bhelp.vlabel, B.small
    V(c, 300, 88, 'STUDY OR OPTIONAL\nBEDROOM 3', '11\'-5" × 15\'-8"', name_pt=5.8, sub_pt=4.8)
    V(c, 1178, 115, 'BEDROOM 2', '11\'-5" × 15\'-8"', name_pt=5.8, sub_pt=4.8)
    V(c, 735, 276, 'CONC. PORCH', name_pt=5.2)
    V(c, 1925, 405, 'TWO-CAR GARAGE', '19\'-7" × 21\'-1"', name_pt=5.8, sub_pt=4.8)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, auto_text=False, drop=DROP, after=labels)
