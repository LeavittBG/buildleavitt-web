"""Helpers for the basement jobs (kept out of blib.py)."""
import sys
import numpy as np, cv2
from scipy import ndimage as ndi
import blib as B


def thin_lines(img_path, walls_geom, drop=(), keep_only=None):
    """1-2 px dark lines (dashed option outlines, hairlines). blib.lineart loses these because a
    1 px contour collapses to a zero-area polygon; here they are widened to 3 px first."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    core = lum < 140
    thick = ndi.binary_opening(core, np.ones((3, 3), bool))
    thick = ndi.binary_dilation(thick, np.ones((3, 3), bool))
    thin = core & ~thick
    wm = np.zeros(grey.shape, np.uint8)
    for p in getattr(walls_geom, 'geoms', [walls_geom]):
        if p.is_empty:
            continue
        cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
    thin &= ~ndi.binary_dilation(wm.astype(bool), np.ones((5, 5), bool))
    dm = B._rects_mask(grey.shape, drop)
    if keep_only is not None:
        dm |= ~B._rects_mask(grey.shape, keep_only)
    thin &= ~dm
    thin = ndi.binary_dilation(thin, np.ones((2, 2), bool))
    return B._contours_to_geom(thin, eps=0.7, min_area=4)


def bands_any(img_path, max_half=15, min_area=250, drop=(), keep=None):
    """Foundation bands for cropped option drawings: narrow white gaps between two foundation
    lines, found without needing an enclosed outline (the crop cuts them open). The image edge
    is treated as ink so a band running off the edge still closes."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = (lum < 200) | grey
    ink[0, :] = ink[-1, :] = True
    ink[:, 0] = ink[:, -1] = True
    free = ~ink
    lab, n = ndi.label(free)
    dist = ndi.distance_transform_edt(free)
    out = np.zeros_like(free)
    for i in range(1, n + 1):
        comp = lab == i
        if comp.sum() < min_area or dist[comp].max() > max_half:
            continue
        out |= comp
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    out[0, :] = out[-1, :] = False
    out[:, 0] = out[:, -1] = False
    return B._contours_to_geom(out, eps=1.0, min_area=50)


def bands_dir(img_path, L=34, min_area=300, drop=(), keep=None):
    """Foundation bands for cropped drawings: white gaps narrower than L px between two solid
    (>= 3 px) lines, closed along each of four directions. Dashed lines are too thin to count.
    Stairs and other striped areas must be excluded with `drop`."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = ndi.binary_opening((lum < 170) | grey, np.ones((3, 3), bool))
    free = ~((lum < 230) | grey)
    k = L
    kernels = [np.ones((1, k), bool), np.ones((k, 1), bool), np.eye(k, dtype=bool), np.fliplr(np.eye(k, dtype=bool))]
    out = np.zeros_like(free)
    for ker in kernels:
        out |= ndi.binary_closing(ink, structure=ker) & free
    lab, n = ndi.label(out)
    sizes = ndi.sum(out, lab, range(1, n + 1))
    keep_ids = [i + 1 for i, s in enumerate(sizes) if s >= min_area]
    out = np.isin(lab, keep_ids)
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    return B._contours_to_geom(out, eps=1.0, min_area=50)


def bands_width(img_path, half=13, win=31, min_area=300, drop=(), keep=None):
    """Foundation bands: white areas whose local half-width (distance to the nearest solid line,
    maximised over a win x win window) stays <= half px, i.e. gaps under about 2*half px between
    two solid lines. Room corners and open space fail the test; stairs must be dropped."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = ndi.binary_opening((lum < 170) | grey, np.ones((3, 3), bool))
    free = ~ink & ~((lum < 230) | grey)
    dist = ndi.distance_transform_edt(~ink)
    lm = ndi.maximum_filter(dist, size=win)
    out = free & (lm <= half)
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    lab, n = ndi.label(out)
    sizes = ndi.sum(out, lab, range(1, n + 1))
    out = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= min_area])
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    out[0, :] = out[-1, :] = False
    out[:, 0] = out[:, -1] = False
    return B._contours_to_geom(out, eps=1.0, min_area=50)


CONC = '#e4e7eb'


def vignette(c, img, drop=(), band_drop=(), win_drop=(), add=(), cut=(), before=None, after=None,
             bands=True, trace_kw=None):
    """Standard option-drawing build: concrete bands, traced linework minus `drop`, hand-drawn
    items (`before`, under the walls), walls and windows, then `after` (labels)."""
    walls, wins = B.trace(img, win_drop=win_drop, add=add, cut=cut, **(trace_kw or {}))
    if bands:
        B.draw_geom(c, bands_width(img, drop=band_drop), CONC)
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    if before:
        before(c)
    B.draw_plan_walls(c, walls, wins)
    if after:
        after(c)


def text_boxes(img, walls=None, hmin=10, hmax=42, pad=4):
    """Find the hand-lettered labels in a brochure raster (for drop rects): small navy glyph
    components merged into words along a line (or down a column, for turned text).
    Returns [(x0,y0,x1,y1)]. Review the result with show_boxes before trusting it."""
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    core = lum < 140
    if walls is not None:
        wm = np.zeros(core.shape, np.uint8)
        for p in getattr(walls, 'geoms', [walls]):
            if not p.is_empty:
                cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
        core &= ~ndi.binary_dilation(wm.astype(bool), np.ones((5, 5), bool))
    lab, n = ndi.label(core, np.ones((3, 3), bool))
    glyphs = []
    for i, sl in enumerate(ndi.find_objects(lab)):
        if sl is None:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        h, w = y1 - y0, x1 - x0
        big, small = max(h, w), min(h, w)
        if not (hmin <= big <= hmax) or small < 4:
            continue
        if (lab[sl] == i + 1).mean() > 0.55 and small > 8:
            continue
        glyphs.append([x0, y0, x1, y1, h >= w * 0.7])
    def merge(boxes, horiz):
        changed = True
        while changed:
            changed = False
            out = []
            for b in boxes:
                for o in out:
                    if horiz:
                        h = max(b[3] - b[1], o[3] - o[1])
                        cy_ok = abs((b[1] + b[3]) - (o[1] + o[3])) / 2 < 0.45 * h or (b[1] >= o[1] - 3 and b[3] <= o[3] + 3)
                        if cy_ok and b[0] <= o[2] + 0.9 * h and o[0] <= b[2] + 0.9 * h:
                            break
                    else:
                        w = max(b[2] - b[0], o[2] - o[0])
                        cx_ok = abs((b[0] + b[2]) - (o[0] + o[2])) / 2 < 0.45 * w or (b[0] >= o[0] - 3 and b[2] <= o[2] + 3)
                        if cx_ok and b[1] <= o[3] + 0.9 * w and o[1] <= b[3] + 0.9 * w:
                            break
                else:
                    out.append(b[:])
                    continue
                o[0], o[1], o[2], o[3] = min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])
                changed = True
            boxes = out
        return boxes
    hb = merge([g[:4] for g in glyphs], True)
    res = []
    singles = []
    for x0, y0, x1, y1 in hb:
        if (x1 - x0) >= 1.6 * (y1 - y0):
            res.append((x0 - pad, y0 - pad, x1 + pad, y1 + pad))
        else:
            singles.append([x0, y0, x1, y1])
    for x0, y0, x1, y1 in merge(singles, False):     # turned (vertical) words
        if (y1 - y0) >= 1.6 * (x1 - x0):
            res.append((x0 - pad, y0 - pad, x1 + pad, y1 + pad))
    return res


def show_boxes(img, boxes, out, scale=0.5):
    from PIL import Image, ImageDraw
    im = Image.open(img).convert('RGB')
    d = ImageDraw.Draw(im)
    for i, b in enumerate(boxes):
        d.rectangle(b, outline=(220, 0, 0), width=3)
        d.text((b[0], b[1] - 12), str(i), fill=(220, 0, 0))
    im.resize((int(im.width * scale), int(im.height * scale))).save(out)


def reuse(c, img, job_path, dx=0, dy=0, drop_text=()):
    """Draw another model's job onto this image, for a drawing that is the same picture moved by
    (dx, dy) px (this image = that one shifted: x_here = x_there + dx, y_here = y_there + dy).
    The job runs on a copy of this image padded back to the other's frame, so everything it
    traces comes from THIS picture; its output is shifted into place. <text> elements whose
    content contains any of `drop_text` are left out (labels the other model has and this
    one does not)."""
    import importlib.util, os, re, tempfile
    from PIL import Image
    im = Image.open(img).convert('RGB')
    pad = Image.new('RGB', (im.width - min(dx, 0) + max(dx, 0) * 0, im.height - min(dy, 0)), 'white')
    pad.paste(im, (-min(dx, 0), -min(dy, 0)))
    fn = os.path.join(tempfile.mkdtemp(), 'reuse.png')
    pad.save(fn)
    s = importlib.util.spec_from_file_location('reused_' + os.path.basename(job_path)[:-3], job_path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    c2 = B.new(fn)
    m.draw(c2, fn)
    parts = [p for p in c2.parts
             if not (p.startswith('<text') and any(t in re.sub('<[^>]+>', '', p) for t in drop_text))]
    c.add(f'<g transform="translate({min(dx, 0):g} {min(dy, 0):g})">')
    for p in parts:
        c.add(p)
    c.add('</g>')


def auto_text_drop(img, walls, skip=(), grow=0.7):
    """text_boxes() widened at both ends by `grow` x their height, to take in the thin glyphs
    (1, ', -) the finder skips. `skip` = rects; boxes centred inside one are left alone."""
    out = []
    for x0, y0, x1, y1 in text_boxes(img, walls):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if any(a <= cx <= c and b <= cy <= d for a, b, c, d in skip):
            continue
        h = min(x1 - x0, y1 - y0)
        if (x1 - x0) >= (y1 - y0):
            out.append((x0 - grow * h, y0 - 2, x1 + grow * h, y1 + 2))
        else:
            out.append((x0 - 2, y0 - grow * h, x1 + 2, y1 + grow * h))
    return out


def simple(c, img, k, after=None, before=None, drop=(), text_skip=(), win_drop=(), add=(), cut=(),
           auto_text=True, trace_kw=None):
    """A brochure drawing with no concrete bands: walls, windows, traced linework and hairlines,
    lettering erased (auto-found plus `drop`), then `before` (hand-drawn items, under the walls)
    and `after` (labels). k = the image's placement dpi (sets c.K and blib.K)."""
    B.K = c.K = k
    walls, wins = B.trace(img, win_drop=win_drop, add=add, cut=cut, **(trace_kw or {}))
    d = list(drop) + (auto_text_drop(img, walls, text_skip) if auto_text else [])
    nv, gr = B.lineart(img, walls, drop=d)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, d), B.NAVY)
    if before:
        before(c)
    B.draw_plan_walls(c, walls, wins)
    if after:
        after(c)
    return walls


def light_walls(img, drop=()):
    """Walls drawn with the lighter fill (206,209,212) some plans use for part of a floor (The
    Pioneer II's owner's suite); B.trace only reads the standard grey. Returns a shape to pass to
    B.trace(add=[...])."""
    a, grey, navy = B.load(img)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    light = (abs(r - 206) < 8) & (abs(g - 209) < 8) & (abs(b - 212) < 8)
    light = ndi.binary_opening(light, np.ones((3, 3), bool))
    m = ndi.binary_dilation(light, np.ones((9, 9), bool)) & (light | navy | (a.sum(-1) < 600))
    m &= ~B._rects_mask(light.shape, drop)
    m = ndi.binary_closing(m, np.ones((3, 3), bool))
    return B._vectorize(m)


def vlabel(c, x, y, name, size_txt=None, note=None, **kw):
    """Room label at the smaller size used on option drawings."""
    kw.setdefault('name_pt', 5.2)
    kw.setdefault('sub_pt', 4.3)
    B.label(c, x, y, name, size_txt, note, **kw)


def thin_walls(img, drop=(), grow=7, k=5):
    """Framed walls drawn thin (navy - narrow grey stripe - navy, about 8-10 px), which B.trace
    misses because its 3x3 opening erases a 2 px grey stripe (The Expressionist II's basement
    furring walls and columns). Any grey pixel, grown by `grow`, kept where it is ink, then
    opened by k x k so lettering and single lines drop out. Returns a shape for B.trace(add=...)."""
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    ink = grey | navy | (lum < 150)
    m = ndi.binary_dilation(grey, np.ones((grow, grow), bool)) & ink
    m = ndi.binary_opening(m, np.ones((k, k), bool))
    m &= ~B._rects_mask(grey.shape, drop)
    m = ndi.binary_closing(m, np.ones((3, 3), bool))
    return B._vectorize(m)


def reuse_k(c, img, job_path, k, dx=0, dy=0, drop_text=()):
    """reuse(), for a drawing that another brochure places at a different dpi: the other job's
    module constant K is replaced by `k` before it draws, so its line weights and lettering come
    out at this page's paper sizes (the drawing itself is the same picture, same px/ft)."""
    import importlib.util, os, re, tempfile
    from PIL import Image
    im = Image.open(img).convert('RGB')
    pad = Image.new('RGB', (im.width - min(dx, 0), im.height - min(dy, 0)), 'white')
    pad.paste(im, (-min(dx, 0), -min(dy, 0)))
    fn = os.path.join(tempfile.mkdtemp(), 'reuse.png')
    pad.save(fn)
    s = importlib.util.spec_from_file_location('reused_' + os.path.basename(job_path)[:-3], job_path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    m.K = k
    c2 = B.new(fn)
    c2.K = B.K = k
    m.draw(c2, fn)
    parts = [p for p in c2.parts
             if not (p.startswith('<text') and any(t in re.sub('<[^>]+>', '', p) for t in drop_text))]
    c.add(f'<g transform="translate({min(dx, 0):g} {min(dy, 0):g})">')
    for p in parts:
        c.add(p)
    c.add('</g>')
    B.K = c.K = k


# ---------------------------------------------------------------- listing-sheet plans (The Storyteller)
# The Storyteller's plans are listing-sheet drawings, not the brochure CAD style: walls are solid
# black bands, floors beige (baths teal), windows are thin framed white boxes set in the wall line,
# and fixtures are drawn white with black hairlines. These read that style.

def listing_wall_mask(img, k=7, drop=()):
    """Solid black wall bands (thin linework removed by an opening of k px)."""
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    blk = lum < 70
    W = ndi.binary_opening(blk, np.ones((k, k), bool))
    if drop:
        W &= ~B._rects_mask(blk.shape, drop)
    return W


def listing_windows(img, W, L=230, tmax=34, fill_min=0.8, drop=()):
    """Windows: gaps in a wall line (closed by a straight closing of length L) whose width is
    spanned by frame lines. Returns (window list for B.window_rot, mask of the window gaps)."""
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    dark = lum < 200
    out, gmask = [], np.zeros(W.shape, bool)
    dm = B._rects_mask(W.shape, drop) if drop else np.zeros(W.shape, bool)
    for horiz in (True, False):
        st = np.ones((1, L), bool) if horiz else np.ones((L, 1), bool)
        C = ndi.binary_closing(W, st) & ~W & ~dm
        lab, n = ndi.label(C)
        for i, sl in enumerate(ndi.find_objects(lab)):
            if sl is None:
                continue
            y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
            t, ln = (y1 - y0, x1 - x0) if horiz else (x1 - x0, y1 - y0)
            if not (6 <= t <= tmax) or ln < 18:
                continue
            blob = lab[sl] == i + 1
            d = dark[sl] & blob
            # every position along the gap must have frame ink across it (2+ dark pixels)
            cover = (d.sum(axis=0) >= 2) if horiz else (d.sum(axis=1) >= 2)
            if cover.mean() < fill_min or d.sum() > 0.6 * blob.sum():
                continue
            gmask[sl] |= blob
            cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
            out.append(((cx, cy), float(ln), float(t), 0.0 if horiz else 90.0))
    return out, gmask


def listing_trace(img, k=7, drop=(), add=(), cut=(), win_drop=(), L=230):
    """Walls (shapely, windows included as wall) and windows for a listing-sheet plan."""
    from shapely.geometry import box as sbox
    from shapely.ops import unary_union
    W = listing_wall_mask(img, k, drop)
    wins, gm = listing_windows(img, W, L=L, drop=win_drop)
    geom = B._vectorize(ndi.binary_closing(W | gm, np.ones((3, 3), bool)))
    extra = [sbox(*r) if isinstance(r, tuple) else r for r in add]
    if extra:
        geom = unary_union([geom] + extra)
    if cut:
        geom = geom.difference(unary_union([sbox(*r) for r in cut]))
    return geom, wins


def listing_lines(img, walls_geom, drop=(), dark=150):
    """Linework of a listing sheet: neutral dark pixels (door leaves and swings, counters, fixtures,
    stair treads) outside the walls; beige floors and teal bath floors are left out."""
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    sat = a.max(-1) - a.min(-1)
    m = (lum < dark) & (sat < 30)
    wm = np.zeros(m.shape, np.uint8)
    for p in getattr(walls_geom, 'geoms', [walls_geom]):
        if not p.is_empty:
            cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
            for h in p.interiors:
                cv2.fillPoly(wm, [np.array(h.coords, np.int32)], 0)
    m &= ~ndi.binary_dilation(wm.astype(bool), np.ones((5, 5), bool))
    if drop:
        m &= ~B._rects_mask(m.shape, drop)
    m = ndi.binary_dilation(m, np.ones((2, 2), bool))
    return B._contours_to_geom(m, eps=0.7, min_area=14)     # drops JPEG speckle on the teal floors


def listing_erase_text(img, rects, out=None, max_glyph=48, fill=(234, 234, 222), hard=()):
    """Copy of a listing-sheet raster with its lettering removed: every dark component whose box
    lies inside one of `rects` and is glyph-sized is painted over, so door swings and lines that
    pass through a label survive. `hard` rects are cleared outright (for lettering that touches a
    line; redraw that line by hand). Returns the new image path."""
    from PIL import Image
    a, grey, navy = B.load(img)
    lum = a.sum(-1) / 3.0
    sat = a.max(-1) - a.min(-1)
    dark = (lum < 120) & (sat < 44)          # glyph cores only: not the teal floors or their JPEG noise
    lab, n = ndi.label(dark, np.ones((3, 3), bool))
    b = a.copy()
    for i, sl in enumerate(ndi.find_objects(lab)):
        if sl is None:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if max(y1 - y0, x1 - x0) > max_glyph:
            continue
        if any(rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1 for rx0, ry0, rx1, ry1 in rects):
            m = ndi.binary_dilation(lab[sl] == i + 1, np.ones((5, 5), bool))
            b[sl][m] = fill
    # faint leftovers (apostrophes, antialiased edges) as small whole components
    faint = (b.sum(-1) / 3.0 < 175) & ((b.max(-1) - b.min(-1)) < 60)
    lab2, n2 = ndi.label(faint, np.ones((3, 3), bool))
    for i, sl in enumerate(ndi.find_objects(lab2)):
        if sl is None:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        comp = lab2[sl] == i + 1
        if max(y1 - y0, x1 - x0) > max_glyph or (b[sl][comp].sum(-1) / 3.0).mean() < 70:
            continue                     # too big, or solid black linework: not a glyph remnant
        if any(rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1 for rx0, ry0, rx1, ry1 in rects):
            b[sl][ndi.binary_dilation(comp, np.ones((3, 3), bool))] = fill
    for x0, y0, x1, y1 in hard:
        b[int(y0):int(y1), int(x0):int(x1)] = fill
    out = out or img[:-4] + '_notext.png'
    Image.fromarray(b.astype(np.uint8)).save(out)
    return out


def ray_box(walls, x, y, L=3000):
    """Nearest wall faces left, right, up and down of (x, y): (xl, xr, yu, yd)."""
    from shapely.geometry import LineString
    res = []
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        hit = LineString([(x, y), (x + dx * L, y + dy * L)]).intersection(walls)
        pts = []
        for g in getattr(hit, 'geoms', [hit]):
            if not g.is_empty and hasattr(g, 'coords'):
                pts += list(g.coords)
        if not pts:
            res.append(None)
            continue
        p = min(pts, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)
        res.append(p[0] if dx else p[1])
    return tuple(res)


def freestanding_tub(c, cx, cy, length_in=60, width_in=30, angle=0, drain_end=1, wall=None):
    """Freestanding tub (Kyle, October 31, 2026): a stadium-shaped outline with an inner basin and a
    drain dot, white-filled, navy lines. (cx, cy) is the tub's centre in image px; sizes in inches
    (B.PXFT). angle in degrees (0 = long side along x). drain_end = +1 / -1 picks which end the
    drain sits at."""
    import math
    k = B.PXFT / 12.0
    L, W = length_in * k, width_in * k
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def stadium(l, w, n=18):
        r = w / 2.0
        h = l / 2.0 - r
        pts = []
        for i in range(n + 1):                       # right cap
            t = -math.pi / 2 + math.pi * i / n
            pts.append((h + r * math.cos(t), r * math.sin(t)))
        for i in range(n + 1):                       # left cap
            t = math.pi / 2 + math.pi * i / n
            pts.append((-h + r * math.cos(t), r * math.sin(t)))
        return [(cx + u * ca - v * sa, cy + u * sa + v * ca) for u, v in pts]

    c.polyline(stadium(L, W), w=0.5, color=B.NAVY, fill='#ffffff', close=True, join='round')
    c.polyline(stadium(L - 5 * k, W - 5 * k), w=0.3, color=B.NAVY, close=True, join='round')
    du = drain_end * (L / 2.0 - W / 2.0)
    c.circle(cx + du * ca, cy + du * sa, 1.1 * k, sw=0.3, color=B.NAVY)
