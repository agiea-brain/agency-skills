# Display Score, raw max and tiers

Phases 3a to 3c of the workflow.

### Phase 3a: Bell curve normalization (when raw stdev hits ceiling)

When the raw rubric's stdev plateaus below target due to structural data-coverage
limits (common when >30% of rubric weight sits on axes with <10% coverage), apply
bell curve normalization as a display layer on top of the raw scores.

This does NOT replace rubric iteration: it runs AFTER the rubric is as good as
the data allows. The raw Grand Total remains the source of truth for debugging.

**Process:**
1. Export non-DQ pool's Grand Total values
2. Compute percentile rank per row → inverse-normal CDF → scale to mean=50, std=20
3. Average Display Score per GT value to build a lookup table
4. Implement as a nested IF formula in Clay (see `references/distribution_techniques.md` §5a)
5. Sync Display Score (not raw GT) to HubSpot as the rep-facing "Fit Score"

**When to use:** Raw stdev is 10-18 on 0-100 scale (0.10-0.18 on 0-1) and further
rubric iteration yields diminishing returns (<+1 stdev per iteration). The bell
curve transform lifts effective stdev to ~20 and centers the distribution at 50.

**When NOT to use:** Raw stdev is already ≥20, or the client needs absolute scores
("hit 70% of the rubric criteria") rather than relative ranking. In those cases,
keep iterating the rubric.

**Recalibration trigger:** The GT → Display lookup must be recomputed whenever DQ
criteria, card bands, or card weights change. A structural rubric change invalidates
the mapping.

### Phase 3b: Raw Grand Total max is typically 85-95, not 100 (this is correct)

A well-designed rubric with mutually-exclusive bullseyes (Field Reps 60-89, FTE
400-799, Revenue $1B-$5B, etc.) produces a structural raw max of ~85-95 because
no real firm hits every card's bullseye simultaneously. **This is intentional, not a bug.**

For example: a 60-rep firm with $3B revenue would need ~50K FTE per rep
(impossible). A 400-FTE firm with $3B revenue has $7.5M/employee (unrealistic
for field-sales orgs). So the structural raw max for real firms is ~90.

**Do not "fix" this by loosening bullseyes**: that reduces discrimination and
collapses the top tier. The right answer is:
- Use the Display Score (Phase 3a bell curve) as the 0-100 rep-facing metric
- Tier on Display Score, not raw Grand Total
- Treat raw Grand Total as a debugging metric only

If a client insists on raw 0-100 with no bell curve, use one of:
- **A. Accept raw max ≈ 90** (most honest)
- **B. Rescale to observed max**: `Final % = (GT / observed_max) × 100`. Warn that
  this makes scoring population-dependent (one new high-scoring firm shifts everyone).
- **C. Use a "perfect-fit firm" denominator**: define an explicit max raw possible
  for the optimal firm (e.g. 92 in the Client A case) and divide by that. Honest but
  requires explaining the denominator to the operator.

Default to A + Display Score. B and C are escape hatches if the client refuses
bell curve normalization.

### Phase 3c: Tier scheme: 20 tiers at 5% intervals on Display Score

The recommended tiering for the rep-facing UX is **20 tiers at 5% intervals**
on the Display Score. This gives finer stack-rank granularity than the
A/B/C/D/Low scheme while still being scannable.

**Two valid scales for Display Score: pick one and match the Tier formula:**

| Scale | When to use | Display values | Tier formula (T1 = best, T20 = worst) |
|---|---|---|---|
| **0-1** (recommended) | Display Score column type = Number, matches Final Score Percentage convention | 0.000 to 1.000 | `"T" + (20 - Math.floor(Math.min(0.99, ({{Display Score}} \|\| 0)) / 0.05))` |
| 0-100 | Display Score column type = Number, want literal integer-ish values | 0 to 100 | `"T" + (20 - Math.floor(Math.min(99, ({{Display Score}} \|\| 0)) / 5))` |

**Both produce T1 (best) through T20 (worst)** with identical population distributions. Pick the scale based on what reads naturally in the client's existing column conventions.

**Tier direction convention:** T1 = top (best fit), T20 = bottom (worst fit). This matches how people naturally read rankings ("we have 200 T1 accounts to call this week"). If a client prefers T20 = best, swap `(20 - Math.floor(...))` for `(Math.floor(...) + 1)` in the Tier formula.

In `references/bell_curve.py`, set `DISPLAY_SCALE = 1` for 0-1 output or `DISPLAY_SCALE = 100` for 0-100. The lookup file generates both the Display Score formula AND the matching Tier formula automatically (defaulting to T1 = best).

**Letter tiers (alternative): 15-tier A+/A/A- ... F-/F+ scheme:**

```
Tier_Letter =
  (({{Display Score}} || 0) >= 95) ? "A+" :
  (({{Display Score}} || 0) >= 90) ? "A"  :
  (({{Display Score}} || 0) >= 85) ? "A-" :
  (({{Display Score}} || 0) >= 80) ? "B+" :
  (({{Display Score}} || 0) >= 75) ? "B"  :
  ... (continue through F-)
```

**Why 5% tiers over the old 5-tier scheme:**
- 5 tiers (A/B/C/D/Low) hide a lot of stack-rank signal: 50% of the pool ends up
  in "C" or "D" with no further differentiation
- 20 tiers map cleanly to the bell-curve Display Score; each tier's expected
  population is predictable (T20 ≈ 2.4%, T11 ≈ 9.2%, T1 ≈ 2.5%)
- Operator can filter "T17 and up" or sort descending: both work without further
  thresholding

**Old 5-tier scheme is still fine** for coarse summaries (boss memos, "we have
3.4% A-tier accounts"). Keep both columns: a 20-tier `Tier` for filtering,
a 5-tier `Tier_Coarse` for reporting.
