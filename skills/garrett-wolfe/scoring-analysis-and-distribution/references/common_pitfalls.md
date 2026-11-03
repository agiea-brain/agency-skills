# Common Pitfalls: Scoring Model Audits

Compiled from past client engagements. Check each before declaring an audit complete.

---

## Derived score bugs (Phase 1.1: most-common, highest-leverage)

### Default-when-null on a "Contains Text" formula
**Symptom:** A derived score (e.g. `Domain Experience Golden`) is nonzero on 98%+ of rows, but its source column has data on a tiny fraction (5% or less).
**Root cause:** Clay-style scoring nodes with "Contains (Text)" comparisons silently match a default-bucket keyword (often "none") against empty cells, returning a non-zero score to every empty row. The result is a constant added to every Grand Total, squashing the distribution.
**Detection:** Compare `nonzero_rate(derived)` to `max(coverage_rate(source_cols))`. If derived nonzero is dramatically larger than source coverage, this bug is live. The `DERIVED_SCORE_AUDIT` config in `profile_data.py` automates this.
**Fix:** In the scoring formula, explicitly check for empty input and return 0. Don't rely on "Contains" semantics for the empty case.
**Example:** Domain Experience Golden was 0.4 (40% of max) on 30,242 of 30,671 rows because empty `Domain Expertise Classification` strings matched the "none" keyword. After fixing the bug, the median dropped from 18% to 13%: accurate distribution shape was hidden under a +1.5pt fixed offset on every row.

### Normalization denominator larger than realistic max
**Symptom:** A `*_Golden` / `*_Pct` column maxes out at 0.5 or 0.6 across the entire dataset: no row ever hits 1.0.
**Root cause:** The percentage formula's denominator is larger than any combination of bands can actually reach. Top firms lose 40% of their credit on that axis automatically.
**Detection:** For every supposedly-0-to-1 column, check `max(column)`. If < 0.95, the denominator is wrong.
**Fix:** Either reduce the denominator to match the realistic top, OR raise the top-tier raw band so it can hit the cap.
**Example:** Country Score Golden capped at 0.60 (raw scores 0-3, denominator 5). Global Presence Golden capped at 0.50 for the same reason. Both were silently bottlenecking top firms.

### Band gap in keyword rubric
**Symptom:** A specific numeric range silently scores 0 because the rubric's bands skip it.
**Root cause:** Keyword bands like `1-5, 11-25, 26-50, ...` miss `6-10` (typo/oversight at rubric setup). Firms with values in the gap fall through to the default 0.
**Detection:** Eyeball the band definitions for off-by-one gaps. For numeric inputs, verify `for v in 1..max_observed: at least one band matches v`.
**Fix:** Add the missing band.
**Example:** Specialist bands skipped 6-10. ~3.7% of firms with specialist data fell in the gap and scored 0 on their strongest signal.

### Dead column referenced in rubric
**Symptom:** A scoring criterion references a column that's 0% populated across the entire dataset.
**Root cause:** The enrichment step that populates the column never ran, or got disconnected from the workflow.
**Detection:** `profile_data.py` auto-flags any column with <2% coverage. Cross-reference against the rubric: any rubric criterion sourced from a dead column is dead weight.
**Fix:** Either repair the enrichment step or remove the criterion from the rubric.
**Example:** `Distinct Company Countries` was an input to Global Presence Scoring but populated 0/30,671 rows. Half of Global Presence's signal was structurally unreachable.

### Sourcing gap masquerading as scoring problem
**Symptom:** Top of new score list looks reasonable but is missing the obvious canonical leaders for the domain.
**Root cause:** The source list (HubSpot, Apollo, manually-curated CSV) never had those entities to begin with. No scoring tweak can fix this.
**Detection:** Maintain a per-domain "canonical top 20" list. Grep source CSV for each. Surface missing entities as sourcing issues, not scoring issues.
**Fix:** Fix the source list before continuing to iterate on scoring. Wrong list + perfect rubric = wrong answer.
**Example:** the top 20 by new score looked legitimate, but 20+ canonical leaders in the vertical were entirely missing from the 30K source. It needed a CRM list fix, not a rubric fix.

### Mixed-population list with single rubric
**Symptom:** Two structurally different entity types in the same list (service firms + in-house teams), both clustering at low scores despite legitimate good-fit candidates in both.
**Root cause:** The rubric is built around one type's axes. The other type gets zeros on every type-specific axis. Adding a "default to average" papers over the issue but kills signal for both types.
**Detection:** Cross-tab score median by entity type / classification. If two populations have very different medians AND very different axis-coverage profiles, single-rubric scoring is mis-handling at least one of them.
**Fix:** Type-aware scoring with three axis groups (universal / type-A-only / type-B-only) and parallel rubrics. See `references/distribution_techniques.md` §3.
**Example:** Corporate / In-House (21K rows) clustered at median 11%; Service firms (1.5K rows) clustered at median 20%. Single rubric was scoring corporates on service-firm axes (practitioners, specialists) where they structurally have zero.

---

## Data quality

### "Global 51+ FTEs" list with median FTE of 7
**Symptom:** Source list claims a filter applied; actual data violates it.
**Root cause:** The filter ran at source-pull time but enrichment overwrote the FTE column with a different (often wrong) value.
**Fix:** Surface the discrepancy in the audit. Recommend re-applying the filter post-enrichment, with a carve-out for known-good exceptions (e.g., small specialist boutiques).

### Small-entity matched to giant-corp via fuzzy LinkedIn match
**Symptom:** Row shows 79K FTEs at a one-person local firm.
**Root cause:** LinkedIn-enrichment fuzzy-matched a small name to a big company with overlapping tokens .
**Fix:** Entity-mismatch heuristic: when small-entity cue (LLC, P.C., "Offices of") + giant FTE + LinkedIn name diverges from source name, suppress derived fields.

### Defunct entities still in the list
**Symptom:** Top of new score list contains firms that merged or dissolved years ago.
**Root cause:** Source list never refreshed; CRM has stale records.
**Fix:** Cross-reference a public list of defunct companies for the vertical against the name column. Filter or flag.

### Inconsistent column sources
**Symptom:** FTE column says 1, Practitioners column says 1136 for the same firm.
**Root cause:** FTE came from LinkedIn (which sometimes captures local-office headcount only), Practitioners came from people-search (which captured firm-wide).
**Fix:** Document the source per column. Don't compare across columns without first asserting same-source.

---

## Rubric design

### Highest-weight criterion has lowest coverage
**Symptom:** Specialist Count weighted 28%, populated on 5% of rows.
**Root cause:** Client designed the rubric around the ICP-defining dimension, but enrichment never filled it.
**Fix:** Either spend to enrich (Phase 2 in the standard flow), or switch to proportional weighting so unenriched rows aren't all clustered at the floor.

### Saturated criterion adds noise to the floor
**Symptom:** Country weighted 20% with 60% US + 35% other tier-1 → 95% of rows score 0.95+ on country.
**Root cause:** Tier-1 includes ~80% of the list, so country adds the same constant to almost every row instead of differentiating.
**Fix:** Cap the country weight; convert to a binary qualifier (in-region or not); or split into finer tiers (e.g., separate US from EU).

### Bin boundaries on dense data
**Symptom:** Histogram of raw values shows median at 3 practitioners; rubric bin boundary is at 3 practitioners (1-3 → 0.2, 4-10 → 0.4).
**Root cause:** Round-number bin design without inspecting the actual data distribution.
**Fix:** Sigmoid centered on the data median, or move bin boundaries to natural breaks (10th, 25th, 50th, 75th, 90th percentile).

### Contains (Text) keyword list incomplete: silent coverage drop
**Symptom:** A scoring card that had 98% coverage suddenly shows 48% nonzero after editing keywords. No error: companies just silently score 0.
**Root cause:** Clay's Contains (Text) comparison only matches values explicitly listed in the Keywords field. Any country, classification, or category not in the keyword list scores 0 with no warning. When switching from a broad keyword list to a tiered one (e.g., giving different countries different scores), it's easy to omit countries that were previously covered by a catch-all.
**Detection:** After any edit to a Contains (Text) card, immediately check the nonzero rate of the output score column. If it dropped significantly from the previous version, keywords are missing.
**Fix:** Build exhaustive keyword lists. For Country cards, include all countries present in the data: even low-value ones at a baseline score (e.g., 0.5). For Classification cards, include every distinct value from the column. Use a `SELECT DISTINCT` / `Counter()` on the source column to generate the complete list before configuring the card.
**Example:** Country Score card was edited to differentiate jurisdictions (US=3, UK=2.5, etc.). Germany (822 rows), India (3,832 rows), China (1,953 rows), and 20+ other countries were omitted from the keyword list. Coverage dropped from 98% to 48%: 15,579 companies silently scored 0 on Country. No Clay error surfaced.

### Missing data → zero (the silent killer)
**Symptom:** Rows with sparse data all collapse to the same low score, indistinguishable from rows that genuinely score low.
**Root cause:** "Missing = 0" treats unknown as bad, instead of as unknown.
**Fix:** Proportional weighting. Re-normalize the score over the criteria that have data when row has ≥50% of total weight populated. This is the single highest-impact distribution fix on most TAMs.

---

## Scoring fitness

### Top of list contains non-ICP rows
**Symptom:** A US oil-and-gas conglomerate scored 0.76 in a "service firm TAM."
**Root cause:** No fitness gate. The rubric scores anything that has the right enriched columns, regardless of whether it's actually the buyer type.
**Fix:** Add a fitness gate keyed on industry / classification / description language. Zero out scores for rows that fail the gate. Be explicit about what "fit" means for this client.

### Top-N validation never done
**Symptom:** Cost plan approved on the strength of distribution stats alone.
**Root cause:** Easier to compute stdev than to eyeball top-25 against actual closed-won.
**Fix:** Always include manual top-25 inspection in acceptance gates. If closed-won data exists, validate against it. If not, validate against the client's stated top-20 known wins as a proxy.

---

## Time-sensitive vs. structural signals

### Recent activity as time-decay
**Symptom:** Rubric has "days since last event" scored on recency.
**Root cause:** Recency is a *signal* (good for outreach trigger timing), not a *fit* attribute (good for ICP scoring).
**Fix:** Convert to structural: "≥1 event in last 5y" yes/no, or rolling-5-year count. Stable, time-invariant.

### Job posting / news / fundraise in scoring
**Symptom:** "Posted a relevant role last month" → +0.5 score.
**Root cause:** Confusing intent signals with ICP fit. The firm is the same firm regardless of last month's job posting.
**Fix:** Keep intent signals for outreach trigger flows, never for the static scoring model. Flag this explicitly to the client.

---

## Cost estimation

### Padding the bill with outreach data
**Symptom:** Scoring cost plan includes Mobile Finder, Personal Email, work-email enrichment.
**Root cause:** Conflating "score the list" with "reach the list."
**Fix:** Hard rule: scoring cost plans contain only line items that improve a score or fix a data-quality issue poisoning scores. Phone/email/mobile go in a separate outreach cost plan, billed after the scored list is approved.

### Claiming Clay charges credits for scoring logic
**Symptom:** Cost doc says "Clay charges X credits per row for bin lookups / IF-ELIF / dict scoring."
**Root cause:** Conflating Clay enrichment actions (Find People, Use AI, HTTP, scrape) with formula columns.
**Fix:** Clay credits burn only on enrichment actions. Formula columns and column references are free. Scoring rubric logic (bin lookups, dict tier maps, regex matches on present text, IF/SWITCH on FTE bands) costs $0 in Clay.

### Re-enriching columns that are already populated
**Symptom:** Cost plan proposes Country enrichment at $X when source CSV has Country at 97% coverage.
**Root cause:** Skipped the existing-vs-net-new inventory step. Defaulting to "rerun the whole workflow."
**Fix:** Always build the three-bucket inventory before pricing anything. Every cost line must trace to a "net-new" or "repair" row.

### Quoting prices from memory
**Symptom:** Cost doc cites prices that don't match current provider pricing.
**Root cause:** Forgot to check the provider's current pricing for each cited tool.
**Fix:** Re-confirm every price live. Pricing changes; quote-checking takes seconds.

### No empirical pilot
**Symptom:** Cost plan claims $X but never ran a single live call.
**Root cause:** Felt costly to spend $0.17 on a 10-row pilot.
**Fix:** Always run the pilot. Even $0.17 grounded data is dramatically more persuasive to a budget approver than a $3K modeled estimate.

### Pricing the full list when most of it will be filtered
**Symptom:** Cost plan prices 45K rows even though Phase 0 cleanup drops 75% of them.
**Root cause:** Conflating "list size" with "enrichable rows."
**Fix:** Always show two columns: full-list and cleaned-list. Recommend spending on cleaned only. Defer full-list spend behind a "Phase 4, conditional approval" line.

---

## Doc quality

### Tables stuffed with long prose cells
**Symptom:** Rubric table has bin definitions occupying 150 characters per cell, forcing uneven row heights.
**Root cause:** Treating tables as the primary content holder.
**Fix:** Tables hold short cell content. Long rules, descriptions, explanations go in bullet lists below the table. Pad columns with spaces so the source view is also readable.

### Mixed analysis prose + code in one doc
**Symptom:** RECOMMENDATIONS.md has 200 lines of Python embedded between paragraphs.
**Root cause:** Pasted code into the doc instead of referencing a separate file.
**Fix:** Code lives in `.py` files. Docs reference them. Docs are for analysis prose, tables, and conclusions.

### Headline buried below context
**Symptom:** Boss has to read 3 pages to find "approve $X to do Y."
**Root cause:** Linear write-up from setup → analysis → recommendation.
**Fix:** TL;DR at the top with the one number that matters. Then context below for those who want to read further.

### Estimate presented as measured
**Symptom:** Cost doc says "the workflow will cost $X" without distinguishing modeled from empirically piloted.
**Root cause:** Sloppy phrasing.
**Fix:** Tag every cost line as `(modeled)`, `(per provider doc)`, or `(empirical, N=10 pilot 2026-MM-DD)`.
