#!/usr/bin/env node
// Builds one static HTML profile card per creator, plus a gallery page, from
// the same data as index.json. Self-contained pages: inline CSS, no build step.
//
//   node tools/build-cards.mjs [rootDir] --repo <owner/name> --out <dir>

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildIndex } from './build-index.mjs';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const safeUrl = (u) => (/^https:\/\//i.test(u ?? '') ? u : '');

// Stable per-creator hue, so a person's card looks the same on every rebuild.
export function hueFor(slug) {
  let h = 0;
  for (const c of slug) h = (h * 31 + c.codePointAt(0)) % 360;
  return h;
}

export const initials = (name) => name.split(/\s+/).filter(Boolean).map((w) => w[0]).slice(0, 2).join('').toUpperCase() || '?';

const firstSentence = (s) => (s.replace(/\s+/g, ' ').match(/^.*?[.!?](\s|$)/)?.[0] ?? s).trim();
const words = (k) => k.replace(/-/g, ' ');

const FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800&display=swap" rel="stylesheet">';

const CSS = `
:root{--paper:#f3f5f8;--card:#fff;--ink:#16203a;--slate:#5a6378;--line:#dfe3ea}
.hue{--tint:hsl(var(--h) 70% 94%);--accent:hsl(var(--h) 62% 36%);--band:hsl(var(--h) 55% 30%);--band-ink:hsl(var(--h) 75% 80%)}
@media (prefers-color-scheme:dark){:root{--paper:#0e1424;--card:#161e33;--ink:#e8ecf4;--slate:#9aa3b8;--line:#2a3450}.hue{--tint:hsl(var(--h) 35% 20%);--accent:hsl(var(--h) 75% 72%);--band:hsl(var(--h) 45% 22%);--band-ink:hsl(var(--h) 55% 52%)}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.55 "Schibsted Grotesk",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.page{max-width:720px;margin:0 auto;padding:40px 16px 64px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.band{position:relative;height:168px;background:var(--band);overflow:hidden}
.band p{margin:0;position:absolute;inset:-6px -12px;color:var(--band-ink);font-weight:800;font-size:44px;line-height:.98;letter-spacing:-.02em;word-spacing:.15em;opacity:.9}
.head{padding:0 32px 28px}
.avatar{position:relative;width:128px;height:128px;margin-top:-64px;border-radius:50%;border:5px solid var(--card);background:var(--tint);color:var(--accent);display:grid;place-items:center;font-weight:800;font-size:44px;overflow:hidden}
.avatar img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
h1{margin:16px 0 2px;font-size:32px;line-height:1.15;font-weight:800;letter-spacing:-.015em}
.role{margin:0;color:var(--slate)}
.headline{margin:16px 0 0;font-size:19px;line-height:1.45;max-width:36em}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:999px;font-weight:700;text-decoration:none;border:1.5px solid var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);color:var(--card)}
.btn svg{width:16px;height:16px;fill:currentColor}
section{border-top:1px solid var(--line);padding:24px 32px}
h2{margin:0 0 14px;font-size:15px;font-weight:700;color:var(--slate)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.chips li{background:var(--tint);color:var(--accent);padding:4px 12px;border-radius:999px;font-size:14px;font-weight:500}
.bio{margin:0;max-width:38em}
.skills{margin:0;padding:0;list-style:none}
.skills li{padding:16px 0;border-top:1px solid var(--line)}
.skills li:first-child{padding-top:0;border-top:0}
.skills h3{margin:0;font-size:18px;line-height:1.3}
.skills h3 a{color:var(--ink);text-decoration:none}
.skills h3 a:hover{text-decoration:underline}
.cat{color:var(--slate);font-size:14px}
.skills p{margin:4px 0 10px;color:var(--slate);max-width:38em}
.install{display:flex;align-items:center;gap:8px;max-width:100%}
.install code{flex:1;min-width:0;overflow-x:auto;white-space:nowrap;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:7px 10px;font:500 13px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace}
.install button{flex:none;font:700 13px "Schibsted Grotesk",system-ui,sans-serif;padding:7px 12px;border-radius:8px;border:1.5px solid var(--accent);background:transparent;color:var(--accent);cursor:pointer}
footer{margin-top:20px;color:var(--slate);font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin:24px 0 0;padding:0;list-style:none}
.grid a{display:block;height:100%;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.grid .band{height:64px}
.grid .band p{font-size:22px}
.grid .avatar{width:64px;height:64px;margin:-32px 0 0 20px;border-width:3px;font-size:22px}
.grid .who{padding:8px 20px 20px}
.grid strong{display:block;font-size:18px}
.grid span{color:var(--slate);font-size:14px}
@media (max-width:540px){.head,section{padding-left:20px;padding-right:20px}.band{height:128px}.band p{font-size:34px}.avatar{width:104px;height:104px;margin-top:-52px;font-size:36px}h1{font-size:27px}.headline{font-size:17px}}
@media (prefers-reduced-motion:no-preference){.card .band p{animation:drift 1.1s ease-out both}@keyframes drift{from{transform:translateX(-24px);opacity:0}}}
`;

const LINKEDIN_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>';

const COPY_JS = `<script>document.addEventListener('click',async(e)=>{const b=e.target.closest('button[data-copy]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copied';}catch{b.textContent='Select and copy';}setTimeout(()=>{b.textContent='Copy';},1800);});</script>`;

function avatar(e) {
  const img = safeUrl(e.avatarUrl) ? `<img src="${esc(e.avatarUrl)}" alt="" loading="lazy" onerror="this.remove()">` : '';
  return `<div class="avatar" aria-hidden="true">${esc(initials(e.name))}${img}</div>`;
}

// Expertise keywords repeated as display type; the band clips the overflow.
const band = (e) => `<div class="band" aria-hidden="true"><p>${esc(Array(3).fill(e.expertise.map(words).join(' ')).join(' '))}</p></div>`;

const page = (title, description, hue, body) => `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
${FONT}
<style>${CSS}</style>
</head>
<body class="hue" style="--h:${hue}">
${body}
</body>
</html>
`;

export function renderCard(expert, skills, { repo }) {
  const tree = `https://github.com/${repo}/tree/main`;
  const mine = skills.filter((s) => s.creator === expert.slug);
  const links = [
    safeUrl(expert.linkedinUrl) && `<a class="btn primary" href="${esc(expert.linkedinUrl)}" rel="noopener">${LINKEDIN_ICON}LinkedIn</a>`,
    safeUrl(expert.websiteUrl) && `<a class="btn" href="${esc(expert.websiteUrl)}" rel="noopener">${esc(expert.companyDomain || 'Website')}</a>`,
  ].filter(Boolean).join('');
  const skillItems = mine.map((s) => {
    const cmd = `npx skills add ${repo} --skill ${s.slug}`;
    return `<li>
<h3><a href="${tree}/skills/${esc(expert.slug)}/${esc(s.slug)}">${esc(s.title || s.slug)}</a> <span class="cat">${esc(s.category)}</span></h3>
<p>${esc(firstSentence(s.description))}</p>
<div class="install"><code>${esc(cmd)}</code><button type="button" data-copy="${esc(cmd)}" aria-label="Copy install command for ${esc(s.title || s.slug)}">Copy</button></div>
</li>`;
  }).join('\n');
  const all = `npx skills add ${repo}/skills/${expert.slug}`;

  return page(`${expert.name} | Agent Skills`, expert.headline, hueFor(expert.slug), `<main class="page">
<article class="card">
${band(expert)}
<div class="head">
${avatar(expert)}
<h1>${esc(expert.name)}</h1>
<p class="role">${esc(expert.title)}</p>
<p class="headline">${esc(expert.headline)}</p>
<div class="actions">${links}</div>
</div>
${expert.bio ? `<section><h2>About</h2><p class="bio">${esc(expert.bio)}</p></section>` : ''}
<section><h2>Skills you can install (${mine.length})</h2>
${mine.length ? `<ul class="skills">\n${skillItems}\n</ul>` : '<p class="bio">No skills published yet.</p>'}
${mine.length > 1 ? `<h2 style="margin-top:20px">Install all of them</h2><div class="install"><code>${esc(all)}</code><button type="button" data-copy="${esc(all)}" aria-label="Copy install command for all skills">Copy</button></div>` : ''}
</section>
<section><h2>Expertise</h2><ul class="chips">${expert.expertise.map((k) => `<li>${esc(words(k))}</li>`).join('')}</ul></section>
</article>
<footer>Part of <a href="https://github.com/${repo}">${esc(repo)}</a>. <a href="index.html">See every creator</a>.</footer>
</main>
${COPY_JS}`);
}

export function renderGallery(experts, { repo }) {
  const items = experts.map((e) => `<li class="hue" style="--h:${hueFor(e.slug)}"><a href="${esc(e.slug)}.html">${band(e)}${avatar(e)}<div class="who"><strong>${esc(e.name)}</strong><span>${esc(e.title)}</span></div></a></li>`).join('\n');
  return page('Creators | Agent Skills', `Profile cards for every creator in ${repo}.`, 220, `<main class="page">
<h1>Creators</h1>
<p class="role">${experts.length} people whose expertise you can install from <a href="https://github.com/${repo}">${esc(repo)}</a>.</p>
<ul class="grid">
${items}
</ul>
</main>`);
}

export function buildCards(rootDir, { repo }) {
  const { experts, skills } = buildIndex(rootDir, { repo, commit: 'main' });
  const pages = new Map(experts.map((e) => [`${e.slug}.html`, renderCard(e, skills, { repo })]));
  pages.set('index.html', renderGallery(experts, { repo }));
  return pages;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const flag = (name, dflt) => { const i = args.indexOf(name); return i === -1 ? dflt : args.splice(i, 2)[1]; };
  const repo = flag('--repo', process.env.GITHUB_REPOSITORY ?? 'agiea-brain/agent-skills');
  const out = path.resolve(flag('--out', 'cards'));
  const rootDir = path.resolve(args[0] ?? process.cwd());
  const pages = buildCards(rootDir, { repo });
  fs.mkdirSync(out, { recursive: true });
  for (const [name, html] of pages) fs.writeFileSync(path.join(out, name), html);
  console.log(`wrote ${pages.size - 1} cards + index.html to ${path.relative(process.cwd(), out) || '.'}`);
}
