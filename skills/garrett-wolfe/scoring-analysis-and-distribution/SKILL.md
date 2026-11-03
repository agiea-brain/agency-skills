---
name: scoring-analysis-and-distribution
title: TAM scoring audit and distribution fix
description: |
  Use this skill when a client's account scoring model piles everyone at the same
  score and the agency needs to audit it against the data, simulate revised
  rubrics and recommend bands, weights and multipliers that make accounts
  stack-rank, with a DQ cutoff that means something. Works on a Clay or
  spreadsheet TAM export plus its rubric. Also use for "rescore this list", "fix
  the scoring", "why is everyone scoring the same", "distribution is
  compressed", "twin-firm test".
category: RevOps
tags: [lead-scoring, tam, icp, clay, data-analysis]
tools: [clay, hubspot]
---

# Scoring Analysis & Distribution Skill

End-to-end workflow for auditing a scoring rubric, simulating revisions on the actual data, and recommending changes that **widen the spread** so accounts stack-rank usefully. Output is a single boss-forwardable doc set plus a before/after comparison.

**Before you start: read `references/scoring-tables-primer.md` for the full conceptual model (mechanics, levers, architectures, Client A worked example). Everything in this SKILL.md is the enforcement layer on top of that primer.**

## The non-negotiable workflow order

Do these phases in this order. Skipping or reordering creates rework.

1. **Phase 0: Architecture decision (FIRST, before any band design).**
   Ask the client one question: *"In your scoring tool, does DQ stop enrichment from running on a row?"*
   - **Yes** (Clay default) → use **pure-positive + smart Hard DQ** architecture. This is the default for any Clay GTM engagement.
   - **No** → ask if they'll tolerate cross-axis formula columns. If yes, use **with-multipliers**. If no, use **pure-card with negatives**.

   This decision determines which levers you can pull. Don't propose bands or weights until this is settled.

2. **Phase 1: Profile + bug-audit (BEFORE touching weights).**
   Coverage per column. Distribution stats on existing Final %. **All 4 bug detectors** (default-when-null, normalization-cap, band-gap, empty enrichment). A single bug fix often moves stdev more than any weight change.

3. **Phase 2: Apply levers within the chosen architecture.** See lever table below. Pull only the ones available to your architecture.

4. **Phase 3: Simulate side-by-side.** Original vs proposed, on the same row pool. Report stdev, histogram, twin-firm spread per axis, tier counts.

5. **Phase 4: Validate against the 6 gates.** Fail any gate → iterate within Phase 2.

6. **Phase 5: Write up.** Boss-forwardable. TL;DR table at top. Paste-ready bands for the client's tool.

## Input contract

The skill expects three things from the client (or the working directory):

| Input | Required | Form |
|---|---|---|
| **Accounts database** | yes | CSV / Clay export / DB query: one row per company, all enrichment columns + current scoring columns |
| **Per-criterion scores** | yes | Already-computed score columns per row (the `*_Score`, `*_Golden`, `Grand Total`, `Final %` columns Clay produces, or equivalent) |
| **Scoring rubric definition** | yes | The bands per card + per-criterion weight + Grand Total formula. Either documented (table) or inferable from the score columns + screenshots |
| Client context | recommended | What they sell, ICP definition, named good-fit firms |
| DQ threshold target | recommended | The Final % below which they want to disqualify (e.g. 40%). Default: pick from histogram. |

## Output contract

The skill produces these artifacts in `Clients/<Client>/scoring/analysis/`:

| File | Contents |
|---|---|
| `RECOMMENDATIONS.md` | TL;DR table (original vs proposed stdev + twin-firm spread + DQ-threshold check), list of bugs found, full revised rubric (bands + weights), 4-lever rationale |
| `simulate_v[N].py` | Per-row simulation script |
| `scored_v[N].csv` | Per-row score + breakdown columns for the revised model |
| `summary_v[N].txt` | Histogram, percentiles, top-K, twin-firm spread, tier counts |
| `display_score_lookup.txt` | GT → Display Score mapping table + paste-ready Clay IF formula (only when bell curve normalization is applied) |
| (optional) `COST_PLAN.md` | Only if new enrichment is required to close real data gaps |

Every recommendation must include:
1. Proposed new distribution (stdev + histogram shape + twin-firm spread)
2. Quantified improvement over the original
3. The new bands/scores/weights/multiplier formulas in copy-paste form for the client's tool (Clay scoring cards or formula columns)
4. Impact on the Final % for a small set of named firms (top 5, bottom 5, 3 known-good targets)
5. If bell curve normalization is applied: the GT → Display Score lookup formula, the Display Score histogram, and the recalibration trigger criteria

## The two metrics that matter

| Metric | What it measures | Target depends on architecture |
|---|---|---|
| **stdev of Final %** (within DQ=False pool) | Overall spread across the list | Pure-positive: ≥ 0.20 / Pure-card w/negs: ≥ 0.27 / With-multipliers: ≥ 0.35 |
| **Twin-firm spread** | Δ between two identical firms differing only in axis X. Run on every weighted axis. | ≥ 10 pts on the top 3 axes regardless of architecture |

Optimize both. stdev alone can be flattered by a long penalty tail without giving you adjacent-row resolution. Twin-firm spread alone can be flattered by one outsized axis weight that compresses the rest.

**The stdev target scales with architecture choice: don't compare a pure-positive 0.22 to a with-multipliers 0.37 and call it failure. Compare to the right baseline.**

## The five levers that actually widen distribution

These are the ONLY five levers. Anything else is a permutation of them.

| Lever | What it does | Free in Clay? | Pure-card OK? |
|---|---|---|---|
| **1. More bands per card** | Increases resolution within an axis. A 3-band card can emit 3 values; a 9-band card can emit 9. **Required prerequisite for any weight adjustment to matter.** | Yes | Yes |
| **2. Balance weights across axes** | Flatter weight distribution → more independent contributors summing → bell-shaped histogram. Don't pile weight onto correlated axes: it creates 5%-of-list pile-ups. | Yes | Yes |
| **3. Deep negative band values within cards** | A card with bands going from −25 to +22 has more variance than one going 0 to 22. The negative tail extends Grand Total downward and the misfit pile separates cleanly from the candidate pile. **In pure-card architecture, this is the primary spread driver.** | Yes | Yes |
| **4. Widen Fit_Multiplier swing (cross-axis)** | Compounds top-tier fit. Range 0.4-1.8 stretches the top of the histogram. Only works if client allows a separate Multiplier formula column. | Yes (one formula column) | **No: breaks the architecture** |
| **5. Deepen Negative_Penalty as separate column (cross-axis)** | Like Lever 3 but cross-axis. Catches misfits that span multiple axes (e.g. DTC consumer brands via name regex). | Yes (one formula column) | **No** |

## What does NOT widen distribution (common traps)

| Tempting move | Why it fails |
|---|---|
| Push more weight into the top axes (Industry/Reps/PE/etc.) | Those axes correlate: firms hitting all of them already top out together. More weight just creates pile-ups at the joint maximum. **Tested: pushed Industry 22→28, stdev moved +0.007 but largest bucket grew from 3.15% to 5.93%.** |
| Raise a card's raw max from 1 to 10 without adding bands | Mathematically identical to original: Golden = score/max → same 0-1 output. Resolution is set by band COUNT, not max value. |
| Add weight to an axis with low coverage | If only 5% of rows have data for axis X, bumping its weight from 5 to 15 only differentiates that 5%. Doesn't widen the overall histogram. |
| Add weight to an axis derived from another already-weighted axis (e.g. Fragmentation as Industry lookup, Rev/Rep as Revenue ÷ Reps) | Double-counts the same signal. Keep redundant-but-useful axes as tie-breakers (weight 2-5). |

## Architecture choice: three options, asked first

Ask the client which architecture they want **before** designing bands. The choice is operational, not mathematical:

| Architecture | What you can use | What you give up | Realistic stdev gain |
|---|---|---|---|
| **Pure-positive + smart Hard DQ** (RECOMMENDED for Clay-based GTM teams where DQ stops enrichment) | All scores ≥ 0. Expanded Hard DQ catches objectively-wrong-fit categories. Soft-fit firms get low positive scores. | Negative scores. Cross-axis multiplier. | **+15% to +35% over baseline** (Client A v10d est: 0.178 → ~0.22) |
| **Pure-card with negatives** | Each card max = weight. Negative bands within cards for misfit categories. No multipliers. Grand Total can go negative. | Cross-axis compounding. Cross-axis name regex. Operator must accept negative scores in the UI. | **+30% to +60% over baseline** (Client A v10c: 0.178 → 0.279) |
| **With-multipliers** | Per-card weights + Fit_Multiplier formula column + Completeness_Multiplier + Negative_Penalty column. Most aggressive. | 3 new formula columns. Most complex Grand Total formula. Cross-axis multiplier is harder to explain to a non-technical reviewer. | **+50% to +110% over baseline** (Client A v9: 0.178 → 0.367) |

### The deciding question: does DQ stop enrichment in the client's setup?

If yes (Clay default behavior): pure-positive + smart Hard DQ is correct. Negative scores feel like "soft-DQ" but actually keep the row in the enrichment loop. That's not what DQ semantically means in Clay. Use Hard DQ for "objectively wrong, never spend another credit," score-low-positive for "weak fit, keep enriching, might surface later via signals."

If no (custom workflow where DQ is just a filter for the active outbound list, not a stop-enrichment flag): pure-card with negatives gives more stdev.

### How to decide which categories belong in Hard DQ vs score-low-positive

- **Hard DQ**: the firm's industry/type is *fundamentally* wrong (software company, bank, school, restaurant). No future enrichment refinement makes them a fit.
- **Score-low-positive**: the firm *might* be misclassified, weak-fit, or have wrong data that better enrichment could refine. Keep in pool with score 0-2.

### Within whichever architecture you pick, push every lever

To maximize stdev within the chosen architecture:
- **Wide band gaps between tiers** (e.g. Tier 1 = 22, Tier 2 = 16, Tier 3 = 8: 6+ pt gaps do the discrimination)
- **Tight bullseyes** (e.g. Field Reps peak only at 60-89, with sharp taper outside)
- **Intra-card tie-breakers** when an axis has a clear primary signal + secondary modifier (e.g. PE = 10 base for any PE firm + 0-4 bonus from Fundraised $ tier; max 14)
- **Pure-card with negatives only**: deep negative bands (e.g. Industry "Other" = −25)
- **Pure-positive only**: expanded Hard DQ list catches the misfits; soft-fit categories score 0-2

### Operational tradeoff to surface in the writeup

The architecture choice has real operating consequences:

| Architecture | Enrichment cost trajectory | Stack-rank cleanness |
|---|---|---|
| Pure-positive + smart Hard DQ | Lower (no enrichment on wrong-fit) | Cleanest (0-100% range, no negatives to explain) |
| Pure-card with negatives | Higher (everything gets enriched, even -25-scoring rows) | Negative scores in UI |
| With-multipliers | Highest + 3 formula columns to maintain | Multiplier values in UI; harder to QA |

## Clay mechanics

Scoring cards hold the per-criterion bands; formula columns (Clayscript) hold DQ logic, Grand Total, Display Score and tiers. Never write a scoring card as a formula, and always wrap null guards in parentheses: `({{Col}} || 0) >= 50`. Card syntax, the paste-ready documentation format and the Clayscript precedence trap are in `references/clay-scoring-cards.md`.

## Process

### Phase 0: Workspace
Create `Clients/<Client>/scoring/analysis/`. List the phases as tasks: profile → audit bugs → simulate → validate → write up.

### Phase 1: Profile coverage and existing distribution
Use `references/profile_data.py` adapted to the client's columns. Compute:
- Per-column coverage (% non-null)
- Distribution stats on Final %: mean, median, stdev, P10/25/50/75/90/95/99
- Histogram (0.05-pct bins)
- **Largest 0.01-pct bucket** (the pile-up metric)
- Per-axis Golden column: min, max, mode, mode share

### Phase 1.1: Bug-hunt the existing scoring (always run all 4)

1. **Default-when-null detector**: for each derived score column, compare its nonzero rate to the coverage of its source columns. If derived nonzero >> source coverage, a default-when-null bug is feeding constant values to most rows.
2. **Normalization-cap check** (for each `*_Golden` column, find the observed max. If it caps well below 1.0, the denominator is larger than realistically achievable raw max) the top of that axis is unreachable.
3. **Band-gap detector**: inspect keyword bands (`1-5, 11-25, 26-50, ...`). Firms whose raw value falls in a gap silently score 0.
4. **Empty enrichment check**: any column referenced in the rubric but <2% populated is dead weight.

Bug fixes are Phase 0: execute these before iterating on weights. **A single default-when-null bug often does more damage to the distribution than any weight imbalance.** See `references/common_pitfalls.md` for worked examples.

### Phase 2: Translate the rubric and apply the 4 levers

For each card and each weight, decide which lever applies:

| Symptom from Phase 1 | Lever | Concrete fix |
|---|---|---|
| Card has ≤4 bands but covers wide value range | 1 (bands) | Add bands; log-shape for right-tailed numerics |
| Two firms identical except axis X differ by <5 pts | 2 (weights) | Bump axis X weight (only if uncorrelated with top axes) |
| Largest 0.01-pct bucket > 5% | 2 (weights) | Trim top-axis weight; spread to mid-tier axes |
| Top-K firms tied at the cap | 3 (multiplier) | Widen Fit_Multiplier swing; remove cap on Final % |
| DQ rows pile at exactly 0 (clamp) | 4 (clamp) | Drop `MAX(0, ...)` on Grand Total |
| Bad-fit firms scoring same as low-data correct-fit | 4 (penalty) | Add Negative_Penalty formula column; make penalties ≥-50 for hard misfits |
| Histogram is bimodal or step-shaped | 2 (weights) | More balanced weights → smoother curve |
| Many firms at exactly the median | sourcing | Re-check the underlying TAM filter; rubric can't fix sourcing gaps |

See `references/distribution_techniques.md` for the formulas behind each lever. See `references/levers.md` for the empirical results from past engagements showing which lever produced which delta.

### Phase 3: Simulate the revised rubric

Use `references/simulate_scoring.py` adapted to the client's columns. **Always run at least two versions side-by-side:** v[N] (current state, baseline) and v[N+1] (proposed). Report:

- stdev (target ≥ 0.30)
- Median, P25, P75
- Histogram (5-pt bins on raw final pts, 0.05 bins on Final %)
- Largest 0.01-pct bucket (target ≤ 5%)
- Tier distribution (A/B/C/D/F)
- **Twin-firm spread** for the top 3 axes by weight (synthesize identical firms varying one axis)
- Top-15 and bottom-10 named lists

### Phase 3a to 3c: Display Score, raw max and tiers

When raw stdev plateaus below target because of data coverage, add bell curve normalization as a display layer (mean 50, std 20) on top of the raw Grand Total, which stays the source of truth. A raw max of 85 to 95 is correct for a rubric with tight bullseyes; do not loosen them to reach 100. Tier on Display Score: 20 tiers at 5% intervals (T1 best), plus a coarse 5-tier column for reporting. Process, formulas and the recalibration trigger are in `references/display-score-and-tiers.md`.

### Phase 4: Validate against gates

| Gate | Target | If fails |
|---|---|---|
| Raw stdev (DQ=False pool) | ≥ 0.15 (raw), or ≥ 0.20 (after bell curve) | Apply more aggressive levers or bell curve normalization |
| Largest 0.01-pct bucket | ≤ 5% | Weights too top-heavy: flatten across mid-tier axes |
| Twin-firm spread on top 3 axes | ≥ 10 pts each | Weight too low on the failing axis; bump it (only if uncorrelated) |
| DQ threshold separation | DQ rows median ≤ threshold − 10 pts; real candidates median ≥ threshold + 10 pts | Negative_Penalty too shallow; deepen |
| Top-K named good-fit firms | ≥ 80% appear in A or B tier | Sourcing gap OR specific bug: re-run Phase 1.1 |
| Histogram shape (Display Score) | Bell-shaped around 50; 20 tiers at 5% intervals with predictable populations (T20 ≈ 2.4%, T11 ≈ 9.2%, T1 ≈ 2.5%) | Rubric iteration or recalibrate bell curve lookup |
| Raw Grand Total max | ~85-95 (NOT 100) for a well-designed rubric. Don't loosen bullseyes to reach 100: that reduces discrimination. Use Display Score for the 0-100 UX. | If raw max < 80, bullseyes may be too tight. If raw max = 100 on many rows, bullseyes are too loose. |
| Rows at Display Score = 100 | ≤ 3% of non-DQ pool (the true top tail). | If >3% pile at exactly 100, suspect the inv_norm_cdf function has the operator-precedence bug (numerator polynomial not wrapped in outer parens: `c[5] / denom` parses as a separate term). See `references/bell_curve.py` for the correct implementation. |
| Rows at Display Score = 0 | ≤ 3% of non-DQ pool. | Same bug as above (tail branch broken). Or DQ list is letting too many true zero-fit rows through. |

### Phase 5: Write up

`RECOMMENDATIONS.md` template:

```
# TL;DR: table comparing original vs proposed on:
#   stdev | mean | median | largest 0.01-pct bucket | A-tier % | F-tier %
#   twin-firm spread for top 3 axes
#   DQ threshold (e.g. "all 5,362 F-tier firms below -10 pts, all real candidates above 25 pts")

# Bugs found in current model (Phase 1.1 output)
# Revised rubric (paste-ready bands + weights + formulas)
# 4-lever rationale: which lever was pulled, why, expected stdev delta
# Validation gate results
# Open questions (sourcing gaps, data-gap fixes that need budget: defer to COST_PLAN.md)
```

## What good looks like

- The architecture question is asked first, and bugs are found and fixed before any weight changes.
- Baseline and proposed models always appear side by side, with the twin-firm test run on every axis weighted 5 or more.
- The proposal passes the gates: stdev at the target for its architecture, largest 0.01 bucket at 5% or less, twin-firm spread of 10 points or more on the top 3 axes.
- Red flag: pushing more weight into correlated top axes. It barely moves stdev and creates pile-ups at the joint maximum.

## Key conventions

- **Always run the twin-firm test.** Synthesize one row from your top-15, clone it 8-10 times varying ONE axis, score all of them, report the spread between #1 and #10. Repeat for each axis with weight ≥ 5.
- **Two versions side-by-side, minimum.** Never report a proposed model without showing the baseline numbers next to it.
- **Bugs before weights.** A default-when-null bug or normalization-cap bug undoes any weight tuning. Find them first.
- **Bands first, weights second, shape third.** Number of bands sets the upper bound on resolution. Weights determine each axis's share. Multiplier/penalty stretch the top and bottom. Always in that order.
- **The bottom matters as much as the top.** Negative_Penalty + no-clamp on the Grand Total formula is responsible for ~half of any meaningful stdev improvement. Don't skip it.
- **Boss-forwardable means one number at the top.** TL;DR has the headline (stdev gain + twin-firm spread gain). Detail goes below.
- **No emojis in docs.**

## When NOT to use this skill

- Building a scoring model from scratch with no existing data
- Pure outreach copy or enrichment with no scoring question

## References

- **`references/scoring-tables-primer.md`: READ FIRST. Full conceptual model: mechanics, 6 levers, 3 architectures, validation gates, Client A empirical track (v4 through v10d). Everything in this SKILL.md is the enforcement layer on top of that primer.**
- `references/levers.md`: empirical results table for all 6 levers + architectural decision flowchart
- `references/distribution_techniques.md`: formulas: log transforms, multiplicative gates, type-aware scoring, percentile normalization, completeness multipliers
- `references/common_pitfalls.md`: failure modes and their fixes

## Templates

- `references/profile_data.py`: coverage + distribution profiler + 4 bug detectors (run in Phase 1)
- `references/simulate_scoring.py`: simulation harness with `ARCHITECTURE` toggle, twin-firm test, DQ-threshold validation, side-by-side comparison report. **Defaults to pure-positive architecture.**
- `references/bell_curve.py`: Phase 3a Display Score normalization. Reads the scored CSV, builds the GT→Display lookup, emits paste-ready Clayscript IF formula. **Includes built-in saturation gates** (warns if >3% of rows pile at Display=100 or =0, which indicates the inv_norm_cdf operator-precedence bug).
