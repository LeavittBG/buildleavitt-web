"""The Novel - SECOND FLOOR OPTIONS, "OPTIONAL BATH" (page 4, xref 26), redrawn clean.
Placed at 688.2 dpi, drawing at 37.95 px/ft (stair treads 31.6 px apart, as on the main plan).
The optional bath keeps its tub (secondary bath). The strip of stair along the top shows the start's
flared stringer; it is straightened to match the squared stair on the second floor. Lettering
re-set as printed."""
import blib as B
import bhelp

PAGE, XREF = 4, 26
B.K, B.PXFT = 688.2, 37.95
TEXT = [(185, 132, 322, 182), (640, 256, 740, 350), (232, 336, 488, 432), (855, 452, 1000, 648)]
STAIR_CURVE = [(0, 76, 96, 112)]
WIN_DROP = [(400, 50, 430, 100), (0, 520, 40, 560)]


def before(c):
    c.rect(0, 85, 100, 14, sw=0, fill=B.NAVY)
    c.line(0, 92, 100, 92, 0.35, color='#ffffff')


def after(c):
    # this vignette prints the plan at 0.6x the main plan's size: lettering set smaller to match
    B.small(c, 254, 158, 'CLOSET', size=3.0)
    bhelp.vlabel(c, 690, 303, 'OPT.\nBATH', name_pt=3.4)
    bhelp.vlabel(c, 348, 385, 'BEDROOM 2', '13\'-0" × 15\'-6"', name_pt=3.8, sub_pt=3.2)
    for i, s in enumerate(('SITTING', 'ROOM')):
        B.small(c, 930, 470 + i * 34, s, size=3.4, weight=700)
    for i, s in enumerate(('10\'-1" ×', '10\'-4"')):
        B.small(c, 930, 548 + i * 32, s, size=3.0, color=B.GREY)


def draw(c, img):
    bhelp.simple(c, img, 688.2, before=before, after=after, drop=TEXT + STAIR_CURVE, win_drop=WIN_DROP,
                 auto_text=False)
