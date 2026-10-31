"""Add the alternate-exterior pages to the Leavitt brochures.

Every brochure's cover shows its plan as a Modern Farmhouse. In October 2026
Kyle added a second exterior to every plan, Modern Brick (charcoal brick, white
lap siding, black windows, stained wood doors), after being told that a buyer
who does not care for farmhouse style should see something else. Each one is a
photo rendering made from that plan's own cover rendering (Artlist, Nano Banana
2.1 image-to-image), keeping the house - roof lines, gables, every window, door,
porch and garage door - and changing only the finishes. The renderings are kept
in assets-src/plans/<slug>-modern-brick.jpg.

This script gives each one a page of its own at the end of the brochure, after
the floor plans, in the October 2026 template: the navy header band with the
model's name and the page title, the rendering at the cover's width, a caption
in the cover's style, one line saying what it is, and the logo and disclaimer
footer. The template's measurements, colours and type are the ones
make-storyteller-brochure.py read off The Visionary and The Craftsman.

The pages to add come from src/plans.json: any page whose id starts with
"elevation-" and names an `image`. Its `label` is the title printed in the
header band (plans.test.js reads it back), and its `page` is where it goes. A
page this script added before is replaced, not added twice, so it is safe to
run again - for instance after a brochure's floor plans have been redrawn and
the PDF replaced. Run it for every brochure, or name the slugs to do.

Needs: pip install reportlab pikepdf pillow, and the Cinzel and Montserrat fonts:
  mkdir -p /tmp/fonts && cd /tmp/fonts && \
  npm pack @expo-google-fonts/cinzel @expo-google-fonts/montserrat && \
  mkdir cz ms && tar -xzf expo-google-fonts-cinzel-*.tgz -C cz && \
  tar -xzf expo-google-fonts-montserrat-*.tgz -C ms

Usage (then run `npm run plans`):
  python3 scripts/add-elevation-pages.py [--fonts /tmp/fonts] [slug ...]
"""
import json, sys, tempfile
from pathlib import Path
import pikepdf
from pikepdf import Name, PdfImage
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets-src"
args = sys.argv[1:]
F = Path("/tmp/fonts")
if "--fonts" in args:
    i = args.index("--fonts")
    F = Path(args[i + 1])
    del args[i:i + 2]
ONLY = set(args)
WORK = Path(tempfile.mkdtemp())

for name, path in {
    "Cinzel-Regular": "cz/package/400Regular/Cinzel_400Regular.ttf",
    "Cinzel-Medium": "cz/package/500Medium/Cinzel_500Medium.ttf",
    "Montserrat-Regular": "ms/package/400Regular/Montserrat_400Regular.ttf",
    "Montserrat-Italic": "ms/package/400Regular_Italic/Montserrat_400Regular_Italic.ttf",
    "Montserrat-SemiBoldItalic": "ms/package/600SemiBold_Italic/Montserrat_600SemiBold_Italic.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(F / path)))

def rgb(r, g, b): return Color(r, g, b)
NAVY = rgb(.05098, .105882, .164706)
GOLD = rgb(.768627, .654902, .482353)
CREAM = rgb(.929412, .901961, .854902)
SUBGREY = rgb(.356863, .403922, .45098)
DIMGREY = rgb(.27451, .321569, .368627)
DISCGREY = rgb(.4, .439216, .478431)
W, H = 612, 792

# What each alternate exterior's page says under the rendering, by page id.
# The caption follows the cover's two lines (style, then "with" materials).
STYLES = {
    "elevation-modern-brick": (
        "MODERN BRICK",
        "with Charcoal Brick and Lap Siding",
        ["The same floor plan as the Modern Farmhouse elevation on the cover, finished in",
         "charcoal brick and white lap siding, with black windows and stained wood doors."],
    ),
}

DISCLAIMER = [
    "Due to our many optional features available to personalize your home, please phone our Sales Representative for",
    "complete information. It is recommended that the architectural blueprints be reviewed for further clarification of",
]
MARK = Name("/LBGElevationPage")   # set on every page this script makes, so a re-run replaces it


def spaced_width(text, font, size, cs):
    return pdfmetrics.stringWidth(text, font, size) + cs * len(text)


def text(c, x, y, s, font, size, color, cs=0):
    t = c.beginText(x, y); t.setFont(font, size); t.setCharSpace(cs); t.setFillColor(color)
    t.textOut(s); c.drawText(t)


def centered(c, cx, y, s, font, size, color, cs=0):
    # ReportLab's char spacing also follows the last glyph; leave it out of the centring
    w = spaced_width(s, font, size, cs) - cs
    text(c, cx - w / 2, y, s, font, size, color, cs)


def extract_logos():
    """The page logo and the Equal Housing mark, from The Visionary, so they are
    the same files every other brochure page carries."""
    pdf = pikepdf.open(SRC / "plans" / "the-visionary.pdf")
    wanted = {2984: "logo-page.png", 480: "eho.png"}
    for _, x in pdf.pages[1].Resources.XObject.items():
        name = wanted.get(int(x.Width))
        if not name:
            continue
        im = PdfImage(x).as_pil_image().convert("RGB")
        if "/SMask" in x:
            im.putalpha(PdfImage(x.SMask).as_pil_image())
        im.save(WORK / name)


def make_page(model, page, out):
    caption, materials, lines = STYLES[page["id"]]
    title = page["label"].upper()
    name = model["name"].upper()
    c = canvas.Canvas(str(out), pagesize=(W, H))

    # header band, as on every page after the cover
    c.setFillColor(NAVY); c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.rect(18, 718, 576, 56, stroke=1, fill=1)
    tw = spaced_width(title, "Cinzel-Regular", 12.5, 1.5) - 1.5
    text(c, 572 - tw, 741.5, title, "Cinzel-Regular", 12.5, CREAM, 1.5)
    size = 19
    while 40 + spaced_width(name, "Cinzel-Regular", size, 1.52) > 572 - tw - 24:
        size -= 0.5
    text(c, 40, 739.3, name, "Cinzel-Regular", size, GOLD, 1.52)

    # the rendering, at the cover's width and left edge
    im = Image.open(SRC / page["image"]).convert("RGB")
    # 2000px across 528pt is 270 dpi, plenty for print, and keeps each page
    # to about half a megabyte
    if im.width > 2000:
        im = im.resize((2000, round(2000 * im.height / im.width)), Image.LANCZOS)
    jpg = WORK / f"{model['slug']}-{page['id']}.jpg"
    im.save(jpg, "JPEG", quality=85, optimize=True, progressive=True)
    pw, ph = 528, 528 * im.height / im.width
    top = 588
    c.drawImage(str(jpg), 42, top - ph, pw, ph)

    y = top - ph - 30
    centered(c, 306, y, caption, "Cinzel-Medium", 12.5, NAVY, 1.75)
    centered(c, 306, y - 15.6, materials, "Montserrat-Italic", 8.8, SUBGREY)
    c.setStrokeColor(GOLD); c.setLineWidth(.75); c.line(286, y - 30, 326, y - 30)
    for i, line in enumerate(lines):
        centered(c, 306, y - 48 - 12 * i, line, "Montserrat-Regular", 8.4, DIMGREY)

    # footer, as on every page after the cover
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
    c.showPage()
    c.save()


def main():
    extract_logos()
    data = json.loads((ROOT / "src" / "plans.json").read_text())
    done = 0
    for model in data["models"]:
        if ONLY and model["slug"] not in ONLY:
            continue
        extra = [p for p in model["pages"] if p["id"].startswith("elevation-") and p.get("image")]
        if not extra:
            continue
        path = SRC / "plans" / f"{model['slug']}.pdf"
        pdf = pikepdf.open(path, allow_overwriting_input=True)
        for i in reversed(range(len(pdf.pages))):
            if MARK in pdf.pages[i].obj:
                del pdf.pages[i]
        for page in sorted(extra, key=lambda p: p["page"]):
            out = WORK / f"{model['slug']}-{page['id']}.pdf"
            make_page(model, page, out)
            new = pikepdf.open(out)
            at = page["page"] - 1
            if at > len(pdf.pages):
                sys.exit(f"{model['slug']}: {page['id']} is page {page['page']}, "
                         f"but the brochure only has {len(pdf.pages)} pages before it")
            pdf.pages.insert(at, new.pages[0])
            pdf.pages[at].obj[MARK] = pikepdf.String(page["id"])
        pdf.save(path)
        print(f"{model['slug']}: {', '.join(p['label'] for p in extra)} -> {len(pdf.pages)} pages")
        done += 1
    print(f"{done} brochure(s) updated")


main()
