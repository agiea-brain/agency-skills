#!/usr/bin/env node
// Builds index.json - the machine-readable contract downstream consumers read
// (web app, server, MCP). Experts + skills + commit-pinned raw URLs. No emails.
//
//   node tools/build-index.mjs [rootDir] --repo <owner/name> --commit <sha> --out <file> [--taxonomy-root <dir>]

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter, readSkillTree } from './validate.mjs';

const asList = (v) => (v === undefined ? [] : Array.isArray(v) ? v : [v]);

export function buildIndex(rootDir, { repo, commit, generatedAt = new Date().toISOString() }) {
  const files = readSkillTree(rootDir) ?? new Map();
  const rawUrl = (p) => `https://raw.githubusercontent.com/${repo}/${commit}/${p}`;

  const experts = new Map();
  const skills = [];

  for (const [p, content] of files) {
    const segs = p.split('/');
    if (segs[0] !== 'skills' || segs.length < 3 || segs[1].startsWith('.')) continue;
    const creator = segs[1];
    if (segs.length === 3 && segs[2] === 'author.md') {
      const { data: fm, body } = parseFrontmatter(content) ?? { data: {}, body: '' };
      experts.set(creator, {
        slug: creator,
        name: fm.name ?? '',
        title: fm.title ?? '',
        headline: fm.headline ?? '',
        expertise: asList(fm.expertise),
        categories: fm.categories === undefined ? null : asList(fm.categories),
        linkedinUrl: fm.linkedinUrl ?? '',
        companyDomain: fm.companyDomain ?? '',
        avatarUrl: fm.avatarUrl ?? null,
        websiteUrl: fm.websiteUrl ?? null,
        bio: body.trim(),
        skills: [],
        path: p,
      });
      continue;
    }
    if (segs.length === 4 && segs[3] === 'SKILL.md') {
      const slug = segs[2];
      const dir = `skills/${creator}/${slug}`;
      const { data: fm, body } = parseFrontmatter(content) ?? { data: {}, body: '' };
      const extra = [...files.keys()].filter((f) => f.startsWith(`${dir}/`) && f !== p).sort()
        .map((f) => ({ path: f, rawUrl: rawUrl(f), ext: path.extname(f).toLowerCase() }));
      skills.push({
        slug,
        title: fm.title ?? '',
        description: typeof fm.description === 'string' ? fm.description.trim() : '',
        category: fm.category ?? '',
        tags: asList(fm.tags),
        tools: asList(fm.tools),
        creator,
        contributors: asList(fm.contributors),
        path: p,
        rawUrl: rawUrl(p),
        files: extra,
        wordCount: body.trim().split(/\s+/).filter(Boolean).length,
      });
    }
  }

  skills.sort((a, b) => a.slug.localeCompare(b.slug));
  for (const s of skills) experts.get(s.creator)?.skills.push(s.slug);
  const expertList = [...experts.values()].sort((a, b) => a.slug.localeCompare(b.slug));
  for (const e of expertList) {
    e.skills.sort();
    if (e.categories === null) {
      e.categories = [...new Set(skills.filter((s) => s.creator === e.slug).map((s) => s.category))].sort();
    }
  }

  return { version: 1, generatedAt, commit, repo, experts: expertList, skills };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const flag = (name, dflt) => { const i = args.indexOf(name); return i === -1 ? dflt : args.splice(i, 2)[1]; };
  const repo = flag('--repo', process.env.GITHUB_REPOSITORY ?? 'agiea-brain/agency-skills');
  const commit = flag('--commit', process.env.GITHUB_SHA ?? 'main');
  const out = flag('--out', 'index.json');
  flag('--taxonomy-root', undefined); // accepted for symmetry with validate.mjs; unused
  const rootDir = path.resolve(args[0] ?? process.cwd());
  const index = buildIndex(rootDir, { repo, commit });
  fs.writeFileSync(out, `${JSON.stringify(index, null, 2)}\n`);
  console.log(`wrote ${out} - ${index.skills.length} skills, ${index.experts.length} experts @ ${commit}`);
}
