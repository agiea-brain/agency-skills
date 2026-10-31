# Contributing

You can contribute with your AI agent (paste the prompt in the [README](README.md#contribute-a-skill-in-one-sitting)), by hand with git, or by filling in an issue form if you have neither. The format and the bar are the same on every route.

## Before you write

**Pick one thing you are unusually good at.** The best skills here are narrow: "how I run a pipeline review", not "sales". If you can describe the moment someone should reach for it in one sentence, it's the right size. Name the folder after that moment or the artifact it produces, in 2 to 5 words (`pipeline-review-coaching`, `first-90-days-transition-plan`).

**Decide which kind of skill it is.**

- *Tool-agnostic*: coaching and operating playbooks. Written in role verbs ("check the CRM", "pull the last three sessions") so they work on any stack. No product names.
- *Tool-specific*: implementation playbooks about a named product. List every product in `tools:` (slugs from `schema/taxonomy.json`) and name it freely in the body.

Mixing the two is the most common reason a draft comes back: a coaching skill that quietly assumes HubSpot, or an implementation skill that never says which product.

## Writing it

Start from `templates/skill/SKILL.md` and `templates/author.md`. The skill body has a fixed spine:

1. One line: when this applies. One line: what it produces.
2. `## The play`: the procedure, with branches (by segment, by company stage, by what you see).
3. `## What good looks like`: required. What you notice first, what the mediocre version does, how you know the output is good.
4. `## Rules`: the MUSTs and NEVERs.

Keep the body to roughly 500 to 800 words and move the heavy material (scoring rubrics with real thresholds, session scripts, configuration checklists, worked examples, edge-case playbooks) into `references/<topic>.md`. The body says when to open each one. Skills with no references are usually skills whose author stopped too early.

Avoid anything that rots: dates, "recently", menu paths and button names that change on the next release.

## Your profile

Your first PR includes `skills/<your-slug>/author.md`. The directory name is your permanent slug: `firstname-lastname`, lowercase, hyphens; add a word if that is already taken. Required: `name`, `title`, `headline` (one line of what you help with, under 140 characters; it's what people search by), `linkedinUrl` (your own profile), `companyDomain`, `expertise` (keywords). Optional: `email`, `avatarUrl`, `categories`, `websiteUrl`. Maintainers verify that you're a real person before merging; a personal LinkedIn is the primary check. Your email, if given, is visible in this public repo but is never copied into the published index.

## Submitting

**With git**

```bash
gh repo fork agiea-brain/agency-skills --clone && cd agency-skills
git checkout -b add-<skill-name>
# add files under skills/<your-slug>/
node tools/validate.mjs
git add skills/<your-slug> && git commit -m "add <skill-name>"
git push -u origin add-<skill-name>
gh pr create --fill
```

One skill per PR. Include `author.md` in your first PR only; later PRs that re-add it will conflict.

**Without git**: open a ["Submit a skill" issue](https://github.com/agiea-brain/agency-skills/issues/new/choose) and paste your files into the form. A maintainer turns it into a PR under your name.

## Review

Every submission is checked in this order; the first failing step is where it comes back to you.

| Step | What's checked | Who |
|---|---|---|
| Format | `node tools/validate.mjs` passes; files in the right place | CI |
| Safety | Nothing in the files could harm the person running the skill (below) | Maintainer |
| Substance | Trigger, judgment, depth (the three tests from the README) | Maintainer |
| Identity | A real person, verifiable from `author.md` | Maintainer |
| Publish | Merge; `index.json` regenerates; downstream libraries re-sync | CI |

Small format and wording fixes are made by maintainers rather than bounced. Substance stays yours.

## Safety: what is rejected outright

A skill is a set of instructions that strangers' agents will follow against their own CRM, inbox and files. Any of the following ends the review:

- Instructions that send data to an address, endpoint or webhook the reader doesn't control
- Embedded secrets, tokens, or URLs that receive data
- Text that tries to override the agent's instructions or disable its approval steps
- Bulk or destructive actions (delete, mass email, mass update) with no human confirmation step
- Asking the end user for passwords or API keys

Report a published skill that does any of this via [SECURITY.md](SECURITY.md).

## Scope of this repo

This repository holds content only. Nothing here ranks, features, or auto-installs a skill anywhere; frontmatter that tries to (`featured`, `rank`, `installs`, `isDefault`) fails validation. Those decisions are made in the systems that serve the library.

## License

MIT, with attribution through your creator profile.
