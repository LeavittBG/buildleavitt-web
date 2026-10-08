# buildleavitt-web

The marketing site for Leavitt Building Group. Hand-written HTML, Tailwind for
styling, deployed by Netlify from `main`.

## Running the build

```
npm install
npm run build      # compiles src/styles.css -> dist/styles.css
npm run dev        # same, but rebuilds as you edit
```

`dist/styles.css` is committed, and Netlify also rebuilds it on deploy
(`netlify.toml`). Tailwind only keeps the classes it can find in the files
listed under `content` in `tailwind.config.js` — currently `./*.html` and
`./plans/*.html`. A class that appears nowhere in those files is deleted from
the stylesheet, so if something loses its styling, that list is the first place
to look.

## Tests

```
npx playwright install chromium   # once per machine
npm test                          # everything, ~3 minutes
npm test -- hero                  # only files with "hero" in the name
node tests/hero-wrap.test.js      # any one file on its own
```

Each file in `tests/` loads the real pages in a headless Chrome and checks
something that has actually gone wrong on this site before — the headline
breaking onto the wrong lines, words not painting on one Windows machine,
content left hidden when a script failed, the site rendering in the wrong typeface,
prices or square footage drifting from Leavitt's figures. The comment at the
top of each file says what it guards against and why. Run `npm test` before
merging anything that touches the markup, the stylesheet or the plans data.

The tests serve the real web fonts from `tests/fixtures/fonts/` rather than
fetching them, because text width decides several of the layout checks. If
you change the Google Fonts URL in the pages, run `npm run test:fonts` to
refresh that copy.

One check in `plans.test.js` reads the brochure PDFs with `pdftotext`
(`brew install poppler` on a Mac). Without it that check is skipped and says
so; the rest still run.

Screenshots the tests leave for a person to look at go to `tests/.output/`,
which git ignores. `tests/` is removed from the Netlify deploy, along with
every other file that is not part of the site - see the comment in
`netlify.toml`.

GitHub runs the whole suite on every pull request
(`.github/workflows/test.yml`) and shows the result as a check named **test**
on the PR. If it fails, the screenshots are attached to the run under
Artifacts. To make a failing run block the merge button:

1. On GitHub, open the repository → **Settings** → **Branches**
2. **Add branch protection rule** (or **Add classic branch protection rule**)
3. Branch name pattern: `main`
4. Tick **Require status checks to pass before merging**, search for `test`
   and select it
5. **Create**

## Fonts

Inter and Playfair Display are declared in `tailwind.config.js` under
`theme.extend.fontFamily`, not as plain CSS rules. That is deliberate: every
`<body>` carries Tailwind's `font-sans` class, and a class outranks a
`body { font-family: ... }` rule whatever order they appear in — so a rule
written in `src/styles.css` is silently ignored and the site renders in the
visitor's system font instead. Setting the theme makes `font-sans` and
`font-serif` mean these two faces, and sets Tailwind's own `html` default too.

The weights requested from Google Fonts have to cover every weight the markup
uses. `font-medium` is 500 and is used heavily; it was missing from the URL for
a while, and because Google serves these as discrete files rather than one
variable font, the browser silently rendered those elements at 400. If you
start using a new weight class, add it to the font URL — which appears in every
page's `<head>` **and** in `scripts/build-plans.mjs`, so the generated plan
pages get it too. Keep them identical.

Headings are set in one upright face throughout. They used to switch to
Playfair Display italic for their last words ("Building legacies, *not just
homes.*"), a stock template flourish that was taken out; the italic font is no
longer downloaded at all. `markup.test.js` fails if an italic serif span comes
back.

## Images

Full-resolution originals live in `assets-src/`. They are inputs only —
`netlify.toml` deletes that directory during deploy so the originals are never
served. Everything the site actually loads is generated from them and committed.

```
npm run images     # resize + WebP the photography in assets-src/
```

## Icons

The icons are inline SVG in the page, not a script. They came from
[Lucide](https://lucide.dev) (ISC License), which the site used to load at
runtime as `lucide@latest` — 444 KB of JavaScript for 17 icons, and whenever
Lucide changed, so did the site. Lucide 1.0 dropped its Facebook and Instagram
icons and every one of them on the site silently went blank; those two now come
from Lucide 0.577.0, the last release that had them.

To add an icon, open it on lucide.dev, **Copy SVG**, paste it in place and give
it the size classes it needs (`class="w-5 h-5"`). Keep `aria-hidden="true"` on
it when it sits beside text; a link or button that contains *only* an icon needs
an `aria-label` saying where it goes. `markup.test.js` fails any link or button
without a name, on every page.

The three service-card icons in "Built for your lifestyle." are the exception:
they were drawn for this site in October 2026, after the stock house, ruler and
hammer read as a template. They show a house drawn in three dimensions with a
dimension line, a floor plan with its doors swinging, and a house with an
addition sketched in dashes. Each is navy line work with gold for the
architect's marks, and sits straight on the page with no tile behind it. Each
viewBox is cropped to its drawing so the three share a baseline and line up
with their headings. Each `stroke-width` is set so every line renders at 1.8px,
however far that drawing is scaled. `markup.test.js` fails if a tile or any
other colour comes back.

## Not-found page

`404.html` is what Netlify shows, with a 404 status, for any address that has
no page behind it. It is served *at* the broken address, so every link and
asset in it must start with `/` — a relative `dist/styles.css` would load from
`/plans/dist/styles.css` when the broken address is under `/plans/`, and the
page would arrive unstyled. `not-found.test.js` requests it at several depths.
It carries `noindex` and is not in the sitemap.

## Home plans

The pages under `/plans/` are generated from data, not edited by hand.

```
npm run plans      # both steps below, in order
npm run plans:images   # PDFs  -> plans/img/*.{webp,png} + plans/pdf/*.pdf
npm run plans:build    # data  -> plans/index.html, plans/<slug>.html, sitemap.xml
```

`plans:build` also writes `sitemap.xml` and `robots.txt`. If you add a new
top-level page to the site, add it to the `STATIC` list in
`scripts/build-plans.mjs` so it ends up in the sitemap.

Each sitemap entry carries `<lastmod>`: the date of the last git commit that
changed that page, or today if the page has uncommitted changes. Google only
uses `lastmod` while it stays accurate, so it is never simply the build date.
Because the date comes from git, re-run `npm run plans:build` after editing a
page by hand, before committing, so the sitemap picks up the change.

Every plan page's meta description — the text under its title in Google — is
built from the specs by `snippet()` in `build-plans.mjs` and held to 155
characters by `plans.test.js`, since Google cuts off anything longer. Each page
also names its front elevation as the image shown when it is shared.

Models appear at `/plans/` in the order they are listed in `src/plans.json` —
currently alphabetical by the name after "The".

### Adding a model

1. Put the brochure at `assets-src/plans/<slug>.pdf` (lowercase, hyphenated —
   `the-visionary.pdf`). The slug becomes the page URL.
2. Run `npm run plans:scaffold`. It reads the brochure the way the site does —
   the elevation caption from the cover, and each later page's title from its
   header band ("FIRST FLOOR", "BASEMENT OPTIONS") — and prints a ready-made
   entry to paste into `src/plans.json`, pages in the brochure's own order.
3. Fill in the specs from Leavitt's own figures (never from the brochure), and
   check every label against the rendered pages. `plans.test.js` fails if a
   label does not match its page's printed title, or a page is left out.
4. Run `npm run plans`, then `npm run build`, then open `plans/index.html` and
   the new model page and check the drawings look right. Every brochure page is
   cut to the bands in `brochureBands` (`src/plans.json`) — the elevation on the
   cover, the body of every other page — so a brochure in a different layout
   needs those checked, or a `band` override on the page.
5. Commit the generated `plans/` files along with your edit. Netlify does not
   run these scripts.

This works for the brochure template Leavitt adopted in October 2026. The
brochures before it carried hidden leftover text layers, so their titles had to
be read through the PDF's outline or off the rendered page; anything in the old
layout has to be filled in by hand.

### A model with no brochure

A model can supply its pages as image files instead of a PDF: put `image` on each
page in `src/plans.json`, relative to `assets-src/`. With no elevation, its card
and link preview show its first-floor plan instead (`coverOf()` in
`build-plans.mjs`). No model works this way now.

A photograph wants `crop: false`, which takes the image whole — the automatic
crop keeps the largest block of ink and drops everything else, which is right
for a sheet and wrong for a photograph. Plan images coming from a listing sheet
should be left to crop normally: that strips the photographer's footer along
with the rest of the furniture.

With no brochure there is no download button.

### The Storyteller's brochure

The Storyteller worked that way until October 2026: its floor plans came as
separate images from a listing sheet, and it had no brochure. Its elevation had
been a photograph of the finished house, and six more photographs of it made up
the home page gallery; they came off the site in September 2026 on Leavitt's
realtor's advice, because it was the only home shown built, which read as though
it were the only one.

Once every other plan showed a photo rendering, Leavitt had a front photograph of
The Storyteller restyled to match them — the house as photographed, with the
sky, trees, light and lawn of the renderings and the house number removed — and
`scripts/make-storyteller-brochure.py` set it, with the three listing-sheet
plans, in the same brochure template as the other sixteen (`assets-src/plans/`
keeps the photo and the plan images it was built from). Its room dimensions are
read off those plans, and the photographer's notice under each plan is cropped
off, as the site always did. Since then it is a brochure model like any other.

### Specs

Specs live in `src/plans.json` and come from Leavitt's own figures. The pages
render "On request" wherever a value is missing. Fill anything in only from real
numbers — a wrong square footage on a builder's website is a problem, and a
blank is not. A test fails the build if a page ever shows a square footage that
is not the one in the data.

Bedrooms, baths and garage are copied from the figures printed on each
brochure's cover ("4+ bedrooms, 2.5+ baths, 2+ car garage"). They used to be the
price sheet's ranges, which disagreed with the brochure a visitor could download
from the same page, so a test now reads every cover and fails if a page shows
anything else. Square footage and price are not on the covers and still come
from the price sheet.

`sqft` is living square footage. `sqftFrom: true` means Leavitt's sheet said
"starting at", and the page renders "From 2,626" rather than a flat figure;
two models are exact and have it `false`. Keep that distinction — it is the
difference between a starting price and a promise.

`price` works the same way, with `priceFrom`. The qualifier printed beside it —
*"Starting price is for the home with all standard features included, and does
not include the homesite"* — is not decoration: `build-plans.mjs` prints it
beside every price on the site, and it has to keep travelling with them. It used
to say "without any optional features added", after Leavitt's price sheet; the
realtor pointed out that made the house sound bare when the Leavitt Standard
already includes so much, so it now says what is included and links to that
list. `pricesAsOf` dates the list and is printed with it. A test fails if any
dollar figure on a page is not the one in the data, or if the qualifier goes
missing.

`sqftNote`, `bathsNote` and `priceNote` print a qualifying line under a figure,
for cases one number cannot carry honestly — The Storyteller gains 70 sq ft with
the three-car garage, and has an optional basement full bath on top of its 4.5.

### The Leavitt Standard

The "what's included in every home" list at `/plans/#included` is built from the
`STANDARD` array in `scripts/build-plans.mjs`, not from a PDF, so it is
searchable and readable on a phone. The printable sheet lives at
`assets-src/leavitt-standard.pdf` and is copied to `plans/pdf/` by
`npm run plans:images`; the section links to it. Edit the array and the PDF
together so they do not drift.

The three cards in the "Home plans" section of `index.html` are hand-written and
point at three specific models. If you rename or remove one of those, update that
section too. Their `width`/`height` attributes are not hand-maintained —
`npm run plans:build` rewrites them from the generated images, so a changed crop
cannot leave them stale.

## Business details

The address, phone number and opening hours are in the footer of every page,
and again in the homepage's structured data (the `application/ld+json` block
in `index.html`), which is what Google reads alongside the Business Profile.
The plan pages get their footer from `scripts/build-plans.mjs`. If any of these
change, change them in all of those places; `markup.test.js` fails if the hours
on any page stop matching the structured data. Saturday is by appointment,
which the structured data has no way to say, so it lists Monday–Friday only.

## Forms

The contact form is a Netlify form. Netlify detects the fields from the
deployed HTML, so every field it should record has to exist in `index.html` —
including `Plan`, the hidden field that records which plan page a visitor came
from. Submissions appear under Forms in the Netlify dashboard.
