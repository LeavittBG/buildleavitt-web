"""The Innovator - FIRST FLOOR OPTIONS: STAIRS FOR OPTIONAL SECOND FLOOR (brochure page 3, image
xref 19, 713x376 px placed at 471.4 dpi, 46.1 px/ft). A straight flight: traced and re-lettered;
nothing to modernise."""
import blib as B
import bhelp

PAGE, XREF = 3, 19
K, PXFT = 471.4, 46.1
DROP = [(10, 158, 66, 204), (603, 140, 664, 188)]


def labels(c):
    B.small(c, 38, 181, 'UP', size=4.2)
    B.small(c, 633, 163, 'DN', size=4.2)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, auto_text=False, drop=DROP, after=labels)
