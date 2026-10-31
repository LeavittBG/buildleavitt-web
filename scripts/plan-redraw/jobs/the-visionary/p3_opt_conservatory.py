"""The Visionary - FIRST FLOOR OPTIONS: OPTIONAL CONSERVATORY (brochure page 3, image xref 23, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 3, 23
CATH = 504          # cathedral-ceiling line (measured)
DROP = [(94, 355, 150, 640), (340, 466, 705, 507), (295, 640, 755, 752)]


def after(c):
    B.small(c, 121, 497, 'OPTIONAL GAS FIREPLACE', size=3.6, rotate=-90)
    B.dashed(c, [(258, CATH), (788, CATH)], w=0.45)
    B.small(c, 522, CATH - 20, 'OPTIONAL CATHEDRAL CEILING', size=3.8, color=B.OPT)
    bhelp.vlabel(c, 522, 690, 'OPTIONAL\nCONSERVATORY', '13\'-6" × 21\'-1"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
