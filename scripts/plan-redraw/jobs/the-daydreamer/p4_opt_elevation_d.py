"""The Daydreamer - SECOND FLOOR OPTIONS: ELEVATION D (page 4, xref 27; 735 dpi, 37.8 px/ft).
The front wall's windows with Elevation D. Traced only; it has no lettering."""
import blib as B, bhelp

PAGE, XREF = 4, 27
B.K = 735.3


def draw(c, img):
    bhelp.simple(c, img, 735.3, auto_text=False)
