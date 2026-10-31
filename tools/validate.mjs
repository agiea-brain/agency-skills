#!/usr/bin/env node
// Validates the agency-skills library layout and frontmatter. Zero dependencies.
//
//   node tools/validate.mjs [rootDir] [--taxonomy-root <dir>]
//
// Errors are one per line, for humans and agents alike:
//   <path>: <what is wrong> - <how to fix it>
//
// The core, validateFiles(), is in-memory so the web app can run the same
// checks on form data before a PR exists. validate() is the filesystem wrapper.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const SKILL_REQUIRED_KEYS = ['name', 'title', 'description', 'category'];
export const SKILL_FORBIDDEN_KEYS = ['prefix', 'slug', 'author', 'isDefault', 'license', 'featured', 'rank', 'installs'];
export const AUTHOR_REQUIRED_KEYS = ['name', 'title', 'headline', 'linkedinUrl', 'companyDomain', 'expertise'];
export const ALLOWED_EXTENSIONS = new Set(['.md', '.txt', '.json', '.csv', '.yaml', '.yml', '.py', '.sql', '.pdf', '.png', '.webp', '.html']);
export const HEADLINE_MAX = 140;
const REQUIRED_SECTION = '## What good looks like';

const KEBAB = /^[a-z0-9][a-z0-9-]*$/;
const FILE_SEGMENT = /^[A-Za-z0-9][A-Za-z0-9._-]*\.[A-Za-z0-9]+$/;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const DOMAIN = /^[a-z0-9][a-z0-9.-]*\.[a-z]{2,}$/;

// --- Frontmatter -------------------------------------------------------------
// Minimal YAML subset, enough for the two frontmatter shapes this repo uses:
//   key: value            key: "quoted"        key: value   # comment
//   key: [a, "b"]         key:  +  - item      key: | / > / >- / |+ (block scalar)
//   key:  +  indented sub: value   (recorded as an object, so `metadata:` is detectable)
// CRLF is normalised. Returns null when the file has no frontmatter.
const BLOCK_INDICATOR = /^[|>][+-]?\d*$/;
const stripComment = (v) => v.replace(/\s+#.*$/, '').trim();
const unquote = (v) => v.replace(/^(["'])(.*)\1$/, '$2');
const scalar = (v) => unquote(stripComment(v));
const flowList = (v) => v.slice(1, -1).split(',').map((s) => unquote(s.trim())).filter(Boolean);

export function parseFrontmatter(raw) {
  raw = raw.replace(/\r\n/g, '\n');
  if (!raw.startsWith('---\n')) return null;
  const end = raw.indexOf('\n---', 4);
  if (end === -1) return null;
  const block = raw.slice(4, end);
  const bodyStart = raw.indexOf('\n', end + 1);
  const body = bodyStart === -1 ? '' : raw.slice(bodyStart + 1);
  const data = {};
  const seen = new Set();
  const dupes = [];
  let lastKey = null;
  let mode = null; // 'list' | 'scalar' | 'object' | null
  for (const line of block.split('\n')) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    if (/^\s/.test(line)) {
      const trimmed = line.trim();
      if (mode === 'list' && trimmed.startsWith('- ')) data[lastKey].push(scalar(trimmed.slice(2)));
      else if (mode === 'scalar') data[lastKey] = data[lastKey] ? `${data[lastKey]} ${trimmed}` : trimmed;
      else if (mode === 'object' || (lastKey && Array.isArray(data[lastKey]) && data[lastKey].length === 0)) {
        const m = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$/);
        if (m) { if (typeof data[lastKey] !== 'object' || Array.isArray(data[lastKey])) data[lastKey] = {}; data[lastKey][m[1]] = scalar(m[2]); mode = 'object'; }
      }
      continue;
    }
    if (line.startsWith('- ') && mode === 'list') { data[lastKey].push(scalar(line.slice(2))); continue; }
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$/);
    if (!match) continue;
    const [, key, rawValue] = match;
    if (seen.has(key)) dupes.push(key);
    seen.add(key);
    lastKey = key;
    const value = stripComment(rawValue);
    if (value === '') { data[key] = []; mode = 'list'; }
    else if (BLOCK_INDICATOR.test(value)) { data[key] = ''; mode = 'scalar'; }
    else if (value.startsWith('[') && value.endsWith(']')) { data[key] = flowList(value); mode = null; }
    else { data[key] = unquote(value); mode = null; }
  }
  return { data, body, dupes: [...new Set(dupes)] };
}

export function loadTaxonomy(rootDir) {
  return JSON.parse(fs.readFileSync(path.join(rootDir, 'schema', 'taxonomy.json'), 'utf8'));
}

// --- Core --------------------------------------------------------------------
// files: Map<relative path from repo root, content>. Only paths under skills/ matter.
export function validateFiles(files, taxonomy, opts = {}) {
  const errors = [];
  const warnings = [];
  const err = (file, msg) => errors.push(`${file}: ${msg}`);
  const warn = (file, msg) => warnings.push(`${file}: ${msg}`);
  const categories = new Set(taxonomy.categories);
  const toolBySlug = new Map(taxonomy.tools.map((t) => [t.slug, t]));

  if (opts.rootHasSkillMd) err('SKILL.md', 'a root-level SKILL.md turns the whole repository into one skill for `npx skills` - delete it; skills live under skills/<creator>/<skill>/');

  // Group paths: skills/<author>/...
  const authors = new Map(); // slug -> { files: Map<relToAuthor, content> }
  for (const [p, content] of files) {
    const segs = p.split('/');
    if (segs[0] !== 'skills') continue;
    if (segs.length === 2) {
      if (segs[1] === '.gitkeep') continue;
      err(p, 'loose file directly under skills/ - only creator directories belong here (skills/<creator>/<skill>/)');
      continue;
    }
    const slug = segs[1];
    if (slug.startsWith('.')) continue;
    if (!authors.has(slug)) authors.set(slug, new Map());
    authors.get(slug).set(segs.slice(2).join('/'), content);
  }

  const skillOwners = new Map(); // skill slug -> author slug
  const readFm = (file, raw) => {
    const parsed = parseFrontmatter(raw);
    if (!parsed) { err(file, 'missing YAML frontmatter - start the file with a --- fenced block'); return { data: {}, body: raw }; }
    if (parsed.dupes.length) err(file, `frontmatter key(s) ${parsed.dupes.join(', ')} appear more than once - only the final value survives; keep one`);
    return parsed;
  };

  for (const [authorSlug, afiles] of [...authors].sort()) {
    const authorDir = `skills/${authorSlug}`;
    if (!KEBAB.test(authorSlug)) err(authorDir, `author directory "${authorSlug}" is not kebab-case (lowercase letters, digits, hyphens)`);

    const authorMdPath = `${authorDir}/author.md`;
    if (!afiles.has('author.md')) {
      err(authorDir, 'missing author.md - every creator directory needs a profile; start from templates/author.md');
    } else {
      validateAuthor(authorMdPath, readFm(authorMdPath, afiles.get('author.md')));
    }

    const skillDirs = new Map(); // skill slug -> Map<relToSkill, content>
    for (const [relPath, content] of afiles) {
      const segs = relPath.split('/');
      if (segs.length === 1) {
        if (relPath === 'SKILL.md') err(`${authorDir}/SKILL.md`, 'SKILL.md sits directly in a creator directory - give the skill its own folder: skills/<creator>/<skill>/SKILL.md');
        else if (relPath !== 'author.md') err(`${authorDir}/${relPath}`, 'unexpected file in a creator directory - only author.md and skill folders belong here');
        continue;
      }
      if (!skillDirs.has(segs[0])) skillDirs.set(segs[0], new Map());
      skillDirs.get(segs[0]).set(segs.slice(1).join('/'), content);
    }
    for (const [skillSlug, sfiles] of [...skillDirs].sort()) validateSkill(authorSlug, skillSlug, sfiles);
  }

  function validateAuthor(file, { data: fm }) {
    for (const key of AUTHOR_REQUIRED_KEYS) {
      if (!fm[key] || (Array.isArray(fm[key]) && fm[key].length === 0)) err(file, `frontmatter is missing \`${key}:\` - see templates/author.md`);
    }
    if (fm.slug) err(file, 'remove `slug:` - the creator slug is the directory name');
    if (fm.headline && fm.headline.length > HEADLINE_MAX) err(file, `\`headline:\` is ${fm.headline.length} characters - keep it under ${HEADLINE_MAX}; it is the one line shown in search results`);
    if (fm.linkedinUrl && !/linkedin\.com\/in\//.test(fm.linkedinUrl)) err(file, '`linkedinUrl:` must point at a personal profile (linkedin.com/in/<handle>), not a company page');
    if (fm.companyDomain && !DOMAIN.test(fm.companyDomain)) err(file, `\`companyDomain: ${fm.companyDomain}\` must be a bare domain (acme.com) - drop the protocol and path`);
    if (Array.isArray(fm.expertise)) for (const e of fm.expertise) if (!KEBAB.test(e)) err(file, `\`expertise\` item "${e}" must be lower-kebab (e.g. sales-coaching)`);
    if (fm.categories !== undefined) {
      const list = Array.isArray(fm.categories) ? fm.categories : [fm.categories];
      for (const c of list) if (!categories.has(c)) err(file, `\`categories\` item "${c}" isn't in schema/taxonomy.json - known: ${[...categories].join(', ')}`);
    }
    if (!fm.email) warn(file, 'no `email:` - maintainers will have no way to contact you about review or refreshes');
    else if (!EMAIL.test(String(fm.email).trim())) err(file, `\`email: ${fm.email}\` is not a valid address`);
    if (!fm.avatarUrl) warn(file, 'no `avatarUrl:` - maintainers may re-host your LinkedIn photo instead');
  }

  function validateSkill(authorSlug, skillSlug, sfiles) {
    const skillDir = `skills/${authorSlug}/${skillSlug}`;
    if (skillSlug === 'author') { err(skillDir, 'a skill folder cannot be called "author" - rename it'); return; }
    if (!KEBAB.test(skillSlug)) err(skillDir, `skill folder "${skillSlug}" is not kebab-case`);
    if (skillSlug.length > 60) err(skillDir, `skill folder name is ${skillSlug.length} characters - keep it ≤ 60`);
    if (skillOwners.has(skillSlug)) err(skillDir, `slug "${skillSlug}" already exists under skills/${skillOwners.get(skillSlug)}/ - skill names are unique across the library; choose another`);
    else skillOwners.set(skillSlug, authorSlug);

    const skillMd = `${skillDir}/SKILL.md`;
    if (!sfiles.has('SKILL.md')) { err(skillDir, 'missing SKILL.md - a skill folder without one is not a skill; start from templates/skill/SKILL.md'); return; }
    const { data: fm, body } = readFm(skillMd, sfiles.get('SKILL.md'));

    for (const key of SKILL_REQUIRED_KEYS) if (!fm[key]) err(skillMd, `frontmatter is missing \`${key}:\` - see templates/skill/SKILL.md`);
    if (fm.name && fm.name !== skillSlug) err(skillMd, `\`name: ${fm.name}\` must equal the folder name "${skillSlug}" - the folder is the identity`);
    if (fm.category && !categories.has(fm.category)) err(skillMd, `\`category: ${fm.category}\` isn't in schema/taxonomy.json - known: ${[...categories].join(', ')}`);
    for (const key of SKILL_FORBIDDEN_KEYS) if (key in fm) err(skillMd, `remove \`${key}:\` - lifecycle and ranking are decided downstream, never in this repo`);
    if ('metadata' in fm) err(skillMd, 'remove the `metadata:` block - it is a template marker left behind');
    const tools = Array.isArray(fm.tools) ? fm.tools : fm.tools ? [fm.tools] : [];
    for (const t of tools) if (!toolBySlug.has(t)) warn(skillMd, `tool "${t}" isn't in schema/taxonomy.json - spelling, or open a PR adding it`);
    for (const c of (Array.isArray(fm.contributors) ? fm.contributors : [])) {
      if (!authors.get(c)?.has('author.md')) err(skillMd, `contributor "${c}" has no profile - each contributor needs skills/<slug>/author.md`);
    }
    if (!body.includes(REQUIRED_SECTION)) err(skillMd, `missing a \`${REQUIRED_SECTION}\` section - that is the judgment that makes it a skill and not a checklist`);

    // Tool rule: mentions of known tools in the body that aren't declared → warning.
    const declared = new Set(tools);
    for (const tool of taxonomy.tools) {
      if (declared.has(tool.slug)) continue;
      const names = [tool.name, ...tool.aliases].map((n) => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      const re = new RegExp(`(?<![A-Za-z0-9])(?:${names.join('|')})(?![A-Za-z0-9])`, 'i');
      const m = body.match(re);
      if (m) warn(skillMd, `mentions "${m[0]}" - declare it in \`tools: [${tool.slug}]\` or use a role verb`);
    }

    for (const relPath of sfiles.keys()) {
      if (relPath === 'SKILL.md') continue;
      const file = `${skillDir}/${relPath}`;
      const segs = relPath.split('/');
      if (segs.length !== 2 || segs[0] !== 'references') { err(file, 'files inside a skill live at SKILL.md or references/<file> - no other folders, no nesting'); continue; }
      const fileName = segs[1];
      if (!ALLOWED_EXTENSIONS.has(path.extname(fileName).toLowerCase())) err(file, `extension "${path.extname(fileName)}" is not allowed - permitted: ${[...ALLOWED_EXTENSIONS].join(' ')}`);
      if (!FILE_SEGMENT.test(fileName)) err(file, 'file name must be alphanumeric plus dot/underscore/hyphen, start with a letter or digit, and have an extension');
    }
  }

  return { errors, warnings, skillCount: skillOwners.size, creatorCount: authors.size };
}

// --- Filesystem wrapper --------------------------------------------------------
const TEXT_EXTENSIONS = new Set(['.md', '.txt', '.json', '.csv', '.yaml', '.yml', '.py', '.sql', '.html']);

export function readSkillTree(rootDir) {
  const files = new Map();
  const skillsDir = path.join(rootDir, 'skills');
  if (!fs.existsSync(skillsDir)) return null;
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, e.name);
      if (e.isDirectory()) walk(full);
      else {
        const rel = path.relative(rootDir, full).split(path.sep).join('/');
        files.set(rel, TEXT_EXTENSIONS.has(path.extname(e.name).toLowerCase()) ? fs.readFileSync(full, 'utf8') : '');
      }
    }
  };
  walk(skillsDir);
  return files;
}

export function validate(rootDir, opts = {}) {
  const taxonomy = opts.taxonomy ?? loadTaxonomy(opts.taxonomyRoot ?? rootDir);
  const files = readSkillTree(rootDir);
  if (files === null) return { errors: ['skills/: directory is missing - create it (keep a .gitkeep inside while it is empty)'], warnings: [], skillCount: 0, creatorCount: 0 };
  return validateFiles(files, taxonomy, { rootHasSkillMd: fs.existsSync(path.join(rootDir, 'SKILL.md')) });
}

// --- CLI -----------------------------------------------------------------------
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const flagIdx = args.indexOf('--taxonomy-root');
  const taxonomyRoot = flagIdx === -1 ? undefined : args.splice(flagIdx, 2)[1];
  const rootDir = path.resolve(args[0] ?? process.cwd());
  const { errors, warnings, skillCount, creatorCount } = validate(rootDir, { taxonomyRoot });
  for (const w of warnings) console.warn(`warn - ${w}`);
  if (errors.length) {
    console.error(`${errors.length} problem${errors.length === 1 ? '' : 's'} found:\n`);
    for (const line of errors) console.error(`  ${line}`);
    process.exit(1);
  }
  console.log(`ok - ${skillCount} skill${skillCount === 1 ? '' : 's'} across ${creatorCount} creator${creatorCount === 1 ? '' : 's'}, all checks passed`);
}
