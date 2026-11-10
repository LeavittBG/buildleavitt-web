"""The Pioneer I - BASEMENT OPTIONS: EXTENDED REC ROOM AND MEDIA ROOM WITH OPTIONAL 2'-0" REAR
EXTENSION AND 4'-0" FAMILY ROOM EXTENSION ABOVE (brochure page 6, image xref 33, 2303x717 px,
438 dpi). Traced walls and linework, concrete foundation bands, tub (kept) and ejector pit
redrawn, lettering re-set in Roboto Condensed."""
import sys
import blib as B, bhelp

PAGE, XREF = 6, 33
IMG = None   # set by draw()
TEXT = [(650, 515, 925, 585), (1445, 615, 1565, 717), (1770, 555, 2090, 665)]
ITEMS = [(1360, 513, 1555, 615), (1276, 530, 1348, 602)]
BATH = [(1360, 506, 1555, 717), (1276, 530, 1348, 602),
        (560, 80, 672, 130), (920, 80, 1022, 130), (145, 460, 322, 510)]   # windows stay white


def before(c):
    B.tub(c, 1363, 509, 1552, 611)
    c.circle(1312, 566, 29, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    B.label(c, 787, 550, 'OPT. REC ROOM')
    B.label(c, 1930, 612, 'OPT. MEDIA ROOM', '18\'-1" × 14\'-7"')
    B.label(c, 1502, 668, 'OPT.\nBATH', name_pt=4.8)
    B.small(c, 1312, 558, 'EJEC.', size=2.7)
    B.small(c, 1312, 575, 'PIT', size=2.7)


def _draw(c):
    bhelp.vignette(c, IMG, drop=TEXT + ITEMS, band_drop=BATH, before=before, after=after)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
