"""The Pioneer II - BASEMENT OPTIONS: EXTENDED REC ROOM AND MEDIA ROOM WITH OPTIONAL 2'-0" REAR
EXTENSION ABOVE (page 6, image xref 34, 2303x565 px, 438 dpi). The Pioneer II has no 4'-0" family
room extension, so the rec-room bay is 152 px shorter; below it the picture is The Pioneer I's
matching vignette moved up 152 px (measured, identical), so this is that job with its lower items
moved: traced walls and linework, concrete foundation bands, tub (kept) and ejector pit redrawn,
lettering re-set."""
import blib as B
import bhelp

PAGE, XREF = 6, 34
DY = -152
TEXT = [(650, 515 + DY, 925, 585 + DY), (1445, 615 + DY, 1565, 565), (1770, 555 + DY, 2090, 665 + DY)]
ITEMS = [(1360, 513 + DY, 1555, 615 + DY), (1276, 530 + DY, 1348, 602 + DY)]
BATH = [(1360, 506 + DY, 1555, 565), (1276, 530 + DY, 1348, 602 + DY),
        (560, 80, 672, 130), (920, 80, 1022, 130), (145, 460 + DY, 322, 510 + DY)]   # windows stay white


def before(c):
    B.tub(c, 1363, 509 + DY, 1552, 611 + DY)
    c.circle(1312, 566 + DY, 29, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    B.label(c, 787, 550 + DY, 'OPT. REC ROOM')
    B.label(c, 1930, 612 + DY, 'OPT. MEDIA ROOM', '18\'-1" × 14\'-7"')
    B.label(c, 1502, 668 + DY, 'OPT.\nBATH', name_pt=4.8)
    B.small(c, 1312, 558 + DY, 'EJEC.', size=2.7)
    B.small(c, 1312, 575 + DY, 'PIT', size=2.7)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT + ITEMS, band_drop=BATH, before=before, after=after)
