"""The Daydreamer - BASEMENT OPTIONS: EXTENDED REC ROOM WITH OPTIONAL SUNROOM ABOVE (page 6,
xref 35; 389.3 dpi, 37.8 px/ft). Traced; concrete fill in the foundation band; the ejector pit
circle and all lettering redrawn. The bath fixtures at the edge are the optional bath's (kept)."""
import blib as B, bhelp

PAGE, XREF = 6, 35
B.K = 389.3
TEXT = [(198, 225, 454, 270)]
PIT = (388, 478, 32)


def before(c):
    x, y, r = PIT
    c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    x, y, r = PIT
    bhelp.vlabel(c, 326, 247, 'OPT. REC ROOM')
    B.small(c, x, y - 8, 'EJEC.', size=2.7)
    B.small(c, x, y + 9, 'PIT', size=2.7)


def draw(c, img):
    x, y, r = PIT
    bhelp.vignette(c, img, drop=TEXT + [(x - r - 5, y - r - 5, x + r + 5, y + r + 5)],
                   band_drop=TEXT, before=before, after=after)
