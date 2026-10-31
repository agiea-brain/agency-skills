# Agent Skills

A library of skills written by people who do the work for a living: sales and executive coaches, RevOps and marketing operators, and the implementers who set up HubSpot, Salesforce, Ashby and the rest. Each skill is a practitioner's actual playbook, packaged so an AI agent can run it.

A skill is a folder with a `SKILL.md`. Any agent that reads Markdown can use one: Claude Code, Cursor, Codex, Claude Desktop, and most others.

## Use a skill

```bash
npx skills add agiea-brain/agency-skills --skill <skill-name>      # one skill
npx skills add agiea-brain/agency-skills/skills/<creator-slug>     # one creator's whole shelf
npx skills add agiea-brain/agency-skills                           # browse interactively
npx skills add agiea-brain/agency-skills --list                    # what's here
```

Pick a target with `-a claude-code`, `-a cursor`, `-a codex`, and so on.

## Contribute a skill in one sitting

The fastest route is to let your own agent do the paperwork. Paste this into Claude, Cursor, Codex, or any agent that can fetch a URL:

> Fetch https://raw.githubusercontent.com/agiea-brain/agency-skills/main/AGENTS.md and follow its contribution flow. Interview me about one thing I'm genuinely expert at, until you have my frameworks, my numbers and two real examples. Draft it in their format, check it, and open the PR. If you can't use git here, give me the prefilled issue link or the paste bundle it describes.

The agent interviews you, writes the files, checks them, and opens a pull request under your name. Prefer to do it by hand, or have no git? [CONTRIBUTING.md](CONTRIBUTING.md) covers both.

## Who writes here

Three kinds of experts, and the library is built so each fits:

| Expert | Example skill | How the body is written |
|---|---|---|
| **Coaches** (sales, executive, leadership) | Pipeline review coaching | Role verbs, framework and session script, no product names |
| **Operators** (GTM, RevOps, CS, hiring, finance, product) | Territory signal digest | Role verbs ("check the CRM"), works on any stack |
| **Implementers** (a specific product) | HubSpot lifecycle stage setup | Names the product, declares it in `tools:` |

Categories, and the list of tools a skill may declare, live in [`schema/taxonomy.json`](schema/taxonomy.json). Adding a category or tool is a one-line PR.

## Layout

```
skills/<creator>/            one directory per person
  author.md                  who they are, what they help with, how to find them
  <skill>/SKILL.md           the skill
  <skill>/references/*.md    optional depth: rubrics, scripts, worked examples
schema/                      taxonomy + JSON Schemas for the two frontmatter shapes
tools/                       validate.mjs, build-index.mjs (zero dependencies)
templates/                   copy these to start
examples/                    three finished skills (fictional people); the shape to imitate
```

The skill folder name is its install name and its URL forever. Everything else is frontmatter and can change.

## What gets merged

A skill is accepted when it passes three tests: it says exactly **when** to fire, it carries the author's **judgment** (what they notice first, what the mediocre version gets wrong, how they know the output is good), and it has **depth** (real numbers, real examples, in `references/`). A tidy checklist with none of those is sent back with notes. The full bar and the review process are in [CONTRIBUTING.md](CONTRIBUTING.md).

## For people building on the library

Every merge to `main` regenerates `index.json` on the `index` branch:

```
https://raw.githubusercontent.com/agiea-brain/agency-skills/index/index.json
```

It lists every expert and skill with commit-pinned raw URLs for the content, and never includes contact emails. A webhook can be configured to fire after each publish. The validator's core is a pure function (`validateFiles` in `tools/validate.mjs`), so a submission UI can run the same checks before a PR exists.

## License

MIT. Your name stays on your skills: `author.md` travels with them wherever the library is served.
