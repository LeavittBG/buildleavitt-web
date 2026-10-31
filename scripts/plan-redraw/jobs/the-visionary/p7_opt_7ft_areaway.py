"""The Visionary - BASEMENT OPTIONS: OPTIONAL 7' AREAWAY (brochure page 7, image xref 40, 478 dpi).
Walls, windows and linework traced, foundation band filled concrete as on the basement plan;
lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 7, 40
DROP = [(210, 243, 245, 289), (297, 622, 523, 674)]


def before(c):
    c.line(178, 261, 307, 261, 0.75, color=B.NAVY)      # tread under the old lettering


def after(c):
    L, S, o = bhelp.vlabel, B.small, B.OPT
    S(c, 228, 241, 'UP', size=3.6, rotate=-90)
    S(c, 410, 648, 'OPT. PATIO DOOR', size=3.6, color=o)


def draw(c, img):
    B.K = c.K = 478.0
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP, before=before, after=after)   # with the concrete foundation band
