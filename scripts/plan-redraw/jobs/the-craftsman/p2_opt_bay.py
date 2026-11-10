"""The Craftsman - OPTIONAL BAY (brochure page 2, image xref 15, 629x138 px at 682 dpi).
Option drawing: traced walls and linework, lettering re-set. No modernising needed.
The two windows in the angled sides are set by hand: the window finder only catches their ends."""
import blib as B
import bhelp

PAGE, XREF = 2, 15
K, PXFT = 682.0, 46.2
ANGLED = [((110.0, 68.0), 72.0, 20.0, -45.0), ((520.0, 68.0), 73.0, 20.0, 45.0)]


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    walls, wins = B.trace(img, win_drop=[(70, 40, 150, 110), (470, 30, 550, 100)])
    nv, gr = B.lineart(img, walls)
    B.draw_geom(c, bhelp.thin_lines(img, walls), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_plan_walls(c, walls, list(wins) + ANGLED)
