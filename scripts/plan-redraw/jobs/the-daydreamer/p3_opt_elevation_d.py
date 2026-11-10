"""The Daydreamer - FIRST FLOOR OPTIONS: ELEVATION D (page 3, xref 19; 482 dpi, 37.8 px/ft).
The wider front porch with Elevation D. Traced and re-lettered only."""
import blib as B, bhelp

PAGE, XREF = 3, 19
B.K = 482.0
SKIP = [(840, 0, 900, 40)]                    # a door-jamb mark, not lettering
WIN_DROP = [(1280, 290, 1320, 350)]


def after(c):
    bhelp.vlabel(c, 707, 246, 'CONC. PORCH')


def draw(c, img):
    bhelp.simple(c, img, 482.0, after=after, drop=[(595, 222, 820, 270)], win_drop=WIN_DROP,
                 auto_text=False)
