"""The Visionary - BASEMENT OPTIONS: OPTIONAL DEN WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY ABOVE (brochure page 7, image xref 37, 478 dpi).
Walls, windows and linework traced, foundation band filled concrete as on the basement plan;
lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 7, 37
DROP = [(425, 466, 662, 562)]


def before(c):
    pass


def after(c):
    L, S, o = bhelp.vlabel, B.small, B.OPT
    L(c, 573, 505, 'OPT. DEN', '12\'-7" × 19\'-11"')


def draw(c, img):
    B.K = c.K = 478.0
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after)   # with the concrete foundation band
