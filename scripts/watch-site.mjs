#!/usr/bin/env node
/*
 * Nightly watch over buildleavitt.com (October 2026).
 *
 * Nobody tells a small business when its website has been tampered with. This
 * script notices, by checking four things that should only ever change on
 * purpose, and listing every difference it finds:
 *
 *  1. The live site is, byte for byte, what this repository says it is. Every
 *     file Netlify publishes (the files git tracks, minus the ones netlify.toml
 *     deletes from the deploy) is downloaded and compared with the committed
 *     copy. The one difference accepted is Netlify's own rewrite of the contact
 *     form's opening tag, which it makes when it wires the form up.
 *  2. The Tag Manager container the pages load (GTM-PHGFM247) still has the
 *     version, the kinds of tags and variables, and the web addresses it had
 *     when BASELINE below was last reviewed. Tag Manager is the one place code
 *     can be added to every page without touching GitHub or Netlify.
 *  3. The domain's DNS: the name servers, the mail servers, where the bare
 *     domain and www point, and that SPF and DMARC are still there and no
 *     weaker than before.
 *  4. Netlify is still the one serving the site, over HTTPS, with the plain
 *     HTTP and www addresses redirecting to it.
 *
 * .github/workflows/watch-site.yml runs this every night and turns the report
 * into a GitHub issue that mentions Kyle, so it reaches him by email. When a
 * change was deliberate (a new Tag Manager version, a DNS change) the baseline
 * below is updated in a pull request; until then every night reports it again,
 * which is the point.
 *
 *   node scripts/watch-site.mjs                      check, print, exit 1 on problems
 *   node scripts/watch-site.mjs --report report.md   also write the report as Markdown
 *   node scripts/watch-site.mjs --only site,dns      run some of the checks
 *   node scripts/watch-site.mjs --site http://...    compare against another address
 *
 * No dependencies beyond Node 20. tests/watch-site.test.js checks that it
 * notices a changed page and does not cry wolf about Netlify's form rewrite.
 */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const USER_AGENT = 'buildleavitt-site-watch (https://github.com/LeavittBG/buildleavitt-web)';

/*
 * What the site is supposed to look like from outside. Reviewed October 24,
 * 2026. Change it only to record a change that was made on purpose.
 */
export const BASELINE = {
  site: 'https://buildleavitt.com',

  // Netlify rewrites the contact form's opening tag when it wires the form up:
  // it drops its own attributes, sorts the rest and shortens the action. The
  // live tag is accepted in place of the committed one; any other form tag is
  // reported, because a form pointed at another address is how leads get stolen.
  form: {
    repo: '<form class="space-y-8" name="contact" method="POST" action="/success.html" data-netlify="true" netlify-honeypot="bot-field">',
    live: "<form action='/success' class='space-y-8' method='POST' name='contact'>",
  },

  gtm: {
    container: 'GTM-PHGFM247',
    // Published container version. A new version means someone published.
    version: '2',
    // Every kind of tag, variable and template in the container: the Google tag
    // and three built-in variables (event, URL, referrer). Nothing custom.
    functions: ['__e', '__f', '__googtag', '__u'],
    // Web addresses the container's code may mention. All Google. Anything
    // else would be a tag sending visitors' data to a stranger.
    hosts: [
      'google.com', 'googletagmanager.com', 'google-analytics.com', 'googlesyndication.com',
      'doubleclick.net', 'googleadservices.com', 'youtube.com', 'gstatic.com', 'googleapis.com',
      'cct.google',
    ],
  },

  dns: {
    domain: 'buildleavitt.com',
    ns: ['aragorn.ns.cloudflare.com', 'jillian.ns.cloudflare.com'],
    mx: ['aspmx.l.google.com', 'alt1.aspmx.l.google.com', 'alt2.aspmx.l.google.com', 'alt3.aspmx.l.google.com', 'alt4.aspmx.l.google.com'],
    // Netlify's load balancer, which the bare domain points at.
    apex: ['75.2.60.5', '99.83.231.61'],
    www: 'buildleavitt.netlify.app',
    // SPF must keep naming Google Workspace and end with ~all or -all.
    spfIncludes: '_spf.google.com',
    // DMARC may be made stricter without a report, never weaker than this.
    // Raise it to 'quarantine' and then 'reject' as the policy moves.
    dmarcAtLeast: 'none',
  },
};

const problem = (area, title, detail = '') => ({ area, title, detail: String(detail).trim() });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Fetch with a timeout and two retries, as a nightly job over the open internet needs. */
async function get(url, fetchImpl, { redirect = 'follow', accept } = {}) {
  let lastError;
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await fetchImpl(url, {
        redirect,
        headers: { 'cache-control': 'no-cache', 'user-agent': USER_AGENT, ...(accept ? { accept } : {}) },
        signal: AbortSignal.timeout(60000),
      });
    } catch (e) {
      lastError = e;
      await sleep(1500 * (attempt + 1));
    }
  }
  throw lastError;
}

// ---------------------------------------------------------------------------
// 1. The live files against the repository
// ---------------------------------------------------------------------------

/**
 * The files Netlify publishes: everything git tracks, minus what netlify.toml
 * deletes from the deploy and the dotfiles and config Netlify never serves.
 */
export function siteFiles(root = ROOT) {
  const toml = fs.readFileSync(path.join(root, 'netlify.toml'), 'utf8');
  const command = (toml.match(/^\s*command\s*=\s*"([^"]*)"/m) || [])[1] || '';
  const removed = ((command.match(/rm -rf ([^&;]*)/) || [])[1] || '').trim().split(/\s+/).filter(Boolean);
  const skip = new Set([...removed, 'netlify.toml']);
  const tracked = execFileSync('git', ['-C', root, 'ls-files', '-z'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 })
    .split('\0').filter(Boolean);
  return tracked.filter((f) => {
    const top = f.split('/')[0];
    return !skip.has(top) && !top.startsWith('.');
  });
}

/** Netlify's rewrite of the contact form tag, undone, so the page can be compared. */
export function acceptNetlifyForm(live, form = BASELINE.form) {
  const text = live.toString('utf8');
  if (!text.includes(form.live)) return live;
  return Buffer.from(text.replace(form.live, form.repo), 'utf8');
}

const TEXT_FILE = /\.(html|css|js|mjs|json|xml|txt|vtt|svg|webmanifest)$/i;

/** A short, readable account of how two copies of a file differ. */
export function describeDifference(file, expected, live) {
  if (!TEXT_FILE.test(file)) return `repository: ${expected.length} bytes, live: ${live.length} bytes`;
  const a = expected.toString('utf8').split('\n');
  const b = live.toString('utf8').split('\n');
  const n = Math.max(a.length, b.length);
  let first = -1;
  let count = 0;
  for (let i = 0; i < n; i++) {
    if (a[i] !== b[i]) { count++; if (first < 0) first = i; }
  }
  const cut = (s) => (s === undefined ? '(no such line)' : s.length > 200 ? s.slice(0, 200) + '…' : s);
  return `${count} line${count === 1 ? '' : 's'} differ, first at line ${first + 1}:\n` +
    `  repository: ${cut(a[first])}\n  live:       ${cut(b[first])}`;
}

/**
 * Download every published file and compare it with the committed copy.
 * Returns { problems, checked, total, bytes }.
 */
export async function checkSite({ site = BASELINE.site, root = ROOT, files, fetchImpl = fetch, concurrency = 8, form = BASELINE.form } = {}) {
  files = files || siteFiles(root);
  const base = site.replace(/\/$/, '');
  const differs = [];
  const unreachable = [];
  let checked = 0;
  let bytes = 0;
  const queue = [...files];

  async function worker() {
    while (queue.length) {
      const file = queue.shift();
      const url = base + '/' + file.split('/').map(encodeURIComponent).join('/');
      const expected = fs.readFileSync(path.join(root, file));
      let res;
      try {
        res = await get(url, fetchImpl);
      } catch (e) {
        unreachable.push(problem('site', `${file}: could not be fetched`, `${url}\n${e.message}`));
        continue;
      }
      if (res.status !== 200) {
        differs.push(problem('site', `${file}: answered HTTP ${res.status} instead of 200`, url));
        continue;
      }
      let live = Buffer.from(await res.arrayBuffer());
      checked++;
      bytes += live.length;
      if (/\.html$/i.test(file)) live = acceptNetlifyForm(live, form);
      if (!live.equals(expected)) {
        differs.push(problem('site', `${file}: the live copy differs from the repository`, describeDifference(file, expected, live)));
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, files.length) }, worker));

  differs.sort((x, y) => x.title.localeCompare(y.title));
  const problems = differs.slice(0, 30);
  if (differs.length > 30) problems.push(problem('site', `and ${differs.length - 30} more files differ`));
  if (unreachable.length > 10) {
    problems.push(problem('site', `${unreachable.length} of ${files.length} files could not be fetched at all`,
      'The site may be down or unreachable from GitHub\'s network. First of them:\n' + unreachable[0].detail));
  } else {
    problems.push(...unreachable);
  }
  return { problems, checked, total: files.length, bytes };
}

// ---------------------------------------------------------------------------
// 2. The Tag Manager container
// ---------------------------------------------------------------------------

/** What a gtm.js file says about its container: version, kinds of tags, hosts. */
export function inspectGtm(text) {
  const version = (text.match(/"resource"\s*:\s*\{\s*"version"\s*:\s*"([^"]+)"/) || [])[1] || null;
  const functions = [...new Set([...text.matchAll(/"function"\s*:\s*"(__[A-Za-z0-9_]+)"/g)].map((m) => m[1]))].sort();
  const hostPattern = /(?:https?:)?\/\/([a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+)(?=[/"'?:;)\s\\]|$)/gi;
  const hosts = [...new Set([...text.matchAll(hostPattern)].map((m) => m[1].toLowerCase()))].sort();
  return { version, functions, hosts };
}

const RISKY_FUNCTIONS = {
  __html: 'a Custom HTML tag, which can run any code on every page',
  __jsm: 'a Custom JavaScript variable, which can run any code on every page',
  __img: 'a Custom Image tag, which can send visitors\' data anywhere',
};

/** Compare a gtm.js file with the baseline. Returns { problems, found }. */
export function checkGtm(text, base = BASELINE.gtm) {
  const problems = [];
  const found = inspectGtm(text);
  if (found.version !== base.version) {
    problems.push(problem('tagmanager', `The Tag Manager container is now version ${found.version ?? '(unknown)'}; the baseline is version ${base.version}`,
      'Someone published the container. If that was you, update BASELINE.gtm in scripts/watch-site.mjs. ' +
      'If not, open Tag Manager, Admin, Container Notifications and Versions, see what changed and who published it, and remove their access.'));
  }
  for (const fn of found.functions) {
    if (base.functions.includes(fn)) continue;
    const why = RISKY_FUNCTIONS[fn] || (fn.startsWith('__cvt_') ? 'a custom template, which can run any code on every page' : 'a kind of tag or variable the baseline does not know');
    problems.push(problem('tagmanager', `The Tag Manager container contains ${fn}: ${why}`,
      'The site needs only the Google tag. Open the container\'s Versions page and look at what was added, by whom.'));
  }
  for (const host of found.hosts) {
    if (base.hosts.some((h) => host === h || host.endsWith('.' + h))) continue;
    problems.push(problem('tagmanager', `The Tag Manager container mentions ${host}, which is not a Google address`,
      'A tag that talks to a non-Google address is sending something about your visitors somewhere else.'));
  }
  return { problems, found };
}

export async function fetchGtm({ container = BASELINE.gtm.container, fetchImpl = fetch } = {}) {
  const url = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(container)}`;
  const res = await get(url, fetchImpl);
  if (res.status !== 200) throw new Error(`${url} answered HTTP ${res.status}`);
  return res.text();
}

// ---------------------------------------------------------------------------
// 3. DNS
// ---------------------------------------------------------------------------

const RECORD_TYPES = { A: 1, NS: 2, CNAME: 5, MX: 15, TXT: 16 };

/** Look a name up over DNS-over-HTTPS, at Google then Cloudflare, so the answer is the same from anywhere. */
export async function resolveDoh(name, type, fetchImpl = fetch) {
  const urls = [
    `https://dns.google/resolve?name=${encodeURIComponent(name)}&type=${type}`,
    `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(name)}&type=${type}`,
  ];
  let lastError;
  for (const url of urls) {
    try {
      const res = await fetchImpl(url, { headers: { accept: 'application/dns-json', 'user-agent': USER_AGENT }, signal: AbortSignal.timeout(20000) });
      if (!res.ok) throw new Error(`${url} answered HTTP ${res.status}`);
      const json = await res.json();
      return (json.Answer || []).filter((a) => a.type === RECORD_TYPES[type]).map((a) => a.data);
    } catch (e) {
      lastError = e;
    }
  }
  throw lastError;
}

const unquote = (txt) => String(txt).replace(/"\s*"/g, '').replace(/^"|"$/g, '');
const hostname = (v) => String(v).toLowerCase().replace(/\.$/, '');

/** Compare the domain's DNS with the baseline. Returns { problems, found }. */
export async function checkDns({ base = BASELINE.dns, resolve = resolveDoh } = {}) {
  const problems = [];
  const found = {};
  const sameSet = (a, b) => JSON.stringify([...a].map(hostname).sort()) === JSON.stringify([...b].map(hostname).sort());

  async function expect(label, name, type, expected, pick = (d) => d) {
    try {
      const got = (await resolve(name, type)).map(pick);
      found[label] = got.map(hostname);
      if (!sameSet(got, expected)) {
        problems.push(problem('dns', `${label} changed`, `expected: ${expected.join(', ')}\nfound:    ${got.map(hostname).join(', ') || '(nothing)'}`));
      }
    } catch (e) {
      problems.push(problem('dns', `${label}: could not be looked up`, e.message));
    }
  }

  await expect('Name servers (who answers for the domain)', base.domain, 'NS', base.ns);
  await expect('Mail servers', base.domain, 'MX', base.mx, (d) => d.split(/\s+/).pop());
  await expect(`Where ${base.domain} points`, base.domain, 'A', base.apex);
  await expect(`Where www.${base.domain} points`, 'www.' + base.domain, 'CNAME', [base.www]);

  try {
    const txt = (await resolve(base.domain, 'TXT')).map(unquote);
    const spf = txt.filter((t) => /^v=spf1\b/i.test(t));
    found.spf = spf;
    if (spf.length !== 1) {
      problems.push(problem('dns', spf.length ? 'There is more than one SPF record' : 'The SPF record is gone',
        spf.join('\n') || 'Without SPF, anyone can send mail that claims to come from @' + base.domain));
    } else {
      if (!spf[0].includes('include:' + base.spfIncludes)) problems.push(problem('dns', 'SPF no longer names Google Workspace as the sender', spf[0]));
      if (!/\s[-~]all\s*$/.test(spf[0])) problems.push(problem('dns', 'SPF no longer ends with ~all or -all', spf[0]));
    }
  } catch (e) {
    problems.push(problem('dns', 'SPF: could not be looked up', e.message));
  }

  try {
    const txt = (await resolve('_dmarc.' + base.domain, 'TXT')).map(unquote);
    const dmarc = txt.find((t) => /^v=DMARC1\b/i.test(t));
    const order = ['none', 'quarantine', 'reject'];
    const policy = dmarc ? (dmarc.match(/\bp=(none|quarantine|reject)\b/i) || [])[1]?.toLowerCase() : undefined;
    found.dmarc = dmarc || null;
    if (!dmarc || !policy) {
      problems.push(problem('dns', 'The DMARC record is gone or has no policy', txt.join('\n') || '(nothing at _dmarc.' + base.domain + ')'));
    } else if (order.indexOf(policy) < order.indexOf(base.dmarcAtLeast)) {
      problems.push(problem('dns', `The DMARC policy was weakened to p=${policy}`, `The baseline requires at least p=${base.dmarcAtLeast}.\n${dmarc}`));
    }
  } catch (e) {
    problems.push(problem('dns', 'DMARC: could not be looked up', e.message));
  }

  return { problems, found };
}

// ---------------------------------------------------------------------------
// 4. HTTPS and who is serving
// ---------------------------------------------------------------------------

export async function checkHttps({ site = BASELINE.site, fetchImpl = fetch } = {}) {
  const problems = [];
  const host = new URL(site).host;
  try {
    const res = await get(site + '/', fetchImpl);
    if (res.status !== 200) problems.push(problem('https', `The homepage answered HTTP ${res.status}`, site + '/'));
    const server = res.headers.get('server') || '';
    if (!/netlify/i.test(server)) {
      problems.push(problem('https', `The site is no longer served by Netlify (server header: ${server || 'none'})`,
        'If the site was moved on purpose, update scripts/watch-site.mjs. If not, someone has changed where the domain points.'));
    }
    if (!res.headers.get('strict-transport-security')) {
      problems.push(problem('https', 'The Strict-Transport-Security header is missing',
        'Netlify sends it for every site with HTTPS; without it browsers may be talked into plain HTTP.'));
    }
  } catch (e) {
    problems.push(problem('https', 'The homepage could not be fetched', e.message));
  }
  for (const from of [`http://${host}/`, `https://www.${host}/`]) {
    try {
      const res = await get(from, fetchImpl, { redirect: 'manual' });
      const to = res.headers.get('location') || '';
      const redirected = res.status >= 301 && res.status <= 308 && (to === site + '/' || to === site);
      if (!redirected) problems.push(problem('https', `${from} does not redirect to ${site}/`, `HTTP ${res.status}${to ? ' to ' + to : ''}`));
    } catch (e) {
      problems.push(problem('https', `${from} could not be fetched`, e.message));
    }
  }
  return { problems };
}

// ---------------------------------------------------------------------------
// Running and reporting
// ---------------------------------------------------------------------------

const AREAS = {
  site: 'The live pages and files',
  tagmanager: 'The Tag Manager container',
  dns: 'The domain\'s DNS',
  https: 'HTTPS and who is serving the site',
};

/** Run the chosen checks. Returns { problems, notes, when }. */
export async function runChecks({ only = ['site', 'gtm', 'dns', 'https'], site = BASELINE.site, root = ROOT, fetchImpl = fetch, log = () => {} } = {}) {
  const problems = [];
  const notes = [];
  const when = new Date();

  if (only.includes('site')) {
    log('Comparing the live files with the repository…');
    const r = await checkSite({ site, root, fetchImpl });
    problems.push(...r.problems);
    notes.push(`${r.checked} of ${r.total} published files downloaded from ${site} and compared with the repository (${(r.bytes / 1048576).toFixed(1)} MB).`);
  }
  if (only.includes('gtm')) {
    log('Reading the Tag Manager container…');
    try {
      const r = checkGtm(await fetchGtm({ fetchImpl }));
      problems.push(...r.problems);
      notes.push(`Tag Manager container ${BASELINE.gtm.container} is version ${r.found.version}, with ${r.found.functions.join(', ')}, mentioning ${r.found.hosts.join(', ')}.`);
    } catch (e) {
      problems.push(problem('tagmanager', 'The Tag Manager container could not be fetched', e.message));
    }
  }
  if (only.includes('dns')) {
    log('Looking up DNS…');
    const r = await checkDns({ resolve: (n, t) => resolveDoh(n, t, fetchImpl) });
    problems.push(...r.problems);
    notes.push(`DNS: name servers ${(r.found['Name servers (who answers for the domain)'] || []).join(', ') || '?'}; www points at ${(r.found[`Where www.${BASELINE.dns.domain} points`] || []).join(', ') || '?'}; SPF ${r.found.spf?.[0] || '?'}; DMARC ${r.found.dmarc || '?'}.`);
  }
  if (only.includes('https')) {
    log('Checking HTTPS and the redirects…');
    const r = await checkHttps({ site, fetchImpl });
    problems.push(...r.problems);
    notes.push('HTTPS, the Netlify server header and the redirects from http:// and www were checked.');
  }
  return { problems, notes, when };
}

/** The report as Markdown, written for the GitHub issue and the run summary. */
export function renderReport({ problems, notes, when }, site = BASELINE.site) {
  const lines = [];
  const stamp = when.toISOString().replace('T', ' ').replace(/\.\d+Z$/, ' UTC');
  if (problems.length === 0) {
    lines.push(`**No differences.** ${site} is exactly what the repository says it is, as of ${stamp}.`);
  } else {
    lines.push(`**${problems.length} difference${problems.length === 1 ? '' : 's'}** between ${site} as served and what this repository and its baseline expect, as of ${stamp}.`);
    for (const area of Object.keys(AREAS)) {
      const mine = problems.filter((p) => p.area === area);
      if (!mine.length) continue;
      lines.push('', `### ${AREAS[area]}`);
      for (const p of mine) {
        lines.push('', `- **${p.title}**`);
        if (p.detail) lines.push('', '  ```', ...p.detail.split('\n').map((l) => '  ' + l), '  ```');
      }
    }
    lines.push('', '### What to do', '',
      '- **If you made this change yourself**, nothing is wrong. Update the baseline in `scripts/watch-site.mjs` through a pull request so tomorrow\'s run is quiet.',
      '- **If you did not**, treat it as a break-in until shown otherwise:',
      '  1. Netlify, Deploys: is there a deploy you did not make? "Publish deploy" on the last good one puts the site back in seconds.',
      '  2. GitHub, the commit list on main: anything you did not merge?',
      '  3. Tag Manager, Versions: anything published that was not you?',
      '  4. Cloudflare, DNS and the audit log: any record or login you do not recognise?',
      '  5. On whichever account it was: sign out all sessions, change the password, check two-factor is on and remove anyone who should not be there.');
  }
  lines.push('', '### What was checked', '', ...notes.map((n) => `- ${n}`));
  return lines.join('\n') + '\n';
}

async function main() {
  const args = process.argv.slice(2);
  const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const site = opt('--site') || BASELINE.site;
  const only = (opt('--only') || 'site,gtm,dns,https').split(',').map((s) => s.trim());
  const report = opt('--report');

  const result = await runChecks({ only, site, log: (m) => console.log(m) });
  const md = renderReport(result, site);

  console.log('');
  if (result.problems.length === 0) {
    console.log('ok  no differences');
  } else {
    for (const p of result.problems) {
      console.log(`FAIL  [${p.area}] ${p.title}`);
      if (p.detail) console.log(p.detail.split('\n').map((l) => '        ' + l).join('\n'));
    }
  }
  console.log('');
  for (const n of result.notes) console.log('note  ' + n);

  if (report) fs.writeFileSync(report, md);
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, '## Site watch\n\n' + md);
  process.exit(result.problems.length ? 1 : 0);
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  main().catch((e) => { console.error(e); process.exit(2); });
}
