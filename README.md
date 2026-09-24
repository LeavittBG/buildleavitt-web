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
breaking onto the wrong lines, italic letters clipped at the edge, words not
painting on one Windows machine, the site rendering in the wrong typeface,
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
which git ignores. `tests/` is removed from the Netlify deploy, the same as
`assets-src/`.

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

Playfair Display has no weight below 400, so a `font-light` heading cannot get
a lighter italic; `src/styles.css` pins those spans to 400 so the stylesheet
asks for what it actually receives.

## Images

Full-resolution originals live in `assets-src/`. They are inputs only —
`netlify.toml` deletes that directory during deploy so the originals are never
served. Everything the site actually loads is generated from them and committed.

```
npm run images     # resize + WebP the photography in assets-src/
```

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

Models appear at `/plans/` in the order they are listed in `src/plans.json` —
currently alphabetical by the name after "The".

### Adding a model

1. Put the brochure at `assets-src/plans/<slug>.pdf` (lowercase, hyphenated —
   `the-visionary.pdf`). The slug becomes the page URL.
2. Run `npm run plans:scaffold`. It reads the PDF's built-in outline (the page
   list Acrobat shows in the sidebar: "The Poet-Foundation", "The Poet-First
   Floor") and prints a ready-made entry to paste into `src/plans.json`.
3. Fill in the one thing the outline does not contain: the caption printed under
   the front elevation, marked `TODO` in the scaffolded entry. **Read it off the
   rendered page.** Do not trust text extracted from the PDF — these brochures
   carry leftover hidden layers, so `pdftotext` reports sheet names that are not
   the ones actually printed. The `_README` in `src/plans.json` has the details.
4. Run `npm run plans`, then `npm run build`, then open `plans/index.html` and
   the new model page and check the drawings look right. If a page is cropped
   badly, give it a `band` override — see `src/plans.json`.
5. Commit the generated `plans/` files along with your edit. Netlify does not
   run these scripts.

If a PDF has no outline, the scaffold says so and that model has to be filled in
by hand, reading each page off the render.

### A model with no brochure

A model can supply its pages as image files instead of a PDF: put `image` on each
page in `src/plans.json`, relative to `assets-src/`. The Storyteller works this
way — it is a house that has actually been built, so its "elevation" is the
photograph from the home page and its floor plans came as separate images.

A photograph also wants `crop: false`, which takes the image whole — the
automatic crop keeps the largest block of ink and drops everything else, which
is right for a sheet and wrong for a photograph. Plan images coming from a
listing sheet should be left to crop normally: that strips the photographer's
footer along with the rest of the furniture.

The download button changes to "See it built", linking to the photographs,
since there is no brochure to offer.

### Specs

Specs live in `src/plans.json` and come from Leavitt's own figures. The pages
render "On request" wherever a value is missing. Fill anything in only from real
numbers — a wrong square footage on a builder's website is a problem, and a
blank is not. A test fails the build if a page ever shows a square footage that
is not the one in the data.

`sqft` is living square footage. `sqftFrom: true` means Leavitt's sheet said
"starting at", and the page renders "From 2,626" rather than a flat figure;
two models are exact and have it `false`. Keep that distinction — it is the
difference between a starting price and a promise.

`price` works the same way, with `priceFrom`. Leavitt's note on the price sheet —
*"starting at means without additional options"* — is not decoration:
`build-plans.mjs` prints it beside every price on the site, and it has to keep
travelling with them. `pricesAsOf` dates the list and is printed with it. A test
fails if any dollar figure on a page is not the one in the data, or if the
qualifier goes missing.

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

## Forms

The contact form is a Netlify form. Netlify detects the fields from the
deployed HTML, so every field it should record has to exist in `index.html` —
including `Plan`, the hidden field that records which plan page a visitor came
from. Submissions appear under Forms in the Netlify dashboard.
