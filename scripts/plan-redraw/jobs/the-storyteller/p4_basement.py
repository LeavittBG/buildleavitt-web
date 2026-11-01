"""The Storyteller - BASEMENT (brochure page 4, image xref 14), redrawn clean.

Listing-sheet source like the first floor (see p2_first_floor.py); 346.7 dpi, 37.6 px/ft. Restyle
only: one open basement with a straight stair. The basement walls are drawn as the listing sheet
draws them (one solid band), not with the concrete fill used on the CAD brochures, because the
source does not separate foundation from framing.
"""
import blib as B
import bhelp as H

PAGE, XREF = 4, 14
K, PXFT = 346.7, 37.6

TEXT = [(1180, 830, 1350, 910)]


def draw(c, img):
    B.K, B.PXFT, c.K = K, PXFT, K
    clean = H.listing_erase_text(img, TEXT)
    walls, wins = H.listing_trace(clean)
    B.draw_geom(c, H.listing_lines(clean, walls), B.NAVY)
    B.draw_plan_walls(c, walls, wins)
    B.label(c, 1265, 870, 'BASEMENT', '63\'-6" × 42\'-7"')
