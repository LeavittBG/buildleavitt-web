"""The Romantic - FIRST FLOOR OPTIONS: OPTIONAL BAY (brochure page 3, image xref 20), redrawn clean.

Source raster 627x137 px placed at 370.6 dpi, 46.2 px/ft. Traced; the two windows in the bay's
angled sides are set by hand (the tracer finds only their jambs). No lettering in the drawing.
"""
import math
import blib as B
import bhelp

PAGE, XREF = 3, 20
K, PXFT = 370.6, 46.2
SIDES = [((83, 43), (133, 93), 45), ((490, 93), (543, 41), -45)]


def windows(c):
    for (x0, y0), (x1, y1), ang in SIDES:
        B.window_rot(c, ((x0 + x1) / 2, (y0 + y1) / 2), math.hypot(x1 - x0, y1 - y0) - 8, 21, ang)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.simple(c, img, K, auto_text=False, after=windows)
