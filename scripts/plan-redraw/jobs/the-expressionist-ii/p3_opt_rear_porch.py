"""The Expressionist II - FIRST FLOOR OPTIONS: OPTIONAL REAR PORCH (brochure page 3, image xref 23), redrawn clean.

370.4 dpi, 29.6 px/ft like the rest of this brochure. Traced and re-lettered only.
Labels stay where they were printed: the drawing shows only part of the house.
"""
import blib as B
import bhelp

PAGE, XREF = 3, 23
K, PXFT = 370.4, 29.6
DROP = [(78, 156, 236, 187), (794, 156, 952, 187), (488, 222, 566, 260), (128, 255, 350, 340), (700, 265, 945, 350)]


def after(c):
    o = B.OPT
    B.small(c, 156, 172, 'OPT. PATIO DOOR', size=3.4, color=o)
    B.small(c, 872, 172, 'OPT. PATIO DOOR', size=3.4, color=o)
    bhelp.vlabel(c, 527, 241, 'BATH', None, name_pt=4.8)
    bhelp.vlabel(c, 230, 297, 'STUDY', '13\'-2" × 13\'-6"')
    bhelp.vlabel(c, 842, 307, 'BEDROOM 1', '14\'-2" × 17\'-10"')


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
