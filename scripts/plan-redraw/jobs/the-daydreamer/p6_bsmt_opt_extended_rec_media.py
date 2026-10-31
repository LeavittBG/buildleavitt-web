"""The Daydreamer - BASEMENT OPTIONS: EXTENDED REC ROOM AND MEDIA ROOM WITH OPTIONAL KITCHEN/FAMILY
ROOM EXTENSION ABOVE (page 6, xref 37; 389.5 dpi, 37.8 px/ft). Traced; concrete fill in the
foundation band; ejector pit and lettering redrawn. The optional bath keeps its fixtures."""
import blib as B, bhelp

PAGE, XREF = 6, 37
B.K = 389.5
TEXT = [(258, 226, 514, 272), (1283, 149, 1574, 241), (978, 79, 1045, 156)]
PIT = (802, 249, 32)


def before(c):
    x, y, r = PIT
    c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    x, y, r = PIT
    bhelp.vlabel(c, 386, 249, 'OPT. REC ROOM')
    bhelp.vlabel(c, 1428, 195, 'OPT. MEDIA ROOM', '18\'-1" × 18\'-3"')
    B.small(c, 1012, 117, 'OPT. CLOSET', size=3.2, rotate=-90)
    B.small(c, x, y - 8, 'EJEC.', size=2.7)
    B.small(c, x, y + 9, 'PIT', size=2.7)


def draw(c, img):
    x, y, r = PIT
    bhelp.vignette(c, img, drop=TEXT + [(x - r - 5, y - r - 5, x + r + 5, y + r + 5)],
                   band_drop=TEXT, before=before, after=after)
