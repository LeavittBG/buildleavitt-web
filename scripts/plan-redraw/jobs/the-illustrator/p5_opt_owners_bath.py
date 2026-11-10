"""The Illustrator - SECOND FLOOR OPTIONS, "OPTIONAL OWNER'S BATH" (page 5, xref 30), redrawn clean.
Placed at 444.6 dpi; drawn at the second floor's 32.3 px/ft (its windows measure 98 px, as there).
Changed (Kyle, October 31, 2026): the angled corner soaker tub on its deck becomes a walk-in
shower in the same space (glass along the deck's angle, open on the right, linear drain, bench); a
wall separates it from the old shower stall, so the stall becomes a towel closet behind its door."""
import blib as B
import bhelp

PAGE, XREF = 5, 30
B.K, B.PXFT = 444.6, 32.3
TEXT = [(291, 154, 454, 296)]
WIN_DROP = []

# old tub and deck; inside of the old shower stall (its outline and door stay)
TUB = [(98, 230, 322, 434)]
STALL = [(106, 26, 202, 169)]


def before(c):
    k = B.PXFT / 12.0
    pts = [(97, 229), (212, 229), (320, 337), (320, 435), (97, 435)]
    c.polyline(pts, w=0.45, color=B.NAVY, close=True, fill='#ffffff')
    c.line(212, 229, 320, 337, 0.9, color=B.NAVY)                 # glass along the angle
    c.rect(97 + 4 * k, 260, 1.6 * k, 160, sw=0.3, color=B.NAVY)   # linear drain
    c.rect(97, 435 - 15 * k, 160, 15 * k, sw=0.4, color=B.NAVY)   # bench
    B.small(c, 190, 360, 'SHOWER', size=3.8)
    B.small(c, 177, 435 - 7.5 * k, 'BENCH', size=3.0, color=B.GREY)


def after(c):
    bhelp.vlabel(c, 373, 225, "OPTIONAL\nOWNER'S\nBATH")
    B.small(c, 154, 88, 'TOWEL', size=3.6)
    B.small(c, 154, 112, 'CLOSET', size=3.6)


def draw(c, img):
    bhelp.simple(c, img, 444.6, after=after, before=before, drop=TEXT + TUB + STALL, win_drop=WIN_DROP,
                 auto_text=False)
