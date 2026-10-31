"""The Draftsman - BASEMENT OPTIONS, "ELEVATION B" (page 6, xref 34), 420.9 dpi. Same treatment
as the basement: concrete band, traced walls and linework, equipment circles redrawn, lettering
re-set."""
import blib as B
import bhelp

PAGE, XREF = 6, 34
B.K, B.PXFT = 420.9, 38.0
CIRCLES = [(437, 163, 55), (731, 276, 40), (731, 359, 40), (416, 408, 32)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]
TEXT = [(1980, 46, 2122, 141), (942, 100, 1056, 195), (1644, 867, 2084, 916)]


def before(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    S = B.small
    B.label(c, 2051, 93, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    B.label(c, 999, 147, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 437, 153, 'SPRINKLER', size=3.0)
    S(c, 437, 174, 'TANK', size=3.0)
    S(c, 731, 276, 'WH', size=3.2)
    S(c, 731, 359, 'WT', size=3.2)
    S(c, 416, 408, 'SUMP', size=3.0)
    S(c, 1863, 891, 'OPTIONAL 3-CAR GARAGE ABOVE', size=3.6, color=B.OPT)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT + CIRC_DROP, band_drop=TEXT + CIRC_DROP, before=before, after=after)
