---
name: sales-call-market-analyzer
title: Sales call market analyzer
category: Marketing
tags: [positioning, jobs-to-be-done, icp-definition, market-segmentation, call-analysis]
description: Analyze batches of intro, discovery, or early-stage B2B sales calls to reveal whether the prospects entering a funnel represent one coherent market or multiple distinct market segments. Use when ChatGPT needs to inspect sales-call transcripts from uploads, pasted text, or connected call-recording sources and extract each prospect's specific job-to-be-done framing, current solution or competitive alternative, persona, and company firmographics; conservatively cluster genuinely equivalent patterns; surface fragmentation and dominant segment signatures; and teach the user how to interpret the evidence without summarizing meaningful differences away.
---

# Sales Call Market Analyzer

Analyze sales calls as market evidence, not as generic call summaries.

The goal is to show **who is actually entering the funnel, what specific job they believe they are trying to do, how they solve it today, and how consistently those patterns repeat.**

The central principle is:

> Variation is not noise to clean up. Variation can be the market signal.

## Workflow

1. Gather the calls.
2. Identify which calls are suitable for analysis.
3. Extract call-level market evidence.
4. Preserve the prospect's specific JTBD framing.
5. Normalize only where meaning is clearly interchangeable.
6. Cluster conservatively across JTBD, current solution, persona, and company.
7. Build segment signatures from recurring combinations.
8. Present the call-level table first, followed by cluster views and teaching observations.

## 1. Gather the calls

Accept calls from any source the user can provide access to, including:

- uploaded transcript files
- pasted transcripts
- call summaries that preserve enough prospect language to support the analysis
- connected call-recording or meeting tools available in the user's environment

Do not require a particular recorder, MCP, API, or connector. Treat access as a separate transport layer from the analysis methodology.

When connected call data is available, retrieve the requested intro/discovery calls before analyzing. Prefer recent calls when the user asks for a current view of the funnel.

If the source contains many meeting types, prioritize prospect-facing intro, discovery, qualification, or first substantive sales conversations. Exclude internal calls, customer support calls, recruiting calls, and later-stage calls dominated by pricing/procurement unless the user explicitly wants them included.

## 2. Extract call-level market evidence

For every usable call, extract these fields:

| Field | What to capture |
|---|---|
| Prospect / account | Person and company when available |
| Industry | Specific industry or vertical; do not invent |
| Company firmographics | Employee range, stage, revenue band, geography, business model, or other materially relevant attributes when known |
| Persona | Function, role, seniority, and buyer/user relationship when evident |
| Prospect JTBD framing | A close paraphrase of the specific job the prospect believes they are trying to do |
| JTBD evidence | Short supporting phrase or moment from the call; quote sparingly |
| Current solution | What they do today instead of using the product |
| Current-solution evidence | Supporting phrase or moment from the call |
| JTBD cluster | Conservative cluster label; leave distinct when meaning is not obviously interchangeable |
| Current-solution cluster | Group strategically equivalent alternatives only when useful |
| Persona cluster | Function/seniority grouping when useful |
| Company cluster | Firmographic/industry grouping when useful |
| Segment signature | Recurring combination of company type + persona + JTBD + current solution |
| Confidence / ambiguity | Note uncertain interpretation or missing evidence |

Prefer `Unknown / not established in this call` over guessing.

## 3. Treat JTBD framing as primary evidence

Do **not** treat the JTBD field as a generic intent-summary exercise.

Capture the specific way the prospect understands the job. Preserve distinctions in:

- the object of the job
- the trigger or situation creating the job
- the process or action they are trying to perform
- the desired result
- the scope of the work
- the language they use to define success

Avoid abstracting upward into umbrella ideas such as:

- improve efficiency
- grow revenue
- automate workflows
- improve sales
- manage data
- save time
- improve marketing

when the prospect has expressed something more specific.

A broad label is useful only if a listener would immediately and unambiguously understand the same underlying job from it.

## 4. Cluster JTBDs conservatively

Use this decision test before placing two JTBD framings in the same cluster:

> Could the framing from Prospect A be substituted into Prospect B's conversation, and vice versa, without changing the buyer's meaning or requiring explanation?

If **yes**, cluster them.

If **maybe**, keep them separate and mark them as `Adjacent / potentially distinct`.

If **no**, keep them separate.

Do not merge clusters merely because:

- the product could serve both jobs
- the jobs occur in the same department
- the ultimate business outcome is similar
- the jobs share a broad category such as lead generation, analytics, automation, collaboration, or productivity
- a higher-order summary makes the table look cleaner

Optimize for preserving meaningful market differences, not for minimizing the number of clusters.

Read `references/jtbd-clustering.md` when resolving difficult clustering decisions or explaining the methodology.

## 5. Analyze the current solution as the competitive alternative

Capture what the prospect does **today** to accomplish the job.

This may be:

- incumbent software
- spreadsheets
- internal staff
- manual work
- agency or consultant
- custom-built tooling
- multiple point solutions
- doing nothing / tolerating the problem
- a different workflow that avoids the job entirely

Do not automatically collapse all manual or internal approaches into `DIY` if the distinction materially changes what the product competes against.

Ask: **Would selling against these alternatives require substantially the same competitive story?**

If yes, a shared cluster may be useful. If no, preserve them separately.

## 6. Analyze persona and company without over-weighting them

Persona consistency alone does not prove market consistency.

For example, three RevOps leaders can represent three distinct segments if they frame the job in materially different ways.

Likewise, firmographic variation alone does not prove fragmentation if buyers across company types repeatedly frame the same job and replace the same solution.

Use persona and company characteristics as dimensions that strengthen or weaken recurring patterns rather than as the sole definition of a market segment.

## 7. Build segment signatures

Create a `Segment signature` by combining the dimensions that repeatedly travel together:

`Company type + Persona + Prospect JTBD framing/cluster + Current solution`

Prefer specific signatures such as:

`Series A-B B2B SaaS + VP Marketing + clarify how a complex product is explained to buyers + internal marketing team`

rather than:

`SaaS marketers + improve marketing`

Count repeated signatures and highlight dominant, secondary, and outlier patterns. Do not imply statistical certainty from a small sample.

## 8. Output the analysis

Make the call-level table the primary output.

### A. Coverage note

State:

- number of calls supplied
- number analyzed
- number excluded and why
- important evidence gaps

### B. Call-level market table

Include the most useful columns from the extraction schema. Keep the prospect's JTBD framing visible; never replace it with only the cluster label.

When the environment supports an interactive table or spreadsheet-like output, use it so the user can filter by JTBD cluster, current-solution cluster, persona, company characteristics, and segment signature.

### C. Cluster views

Summarize recurring patterns separately for:

- JTBD framing
- current solution / competitive alternative
- persona
- company type
- segment signatures

Use counts and proportions when the sample makes them meaningful.

### D. What to notice

Add 2-5 short teaching observations that help the user interpret the evidence.

Good observations explain *why* a pattern matters, for example:

- `These prospects share the same persona but describe three materially different jobs. Persona consistency alone is hiding market fragmentation.`
- `The job is extremely consistent even though company size varies. Firmographics may be less important than the situation triggering demand.`
- `I kept these two JTBDs separate. They are adjacent, but the buyer would need an explanation to see them as the same job.`
- `I could summarize these as “improve sales efficiency,” but that would erase a useful distinction in how prospects understand the job.`

### E. Fragmentation read

End with a qualitative diagnosis such as:

- `Strongly coherent`
- `Mostly coherent with one secondary segment`
- `Several meaningful segments`
- `Highly fragmented`
- `Insufficient evidence`

Explain the diagnosis in 2-4 sentences using the observed patterns.

Do **not** invent a numerical consistency score unless the user explicitly requests a scoring model.

## 9. Teach while applying the methodology

Act like a Fletch analyst helping the user learn to see the market evidence.

When making a non-obvious clustering decision:

1. State the decision.
2. Briefly explain why.
3. Connect the distinction to the possible market implication.

When the user proposes merging two clusters, do not automatically comply. Evaluate whether the merge would erase meaningful differences. Push back politely when necessary.

When the user proposes splitting a cluster, evaluate whether the difference genuinely changes how the prospect defines the job or what the product competes with.

Keep teaching concise. The analysis should remain useful, not turn into a positioning lecture.

## What good looks like

- The first thing to check is whether the prospects who look alike actually are alike. Three people with the same title, at similar companies, can be describing three different jobs. Persona and firmographic consistency are the easiest places to mistake tidiness for a coherent market.
- The mediocre version of this analysis produces a short list of clean clusters. It reaches labels like "improve sales efficiency" or "automate workflows", loses the prospect's own framing, and leaves the reader with nothing they could not have guessed before reading any calls.
- The output is right when a reader can see each prospect's specific job in their own terms, can tell which distinctions were deliberately kept apart and why, and ends with a fragmentation read that is traceable to the rows above it rather than asserted.

## 10. Boundaries

This skill diagnoses the **current funnel composition and market patterns** visible in sales calls.

Do not automatically:

- choose the company's future ICP
- recommend a new positioning
- rewrite messaging
- declare a segment strategically attractive
- conclude that the dominant observed segment is necessarily the best market to pursue

Those are downstream strategy decisions requiring additional evidence.

It is appropriate to say that a pattern **may require different problem framing, competitive framing, or value explanation**. Stop short of prescribing that messaging unless the user explicitly asks for a separate strategy step.
