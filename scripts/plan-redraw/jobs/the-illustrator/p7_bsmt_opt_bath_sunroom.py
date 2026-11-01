"""The Illustrator - BASEMENT OPTIONS, "OPTIONAL BATH LOCATION WITH OPTIONAL SUNROOM ABOVE"
(page 7, xref 41), redrawn clean. Placed at 370.4 dpi, 32.3 px/ft like the basement. Traced
walls, doors and fixtures; the ejector-pit circle redrawn; lettering re-set. The optional bath
keeps its tub/shower and its vanity."""
import blib as B
import bhelp

PAGE, XREF = 7, 41
B.K, B.PXFT = 370.4, 32.3
TEXT = [(256, 236, 352, 325), (413, 171, 521, 264), (125, 438, 383, 470), (171, 510, 425, 553)]
PIT = (431, 102, 32)


def before(c):
    x, y, r = PIT
    c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    bhelp.vlabel(c, 304, 281, 'OPT.\nBATH')
    bhelp.vlabel(c, 467, 218, 'OPT.\nMECH.')
    B.small(c, 254, 454, '3 PIECE ROUGH-IN STD.', size=3.6)
    bhelp.vlabel(c, 298, 531, 'OPT. REC ROOM')
    B.small(c, 431, 93, 'EJEC.', size=2.8)
    B.small(c, 431, 112, 'PIT', size=2.8)


def draw(c, img):
    x, y, r = PIT
    bhelp.simple(c, img, 370.4, before=before, after=after,
                 drop=TEXT + [(x - r - 5, y - r - 5, x + r + 5, y + r + 5)], auto_text=False,
                 win_drop=[(95, 385, 225, 425)])     # an L of wall the window finder misreads
