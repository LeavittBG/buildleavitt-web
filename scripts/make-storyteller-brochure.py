"""Build The Storyteller's brochure in the October 2026 Leavitt brochure template.

The other sixteen brochures came to Leavitt ready-made; The Storyteller had only
three listing-sheet floor plans and a photograph. Every measurement, colour and
type size below is read off those brochures (The Visionary and The Craftsman): a
cover with the navy title band, the elevation, the caption, the three figures and
a highlights line, then one page per floor with the navy header band, the plan,
room dimensions, options and the disclaimer footer. The logos are taken from
The Visionary's brochure, so they are the same files.

The cover figures are what plans.test.js reads against src/plans.json, so change
them together. Room dimensions are read off the plan images.

Needs: pip install reportlab pikepdf pillow, and the Cinzel and Montserrat fonts:
  mkdir -p /tmp/fonts && cd /tmp/fonts && \
  npm pack @expo-google-fonts/cinzel @expo-google-fonts/montserrat && \
  mkdir cz ms && tar -xzf expo-google-fonts-cinzel-*.tgz -C cz && \
  tar -xzf expo-google-fonts-montserrat-*.tgz -C ms

Usage (then run `npm run plans`):
  python3 scripts/make-storyteller-brochure.py /tmp/fonts
"""
import sys, tempfile
from pathlib import Path
import pikepdf
from pikepdf import PdfImage
from PIL import Image, ImageChops
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets-src" / "plans"
F = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/fonts")
WORK = Path(tempfile.mkdtemp())
for name, path in {
    "Cinzel-Regular": "cz/package/400Regular/Cinzel_400Regular.ttf",
    "Cinzel-Medium": "cz/package/500Medium/Cinzel_500Medium.ttf",
    "Montserrat-Regular": "ms/package/400Regular/Montserrat_400Regular.ttf",
    "Montserrat-Medium": "ms/package/500Medium/Montserrat_500Medium.ttf",
    "Montserrat-SemiBold": "ms/package/600SemiBold/Montserrat_600SemiBold.ttf",
    "Montserrat-Italic": "ms/package/400Regular_Italic/Montserrat_400Regular_Italic.ttf",
    "Montserrat-SemiBoldItalic": "ms/package/600SemiBold_Italic/Montserrat_600SemiBold_Italic.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(F / path)))

def rgb(r, g, b): return Color(r, g, b)
NAVY = rgb(.05098, .105882, .164706)
GOLD = rgb(.768627, .654902, .482353)
CREAM = rgb(.929412, .901961, .854902)
DARKGOLD = rgb(.611765, .494118, .305882)
SUBGREY = rgb(.356863, .403922, .45098)
FEATGREY = rgb(.243137, .290196, .337255)
DIMGREY = rgb(.27451, .321569, .368627)
RULE = rgb(.913725, .882353, .827451)
DISCGREY = rgb(.4, .439216, .478431)
W, H = 612, 792

NAME = "THE STORYTELLER"
CAPTION = "FRONT ELEVATION — MODERN FARMHOUSE"
MATERIALS = "with Stone, Board & Batten, Shakes and Siding"
FIGURES = [("4", False, "BEDROOMS"), ("4.5", False, "BATHS"), ("2", True, "CAR GARAGE")]
HIGHLIGHTS = ["First-Floor In-Law Suite", "Home Office", "Second-Floor Family Room", "Second-Floor Laundry"]
X = "×"
PAGES = [
    ("FIRST FLOOR", 1, [
        ("Living Room", f"19'-7\" {X} 14'-8\""),
        ("Kitchen", f"27'-2\" {X} 17'-10\""),
        ("Breakfast Nook", f"21'-2\" {X} 9'-1\""),
        ("Dining Room", f"11'-7\" {X} 17'-10\""),
        ("Office", f"12'-6\" {X} 9'-9\""),
        ("Foyer", f"9'-4\" {X} 12'-0\""),
        ("In-Law Suite Bedroom", f"13'-7\" {X} 15'-5\""),
        ("Garage", f"17'-10\" {X} 24'-10\""),
    ], ["Optional 3 Car Garage"]),
    ("SECOND FLOOR", 2, [
        ("Primary Bedroom", f"18'-0\" {X} 27'-2\""),
        ("Bedroom 2", f"11'-7\" {X} 13'-1\""),
        ("Bedroom 3", f"10'-11\" {X} 10'-9\""),
        ("Bedroom 4", f"10'-11\" {X} 9'-9\""),
        ("Family Room", f"12'-6\" {X} 12'-0\""),
        ("Laundry", f"6'-9\" {X} 7'-9\""),
    ], []),
    ("BASEMENT", 3, [
        ("Basement", f"63'-6\" {X} 42'-7\""),
    ], ["Optional Full Bath"]),
]
DISCLAIMER = [
    "Due to our many optional features available to personalize your home, please phone our Sales Representative for",
    "complete information. It is recommended that the architectural blueprints be reviewed for further clarification of",
]

def spaced_width(text, font, size, cs):
    return pdfmetrics.stringWidth(text, font, size) + cs * len(text)

def text(c, x, y, s, font, size, color, cs=0):
    t = c.beginText(x, y); t.setFont(font, size); t.setCharSpace(cs); t.setFillColor(color)
    t.textOut(s); c.drawText(t)

def centered(c, cx, y, s, font, size, color, cs=0):
    # ReportLab's char spacing also follows the last glyph; leave it out of the centring
    w = spaced_width(s, font, size, cs) - cs
    text(c, cx - w / 2, y, s, font, size, color, cs)

def as_jpeg(im, max_w, name):
    """Embed images as JPEG files: handed a PIL image, ReportLab stores raw
    pixels, which made this brochure 16MB against about 2MB for the others."""
    if im.width > max_w:
        im = im.resize((max_w, round(max_w * im.height / im.width)), Image.LANCZOS)
    path = WORK / name
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    return str(path)

def trimmed(path):
    """The plan drawing without the listing photographer's notice printed in
    small type at the foot of each sheet, as the site's own crop always dropped
    it (README, "A model with no brochure"). The notice is the last block of ink
    rows; everything above it is the drawing, kept whole."""
    im = Image.open(path).convert("RGB")
    grey = im.convert("L")
    w, h = grey.size
    px = grey.load()
    inked = [sum(1 for x in range(0, w, 4) if px[x, y] < 200) > 3 for y in range(h)]
    blocks, start, gap = [], None, 0
    for y, ink in enumerate(inked + [False] * 40):
        if ink:
            if start is None: start = y
            gap = 0
        elif start is not None:
            gap += 1
            if gap > 30:
                blocks.append((start, y - gap)); start = None
    notice = blocks[-1]
    assert notice[1] - notice[0] < 0.05 * h and notice[0] > 0.85 * h, f"no notice found in {path}"
    top, bottom = blocks[0][0], blocks[-2][1]
    band = im.crop((0, top, w, bottom + 1))
    bg = Image.new("RGB", band.size, (255, 255, 255))
    box = ImageChops.difference(band, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    pad = 20
    return im.crop((max(0, box[0] - pad), max(0, top - pad), min(w, box[2] + pad), min(h, bottom + 1 + pad)))

def cover(c, photo):
    c.setFillColor(NAVY); c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.rect(18, 650, 576, 124, stroke=1, fill=1)
    c.saveState(); c.setStrokeAlpha(.55); c.setLineWidth(.5); c.rect(24, 656, 564, 112, stroke=1, fill=0); c.restoreState()
    centered(c, 306, 735, "LEAVITT BUILDING GROUP", "Montserrat-Medium", 8, CREAM, 1.12)
    size = 46
    while spaced_width(NAME, "Cinzel-Regular", size, 3.22) > 540: size -= 1
    centered(c, 306, 685.1, NAME, "Cinzel-Regular", size, GOLD, 3.22)
    c.setStrokeColor(GOLD); c.setLineWidth(.75); c.line(286, 667, 326, 667)

    im = Image.open(photo).convert("RGB")
    pw, ph = 528, 528 * im.height / im.width
    c.drawImage(as_jpeg(im, 2400, "cover.jpg"), 42, 326, pw, ph)

    centered(c, 306, 296, CAPTION, "Cinzel-Medium", 12.5, NAVY, 1.75)
    centered(c, 306, 280.4, MATERIALS, "Montserrat-Italic", 8.8, SUBGREY)
    for (fig, plus, label), cx in zip(FIGURES, (156, 306, 456)):
        nw = pdfmetrics.stringWidth(fig, "Cinzel-Regular", 30)
        gap, pw_ = 1.5, pdfmetrics.stringWidth("+", "Montserrat-Medium", 22)
        total = nw + (gap + pw_ if plus else 0)
        x0 = cx - total / 2
        text(c, x0, 229.9, fig, "Cinzel-Regular", 30, NAVY)
        if plus:
            text(c, x0 + nw + gap, 232.4, "+", "Montserrat-Medium", 22, DARKGOLD)
        centered(c, cx, 212.2, label, "Montserrat-SemiBold", 7, DARKGOLD, .84)
    c.setStrokeColor(GOLD); c.setLineWidth(.75)
    c.line(231, 252, 231, 210); c.line(381, 252, 381, 210)

    sep = "   •   "
    parts = []
    for i, h in enumerate(HIGHLIGHTS):
        if i: parts.append((sep, GOLD))
        parts.append((h, FEATGREY))
    total = sum(pdfmetrics.stringWidth(s, "Montserrat-Regular", 7.8) for s, _ in parts)
    x = 306 - total / 2
    for s, col in parts:
        text(c, x, 177.3, s, "Montserrat-Regular", 7.8, col)
        x += pdfmetrics.stringWidth(s, "Montserrat-Regular", 7.8)

    c.setFillColor(NAVY); c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.rect(18, 18, 576, 134, stroke=1, fill=1)
    c.saveState(); c.setStrokeAlpha(.55); c.setLineWidth(.5); c.rect(24, 24, 564, 122, stroke=1, fill=0); c.restoreState()
    c.drawImage(str(WORK / "logo-cover.png"), 190, 68.48794, 232, 55.51206, mask="auto")
    centered(c, 306, 44, "BUILDLEAVITT.COM", "Montserrat-Medium", 7.6, GOLD, .99)

def floor_page(c, title, plan, dims, options):
    c.setFillColor(NAVY); c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.rect(18, 718, 576, 56, stroke=1, fill=1)
    tw = spaced_width(title, "Cinzel-Regular", 12.5, 1.5) - 1.5
    text(c, 572 - tw, 741.5, title, "Cinzel-Regular", 12.5, CREAM, 1.5)
    text(c, 40, 739.3, NAME, "Cinzel-Regular", 19, GOLD, 1.52)

    im = trimmed(plan)
    bw, bh = 540, 440
    s = min(bw / im.width, bh / im.height)
    w, h = im.width * s, im.height * s
    c.drawImage(as_jpeg(im, 2600, title.lower().replace(" ", "-") + ".jpg"), 306 - w / 2, 260 + (bh - h) / 2, w, h)

    text(c, 36, 234.16, "ROOM DIMENSIONS", "Montserrat-SemiBold", 7, DARKGOLD, .84)
    c.setStrokeColor(GOLD); c.setLineWidth(.75); c.line(36, 227.2, 242, 227.2)
    y = 214.64
    for label, value in dims:
        text(c, 36, y, label, "Montserrat-Medium", 8.4, NAVY)
        vw = pdfmetrics.stringWidth(value, "Montserrat-Regular", 8.4)
        text(c, 242 - vw, y, value, "Montserrat-Regular", 8.4, DIMGREY)
        c.setStrokeColor(RULE); c.setLineWidth(.5); c.line(36, y - 5.19, 242, y - 5.19)
        y -= 17.5

    if options:
        text(c, 262, 234.16, "AVAILABLE OPTIONS", "Montserrat-SemiBold", 7, DARKGOLD, .84)
        c.setStrokeColor(GOLD); c.setLineWidth(.75); c.line(262, 227.2, 576, 227.2)
        y = 213.45
        for o in options:
            text(c, 262, y, "•", "Montserrat-Regular", 7.2, GOLD)
            text(c, 270, y, o, "Montserrat-Regular", 7.2, DIMGREY)
            y -= 9.6

    c.setStrokeColor(GOLD); c.setLineWidth(.75); c.line(36, 65, 576, 65)
    c.drawImage(str(WORK / "logo-page.png"), 36, 26.12198, 116, 27.75603, mask="auto")
    y = 30.46 + 19.24
    for line in DISCLAIMER:
        text(c, 172, y, line, "Montserrat-Regular", 5.9, DISCGREY); y -= 8.38
    text(c, 172, y, "features. ", "Montserrat-Regular", 5.9, DISCGREY)
    text(c, 172 + pdfmetrics.stringWidth("features. ", "Montserrat-Regular", 5.9), y,
         "This Brochure is for illustrative purposes only and not part of a legal contract.",
         "Montserrat-SemiBoldItalic", 5.9, DISCGREY)
    c.drawImage(str(WORK / "eho.png"), 552.5625, 28, 23.4375, 25, mask="auto")

def extract_logos():
    """The two Leavitt logos and the Equal Housing mark, from The Visionary."""
    pdf = pikepdf.open(SRC / "the-visionary.pdf")
    for page, wanted in ((0, {2984: "logo-cover.png"}), (1, {2984: "logo-page.png", 480: "eho.png"})):
        for _, x in pdf.pages[page].Resources.XObject.items():
            name = wanted.get(int(x.Width))
            if not name: continue
            im = PdfImage(x).as_pil_image().convert("RGB")
            if "/SMask" in x: im.putalpha(PdfImage(x.SMask).as_pil_image())
            im.save(WORK / name)

def main():
    extract_logos()
    out = SRC / "the-storyteller.pdf"
    plans = {1: SRC / "the-storyteller-first.jpg", 2: SRC / "the-storyteller-second.jpg",
             3: SRC / "the-storyteller-basement.jpg"}
    c = canvas.Canvas(str(out), pagesize=(W, H))
    c.setTitle("The Storyteller | Leavitt Building Group"); c.setAuthor("Leavitt Building Group")
    cover(c, SRC / "the-storyteller-photo.jpg"); c.showPage()
    for title, key, dims, options in PAGES:
        floor_page(c, title, plans[key], dims, options); c.showPage()
    c.save()
    print("wrote", out.relative_to(ROOT))

main()
