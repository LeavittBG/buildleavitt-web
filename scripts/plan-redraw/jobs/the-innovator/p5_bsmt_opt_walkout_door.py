"""The Innovator - BASEMENT OPTIONS: DOOR WITH OPTIONAL WALKOUT CONDITION (brochure page 5,
image xref 25, 605x209 px placed at 711.8 dpi, 46.2 px/ft).

Nearly The Craftsman's picture (jobs/the-craftsman/p4_opt_walkout_door.py) but its left wall runs
straight instead of turning a corner, so it has its own job in the same form: traced walls and
linework, foundation band filled (not under the label), lettering re-set. Nothing to modernise.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 25
K, PXFT = 711.8, 46.2
DROP = [(186, 2, 420, 40)]


def labels(c):
    B.small(c, 303, 21, 'OPT. PATIO DOOR', size=3.8, color=B.OPT)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.vignette(c, img, drop=DROP, band_drop=[(140, 0, 470, 62)], after=labels)
