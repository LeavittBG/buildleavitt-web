"""The Maestro - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 5 (brochure page 3, image xref 23,
1056x765 px placed at 945.8 dpi, 46.1 px/ft). Walls, windows and linework traced; lettering
re-set, bedroom name centred. The optional bath keeps its tub/shower and vanity (secondary bath).
At the right edge the drawing shows part of the owner's bath; its old shower stall is drawn as the
towel closet it became on the second floor (shower lines erased, shelf line added)."""
import blib as B
import bhelp

PAGE, XREF = 3, 23
K, PXFT = 945.8, 46.1
DROP = [(210, 322, 619, 425), (721, 250, 822, 353), (725, 519, 865, 619)]
OLD_STALL = [(960, 385, 1056, 555)]


def before(c):
    k = B.PXFT / 12.0
    c.rect(960, 385, 96, 170, sw=0, fill='#ffffff')
    c.line(958 + 16 * k, 385, 958 + 16 * k, 555, 0.45, color=B.NAVY, dash=c.dash(2.5, 1.6))


def after(c):
    L = bhelp.vlabel
    L(c, 409, 385, 'OPTIONAL BEDROOM 5', '12\'-2" × 11\'-3"', name_pt=3.9, sub_pt=3.4)
    L(c, 770, 302, 'OPT.\nBATH', name_pt=3.3)
    L(c, 795, 569, 'OPT.\nCLOSET', name_pt=3.3)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, before=before, drop=DROP + OLD_STALL, auto_text=False)
