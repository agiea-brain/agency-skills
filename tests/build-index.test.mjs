import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { buildIndex } from '../tools/build-index.mjs';

const ROOT = path.resolve(import.meta.dirname, '..');
const GOOD = path.join(ROOT, 'examples');
const EMPTY = path.join(ROOT, 'tests/fixtures/empty');
const OPTS = { repo: 'agiea-brain/agent-skills', commit: 'abc123', generatedAt: '2026-01-01T00:00:00.000Z', taxonomyRoot: ROOT };

test('index lists experts and skills from the good fixture', () => {
  const idx = buildIndex(GOOD, OPTS);
  assert.equal(idx.version, 1);
  assert.equal(idx.repo, 'agiea-brain/agent-skills');
  assert.equal(idx.commit, 'abc123');
  assert.equal(idx.generatedAt, OPTS.generatedAt);
  assert.deepEqual(idx.experts.map((e) => e.slug), ['jane-doe', 'priya-natarajan', 'sam-ops']);
  assert.deepEqual(idx.skills.map((s) => s.slug), ['first-90-days-transition-plan', 'hubspot-lifecycle-stage-setup', 'pipeline-review-coaching']);
});

test('expert categories are derived from skills when omitted, kept when declared', () => {
  const idx = buildIndex(GOOD, OPTS);
  const jane = idx.experts.find((e) => e.slug === 'jane-doe');
  const sam = idx.experts.find((e) => e.slug === 'sam-ops');
  assert.deepEqual(jane.categories, ['Sales Coaching']);
  assert.deepEqual(sam.categories, ['Implementation', 'RevOps']);
  assert.deepEqual(jane.skills, ['pipeline-review-coaching']);
  assert.deepEqual(jane.expertise, ['sales-coaching', 'pipeline-reviews', 'forecasting']);
  assert.equal(jane.path, 'skills/jane-doe/author.md');
  assert.match(jane.bio, /^Jane spent twelve years/);
});

test('skills carry creator, tools, files with pinned raw URLs, and word count', () => {
  const idx = buildIndex(GOOD, OPTS);
  const sam = idx.skills.find((s) => s.slug === 'hubspot-lifecycle-stage-setup');
  const jane = idx.skills.find((s) => s.slug === 'pipeline-review-coaching');
  assert.equal(sam.creator, 'sam-ops');
  assert.deepEqual(sam.tools, ['hubspot']);
  assert.equal(sam.category, 'Implementation');
  assert.deepEqual(sam.files, []);
  assert.equal(jane.files.length, 1);
  assert.equal(jane.files[0].path, 'skills/jane-doe/pipeline-review-coaching/references/scorecard.md');
  assert.equal(jane.files[0].ext, '.md');
  assert.equal(jane.files[0].rawUrl, 'https://raw.githubusercontent.com/agiea-brain/agent-skills/abc123/skills/jane-doe/pipeline-review-coaching/references/scorecard.md');
  assert.equal(jane.rawUrl, 'https://raw.githubusercontent.com/agiea-brain/agent-skills/abc123/skills/jane-doe/pipeline-review-coaching/SKILL.md');
  assert.ok(jane.wordCount > 50 && jane.wordCount < 400, String(jane.wordCount));
  assert.match(jane.description, /^Use this skill when/);
  assert.deepEqual(jane.contributors, []);
});

test('index never contains email', () => {
  assert.ok(!JSON.stringify(buildIndex(GOOD, OPTS)).includes('"email"'));
});

test('empty tree yields empty arrays', () => {
  const idx = buildIndex(EMPTY, OPTS);
  assert.deepEqual(idx.experts, []);
  assert.deepEqual(idx.skills, []);
});

test('CLI writes index.json to --out', () => {
  const out = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'agent-skills-idx-')), 'index.json');
  const r = spawnSync('node', ['tools/build-index.mjs', 'examples', '--repo', 'x/y', '--commit', 'deadbeef', '--out', out, '--taxonomy-root', ROOT], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  const idx = JSON.parse(fs.readFileSync(out, 'utf8'));
  assert.equal(idx.repo, 'x/y');
  assert.equal(idx.skills.length, 3);
  assert.ok(idx.skills[0].rawUrl.startsWith('https://raw.githubusercontent.com/x/y/deadbeef/'));
});
