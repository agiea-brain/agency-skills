# The Commercial Telemetry Workbook

One Google Sheets file in the connected document store, five tabs. Built in this order during /setup-telemetry, one tab per exchange, each confirmed before the next.

## 1. Targets_and_Quotas

| Rep | M0 quota | M+1 quota | M+2 quota | Source | Updated |
|---|---|---|---|---|---|

Ask for rep names first, then each rep's monthly quota across the three months. Lay the grid out and read it back. Recap: "Five reps, £200k a month in total, flat across the horizon."

## 2. Booked_Revenue (contracted cash)

| Rep | M0 booked | M+1 booked | M+2 booked | Source export | Updated |
|---|---|---|---|---|---|

Only revenue that is contracted and invoiced or scheduled for invoice, for delivery in that month, taken from finance or invoice exports. Not a verbal yes, not a stage called "Closed Won" with no contract, not a renewal assumed.

Introduce the benchmark here: M0 should be at least 80% booked, M+1 at least 55%, M+2 at least 35%. Below the line is the gap the pipeline must cover.

## 3. Active_Pipeline (Stage 2+)

| Rep | Deal | Amount | Close month | Presentation date | Pricing on table (Y/N) | Stage | Updated |
|---|---|---|---|---|---|---|---|

Filter HubSpot (or the pipeline document) to deals closing inside the window where a presentation has been held and pricing is on the table. Anything speculative, early, or without a pricing date is removed from this tab, however the CRM labels it.

## 4. Client_Portfolio_50 (rent the list)

| Rep | Account | Tier (A/B/C/Flag) | Last meaningful touch | Days since | Eviction due (Y/N) |
|---|---|---|---|---|---|

Each rep holds up to 50 accounts: 8 A, 15 B, 27 C, plus up to 15 developmental flags. A meaningful touch is a meeting booked or a brief taken. An account untouched for 30 days is due for eviction to the house pool.

## 5. Weekly_Commitments

| Week | Rep | Call 1s committed | Presentations committed | Cash asks committed | Call 1s held | Presentations made | Cash asks made | Friday note |
|---|---|---|---|---|---|---|---|---|

Monday 08:30: each rep enters voluntary commitments. Friday 15:30: actuals go beside them and the reality review runs off the gap.

## Staleness

Any tab with an Updated date older than 7 days is stale. A coverage check on stale data is reported as such, and the refresh is requested before the numbers are trusted.
