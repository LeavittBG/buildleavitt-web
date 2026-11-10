"""blib.py - redraw the raster floor plans inside Leavitt brochures as clean vector drawings.

Coordinates are the SOURCE IMAGE's pixels (x right, y down). The new drawing is rendered at the
image's exact size and put back in the image's exact rectangle on the brochure page, so it lines
up with the original by construction. At the brochure resolution (438 px per paper inch) the plans
are about 37.8 px per foot (Pioneer I: garage 21'-4" inside = 806 px).

  c = new(img_path)                      -> Canvas (planlib) sized to the image; c.W, c.H
  walls, wins = trace(img_path, ...)     -> wall geometry (shapely) + window polygons
  draw_plan_walls(c, walls, wins)        -> solid navy walls, windows on top
  door(c, H, J, side)                    -> any-angle hinged door: hinge H, closed leaf to J
  label(c, x, y, 'NAME', '13\'-7" × 13\'-10"')   etc.
  render(c, out_pdf) ; compare(img_path, out_pdf, out_png)
  swap(src_pdf, page_no, xref, new_pdf, dst_pdf)  -> brochure with the image replaced
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import cv2
from shapely.geometry import Polygon, MultiPolygon, box as sbox, LineString
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import planlib as P
from planlib import Canvas

K = 438.0                      # image px per paper inch
PXFT = 37.8                    # px per foot (calibrated on Pioneer I)
NAVY = '#0d1b2a'               # brochure navy
INKC = '#0d1b2a'
GREY = '#6b7480'               # secondary text (sizes, notes)
OPT = '#8a94a0'                # optional / dashed work
FILL = '#0d1b2a'
FONT = "'Roboto Condensed', 'Arial Narrow', sans-serif"
P.INK = INKC                   # planlib primitives default to this ink


def ft_px(feet, inches=0.0):
    return (feet * 12 + inches) / 12.0 * PXFT


# ------------------------------------------------------------------ raster reading
def load(img_path):
    a = np.asarray(Image.open(img_path).convert('RGB')).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    grey = (abs(r - 146) < 14) & (abs(g - 152) < 14) & (abs(b - 159) < 14)
    navy = (r < 70) & (g < 80) & (b < 95)
    return a, grey, navy


def _rects_mask(shape, rects):
    m = np.zeros(shape, bool)
    for x0, y0, x1, y1 in rects:
        m[int(y0):int(y1), int(x0):int(x1)] = True
    return m


def _snap_ring(pts, tol_deg=9):
    """Snap each edge to 0/45/90/135 degrees when close, then rebuild the corners as the
    intersections of consecutive edges."""
    n = len(pts)
    if n < 3:
        return pts
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) % 180
        best = min((0, 45, 90, 135, 180), key=lambda a: abs(a - ang))
        if abs(best - ang) <= tol_deg:
            ang = best % 180
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        lines.append((mx, my, math.cos(math.radians(ang)), math.sin(math.radians(ang)), ang))
    # merge consecutive collinear edges
    merged = []
    for L in lines:
        if merged and abs(merged[-1][4] - L[4]) < 1e-6:
            pm = merged[-1]
            # perpendicular offset between the two parallel lines
            d = abs((L[0] - pm[0]) * (-pm[3]) + (L[1] - pm[1]) * pm[2])
            if d < 2.5:
                continue
        merged.append(L)
    if len(merged) > 1 and abs(merged[0][4] - merged[-1][4]) < 1e-6:
        pm, L = merged[-1], merged[0]
        if abs((L[0] - pm[0]) * (-pm[3]) + (L[1] - pm[1]) * pm[2]) < 2.5:
            merged.pop()
    out = []
    m = len(merged)
    for i in range(m):
        a, b = merged[i - 1], merged[i]
        det = a[2] * b[3] - a[3] * b[2]
        if abs(det) < 1e-9:
            continue
        t = ((b[0] - a[0]) * b[3] - (b[1] - a[1]) * b[2]) / det
        out.append((a[0] + a[2] * t, a[1] + a[3] * t))
    return out


def _vectorize(mask, eps=1.6, min_area=60):
    m = mask.astype(np.uint8) * 255
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    if hier is None:
        return Polygon()
    hier = hier[0]
    for i, cnt in enumerate(cs):
        if hier[i][3] != -1:
            continue
        if cv2.contourArea(cnt) < min_area:
            continue
        ring = _snap_ring([tuple(map(float, p[0])) for p in cv2.approxPolyDP(cnt, eps, True)])
        holes = []
        j = hier[i][2]
        while j != -1:
            if cv2.contourArea(cs[j]) >= min_area:
                h = _snap_ring([tuple(map(float, p[0])) for p in cv2.approxPolyDP(cs[j], eps, True)])
                if len(h) >= 3:
                    holes.append(h)
            j = hier[j][0]
        if len(ring) >= 3:
            p = Polygon(ring, holes).buffer(0)
            if not p.is_empty:
                polys.append(p)
    return unary_union(polys)


def trace(img_path, drop=(), add=(), win_drop=(), win_keep=None, grow=9, win_k=13, cut=()):
    """Wall shape + window polygons from the brochure raster.
    drop     : rects (x0,y0,x1,y1) whose pixels are ignored (stairs, fixtures picked up as walls)
    add      : extra wall shapes (shapely or rects) for walls the raster test misses
    cut      : rects removed from the final wall shape (door gaps the raster closes)
    win_drop : rects; window blobs whose centre falls inside are discarded
    win_keep : optional rect list; when given, only window blobs centred inside are kept"""
    a, grey, navy = load(img_path)
    g = ndi.binary_opening(grey, np.ones((3, 3), bool))
    walls = ndi.binary_dilation(g, np.ones((grow, grow), bool)) & (grey | navy)
    win = ndi.binary_opening(navy, np.ones((win_k, win_k), bool))
    dm = _rects_mask(grey.shape, drop)
    walls &= ~dm
    win &= ~dm
    # windows: navy blobs that touch wall fill
    lab, n = ndi.label(win)
    wins = []
    near = ndi.binary_dilation(walls, np.ones((19, 19), bool))
    for i in range(1, n + 1):
        blob = lab == i
        if not (blob & near).any():
            continue
        ys, xs = np.nonzero(blob)
        cx, cy = xs.mean(), ys.mean()
        if any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in win_drop):
            continue
        if win_keep is not None and not any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in win_keep):
            continue
        cnts, _ = cv2.findContours(blob.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rect = cv2.minAreaRect(max(cnts, key=cv2.contourArea))
        wins.append(rect)
    allm = walls.copy()
    for (cx, cy), (w, h), ang in wins:
        pts = cv2.boxPoints(((cx, cy), (w + 2, h + 2), ang)).astype(np.int32)
        cv2.fillPoly(allm.view(np.uint8), [pts], 1)
    allm = ndi.binary_closing(allm, np.ones((3, 3), bool))
    geom = _vectorize(allm)
    extra = [sbox(*r) if isinstance(r, tuple) else r for r in add]
    if extra:
        geom = unary_union([geom] + extra)
    if cut:
        geom = geom.difference(unary_union([sbox(*r) for r in cut]))
    wpolys = []
    for (cx, cy), (w, h), ang in wins:
        if w < h:
            w, h, ang = h, w, ang + 90
        ang = round(ang / 45.0) * 45.0
        wpolys.append(((cx, cy), w, h, ang))
    return geom, wpolys


# ------------------------------------------------------------------ drawing
def new(img_path):
    im = Image.open(img_path)
    c = Canvas(K)
    c.W, c.H = im.size
    c.img = img_path
    return c


def poly_path(geom):
    return P._poly_path(geom)


def draw_plan_walls(c, geom, wins=(), style='solid'):
    """Solid navy walls (the Valoetis look); windows drawn over them."""
    if not geom.is_empty:
        b = geom.bounds
        c.grow(b[0], b[1]); c.grow(b[2], b[3])
        c.path(poly_path(geom), sw=0.35, color=NAVY, fill=FILL,
               extra='fill-rule="evenodd" stroke-linejoin="miter"')
    for w in wins:
        window_rot(c, *w)


def window_rot(c, center, length, thick, ang):
    """Window at any angle: white glazing pocket with a centre line, end jambs in navy."""
    cx, cy = center
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    L, T = length / 2.0, thick / 2.0
    def p(u, v):
        return (cx + u * ux + v * vx, cy + u * uy + v * vy)
    inset = c.pt(0.9)
    c.polyline([p(-L + inset, -T + inset * 0.6), p(L - inset, -T + inset * 0.6),
                p(L - inset, T - inset * 0.6), p(-L + inset, T - inset * 0.6)],
               w=0.3, color=NAVY, fill='#ffffff', close=True)
    c.line(*p(-L + inset, 0), *p(L - inset, 0), w=0.3, color=NAVY)


def door(c, H, J, side=1, leaf=None, arc=True, w=0.55):
    """Hinged door drawn open 90 degrees. H = hinge point, J = the other jamb (where the leaf
    sits when closed). side = +1 / -1 picks which side of the wall it swings to (rotation of
    H->J by +90 or -90 degrees in screen coordinates)."""
    hx, hy = H
    jx, jy = J
    dx, dy = jx - hx, jy - hy
    r = math.hypot(dx, dy)
    ox, oy = (-dy, dx) if side > 0 else (dy, -dx)
    tip = (hx + ox, hy + oy)
    lt = leaf or c.pt(1.6)
    nx, ny = ox / r, oy / r            # along the open leaf
    px_, py_ = dx / r * lt, dy / r * lt  # leaf thickness toward the opening
    c.polyline([(hx, hy), tip, (tip[0] + px_, tip[1] + py_), (hx + px_, hy + py_)], w=w, color=NAVY,
               fill='#ffffff', close=True)
    if arc:
        a0 = math.degrees(math.atan2(oy, ox))
        a1 = math.degrees(math.atan2(dy, dx))
        d = (a1 - a0 + 540) % 360 - 180
        c.arc(hx, hy, r, a0, a0 + d, sw=0.3, color=NAVY)


def double_door(c, A, B, side=1, **kw):
    m = ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0)
    door(c, A, m, side, **kw)
    door(c, B, m, -side, **kw)


def bifold_pair(c, A, B, side=1, depth=0.42):
    """Bifold closet doors across A-B (any angle)."""
    ax, ay = A; bx, by = B
    dx, dy = bx - ax, by - ay
    r = math.hypot(dx, dy)
    nx, ny = (-dy / r, dx / r) if side > 0 else (dy / r, -dx / r)
    for s, e in ((A, (ax + dx / 2, ay + dy / 2)), (B, (ax + dx / 2, ay + dy / 2))):
        sx, sy = s; ex, ey = e
        L = math.hypot(ex - sx, ey - sy)
        k = L / 2.0 * depth
        mx, my = (sx + ex) / 2 + nx * k, (sy + ey) / 2 + ny * k
        c.polyline([s, (mx, my), e], w=0.5, color=NAVY)


def slider(c, A, B, thick):
    """Sliding glass door between A and B (wall thickness thick), any angle."""
    ax, ay = A; bx, by = B
    dx, dy = bx - ax, by - ay
    r = math.hypot(dx, dy)
    ux, uy = dx / r, dy / r
    vx, vy = -uy, ux
    t = thick / 2.0
    pnl = thick * 0.22
    def p(u, v):
        return (ax + ux * u + vx * v, ay + uy * u + vy * v)
    c.polyline([p(0, -t), p(r, -t), p(r, t), p(0, t)], w=0.3, color=NAVY, fill='#ffffff', close=True)
    c.polyline([p(0, -pnl * 1.2), p(r * 0.55, -pnl * 1.2), p(r * 0.55, -pnl * 0.2), p(0, -pnl * 0.2)],
               w=0.4, color=NAVY, fill='#ffffff', close=True)
    c.polyline([p(r * 0.45, pnl * 0.2), p(r, pnl * 0.2), p(r, pnl * 1.2), p(r * 0.45, pnl * 1.2)],
               w=0.4, color=NAVY, fill='#ffffff', close=True)


def text(c, x, y, s, size=4.6, weight=500, color=NAVY, **kw):
    kw.setdefault('family', FONT)
    c.text(x, y, s, size=size, weight=weight, color=color, **kw)


def label(c, x, y, name, size_txt=None, note=None, name_pt=6.6, sub_pt=5.0, color=NAVY, rotate=0):
    """Room name (bold caps, may contain \\n), optional size line and note (e.g. OPT. TRAY CEILING)."""
    lines = name.split('\n')
    lh = c.pt(name_pt) * 1.12
    extra = (1 if size_txt else 0) + (1 if note else 0)
    total = lh * len(lines) + extra * c.pt(sub_pt) * 1.35
    y0 = y - total / 2.0 + lh / 2.0
    for i, s in enumerate(lines):
        text(c, x, y0 + i * lh, s, size=name_pt, weight=700, color=color, spacing=0.25, rotate=rotate)
    yy = y0 + (len(lines) - 1) * lh + lh * 0.5 + c.pt(sub_pt) * 0.75
    if size_txt:
        text(c, x, yy, size_txt, size=sub_pt, weight=500, color=GREY, spacing=0.1)
        yy += c.pt(sub_pt) * 1.35
    if note:
        text(c, x, yy, note, size=sub_pt * 0.9, weight=500, color=OPT, spacing=0.3)


def small(c, x, y, s, size=3.9, color=NAVY, weight=500, **kw):
    text(c, x, y, s, size=size, weight=weight, color=color, spacing=0.2, **kw)


def dashed(c, pts, close=False, w=0.4, color=OPT, on=3.0, off=2.0):
    c.polyline(pts, w=w, color=color, dash=c.dash(on, off), close=close)


def dashed_rect(c, x0, y0, x1, y1, **kw):
    dashed(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, **kw)


def treads(c, x0, y0, x1, y1, n, axis='x', w=0.4, color=NAVY):
    """n tread lines across a straight flight box; axis='x' means the run goes along x."""
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0.5, color=color)
    for i in range(1, n):
        t = i / float(n)
        if axis == 'x':
            x = x0 + (x1 - x0) * t
            c.line(x, y0, x, y1, w, color=color)
        else:
            y = y0 + (y1 - y0) * t
            c.line(x0, y, x1, y, w, color=color)


def arrow(c, pts, w=0.45, color=NAVY):
    c.polyline(pts, w=w, color=color)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    L, W = c.pt(3.6), c.pt(1.3)
    bx, by = x1 - L * math.cos(ang), y1 - L * math.sin(ang)
    px_, py_ = -math.sin(ang), math.cos(ang)
    c.polyline([(x1, y1), (bx + px_ * W, by + py_ * W), (bx - px_ * W, by - py_ * W)], w=0.1, color=color,
               fill=color, close=True)


def break_line(c, x0, y0, x1, y1, w=0.4):
    """Stair cut line with a zig-zag in the middle, from (x0,y0) to (x1,y1)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    vx, vy = -uy, ux
    z = c.pt(2.2)
    m = L / 2.0
    pts = [(x0, y0)]
    for u, v in ((m - z, 0), (m - z * 0.4, z), (m + z * 0.4, -z), (m + z, 0)):
        pts.append((x0 + ux * u + vx * v, y0 + uy * u + vy * v))
    pts.append((x1, y1))
    c.polyline(pts, w=w, color=NAVY)


# fixtures ------------------------------------------------------------------
def frame(c, x, y, facing):
    return P.Frame(c, x, y, facing)


def toilet(c, x, y, facing, s=1.0):
    """Toilet scaled to the plan: (x,y) = tank back centre on the wall."""
    F = P.Frame(c, x, y, facing)
    k = PXFT / 12.0 * s           # px per inch
    F.rect(-10 * k, 0.5 * k, 10 * k, 8.5 * k, sw=0.4, color=NAVY, fill='#ffffff', rx=1 * k)
    F.ellipse(0, 18.5 * k, 7.5 * k, 10 * k, sw=0.4, color=NAVY, fill='#ffffff')
    F.ellipse(0, 19.5 * k, 5.5 * k, 7.5 * k, sw=0.25, color=NAVY)


def vanity(c, x, y, facing, length_in, depth_in=21, sinks=(0,), rect_sinks=True):
    """Vanity with undermount rectangular sinks (sink offsets in inches along the wall)."""
    k = PXFT / 12.0
    F = P.Frame(c, x, y, facing)
    F.rect(-length_in * k / 2, 0, length_in * k / 2, depth_in * k, sw=0.45, color=NAVY, fill='#ffffff')
    for su in sinks:
        u = su * k
        if rect_sinks:
            F.rect(u - 8.5 * k, 4 * k, u + 8.5 * k, 16.5 * k, sw=0.35, color=NAVY, rx=2 * k)
        else:
            F.ellipse(u, 10.5 * k, 8 * k, 6.5 * k, sw=0.35, color=NAVY)
        F.circle(u, 2.2 * k, 1.0 * k, sw=0.3, color=NAVY)


def shower(c, x0, y0, x1, y1, glass=None, drain='linear'):
    """Walk-in tiled shower: outline, linear drain along the far wall, glass panel line.
    glass = ((xa,ya),(xb,yb)) for the glass panel."""
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0.45, color=NAVY, fill='#ffffff')
    k = PXFT / 12.0
    if drain == 'linear':
        if (x1 - x0) >= (y1 - y0):
            yy = y0 + 4 * k
            c.rect(x0 + 6 * k, yy, (x1 - x0) - 12 * k, 1.6 * k, sw=0.3, color=NAVY)
        else:
            xx = x0 + 4 * k
            c.rect(xx, y0 + 6 * k, 1.6 * k, (y1 - y0) - 12 * k, sw=0.3, color=NAVY)
    else:
        c.circle((x0 + x1) / 2, (y0 + y1) / 2, 1.6 * k, sw=0.3, color=NAVY)
    if glass:
        (xa, ya), (xb, yb) = glass
        c.line(xa, ya, xb, yb, 0.9, color=NAVY)


def tub(c, x0, y0, x1, y1):
    k = PXFT / 12.0
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0.45, color=NAVY, fill='#ffffff')
    c.rect(x0 + 3 * k, y0 + 3 * k, x1 - x0 - 6 * k, y1 - y0 - 6 * k, sw=0.3, color=NAVY, rx=7 * k)


def box(c, x0, y0, x1, y1, sw=0.45, fill='#ffffff', **kw):
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=sw, color=NAVY, fill=fill, **kw)


def counter(c, pts, sw=0.45):
    c.polyline(pts, w=sw, color=NAVY, close=True, fill='#ffffff')


def kitchen_sink(c, cx, cy, horizontal=True, w_in=33, d_in=19, bowls=1):
    k = PXFT / 12.0
    w, d = w_in * k, d_in * k
    if not horizontal:
        w, d = d, w
    if bowls == 1:
        c.rect(cx - w / 2, cy - d / 2, w, d, sw=0.4, color=NAVY, rx=2 * k)
    else:
        g = 1.5 * k
        if horizontal:
            c.rect(cx - w / 2, cy - d / 2, w / 2 - g, d, sw=0.4, color=NAVY, rx=2 * k)
            c.rect(cx + g, cy - d / 2, w / 2 - g, d, sw=0.4, color=NAVY, rx=2 * k)
        else:
            c.rect(cx - w / 2, cy - d / 2, w, d / 2 - g, sw=0.4, color=NAVY, rx=2 * k)
            c.rect(cx - w / 2, cy + g, w, d / 2 - g, sw=0.4, color=NAVY, rx=2 * k)


def range_top(c, x0, y0, x1, y1):
    box(c, x0, y0, x1, y1)
    w, h = x1 - x0, y1 - y0
    r = min(w, h) * 0.17
    for fx in (0.28, 0.72):
        for fy in (0.3, 0.7):
            c.circle(x0 + w * fx, y0 + h * fy, r, sw=0.35, color=NAVY)


def fireplace(c, x0, y0, x1, y1):
    box(c, x0, y0, x1, y1)
    k = PXFT / 12.0
    c.rect(x0 + 6 * k, y0 + 3 * k, (x1 - x0) - 12 * k, (y1 - y0) - 6 * k, sw=0.3, color=NAVY)


# ------------------------------------------------------------------ output
def _fontfaces():
    """@font-face rules for Roboto Condensed from LEAVITT_FONTS or ./fonts (see build.py)."""
    for d in (os.environ.get('LEAVITT_FONTS', ''), os.path.join(HERE, 'fonts', 'node_modules', '@fontsource')):
        if d and os.path.isdir(d):
            break
    else:
        raise SystemExit('Roboto Condensed not found: install the fonts as build.py describes')
    faces = []
    for w in (400, 500, 700):
        fn = f'{d}/roboto-condensed/files/roboto-condensed-latin-{w}-normal.woff2'
        if os.path.exists(fn):
            faces.append(f"@font-face{{font-family:'Roboto Condensed';src:url('file://{fn}') format('woff2');"
                         f"font-weight:{w};font-style:normal;}}")
    return "\n".join(faces)


def render(c, out_pdf, png=True):
    """SVG at the image's pixel size -> one-page PDF whose page is the image's size at 438 dpi."""
    Wpx, Hpx = c.W, c.H
    win, hin = Wpx / K, Hpx / K
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{win}in" height="{hin}in" '
           f'viewBox="0 0 {Wpx} {Hpx}">\n{c.svg()}\n</svg>')
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{_fontfaces()}\n"
            f"@page {{ size: {win}in {hin}in; margin: 0; }} html,body {{ margin:0; padding:0; }}"
            f" svg {{ display:block; }}</style></head><body>{svg}</body></html>")
    hp = out_pdf[:-4] + '.html'
    open(hp, 'w').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        exe = os.environ.get('CHROMIUM_PATH', '/opt/pw-browsers/chromium')
        b = pw.chromium.launch(executable_path=exe) if os.path.exists(exe) else pw.chromium.launch()
        pg = b.new_page()
        pg.goto('file://' + hp)
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(300)
        pg.pdf(path=out_pdf, width=f'{win}in', height=f'{hin}in', print_background=False,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        b.close()
    os.remove(hp)
    # Chromium rounds the page up a little; trim it to the drawing's exact size (top-left
    # origin) so swap() maps the drawing onto the image's rectangle without rescaling it.
    import pikepdf
    with pikepdf.open(out_pdf, allow_overwriting_input=True) as pdf:
        pg = pdf.pages[0]
        x0, y0, x1, y1 = [float(v) for v in pg.mediabox]
        pg.mediabox = pikepdf.Array([x0, y1 - hin * 72.0, x0 + win * 72.0, y1])
        if '/CropBox' in pg.obj:
            del pg.obj['/CropBox']
        pdf.save(out_pdf)
    if png:
        subprocess.run(['pdftoppm', '-r', str(int(K)), '-png', '-singlefile', out_pdf, out_pdf[:-4]], check=True)
    return out_pdf


def compare(img_path, new_pdf, out_png, crop=None, scale=0.5):
    """Original in light blue-grey under the redraw in red; crop=(x0,y0,x1,y1) in px."""
    orig = Image.open(img_path).convert('L')
    newp = new_pdf[:-4] + '.png'
    if not os.path.exists(newp):
        subprocess.run(['pdftoppm', '-r', str(int(K)), '-png', '-singlefile', new_pdf, new_pdf[:-4]], check=True)
    nw = Image.open(newp).convert('L').resize(orig.size)
    o = np.asarray(orig).astype(float) / 255
    n = np.asarray(nw).astype(float) / 255
    rgb = np.ones(o.shape + (3,))
    shade = 1 - (1 - o) * 0.45
    rgb[..., 0] = shade * 0.75 + 0.25 * shade
    rgb[..., 1] = shade
    rgb[..., 2] = shade
    ink = 1 - n
    rgb[..., 0] = rgb[..., 0] * (1 - ink) + 0.85 * ink
    rgb[..., 1] = rgb[..., 1] * (1 - ink) + 0.05 * ink
    rgb[..., 2] = rgb[..., 2] * (1 - ink) + 0.05 * ink
    im = Image.fromarray((rgb * 255).astype(np.uint8))
    if crop:
        im = im.crop(crop)
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out_png)
    return out_png


def side_by_side(img_path, new_pdf, out_png, crop=None, scale=1.0):
    crop = crop or (0, 0) + Image.open(img_path).size
    orig = Image.open(img_path).convert('RGB').crop(crop)
    nw = Image.open(new_pdf[:-4] + '.png').convert('RGB')
    nw = nw.resize(Image.open(img_path).size).crop(crop)
    im = Image.new('RGB', (orig.width * 2 + 20, orig.height), 'white')
    im.paste(orig, (0, 0)); im.paste(nw, (orig.width + 20, 0))
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out_png)
    return out_png


def swap(src_pdf, replacements, dst_pdf):
    """replacements: [(page_no (1-based), image xref, new_pdf)]. Each image's drawing operator is
    removed from the page and the new one-page PDF is placed as a Form XObject in exactly the
    rectangle the image occupied. The image objects drop out of the file when unused."""
    import pikepdf
    import pymupdf
    d = pymupdf.open(src_pdf)
    rects = {}
    for pno, xref, _ in replacements:
        r = d[pno - 1].get_image_rects(xref)[0]
        rects[(pno, xref)] = (r.x0, r.y0, r.x1, r.y1)
    H = d[0].rect.height
    d.close()
    pdf = pikepdf.open(src_pdf)
    for pno, xref, new_pdf in replacements:
        page = pikepdf.Page(pdf.pages[pno - 1])
        name = None
        for nm, obj in page.images.items():
            if obj.objgen[0] == xref:
                name = nm
        assert name, f'xref {xref} not on page {pno}'
        ops = pikepdf.parse_content_stream(page.obj)
        keep = [(o, op) for o, op in ops if not (str(op) == 'Do' and o and str(o[0]) == str(name))]
        assert len(keep) == len(ops) - 1, 'expected exactly one Do for the image'
        page.obj.Contents = pdf.make_stream(pikepdf.unparse_content_stream(keep))
        del page.obj.Resources.XObject[name]
        src = pikepdf.open(new_pdf)
        x0, y0, x1, y1 = rects[(pno, xref)]
        page.add_overlay(pdf.copy_foreign(src.pages[0].obj) if False else src.pages[0],
                         pikepdf.Rectangle(x0, H - y1, x1, H - y0))
    pdf.remove_unreferenced_resources()
    pdf.save(dst_pdf, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    return dst_pdf


# ------------------------------------------------------------------ line art (everything that is not wall)
def _contours_to_geom(mask, eps=0.9, min_area=6):
    m = mask.astype(np.uint8) * 255
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hier is None:
        return Polygon()
    hier = hier[0]
    polys = []
    for i, cnt in enumerate(cs):
        if hier[i][3] != -1 or cv2.contourArea(cnt) < min_area:
            continue
        ring = [tuple(map(float, p[0])) for p in cv2.approxPolyDP(cnt, eps, True)]
        holes = []
        j = hier[i][2]
        while j != -1:
            if cv2.contourArea(cs[j]) >= 2:
                holes.append([tuple(map(float, p[0])) for p in cv2.approxPolyDP(cs[j], eps, True)])
            j = hier[j][0]
        if len(ring) >= 3:
            p = Polygon(ring, [h for h in holes if len(h) >= 3]).buffer(0)
            if not p.is_empty:
                polys.append(p)
    return unary_union(polys)


def lineart(img_path, walls_geom, drop=(), keep_only=None, thin=0.0, grey_thin=0.0):
    """Vector copies of the plan's own linework (door leaves and swings, cabinets, fixtures, stair
    treads, dashed option outlines), minus walls and minus `drop` rects (text, items redrawn by
    hand). Returns (navy_geom, grey_geom). thin = how much each navy stroke is slimmed (px)."""
    a, grey, navy = load(img_path)
    H, W = grey.shape
    wm = np.zeros((H, W), np.uint8)
    if not walls_geom.is_empty:
        for p in getattr(walls_geom, 'geoms', [walls_geom]):
            cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
            for h in p.interiors:
                cv2.fillPoly(wm, [np.array(h.coords, np.int32)], 0)
    wm = ndi.binary_dilation(wm.astype(bool), np.ones((5, 5), bool))
    dm = _rects_mask(grey.shape, drop)
    if keep_only is not None:
        dm |= ~_rects_mask(grey.shape, keep_only)
    lum = a.sum(-1) / 3.0
    core = lum < 75
    nv = ndi.binary_dilation(core, np.ones((2, 2), bool)) & (lum < 150) & ~wm & ~dm
    near_nv = ndi.binary_dilation(core, np.ones((5, 5), bool))
    fill = ndi.binary_dilation(ndi.binary_opening(grey, np.ones((5, 5), bool)), np.ones((3, 3), bool))
    gr = (lum < 215) & ~near_nv & ~fill & ~wm & ~dm
    gr = ndi.binary_dilation(gr, np.ones((2, 2), bool)) & ~near_nv & ~wm & ~dm
    navy_g = _contours_to_geom(nv)
    if thin:
        navy_g = navy_g.buffer(-thin, join_style=2).buffer(0)
    grey_g = _contours_to_geom(gr, eps=0.7, min_area=2)
    if grey_thin:
        grey_g = grey_g.buffer(-grey_thin, join_style=2)
    return navy_g, grey_g


def draw_geom(c, geom, color=NAVY):
    if geom.is_empty:
        return
    c.path(poly_path(geom), sw=0, fill=color, extra='fill-rule="evenodd"')


def hairlines(img_path, walls_geom, drop=()):
    """1-px linework that lineart() loses (its outline has no area): optional doors, hairline
    dashes, ceiling lines. Picked out as dark pixels not part of a thicker stroke, widened to 2 px."""
    a, grey, navy = load(img_path)
    lum = a.sum(-1) / 3.0
    core = lum < 120
    thick = ndi.binary_opening(core, np.ones((3, 3), bool))
    thin = core & ~ndi.binary_dilation(thick, np.ones((3, 3), bool))
    wm = np.zeros(core.shape, np.uint8)
    for p in getattr(walls_geom, 'geoms', [walls_geom]):
        if p.is_empty:
            continue
        cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
    wm = ndi.binary_dilation(wm.astype(bool), np.ones((7, 7), bool))
    thin &= ~wm & ~_rects_mask(core.shape, drop)
    thin = ndi.binary_dilation(thin, np.ones((2, 2), bool))
    return _contours_to_geom(thin, eps=0.6, min_area=2)
