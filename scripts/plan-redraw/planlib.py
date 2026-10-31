"""planlib.py - drawing library for Leavitt Building Group bid-set floor plans.

Conventions
- Plans are drawn in MODEL INCHES: x to the right, y DOWN the sheet. Keep one origin per job
  (usually a corner of the main walls) so every level lines up.
- The sheet shrinks each plan by 1/K (K = model inches per paper inch; 48 = 1/4"=1'-0").
- Line weights, text sizes, ticks and arrowheads are PAPER sizes in points. c.pt(p) turns paper
  points into model inches, so "28 pt outside the wall" is written -c.pt(28) at any scale.
- ft(9, 5) = 113 inches. Dimension labels are always the WRITTEN strings from the layout.
- Fixtures take the point where their back meets the wall and the direction they face
  ('down', 'up', 'left', 'right') so tanks, faucets and appliance backs land on the wall.
- Loose furniture (beds, sofas, tables, stools) is drawn in light gray so it reads as reference;
  built-ins (counters, benches, lockers, vanities) are drawn in ink.
"""
import math
from shapely.geometry import box as _box, Polygon, LineString
from shapely.ops import unary_union

INK, NAVY, GOLD = '#161616', '#1C2B48', '#A9834A'
WALL_FILL, CONC_FILL, CONC_HATCH = '#3a3a3a', '#dcdcdc', '#8f8f8f'
LIGHT, WHITE = '#e9e9e9', '#ffffff'
FURN, FURN_TXT = '#8a8a8a', '#5a5a5a'
FONT = "'Roboto Condensed', 'Arial Narrow', sans-serif"


def ft(feet, inches=0.0):
    return feet * 12.0 + inches


def fmt_ftin(inches):
    """113.5 -> 9'-5½" (nearest 1/8"). The brand font only has ¼ ½ ¾ glyphs, so other
    fractions are written 1/8, 3/8 ... (type them the same way in labels)."""
    n = int(round(inches * 8))
    feet, r = divmod(n, 96)
    whole, eighth = divmod(r, 8)
    frac = ['', ' 1/8', '¼', ' 3/8', '½', ' 5/8', '¾', ' 7/8'][eighth]
    return f"{feet}'-{whole}{frac}\""


def f(v):
    return f"{v:.3f}".rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Canvas:
    """Collects the SVG for one plan (or the sheet, with K=1) and tracks its extents."""

    def __init__(self, K):
        self.K = K
        self.parts = []
        self._bb = [math.inf, math.inf, -math.inf, -math.inf]

    def pt(self, p):
        return p / 72.0 * self.K

    def dash(self, on, off):
        return f"{f(self.pt(on))},{f(self.pt(off))}"

    def add(self, s):
        self.parts.append(s)

    def svg(self):
        return "\n".join(self.parts)

    def grow(self, x, y):
        b = self._bb
        b[0], b[1], b[2], b[3] = min(b[0], x), min(b[1], y), max(b[2], x), max(b[3], y)

    def bounds(self):
        return tuple(self._bb)

    # ---------- primitives ----------
    def line(self, x1, y1, x2, y2, w=0.35, color=INK, dash=None, cap='butt'):
        self.grow(x1, y1); self.grow(x2, y2)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
                 f'stroke="{color}" stroke-width="{f(self.pt(w))}" stroke-linecap="{cap}"{d}/>')

    def polyline(self, pts, w=0.35, color=INK, dash=None, fill='none', close=False, join='miter'):
        for x, y in pts:
            self.grow(x, y)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        tag = 'polygon' if close else 'polyline'
        p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        self.add(f'<{tag} points="{p}" fill="{fill}" stroke="{color}" '
                 f'stroke-width="{f(self.pt(w))}" stroke-linejoin="{join}"{d}/>')

    def rect(self, x, y, w, h, sw=0.35, color=INK, fill='none', dash=None, rx=0):
        self.grow(x, y); self.grow(x + w, y + h)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        stroke = f'stroke="{color}" stroke-width="{f(self.pt(sw))}"' if sw else 'stroke="none"'
        r = f' rx="{f(rx)}"' if rx else ''
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{r} fill="{fill}" {stroke}{d}/>')

    def circle(self, cx, cy, r, sw=0.35, color=INK, fill='none'):
        self.grow(cx - r, cy - r); self.grow(cx + r, cy + r)
        self.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" '
                 f'stroke="{color}" stroke-width="{f(self.pt(sw))}"/>')

    def ellipse(self, cx, cy, rx, ry, sw=0.35, color=INK, fill='none'):
        self.grow(cx - rx, cy - ry); self.grow(cx + rx, cy + ry)
        self.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" '
                 f'stroke="{color}" stroke-width="{f(self.pt(sw))}"/>')

    def path(self, d, sw=0.35, color=INK, fill='none', dash=None, extra=''):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        stroke = f'stroke="{color}" stroke-width="{f(self.pt(sw))}"' if sw else 'stroke="none"'
        self.add(f'<path d="{d}" fill="{fill}" {stroke}{da} {extra}/>')

    def text(self, x, y, s, size=8, weight=400, anchor='middle', rotate=0, italic=False,
             color=INK, spacing=0, baseline='central', family=FONT, bg=None):
        """bg='#ffffff' paints a knockout behind the text (labels over tread or hatch lines)."""
        w = self.pt(size) * 0.5 * len(s) + self.pt(spacing) * len(s)
        h = self.pt(size)
        u0 = {'middle': -w / 2.0, 'start': 0.0, 'end': -w}[anchor]
        a = math.radians(rotate)
        ca, sa = math.cos(a), math.sin(a)
        corners = [(x + u * ca - v * sa, y + u * sa + v * ca)
                   for u, v in ((u0, -h / 2), (u0 + w, -h / 2), (u0, h / 2), (u0 + w, h / 2))]
        for px, py in corners:
            self.grow(px, py)
        if bg:
            pad = self.pt(1.5)
            xs, ys = [p[0] for p in corners], [p[1] for p in corners]
            self.rect(min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad,
                      sw=0, fill=bg)
        tr = f' transform="rotate({f(rotate)} {f(x)} {f(y)})"' if rotate else ''
        st = ' font-style="italic"' if italic else ''
        ls = f' letter-spacing="{f(self.pt(spacing))}"' if spacing else ''
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{f(self.pt(size))}" '
                 f'font-weight="{weight}" text-anchor="{anchor}" dominant-baseline="{baseline}" '
                 f'fill="{color}"{st}{ls}{tr}>{_esc(s)}</text>')

    def lines_text(self, x, y, lines, size=8, lead=1.18, **kw):
        """Several lines of text centred vertically on y."""
        h = self.pt(size) * lead
        y0 = y - h * (len(lines) - 1) / 2.0
        for i, s in enumerate(lines):
            self.text(x, y0 + i * h, s, size=size, **kw)

    def arc(self, cx, cy, r, a0, a1, sw=0.3, color=INK, dash=None, n=40):
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.polyline(pts, w=sw, color=color, dash=dash, join='round')


# ---------- walls ----------
def wall_geometry(walls, openings=()):
    """walls / openings: lists of (x0, y0, x1, y1) boxes. Returns the merged wall shape."""
    g = unary_union([_box(*w) for w in walls])
    if openings:
        g = g.difference(unary_union([_box(*o) for o in openings]))
    return g


def _poly_path(geom):
    polys = [geom] if isinstance(geom, Polygon) else [p for p in getattr(geom, 'geoms', [])
                                                       if isinstance(p, Polygon)]
    d = []
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = list(ring.coords)[:-1]
            d.append("M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z")
    return " ".join(d)


def _segments(geom):
    if geom.is_empty:
        return []
    if geom.geom_type == 'LineString':
        return [list(geom.coords)]
    if geom.geom_type in ('MultiLineString', 'GeometryCollection'):
        out = []
        for g in geom.geoms:
            out += _segments(g)
        return out
    return []


def hatch(c, geom, spacing_pt=4.5, color=CONC_HATCH, w=0.3):
    """45-degree hatch lines clipped to a shape."""
    x0, y0, x1, y1 = geom.bounds
    step = c.pt(spacing_pt) * math.sqrt(2)
    k = x0 - y1
    while k <= x1 - y0:
        ln = LineString([(y0 - 1 + k, y0 - 1), (y1 + 1 + k, y1 + 1)])
        for seg in _segments(ln.intersection(geom)):
            (ax, ay), (bx, by) = seg[0], seg[-1]
            c.line(ax, ay, bx, by, w, color=color)
        k += step


def draw_walls(c, geom, style='framed'):
    """style 'framed' = solid dark fill (new stud walls); 'concrete' = light gray with hatch
    (foundation walls); 'existing' = the same hatch, for walls of an existing house."""
    if geom.is_empty:
        return
    b = geom.bounds
    c.grow(b[0], b[1]); c.grow(b[2], b[3])
    d = _poly_path(geom)
    if style in ('concrete', 'existing'):
        c.path(d, sw=0, fill=CONC_FILL, extra='fill-rule="evenodd"')
        hatch(c, geom)
        c.path(d, sw=0.8, color=INK, fill='none', extra='stroke-linejoin="miter"')
    else:
        c.path(d, sw=0.7, color=INK, fill=WALL_FILL, extra='fill-rule="evenodd" stroke-linejoin="miter"')


# ---------- openings ----------
def window(c, orient, a, b, t0, t1, label=None, label_side=None, label_off=7, mull=None, size=6.8):
    """Window in a wall. orient 'h': wall runs along x (opening x a..b, wall faces y t0..t1);
    'v': wall runs along y (opening y a..b, wall faces x t0..t1). label_side 'out_neg' puts the
    label on the t0 side, anything else on the t1 side. mull = mullion positions."""
    lw, g = 0.35, 0.55
    mid = (t0 + t1) / 2.0
    if orient == 'h':
        c.line(a, t0, b, t0, lw); c.line(a, t1, b, t1, lw)
        c.line(a, t0, a, t1, lw); c.line(b, t0, b, t1, lw)
        c.line(a, mid - g, b, mid - g, 0.3); c.line(a, mid + g, b, mid + g, 0.3)
        for m in (mull or []):
            c.rect(m - 1.5, t0, 3, t1 - t0, sw=0.35, fill=WHITE)
        if label:
            y = (t0 - label_off) if label_side == 'out_neg' else (t1 + label_off)
            c.text((a + b) / 2.0, y, label, size=size, weight=500)
    else:
        c.line(t0, a, t0, b, lw); c.line(t1, a, t1, b, lw)
        c.line(t0, a, t1, a, lw); c.line(t0, b, t1, b, lw)
        c.line(mid - g, a, mid - g, b, 0.3); c.line(mid + g, a, mid + g, b, 0.3)
        for m in (mull or []):
            c.rect(t0, m - 1.5, t1 - t0, 3, sw=0.35, fill=WHITE)
        if label:
            x = (t0 - label_off) if label_side == 'out_neg' else (t1 + label_off)
            c.text(x, (a + b) / 2.0, label, size=size, weight=500, rotate=-90)


def swing_door(c, orient, a, b, face, hinge, sd, leaf_t=1.5):
    """Hinged door drawn open 90 degrees with its swing arc.
    orient 'h': wall along x, opening x a..b, swing-side wall face at y=face, sd=+1 swings to +y.
    orient 'v': wall along y, opening y a..b, swing-side face at x=face, sd=+1 swings to +x.
    hinge: 'a' or 'b' = which end of the opening the hinges are on."""
    w = b - a
    if orient == 'h':
        hx, ox = (a, b) if hinge == 'a' else (b, a)
        C, tip, closed = (hx, face), (hx, face + sd * w), (ox, face)
        lx = hx if hinge == 'a' else hx - leaf_t
        ly = face if sd > 0 else face - w
        c.rect(lx, ly, leaf_t, w, sw=0.55, fill=WHITE)
    else:
        hy, oy = (a, b) if hinge == 'a' else (b, a)
        C, tip, closed = (face, hy), (face + sd * w, hy), (face, oy)
        ly = hy if hinge == 'a' else hy - leaf_t
        lx = face if sd > 0 else face - w
        c.rect(lx, ly, w, leaf_t, sw=0.55, fill=WHITE)
    a0 = math.degrees(math.atan2(tip[1] - C[1], tip[0] - C[0]))
    a1 = math.degrees(math.atan2(closed[1] - C[1], closed[0] - C[0]))
    d = a1 - a0
    while d > 180:
        d -= 360
    while d < -180:
        d += 360
    c.arc(C[0], C[1], w, a0, a0 + d, sw=0.3)


def double_door(c, orient, a, b, face, sd):
    """Pair of doors hinged at both jambs, meeting in the middle."""
    m = (a + b) / 2.0
    swing_door(c, orient, a, m, face, 'a', sd)
    swing_door(c, orient, m, b, face, 'b', sd)


def bifold(c, a, b, face, sd, depth_ratio=0.38):
    """Bifold pair on a horizontal wall, opening x a..b at face y=face, folding toward sd."""
    m = (a + b) / 2.0
    for x0, x1 in ((a, m), (b, m)):
        dep = abs(x1 - x0) / 2.0 * depth_ratio
        c.polyline([(x0, face), (x0 + (x1 - x0) * 0.46, face + sd * dep), (x0 + (x1 - x0) * 0.92, face)], w=0.5)


def sliding_door(c, orient, a, b, t0, t1, panel=1.25):
    """Sliding glass door: two overlapping panels in the wall. Same arguments as window()."""
    m, mid, ov = (a + b) / 2.0, (t0 + t1) / 2.0, 1.5
    if orient == 'h':
        c.line(a, t0, a, t1, 0.45); c.line(b, t0, b, t1, 0.45)
        c.rect(a, mid - panel - 0.3, (m - a) + ov, panel, sw=0.45, fill=WHITE)
        c.rect(m - ov, mid + 0.3, (b - m) + ov, panel, sw=0.45, fill=WHITE)
    else:
        c.line(t0, a, t1, a, 0.45); c.line(t0, b, t1, b, 0.45)
        c.rect(mid - panel - 0.3, a, panel, (m - a) + ov, sw=0.45, fill=WHITE)
        c.rect(mid + 0.3, m - ov, panel, (b - m) + ov, sw=0.45, fill=WHITE)


def overhead_door(c, a, b, face, sd, wall_t, depth=84):
    """Overhead garage door on a horizontal wall. face = inside face y, sd = direction into the
    building (+1/-1), wall_t = wall thickness. Draws the panel and the open position (dashed)."""
    c.rect(a + 1, min(face + sd * 2, face + sd * (2 + depth)), b - a - 2, depth, sw=0.4, dash=c.dash(3.5, 2.5))
    c.rect(a, min(face, face + sd * 2.5), b - a, 2.5, sw=0.55, fill=WHITE)
    c.line(a, face, a, face - sd * wall_t, 0.35); c.line(b, face, b, face - sd * wall_t, 0.35)


def pocket_door(c, orient, a, b, t0, t1, pocket_end, leaf_t=1.5):
    """Pocket door, drawn closed. Same wall arguments as window(): opening a..b, wall faces t0..t1.
    pocket_end = far end of the pocket (below a or above b). Cut the wall opening from pocket_end
    through the far jamb first; this draws the wall skins along the pocket, the slot and the leaf."""
    skin = (t1 - t0 - leaf_t) / 2.0
    if pocket_end < a:
        lo, hi, leaf0, leaf1, jamb = pocket_end, a, a - 2, b, b
    else:
        lo, hi, leaf0, leaf1, jamb = b, pocket_end, a, b + 2, a
    if orient == 'h':
        for ys in (t0, t1 - skin):
            c.rect(lo, ys, hi - lo, skin, sw=0.5, fill=WALL_FILL)
        c.line(pocket_end, t0, pocket_end, t1, 0.5)
        c.rect(leaf0, t0 + skin, leaf1 - leaf0, leaf_t, sw=0.5, fill=WHITE)
        c.line(jamb, t0, jamb, t1, 0.35)
    else:
        for xs in (t0, t1 - skin):
            c.rect(xs, lo, skin, hi - lo, sw=0.5, fill=WALL_FILL)
        c.line(t0, pocket_end, t1, pocket_end, 0.5)
        c.rect(t0 + skin, leaf0, leaf_t, leaf1 - leaf0, sw=0.5, fill=WHITE)
        c.line(t0, jamb, t1, jamb, 0.35)


def cased_opening(c, orient, a, b, t0, t1):
    """Doorless opening or arch: dashed header lines across the cut (cut the wall first).
    Same wall arguments as window()."""
    d = c.dash(3, 2)
    if orient == 'h':
        c.line(a, t0, b, t0, 0.3, dash=d); c.line(a, t1, b, t1, 0.3, dash=d)
    else:
        c.line(t0, a, t0, b, 0.3, dash=d); c.line(t1, a, t1, b, 0.3, dash=d)


# ---------- dimensions & leaders ----------
def tick(c, x, y, size=None):
    s = size or c.pt(3.6)
    c.line(x - s / 2, y + s / 2, x + s / 2, y - s / 2, 0.8, cap='butt')


def dim_h(c, x1, x2, y, text, ref1=None, ref2=None, size=7.2, above=True, ext_over=None, gap=None,
          text_at=None):
    """Horizontal dimension at height y between x1 and x2. ref1/ref2 = y of the measured object;
    when given, an extension line is drawn from it to the dimension line. text_at=(x, y) moves
    the number (e.g. outside a narrow wall)."""
    over = ext_over if ext_over is not None else c.pt(4)
    g = gap if gap is not None else c.pt(2.5)
    xa, xb = min(x1, x2), max(x1, x2)
    c.line(xa - c.pt(3), y, xb + c.pt(3), y, 0.3)
    for x, ref in ((x1, ref1), (x2, ref2)):
        if ref is not None:
            sgn = 1 if y > ref else -1
            c.line(x, ref + sgn * g, x, y + sgn * over, 0.3)
        tick(c, x, y)
    tx, ty = text_at or ((x1 + x2) / 2.0, y - c.pt(size * 0.72) if above else y + c.pt(size * 0.72))
    c.text(tx, ty, text, size=size, weight=500)


def dim_v(c, y1, y2, x, text, ref1=None, ref2=None, size=7.2, left=True, ext_over=None, gap=None,
          text_at=None):
    """Vertical dimension at x between y1 and y2. ref1/ref2 = x of the measured object."""
    over = ext_over if ext_over is not None else c.pt(4)
    g = gap if gap is not None else c.pt(2.5)
    ya, yb = min(y1, y2), max(y1, y2)
    c.line(x, ya - c.pt(3), x, yb + c.pt(3), 0.3)
    for y, ref in ((y1, ref1), (y2, ref2)):
        if ref is not None:
            sgn = 1 if x > ref else -1
            c.line(ref + sgn * g, y, x + sgn * over, y, 0.3)
        tick(c, x, y)
    tx, ty = text_at or (x - c.pt(size * 0.72) if left else x + c.pt(size * 0.72), (y1 + y2) / 2.0)
    c.text(tx, ty, text, size=size, weight=500, rotate=-90)


def leader(c, pts, arrow=True, w=0.35):
    c.polyline(pts, w=w)
    if arrow:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        ang = math.atan2(y1 - y0, x1 - x0)
        L, W = c.pt(5.0), c.pt(1.7)
        bx, by = x1 - L * math.cos(ang), y1 - L * math.sin(ang)
        px, py = -math.sin(ang), math.cos(ang)
        c.polyline([(x1, y1), (bx + px * W, by + py * W), (bx - px * W, by - py * W)], w=0.1, fill=INK, close=True)


def arrow_line(c, x1, y1, x2, y2, w=0.45):
    leader(c, [(x1, y1), (x2, y2)], arrow=True, w=w)


# ---------- labels ----------
def room_label(c, x, y, name, sub=None, area=None, size=11.5, sub_size=7.2):
    """Room name (bold, may contain \\n) centred on (x, y); optional flooring note and area below."""
    lines = name.split('\n')
    h = c.pt(size) * 1.1
    top = y - h * (len(lines) - 1) / 2.0
    for i, s in enumerate(lines):
        c.text(x, top + i * h, s, size=size, weight=700, spacing=0.35)
    yy = top + (len(lines) - 1) * h + c.pt(size) * 0.5
    if sub:
        yy += c.pt(sub_size) * 0.95
        c.text(x, yy, sub, size=sub_size, weight=400, spacing=0.2)
        yy += c.pt(sub_size) * 0.35
    if area:
        yy += c.pt(7.6) * 1.05
        c.text(x, yy, area, size=7.6, weight=500, italic=True, color=NAVY)


def area_tag(c, x, y, s, size=7.6):
    c.text(x, y, s, size=size, weight=500, italic=True, color=NAVY)


def note(c, x, y, lines, size=6.6, leaders=(), **kw):
    """Printed note (string with \\n or list of lines) plus optional leaders [(pts), ...]."""
    if isinstance(lines, str):
        lines = lines.split('\n')
    kw.setdefault('weight', 500)
    c.lines_text(x, y, lines, size=size, **kw)
    for pts in leaders:
        leader(c, pts)


# ---------- fixtures ----------
class Frame:
    """Local frame for a fixture: u runs along the wall, v points out into the room."""
    DIRS = {'down': ((1, 0), (0, 1)), 'up': ((-1, 0), (0, -1)),
            'right': ((0, -1), (1, 0)), 'left': ((0, 1), (-1, 0))}

    def __init__(self, c, x, y, facing):
        self.c, self.x, self.y = c, x, y
        (self.ux, self.uy), (self.vx, self.vy) = self.DIRS[facing]
        self.swap = facing in ('left', 'right')

    def p(self, u, v):
        return (self.x + u * self.ux + v * self.vx, self.y + u * self.uy + v * self.vy)

    def rect(self, u0, v0, u1, v1, **kw):
        (xa, ya), (xb, yb) = self.p(u0, v0), self.p(u1, v1)
        self.c.rect(min(xa, xb), min(ya, yb), abs(xb - xa), abs(yb - ya), **kw)

    def ellipse(self, cu, cv, ru, rv, **kw):
        x, y = self.p(cu, cv)
        rx, ry = (rv, ru) if self.swap else (ru, rv)
        self.c.ellipse(x, y, rx, ry, **kw)

    def circle(self, cu, cv, r, **kw):
        x, y = self.p(cu, cv)
        self.c.circle(x, y, r, **kw)

    def line(self, u0, v0, u1, v1, **kw):
        self.c.line(*self.p(u0, v0), *self.p(u1, v1), **kw)

    def poly(self, pts, **kw):
        self.c.polyline([self.p(u, v) for u, v in pts], **kw)

    def text(self, cu, cv, s, **kw):
        x, y = self.p(cu, cv)
        self.c.text(x, y, s, **kw)


def toilet(c, x, y, facing):
    """Toilet: (x, y) = centre of the tank on the wall face; the bowl faces `facing`."""
    F = Frame(c, x, y, facing)
    F.rect(-10, 0.5, 10, 8.5, sw=0.45, fill=WHITE, rx=1)
    F.ellipse(0, 18.5, 7.5, 10, sw=0.45, fill=WHITE)
    F.ellipse(0, 19.5, 5.5, 7.5, sw=0.25)


def vanity(c, x, y, facing, length, depth=21, sinks=(0,)):
    """Vanity counter against a wall; sinks = sink centre offsets along the wall from (x, y)."""
    F = Frame(c, x, y, facing)
    F.rect(-length / 2.0, 0, length / 2.0, depth, sw=0.45)
    for su in sinks:
        F.ellipse(su, depth / 2.0 + 1, 8, 6.5, sw=0.4)
        F.ellipse(su, depth / 2.0 + 1.5, 6, 4.8, sw=0.25)
        F.circle(su, 2.5, 1.1, sw=0.35)


def sink(c, x, y, facing, w=33, d=19, bowls=2):
    """Sink set in a counter; (x, y) = centre of the counter back edge. Faucet at the back."""
    F = Frame(c, x, y, facing)
    bw = (w - 3 * (bowls - 1)) / float(bowls)
    for i in range(bowls):
        u0 = -w / 2.0 + i * (bw + 3)
        F.rect(u0, 3.5, u0 + bw, 3.5 + d - 2, sw=0.4, rx=2)
    F.circle(0, 2, 1.3, sw=0.35)


def appliance(c, x, y, facing, w, d, label=None, size=6.3):
    """Box appliance (washer, dryer, fridge, range, dishwasher) with its back on the wall."""
    F = Frame(c, x, y, facing)
    F.rect(-w / 2.0, 0, w / 2.0, d, sw=0.45, fill=WHITE)
    if label:
        F.text(0, d / 2.0, label, size=size, weight=500)


def cooktop(c, x, y, facing, w=30, d=21, cols=2, rows=2):
    F = Frame(c, x, y, facing)
    F.rect(-w / 2.0, 1, w / 2.0, d, sw=0.45, fill=WHITE)
    for i in range(cols):
        for j in range(rows):
            F.circle(-w / 2.0 + w * (i + 0.5) / cols, 1 + (d - 1) * (j + 0.5) / rows, min(w / cols, d / rows) * 0.3,
                     sw=0.35)


def round_equipment(c, x, y, d, double=False):
    """Water heater, sump pit, etc. drawn as a circle (double ring for a pit)."""
    c.circle(x, y, d / 2.0, sw=0.45, fill=WHITE)
    if double:
        c.circle(x, y, d / 2.0 - 3, sw=0.3)


def ceiling_fan(c, x, y, r=25):
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux
        r0, hw = 5.0, 3.0
        c.polyline([(x + ux * r0 + px * hw * 0.6, y + uy * r0 + py * hw * 0.6),
                    (x + ux * r + px * hw, y + uy * r + py * hw),
                    (x + ux * (r + 2), y + uy * (r + 2)),
                    (x + ux * r - px * hw, y + uy * r - py * hw),
                    (x + ux * r0 - px * hw * 0.6, y + uy * r0 - py * hw * 0.6)],
                   w=0.35, close=True, fill=WHITE, join='round')
    c.circle(x, y, 5.0, sw=0.45, fill=WHITE)
    c.circle(x, y, 2.0, sw=0.3)


def column(c, x, y, d=6, square=False):
    if square:
        c.rect(x - d / 2.0, y - d / 2.0, d, d, sw=0.5, fill=WHITE)
        c.line(x - d / 2.0, y - d / 2.0, x + d / 2.0, y + d / 2.0, 0.3)
        c.line(x + d / 2.0, y - d / 2.0, x - d / 2.0, y + d / 2.0, 0.3)
    else:
        c.circle(x, y, d / 2.0, sw=0.5, fill=WHITE)


def shower(c, x0, y0, x1, y1, drain=True):
    """Shower floor: slope lines to a centre drain."""
    c.line(x0, y0, x1, y1, 0.25); c.line(x1, y0, x0, y1, 0.25)
    if drain:
        c.circle((x0 + x1) / 2.0, (y0 + y1) / 2.0, 2.0, sw=0.35, fill=WHITE)


def tub(c, x0, y0, x1, y1):
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0.45)
    c.rect(x0 + 3, y0 + 3, x1 - x0 - 6, y1 - y0 - 6, sw=0.3, rx=6)


def fireplace(c, x, y, facing, w=60, d=16):
    """Fireplace / hearth box with its back on the wall at (x, y)."""
    F = Frame(c, x, y, facing)
    F.rect(-w / 2.0, 0, w / 2.0, d, sw=0.45, fill=WHITE)
    F.rect(-w / 2.0 + 12, 3, w / 2.0 - 12, d - 4, sw=0.3)


# ---------- loose furniture (light gray, for layout only) ----------
BED_SIZES = {'twin': (39, 75), 'full': (54, 75), 'queen': (60, 80), 'king': (76, 80)}


def furniture(c, x, y, w, h, rx=0):
    c.rect(x, y, w, h, sw=0.4, color=FURN, rx=rx)


def furniture_poly(c, pts):
    """Any outline, e.g. an L-shaped sectional."""
    c.polyline(pts, w=0.4, color=FURN, close=True)


def furniture_label(c, x, y, s, size=5.8, **kw):
    c.text(x, y, s, size=size, weight=500, color=FURN_TXT, **kw)


def bed(c, x, y, facing, size='king', nightstands=0, gap=2):
    """Bed with its headboard centred on the wall at (x, y), foot toward `facing`. size is
    'twin' | 'full' | 'queen' | 'king' or (width, length). nightstands = width of one each side."""
    w, l = BED_SIZES[size] if isinstance(size, str) else size
    F = Frame(c, x, y, facing)
    kw = dict(sw=0.4, color=FURN)
    F.rect(-w / 2.0, gap, w / 2.0, gap + l, rx=1.5, **kw)
    pw = (w - 7) / 2.0
    F.rect(-w / 2.0 + 2.5, gap + 2.5, -w / 2.0 + 2.5 + pw, gap + 13.5, rx=2.5, **kw)
    F.rect(w / 2.0 - 2.5 - pw, gap + 2.5, w / 2.0 - 2.5, gap + 13.5, rx=2.5, **kw)
    F.line(-w / 2.0, gap + 24, w / 2.0, gap + 24, w=0.35, color=FURN)
    if nightstands:
        for s in (-1, 1):
            u0, u1 = s * (w / 2.0 + 2), s * (w / 2.0 + 2 + nightstands)
            F.rect(min(u0, u1), gap, max(u0, u1), gap + 16, **kw)


def sofa(c, x, y, facing, w=84, d=36, arms=True):
    """Sofa with its back centred on (x, y), seats facing `facing`."""
    F = Frame(c, x, y, facing)
    a = 6 if arms else 0
    F.rect(-w / 2.0, 0, w / 2.0, d, sw=0.4, color=FURN, rx=2)
    F.line(-w / 2.0 + a, 9, w / 2.0 - a, 9, w=0.35, color=FURN)
    if arms:
        F.line(-w / 2.0 + a, 0, -w / 2.0 + a, d, w=0.35, color=FURN)
        F.line(w / 2.0 - a, 0, w / 2.0 - a, d, w=0.35, color=FURN)


def table(c, x, y, w, l=None, rx=3):
    """Table centred on (x, y): round when l is None (w = diameter), else w across by l down."""
    if l is None:
        c.circle(x, y, w / 2.0, sw=0.4, color=FURN)
    else:
        c.rect(x - w / 2.0, y - l / 2.0, w, l, sw=0.4, color=FURN, rx=rx)


def stools(c, pts, d=15):
    for x, y in pts:
        c.circle(x, y, d / 2.0, sw=0.4, color=FURN)


def stair_lines(c, x0, y0, x1, y1, n, axis='y', w=0.35):
    """n tread lines evenly spaced from one end of the box to the other. axis='y': lines are
    horizontal (the run goes up/down the sheet); axis='x': lines are vertical."""
    for i in range(n):
        t = i / float(n - 1) if n > 1 else 0.5
        if axis == 'y':
            y = y0 + (y1 - y0) * t
            c.line(x0, y, x1, y, w)
        else:
            x = x0 + (x1 - x0) * t
            c.line(x, y0, x, y1, w)
