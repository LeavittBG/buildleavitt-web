"""The Pioneer I - BASEMENT OPTIONS: OPTIONAL DEN WITH OPTIONAL MORNING ROOM ABOVE
(brochure page 6, image xref 30, 1310x912 px, 438 dpi). Same treatment as p1_bsmt.py: traced walls
and linework, concrete fill in the foundation band, bath fixtures redrawn (tub kept), lettering
re-set in Roboto Condensed."""
import sys
import blib as B, bhelp

PAGE, XREF = 6, 30
IMG = None   # set by draw()
TEXT = [(630, 225, 900, 330), (780, 700, 1090, 805), (283, 650, 375, 745), (122, 825, 380, 860)]
ITEMS = [(188, 506, 382, 618), (188, 640, 285, 700), (188, 712, 255, 815), (100, 528, 176, 606)]
BATH = [(188, 506, 382, 815), (95, 515, 182, 612), (95, 462, 205, 497)]


def before(c):
    B.tub(c, 191, 509, 379, 613)
    B.toilet(c, 191, 663, 'right')
    B.vanity(c, 191, 763, 'right', 30, 19)
    c.circle(137, 566, 30, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    B.label(c, 785, 277, 'OPT. DEN', '28\'-4" × 11\'-8"')
    B.label(c, 935, 752, 'OPT. MEDIA ROOM', '18\'-1" × 12\'-7"')
    B.label(c, 328, 697, 'OPT.\nBATH', name_pt=4.8)
    B.small(c, 252, 842, '3 PIECE ROUGH-IN STD.', size=3.6)
    B.small(c, 137, 558, 'EJEC.', size=2.7)
    B.small(c, 137, 575, 'PIT', size=2.7)


def _draw(c):
    bhelp.vignette(c, IMG, drop=TEXT + ITEMS, band_drop=BATH, before=before, after=after)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
