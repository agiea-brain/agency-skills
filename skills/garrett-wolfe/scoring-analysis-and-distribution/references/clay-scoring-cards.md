# Clay scoring cards vs formula columns

Clay has two distinct column types for scoring. Use the right one.

### Scoring cards (band-based UI)

Used for: individual criterion scores (Headcount Score, FTE Score, etc.).

Clay's scoring card UI defines bands declaratively: no code. Each card has
one or more **Scoring Criteria**, and their scores sum within the card.

Each scoring criteria has:
- **Values to Score**: the input column
- **Comparison Type**: `Contains (Text)` or `Between (Number)`
- **Keywords**: comma-separated values/ranges to match
- **Scores**: comma-separated scores, one per keyword

**Between (Number) rules:**
- Every keyword must be a range, not a bare number. Use `0-0.9` not `0`.
- Open-ended upper bounds: `251-999999` not `251+`.
- Ranges are inclusive on both ends.

**Contains (Text) rules:**
- Keywords match if the cell value contains the keyword text (case-insensitive).
- First matching keyword wins. Order keywords from most-specific to least.
- Empty cells match no keyword and score 0 by default.
- **Exhaustive keyword lists required.** Any value not matching a keyword silently
  scores 0. This is especially dangerous for Country/Geography cards: if Germany
  isn't in the keyword list, all German firms score 0 with no error. Always validate
  coverage (% nonzero) after creating or editing a Contains (Text) card.

**Multi-criteria cards:**
A single scoring card can have multiple criteria (e.g., Domain Experience
has Criteria 1 on `Domain Expertise Classification` and Criteria 2 on
`Service Count`). The scores from all criteria in the same card **sum**.

**Documenting scoring cards in RECOMMENDATIONS.md:**
Use this format for each card so the operator can paste directly into Clay:

```
> **Scoring Criteria 1**
> Values to Score: `Column Name`
> Comparison Type: Between (Number)
> Keywords: `0-0.9, 1-5, 6-10, 11-999999`
> Scores: `0, 3, 6, 10`
```

### Formula columns (Clayscript)

Used for: DQ logic, Grand Total (sum of card scores), Display Score
(bell curve lookup), Tier labels, and any cross-column computation.

Clayscript is JavaScript. Column references use `{{Column Name}}` syntax.
Guard against null with `|| 0` for numbers, `|| ""` for strings.

**Critical: Clay strips `const`/`let`/`var` declarations and inlines the
expression.** This breaks operator precedence. Never write `const gt =
{{Col}} || 0; gt >= 50 ? ...`: Clay will render it as `{{Col}} || 0 >= 50`
which parses as `{{Col}} || (0 >= 50)` due to `>=` binding tighter than `||`.
Always wrap the null guard in parentheses: `({{Col}} || 0) >= 50 ? ...`

Scoring cards should NEVER be written as Clayscript formulas. Clayscript is
only for columns that need cross-column logic (sums, lookups, conditionals
across multiple scoring card outputs).
