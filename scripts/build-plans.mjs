/**
 * Generates the plan pages from data.
 *
 *   npm run plans:build
 *
 * Inputs
 *   src/plans.json        - hand-authored model data (names, page labels, specs)
 *   src/plan-images.json  - measured image sizes, written by extract-plans.mjs
 *
 * Outputs
 *   plans/index.html      - the card grid at /plans/
 *   plans/<slug>.html     - one page per model, so each gets its own URL
 *
 * Adding model 17 is one entry in src/plans.json plus its PDF; run
 * `npm run plans` and both the images and the pages regenerate.
 *
 * Everything here is static: no class on a generated page depends on
 * JavaScript to become visible (deliberately not using .reveal-element, which
 * starts at opacity 0), so the plans read fine with scripts blocked.
 *
 * Pages live one directory down, so every asset path must be root-relative
 * (/dist/styles.css, not dist/styles.css).
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'plans');
const SITE = 'https://buildleavitt.com';
const GTM = 'GTM-K9ND8BDT';

const plansData = JSON.parse(readFileSync(join(ROOT, 'src', 'plans.json'), 'utf8'));
const { models } = plansData;
const PRICES_AS_OF = plansData.pricesAsOf || '';

/** A starting price, or null where Leavitt has not given one. */
const money = (n) => '$' + n.toLocaleString('en-US');

/**
 * The one sentence that has to travel with every price on the site.
 *
 * Leavitt's sheet says: *"Starting at" means without additional options*. That
 * qualifier is the difference between a headline number and a misleading one,
 * so it is printed wherever prices are, not buried once at the foot of a page.
 *
 * The homesite exclusion matters even more: it is the first thing a buyer
 * assumes either way, and assuming wrong is the difference between these
 * figures and the real cost of the house. Leavitt confirmed the lot is not
 * included, so the page says so rather than leaving it to be inferred.
 */
const priceNote = (extra = '') =>
  `Starting prices are for the home without any optional features added, and do ` +
  `not include the homesite` +
  (PRICES_AS_OF ? `. Current as of ${PRICES_AS_OF}` : '') + `.${extra}`;
const images = JSON.parse(readFileSync(join(ROOT, 'src', 'plan-images.json'), 'utf8'));

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/**
 * "The Leavitt Standard" - what every home includes, from Leavitt's own sheet.
 *
 * Built as real HTML rather than linking the PDF: this is the answer to "what
 * do I actually get for the money", which is the question a buyer comparing
 * builders is asking, and a PDF is invisible to search, awkward on a phone and
 * a dead end once opened. The PDF is still offered underneath for printing.
 *
 * Wording is Leavitt's, trimmed only of the decorative capitals. Brand names
 * carry their trademark symbols exactly as the sheet does.
 */
const STANDARD = [
  ['Premium interior', [
    ['9&rsquo; ceilings', 'basement and first floor'],
    ['Custom hardwood or luxury vinyl plank flooring', 'entire first floor'],
    ['Level 5 drywall finish', 'in the main living areas, for smooth, flawless walls'],
    ['Gourmet kitchen', 'quartz countertops, tile backsplash, premium GE &ldquo;Caf&eacute;&rdquo; series appliance allowance'],
    ['Owner&rsquo;s retreat', 'quartz countertops, custom tiled shower walls, tiled to the ceiling'],
    ['Solid core interior doors', 'with fully cased windows and openings throughout'],
    ['Stain grade stairs and handrail', 'first to second floor'],
    ['Insulated bedroom, bathroom and laundry walls', 'for sound dampening'],
  ]],
  ['Exterior &amp; infrastructure', [
    ['High-performance Andersen&reg; windows', null],
    ['Zip System&reg; wall sheathing', 'for moisture protection'],
    ['Upgraded siding &amp; 40-year architectural shingles', null],
    ['Stone to grade', 'front and side elevations'],
    ['Finished &amp; painted garage', 'insulated walls and service door'],
    ['Customer-owned propane tank', 'topped off at move-in'],
    ['75&rsquo; &times; 10&rsquo; asphalt drive', 'includes 30&rsquo; &times; 30&rsquo; parking pad and 10&rsquo; &times; 10&rsquo; turnaround'],
    ['Structural integrity', 'TGI floor joists and Advantech&reg; subflooring, glued and screwed'],
  ]],
];

const standardSection = () => `
        <section id="included" class="mt-20 scroll-mt-24">
            <div class="border-t border-gray-200 pt-16">
                <p class="text-[11px] font-bold uppercase tracking-[0.3em] text-[#c2a67a] mb-4">Included, not upgraded</p>
                <h2 class="text-3xl md:text-5xl font-light text-[#0f172a] mb-6">
                    The Leavitt <span class="font-serif italic">Standard.</span>
                </h2>
                <p class="text-gray-600 text-lg max-w-2xl mb-14">
                    Much of what other builders sell as an upgrade is simply how we build. Every home
                    on this page includes all of the following as standard.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-x-16 gap-y-12">
${STANDARD.map(([heading, items]) => `                    <div>
                        <h3 class="text-[11px] font-bold uppercase tracking-[0.2em] text-[#c2a67a] mb-6">${heading}</h3>
                        <ul class="space-y-4">
${items.map(([title, detail]) => `                            <li class="flex gap-3">
                                <span aria-hidden="true" class="text-[#c2a67a] shrink-0 mt-1">&#10003;</span>
                                <span class="text-gray-700 leading-relaxed"><strong class="text-[#0f172a] font-medium">${title}</strong>${detail ? ` &mdash; ${detail}` : ''}</span>
                            </li>`).join('\n')}
                        </ul>
                    </div>`).join('\n')}
                </div>

                <p class="mt-12 text-sm text-gray-500">
                    <a href="/plans/pdf/leavitt-standard.pdf" target="_blank" rel="noopener" class="text-[#c2a67a] font-medium hover:underline">Download the Leavitt Standard (PDF)</a>
                    &mdash; handy for comparing against another builder&rsquo;s quote.
                </p>
            </div>
        </section>`;

/**
 * A spec we do not have is shown as "On request" - never guessed.
 *
 * Each formatter takes the value and the whole specs object, because square
 * footage needs `sqftFrom`: Leavitt's figures say "starting at" for fourteen of
 * the sixteen models and give an exact number for the other two, and the page
 * has to keep that distinction rather than flatten it into one claim.
 */
const SPECS = [
  ['beds', 'Bedrooms', (v) => String(v).replace('-', '–')],
  ['baths', 'Bathrooms', (v) => v],
  ['sqft', 'Living Sq Ft', (v, s) => (s.sqftFrom ? 'From ' : '') + v.toLocaleString('en-US')],
  ['stories', 'Stories', (v) => (v === 1 ? '1 (ranch)' : v)],
  ['garage', 'Garage', (v) => v],
  ['price', 'Starting Price', (v, s) => (s.priceFrom ? 'From ' : '') + money(v)],
];

/** Specs whose value can carry a qualifying line underneath it. */
const NOTE_FOR = { sqft: 'sqftNote', baths: 'bathsNote', price: 'priceNote' };

const head = ({ title, description, canonical }) => `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','${GTM}');</script>
    <!-- End Google Tag Manager -->

    <title>${esc(title)}</title>
    <meta name="description" content="${esc(description)}">
    <link rel="canonical" href="${SITE}${canonical}">

    <meta property="og:type" content="website">
    <meta property="og:title" content="${esc(title)}">
    <meta property="og:description" content="${esc(description)}">
    <meta property="og:url" content="${SITE}${canonical}">

    <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <!-- Compiled Tailwind + custom styles (source: src/styles.css, build: npm run build) -->
    <link rel="stylesheet" href="/dist/styles.css">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-[#fcfcfc] text-gray-900 font-sans">
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${GTM}"
    title="Google Tag Manager" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <header class="bg-[#0f172a] px-6 py-6">
        <div class="max-w-6xl mx-auto flex items-center justify-between gap-6">
            <a href="/" class="inline-block" aria-label="Leavitt Building Group - back to home">
                <picture class="contents"><source srcset="/Gold.webp" type="image/webp"><img src="/Gold.png" alt="Leavitt Building Group" width="1200" height="293" class="h-12 md:h-14 w-auto object-contain"></picture>
            </a>
            <nav aria-label="Main" class="flex items-center gap-6 md:gap-8 text-xs md:text-sm uppercase tracking-widest font-semibold">
                <a href="/plans/" class="text-gray-300 hover:text-white transition-colors">Plans</a>
                <a href="/#gallery" class="hidden sm:inline text-gray-300 hover:text-white transition-colors">Gallery</a>
                <a href="/#contact" class="bg-[#c2a67a] text-[#0f172a] px-5 py-3 hover:bg-white transition-colors">Get a Quote</a>
            </nav>
        </div>
    </header>
`;

const foot = () => `
    <footer class="bg-[#0f172a] text-gray-400 py-10 px-6">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-center md:text-left">
            <p class="text-sm">&copy; <span id="year">2026</span> Leavitt Building Group. All Rights Reserved.</p>
            <div class="flex gap-6 text-sm uppercase tracking-wider font-semibold">
                <a href="/" class="hover:text-white transition-colors">Home</a>
                <a href="/plans/" class="hover:text-white transition-colors">Plans</a>
                <a href="/privacy.html" class="hover:text-white transition-colors">Privacy</a>
                <a href="/terms.html" class="hover:text-white transition-colors">Terms</a>
            </div>
        </div>
        <p class="max-w-6xl mx-auto mt-6 text-xs text-gray-500 tracking-wider text-center md:text-left">MHBR 9796 | MHIC 161316 | PAHIC 212160</p>
    </footer>

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>
</body>
</html>
`;

/**
 * <picture> with the WebP first and the PNG as the fallback, carrying the real
 * pixel size so the browser reserves the space before the image loads.
 */
const picture = (img, { alt, cls, lazy = true }) => {
  const a = lazy ? ' loading="lazy" decoding="async"' : ' decoding="async"';
  return `<picture class="contents"><source srcset="/plans/img/${img.file}.webp" type="image/webp">` +
    `<img src="/plans/img/${img.file}.${img.ext || 'png'}" alt="${esc(alt)}" width="${img.width}" height="${img.height}"${a} class="${cls}"></picture>`;
};

/** Every sheet this model has, in the order they are shown. */
const sheets = (model) => model.pages.map((p) => ({ ...p, img: images[model.slug]?.[p.id] }))
  .filter((p) => p.img);

const floorsOf = (model) => sheets(model).filter((s) => !s.id.startsWith('elevation'));

/**
 * One factual sentence assembled from the data - no adjectives we cannot stand
 * behind. Doubles as the page's meta description, so it has to read like prose
 * rather than a spec dump.
 */
const blurb = (model) => {
  if (model.summary) return model.summary;
  const s = model.specs || {};
  const beds = s.beds ? `${String(s.beds).replace('-', '–')} bedrooms` : '';
  const shape = s.stories === 1 ? 'single-story' : 'two-story';
  const style = model.style ? `${model.style} ` : '';
  const sqft = s.sqft
    ? `${s.sqftFrom ? 'from ' : ''}${s.sqft.toLocaleString('en-US')} living square feet`
    : '';
  const garage = s.garage ? `a ${s.garage} garage` : '';

  const head = [`A ${shape} ${style}plan`, beds && `with ${beds}`].filter(Boolean).join(' ');
  const tail = [sqft, garage].filter(Boolean).join(' and ');
  return tail ? `${head}, ${tail}.` : `${head}.`;
};

// ---------------------------------------------------------------- model pages

for (const [i, model] of models.entries()) {
  const all = sheets(model);
  const elevation = all.find((s) => s.id === 'elevation');
  const rest = all.filter((s) => s !== elevation);
  const prev = models[(i - 1 + models.length) % models.length];
  const next = models[(i + 1) % models.length];
  // A model built from images has no brochure to download - The Storyteller
  // offers its photographs instead.
  const hasBrochure = !model.pages.every((p) => p.image);

  const description =
    `${model.name} floor plans and front elevation from Leavitt Building Group, ` +
    `custom home builders in Forest Hill, Maryland. ${blurb(model)}`.trim();

  const specRows = SPECS.map(([key, label, fmt]) => {
    const v = model.specs?.[key];
    const known = v !== null && v !== undefined && v !== '';
    return `                    <div class="border-t border-gray-200 py-4">
                        <dt class="text-[11px] font-bold uppercase tracking-[0.2em] text-gray-500 mb-1">${esc(label)}</dt>
                        <dd class="text-lg ${known ? 'text-[#0f172a] font-medium' : 'text-gray-400'}">${known ? esc(fmt(v, model.specs)) : 'On request'}</dd>${NOTE_FOR[key] && model.specs?.[NOTE_FOR[key]] ? `
                        <dd class="text-xs text-gray-500 mt-1">${esc(model.specs[NOTE_FOR[key]])}</dd>` : ''}
                    </div>`;
  }).join('\n');

  const sheetBlocks = rest.map((s) => `
            <figure class="mb-16">
                <h2 class="text-2xl md:text-3xl font-serif text-[#0f172a] mb-6">${esc(s.label)}</h2>
                ${picture(s.img, {
                  alt: `${model.name} ${s.label.toLowerCase()} drawing`,
                  cls: 'w-full h-auto bg-white border border-gray-200',
                })}
                <figcaption class="mt-3 text-sm text-gray-500 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1">
                    <span>Dashed outlines mark optional features available for this plan.</span>
                    <!-- At phone width the drawing is ~360px wide and the room labels are
                         unreadable. Opening the image itself is the zero-JavaScript way to
                         let someone pinch and zoom it. -->
                    <a href="/plans/img/${s.img.file}.${s.img.ext || 'png'}" target="_blank" rel="noopener"
                       class="text-[#c2a67a] font-medium hover:underline whitespace-nowrap">
                        Open full size<span class="sr-only"> image of the ${esc(model.name)} ${esc(s.label.toLowerCase())}</span>
                    </a>
                </figcaption>
            </figure>`).join('\n');

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE}/` },
      { '@type': 'ListItem', position: 2, name: 'Home Plans', item: `${SITE}/plans/` },
      { '@type': 'ListItem', position: 3, name: model.name, item: `${SITE}/plans/${model.slug}.html` },
    ],
  };

  const html = head({
    title: `${model.name} | Home Plans | Leavitt Building Group`,
    description,
    canonical: `/plans/${model.slug}.html`,
  }) + `
    <main class="max-w-6xl mx-auto px-6 py-14 md:py-20">

        <nav aria-label="Breadcrumb" class="mb-10 text-sm text-gray-500">
            <a href="/" class="hover:text-[#c2a67a]">Home</a>
            <span class="mx-2" aria-hidden="true">/</span>
            <a href="/plans/" class="hover:text-[#c2a67a]">Home Plans</a>
            <span class="mx-2" aria-hidden="true">/</span>
            <span class="text-[#0f172a]">${esc(model.name)}</span>
        </nav>

        <p class="text-[11px] font-bold uppercase tracking-[0.3em] text-[#c2a67a] mb-4">Home Plan</p>
        <h1 class="text-4xl md:text-6xl font-light text-[#0f172a] mb-6">
            The <span class="font-serif italic">${esc(model.name.replace(/^The\s+/i, ''))}</span>
        </h1>
        <p class="text-gray-600 text-lg max-w-2xl mb-6">${esc(blurb(model))}</p>
        ${model.specs?.price ? `<p class="mb-3">
            <span class="text-[11px] font-bold uppercase tracking-[0.2em] text-gray-500 block mb-1">Starting price</span>
            <span class="text-3xl md:text-4xl font-light text-[#0f172a]">${model.specs.priceFrom ? 'From ' : ''}${money(model.specs.price)}</span>
        </p>
        <p class="text-sm text-gray-500 max-w-2xl mb-12">${priceNote()}</p>` : `
        <p class="text-sm text-gray-500 max-w-2xl mb-12">Pricing for this plan is available on request.</p>`}

        ${elevation ? `
        <!-- The drawing carries its own caption, so no figcaption repeating it here.
             The alt text still names the elevation for anyone not seeing the image. -->
        <div class="mb-12">
            ${picture(elevation.img, {
              alt: `${model.name} front elevation - ${elevation.label}`,
              cls: 'w-full h-auto bg-white border border-gray-200',
              lazy: false,
            })}
        </div>` : ''}

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-10 lg:gap-16 mb-20">
            <div class="lg:col-span-2">
                <h2 class="text-2xl md:text-3xl font-serif text-[#0f172a] mb-2">At a glance</h2>
                <dl class="grid grid-cols-2 sm:grid-cols-3 gap-x-8">
${specRows}
                </dl>
                <p class="text-sm text-gray-500 mt-6 leading-relaxed">
                    Every plan here is a starting point. Room sizes, elevations and optional features
                    are adjusted to your lot and how you want to live &mdash; tell us what you have in mind
                    and we will price the version you actually want to build.
                </p>
            </div>

            <aside class="bg-white border border-gray-200 p-8 h-fit">
                <h2 class="text-xl font-serif text-[#0f172a] mb-4">Interested in this plan?</h2>
                <a href="/?plan=${encodeURIComponent(model.name)}#contact"
                   class="block w-full text-center bg-[#0f172a] text-white px-6 py-4 uppercase tracking-[0.2em] font-bold text-xs hover:bg-[#c2a67a] hover:text-[#0f172a] transition-colors mb-4">
                    Start with this plan
                </a>
                ${hasBrochure ? `<a href="/plans/pdf/${model.slug}.pdf" target="_blank" rel="noopener"
                   class="block w-full text-center border border-gray-300 px-6 py-4 uppercase tracking-[0.2em] font-bold text-xs text-[#0f172a] hover:border-[#c2a67a] hover:text-[#c2a67a] transition-colors">
                    Download the PDF
                </a>
                <p class="text-xs text-gray-500 mt-4">Opens the full brochure for ${esc(model.name)} in a new tab.</p>` : `<a href="/#gallery"
                   class="block w-full text-center border border-gray-300 px-6 py-4 uppercase tracking-[0.2em] font-bold text-xs text-[#0f172a] hover:border-[#c2a67a] hover:text-[#c2a67a] transition-colors">
                    See it built
                </a>
                <p class="text-xs text-gray-500 mt-4">Photographs of this home, inside and out.</p>`}
                <p class="text-sm text-gray-600 mt-6 pt-6 border-t border-gray-200">
                    Every Leavitt home includes
                    <a href="/plans/#included" class="text-[#c2a67a] font-medium hover:underline">the Leavitt Standard</a>
                    &mdash; quartz, Andersen&reg; windows, 9&rsquo; ceilings and more, at no upgrade cost.
                </p>
                <p class="text-sm text-gray-600 mt-4">
                    Prefer to talk it through?
                    <a href="tel:+18668326524" class="text-[#c2a67a] font-medium hover:underline">(866) 832-6524</a>
                </p>
            </aside>
        </div>

        <h2 class="sr-only">Drawings</h2>
${sheetBlocks}

        <nav aria-label="Other plans" class="border-t border-gray-200 pt-10 flex flex-col sm:flex-row justify-between gap-6 text-sm">
            <a href="/plans/${prev.slug}.html" class="group">
                <span class="block text-[11px] font-bold uppercase tracking-[0.2em] text-gray-500 mb-1">Previous plan</span>
                <span class="text-lg text-[#0f172a] group-hover:text-[#c2a67a] transition-colors">${esc(prev.name)}</span>
            </a>
            <a href="/plans/" class="self-center text-[#c2a67a] uppercase tracking-widest font-bold text-xs hover:underline">All plans</a>
            <a href="/plans/${next.slug}.html" class="group sm:text-right">
                <span class="block text-[11px] font-bold uppercase tracking-[0.2em] text-gray-500 mb-1">Next plan</span>
                <span class="text-lg text-[#0f172a] group-hover:text-[#c2a67a] transition-colors">${esc(next.name)}</span>
            </a>
        </nav>

    </main>

    <script type="application/ld+json">${JSON.stringify(jsonLd)}</script>
` + foot();

  writeFileSync(join(OUT, `${model.slug}.html`), html);
  console.log(`plans/${model.slug}.html  (${all.length} drawings)`);
}

// ----------------------------------------------------------------- index page

const cards = models.map((model) => {
  const elevation = sheets(model).find((s) => s.id === 'elevation');
  const floors = floorsOf(model).length;
  return `
                <a href="/plans/${model.slug}.html" class="group block bg-white border border-gray-200 hover:border-[#c2a67a] transition-colors">
                    <div class="aspect-[4/3] w-full overflow-hidden bg-white flex items-center justify-center p-4">
                        ${elevation ? picture(elevation.img, {
                          alt: `${model.name} front elevation`,
                          cls: 'max-h-full w-auto object-contain',
                        }) : '<span class="text-gray-400 text-sm">Elevation coming soon</span>'}
                    </div>
                    <div class="border-t border-gray-200 p-6">
                        <h3 class="text-2xl font-serif text-[#0f172a] group-hover:text-[#c2a67a] transition-colors">${esc(model.name)}</h3>
                        <p class="text-sm text-gray-500 mt-2">${floors} floor plan${floors === 1 ? '' : 's'}${model.specs?.stories === 1 ? ' &middot; Ranch' : ''}</p>
                        ${model.specs?.price ? `<p class="mt-3 text-lg text-[#0f172a]">${model.specs.priceFrom ? '<span class="text-sm text-gray-500">From</span> ' : ''}${money(model.specs.price)}</p>` : ''}${model.built ? `
                        <p class="mt-2 inline-block bg-[#0f172a] text-white text-[10px] font-bold uppercase tracking-[0.2em] px-3 py-1">Built &mdash; photographed</p>` : ''}
                        <span class="inline-block mt-4 text-[11px] font-bold uppercase tracking-[0.2em] text-[#c2a67a]">View plan &rarr;</span>
                    </div>
                </a>`;
}).join('\n');

const indexHtml = head({
  title: 'Home Plans | Leavitt Building Group',
  description:
    `Browse ${models.length} home plans from Leavitt Building Group, custom home builders in ` +
    'Forest Hill, Maryland. Front elevations, floor plans and downloadable brochures for each model.',
  canonical: '/plans/',
}) + `
    <main class="max-w-6xl mx-auto px-6 py-14 md:py-20">

        <nav aria-label="Breadcrumb" class="mb-10 text-sm text-gray-500">
            <a href="/" class="hover:text-[#c2a67a]">Home</a>
            <span class="mx-2" aria-hidden="true">/</span>
            <span class="text-[#0f172a]">Home Plans</span>
        </nav>

        <p class="text-[11px] font-bold uppercase tracking-[0.3em] text-[#c2a67a] mb-4">Where to begin</p>
        <h1 class="text-4xl md:text-6xl font-light text-[#0f172a] mb-6">
            Home <span class="font-serif italic">plans.</span>
        </h1>
        <p class="text-gray-600 text-lg max-w-2xl mb-4">
            A starting point, not a catalogue. Each of these plans has been built before and can be
            adapted &mdash; elevation, room sizes, optional spaces &mdash; to your lot and the way you
            want to live.
        </p>
        <p class="text-gray-600 max-w-2xl mb-6">
            Every sheet shows the optional features available for that model in dashed outline:
            in-law suites, conservatories, sunrooms, extended garages and finished lower levels.
        </p>
        <p class="text-sm text-gray-500 max-w-2xl mb-14">${priceNote(' Talk to us about your homesite and we will price the version you actually want to build.')}</p>

        <h2 class="sr-only">Available plans</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
${cards}
        </div>

${standardSection()}

        <section class="mt-20 bg-[#0f172a] text-white p-10 md:p-14">
            <h2 class="text-3xl md:text-4xl font-light mb-4">
                Don&rsquo;t see the one? <span class="font-serif italic text-gray-300">We draw from scratch too.</span>
            </h2>
            <p class="text-gray-400 max-w-2xl mb-8">
                These are the plans we have on the shelf. If none of them is quite right, bring us a
                sketch, a photograph, or nothing at all &mdash; a fully custom home starts the same way.
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
                <a href="/#contact" class="bg-[#c2a67a] text-[#0f172a] px-8 py-4 uppercase tracking-[0.2em] font-bold text-xs hover:bg-white transition-colors text-center">
                    Start the conversation
                </a>
                <a href="tel:+18668326524" class="border border-white/20 px-8 py-4 uppercase tracking-[0.2em] font-bold text-xs hover:bg-white hover:text-[#0f172a] transition-colors text-center">
                    (866) 832-6524
                </a>
            </div>
        </section>

    </main>
` + foot();

mkdirSync(OUT, { recursive: true });
writeFileSync(join(OUT, 'index.html'), indexHtml);
console.log(`plans/index.html  (${models.length} models)`);

// ------------------------------------------------- homepage teaser dimensions
// index.html is hand-maintained, but the three teaser cards point at generated
// images whose size changes whenever a crop does. Typing those numbers by hand
// went stale the first time a crop moved, so they are synced from the manifest
// instead. Only width/height on plans/img/* are touched; nothing else in the
// file is rewritten, and re-running with no change is a no-op.
{
  const indexPath = join(ROOT, 'index.html');
  const before = readFileSync(indexPath, 'utf8');
  const byFile = Object.fromEntries(
    Object.values(images).flatMap((m) => Object.values(m).map((i) => [i.file, i])));

  let patched = 0;
  const after = before.replace(
    /(<img\s[^>]*?src="plans\/img\/([^".]+)\.png"[^>]*?)width="(\d+)" height="(\d+)"/g,
    (whole, lead, file, w, h) => {
      const real = byFile[file];
      if (!real) {
        console.error(`  ! index.html references plans/img/${file}.png, which is not generated`);
        return whole;
      }
      if (+w === real.width && +h === real.height) return whole;
      patched++;
      return `${lead}width="${real.width}" height="${real.height}"`;
    });

  if (after !== before) writeFileSync(indexPath, after);
  console.log(patched
    ? `index.html  (${patched} teaser image size${patched === 1 ? '' : 's'} synced)`
    : 'index.html  (teaser image sizes already correct)');
}

// -------------------------------------------------------------- sitemap
// Generated here because this script already knows every plan URL. The static
// pages are listed explicitly; success.html is left out on purpose, it is
// noindex. If a new top-level page is added to the site, add it to STATIC.
const STATIC = ['/', '/plans/', '/privacy.html', '/terms.html'];
const urls = [...STATIC, ...models.map((m) => `/plans/${m.slug}.html`)];

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${SITE}${u}</loc></url>`).join('\n')}
</urlset>
`;
writeFileSync(join(ROOT, 'sitemap.xml'), sitemap);
console.log(`sitemap.xml  (${urls.length} URLs)`);

writeFileSync(join(ROOT, 'robots.txt'), `User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap.xml
`);
console.log('robots.txt');
