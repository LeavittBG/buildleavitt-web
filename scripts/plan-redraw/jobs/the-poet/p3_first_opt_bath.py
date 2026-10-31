"""The Poet - FIRST FLOOR OPTIONS: OPTIONAL BATH off the office (image xref 19).
Traced walls, tub/shower, toilet and vanity (a secondary bath keeps its tub; the sink is already
in a vanity); lettering re-set."""
import blib as B, bhelp

PAGE, XREF = 3, 19
B.K, B.PXFT = 421.7, 38.0
TEXT = [(126, 0, 248, 46), (74, 48, 300, 94), (237, 190, 418, 235)]


def after(c):
    B.label(c, 187, 45, 'OFFICE', '13\'-8" × 18\'-8"', name_pt=5.6)
    B.label(c, 327, 212, 'OPT. BATH', name_pt=5.0)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, bands=False, after=after)
