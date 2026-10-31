"""The Novel - BASEMENT OPTIONS, "EXTENDED REC ROOM WITH OPTIONAL SUNROOM ABOVE" (page 6, xref 31).
Placed at 412.4 dpi, 37.95 px/ft. Foundation walls traced with the light concrete fill used on the
basement; lettering re-set as printed. No modernising needed."""
import blib as B
import bhelp

PAGE, XREF = 6, 31
B.K, B.PXFT = 412.4, 37.95
TEXT = [(82, 360, 345, 412), (575, 518, 900, 626)]


def after(c):
    bhelp.vlabel(c, 213, 387, 'OPT. REC ROOM')
    bhelp.vlabel(c, 742, 572, 'OPT. MEDIA ROOM', '21\'-8" × 13\'-5"')


def draw(c, img):
    B.K = c.K = 412.4
    bhelp.vignette(c, img, drop=TEXT, band_drop=TEXT, after=after)
