import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { buildCards, hueFor, initials } from '../tools/build-cards.mjs';

const ROOT = path.resolve(import.meta.dirname, '..');
const GOOD = path.join(ROOT, 'examples');
const EMPTY = path.join(ROOT, 'tests/fixtures/empty');
const OPTS = { repo: 'agiea-brain/agent-skills' };

test('one card per creator plus a gallery', () => {
  const pages = buildCards(GOOD, OPTS);
  assert.deepEqual([...pages.keys()].sort(), ['index.html', 'jane-doe.html', 'priya-natarajan.html', 'sam-ops.html']);
  const gallery = pages.get('index.html');
  for (const slug of ['jane-doe', 'priya-natarajan', 'sam-ops']) assert.ok(gallery.includes(`href="${slug}.html"`), slug);
});

test('card shows profile, skills with install commands, and expertise', () => {
  const jane = buildCards(GOOD, OPTS).get('jane-doe.html');
  assert.match(jane, /^<!doctype html>/);
  assert.match(jane, /<h1>Jane Doe<\/h1>/);
  assert.ok(jane.includes('npx skills add agiea-brain/agent-skills --skill pipeline-review-coaching'));
  assert.ok(jane.includes('https://github.com/agiea-brain/agent-skills/tree/main/skills/jane-doe/pipeline-review-coaching'));
  assert.ok(jane.includes('<li>sales coaching</li>'));
  assert.ok(jane.includes('Skills you can install (1)'));
  assert.ok(!jane.includes('Install all of them'), 'single-skill creators get no install-all line');
});

test('cards never contain email', () => {
  for (const html of buildCards(GOOD, OPTS).values()) assert.ok(!/mailto:|@[a-z0-9-]+\.[a-z]{2,}/i.test(html.replace(/<style>[\s\S]*?<\/style>/, '')));
});

test('hue is stable and initials fall back sensibly', () => {
  assert.equal(hueFor('jane-doe'), hueFor('jane-doe'));
  assert.ok(hueFor('jane-doe') >= 0 && hueFor('jane-doe') < 360);
  assert.equal(initials('Jane Doe'), 'JD');
  assert.equal(initials('Priya Natarajan Rao'), 'PN');
  assert.equal(initials(''), '?');
});

test('empty tree yields only the gallery', () => {
  assert.deepEqual([...buildCards(EMPTY, OPTS).keys()], ['index.html']);
});

test('CLI writes cards to --out', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-skills-cards-'));
  const r = spawnSync('node', ['tools/build-cards.mjs', 'examples', '--repo', 'x/y', '--out', out], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.ok(fs.readFileSync(path.join(out, 'jane-doe.html'), 'utf8').includes('npx skills add x/y --skill pipeline-review-coaching'));
  assert.ok(fs.existsSync(path.join(out, 'index.html')));
});
