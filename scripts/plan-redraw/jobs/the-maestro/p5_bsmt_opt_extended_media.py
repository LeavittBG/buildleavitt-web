"""The Maestro - BASEMENT OPTIONS: EXTENDED MEDIA ROOM WITH OPTIONAL MORNING ROOM ABOVE (brochure
page 5, image xref 27, 717x788 px placed at 446.5 dpi, 46.1 px/ft). Walls traced, the foundation
band gets the light concrete fill used on the basement, lettering re-set and centred."""
import blib as B
import bhelp

PAGE, XREF = 5, 27
K, PXFT = 446.5, 46.1
DROP = [(239, 367, 580, 467)]
ROOM = [(152, 58, 656, 788)]


def after(c):
    B.label(c, 404, 420, 'OPT. MEDIA ROOM', '11\'-5" × 34\'-9"')


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    bhelp.vignette(c, img, drop=DROP, band_drop=ROOM, after=after)
