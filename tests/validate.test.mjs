import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import {
  parseFrontmatter, validateFiles, validate, loadTaxonomy,
  SKILL_REQUIRED_KEYS, SKILL_FORBIDDEN_KEYS, AUTHOR_REQUIRED_KEYS,
} from '../tools/validate.mjs';

const ROOT = path.resolve(import.meta.dirname, '..');
const GOOD = path.join(ROOT, 'examples');
const EMPTY = path.join(ROOT, 'tests/fixtures/empty');
const taxonomy = loadTaxonomy(ROOT);

const JANE = 'skills/jane-doe/pipeline-review-coaching/SKILL.md';
const SAM = 'skills/sam-ops/hubspot-lifecycle-stage-setup/SKILL.md';
const JANE_AUTHOR = 'skills/jane-doe/author.md';

const readTree = (root) => {
  const files = new Map();
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, e.name);
      if (e.isDirectory()) walk(full);
      else files.set(path.relative(root, full), fs.readFileSync(full, 'utf8'));
    }
  };
  walk(path.join(root, 'skills'));
  return files;
};

// Build the good fixture as a Map and apply edits: a string replaces a file,
// null deletes it, a function receives the current content.
const tree = (overrides = {}) => {
  const files = readTree(GOOD);
  for (const [p, v] of Object.entries(overrides)) {
    if (v === null) files.delete(p);
    else if (typeof v === 'function') files.set(p, v(files.get(p)));
    else files.set(p, v);
  }
  return files;
};
const swapFm = (key, value) => (raw) => raw.replace(new RegExp(`^${key}:.*$`, 'm'), value === null ? '' : `${key}: ${value}`);
const has = (list, s) => list.some((l) => l.includes(s));

test('good fixture passes with no errors and no warnings', () => {
  const r = validateFiles(tree(), taxonomy);
  assert.deepEqual(r.errors, []);
  assert.deepEqual(r.warnings, []);
});

test('empty skills dir passes', () => {
  const r = validateFiles(new Map(), taxonomy);
  assert.deepEqual(r.errors, []);
});

test('parseFrontmatter joins a block-scalar description', () => {
  const raw = '---\nname: x\ndescription: |\n  first line\n  second line\n---\nbody';
  const { data, body } = parseFrontmatter(raw);
  assert.equal(data.description, 'first line second line');
  assert.equal(body.trim(), 'body');
});

test('undeclared tool mention in body is a warning, not an error', () => {
  const r = validateFiles(tree({ [JANE]: (s) => s.replace('Pull the open pipeline', 'Log it in Outreach, then pull the open pipeline') }), taxonomy);
  assert.deepEqual(r.errors, []);
  assert.equal(r.warnings.length, 1);
  assert.ok(has(r.warnings, 'mentions "Outreach"'), r.warnings.join('\n'));
});

test('tool mention matches whole words only', () => {
  // "outreach" as a plain word in lowercase inside a sentence: "cold outreach" - must not fire on substrings like "outreaching"
  const r = validateFiles(tree({ [JANE]: (s) => s.replace('Pull the open pipeline', 'Stop outreaching and pull the open pipeline') }), taxonomy);
  assert.deepEqual(r.warnings, []);
});

test('declared tool mention produces no warning', () => {
  const r = validateFiles(tree(), taxonomy);
  assert.ok(!has(r.warnings, 'HubSpot'));
});

test('author categories outside taxonomy is an error', () => {
  const r = validateFiles(tree({ [JANE_AUTHOR]: (s) => s.replace('expertise:', 'categories: [Nonsense]\nexpertise:') }), taxonomy);
  assert.ok(has(r.errors, 'categories'), r.errors.join('\n'));
});

test('headline over 140 chars is an error', () => {
  const r = validateFiles(tree({ [JANE_AUTHOR]: swapFm('headline', 'x'.repeat(141)) }), taxonomy);
  assert.ok(has(r.errors, 'headline'));
});

test('missing expertise is an error', () => {
  const r = validateFiles(tree({ [JANE_AUTHOR]: swapFm('expertise', null) }), taxonomy);
  assert.ok(has(r.errors, 'expertise'));
});

test('skill name not equal to folder is an error', () => {
  const r = validateFiles(tree({ [JANE]: swapFm('name', 'other-name') }), taxonomy);
  assert.ok(has(r.errors, 'must equal the folder name'));
});

test('duplicate skill slug across creators is an error', () => {
  const dup = tree();
  dup.set('skills/sam-ops/pipeline-review-coaching/SKILL.md', dup.get(JANE));
  const r = validateFiles(dup, taxonomy);
  assert.ok(has(r.errors, 'already exists'));
});

test('file outside references/ inside a skill is an error', () => {
  const r = validateFiles(tree({ 'skills/jane-doe/pipeline-review-coaching/assets/x.png': '' }), taxonomy);
  assert.ok(has(r.errors, 'references/'), r.errors.join('\n'));
});

test('nested folder under references/ is an error', () => {
  const r = validateFiles(tree({ 'skills/jane-doe/pipeline-review-coaching/references/sub/x.md': '# x' }), taxonomy);
  assert.ok(has(r.errors, 'references/'));
});

test('disallowed extension is an error', () => {
  const r = validateFiles(tree({ 'skills/jane-doe/pipeline-review-coaching/references/tool.exe': '' }), taxonomy);
  assert.ok(has(r.errors, 'extension'));
});

test('forbidden frontmatter key is an error', () => {
  const r = validateFiles(tree({ [JANE]: (s) => s.replace('tags:', 'featured: true\ntags:') }), taxonomy);
  assert.ok(has(r.errors, 'featured'));
});

test('template metadata marker left behind is an error', () => {
  const r = validateFiles(tree({ [JANE]: (s) => s.replace('tags:', 'metadata:\n  internal: true\ntags:') }), taxonomy);
  assert.ok(has(r.errors, 'metadata'));
});

test('missing What good looks like section is an error', () => {
  const r = validateFiles(tree({ [JANE]: (s) => s.replace('## What good looks like', '## Quality') }), taxonomy);
  assert.ok(has(r.errors, 'What good looks like'));
});

test('unknown tool slug in tools: is a warning', () => {
  const r = validateFiles(tree({ [SAM]: swapFm('tools', '[hubspot, mystery-crm]') }), taxonomy);
  assert.deepEqual(r.errors, []);
  assert.ok(has(r.warnings, 'mystery-crm'));
});

test('unknown category is an error', () => {
  const r = validateFiles(tree({ [SAM]: swapFm('category', 'Wizardry') }), taxonomy);
  assert.ok(has(r.errors, 'Wizardry'));
});

test('contributor without profile is an error', () => {
  const r = validateFiles(tree({ [SAM]: (s) => s.replace('tags:', 'contributors: [ghost]\ntags:') }), taxonomy);
  assert.ok(has(r.errors, 'ghost'));
});

test('root SKILL.md is an error', () => {
  const r = validateFiles(tree(), taxonomy, { rootHasSkillMd: true });
  assert.ok(has(r.errors, 'SKILL.md'));
});

test('malformed email is an error, absent email is a warning', () => {
  assert.ok(has(validateFiles(tree({ [JANE_AUTHOR]: swapFm('email', 'notanemail') }), taxonomy).errors, 'email'));
  const r = validateFiles(tree({ [JANE_AUTHOR]: swapFm('email', null) }), taxonomy);
  assert.deepEqual(r.errors, []);
  assert.ok(has(r.warnings, 'email'));
});

test('missing author.md is an error', () => {
  const r = validateFiles(tree({ [JANE_AUTHOR]: null }), taxonomy);
  assert.ok(has(r.errors, 'author.md'));
});

test('loose file under skills/ is an error', () => {
  const r = validateFiles(tree({ 'skills/README.md': '# no' }), taxonomy);
  assert.ok(has(r.errors, 'loose file'));
});

test('validate(rootDir) walks the fixture', () => {
  assert.deepEqual(validate(GOOD, { taxonomyRoot: ROOT }).errors, []);
  assert.deepEqual(validate(EMPTY, { taxonomyRoot: ROOT }).errors, []);
});

test('validator key lists match the JSON schemas', () => {
  const skill = JSON.parse(fs.readFileSync(path.join(ROOT, 'schema/skill.schema.json'), 'utf8'));
  const author = JSON.parse(fs.readFileSync(path.join(ROOT, 'schema/author.schema.json'), 'utf8'));
  assert.deepEqual(SKILL_REQUIRED_KEYS, skill.required);
  assert.deepEqual(AUTHOR_REQUIRED_KEYS, author.required);
  for (const k of SKILL_FORBIDDEN_KEYS) assert.ok(!(k in skill.properties), `${k} is forbidden but in schema`);
});

test('CLI exits 0 with summary on good and empty fixtures', () => {
  const run = (dir) => spawnSync('node', ['tools/validate.mjs', dir, '--taxonomy-root', ROOT], { cwd: ROOT, encoding: 'utf8' });
  const g = run('examples');
  assert.equal(g.status, 0, g.stderr);
  assert.match(g.stdout, /ok - 3 skills across 3 creators/);
  const e = run('tests/fixtures/empty');
  assert.equal(e.status, 0, e.stderr);
  assert.match(e.stdout, /ok - 0 skills across 0 creators/);
});

test('CLI exits 1 on a broken tree', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-skills-'));
  fs.cpSync(GOOD, tmp, { recursive: true });
  fs.writeFileSync(path.join(tmp, 'SKILL.md'), '---\nname: root\n---\n');
  const r = spawnSync('node', ['tools/validate.mjs', tmp, '--taxonomy-root', ROOT], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /SKILL\.md/);
});

// --- Review fixes: YAML subset robustness ------------------------------------

test('inline comments after scalar values are stripped', () => {
  const { data } = parseFrontmatter('---\ncompanyDomain: acme.com   # bare domain\ntitle: Coach, Acme # role\n---\n');
  assert.equal(data.companyDomain, 'acme.com');
  assert.equal(data.title, 'Coach, Acme');
});

test('inline comments after flow lists are stripped and quoted items unquoted', () => {
  const { data } = parseFrontmatter('---\ntools: []   # tool-specific?\nexpertise: ["sales-coaching", \'hubspot\']\nlist:\n  - "a"\n  - \'b\'\n---\n');
  assert.deepEqual(data.tools, []);
  assert.deepEqual(data.expertise, ['sales-coaching', 'hubspot']);
  assert.deepEqual(data.list, ['a', 'b']);
});

test('block scalar indicators with chomping are recognised', () => {
  for (const ind of ['|', '>', '>-', '|-', '|+', '| ']) {
    const { data } = parseFrontmatter(`---\ndescription: ${ind}\n  one\n  two\n---\n`);
    assert.equal(data.description, 'one two', `indicator ${JSON.stringify(ind)}`);
  }
});

test('CRLF line endings parse as frontmatter', () => {
  const raw = '---\r\nname: x\r\ndescription: |\r\n  hello\r\n---\r\nbody\r\n';
  const parsed = parseFrontmatter(raw);
  assert.ok(parsed);
  assert.equal(parsed.data.name, 'x');
  assert.equal(parsed.data.description, 'hello');
  assert.equal(parsed.body.trim(), 'body');
});

test('templates copied verbatim (minus the metadata marker) validate with no errors', () => {
  const author = fs.readFileSync(path.join(ROOT, 'templates/author.md'), 'utf8');
  const skill = fs.readFileSync(path.join(ROOT, 'templates/skill/SKILL.md'), 'utf8').replace(/^metadata:\n(?:[ \t]+.*\n)+/m, '');
  const files = new Map([
    ['skills/full-name/author.md', author],
    ['skills/full-name/my-skill-name/SKILL.md', skill],
  ]);
  const r = validateFiles(files, taxonomy);
  assert.deepEqual(r.errors, [], r.errors.join('\n'));
});
