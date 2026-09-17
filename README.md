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

Such a page usually also wants `crop: false`, which takes the image whole.
The automatic crop keeps the largest block of ink and drops everything else,
which is right for a brochure sheet and wrong for a photograph — and it would
strip the third-party disclaimer printed along the bottom of The Storyteller's
floor plans, which has to stay with the drawing it belongs to.

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
