# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Marketing site for Leavitt Building Group, a custom home builder in Forest Hill, MD. Static hand-written HTML plus a Tailwind stylesheet, deployed by Netlify from `main`. README.md has the full background; this file is the working summary.

## Commands

```
npm install
npm run build              # src/styles.css -> dist/styles.css (Tailwind, minified)
npm run dev                # same, watching
npm test                   # every tests/*.test.js in headless Chromium, ~4 min
npm test -- hero           # only test files whose name contains "hero"
node tests/layout.test.js  # one file on its own (each test is a plain script)
npm run plans              # plans:images (PDFs -> plans/img, plans/pdf) then plans:build
npm run plans:build        # src/plans.json -> plans/*.html, sitemap.xml, robots.txt
npm run plans:scaffold     # print a src/plans.json entry from a new brochure PDF's outline
npm run images             # resize + WebP the photos in assets-src/
npm run test:fonts         # refresh tests/fixtures/fonts after changing the Google Fonts URL
```

There is no linter. The test suite is the gate: GitHub Actions (`.github/workflows/test.yml`) runs `npm run build && npm test` on every PR as the check named **test**. Test screenshots land in `tests/.output/` (gitignored) and are attached to failed CI runs.

The plan scripts need poppler (`pdftoppm`, `pdfinfo`, `pdftohtml`). One check in `plans.test.js` uses `pdftotext` and is skipped with a notice if it's missing.

## How the site is put together

- **Pages:** `index.html` (the homepage, with all its JS inline at the bottom), `privacy.html`, `terms.html`, `success.html` (form thank-you, noindex), `404.html`. Everything under `plans/` is **generated** by `scripts/build-plans.mjs` from `src/plans.json`. Never hand-edit `plans/*.html`; change the data or the script and re-run `npm run plans:build`.
- **Committed build outputs:** `dist/styles.css`, `plans/*`, `sitemap.xml`, `robots.txt` and the resized `*.webp`/`*.jpg` in the root are all committed. Netlify only runs `npm run build`, not the image or plan scripts, and then deletes every non-site file from the deploy (`assets-src/`, `tests/`, `src/`, `scripts/`, `package*.json`, `tailwind.config.js`, `README.md`, `CLAUDE.md`). A new top-level file that is not part of the site belongs on that list in `netlify.toml`, which `markup.test.js` checks. After changing markup, rebuild the CSS. After changing plan data or a page by hand, run `npm run plans:build` before committing: it rewrites the plan pages and the sitemap `<lastmod>` dates, which come from git.
- **Tailwind purges** any class it can't find in `./*.html` or `./plans/*.html` (`tailwind.config.js` `content`). A class used only in JS elsewhere, or only in a new file outside those globs, silently loses its styling. Scratch HTML files left in the repo root get scanned too, so keep mockups out of the root or delete them before building.
- **Fonts:** Inter and Playfair Display are set in `tailwind.config.js` `theme.extend.fontFamily`, not with a CSS `body` rule. The `font-sans` class on `<body>` would override such a rule. The Google Fonts URL must list every weight the markup uses (500 is needed for `font-medium`). It appears in every page's `<head>` and in `build-plans.mjs`; keep them identical.
- **Icons** are inline SVG copied from Lucide, not a script. Icon-only links and buttons need an `aria-label`; `markup.test.js` fails any unnamed link or button on any page.
- **404.html** is served by Netlify at the broken address, at any depth. Every asset and link in it must be root-absolute (`/dist/styles.css`).
- **`netlify.toml`** keeps `pretty_urls = false`, so published links match the canonical tags and sitemap. A test checks it.
- **Contact form** is a Netlify form. Every field it records, including the hidden `Plan` field, must exist in the deployed `index.html`.

## Homepage specifics

- **Hero** (`#hero`): one block of markup, two layouts. From `lg` up the photo fills the screen behind the copy. Below `lg` the photo is a banner above the copy. `layout.test.js` checks both at six sizes, including that "What We Build" is on the first screen.
- **Headline animation:** `<head>` adds a `js-anim` class before first paint. That class is the only thing that hides the words for the slide-up reveal, and CSS failsafe animations bring the words back if the script never runs. Don't put `will-change` on the headline: it left words blank on a Windows Chrome machine (`hero-layers.test.js`).
- **Business facts must stay consistent** across the footer on every page, the JSON-LD in `index.html` and the plan-page footer in `build-plans.mjs`. These are the address, phone (866) 832-6524, and opening hours (Mon–Fri 8–5, Saturday by appointment, closed Sunday). `markup.test.js` enforces that the hours match the JSON-LD. The Facebook link is `https://www.facebook.com/profile.php?id=61591583276647` in all three places, also enforced.

## Plans data rules (`src/plans.json`)

Specs, prices and square footage come only from Leavitt's own figures, never estimates. A missing value renders "On request". `sqftFrom`/`priceFrom` mean "starting at", and the "starting at means without additional options" qualifier must travel with every price. `plans.test.js` fails if any figure on a page differs from the data or the qualifier goes missing. Elevation captions must be read off the rendered page, not from `pdftotext`, because the brochures carry hidden text layers. The `_README` inside `src/plans.json` and the README's "Home plans" section have the full workflow for adding a model.

## Tests

- **Shared helpers** live in `tests/lib/`:
  - `env.js`: `ROOT`, `FILE_ROOT`, `launch()` and `serveRepo()`. `launch()` uses `CHROMIUM_PATH` or `/opt/pw-browsers/chromium` when present. `serveRepo()` is an HTTP server that mimics Netlify's 404 handling, which pages using root-absolute paths need.
  - `fonts.js`: serves the real web fonts from `tests/fixtures/fonts/`, because text width decides several layout checks.
- **Structure of a test file:** each one starts with a comment saying what past bug it guards against. Keep that pattern for new tests, and confirm a new check fails against the old behavior before relying on it.
- **Timing:** checks that measure the animated hero must not read positions mid-animation. Measure the static `.overflow-hidden-mask` rather than the moving word inside it.
