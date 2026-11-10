"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL ENTRY FROM GARAGE THROUGH LAUNDRY (page 3,
xref 20; 482 dpi, 37.8 px/ft). Traced; the powder room's pedestal sink becomes a vanity, as on the
first floor (Kyle, October 31, 2026); lettering re-set."""
import blib as B, bhelp

PAGE, XREF = 3, 20
B.K = 482.0
SKIP = [(240, 320, 280, 350)]                 # washer handle
SINK = [(0, 180, 96, 246)]
TEXT = [(0, 246, 95, 322), (128, 240, 280, 284)]


def before(c):
    B.vanity(c, 47, 178, 'down', 24, 18)


def after(c):
    bhelp.vlabel(c, 47, 282, 'PDR.\nROOM', name_pt=4.6)
    bhelp.vlabel(c, 204, 262, 'LAUNDRY')


def draw(c, img):
    bhelp.simple(c, img, 482.0, before=before, after=after, drop=SINK + TEXT, auto_text=False)
