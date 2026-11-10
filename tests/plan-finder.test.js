/*
 * The plan finder (October 2026).
 *
 * Seventeen plans used to be seventeen cards and nothing else: the homepage
 * showed three of them, eighth on the page, and /plans/ showed them all with no
 * way to narrow them but opening each one. The finder asks three questions
 * (stories, bedrooms, size) and shows the plans that fit; "Start with this
 * plan" takes the choice to the contact form.
 *
 * What this guards:
 *  - every figure a card is matched on (stories, bedrooms, square feet) is the
 *    one in src/plans.json, on both pages, so a plan can never be filed under
 *    the wrong answer;
 *  - the homepage shows its six featured plans before any question is answered
 *    and all seventeen are in the page, so with scripts blocked the plans are
 *    still there (and /plans/ shows all seventeen);
 *  - the answers narrow the list to exactly the plans the data says fit, the
 *    count is right, nothing fits gives the "we draw from scratch" way out, and
 *    the homepage's "See all" link carries the answers to /plans/, which opens
 *    already narrowed;
 *  - "Start with this plan" on the homepage names the plan in the form without
 *    a reload, and chooses Semi-Custom Home;
 *  - every plan page offers three other plans like it, none of them itself.
 */
const { ROOT, launch, serveRepo } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const { models } = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/plans.json'), 'utf8'));
const minBeds = (b) => parseInt(String(b), 10) || 0;
const band = (sqft) => (sqft < 3000 ? 'under-3000' : sqft <= 4000 ? '3000-4000' : 'over-4000');
const fits = (m, f) => (!f.stories || String(m.specs.stories) === f.stories)
  && (!f.beds || minBeds(m.specs.beds) >= Number(f.beds))
  && (!f.size || band(m.specs.sqft) === f.size);
const read = (file) => new JSDOM(fs.readFileSync(path.join(ROOT, file), 'utf8')).window.document;

(async () => {
  console.log('\n== the cards carry the data, on both pages ==');
  for (const file of ['index.html', 'plans/index.html']) {
    const d = read(file);
    const root = d.getElementById('plan-finder');
    ok(!!root, `${file}: has the finder`);
    if (!root) continue;
    const cards = [...root.querySelectorAll('[data-plan]')];
    ok(cards.length === models.length, `${file}: one card per plan (${cards.length} of ${models.length})`);
    const wrong = [];
    for (const m of models) {
      const c = cards.find((x) => x.getAttribute('data-plan') === m.slug);
      if (!c) { wrong.push(`${m.slug}: no card`); continue; }
      if (c.getAttribute('data-stories') !== String(m.specs.stories)) wrong.push(`${m.slug}: stories ${c.getAttribute('data-stories')}`);
      if (c.getAttribute('data-beds') !== String(minBeds(m.specs.beds))) wrong.push(`${m.slug}: beds ${c.getAttribute('data-beds')}`);
      if (c.getAttribute('data-sqft') !== String(m.specs.sqft)) wrong.push(`${m.slug}: sqft ${c.getAttribute('data-sqft')}`);
      if (!c.querySelector(`a[href="/plans/${m.slug}.html"]`)) wrong.push(`${m.slug}: no link to its page`);
      const start = c.querySelector('[data-start-plan]');
      const want = `/?plan=${encodeURIComponent(m.name)}&interest=Semi-Custom%20Home#contact`;
      if (!start || start.getAttribute('data-start-plan') !== m.name || start.getAttribute('href') !== want) wrong.push(`${m.slug}: start link ${start && start.getAttribute('href')}`);
      if (/\$/.test(c.textContent)) wrong.push(`${m.slug}: price on card`);
    }
    ok(wrong.length === 0, `${file}: every card matches plans.json and links on` + (wrong.length ? ' - ' + wrong.slice(0, 5).join(' | ') : ''));
    for (const k of ['stories', 'beds', 'size']) {
      const radios = [...root.querySelectorAll(`input[type="radio"][name="finder-${k}"]`)];
      ok(radios.length >= 3 && radios[0].value === '' && radios[0].hasAttribute('checked') && radios.slice(1).every((r) => !r.hasAttribute('checked')),
        `${file}: the ${k} question starts on "any" (${radios.length} options)`);
    }
    const visible = cards.filter((c) => !c.classList.contains('hidden')).map((c) => c.getAttribute('data-plan'));
    if (file === 'index.html') {
      ok(visible.length === 6, `homepage: six plans show before a question is answered (${visible.length})`);
      ok(visible[0] === 'the-pioneer-i', `homepage: The Pioneer I, the house in the hero photo, leads (${visible[0]})`);
      ok(/<!-- plan-finder:start -->[\s\S]*<!-- plan-finder:end -->/.test(fs.readFileSync(path.join(ROOT, file), 'utf8')), 'homepage: the finder sits between its build markers');
      ok(!!d.querySelector('#plans [data-finder-more][href="/plans/"]'), 'homepage: links to all the plans');
      ok(!!d.querySelector('#hero a[href="#plans"]'), 'homepage: the hero button opens the finder');
    } else {
      ok(visible.length === models.length, `/plans/: all ${models.length} plans show before a question is answered (${visible.length})`);
    }
    const empty = root.querySelector('[data-finder-empty]');
    ok(!!empty && empty.classList.contains('hidden') && !!empty.querySelector('a[href="/?interest=Custom%20Home%20Build#contact"]'),
      `${file}: the "nothing fits" message waits hidden and offers a custom home`);
  }

  console.log('\n== every plan page offers plans like it ==');
  {
    const bad = [];
    for (const m of models) {
      const d = read(`plans/${m.slug}.html`);
      const h = [...d.querySelectorAll('h2')].find((x) => /Plans like this one/.test(x.textContent));
      const links = h ? [...h.parentElement.querySelectorAll('.plan-card a[href^="/plans/"]')].map((a) => a.getAttribute('href')) : [];
      const others = [...new Set(links)].filter((l) => l !== '/plans/');
      if (!h || others.length !== 3 || others.includes(`/plans/${m.slug}.html`)) bad.push(`${m.slug}: ${others.join(', ') || 'none'}`);
    }
    ok(bad.length === 0, `each of ${models.length} plan pages shows three other plans` + (bad.length ? ' - ' + bad.slice(0, 3).join(' | ') : ''));
  }

  // ------------------------------------------------------------------ browser
  const b = await launch();
  const site = await serveRepo();
  const answer = async (p, key, value) => p.click(`#plan-finder label:has(input[name="finder-${key}"][value="${value}"])`);
  const shown = (p) => p.evaluate(() => [...document.querySelectorAll('#plan-finder [data-plan]')].filter((c) => !c.classList.contains('hidden')).map((c) => c.getAttribute('data-plan')));
  const status = (p) => p.evaluate(() => document.querySelector('#plan-finder [data-finder-status]').textContent.trim());

  console.log('\n== the questions narrow the plans ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = []; p.on('pageerror', (e) => errs.push(e.message));
    await p.goto(`${site.base}/`, { waitUntil: 'load' });
    await answer(p, 'stories', '2'); await answer(p, 'beds', '4'); await answer(p, 'size', 'over-4000');
    const want = models.filter((m) => fits(m, { stories: '2', beds: '4', size: 'over-4000' })).map((m) => m.slug).sort();
    const got = (await shown(p)).sort();
    ok(want.length > 0 && want.length <= 6 && JSON.stringify(got) === JSON.stringify(want), `two stories, 4+, over 4,000: shows exactly ${want.join(', ')} (got ${got.join(', ')})`);
    ok((await status(p)) === `${want.length} plans match.`, `and says so (${await status(p)})`);

    await answer(p, 'stories', '1');
    const none = models.filter((m) => fits(m, { stories: '1', beds: '4', size: 'over-4000' }));
    ok(none.length === 0, 'no plan is a one-story 4+ bedroom over 4,000 sq ft (the data has none)');
    ok((await shown(p)).length === 0, 'one story, 4+, over 4,000: no card shows');
    const empty = await p.evaluate(() => { const e = document.querySelector('#plan-finder [data-finder-empty]'); return !e.classList.contains('hidden') && e.getBoundingClientRect().height > 0; });
    ok(empty && /No plan matches/.test(await status(p)), `the "nothing fits" message shows with the custom-home way out (${await status(p)})`);

    await answer(p, 'stories', ''); await answer(p, 'beds', ''); await answer(p, 'size', '');
    const back = await shown(p);
    ok(back.length === 6 && back[0] === 'the-pioneer-i', `back to "any": the six featured plans again (${back.length})`);
    ok(/Six of our 17 plans/.test(await status(p)), `and the opening line (${await status(p)})`);

    // More matches than the homepage shows: capped at six, with the rest a link away.
    await answer(p, 'stories', '2');
    const two = models.filter((m) => fits(m, { stories: '2' }));
    const more = await p.evaluate(() => { const a = document.querySelector('#plan-finder [data-finder-more]'); return { text: a.textContent.trim(), href: a.getAttribute('href') }; });
    ok((await shown(p)).length === Math.min(6, two.length) && two.length > 6, `two stories: six of the ${two.length} shown`);
    ok(more.text === `See all ${two.length} matching plans` && more.href === '/plans/?stories=2', `the link offers the rest with the answer in it (${more.text} -> ${more.href})`);
    ok(/Showing 6 of the/.test(await status(p)), `and the line says six of ${two.length} (${await status(p)})`);
    ok(!/[?&]stories=/.test(p.url()), 'the homepage address is left alone (?plan= belongs to the form there)');

    // The link opens /plans/ already narrowed, and /plans/ keeps its answers in the address.
    await p.click('#plan-finder [data-finder-more]');
    await p.waitForURL(/\/plans\/\?stories=2$/);
    ok((await p.evaluate(() => document.querySelector('#plan-finder input[name="finder-stories"]:checked').value)) === '2', '/plans/ opens with "Two stories" chosen');
    ok((await shown(p)).length === two.length, `/plans/ shows all ${two.length} two-story plans`);
    await answer(p, 'beds', '4');
    const twoFour = models.filter((m) => fits(m, { stories: '2', beds: '4' }));
    ok((await shown(p)).length === twoFour.length && /[?&]beds=4/.test(p.url()) && /[?&]stories=2/.test(p.url()), `adding "4 or more" narrows to ${twoFour.length} and the address follows (${new URL(p.url()).search})`);
    ok(errs.length === 0, 'no script errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await p.close();
  }

  console.log('\n== "Start with this plan" hands the plan to the form ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(`${site.base}/`, { waitUntil: 'load' });
    const before = p.url();
    await p.click('#plan-finder [data-start-plan="The Visionary"]');
    // The page scrolls smoothly (html { scroll-behavior: smooth }), so wait for it to arrive.
    await p.waitForFunction(() => Math.abs(document.getElementById('contact').getBoundingClientRect().top) < 200, null, { timeout: 5000 }).catch(() => {});
    const r = await p.evaluate(() => ({
      plan: document.getElementById('contact-plan').value,
      note: document.getElementById('contact-plan-note').getBoundingClientRect().height > 0 && document.getElementById('contact-plan-name').textContent,
      interest: (document.querySelector('input[name="Interest"]:checked') || {}).value,
      step1: document.getElementById('contact-step-1').getBoundingClientRect().height > 0,
      nearForm: Math.abs(document.getElementById('contact').getBoundingClientRect().top) < 200,
    }));
    ok(p.url() === before, 'no reload: the address is unchanged');
    ok(r.plan === 'The Visionary' && r.note === 'The Visionary', `the form names the plan (${r.plan})`);
    ok(r.interest === 'Semi-Custom Home', `and Semi-Custom Home is chosen (${r.interest})`);
    ok(r.step1 && r.nearForm, 'and the form is in view at step 1');
    await p.close();
  }

  console.log('\n== without script, the plans are still there ==');
  {
    const ctx = await b.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(`${site.base}/`, { waitUntil: 'load' });
    ok((await shown(p)).length === 6 && await p.locator('#plan-finder a[href="/plans/the-pioneer-i.html"]').first().isVisible(), 'homepage: six plan cards show with JS disabled');
    await p.goto(`${site.base}/plans/`, { waitUntil: 'load' });
    ok((await shown(p)).length === models.length, `/plans/: all ${models.length} cards show with JS disabled`);
    await ctx.close();
  }

  await site.close();
  await b.close();
  console.log(fail === 0 ? '\nAll plan finder checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
