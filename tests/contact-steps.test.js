/*
 * The contact form in two steps (October 2026).
 *
 * The form used to ask for everything at once - name and email at the top,
 * then two drop-downs and a note - under one "Submit Inquiry" button. Now the
 * easy questions come first (what kind of project, roughly what budget, as
 * choices to tap) and name and email come last, once the visitor has already
 * said what they want. It is still one Netlify form.
 *
 * What this guards:
 *  - the fields and values Netlify receives are exactly the ones it recorded
 *    before: the same names (Name, Email, Phone, Interest, Budget, Details,
 *    Plan) and the same Interest and Budget strings, so nothing changes in the
 *    submissions, and every field is in the deployed HTML;
 *  - both steps are in the page and shown without script; with it, one at a
 *    time, and step 2 cannot be reached until a project type and a budget are
 *    chosen;
 *  - ?plan= and ?interest= still land in the form, and show in the summary.
 */
const { ROOT, launch, serveRepo } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const INTERESTS = ['Custom Home Build', 'Semi-Custom Home', 'Large-Scale Renovation', 'Home Addition', 'Other / Unsure'];
const BUDGETS = ['$250,000 – $500,000', '$500,000 – $750,000', '$750,000 – $1 million', '$1 million – $2 million', '$2 million and above', 'Not sure yet'];

(async () => {
  console.log('\n== the form Netlify sees ==');
  {
    const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
    const d = new JSDOM(html).window.document;
    const form = d.querySelector('form[name="contact"][data-netlify="true"]');
    ok(!!form && form.getAttribute('method') === 'POST' && form.getAttribute('action') === '/success.html', 'the Netlify form is still there, posting to the thank-you page');
    const names = [...new Set([...form.querySelectorAll('[name]')].map((e) => e.getAttribute('name')))].sort();
    ok(JSON.stringify(names) === JSON.stringify(['Budget', 'Details', 'Email', 'Interest', 'Name', 'Phone', 'Plan', 'bot-field', 'form-name']),
      `the fields are the ones Netlify records (${names.join(', ')})`);
    const values = (name) => [...form.querySelectorAll(`input[name="${name}"]`)].map((r) => r.value);
    ok(JSON.stringify(values('Interest')) === JSON.stringify(INTERESTS), `Project Interest offers exactly ${INTERESTS.join(' / ')}`);
    ok(JSON.stringify(values('Budget')) === JSON.stringify(BUDGETS), `Estimated Budget offers exactly the six ranges, lowest $250,000`);
    ok(form.querySelector('input[name="Interest"][required]') && form.querySelector('input[name="Budget"][required]')
      && form.querySelector('input[name="Name"][required]') && form.querySelector('input[name="Email"][required]'), 'project type, budget, name and email are required');
    const s1 = d.getElementById('contact-step-1'), s2 = d.getElementById('contact-step-2');
    ok(s1 && s2 && form.contains(s1) && form.contains(s2) && !s1.classList.contains('hidden') && !s2.classList.contains('hidden'),
      'both steps are inside the form and neither starts hidden in the markup');
    ok(s1.querySelector('input[name="Interest"]') && s1.querySelector('input[name="Budget"]') && !s1.querySelector('input[name="Name"]')
      && s2.querySelector('input[name="Name"]') && s2.querySelector('input[name="Email"]') && s2.querySelector('button[type="submit"]'),
      'step 1 asks the project questions, step 2 asks for contact details and sends');
  }

  // ------------------------------------------------------------------ browser
  const b = await launch();
  const site = await serveRepo();
  const visible = (p, id) => p.evaluate((id) => { const e = document.getElementById(id); return !!e && e.getBoundingClientRect().height > 0; }, id);

  console.log('\n== one step at a time ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = []; p.on('pageerror', (e) => errs.push(e.message));
    await p.goto(`${site.base}/#contact`, { waitUntil: 'load' });
    ok(await visible(p, 'contact-step-1') && !await visible(p, 'contact-step-2'), 'the form opens on step 1 with step 2 out of sight');
    await p.click('#contact-continue');
    ok(await visible(p, 'contact-step-error') && !await visible(p, 'contact-step-2'), 'Continue with nothing chosen explains what is needed and stays on step 1');
    await p.click('label[for="contact-interest-renovation"]');
    await p.click('#contact-continue');
    ok(await visible(p, 'contact-step-error') && !await visible(p, 'contact-step-2'), 'a project type alone is not enough');
    await p.click('label[for="contact-budget-500"]');
    ok(!await visible(p, 'contact-step-error'), 'the message clears as soon as the budget is chosen');
    await p.click('#contact-continue');
    await p.waitForTimeout(300);
    const r = await p.evaluate(() => ({
      s1: document.getElementById('contact-step-1').getBoundingClientRect().height > 0,
      s2: document.getElementById('contact-step-2').getBoundingClientRect().height > 0,
      summary: document.getElementById('contact-summary-text').textContent.trim(),
      focused: document.activeElement && document.activeElement.id,
      formTop: document.getElementById('contact-form').getBoundingClientRect().top,
    }));
    ok(!r.s1 && r.s2, 'with both chosen, Continue shows step 2 and hides step 1');
    ok(r.summary === 'Large-Scale Renovation · $500,000 – $750,000', `step 2 repeats the choices (${r.summary})`);
    ok(r.focused === 'contact-name' && r.formTop >= 0 && r.formTop < 200, `the name field has focus and the form is in view (top ${Math.round(r.formTop)}px)`);
    await p.fill('#contact-name', 'Test Person');
    await p.fill('#contact-email', 'test@buildleavitt.com');
    const data = await p.evaluate(() => Object.fromEntries(new FormData(document.getElementById('contact-form'))));
    ok(data.Interest === 'Large-Scale Renovation' && data.Budget === '$500,000 – $750,000' && data.Name === 'Test Person' && data['form-name'] === 'contact' && data.Plan === '',
      `what would be sent carries both steps (${Object.keys(data).join(', ')})`);
    await p.click('#contact-back');
    ok(await visible(p, 'contact-step-1') && !await visible(p, 'contact-step-2'), 'Change goes back to step 1');
    ok((await p.evaluate(() => document.querySelector('input[name="Budget"]:checked').value)) === '$500,000 – $750,000', 'with the choices kept');
    ok(errs.length === 0, 'no script errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await p.close();
  }

  console.log('\n== arriving with a plan ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(`${site.base}/?plan=The%20Poet&interest=Semi-Custom%20Home#contact`, { waitUntil: 'load' });
    const r = await p.evaluate(() => ({
      note: document.getElementById('contact-plan-note').getBoundingClientRect().height > 0,
      plan: document.getElementById('contact-plan').value,
      interest: (document.querySelector('input[name="Interest"]:checked') || {}).value,
    }));
    ok(r.note && r.plan === 'The Poet' && r.interest === 'Semi-Custom Home', `the plan is named and Semi-Custom Home chosen (${JSON.stringify(r)})`);
    await p.click('label[for="contact-budget-1m"]');
    await p.click('#contact-continue');
    const summary = await p.evaluate(() => document.getElementById('contact-summary-text').textContent.trim());
    ok(summary === 'Semi-Custom Home · $1 million – $2 million · starting from The Poet', `the summary names the plan (${summary})`);
    await p.close();
  }

  console.log('\n== without script, the whole form is there ==');
  {
    const ctx = await b.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(`${site.base}/`, { waitUntil: 'load' });
    ok(await visible(p, 'contact-step-1') && await visible(p, 'contact-step-2') && await p.locator('#contact-form button[type="submit"]').isVisible(),
      'both steps and the send button show with JS disabled');
    await ctx.close();
  }

  await site.close();
  await b.close();
  console.log(fail === 0 ? '\nAll contact form checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
