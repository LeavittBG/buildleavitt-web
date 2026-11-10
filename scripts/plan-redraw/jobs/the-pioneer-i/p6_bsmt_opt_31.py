"""The Pioneer I - BASEMENT OPTIONS: OPTIONAL OFFICE WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY
ABOVE (brochure page 6, image xref 31, 969x1049 px, 438 dpi). Traced walls and linework, concrete
fill in the foundation bands, lettering re-set in Roboto Condensed."""
import sys
import blib as B, bhelp

PAGE, XREF = 6, 31
IMG = None   # set by draw()
TEXT = [(415, 460, 680, 565)]


def after(c):
    B.label(c, 547, 512, 'OPT. OFFICE', '12\'-7" × 19\'-11"')


def _draw(c):
    bhelp.vignette(c, IMG, drop=TEXT, after=after, add=[(889, 974, 904, 1001), (889, 986, 930, 1001)])


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
