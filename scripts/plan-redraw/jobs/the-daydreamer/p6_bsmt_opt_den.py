"""The Daydreamer - BASEMENT OPTIONS: OPTIONAL DEN WITH OPTIONAL IN-LAW SUITE OR CONSERVATORY
ABOVE (page 6, xref 38; 389.4 dpi, 37.8 px/ft). Traced; concrete fill in the foundation band;
lettering re-set."""
import blib as B, bhelp

PAGE, XREF = 6, 38
B.K = 389.4
TEXT = [(395, 462, 644, 564)]


def after(c):
    bhelp.vlabel(c, 500, 514, 'OPT. DEN', '12\'-7" × 19\'-11"')


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT, after=after)
