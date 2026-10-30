import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const load = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));

const CATEGORIES = [
  'Sales', 'Marketing', 'RevOps', 'Customer Success', 'Leadership', 'Executive Coaching',
  'Sales Coaching', 'Hiring', 'Operations', 'Finance', 'Product', 'Strategy', 'Implementation',
];

test('taxonomy has exactly the 13 categories in order', () => {
  const t = load('schema/taxonomy.json');
  assert.deepEqual(t.categories, CATEGORIES);
});

test('taxonomy tools have unique slugs, names, and alias arrays', () => {
  const t = load('schema/taxonomy.json');
  assert.ok(t.tools.length >= 20);
  const slugs = new Set();
  for (const tool of t.tools) {
    assert.match(tool.slug, /^[a-z0-9][a-z0-9-]*$/);
    assert.ok(!slugs.has(tool.slug), `duplicate slug ${tool.slug}`);
    slugs.add(tool.slug);
    assert.ok(tool.name.length > 0);
    assert.ok(Array.isArray(tool.aliases));
  }
  for (const s of ['hubspot', 'salesforce', 'ashby']) assert.ok(slugs.has(s));
});

test('skill schema category enum equals taxonomy categories', () => {
  const t = load('schema/taxonomy.json');
  const s = load('schema/skill.schema.json');
  assert.deepEqual(s.properties.category.enum, t.categories);
  assert.deepEqual(s.required, ['name', 'title', 'description', 'category']);
  assert.equal(s.additionalProperties, false);
});

test('author schema categories enum equals taxonomy categories', () => {
  const t = load('schema/taxonomy.json');
  const a = load('schema/author.schema.json');
  assert.deepEqual(a.properties.categories.items.enum, t.categories);
  assert.deepEqual(a.required, ['name', 'title', 'headline', 'linkedinUrl', 'companyDomain', 'expertise']);
  assert.equal(a.properties.headline.maxLength, 140);
  assert.equal(a.properties.expertise.minItems, 1);
  assert.equal(a.additionalProperties, false);
});
