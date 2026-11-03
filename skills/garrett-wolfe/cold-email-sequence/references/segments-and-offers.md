# Segments, Messaging Maps and Offer Switching

How to send different pains, proof and offers to different slices of the list without writing a
new campaign from scratch each time. Researched 2026-10-26.

## 1. The principle: one positioning, many pitches

April Dunford: most segments don't need separate positioning. The product's differentiated value
is usually the same, but the **pitch** changes (her IBM example: "keep the registers running" for
retailers, "keep the lights on" for utilities).

So per segment, **keep the core value and vary four things:**
1. **Pain language**, in that segment's own words.
2. **The lever** (make money, save time or money, reduce risk), if the segment feels a different one most.
3. **Proof**: same-segment first, then same problem shape.
4. **Offer**: the lowest-commitment thing that shows the value *to that segment*.

The template, CTA style and voice stay the same. Segments switch **slots**, not emails.

## 2. The messaging map (one row per segment)

Keep it as a table in the campaign spec (or the client graph), not in prompts. Every campaign and
AI slot reads from it.

```yaml
# messaging_map: one entry per segment. First matching rule wins (top to bottom).
- segment_id: s1-vsaas-new-vp
  rule: vertical_saas AND employees 20-200 AND new_vp_sales_days <= 90   # signal segments first
  persona: VP Sales
  trigger: new VP Sales in seat ≤ 90 days
  pain: "inherits a thin pipeline and a quota due in two quarters"      # their words
  cost_of_pain: "a missed first two quarters"
  best_alternative: "AEs prospecting their own lists"
  lever: make_money
  angle: first-90-days pipeline
  offer: { primary: 50-hand-scored-accounts, fallback: peer-case-study }
  proof: { primary: <cleared same-segment result>, fallback: <same problem shape> }
  cta: value_exchange          # "want the list?"
  subject_pattern: signal      # "new role"
  avoid: ["congrats on the new role" as the whole email; naming their predecessor]
  campaign_id: <instantly id>
  status: testing              # testing | champion | retired
  min_volume_ok: true          # can reach ~1,000-2,500 leads in the test window
- segment_id: default
  rule: ICP fit, no segment or signal
  pain: <the shared best-alternative pain>
  lever: <the core lever>
  offer: { primary: soft-resource, fallback: none }
  proof: { primary: <broadest cleared proof> }
  cta: soft_question
```

Columns worth keeping even in a spreadsheet: `segment_id | rule | est. monthly volume | trigger |
persona | pain (their words) | cost of pain | best alternative | lever | angle | offer (primary →
fallback) | proof | CTA | subject pattern | avoid | campaign_id | status | PRR | meetings/1k`.

Build the pain column from the persona's world (Jason Bay's messaging matrix: priorities, current
solution, problems, aspirations), sorted into the four pain kinds: financial, productivity,
process, risk. For multi-persona accounts, add a **buying-job** column (economic approver,
operational owner, technical evaluator, champion), each with what they need to validate and the
proof they need (Unify). If one person holds two jobs, send one combined message. Route replies at
the account level before emailing the next persona.

## 3. Routing leads (deterministic, in code)

1. **Compute `segment` with an ordered rule list, first match wins:** signal segments first (most
   specific, most perishable) → vertical × size → persona-only → `default`. Never let a model pick
   the segment.
2. **Look up the map** for that segment: offer, angle, proof, pain line, CTA, campaign_id.
3. **Fill slots inside the fixed template** with those values. AI writes at most one or two short
   lines (`ai-lines-and-spintax.md`).
4. **One segment = one campaign.** It keeps results attributable and stops variables leaking
   between segments.
5. **Offer waterfall within a segment:** if the lead has what the primary offer needs (say, the data
   for a custom audit), use it; otherwise the fallback offer (a sample list, a case study);
   otherwise the default soft CTA. The waterfall result is a variable (`{{offer_line}}`), never a
   blank.
6. **Preflight** every slot non-empty on every lead before push.

In Clay this is an IF / ELSE IF / ELSE formula column (`segment`) plus lookups. ELSE is the
default. In code, a list of `(predicate, segment_id)` tuples.

## 4. Picking an offer per segment

Score candidates with `offers.md`, then choose the one with:
1. the **lowest commitment** that still shows the core value;
2. a **direct tie to the segment's #1 pain or trigger**;
3. **proof from the same segment** (or the same problem shape);
4. the **lowest delivery cost** at the positive-reply volume you expect. A 2% PRR on 2,000 sends is 40
   audits.

Rules:
- **Lead with the segment where proof is deepest.** Single-segment pitches outperform broad ones
  (Smartlead claims 6.8% vs 4.7%; directional only). Save the other services for the call.
- **One case study, many angles.** Reframe one result per segment instead of hunting a new case
  study each time.
- **For retainer services, offer a smaller first step** (an audit, sprint, sample or free test)
  that leads into the engagement. Never a price.

## 5. How many segments

A segment earns its own copy only if it can reach **~1,000-2,500 contacted leads in the test
window**, the volume needed to see a 2x difference at 1-2% PRR (`testing.md` §1). Otherwise merge it
into its parent and vary only the pain or proof slot, or keep it as a tag inside a larger campaign.

**Practical cap: 3-6 live segments × 1-2 offers each, plus the default.**

## 6. The default campaign is your control

- Write it around the **shared best-alternative value**, the broadest cleared proof and a soft
  interest CTA. Never a segment-specific offer it can't back.
- Every segment is tested **against the default**. If a segment can't beat the default by ~1.5x on
  PRR after 2,000+ sends, merge it back: its custom copy isn't earning its maintenance.

## 7. Testing order for a map

1. **Segment × offer as separate campaigns vs the default.** The coarse test, where 2x+ effects
   are plausible.
2. Within winning segments: **angle or lever**, champion vs challenger.
3. Then **first line or CTA** as step-1 variants.
4. Subject, PS and length only once a segment sends 10k+ a month, or pooled across segments
   through tags.

## 8. Worked example (fictional outbound-services firm)

| Segment | Trigger | Persona | Pain | Lever | Offer → fallback | CTA |
|---|---|---|---|---|---|---|
| S1 Vertical SaaS 20-200 | new VP Sales ≤ 90 days | VP Sales | inherits thin pipeline, quota in 2 quarters | make money | 50 hand-scored ICP accounts → peer case study | "want the list?" |
| S2 B2B services 50-500 | hiring BDRs | Managing partner | partners still prospect themselves | save time | sample list of 25 targets → 2-min teardown video | "worth a look?" |
| S3 PE-backed portfolio co | new sponsor ≤ 12 months | CEO / CRO | 100-day plan needs pipeline | reduce risk | outbound audit readout → plan template | "want the readout?" |
| S4 AE, no SDR | AE hired, no SDR team | Head of Sales | AEs prospecting instead of closing | save time | AE-ready account list → checklist | interest CTA |
| D Default | none | any | inconsistent pipeline | core lever | "happy to send what's working in your space" | "worth a chat?" |
