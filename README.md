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

### Specs

`beds`, `baths`, `sqft` and `garage` are `null` for every model because the
brochures do not state them. The pages render "On request" wherever a value is
missing. Fill them in only from real numbers — a wrong square footage on a
builder's website is a problem, and a blank is not.

The three cards in the "Home plans" section of `index.html` are hand-written
and point at three specific models. If you rename or remove one of those, update
that section too.

## Forms

The contact form is a Netlify form. Netlify detects the fields from the
deployed HTML, so every field it should record has to exist in `index.html` —
including `Plan`, the hidden field that records which plan page a visitor came
from. Submissions appear under Forms in the Netlify dashboard.
