"""The Draftsman - BASEMENT OPTIONS, "OPTIONAL MEDIA ROOM WITH OPTIONAL IN-LAW SUITE OR SUNROOM
ABOVE" (page 6, xref 35), 420.9 dpi. Same treatment as the basement: concrete band, traced
walls and linework, lettering re-set."""
import blib as B
import bhelp

PAGE, XREF = 6, 35
B.K, B.PXFT = 420.9, 38.0
TEXT = [(404, 490, 704, 588)]


def after(c):
    B.label(c, 554, 539, 'OPT. MEDIA ROOM', '20\'-9" × 11\'-11"')


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT, after=after)
