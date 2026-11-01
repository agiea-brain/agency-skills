---
name: icp-review
title: ICP review
description: |
  Use this skill before shipping customer-facing copy you will spend money or
  reputation on: a blog post, ad, cold email, proposal, pricing or landing
  page. Produces an evidence-based buyer panel read built only from verbatim
  quotes in your own sales and client call transcripts: where a buyer stops
  reading, the strongest objection the copy raises and never answers, and the
  questions the reader brings with them, every claim tied to a real quote and
  checked by code. Also use for "ICP review this", "would this resonate",
  "what would a buyer think", "which of these lands", "why isn't this
  converting", "review this before I ship". First run walks through setup.
category: Marketing
tags: [icp, buyer-research, copy-review, voice-of-customer, call-transcripts, message-testing]
---

Applies to any draft, topic, set of variants or live page that a real buyer will read. Produces one validated verdict per seat, every claim citing a buyer quote that exists, with the strongest objection first and the verdict last.

A made-up persona invents opinions. This panel can only use what buyers actually said on calls, and when the evidence is thin it says "I can't judge this" instead of guessing.

## The play

Run every command from this skill's folder (`cd "<skill base directory>"` first). The tools are Python 3, standard library only.

1. Check setup. Read `references/profile.json`. If `setup_complete` is `false`, or `data/corpus.json` does not exist, stop and run `references/setup.md` with the user before anything else: eight short questions, then extract and tag verbatim buyer quotes from their call transcripts. Never judge copy from general knowledge as a stand-in. A panel with no corpus is a persona, and personas make things up.
2. Route. Work out the play from what the user hands over (Brief, Gate, Choose, Diagnose, Retention), pick the seats, and say in one line which ran and why. The routing table, the four seats and what each may never judge are in `references/routing-and-seats.md`. `objector` runs in every play except Brief.
3. Retrieve. `mkdir -p runs/<YYYY-MM-DD>-<slug>`, then `python3 references/panel.py evidence --seat <seat> [--persona …] [--stage …] [--pattern …] > runs/<…>/pack-<seat>.json`.
4. Respect the band. `insufficient` (n under 5): the verdict MUST be `null`; say the corpus does not cover it. `thin` (5 to 11): `confidence` MUST be `"weak signal"`. Never widen past the seat's base filter to manufacture an answer.
5. Read the widening. A non-empty `dropped` means the answer is not persona-specific. Say which level it was answered at before anything else.
6. Draft the verdict to `references/verdict-schema.json` and save it as `runs/<…>/verdict-<seat>.json`. Every assertion carries `quote_key`s drawn only from the returned pack.
7. Validate. `python3 references/validate_verdict.py runs/<…>/verdict-<seat>.json --evidence runs/<…>/pack-<seat>.json`. If it rejects, fix the verdict, never the validator.
8. Present the answer first: two or three sentences on what to fix, then the detail in the inverted reporting order in `references/routing-and-seats.md`.
9. On a Choose play with a real result coming, pre-register the pick in `predictions.jsonl` before the result exists, fill in the winner when it lands, and run `python3 references/score.py`.
10. Keep it fresh. When the user says "refresh the panel", or the newest quote is more than about 90 days old, run step 3 of `references/setup.md` on the new transcripts only, then `python3 references/build_corpus.py`.

## What good looks like

- First thing I check that most people skip: `strongest_objection`, not the verdict. The verdict tends to agree with whoever wrote the draft, because the draft came from the same instincts. The objection is the field with no polite answer.
- The mediocre version: asking an AI to "pretend to be my ICP". It reads well, cites nothing, and invents an opinion for every gap.
- Second mediocre version: running it on every draft. The dissent becomes noise and gets ignored on the one that mattered.
- I know a run is honest when a thin seat declines to judge, `distinct_calls` is reported next to the quote count, and a stale or widened slice is named before any answer.
- I know the panel is right only from `score.py`. The gate proves the evidence exists; it cannot prove the reasoning. Until roughly 30 scored predictions, these are well-sourced opinions, not calibrated predictions, and say so.

## Rules

- MUST cite only `quote_key`s from the retrieved evidence pack.
- MUST pass `references/validate_verdict.py` (exit 0) before showing the user any verdict.
- MUST include `strongest_objection` on every verdict, including favourable ones.
- MUST pre-register Choose predictions before the real result exists.
- NEVER load anything in `excluded_docs`: the user's own positioning, message house, site copy or scripts. That grades their copy against their copy.
- NEVER add the draft under review to the evidence base.
- NEVER let the panel write copy. It judges; a panel that grades its own drafts converges on its own priors.
- NEVER give a seat a name, backstory, mood or biography.
- NEVER use the `client` seat on acquisition copy.
- NEVER simulate a click path. Navigation is answered as `unresolved_questions`.
- NEVER pad the corpus with invented or paraphrased quotes.
- NEVER publish a buyer quote or attribute one to a named person or company unless `public_quote_rule` in `references/profile.json` allows it.
