"""The Visionary - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 7, image xref 36, 478 dpi).
Walls, windows and linework traced, foundation band filled concrete as on the basement plan;
lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 7, 36
DROP = [(150, 0, 348, 36)]


def before(c):
    pass


def after(c):
    L, S, o = bhelp.vlabel, B.small, B.OPT
    S(c, 248, 17, 'OPT. PATIO DOOR', size=3.6, color=o)


def draw(c, img):
    B.K = c.K = 478.0
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after)   # with the concrete foundation band
