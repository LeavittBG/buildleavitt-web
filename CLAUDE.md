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
npm run plans:scaffold     # print a src/plans.json entry from a new brochure's cover caption and page titles
npm run images             # resize + WebP the photos in assets-src/
npm run test:fonts         # refresh tests/fixtures/fonts after changing the Google Fonts URL
```

There is no linter. The test suite is the gate: GitHub Actions (`.github/workflows/test.yml`) runs `npm run build && npm test` on every PR as the check named **test**. Test screenshots land in `tests/.output/` (gitignored) and are attached to failed CI runs.

The plan scripts need poppler (`pdftoppm`, `pdfinfo`, `pdftohtml`). One check in `plans.test.js` uses `pdftotext` and is skipped with a notice if it's missing.

## How the site is put together

- **Pages:** `index.html` (the homepage, with all its JS inline at the bottom), `privacy.html`, `terms.html`, `success.html` (form thank-you, noindex), `404.html`. Everything under `plans/` is **generated** by `scripts/build-plans.mjs` from `src/plans.json`. Never hand-edit `plans/*.html`; change the data or the script and re-run `npm run plans:build`.
- **Committed build outputs:** `dist/styles.css`, `plans/*`, `sitemap.xml`, `robots.txt` and the resized `*.webp`/`*.jpg` in the root are all committed. Netlify only runs `npm run build`, not the image or plan scripts, and then deletes every non-site file from the deploy (`assets-src/`, `tests/`, `src/`, `scripts/`, `package*.json`, `tailwind.config.js`, `README.md`, `CLAUDE.md`). A new top-level file that is not part of the site belongs on that list in `netlify.toml`, which `markup.test.js` checks. After changing markup, rebuild the CSS. After changing plan data or a page by hand, run `npm run plans:build` before committing: it rewrites the plan pages and the sitemap `<lastmod>` dates, which come from git.
- **Tailwind purges** any class it can't find in `./*.html` or `./plans/*.html` (`tailwind.config.js` `content`). A class used only in JS elsewhere, or only in a new file outside those globs, silently loses its styling. Scratch HTML files left in the repo root get scanned too, so keep mockups out of the root or delete them before building.
- **Fonts:** Inter and Playfair Display are set in `tailwind.config.js` `theme.extend.fontFamily`, not with a CSS `body` rule. The `font-sans` class on `<body>` would override such a rule. The Google Fonts URL must list every weight the markup uses (500 is needed for `font-medium`). It appears in every page's `<head>` and in `build-plans.mjs`; keep them identical. Headings are one upright face throughout: the italic-serif endings ("Building legacies, *not just homes.*") were removed as a template tell, the italic font is no longer requested, and `markup.test.js` fails any italic text.
- **Icons** are inline SVG copied from Lucide, not a script. The three service-card icons are the exception: custom line drawings (see README "Icons"). Icon-only links and buttons need an `aria-label`; `markup.test.js` fails any unnamed link or button on any page.
- **404.html** is served by Netlify at the broken address, at any depth. Every asset and link in it must be root-absolute (`/dist/styles.css`).
- **`netlify.toml`** keeps `pretty_urls = false`, so published links match the canonical tags and sitemap. A test checks it.
- **Google Tag Manager** container `GTM-PHGFM247` belongs to kyle@buildleavitt.com; the marketing agency is a user on it. It is in every page's `<head>` and `<body>` and in `build-plans.mjs`; `markup.test.js` fails if any page loads a different container. Analytics (`G-RT4JHER039`) is added inside the container, not in the site's code.
- **Contact form** is a Netlify form. Every field it records, including the hidden `Plan` field, must exist in the deployed `index.html`.

## Homepage specifics

- **Hero** (`#hero`): one block of markup, two layouts. From `lg` up the photo fills the screen behind the copy. Below `lg` the photo is a banner above the copy. `layout.test.js` checks both at six sizes, including that "What We Build" is on the first screen.
- **No template effects:** there is no loading screen, scroll-progress bar, custom cursor or scrollbar, magnetic buttons, count-up figures, parallax, word-by-word headline or fade-in-on-scroll. They were removed as stock template tells, and because each one left content hidden until script ran. Content is visible from the first paint; `markup.test.js` and `hero-loading.test.js` fail if any of it comes back. Don't put `will-change` on anything either: it left the headline blank on a Windows Chrome machine (`hero-layers.test.js`).
- **Business facts must stay consistent** across the footer on every page, the JSON-LD in `index.html` and the plan-page footer in `build-plans.mjs`. These are the address, phone (866) 832-6524, and opening hours (Mon–Fri 8–5, Saturday by appointment, closed Sunday). `markup.test.js` enforces that the hours match the JSON-LD. The Facebook link is `https://www.facebook.com/profile.php?id=61591583276647` in all three places, also enforced.

## Plans data rules (`src/plans.json`)

Specs, prices and square footage come only from Leavitt's own figures, never estimates. A missing value renders "On request". `sqftFrom`/`priceFrom` mean "starting at", and the qualifier "Starting price is for the home with all standard features included, and does not include the homesite" must travel with every price (it links to the Leavitt Standard list at `#included`). `plans.test.js` fails if any figure on a page differs from the data or the qualifier goes missing. Bedrooms, baths and garage are copied from each brochure's cover ("4+", "2.5+", "2+ car"), and the test fails if they differ from it. The brochures (October 2026 template) share one layout: a cover with the elevation, then one page per floor and per set of options, each titled in its header band. Every page is shown on the site in the brochure's order, cut to `brochureBands` in `src/plans.json`; the cover caption and specs are cut off. `plans.test.js` checks each label against its page's printed title and that no page is left out. The `_README` inside `src/plans.json` and the README's "Home plans" section have the full workflow for adding a model.

## Tests

- **Shared helpers** live in `tests/lib/`:
  - `env.js`: `ROOT`, `FILE_ROOT`, `launch()` and `serveRepo()`. `launch()` uses `CHROMIUM_PATH` or `/opt/pw-browsers/chromium` when present. `serveRepo()` is an HTTP server that mimics Netlify's 404 handling, which pages using root-absolute paths need.
  - `fonts.js`: serves the real web fonts from `tests/fixtures/fonts/`, because text width decides several layout checks.
- **Structure of a test file:** each one starts with a comment saying what past bug it guards against. Keep that pattern for new tests, and confirm a new check fails against the old behavior before relying on it.
- **Timing:** nothing on the homepage animates on load any more, so tests can measure as soon as fonts are ready. `hero-wrap.test.js` reads each `.hero-line`'s line boxes with a Range to confirm the headline stays on two lines.

## Decisions and history (September–October 2026)

What Kyle Leavitt (the owner) decided while reviewing the site with Claude, so later sessions do not reopen it. Pull requests #18–#31.

### How changes are made
- Every change goes through a pull request from `claude/leavitt-website-review-79vqny`. Kyle checks the Netlify deploy preview and says "merge". After merging, reset that branch to `main` and confirm the change on buildleavitt.com.
- Explain changes in plain language. When Kyle asks for an overview before a push, wait for his go-ahead.
- This sandbox cannot reach facebook.com, googletagmanager.com, Netlify deploy previews or Kyle's computer. Files from him come through Google Drive (`LBG Home Brochures`) or chat attachments.

### Content decisions
- **Leave homepage pricing alone.**
- **Hero:** the AI-generated house stays until the photographer's shots arrive. A replacement needs a full-resolution file (about 2400px wide or more). A daylight photo wants a neutral dark shadow behind the copy, not the navy fade.
- **No template look:** no italic heading endings, no eyebrow labels over headings, no "1 Uncompromising Standard" figure. All three testimonials show at once; there is no carousel.
- **Service icons (Kyle, October 3, 2026):** the stock house, ruler and hammer in navy tiles were replaced by custom line drawings with no tiles and no hover colour flip. They follow Kyle's "Service Icon Redesign Guide": a house in 3-D with a dimension line, a floor plan, and a house with a dashed addition, navy with gold marks.
- **Process steps (Kyle, October 4, 2026):** the boxed 01–04 numbers that filled with gold on hover became a left-aligned timeline: a fine rule over each step, a small gold square where it starts, and the number as a small gold label. The numbers stay because the steps happen in order. `markup.test.js` guards this and the service icons.
- **Contact details (Kyle, October 4, 2026):** the email, phone and office links lost their icon tiles, which turned navy on hover. They are a plain directory, each entry between fine rules that match the form's underlined fields, and only the text turns gold on hover. Nothing on the homepage fills with colour on hover any more, and `markup.test.js` fails if a `group-hover:bg-` class comes back.
- **"Read More" always shows (Kyle, October 4, 2026):** on the service cards and process steps it used to fade in only on hover, so it was easy to miss and never appeared on phones. It is always visible now, aligned along the bottom of each row and underlined while its card is hovered. It is navy with a gold arrow on the white service cards (pale gold is hard to read on white), and gold on the navy process section.
- **Trust figures:** "20+ years" and "100+ homes" are confirmed accurate.
- **About section:** the two paragraphs are Kyle's own words. Don't rewrite them.
- **Removed claims:** "3D renderings" and "premier architects" were taken out. The process pop-ups still mention a "dedicated project manager" (step 03) and a "comprehensive warranty package" (step 04); Kyle has not confirmed either.
- **Copy rewrite:** Kyle's answers to the copy-rewrite questions are deferred to a later date.
- **Menu:** the menu links stay as they are. Client Login is at the top (Kyle, October 7, 2026): at the end of the desktop menu bar after a fine rule, small and gold, and in the plan-page header from tablet width up. It is also in the phone menu and the footer. It once wrapped onto two lines on small laptops, and `layout.test.js` checks it stays on one line at every width.
- **Storyteller photos (removed on the realtor's advice):** they made it look as if Leavitt had built one house, and the granite read as dated. The photos, gallery, lightbox and Gallery menu links were removed everywhere. A gallery can return when new photography exists. Link previews use The Visionary's elevation.
- **Price wording:** the qualifier reads "with all standard features included", on the realtor's suggestion.

### Brochures and plan figures
- The October 2026 brochures came from Kyle's Drive folder `LBG Home Brochures/Updates Home brochures`. Their covers give starting points ("4+ bedrooms, 2.5+ baths").
- Bedrooms, baths and garage on each plan page match the brochure cover exactly (Kyle's choice, October 3, 2026). They replaced the price-sheet ranges, and `plans.test.js` reads every cover and fails if a page differs. Square footage and prices are not on the covers and still come from the September 2026 price sheet.
- The Innovator is a two-story home (Kyle, October 3, 2026). Its current brochure is wrong to call the second floor optional, and Kyle is having it corrected. Until the corrected brochure arrives, the site keeps the current cover's figures (2+ bedrooms, 2+ baths) but stays two-story at 2,330 sq ft. Don't change it to one story to match the brochure.
- The Storyteller has no brochure. A brochure for it needs a front elevation drawing, ideally from the permit set.

### Analytics, accounts and marketing
- **Ownership:** Kyle (kyle@buildleavitt.com) owns and administers Tag Manager (`GTM-PHGFM247`), Google Analytics 4 (`G-RT4JHER039`; setting data retention to 14 months was recommended but is unconfirmed) and Search Console (Domain property, verified June 29, 2026).
- **Lead tracking:** contact-form sends count as the `generate_lead` key event. It is configured in GA ("Create event": `page_view` where the URL contains `success.html`), not in the site's code.
- **Marketing agency:** Brighter Media Group (Ken Guise) works through smartadops@gmail.com. Its access:
  - Google Business Profile: manager
  - Tag Manager: account User, container Publish
  - GA: Editor
  - Search Console: Full user
  - Netlify: team invite. Kyle appears to have upgraded to Netlify Pro for it (the upgrade came minutes before the invite); check the agency is not an Owner.
- **Old container:** the agency's own container, `GTM-K9ND8BDT`, was replaced and must not return.
- **Privacy policy:** it names Google Analytics and Tag Manager. If the agency adds ad tags (Google Ads, Meta pixel, remarketing), name them in `privacy.html`, and have an attorney check the "we do not sell" line under Maryland's privacy law. The REVIEW comments in that file say so too.
