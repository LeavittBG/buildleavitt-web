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
square footage drifting from Leavitt's figures, a price reappearing on the plans. The comment at the
top of each file says what it guards against and why. Run `npm test` before
merging anything that touches the markup, the stylesheet or the plans data.

The tests serve the real web fonts from `tests/fixtures/fonts/` rather than
fetching them, because text width decides several of the layout checks. If
you change the Google Fonts URL in the pages, run `npm run test:fonts` to
refresh that copy.

The tests never reach Google Analytics. Every page carries the live Tag
Manager container, and until November 2026 a test run let it load: page views
went to the real Analytics property from `127.0.0.1`, and one test opens the
thank-you page, whose page view Analytics counts as a lead. `launch()` in
`tests/lib/env.js` now refuses Google's tag and analytics hosts on every page
a test opens, and `tests/analytics-off.test.js` checks that it does. Always get
the browser from `launch()`, never from Playwright directly.

`tests/seo.test.js` is the one file that opens no browser: it reads the pages
with jsdom and checks what search engines are told. Structured data parses on
every page; every visible breadcrumb matches its BreadcrumbList; each service
page describes its service and repeats the business (name, address, phone)
exactly as the homepage does; the towns on the homepage band are the `City`
entries in the structured data; `/plans/` lists every plan; every footer links
the three services; every file the hero's `srcset` names exists; and
`netlify.toml` sets the cache and security headers. `markup.test.js` also
holds every indexable page to a title of at most 70 characters and a
description of 70–155, repeated in the preview tags.

One check in `plans.test.js` reads the brochure PDFs with `pdftotext`
(`brew install poppler` on a Mac). Without it that check is skipped and says
so; the rest still run.

Screenshots the tests leave for a person to look at go to `tests/.output/`,
which git ignores. `tests/` is removed from the Netlify deploy, along with
every other file that is not part of the site - see the comment in
`netlify.toml`.

GitHub runs the whole suite on every pull request
(`.github/workflows/test.yml`) and shows the result as a check named **test**
on the PR, listed there as **Tests / test** because the workflow is named
**Tests** (the name to look for in the Actions tab). If it fails, the screenshots are attached to the run under
Artifacts. To make a failing run block the merge button:

1. On GitHub, open the repository → **Settings** → **Branches**
2. **Add branch protection rule** (or **Add classic branch protection rule**)
3. Branch name pattern: `main`
4. Tick **Require status checks to pass before merging**, search for `test`
   and select it
5. **Create**

## Site watch

Nobody tells a small business when its website has been tampered with, so the
repository checks for itself. Every night `.github/workflows/watch-site.yml`
runs `scripts/watch-site.mjs`, which:

- downloads every file Netlify publishes and compares it, byte for byte, with
  what is on `main`. The only difference it accepts is the rewrite Netlify
  makes to the contact form's opening tag when it wires the form up. The watch
  works that rewrite out from the committed tag (Netlify drops its own two
  attributes, sorts the rest, uses single quotes and shortens the action), so
  restyling the form needs no change here. A form pointed anywhere else is
  reported, because that is how leads get stolen;
- reads the live Tag Manager container (`GTM-PHGFM247`): its version, the
  kinds of tags and variables in it, and every web address it mentions. Tag
  Manager is the one place code can be added to every page without touching
  GitHub or Netlify, so a new version, a Custom HTML tag or a non-Google
  address is reported;
- looks up the domain's DNS: the name servers, the mail servers, where the
  bare domain and `www` point, that SPF still names Google Workspace, and
  that the DMARC policy is no weaker than the baseline;
- confirms Netlify is still the one serving the site, over HTTPS, with the
  `http://` and `www` addresses redirecting to it.

When anything differs, the run opens a GitHub issue labelled `site-watch`
that mentions Kyle, or adds to the one already open, and GitHub emails it to
him. A quiet night leaves nothing but a green run under Actions.

The expected state is `BASELINE` at the top of the script. When a change was
made on purpose (a new Tag Manager version, a DNS change, DMARC moved from
`none` to `quarantine`), update the baseline in a pull request so the next
night is quiet. Until then the issue comes back every night, which is the
point. If the change was not deliberate, the issue says where to look and how
to put the site back.

To run it by hand: on GitHub, Actions, **Site watch**, **Run workflow**; or
locally, `node scripts/watch-site.mjs`, which needs no `npm install`.
`tests/watch-site.test.js` checks that the watch notices a changed page, a
redirected form and a tampered container, and does not cry wolf about the
form rewrite.

One thing GitHub does on its own: in a public repository it switches scheduled
runs off after 60 days with no activity in the repository, and emails first.
If that happens, Actions, **Site watch**, **Enable workflow** turns it back on.

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

The two hero crops are also written at smaller widths (`hero-home-1280`,
`hero-home-1920`, `hero-home-phone-800`, `hero-home-phone-1200`, JPEG and WebP)
for the hero's `srcset`, so a phone is not sent the 2560-pixel file. The widths
are the `srcset` lists in `TARGETS` in `scripts/optimize-images.mjs`; the files
are committed like the rest.

The logo is written the same way at 656 pixels (`Gold-656.png`, `Gold-656.webp`)
beside the 1200-pixel `Gold.png` and `Gold.webp`. Its largest place on any page
is 328 pixels wide, so the 656 file is what every phone and ordinary laptop is
sent; each page's logo lists both files with a `sizes` matching its own logo.
`Gold.png` must keep its name: the business's structured data gives that address
as the logo.

No picture has an `onerror` stand-in, and none comes from another site: a
picture that fails to load shows its description. `tests/seo.test.js` checks
both, and that every file a `srcset` names with a width really is that wide.

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

Each photo rendering (a plan's cover picture and its Modern Brick twin) is
written in three widths: full size (1468 or 1600 pixels), 960 and 640, as WebP
and JPEG. `plans:images` writes them (`SMALL_WIDTHS` in
`scripts/extract-plans.mjs`) and records the widths in `src/plan-images.json`;
`plans:build` then lists all three wherever a rendering is shown, with the width
it is drawn at, so a browser takes the smallest that still looks sharp: the 640
copy for a card on a laptop, the 960 copy on a phone, the full file for the
picture across a plan page on a desktop. The first entry of each `sizes`
(`(max-width: 639px) and (min-resolution: 2.5dppx) 74vw`) is there for iPhones,
which would otherwise take the full-size file for a small card; keep it. Floor
plans are line drawings people zoom into and stay one full-size file.
`tests/plan-pictures.test.js` opens the pages as an iPhone, an older phone and a
laptop and checks which file each takes.

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

### A second exterior: Modern Brick

Every cover shows its plan as a Modern Farmhouse. In October 2026 Kyle was told
that a buyer who does not care for farmhouse style needs to see something else,
so every plan gained a second exterior. He compared five on The Pioneer I
(classic red brick with shutters, limewashed brick, charcoal brick, coastal
shake and Craftsman) and chose charcoal brick: it reads as a current brick home
and is plainly different from the white farmhouse.

Each one is a photo rendering made from that plan's own cover rendering with
Artlist (Nano Banana 2.1 image-to-image, 2K, 16:9), which keeps the camera, the
house, every window, door, porch and garage door, the lawn and the light, and
changes only the finishes. Every rendering was checked against its farmhouse
rendering for windows, doors, gables, porch and garage, and redone if it changed
the house. Kyle then had the garage doors made black on the eight plans whose
garage faces the street (Pioneer I and II, Craftsman, Illustrator, Impressionist,
Innovator, Maestro, Romantic), so they sit back in the dark brick and the
stained front door is the one warm accent; that was a second, targeted edit of
each rendering ("Change only the garage doors: make them satin black, keeping
exactly the same door design..."). They are kept as
`assets-src/plans/<slug>-modern-brick.jpg`. The first prompt, for a retake
(Kyle approves the cost of any retake first), followed on those eight by the
garage-door edit:

> Keep this exact photograph: the same camera position, framing and lens; the
> same house footprint, massing, roof lines, roof pitches and gables; every
> window, door, porch, balcony and garage door in exactly the same number, size
> and position; the same driveway, lawn, landscaping, trees, sky and warm
> late-afternoon light. Do not add or remove any window, door, porch, dormer,
> gable, chimney, garage door or wing.
>
> Change only the exterior style and materials, to a current modern brick home:
> the first-floor front walls, any porch base and any garage front in dark
> charcoal brick with light gray mortar (in place of the stone and the
> first-floor siding); crisp white horizontal lap siding on the second floor and
> in all the gables (no board and batten, no vertical siding, no shakes); white
> trim; black window frames without grilles; no shutters; slim square white porch
> columns in place of any wood or dark porch posts; any small roofs over the
> porch, windows or garage doors in the same dark asphalt shingles as the main
> roof (no metal roofs); no decorative gable trusses or brackets; a warm stained
> wood front door; warm stained wood garage doors wherever there are garage
> doors. Photorealistic architectural photograph.

`scripts/add-elevation-pages.py` sets each rendering as the last page of its
brochure, "Modern Brick Elevation", in the brochure template. It works from the
page entry in `src/plans.json` (id `elevation-modern-brick`), which also names
the rendering as the page's `image` with `crop: false`, so the site shows the
rendering itself rather than a crop of the brochure page. The script replaces a
page it made before, so when a brochure PDF is replaced, for instance with
redrawn floor plans, set the entry's `page` to the new last page and run it
again before `npm run plans`.

On the plan page the rendering comes straight after the specs, ahead of the
floor plans, with a link to it under the main photo; at the end of the drawings
it would sit below every floor plan, where the buyer it is for has already
left. `plans.test.js` checks both, and that every plan has one. Since a plan now
comes in two exteriors, the line under its name and its Google description no
longer name a style ("A two-story plan with 4+ bedrooms..."), and the models'
`style` field was dropped from `src/plans.json`.

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
anything else. Square footage is not on the covers and still comes from the
price sheet.

`sqft` is living square footage. `sqftFrom: true` means Leavitt's sheet said
"starting at", and the page renders "From 2,626" rather than a flat figure;
two models are exact and have it `false`. Keep that distinction — it is the
difference between a starting price and a promise.

There are no prices in the data. Until October 26, 2026 each model carried its
starting price (`price`, `priceFrom`, dated by `pricesAsOf`), and the collection
page showed one, "Pricing starts at" the lowest of them, with the qualifier
*"Starting price is for the home with all standard features included, and does
not include the homesite"*. Kyle took the figure off the page and then had the
prices deleted from `src/plans.json`, because this repository is public: a
figure kept in the data was still published to anyone reading the code. Older
commits still hold the September 2026 figures. If a price ever goes back on a
page, the qualifier goes with it. A test fails if a dollar figure or "starting
price" wording appears on any plan page, or if any key in the data has "price"
in its name.

`sqftNote` and `bathsNote` print a qualifying line under a figure,
for cases one number cannot carry honestly — The Storyteller gains 70 sq ft with
the three-car garage, and has an optional basement full bath on top of its 4.5.

### The Leavitt Standard

The "what's included in every home" list at `/plans/#included` is built from the
`STANDARD` array in `scripts/build-plans.mjs`, not from a PDF, so it is
searchable and readable on a phone. The printable sheet lives at
`assets-src/leavitt-standard.pdf` and is copied to `plans/pdf/` by
`npm run plans:images`; the section links to it. Edit the array and the PDF
together so they do not drift. The PDF was made with WeasyPrint and its source
is not in this repository, so a small wording fix is made in the PDF itself:
"TGI" became "TJI" on October 27, 2026 by swapping one letter's glyph in its
page content (the "J" was already in the embedded font), checked by rendering
before and after. `plans.test.js` reads the PDF's text for that line.

### The plan finder

The "Find your plan" section of `index.html` and the card grid on `/plans/` are
the same thing: three questions (stories, bedrooms, size) that narrow the plans
as they are answered, with every plan as a card underneath. Both are generated
by `npm run plans:build` — the homepage's between the `<!-- plan-finder:start -->`
and `<!-- plan-finder:end -->` markers (and its script between
`<!-- plan-finder-script:start -->` / `end`), so never edit between them by hand.
Each card carries the figures it is matched on as `data-stories`, `data-beds`
(the fewest bedrooms, so "4+" is 4) and `data-sqft`, straight from
`src/plans.json`. All seventeen cards are in the page and the script only shows
and hides them, so with scripts blocked the plans are still there: the homepage
shows the six in `FEATURED` in `build-plans.mjs` and links to the rest, `/plans/`
shows them all. The homepage shows six matches at most and its "Browse all"
button becomes "See all N matching plans", pointing at `/plans/?stories=2&beds=4`,
which opens already narrowed; `/plans/` keeps the answers in its address. When
nothing fits, the finder says so and offers a custom home instead of an empty
grid. "Start with this plan" on a card opens the contact form with the plan named
and "Semi-Custom Home" chosen (on the homepage without a reload). Each plan page
ends with three "Plans like this one": the same number of stories, nearest in
size. `tests/plan-finder.test.js` checks all of this against the data.

The three cards on `semi-custom-homes.html` are still hand-written; their facts
line (`data-plan-facts`) is filled in by `npm run plans:build`.

## Business details

The address, phone number and opening hours are in the footer of every page,
and again in the homepage's structured data (the `application/ld+json` block
in `index.html`), which is what Google reads alongside the Business Profile.
The plan pages get their footer from `scripts/build-plans.mjs`. If any of these
change, change them in all of those places; `markup.test.js` fails if the hours
on any page stop matching the structured data. Saturday is by appointment,
which the structured data has no way to say, so it lists Monday–Friday only.

The three service pages repeat the name, address, phone and logo in a compact
business node with the same `@id` as the homepage's, so Google can read each
page on its own; `tests/seo.test.js` fails if the copy drifts. The towns listed
under each county on the homepage's service-area band are repeated as `City`
entries in the homepage's `areaServed`; change both together, the same test
compares them.

## Service pages

`custom-homes.html`, `semi-custom-homes.html` and `renovations.html` are
hand-written, one per service, with the same header and footer as the plan
pages. The homepage service cards link to them (they used to open a pop-up).
Each page's call to action opens the contact form with "Project Interest"
already chosen: `/?interest=Custom%20Home%20Build#contact`. The semi-custom
page shows three plan cards whose facts line (`data-plan-facts`) is filled in
by `npm run plans:build`. `tests/service-pages.test.js`
checks the pages, the hand-off and that every link is at least 24px tall;
`tests/tap-targets.test.js` holds every other page to the same 24px on phones,
tablets and laptops.

Each service page's head carries a BreadcrumbList (matching the visible
breadcrumb), a Service whose provider is the business, and the compact business
node described under Business details. Each has a "Where we build" section that
names the towns in the five counties, and links to the other services and to
the plans. Every footer on the site, the plan pages' included, has a Services
row linking the three pages; the menu bar is Kyle's and does not change.

## Leavitt Connect

Leavitt Connect is Leavitt's own app for homeowners, at
`https://connect.buildleavitt.com`. It opens in the phone's browser and is not
in an app store. The site uses it in two ways: as the sign-in link for current
clients ("Client Login"), and as a selling point for buyers.

This section was written on November 9, 2026 and sat on a branch without a pull
request; it was checked against the site and added here on November 11, 2026.

### Where it appears

- **Client Login** links to `https://connect.buildleavitt.com` in a new tab:
  - at the end of the homepage's desktop menu bar, after a fine rule, small,
    under the phone number;
  - in the header of the plan pages and the three service pages, from tablet
    width up, beside the phone number;
  - in the phone menu;
  - in the footer of every page.

  On the homepage it is white while the menu bar is transparent over the hero
  photo, and gold once the bar turns navy.
- **Homepage section `#leavitt-connect`**, after the process steps. It has:
  - the heading "Leavitt Connect." and an introduction;
  - the homebuyer tour video, with a written transcript underneath;
  - six features, each with a "See it in the video" button: schedule,
    selections, change orders signed online, inspections / punch lists /
    documents, "Nothing to download, no password", and email updates;
  - "Let's talk about your home", the office line and a sign-in link.
- **"Follow the build from your phone."** on `custom-homes.html` and
  `semi-custom-homes.html`. It is a short paragraph linking to
  `/#leavitt-connect`. The semi-custom page also lists Leavitt Connect among
  what is the same for custom and semi-custom builds.
- **The homepage questions:** the project-manager answer, and its FAQPage
  structured data, say homeowners follow the build in Leavitt Connect.
- **`terms.html`** says the portal is Leavitt's own service and the terms
  apply there.

### History

| Date (2026) | Pull request | What changed |
|---|---|---|
| Aug 5 | early commit | "Client Login" added to the header and phone menu. It pointed at `builderpro.com/login`, an unrelated company's site. |
| Sep 22 | #12 | Client Login pointed at Leavitt's own portal, connect.buildleavitt.com. The terms stopped calling the portal someone else's service. |
| Sep 27 | #26 | Client Login moved to the footer and the phone menu. On small laptops it wrapped onto two lines in the desktop bar. |
| Oct 7–8 | #38 | Kyle wanted it back at the top. It returned small and set apart after "Get a Quote", and on the plan-page header. The same pull request added the homepage section and the video. |
| Oct 11 | #40 | The video's `uploadDate` was given a time and timezone, after Search Console flagged the bare date. |
| Oct 16 | #42–#46 | The service pages gained the "Follow the build from your phone." paragraph. The video buttons got taller tap targets (`py-2`). Client Login turned white over the new daylight hero photo. |
| Oct 31 | #51 | The homepage sections were reordered. Leavitt Connect stayed directly after the process steps. |
| Nov 9 | #57 | The office line changed to (443) 613-9750 everywhere, the section's own call link included. The video still says and shows the old (866) number at its end, so that caption and transcript sentence keep it. |
| Nov 10 | #58 | The phone number went into every header, above or beside Client Login. |
| Nov 13 | #66 | The video's ending was re-cut: the closing card shows (443) 613-9750, the sentence that spoke the old number is gone, and it runs 1:44 (see "The ending, re-cut" below). The old number is no longer anywhere on the site. |

### Wording rule

Kyle's rule: every claim is true and can be checked. Never say or imply Leavitt
is the only builder with an app. "Our own app, built for Leavitt homeowners"
and "one more way building with Leavitt is different" are his approved phrases.

The facts come from two sources:
- **Kyle's list (October 5, 2026):** schedule and what's next, selections,
  change orders signed online by every homeowner on the home, inspections
  passed, walk-through punch lists with photos, documents, sign-in by emailed
  code or Face ID, and short email updates, never a flood.
- **The video's narration**, which gives more detail.

Kyle confirmed on October 7–8, 2026 that:
- the app is not in an app store, which is why the page says "Nothing to
  download";
- biometric sign-in works on iPhone and Android, which is why it says "Face ID
  or your fingerprint".

The six features keep Kyle's short approved wording. A longer version taken
from the narration was offered and not adopted.

`markup.test.js` checks the `#leavitt-connect` section:
- all six features are there;
- the change-order line says every homeowner signs;
- it links to the sign-in, the office line and the contact form;
- nothing says "only … builder/app", "first builder/app", "unique",
  "unlike any", "no other", an app store or "download the app".

The check reads that section only. The service-page paragraphs and the
question answer are not scanned, so keep them to the same facts by hand.

### The video

- **Source.** The source files are in Kyle's Google Drive, under
  `Builder Pro App/Tutorial videos`:
  - `Leavitt Connect - Homebuyers.mp4`: 1:48, 1920×1080, 38 MB. It still
    ends on the old (866) number: the site's copy was corrected, the source
    was not (see "The ending, re-cut");
  - `Leavitt Connect - Homebuyers (captions).srt`;
  - `Chapters for YouTube.txt`;
  - the narration scripts.

  The same folder has tutorials for homeowners, realtors, office staff and
  trade partners; none of them is on the site. The video shows a made-up demo
  home, so its names are not real clients.
- **Why it is hosted here and not on YouTube.** YouTube can run ads, possibly
  a competitor's, on any video from a channel outside its Partner Program.
  Viewers without YouTube Premium would see them, and a new channel cannot
  switch them off.
- **Files in `media/`:**
  - `leavitt-connect-homebuyers.mp4`, the web copy: 6.2 MB, 1:44;
  - `leavitt-connect-homebuyers.vtt`, the captions;
  - `leavitt-connect-poster.webp`, the cover still.

  Netlify caches `/media/` for one week (`netlify.toml`). The files are
  replaced in place under the same names, so the cache is never longer than
  that and never `immutable`.
- **Loading.** The `<video>` has `preload="none"`, so nothing downloads until
  play is pressed. Captions are a `<track>` the viewer turns on.
- **The cover still** is the schedule screen at 0:39.5. The "home at a glance"
  screen was rejected because it shows a demo price, which could be read as a
  real Leavitt price.
- **The transcript** under the video is the captions, word for word, in six
  paragraphs.
- **The six buttons** start at 0:35, 0:42, 0:50, 1:10, 0:18 and 1:25, each the
  start of the caption where that feature is described. A small script waits
  for the video's metadata, then seeks and plays.
- **The line under the video** reads only "A sample home: the names and
  numbers aren't real." Kyle kept it short on October 8, 2026. Someone watching
  without sound never hears the narration say the same thing at 0:11.
- **Structured data.** A `VideoObject` in the homepage's JSON-LD names the
  file, poster, 1:44 duration and
  `uploadDate` `2026-10-08T15:19:04-04:00`. Google needs a full date and time
  with a timezone. The date is when the video was first published; the
  November re-cut of its ending did not change it.

#### The ending, re-cut (November 13, 2026; audit item 7)

The source video ends on a closing card, "Let's talk about your home", that
shows the old (866) number from 1:36, and the narrator's last sentence says it
(1:39.9 to 1:45.6). Kyle chose to correct the site's copy and not re-record:

- **The card shows (443) 613-9750** for the whole time it is on screen. The
  line was set again in the card's own lettering (Inter 500 at 29.66px, colour
  `rgb(216,224,244)`, centred on the frame, ink from row 675) on a patch of the
  card's background, and blended into each of the 18 frames of the fade-in by
  that frame's share of the card, so the old number never shows through. The
  corrected card is kept as `assets-src/leavitt-connect-closing-card.png`.
- **The last sentence is cut.** The sound stops at 1:39.9, in the pause after
  "one more way building with Leavitt is different", and the card holds in
  silence to 1:44. The sound was copied, not encoded again.
- **The picture was encoded again from the site's copy**, not from the 38 MB
  original, at CRF 23 with the settings in step 2 below. Against the copy it
  replaced, the first 95 seconds measure SSIM 0.999 (51.6 dB): no visible
  difference in the smallest text. If the original is ever used again, its
  ending needs the same correction.
- **The narrator now says no phone number.** The number is on the card only.
- The last caption and the last transcript sentence went with the audio, the
  `VideoObject` says `PT1M44S`, and the exemption `markup.test.js` made for the
  old number is gone: it now fails any other number on any page or in the
  captions.

A returning visitor's browser may keep the old video for up to a week
(`/media/` is cached for seven days).

#### Replacing the video

1. **Get the new MP4 from Drive.** The Drive connector returns files as text,
   which is too large for a video. Kyle sets the one file to "Anyone with the
   link" for a few minutes. Download it with
   `curl -L "https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t"`,
   then he sets it back.
2. **Re-encode it:**
   `ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 26 -tune stillimage -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 64k -ac 1 media/leavitt-connect-homebuyers.mp4`.
   Before choosing, compare the smallest on-screen text against the original.
   At CRF 26 it looked the same; at 30 it softened.
3. **Make the captions.** Turn the `.srt` into WebVTT: add a `WEBVTT` header
   and change the comma in each timestamp to a dot.
4. **Choose a cover still** with no demo prices. Write it as WebP with sharp.
5. **Update the page.** Rewrite the transcript paragraphs from the new
   captions. Move each button's `data-seek` to the caption where its feature
   starts. Update the `VideoObject`'s `duration` and `uploadDate`.
6. **Run `node tests/connect-video.test.js`.** It checks:
   - nothing downloads before play;
   - the file is under 8 MB, with its index (`moov`) before the data;
   - it runs 1:44;
   - the captions fit the video, and the transcript has every caption;
   - every button starts on a caption and plays from its moment;
   - the `VideoObject` matches the files.

   Headless Chromium cannot decode H.264, so the button check plays the blank
   WebM in `tests/fixtures/blank-104s.webm`, served with byte ranges as
   Netlify serves the real file. A different length means changing the
   1:44 check and that fixture
   (`ffmpeg -f lavfi -i color=c=black:s=64x36:r=5 -t <seconds> -c:v libvpx-vp9 -b:v 0 -crf 60 -an blank-<seconds>s.webm`).

   `markup.test.js` fails any phone number but the real one, on every page
   and in the captions. A new recording must not say or show another.

### Open items

- **A demo markup figure in the video.** At about 0:55 the sample change order
  shows an overhead-and-profit percentage. The video and the line under it say
  the numbers aren't real, but a viewer who pauses could read it as Leavitt's
  markup. It was pointed out to Kyle on October 8, 2026. On November 13, 2026,
  with the ending being re-cut, he chose to leave that screen alone. It
  scrolls, so covering the figure would look patched; the clean fix is
  re-recording that part, if he ever wants it. The figure itself is left out
  of these notes on purpose.
- **The narrator gives no phone number** since the ending was re-cut; the
  number is on the closing card only. A new recording could say it again.
- **Unreviewed wording.** Kyle has not reviewed the service pages' wording,
  the Leavitt Connect paragraph included (see "Service pages").
- **The wording check covers the homepage section only.** Extending it in
  `markup.test.js` to the service pages' paragraphs and the project-manager
  answer was proposed on November 9, 2026 and not done.
- **Video sharing in Drive.** The source video is shared with "Leavitt Building
  Group", meaning buildleavitt.com accounts. Kyle is the only one, so he kept
  it. If employee accounts are added, they will be able to open it.

## Keyboard and screen readers

Every page has one `<main id="main">` holding the page's content, which is the
landmark a screen reader's "jump to main content" key looks for. Every page
with a bar starts with a "Skip to main content" link (`class="skip-link"`,
styled in `src/styles.css`), directly after the Tag Manager `<noscript>`: it
takes no room until the Tab key reaches it, then shows as a white button at the
top left and sends the keyboard past the logo, menu, phone number and Client
Login into the page. It is in the same seven places as the header (the homepage,
the three service pages, `privacy.html`, `terms.html` and `build-plans.mjs`).
The thank-you and not-found pages have only a logo above their content, so they
have the landmark and no skip link.

In the contact form, the field being typed in is marked by a 2px underline in
the deeper gold (`#866f4f`), and a choice chip reached with the keyboard is
ringed in the same colour, in the form and in the plan finder. The paler gold is
too faint on white for this (2.3:1; a focus mark needs 3:1).

`tests/keyboard.test.js` checks all of it on every page at phone and laptop
width: it presses Tab, confirms the skip link appears on top of the page, presses
Enter and confirms the next Tab lands inside the content, and photographs the
chosen fields and chips to measure the mark against the page around it.

## Smallest text

No text on the site is smaller than 12px (`text-xs`). Until November 2026 the
small capital-letter labels were 11px, and a few were 9 or 10px on a phone.
`tests/text-size.test.js` reads the size the browser gives every piece of text
on every page, at a phone and a laptop width, hidden or not, and fails anything
smaller. The two links under each plan card ("View plan", "Start with this
plan") are set a little closer (`tracking-widest`) so that the larger letters
take no more room than the old ones did.

## Response headers

`netlify.toml` sets `X-Content-Type-Options`, `Referrer-Policy` and
`Permissions-Policy` on every response, and a one-week `Cache-Control` on
`/plans/img/`, `/plans/pdf/` and `/media/` and, since November 2026, on the
pictures in the site's root: the hero photograph in every size
(`/hero-home*`), the logo (`/Gold*`), Kyle's portrait (`/kyle.*`) and the
before/after pair (`/Before.*`, `/After.*`). The HTML and `dist/styles.css` keep
Netlify's default (`max-age=0, must-revalidate`), because their names never
change and an edit has to show at once. The cached paths hold files that are
replaced in place under the same name (a redrawn brochure, a retaken
rendering), so the age stays short and is never `immutable`.

`tests/seo.test.js` checks the blocks: every picture any page shows must fall
under a cache rule, every rule is a day to a week, and no page, stylesheet or
sitemap may be caught by one. A new picture in the root therefore fails the
test until it has a rule; in `netlify.toml` a `*` stands for any characters
inside a path segment.

## Forms

The contact form is in two steps since October 2026: first the project type and
the budget range, as radio cards and chips, then name, email, phone and details.
Both steps are in the markup inside the one `<form>` and show without script;
the script shows one at a time and will not open step 2 until a project type and
a budget are chosen. The field names and the Interest and Budget values are
exactly what the old single-step form sent, so Netlify's submissions are
unchanged. `tests/contact-steps.test.js` checks the fields and the steps.

The contact form is a Netlify form. Netlify detects the fields from the
deployed HTML, so every field it should record has to exist in `index.html` —
including `Plan`, the hidden field that records which plan page a visitor came
from. Submissions appear under Forms in the Netlify dashboard. The form posts
to `/success.html`, but Netlify rewrites that to `/success` when it publishes
the page, so the thank-you address visitors see is `buildleavitt.com/success`;
anything that counts a lead by URL (the Google Analytics `generate_lead` event)
has to match that.
