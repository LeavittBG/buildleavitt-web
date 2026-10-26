# Leavitt Job Pricing — handoff

Written October 14, 2026 for whoever continues the job-pricing app in a new session with no access to the chat that built it. Read this first, then the pricing-app section at the end of `CLAUDE.md`.

The app is **not in this repository and must never be added to it**: the repository is public (it is the buildleavitt.com website). This file therefore holds no prices, margins, fees, client names or vendor names. Those live only in the app's database and in the backup Kyle keeps.

## 1. Goal

Kyle Leavitt (owner of Leavitt Building Group, a custom home builder in Forest Hill, MD) hard-bids every job. That is accurate but takes two to three weeks. He wants a defensible price in minutes, from his own history, and then firms it up with bids only where they matter. He also wants every line item of a custom home in front of him, because items that appear on one home in five or six were being missed.

What exists: **Leavitt Job Pricing**, a private web app on Kyle's claude.ai account. It is a claude.ai Artifact (one HTML page) with the artifact's shared database behind it, pinned to his sidebar. It:

- prices a new home, an addition, a detached garage or a finished basement from the job's inputs (plan, areas, counts, lot conditions), using median unit rates per cost code from his past jobs;
- lets each line run in one of five modes: auto (from history), bid (a sub's number), allowance, manual, excluded;
- carries a 248-item scope checklist (included / extra, yes / no / to be decided, with conditions driven by the inputs) so nothing is forgotten;
- requests and tracks bids (bid packages per trade, Gmail send from inside the app, a bid board across estimates);
- holds county fee tables and lot flags on a Lot tab;
- tracks the contract (snapshots, change orders, allowances, draw schedule);
- prints a branded proposal with the Leavitt Standard list and the required price qualifier;
- keeps a plan library (17 Leavitt models with brochure takeoffs, plus custom plans with uploaded files), a materials price index, estimate comparison, a quick quote, and settings.

Users: Kyle only, so far. The artifact's `user` capability records who edited what if he shares it with his team.

## 2. Status

### Done and live (artifact version 9, published October 11, 2026)

- Every feature above is built, published and seeded. Kyle's last word on it: "everything is working correctly".
- Four headless-Chromium test suites pass against the published build (see §6). The last one drives the page against a mock of the live database, with latency and frozen snapshot bodies, because that is where the real bugs were.
- The database holds 9 collections and about 880 documents: settings (1), cost codes (62), past jobs (8), vendors (118), options (200), estimates (1, an empty draft), checklist (248), plans (17), materials (225). Kyle has edited settings and two past jobs in the app since seeding; those edits are only in the database.
- Delivered to Kyle in chat: an offline copy of the page (`leavitt-job-pricing-v4.html`, same build as version 9), a backup of the live database (`leavitt-pricing-backup-2026-10-11.json`), a 40-page user guide (`Leavitt-Job-Pricing-User-Guide.pdf`), the county-fee and plan-takeoff research notes, and on October 14 the editable source tree (`leavitt-job-pricing-source-2026-10-14.zip`).

### Half-done or unverified

- **Gmail send from the app** is wired (the artifact's `mcp` capability names the Gmail server and its `send_message` tool) but has never been exercised with a real email. Test it once with Kyle watching. If the connector is missing, the app falls back to a mail-app link and a "Mark as requested" button.
- **County fee tables** came from official 2025–2026 fee schedules fetched on October 10, 2026. Rows are tagged with a confidence; medium and low rows should be replaced as Kyle's actual permit invoices come in.
- **Plan takeoffs** were measured from the brochure PDFs in `assets-src/plans/`. Three carry notes: The Innovator's first/second floor split is estimated (its brochure wrongly calls the second floor optional; a corrected brochure is coming), The Poet's published square footage is well above what the drawings measure, and The Expressionist II draws larger than its published figure.
- **"Count from photos"** (the plan takeoff helper that reads uploaded drawings) works in tests but has had little real use.

### Known limits (not bugs)

- No live parcel lookup. IQLand has no Maryland coverage, county GIS sites are unreachable from the sandbox, and Zapier is not connected. Lot facts are entered by hand.
- Plan file uploads work only inside claude.ai for the artifact's owner or an editor. The offline copy hides the upload control.
- The offline HTML copy keeps its own data in the browser (localStorage). It does not sync with the live artifact; "Restore from backup" under Settings loads a backup into it.
- Fonts load from Google Fonts; with no internet the page falls back to system fonts.

## 3. Decisions, and what was tried and failed

### Decisions (Kyle's unless noted)

- **Platform:** a single-page claude.ai Artifact with the artifact database, not a Netlify site and not this repository. Reason: the data is private, there is no server to run, and Kyle opens it from his sidebar. Published as a private artifact; sharing is Kyle's call.
- **Figures only from Leavitt's own data.** Every default dollar amount in the database came from Kyle's budgets, quotes, price sheets or an official fee schedule. Nothing is estimated or invented. A line with no usable figure shows as missing and asks for a number or a bid rather than guessing.
- **Project types.** Kyle: "an addition still requires permits. It may also require tying into a septic." So additions keep the permit lines, get septic/water/electrical tie-in, demolition, matching and interior-patch checklist items (`add-*` ids), and drop whole-house lines (well, driveway, construction loan) by default. Rates for an addition come from past additions first, then from new-home jobs flagged as a fallback; a borrowed whole-house lump sum is shown as missing instead of being applied to a small job.
- **Brand look, no template effects.** Same rules as the website: content visible from first paint, no loaders or animations, Leavitt navy and gold, Inter and Playfair Display. Dark mode follows the system.
- **Bedrooms, baths and garage** on the plan presets match the brochure covers exactly; square footage and starting prices come from the website's plan data (`src/plans.json`), though the site itself no longer shows the prices.
- **Public repository rule (established while building):** nothing of the app, its data, backups or figures goes into this repository. Only this handoff and the `CLAUDE.md` rules.

### Tried and failed (and what fixed it)

- **"The buttons don't work"** (reported twice). Root cause: the live database delivers frozen snapshot bodies. The app mutated them in strict mode, threw, and the click handlers were never bound. Fix: clone every body on arrival in `onSnapshot`. Guarded by `ui-test-4-db.cjs`, which deep-freezes the mock bodies and reopens the estimate from the list.
- **Lost clicks under live saves.** A snapshot echo from one save landed between a second click and its debounced write and the stale document was re-sent. Fix: a `pendingDocs` overlay of unsaved local edits, change detection with a stable string, and renders deferred while a dialog is open or a field has focus.
- **Build script mangled `$$`.** `String.replace` with a string replacement turned `$$` into `$` and broke `$(...).forEach`. Fix: function-form replacements in `build.mjs`.
- **Left inputs panel would not scroll** until the long right panel reached the bottom. Fix: the sticky panel got its own `max-height` and `overflow-y: auto`.
- **"â€”" in the offline copy.** Safari read the local file as Latin-1. Fix: `<meta charset="utf-8">` as the page's first line.
- **Fee defaults matched the wrong words** ("dwelling" contains "well"). Fix: word-boundary regexes in `feeDefault`.
- **Quick quote priced a small addition like a house** because a preset plan's garage and porch areas stayed in the inputs. Fix: choosing a plan zeroes the area and count fields first; build months come from the project type.
- **New estimate opened on the Contract tab** because the tab was remembered across estimates. Fix: reset the tab when the open estimate changes.
- **A custom plan did not appear after saving** because the name was validated before the form was read. Fix: read, then validate.
- **The guide's dialog screenshot spanned pages** (8,634 px tall). Fix: crop to the dialog and a `figure.tall` max-height rule.
- **Parcel data from IQLand, county GIS or Zapier:** none reachable or covering Maryland. Dropped; lot facts are manual.

## 4. Design specs and style

There is no video in this project; this section records the app's visual contract instead.

- **Fonts:** Inter 400/500/600/700 for the interface, Playfair Display 600 for the wordmark. Loaded by one Google Fonts link in `build.mjs`; 14 px base size, line height 1.45, tabular numerals on money (`.num`).
- **Palette (light), defined as tokens on `:root` in `style.css`:** background `#f6f5f2`, paper `#ffffff` and `#efede8`, text `#16213a` / `#4b5569` / `#7d8597`, rules `#ddd9d0` / `#cdc8bc`, navy `#0f172a` with `#f6f5f2` text on it, gold `#c2a67a`, gold ink `#8a6d35`, pale gold `#f3ecdd`, good `#2f7d4f`, warn `#b7791f`, bad `#b23b3b`. A dark theme redefines the same tokens under `prefers-color-scheme: dark` (guarded by `:root:not([data-theme="light"])`) and under `:root[data-theme="dark"]`.
- **Shape:** 6 px radius, one soft shadow token, fine 1 px rules, no filled hover states.
- **Layout:** a fixed top bar that always shows the estimate's price; below it a two-column workspace, job inputs on the left (sticky, scrolls on its own) and the budget grid on the right, stacking on a phone. Every edit happens in a modal dialog; the budget rows carry a mode select (minimum width 104 px so "History" is not clipped).
- **Logo:** `favicon-192.png` from this repository, inlined as base64 at build time where `features.js` says `__BRAND_LOGO__`.
- **Printed pieces:** the proposal is Letter size with a branded header (company facts from the `COMPANY` constant in `features.js`), the Leavitt Standard list and the price qualifier; it is printed from the browser. The user guide is Letter, rendered by Playwright with page numbers in the footer.
- **File formats:** the app is one HTML file (about 300 KB). Backups are JSON shaped `{ collection: { id: document } }` for the nine collections. Budgets and draw schedules export as CSV. Plan files are stored through the artifact's asset store as `{id, name, contentType, sizeBytes, at}` and served from `/_blob/<id>`; email attachments are base64 and capped at 18 MB.

## 5. File map

### In this repository (public)

- `HANDOFF.md` — this file. `netlify.toml` deletes it from the deploy and `tests/markup.test.js` checks that.
- `CLAUDE.md` — website rules, plus the pricing-app rules at the end.
- `favicon-192.png` — the logo the app build inlines.
- `src/plans.json` and `assets-src/plans/*.pdf` — the source of the 17 plan presets (published figures and brochures).

### Where the app lives

- **The artifact.** Find it with the Artifact tool's `list` action; the title is "Leavitt Job Pricing" and it is pinned in Kyle's sidebar. Version 9 is current. Read its page with `action: "read"`; the HTML you get back is the whole app.
- **Its database** (9 collections, read and written with the `ArtifactData` tool, see §6).
- **Declared capabilities** (restate all of them, in full, on any publish that passes the field): `{"db": {}, "user": {"scopes": ["profile"]}, "downloads": true, "sample": {"images": true}, "assets": {}, "mcp": {"servers": [{"server": "Gmail", "tools": ["send_message"]}]}}`. Runtime contract 0.2.75 (leave `contract` out when publishing to keep it).

### The source tree (in Kyle's zip; the sandbox it was written in is gone)

```
app/engine.js        pure calculation engine, exported as window.Pricing (no DOM)
app/app.js           store, routing, estimate screen, library, scope, settings; has a /* FEATURES */ marker
app/features.js      spliced in at the marker: bids, bid board, lot, contract, draws, proposal,
                     quick quote, takeoff, plans, materials, compare, settings extras, edit history
app/style.css        tokens, layout, components, dark theme
app/build.mjs        css + engine + app(+features) -> app/leavitt-job-pricing.html
app/ui-test.cjs      flow test on the localStorage backend (seeded from seed/backup.json)
app/ui-test-2.cjs    the October feature set
app/ui-test-3.cjs    project types and custom plans
app/ui-test-4-db.cjs the live-database race and frozen-body guard (mock db capability)
app/shots-guide.cjs  screenshots for the user guide -> guide/img
app/dbg.cjs          tiny page-error probe
guide/guide.html     the user guide (placeholders <!--CODES--> and __LOGO__)
guide/render.cjs     fills the placeholders from seed/backup.json and prints the PDF
seed/build_seed.py   builds seed/<collection>/<id>.json and seed/backup.json from data/
seed/checklist_items.py  the master scope checklist (248 items)
data/                extraction outputs: county fees, plan takeoffs, materials, jobs, subs,
                     options, quotes, the Leavitt Standard, and SUMMARY-*.md notes per set
scripts/             one-off parsers that produced data/ from Kyle's spreadsheets and PDFs
```

Engine API (`window.Pricing`): `BASES, MODES, DEFAULT_SETTINGS, PROJECT_TYPES, projectType, appliesTo, quantities, libraryRates, computeEstimate, priceRange, drawSchedule, scopeState, scopeAmount, evalCond, money, fmtRate, fmtQty, budgetCsv, toCsv, median, num`.

Sections of `features.js`, in order: shared "who still needs to price what", Bids tab, bid-request modal, bid board, Lot tab, Contract tab, draw schedule, branded proposal, quick quote, plan takeoff from photos, Plans page, materials, compare, settings extras, who edited what.

### The database

| Collection | Doc id | Fields |
|---|---|---|
| settings | `main` | bidDays, contingencyPct, countyFees[], defaultMonths, escalationPct, markupPct, proposalValidDays, rateSource, realtorPct, riskContingency, roofFactor, shapeFactor, staleMonths, tiers[], wallHeight |
| codes | the cost code, e.g. `100` | basis, bidFirst, code, finish, name, notes, order, phase, phaseOrder, subcodes, trade, applies |
| jobs | `j-<client>-<year>` | address, client, contract, date, excluded, inputs, lines, markupPct, name, notes, source, total, type |
| vendors | `v-<slug>` | codes, company, contact, email, notes, phone, trade |
| options | the option code, e.g. `BA-01` | category, code, included, name, price, priceFrom, selectBy, unit |
| estimates | random id | address, allowances, bids, changeOrders, client, contingencyPct, createdAt, inputs, lines, lot, markupPct, name, notes, options, realtor, status, updatedAt, versions, files |
| checklist | item id (`add-*` for addition items) | applies, basis, code, defaultAmount, freq, kind, label, note, order, unit |
| plans | the website slug, or `p-…` for custom plans | confidence, inputs, measured, name, notes, printed, published, takeoff, custom, type, files |
| materials | `m-<slug>` | category, first, history, label, last, n, unit, vendor |

`applies` arrays on codes and checklist items name the project types they belong to; absent means all. Jobs marked `excluded` stay out of the new-home rate library but still feed their own project type.

### Files Kyle holds (ask him for them)

`leavitt-job-pricing-v4.html` (offline copy, same build as version 9), `leavitt-pricing-backup-2026-10-11.json`, `Leavitt-Job-Pricing-User-Guide.pdf`, `county-fees-2026-10-10.md`, `plan-takeoffs-2026-10-10.md`, `leavitt-job-pricing-source-2026-10-14.zip`. He also has the original spreadsheets and brochures in Google Drive (`LBG Home Brochures`).

## 6. How to run it

Everything below runs in a session's scratchpad directory, never inside this repository's tree.

### Recover the sources

1. Best: ask Kyle to attach `leavitt-job-pricing-source-2026-10-14.zip` and unzip it in the scratchpad. The tests, build script and guide exist only there.
2. Otherwise rebuild from the page: `Artifact read` on the artifact returns the HTML. Its `<style>` block is `style.css`, the first `<script>` is `engine.js`, the second is `app.js` with `features.js` already spliced in. Treat that second script as the whole `app.js`, drop the splice from `build.mjs`, and you can rebuild. The tests cannot be recovered this way.

### Build

```
cd app && node build.mjs          # writes app/leavitt-job-pricing.html (~300 KB)
```

`build.mjs` reads the logo from `/home/user/buildleavitt-web/favicon-192.png`; with the repository elsewhere, change that path or the logo comes out blank.

### Test (all four must pass before any publish)

```
cd app
NODE_PATH=/opt/node-tools/node_modules node ui-test.cjs
NODE_PATH=/opt/node-tools/node_modules node ui-test-2.cjs
NODE_PATH=/opt/node-tools/node_modules node ui-test-3.cjs
NODE_PATH=/opt/node-tools/node_modules node ui-test-4-db.cjs leavitt-job-pricing.html
```

They use Playwright's Chromium at `/opt/pw-browsers/chromium` and seed from `../seed/backup.json`. If `seed/` is missing, a backup downloaded from the app's Settings page has the same shape and works in its place. Each test writes a `wrapped.html` that reproduces the artifact service's page skeleton; keep that wrapper if you add a test.

### User guide

```
cd app && NODE_PATH=/opt/node-tools/node_modules node shots-guide.cjs     # screenshots -> guide/img
cd ../guide && NODE_PATH=/opt/node-tools/node_modules node render.cjs      # -> Leavitt-Job-Pricing-User-Guide.pdf
```

### Seed data (only to rebuild from the raw extraction; the live database is the truth)

```
cd seed && python3 -I build_seed.py       # -> seed/<collection>/<id>.json and seed/backup.json
```

Never load seed output over the live database wholesale: Kyle has edited settings and jobs there. Merge, or skip documents whose version is above 1.

### Publish

Use the Artifact tool: `action: "publish"`, `file_path` = `app/leavitt-job-pricing.html`, `url` = the artifact's link, `icon` omitted (keeps the current one), `capabilities` omitted unless they change (then pass the full set from §5). A publish is refused until the session has read or published that artifact once; a refusal hands back the live version, so read it first. Then send Kyle a fresh offline copy and, when asked, a backup assembled from the live database.

### Read or fix the database from a session

The `ArtifactData` tool, with the artifact's URL: `get` (collection + doc id), `list` (collection), `query`; writes `set` (full replace), `update` (merge), `delete`, `batch` (several writes, at most 50 per call). Writes to existing documents need the document's current version as a pin; read first. Never run a write to find out what a result looks like.

### Offline copy

Open the HTML file in any browser. Data stays in that browser's localStorage under `ljp:<collection>`; Settings → "Restore from backup…" loads a backup JSON, "Download backup (JSON)" writes one.

## 7. Gotchas

- **This repository is public.** No app code, data, backups, screenshots or figures here, ever. Netlify publishes the repository root, so a new top-level file that is not part of the site must also be added to the `rm -rf` list in `netlify.toml` and to `mustGo` in `tests/markup.test.js` (done for `HANDOFF.md`).
- **The sandbox is wiped between sessions.** The app's editable sources exist only in Kyle's zip and in the published page.
- **Database bodies arrive frozen and shared.** Clone before editing (the store does this in `onSnapshot`). `set` replaces the whole document; one write per document at a time; documents are limited to 256 KiB; a bad body fails with `invalid_argument`.
- **Renders are deferred** while a dialog is open or a field has focus (`renderPending`), so a snapshot never wipes what Kyle is typing. Keep that when adding screens.
- **`features.js` is spliced before the boot section** of `app.js` so its constants exist when `render()` first runs. Use function-form `replace` in the build (the `$$` bug).
- **Rates by project type:** same-type jobs first, new-home rates as a flagged fallback; `lumpNeedsNumber` turns a borrowed whole-house lump sum into a missing line. Preset plans zero the area and count inputs when chosen.
- **Fee matching uses word boundaries** (`\bwell\b`, `\btaps?\b`, `\bperc\b`, `\baccess\b`); keep it that way.
- **Gmail sends are real.** They go through the viewer's Gmail connector (claude.ai Settings → Connectors). Never retry a send unattended; attachments over 18 MB are refused.
- **The page is wrapped** by the artifact service in its own `<html>`/`<head>`/`<body>`; the page file itself starts with `<meta charset="utf-8">`, which the offline copy needs for Safari.
- **Local file quirks:** the upload control hides outside claude.ai; fonts need internet.
- **No API keys exist anywhere in the app.** Gmail is the viewer's connector; the database and asset store are the artifact's own. The website's analytics ids are documented in `CLAUDE.md`, not in the app.

## 8. Next steps and open questions

1. **Where should the source live long-term?** Options: a private GitHub repository (not this one), Kyle's Google Drive, or attaching the zip to each session. Kyle decides; until then, ask him for the zip at the start of a session.
2. **Send one real bid request** from the app with Kyle present, to prove the Gmail path, then try a reminder from the bid board.
3. **Replace estimated fee rows** as actual permit invoices arrive; add any jurisdiction Kyle builds in that is not in the table (Settings has a JSON editor for the fee table).
4. **The Innovator:** when the corrected brochure arrives, redo its takeoff (it is a two-story home) and update the website's plan data at the same time.
5. **More past jobs.** Medians from 8 jobs are thin. After each closed job, "Save as past job" from its estimate; rates improve with every one, and codes go stale after the `staleMonths` setting.
6. **Confirm with Kyle** whether the addition checklist items should carry default amounts from a past addition, or keep asking for a number each time.
7. **Team access,** if he wants it: he shares the artifact; the app already records editors by profile.

## 9. Working preferences (Kyle)

- Plain language, in terms of his workflow (jobs, subs, permits, draws). He is not a developer; never show him code or internal names.
- He reports bugs with a screenshot and a sentence. Reproduce in headless Chromium, write the guarding test, confirm it fails on the old build, then fix and publish a new version. Tell him what changed in one or two lines.
- After a fix he expects a fresh offline copy and, on request, a backup from the live database.
- Ask before anything outward-facing or hard to undo (emails, sharing, deleting data, pull requests). For website changes he reviews the Netlify deploy preview and says "merge".
- Never invent a number. Say "needs a figure" and ask.
- Do not rewrite his wording in the About text on the website; the same respect applies to any proposal language he supplies.
