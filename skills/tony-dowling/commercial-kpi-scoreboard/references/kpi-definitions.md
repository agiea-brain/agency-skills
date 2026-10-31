# The six KPIs

All six are computed for the resolved scope (one deal owner, or all owners) and period (today, this week, this month, this quarter; default current month), within the resolved pipeline.

| KPI | Definition | Source fields | Edge handling |
|---|---|---|---|
| Presentations Made | Count of deals that entered the "Presentation Made" or "Presentation Sent" stage inside the period | Stage-entry timestamp for that stage | Count every entry, whatever call it happened on. Re-entries of the same deal inside the period count once |
| Closing Ratio | Closed Won deals that had a presentation in the period ÷ Presentations Made in the period | Stage-entry timestamp, closed-won date | No presentations: "n/a". Show the fraction next to the percentage, for example "7 of 23" |
| Sales Velocity | Mean days from create date to close date for deals closed won in the period | Create date, close date | Deals missing either date are excluded and listed by name |
| Average Order Value | Mean amount of Closed Won deals in the period | Amount | Deals missing amount are excluded and listed by name |
| Current Billing | Sum of Closed Won amounts in the period | Amount | Same exclusion list as AOV |
| Position Against Target | Current Billing ÷ target, and target minus Current Billing as the cash gap | Target property in HubSpot, else the targets document | No target: "target not set" |

## What counts as a presentation

A presentation is any moment the business was asked for cash. It does not matter whether that was Call 1, Call 2 or Call 5. If pricing or a proposal was put on the table, it is a presentation. A meeting where no money was mentioned is not, whatever stage it sits in.

## Target source order

1. A target or quota property on the owner or a HubSpot goals report, if the account has one.
2. The client's targets document in the client brain: a maintained sheet with one row per rep per period, updated as targets are allocated.
3. Neither: show the other five KPIs and write "target not set" in the sixth row. Do not estimate.

Multiple rows for the same rep and period: use the most recent.

## Scoreboard layout

```
Scope: [rep name or Team] · Period: [period] · Pipeline: [pipeline name]

| KPI | Value | Context |
|---|---|---|
| Presentations Made | 23 | over the period |
| Closing Ratio | 31% | 7 of 23 presentations → Closed Won |
| Sales Velocity | 42 days | avg create → close |
| Average Order Value | £8,400 | across 7 won deals |
| Current Billing | £58,800 | Closed Won revenue |
| Position Against Target | 82% (£12,200 gap) | vs £71,000 target |
```

Then 2 to 3 lines: what stands out, the biggest move to make, any caveat (deals missing amount or date, stale or absent target).

## Reading the board

- High presentations, low closing ratio: the ask for cash is happening before the diagnosis has landed. Look at Call 1 quality.
- Low presentations, high closing ratio: the rep only asks when it is safe. Push for more presentations; the ratio will drop and billing will rise.
- Long velocity with a healthy ratio: deals are being nursed. Check for missing close dates propping the number up.
- Billing on target with a low presentation count: one large deal is carrying the month. Say so; next month has no cover.
