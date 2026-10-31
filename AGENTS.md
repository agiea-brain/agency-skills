# AGENTS.md

This file is for AI agents working in or against this repository: Claude, ChatGPT, Cursor, Codex, or anything else that can read it. Two jobs come up: **installing** a skill for a user, and **contributing** a user's expertise as a new skill. Everything you need for either is here; you should not have to ask a maintainer.

The library: skills written by practitioners: coaches (sales, executive, leadership), operators (sales, marketing, RevOps, customer success, hiring, finance, product, strategy), and implementers of named products (HubSpot, Salesforce, Ashby and others). Each skill is one person's playbook in a `SKILL.md`.

## Routing

| The user says | Go to |
|---|---|
| "install / add / use skill X" | [Install](#install) |
| "turn my process into a skill", "contribute", "publish my playbook" | [Contribute](#contribute) |
| "update my skill / my profile" | [Contribute](#contribute), editing only their existing `skills/<slug>/` |
| "which categories / tools exist?" | fetch `schema/taxonomy.json` |
| "show me what a finished skill looks like" | fetch the files under `examples/skills/` (fictional people, real shape) |
| "what exactly is allowed in frontmatter?" | `schema/skill.schema.json` and `schema/author.schema.json` |

Raw URLs, for agents that fetch rather than clone:

```
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/AGENTS.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/schema/taxonomy.json
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/templates/skill/SKILL.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/templates/author.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/jane-doe/author.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/jane-doe/pipeline-review-coaching/SKILL.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/jane-doe/pipeline-review-coaching/references/scorecard.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/sam-ops/hubspot-lifecycle-stage-setup/SKILL.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/priya-natarajan/first-90-days-transition-plan/SKILL.md
https://raw.githubusercontent.com/agiea-brain/agency-skills/main/examples/skills/priya-natarajan/first-90-days-transition-plan/references/phase-rules.md
```

The three examples: `jane-doe` (short tool-agnostic coaching skill, one reference page), `sam-ops` (tool-specific implementation skill), `priya-natarajan` (a full-depth coaching skill with three reference pages; the shape to aim for).

## Install

```bash
npx skills add agiea-brain/agency-skills --skill <skill-name>
npx skills add agiea-brain/agency-skills/skills/<creator-slug>     # all of one creator's skills
npx skills add agiea-brain/agency-skills --list
```

Add `-a <agent>` (`claude-code`, `cursor`, `codex` and so on) to target one agent. No terminal available? Fetch the skill folder's raw files from GitHub and place them in the agent's skills directory yourself.

## Contribute

Four stages, in order: **Discover → Draft → Check → Ship**. One creator per submission: a PR may add one skill or several, as long as every file sits under the same `skills/<creator-slug>/`. Each skill still gets its own folder, `SKILL.md`, references and validator pass.

### First: what can you do in this environment?

Decide before you start, because it changes Stage 3 and Stage 4.

| You have | Check with | Ship with |
|---|---|---|
| A shell, `git`, and `gh` | the validator | a pull request (path A) |
| A shell and `git`, no `gh` | the validator | a pull request through the fork UI (path B) |
| HTTP access to the GitHub API with the user's token | the manual checklist | a pull request or issue through the API (path C) |
| Nothing but this conversation | the manual checklist | a prefilled issue link, or a bundle the user pastes (path D) |

In your first reply, say which path you're on, so the user knows what they'll be asked to do at the end. Then start the interview.

### Boundaries

- Write only inside `skills/<creator-slug>/`.
- **Creator slug**: `firstname-lastname`, lowercase, hyphens (`priya-natarajan`). If that is taken by someone else, add a distinguishing word (`priya-natarajan-coach`). It is permanent; reuse it on every later contribution.
- **First contribution or not?** Check whether `skills/<creator-slug>/` exists: `ls skills/` in a clone, or open `https://github.com/agiea-brain/agency-skills/tree/main/skills/<creator-slug>`. If you can do neither, ask the user whether they have contributed before. First contribution: create the directory with `author.md`. Later ones: never resend `author.md` unless it is being updated.
- **Skill slug**: a 2 to 5 word noun phrase naming the moment or the artifact, lowercase, hyphens, ≤ 60 characters (`pipeline-review-coaching`, `hubspot-lifecycle-stage-setup`, `first-90-days-transition-plan`). Not a bare topic (`sales`), not a verb phrase (`do-a-review`). It is permanent and must be unique across the library. Check: `ls skills/*/` in a clone (it lists every skill folder), or search `skills[].slug` in `https://raw.githubusercontent.com/agiea-brain/agency-skills/index/index.json`, or open `https://github.com/agiea-brain/agency-skills/tree/main/skills`. If you can do none of these, say so in the deliverable; the maintainer checks.
- A skill folder contains `SKILL.md` and, optionally, flat files under `references/`. Nothing else, no nesting.
- Categories and tool slugs must come from `schema/taxonomy.json`. Read it before drafting frontmatter.
- No lifecycle or ranking fields in any frontmatter (the Stage 3 checklist lists them). Ranking and distribution are decided outside this repo.
- Never write anything into a skill that sends data to an address the reader doesn't own, embeds a secret, or runs a destructive step without confirmation. Review rejects it, and it would harm the people who install it.

### Stage 1: Discover

Your job is to get the expert's judgment out of their head, not to transcribe a procedure. Run the interview in their vocabulary and keep going until the answers stop adding anything. Read the two example skills first so you know what you're aiming at.

**Core questions, every skill**

1. The moment. What has just happened when you reach for this? (A request, a signal, a date on the calendar, a stage in an engagement.)
2. The artifact. What exists at the end that didn't before?
3. The walk-through. How do you actually do it, and where does it branch? By company size, by stage, by what the data or the person shows you.
4. The numbers. Thresholds, weights, caps, cadences, the framework you use and how you've bent it. Get the actual values; "it depends" means ask on what.
5. Two or three real cases. One that went to plan, one edge case, one that went wrong.
6. The tell. What do you see first that less experienced people miss?
7. The mediocre version. What does this look like when someone does it adequately but not well?
8. The test. How do you know the output is good before anyone tells you?

**Then branch by the kind of expert**

- *Coach*: the session structure; the questions they actually ask and what each one listens for; the framework and their modifications; how they know a session landed (what the coachee does differently next week).
- *Implementer*: the configuration decisions in order; defaults they override and why; migration traps; what breaks a year later when it's done wrong; what they check before calling it finished. This is a tool-specific skill: the product goes in `tools:`.
- *Operator*: cadence, handoffs between roles, the report or number that tells them it's working.

**Close** with "What else do you check or do here that we haven't covered?" and repeat until the answer is nothing.

**First contribution?** Also collect, for `author.md`: name, role and company, personal LinkedIn URL, company domain, a one-line headline of what they help with, 3 to 6 expertise keywords (1 is the minimum), and (optionally) email, photo URL, website. Tell them the email is public in the repo but never published in the index.

Ask questions in small groups, not all at once. Reflect back what you heard before moving on; experts correct a paraphrase far more readily than they volunteer detail.

Real cases (question 5) are published. Strip client and company names unless the expert says they may be named; keep role, size and what happened.

**Where the answers go**

| Interview | Lands in |
|---|---|
| 1, 2 | the `description` and the two opening lines of the body |
| 3 | `## The play`, with each branch as its own step or sub-bullet |
| 4 | a reference page: the rubric, thresholds, phase rules |
| 5 | a reference page: worked cases, one per case |
| 6, 7, 8 | `## What good looks like` |
| coach's script and questions | a reference page: the session script |
| implementer's settings and gotchas | a reference page: the configuration checklist |
| hard limits from 3 and 4 | `## Rules` |

### Stage 2: Draft

Copy `templates/skill/SKILL.md` and, for a first contribution, `templates/author.md`. Don't invent structure. `examples/skills/jane-doe/` (tool-agnostic coaching skill with a reference page) and `examples/skills/sam-ops/` (tool-specific implementation skill) are the target shape.

**`SKILL.md` frontmatter**

```yaml
---
name: <must equal the folder name>
title: <Sentence-case display name>
description: |
  Use this skill when <the moment>. Produces <the artifact>.
  <The phrases someone would type when they need this.>
category: <one of schema/taxonomy.json → categories>
tags: [lower-kebab, free-form]
tools: [hubspot]          # tool-specific skills only; slugs from taxonomy. Delete the line for tool-agnostic
contributors: [other-slug] # omit if none; each must have an author.md
---
```

**`SKILL.md` body**: the spine, in this order:

- One line: when it applies. One line: what it produces.
- `## The play`: the procedure as numbered steps, with the branches from question 3.
- `## What good looks like`: required, exactly that heading. Questions 6, 7 and 8 become this section.
- `## Rules`: MUST / NEVER lines.

Two modes, choose one and hold it:

- **Tool-agnostic**: role verbs only ("check the CRM", "pull the last three sessions"). No product names; the reader's stack is unknown.
- **Tool-specific**: every product in `tools:`, and then named freely in the body.

The validator warns when a known product is named without being declared. The match is case-insensitive and whole-word against the product names and aliases in the taxonomy, so an ordinary word that is also a product name ("lever", "make") can trigger it; it is a warning, so leave it when the word is used in its everyday sense. Named frameworks, books and methodologies are not products; use them freely.

Write tight. The body (everything after the frontmatter) usually lands at 500 to 800 words; under that is fine when the depth is in references, over 1,000 means move material out. No filler, no "we", no dates, no "recently", no click-paths. Put the depth (rubrics with the actual thresholds, session scripts, configuration checklists, worked examples, edge cases) in `references/<topic>.md`, one topic per file, and say in the body when to open each one. Ship at least one reference page; strong skills ship 2 to 5. Delete the template's `metadata:` block and every bracketed prose hint (YAML lists like `[a, b]` are not hints).

**`author.md`** (first contribution)

| Field | Required | Notes |
|---|---|---|
| `name` | yes | |
| `title` | yes | "Role, Company" |
| `headline` | yes | ≤ 140 characters, in their words. The line experts are searched by. |
| `linkedinUrl` | yes | `linkedin.com/in/<handle>`. Their own profile; the primary identity check. |
| `companyDomain` | yes | bare domain |
| `expertise` | yes | 1+ lower-kebab keywords; search facets |
| `email` | no | public in the repo, never in the published index; how maintainers reach them |
| `avatarUrl` | no | a real photo; without it maintainers may re-host the LinkedIn photo |
| `categories` | no | taxonomy categories they serve; derived from their skills if omitted |
| `websiteUrl` | no | |

Body: 2 to 4 sentences, person-first, verifiable. No `slug` field; the directory name is the slug.

Before Stage 3, show the user the complete draft and get a yes. It's their name on it. If checking changes anything, show them the change before shipping.

### Stage 3: Check

**With a shell** (paths A, B):

```bash
node tools/validate.mjs
```

Errors must be fixed; each message says how. Warnings are advice: read them and act on the ones that apply. CI runs the same command on the PR.

**Without a shell** (paths C, D): walk this list yourself, line by line. It is what the validator enforces.

- [ ] Folder and `name:` are identical, lowercase, hyphens only, ≤ 60 characters, and not already in the library (if you could not check, say so in the deliverable)
- [ ] Frontmatter has `name`, `title`, `description`, `category`; `category` is spelled exactly as in `schema/taxonomy.json`
- [ ] No `metadata:` block, no `featured` / `rank` / `installs` / `isDefault` / `prefix` / `slug` / `author` / `license`
- [ ] Every `tools:` entry is a slug from `schema/taxonomy.json`; any product named in the body is declared there, or the body uses role verbs instead
- [ ] Body contains a line that is exactly `## What good looks like`
- [ ] Extra files are only under `references/`, flat, with an extension from: `.md .txt .json .csv .yaml .yml .py .sql .pdf .png .webp .html`
- [ ] `author.md` has `name`, `title`, `headline` (≤ 140 chars), `linkedinUrl` containing `linkedin.com/in/`, `companyDomain` as a bare domain, `expertise` with 1+ lower-kebab items; `categories`, if present, only uses taxonomy values
- [ ] No bracketed prose hints from the template left anywhere (YAML lists are fine)
- [ ] Nothing sends data to a third party, embeds a secret, overrides agent instructions, or runs a bulk/destructive step without a confirmation

### Stage 4: Ship

**Path A: shell, git, gh**

```bash
gh repo fork agiea-brain/agency-skills --clone && cd agency-skills
git checkout -b add-<skill-name>
# write files under skills/<creator-slug>/, run the validator
git add skills/<creator-slug> && git commit -m "add <skill-name>"
git push -u origin add-<skill-name>
gh pr create --repo agiea-brain/agency-skills --title "add <skill-name>" --fill
```

Complete the PR template honestly. Include `author.md` only in the first PR.

**Path B: shell and git, no gh**

Same as A, but fork in the browser first (`https://github.com/agiea-brain/agency-skills/fork`), clone the fork, push the branch, then give the user this link to open the PR:

```
https://github.com/agiea-brain/agency-skills/compare/main...<github-user>:agency-skills:add-<skill-name>?expand=1
```

**Path C: GitHub REST API with the user's token**

Preferred, a pull request:

1. `POST /repos/agiea-brain/agency-skills/forks` → note `owner.login`
2. `GET /repos/agiea-brain/agency-skills/git/ref/heads/main` → `object.sha`
3. `POST /repos/<login>/agency-skills/git/refs` with `{"ref":"refs/heads/add-<skill-name>","sha":"<sha>"}`
4. For each file: `PUT /repos/<login>/agency-skills/contents/skills/<creator>/<...>` with `{"message":"add <skill-name>","content":"<base64>","branch":"add-<skill-name>"}`
5. `POST /repos/agiea-brain/agency-skills/pulls` with `{"title":"add <skill-name>","head":"<login>:add-<skill-name>","base":"main","body":"<the PR template, filled in>"}`

Fallback, an issue: `POST /repos/agiea-brain/agency-skills/issues` with `{"title":"[submission] <skill-name>","labels":["skill-submission"],"body":"<the bundle below>"}`.

**Path D: no tools at all**

Give the user one of these, in this order of preference:

1. **A prefilled issue link.** Build the URL below with every value URL-encoded. Field names are the form's `id`s. If the finished URL is over about 8,000 characters (most skills with references are), or the link opens an empty form, use option 2 instead.

   ```
   https://github.com/agiea-brain/agency-skills/issues/new?template=submit-skill.yml
     &title=[submission]%20<skill-name>
     &creator=<creator-slug>
     &skill=<skill-name>
     &skill-md=<SKILL.md contents>
     &references=<reference pages, see bundle format>
     &author-md=<author.md contents>
   ```

2. **A paste bundle.** One Markdown block the user pastes into the "Submit a skill" issue form at `https://github.com/agiea-brain/agency-skills/issues/new/choose`, or into a PR if they have git. Format:

   ```
   === skills/<creator-slug>/author.md ===
   <contents>

   === skills/<creator-slug>/<skill-name>/SKILL.md ===
   <contents>

   === skills/<creator-slug>/<skill-name>/references/<topic>.md ===
   <contents>
   ```

   The issue form has three big boxes. `SKILL.md` box: the file contents only, no `===` line. `Reference pages` box: every reference file, each preceded by its `=== path ===` line. `author.md` box: the file contents only; leave it empty on a repeat contribution. The two short fields take the creator slug and the skill slug. Tell the user this, and that a maintainer will open the PR under their name.

   Updating an existing skill on this path: same bundle, only the files that change, and an opening line saying it is an update to `skills/<creator-slug>/<skill-name>/`.

### After shipping

Review runs format → safety → substance → identity → publish (details in `CONTRIBUTING.md`). Safety is a hard gate: anything that exfiltrates data, embeds secrets, overrides agent instructions, or runs destructive steps without confirmation is rejected. On merge, `index.json` on the `index` branch is regenerated and downstream libraries re-sync; the skill installs with `npx skills add agiea-brain/agency-skills --skill <name>`.

Tell the user what to expect: a maintainer reply on the PR or issue, possibly with edits for house voice; the substance stays theirs.
