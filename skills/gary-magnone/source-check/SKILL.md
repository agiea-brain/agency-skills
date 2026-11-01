---
name: source-check
title: Source check before sending
description: Audits a finished deliverable claim by claim before it goes to a client, and traces a number back to its origin when somebody on the client side says it is wrong. Lists every factual claim in the deck, doc, or sheet, ties each one to a named primary source, and marks the ones that cannot be sourced so they get cut or backed up before the thing ships. Use when the user says "/source-check", "fact check all of this", "fact check yourself", "where did we get [the number]", "how do you know that", "I need to be 100% confident in the source for every finding", "read the sources before quoting any of it", "before this goes to [client]", or when someone on the client side says a figure in a deliverable is wrong. Never sends anything.
category: Operations
---

# /source-check

The user's name is on the deck. When a number in it is wrong, the client's own marketing person finds it, flags it in the comments, and every other number in the file gets doubted too. This skill is the pass that happens before that, and the trace that happens after it when one gets through.

Two modes. **Pre-flight** audits a whole deliverable before it ships. **Trace** takes one disputed claim and finds where it came from, what the true number is, and what else in the file moves because of it.

Siblings: `/work-review` judges something a teammate built. `/rundown` writes the note that goes out with the finished piece. This skill checks a finished artifact.

## When to use
- A deck, strategy doc, plan, audit, or report is about to go to a client or get presented by somebody else
- The user has to speak to findings they did not personally pull, or somebody else is running the call and the user is on for depth
- A client or someone on their team says a figure is wrong, or comments on a slide
- A section came back reading confidently and the user does not believe it

## When not to use
- Building the deliverable in the first place. This runs on a draft that already exists.
- Line editing or voice. That is the style guide's job.

## Inputs
1. **The deliverable.** The actual file, deck, sheet, or live URL. Open it and read what is in it now, not the conversation about it.
2. **The source set it was built from.** The exports, transcripts, screenshots, tool pulls, and client docs in the client's project folder. List them before you start.
3. **The client's account notes** for what their stack is, who owns which system, and which tools they use.
4. **The dispute, in trace mode.** The exact comment, the number the client says is right, and the screenshot or export they pointed to.

## What counts as a claim

Every one of these gets a row. Nothing else does.
- Any number, percentage, dollar figure, or count
- Any date range, and the comparison window next to it
- Any statement about what the client has, does not have, or is doing today ("they have no service pages," "nothing is tracked")
- Any statement about a competitor
- Any quote or paraphrase attributed to a person
- Any industry or benchmark figure that came from outside the client's own data

## Workflow

**1. Build the source list first.** Name every file, export, transcript, and tool pull the deliverable could have drawn from, with its date. A source that is itself a summary is not a source. If a claim traces back to a prior deck, a recap, or an earlier AI session, keep walking back until you reach the export, the transcript, or the live tool.

**2. Pull every claim into a ledger.** One row per claim, in the order they appear, with the slide or section number so the user can find it fast.

| # | Where | The claim as written | Source | Verdict | What to do |

**3. Verdict each row.** Four verdicts, no others:
- **Sourced.** Names the file or tool, the date range, and the exact field. "CRM contact export, all time, Original Source = Form."
- **Thin.** True but built on a small sample, a demo pull, or one month. It can stay if the deliverable says so on the slide.
- **Unsourced.** Nothing in the source set produces this. It gets cut or it gets a data request. It does not get softened into a hedge.
- **Wrong.** The source set says something different. Give the correct figure in the same row.

**4. Check the definition, not only the arithmetic.** Most of these are not math errors. They are the wrong field from the right tool. Before marking a number Sourced, say in one line what the field counts and whether that is what the sentence claims. Website analytics form submissions and CRM contacts by original source are different populations, and quoting one as the other can be off by thousands. Sessions are not users. Leads are not calls.

**5. Never mix two estimate tools in one claim.** Two SEO or traffic estimate tools can disagree enough to reverse a finding. Name which one the number came from, and use one of them for a whole comparison.

**6. Flag at the real size.** A best practices cleanup is not a broken system. If a finding is true but overstated, mark it Thin and rewrite it at its actual size rather than deleting it. Over-flagging costs as much trust as under-flagging.

**7. Keep the client's team out of it.** The ledger says what a number is and where it came from. It never says who got it wrong or how well anyone does their job.

**8. Say what else moves.** When a claim changes, list every other slide, chart, or recommendation built on it. In trace mode this is the point of the run. A number that moves from 1 to several thousand does not fix one slide. It changes what the deliverable argues.

**9. Hand the user the short version first.** Three lines at the top before the table: how many claims, how many Unsourced or Wrong, and the one that matters most. Then the ledger. Then, if anything is Unsourced, the exact data request to send, written as a list of files by name.

**10. Fix nothing without the user.** Propose the corrected wording per row. Do not rewrite the deliverable until the user picks the rows.

## Output

Write the ledger next to the deliverable it checks, in the client's project folder:

`source-check/<deliverable-name>-claims.md`

For a trace run, the same folder, named `<claim>-trace.md`. Keep the file, because the next version of that deck gets checked against it.

Never send, post, or comment anywhere. Show it and stop.

## What good looks like

- First thing I check that most people skip: statements about what the client does not have. "They have no service pages" is a claim and needs a source like any number does.
- The mediocre version checks the numbers and leaves the framing sentences alone. Dates, comparison windows, competitor statements and attributed quotes all get a row.
- I know it is right when every claim has a named source next to it before the client sees it, and anything that cannot be sourced is pulled rather than softened.
- The cost of missing one is not the number. The client's team knows their own data, so one wrong figure in their comments puts the whole deliverable in doubt.

## Why this exists

AI makes the first draft of a deck fast, and it states every number with the same confidence whether it came from an export or from nowhere. The client's team knows their own data, so a wrong number gets caught in their comments, and then the whole deliverable is in doubt. This skill puts a named source next to every claim before the client sees it.
