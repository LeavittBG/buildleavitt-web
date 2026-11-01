"""The Novel - BASEMENT OPTIONS, "OPTIONAL DEN WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY ABOVE"
(page 6, xref 34). Placed at 412.4 dpi, 37.95 px/ft. Foundation walls traced with the light concrete
fill; lettering re-set as printed. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 6, 34
B.K, B.PXFT = 412.4, 37.95
TEXT = [(400, 465, 642, 562)]


def after(c):
    bhelp.vlabel(c, 515, 514, 'OPT. OFFICE', '12\'-7" × 19\'-11"')


def draw(c, img):
    B.K = c.K = 412.4
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT, after=after)
