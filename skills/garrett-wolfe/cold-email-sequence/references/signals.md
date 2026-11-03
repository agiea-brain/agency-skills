# Signals: Writing Copy for Every Buying Signal

The catalog of buying signals we work with, and how to write for each: what it is, where it comes
from, how strong it is, the send window, whether to name it, the angle, an example line, and the
pitfalls. Researched 2026-10-26.

- **This file** owns signal copy.
- `triggers.md` owns real-world time triggers (sports, weather, the calendar) and the general
  freshness rules.
- `conferences.md` owns events.

**Evidence warning:** nearly every per-signal reply number is published by the vendor that sells
that signal (Unify, UserGems, RB2B, Valley, Trigify, ColdIQ). There's no independent, controlled
dataset. Compare claims against the real baseline: the Smartlead 2026 median sender gets 1 reply
per 135 contacts (0.74%). **Expect a real signal to lift replies 2-5x, not 10x.**

---

## 1. Four kinds of signal (and score ≠ signal)

| Axis | Question | Decays? | Examples |
|---|---|---|---|
| **Fit** | Should they ever buy? | No | industry, size, stack, growth, awards, lookalike of closed-won |
| **Intent** | Are they looking? First-party (high) or third-party (medium) | Fast (days) | website visits, PQL, content, own-post engagement · Bombora, G2, competitor engagement |
| **Timing / trigger** | Why now? | Weeks | new hire, promotion, exec change, funding, M&A, job post, deadline |
| **Access / relationship** | Do they know us? | Slowly | past champion, closed-lost, followers, mutual connections, event co-attendance |

**Fit and signal are separate fields, never summed.** Outreach needs
both. Priority = fit × signal strength × freshness.

## 2. The naming rules (the most important part of this file)

1. **Public, self-announced events may be named**: job change, promotion, funding, job post, talk,
   filing, award, launch. But naming must come with an **observation or implication**. "Congrats
   on the raise" alone is the most saturated opener in B2B.
2. **Tracked behavior is never stated**: website visits, pricing-page views, third-party intent,
   G2, likes, stars, competitor reviews. Write to the **problem it implies**, at the persona level,
   as a question. Company-level signals (reverse IP, Bombora, G2) must never be written as if *this
   person* did the thing. "Saw you on our pricing page" reads as surveillance, and is often wrong
   about who looked.
3. **First-party relationships are named; the relationship is the hook**: past champion,
   closed-lost, engagement with *our* posts, a webinar they attended, their own product usage.
4. **Every inference is a hypothesis**: "usually", "my guess is", "am I off?". Assertive claims
   about their business cut replies 26% (Lavender via UserGems).
5. **Never say where or how you found them** for tracked signals. If someone asks, have an honest
   one-line answer ready. For shared rosters, *do* say where the address came from
   (`conferences.md`).

House call on a known conflict: Kellen's Warm archetype opens with "saw {{companyName}} was on the
[product] site". Our rule is **never state the visit**.
Use the visit to time and aim, not as the subject. Our rule wins.

## 3. Archetypes (how the 4 moves adapt), after Kellen Casebeer

| Archetype | Signals | Move 1 (opener) | Insight pattern | CTA shape |
|---|---|---|---|---|
| **Transition** | new hire, promotion, exec change, champion move | name the move ("congrats on joining") | "the first window is when it's easiest to see what's working and what's messy" | "have a system you love, or open to changes as you settle in?" |
| **Event** | funding, M&A, launch, job posts, expansion, earnings | name the event plainly ("saw the deal") | "after a [event], the question shifts from [old] to [new]" | "already planned for, or still being worked out?" |
| **Competitive** | competitor engagement, tool evaluation, tech change, competitor reviews | the *topic*, never the competitor; one hedge at most | "[tool] covers X; the hard part is Y when Z" | "open to alternatives, or still mapping what you need?" |
| **Warm (first-party)** | own-post engagement, content, webinar, champion, closed-lost, PQL | name the relationship | continue the conversation | a reply, not a meeting |
| **Implied (tracked)** | website visits, third-party intent, G2 | **no mention**; open on the problem the page or topic implies | "teams at your stage usually hit X when they start comparing" | "is that what's going on, or am I off?" |
| **Search** | none | "trying to find the [team] that [has X figured out]" | | binary |

---

## 4. The catalog

S = strength (H/M/L). Window = when to send. Name = whether to state the signal.

### First-party intent

**Website visitor: company level** (reverse IP: HubSpot Breeze/Clearbit, Dealfront, Snitcher,
Koala, Warmly, Vector, Common Room)
- S: M; **H on pricing, demo, comparison, integration, security or docs pages, or a repeat visit
  within 7 days.** Homepage visits barely count (docs and pricing page visits are the ones
  that matter).
- Window: same day to 48h. Decay weights: 100% (0-7 days) / 50% (8-14) / 25% (15-30) / drop after
  30.
- Name: **never.** You don't know who looked.
- Angle: the problem the page implies (pricing → ROI or time-to-value; integrations → stack fit),
  aimed at the persona who owns it.
- Example: "teams at {{companyName}}'s stage usually hit [pain] right around when they start
  comparing options. worth a two-line note on how others handled it?"
- Pitfalls: company ID accuracy is low across vendors, and claimed match rates range 15-60%. VPN,
  mobile and home IPs give false hits. Exclude customers, competitors, and careers-page visitors
  (job seekers).
- **Route to a human same day**; automating it into a drip wastes it.

**Website visitor: person level** (RB2B, Warmly, Vector, Knock2)
- S: H if the match is right.
- Window: within hours; skip after 14 days.
- Name: never (house rule). RB2B's own team names pages and claims 30% positive replies
  (self-reported); Knock2, Unify and ColdIQ say never.
- Angle: as above, plus the persona's job.
- Example: "{{firstName}}, most [role]s I talk to look at [category] when [trigger pain]. is that
  what's going on at {{companyName}}, or am I off?"
- Pitfalls: US-only, needs LinkedIn coverage (weak in trades, healthcare, manufacturing). In the
  EU, person-level ID without consent is high-risk under GDPR plus ePrivacy, so get counsel or
  don't. Suppress EU person-level matches by default.

**Content download / gated asset** (HubSpot, Marketo forms)
- S: M (often research or students).
- Window: within 48h.
- Name: yes; they gave their email knowingly.
- Angle: the asset's topic → the next logical question.
- Example: "you grabbed the [asset]. the part most people get stuck on is [X]. want the two-minute
  version of how [peer] handled it?"
- Pitfalls: a download isn't an MQL. Gate on fit. Students and vendors.

**Webinar registration / attendance** (Zoom, Goldcast, ON24, Luma)
- S: M (registered) / M-H (attended) / H (asked a question).
- Window: 0-24h, then 2-4 touches over 5-7 days.
- Name: yes.
- Angle: attendees → the next step, or their question answered; no-shows → the replay plus a
  3-line recap. Never scold a no-show.
- Example (asked a question): "you asked about [X] in the session. the short answer is [Y]; the
  longer one depends on [Z]. worth 15 minutes to walk through yours?"

**Engagement with our posts / new followers** (Teamfluence, Trigify, Common Room, PhantomBuster)
- S: M-H; they already know us.
- Window: 48-72h.
- Name: yes. It's public and with us.
- Angle: continue the conversation; **no pitch in message 1**.
- Example: "thanks for jumping on the [topic] post. curious what you're seeing at {{companyName}}:
  [question]?"
- Pitfalls: peers, vendors and job seekers inflate the list. Comments ≫ likes. LinkedIn first, then
  email.

**Product signup / PQL** (product events via Segment, Pocus, Unify)
- S: H.
- Window: 1-4h after the action (limit hit, invites sent, setup done).
- Name: yes, it's their own usage. Avoid creepy granularity ("you clicked X 7 times").
- Angle: help with the specific action.
- Example subject: "hit the [feature] limit?"
- Pitfalls: Gmail signups, students, competitors. Gate on fit + usage + role.

**Community / GitHub / Slack activity** (Common Room, Reo.dev)
- S: H in our own community or repo; M in a competitor's.
- Window: days.
- Name: our community yes; a star → imply only.
- Angle: help with the problem they starred or asked about.
- Pitfalls: hobbyists; GitHub handle → work email matching is error-prone.

### Relationship

**Past champion / user changes job** (UserGems, Champify, Common Room, Deepline champion tracking)
- S: **highest of the cold signals** (vendors: 3x conversion; one case reports 40-50% response).
- Window: touch 1 fast with no ask; pitch at weeks 2-4; ~10 touches over ~45 days at a slower pace.
- Name: yes; the history is the point.
- Angle: shared history → bridge.
- Example: "congrats on the move to {{companyName}}. at [OldCo] you [result]. curious if [NewCo]
  has the same [problem], or if it's a different animal."
- Pitfalls: verify the employer (a mismatch is "a lead, not proof"). Route customers and open deals
  to their owners; manager review for churned or negative history. **Also email the replacement at
  the old account within ~5 days.**

**Closed-lost / old opportunity** (CRM + a new signal)
- S: H (vendors claim 10-15% reply).
- Window: **when the loss reason changes** (new budget, new leader, M&A, tech shift), not on a
  timer. 4-5 touches over 2-3 weeks.
- Name: yes, both the old conversation and what changed.
- Angle: touch 1 = old conversation + the change; 2 = proof; 3 = a resource on the objection;
  4 = a 15-minute ask.
- Example: "we spoke last [quarter] about [use case] and timing was [objection]. with [new
  signal], figured it might look different now."
- Pitfalls: no "checking in", don't re-litigate the loss, check the original owner.

**Event co-attendance:** see `conferences.md`. A registration is a fact; a LinkedIn post about
going is an inference.

### Transition (people)

**New hire in the target persona** (UserGems, Champify, Sales Nav alerts, Coresignal, PDL,
LeadMagic, Deepline job-change enrichment)
- S: H for timing; a mandate and a 90-day clock.
- Window: **days 14-90** (sources disagree: LeadMagic says first touch days 14-21, never day 1;
  ColdIQ says peak 14-45; Apollo says evaluation at 31-60).
- Name: yes, briefly, but "congrats" can't be the whole opener.
- Angle: what people in this seat inherit in the first 90 days, as a hypothesis.
- Example: "congrats on joining {{companyName}}. people stepping into [role] at a [stage] company
  usually inherit [pain] in the first quarter. have a system you love, or open to changes as you
  settle in?"
- Pitfalls: stale profiles (verify the role is current); 28% of "new roles" are internal moves (say
  "started", never "hired"). Keep it under 50 words, 0-1 questions. Dual track: also email their
  boss or the CEO about the same mandate.

**Promotion**
- S: M-H; new scope, but they inherit the existing stack.
- Window: 2-6 weeks.
- Name: yes, briefly.
- Angle: the **new scope**: the function or team that now sits under them.
- Example: "congrats on the promotion. now that [function] sits with you, [pain] becomes your call
  rather than someone else's."
- Pitfalls: inflated LinkedIn title bumps. Little published evidence.

**Leadership change (new CEO, CRO, CFO, VP)**
- S: H.
- Window: days 14-60 (a new VP moves within ~30 days; 90+ may be too late).
- Name: yes.
- Angle: the new exec's likely first-quarter mandate; **also email the team under them**, who face
  it.
- Example: "new [CRO]s usually re-baseline [metric] in quarter one. if [X] is on the list, happy to
  share what we've seen work."
- Pitfalls: execs get flooded; this is where real research earns its keep (POV framework,
  `frameworks.md` #14).

**Work anniversary** (lifecycle)
- S: L-M.
- Window: the anniversary week.
- Name: yes, with a business angle ("2 years running [function], what's changed since you took it
  over?").
- Never birthdays.

### Company events

**Job postings** (PredictLeads, TheirStack, Coresignal, LinkUp, Sumble, Apify scrapers)
- S: M (a RevOps or ops req for a problem we solve is the strongest variant).
- Window: weeks 1-2 → the hiring manager or CEO ("the gap before the hire lands"); weeks 3-8 → find
  who was hired and target them on days 1-30. Verify the post is still live.
- Name: yes, **by its content**, not "I see you're hiring". Quote one requirement and tie it to an
  operational problem. Say you saw it, don't quote their headline back, and
  never say where you saw it.
- Example subject: "{{RANDOM|the [role] req|[role] question}}". Line: "the [role] req mentions owning
  [X] from day one. most teams fill that seat and still [gap] for six months. how are you covering
  it in the meantime?"
- Pitfalls: evergreen and repost roles, agency postings. **Rank on distinct titles, not posting
  count** (one company: 146 postings, 2 distinct titles). A post doesn't prove budget.

**Hiring surge / headcount growth** (Coresignal, PredictLeads, Sumble, Harmonic, Sales Nav)
- S: M; a good fit or timing filter.
- Window: weeks.
- Name: yes, in aggregate ("you've roughly doubled the AE team").
- Angle: what breaks at scale.
- Gate: 2+ related roles in 30 days, or role starts ≥2 in a department of ≥4.
- Pitfalls: LinkedIn headcount lags.

**Fundraise** (Crunchbase, Harmonic, PitchBook, Dealroom, SEC Form D, Fundable)
- S: **M-L alone.** Consistently the lowest-replying signal in vendor data (Unify 3-6%).
- Window: week 1 is noise (the inbox floods); **weeks 2-8 are the window**; drop the reference after
  ~3 months. Indexes lag 3-4 months, so check the date.
- Name: weeks 0-2 only with a sharp observation; weeks 4-8, name **what the money is for**, not the
  round.
- Angle: the execution plan the round funds (hiring, a new market), not "you have budget".
- Example: "the plan after the series b looks like [new market / hiring 6 AEs]. the part that
  usually lags is [X]. is that on your radar yet?"
- Pitfalls: never infer a project from round size; never the valuation or investors. **Stack it**
  with a matching job post (funding in 90 days + a related post in 60 days).

**M&A / acquisition** (Crunchbase, PitchBook, news APIs)
- S: M-H; tool consolidation is coming.
- Window: after close, months 1-2; integration is the real window (14-120 days).
- Name: yes, neutrally ("saw the deal"), never "congrats".
- Angle: acquirer → standardizing tools across the combined company; target → meeting the parent's
  requirements. Lead with empathy for full plates; offer a resource and defer the pitch.
- Example: "guessing the next two quarters are mostly integration. when [tool area] comes up, happy
  to share the checklist we see teams use."
- Pitfalls: don't pitch before close; job insecurity is real (tone).

**Product launch** (news, Product Hunt, changelog)
- S: L-M; stack it.
- Window: 1-3 weeks.
- Name: yes, specifically ("saw [product] went live last week"), never "congrats on the launch!".
- Angle: the GTM work after launch (pipeline, adoption, field readiness).

**New office / geographic expansion** (PredictLeads news, TheirStack geo jobs)
- S: M.
- Window: 0-8 weeks.
- Name: yes.
- Angle: building [X] from zero in the new market (hiring, compliance, local pipeline).
- Pitfalls: "expansion" is sometimes one remote hire.

**Earnings / 10-K / annual report** (EDGAR, Quartr, AlphaSense)
- S: M for enterprise.
- Window: 1-3 weeks after.
- Name: yes, and cite it.
- Angle: quote the stated initiative (Item 1A risk factors, MD&A, the call) → where it lands on
  this persona's desk.
- Example: "[CEO] called out [initiative] as the 2026 priority on the Q2 call. that usually lands on
  [persona]'s desk as [pain]."
- Pitfalls: public companies only; never misquote.

**Partnerships / integrations announced:** S L-M, window 0-6 weeks, name it. Angle: what the
partnership requires operationally, or that we integrate with the same partner. Weak alone.

**Awards / rankings** (Inc 5000, Deloitte Fast 500, G2 badges): S L as intent (it's a fit signal of
growth). Window 0-4 weeks. A brief, verifiable nod, then "[X]% growth usually means [process] is
about to break". Every Inc 5000 company gets hundreds of these emails, so stack it.

**Layoffs / restructuring** (WARN notices, layoffs.fyi, headcount drops)
- S: M, and **only** for cost-down, efficiency or retention offers.
- Window: wait 2-4 weeks.
- Name: **never.**
- Angle: covering the same ground with a leaner team ("a lot of [function] teams are being asked to
  cover more this year. here's how [peer] kept [metric] flat").
- Pitfalls: never email the people laid off; no gloating, no "do more with less"; never pitch
  headcount-based seats; low touch count.

**Regulatory / compliance deadline** (regulator calendars, GovFiles): S M-H for in-scope firms.
Window 3-9 months before. Name it (public). Angle: one specific friction point. Verify they're in
scope, don't fearmonger with fines, and get the dates right.

**Prospect's website or pricing change** (Visualping, Firecrawl change tracking): S L-M, window
1-3 weeks, name it ("noticed you added an enterprise tier"). Angle: the new motion it implies.
Ignore cosmetic changes.

**Press / newsletter / exec quote:** S L, window 1-2 weeks, name and cite it briefly and verifiably.
"Saw your article" with no specifics reads as automated.

**Permits / project announcements** (local permit portals, project databases): S M-H for
construction-adjacent sellers, window 0-21 days. See `triggers.md`.

### Competitive and third-party

**Competitor LinkedIn post engagement** (Trigify, Valley, Common Room, PhantomBuster, Apify, Clay
post audience, Teamfluence)
- S: M; **a comment ≫ a like**; repeat engagement > one-off.
- Window: within 48h.
- Name: the **topic**, never the competitor ("I saw you follow [competitor]" spends the goodwill).
  "saw your take on [topic]" only for comments.
- Example: "saw your comment on [topic]. we've found [specific, slightly contrarian point]. how are
  you handling it at {{companyName}}?"
- Pitfalls: engagers include competitor employees, vendors, job seekers and the poster's friends,
  so filter to ICP. Scraping and automation risk LinkedIn bans. Vendor claims of 25-54% replies are
  unverified.

**Third-party intent** (Bombora topic surges, G2 Buyer Intent, TrustRadius, 6sense, Demandbase)
- S: M (category research, not interest in us). G2 compare and alternatives pages are the strongest.
- Window: the week of the surge (data already lags a week).
- Name: **never** (G2: a contact on the list "does not mean a specific contact generated" it).
- Angle: the category and the buyer's evaluation criteria.
- Example: "teams comparing [category] tools usually get stuck on [criterion]. worth one paragraph
  on how we'd answer it?"
- Pitfalls: accuracy claims range from ~15% to ~81%. Always overlay fit. **Backtest before buying:**
  if more than 60% of the last 50 closed-won deals showed prior intent, it's real; under 40% is
  noise. $20-100K+ a year.

**Tech install / removal / competitor renewal** (BuiltWith, Wappalyzer, HG Insights, Sumble,
TheirStack via job descriptions)
- S: M; a removal or replacement is H.
- Window: install or removal 1-2 weeks; renewal ~90+ days before the estimated date (adoption date
  + a 12/24-month term).
- Name: the public tool, yes ("you're on [tool]"); never claim to know their contract date.
- Angle: install → the adjacent problem it creates; competitor user → the known gap. Never trash
  the competitor.
- Example: "most [tool] teams we talk to love [strength] but end up exporting to sheets for [gap].
  same at {{companyName}}?"
- Pitfalls: client-side tech only; a detection date isn't a purchase date; **never infer an absence.**

**Negative reviews of a competitor** (G2, Capterra, Reddit)
- S: H if the reviewer is identifiable and ICP.
- Window: days.
- Name: **no**; lead with the pain they described.
- Example: "teams on [competitor] keep telling us [gap] is what breaks at [scale]. true for you?"
- Pitfalls: most reviewers are anonymous; terms of service; it can feel predatory.

**Social posts expressing pain** (Trigify, Common Room, Octolens, Syften, F5Bot)
- S: H for a first-person complaint.
- Window: 24-72h.
- Name: the public post's topic, yes; how you tracked it, no.
- Angle: reply to the idea with one useful point. Don't assume a buying motive.

**Podcast appearance** (Podscan, Listen Notes): S L as intent, high personalization value. Window
1-4 weeks after release. Quote one specific idea they said → the problem it implies. Never fake
having listened.

### Fit-only (good for lists, not reasons)
Lookalikes of recent closed-won · accounts a competitor just won (wait 6-12 months) · Glassdoor or
Indeed reviews naming process pain · tech-stack fit · growth rankings · mutual connections and warm
paths (these earn line 1 only if real). **Customer expansion and customers on the pricing page →
route to the account owner, never outbound.**

---

## 5. Stacking, routing and priority

- **Composite priority = fit × signal × freshness.** Score a surge against the account's own
  baseline, not raw volume. Run 5-7 signal types at most.
- **Stacks that work:** new VP + pricing-page visit · past champion + intent · funding + a related
  job post or sales hiring surge · website visit + a growing buying committee · job post + a new
  leader in that function.
- 1 signal = normal priority; 2 = high; 3+ = same-day human outreach (ColdIQ heuristic; its reply
  claims look inflated).
- **One account gets one message combining its signals**, not one sequence per trigger.
  Idempotency is per signal, not per company: the same signal never fires twice, and the
  highest-intent unacted signal goes first.
- **Routing:** high fit + high intent → a human today. Mixed → automated sequence. Low fit → monitor.
- **Suppress always:** customers, open opportunities, competitors, job seekers, non-ICP, EU
  person-level visitor matches, anyone who replied anywhere, the do-not-contact list.

## 6. Who gets the email (signal holder ≠ buyer)

The person who generated the signal isn't always the buyer :
- A recruiter posts the job → email the **hiring leader**, and never mention the post or who wrote it.
- A new IC joins → email their **boss** about the mandate, and optionally the new person separately.
- An exec changes → email the **exec and the team under them**.
- Competitor engagement by a junior → email the **function lead** about the topic, not the
  engagement.

Write one version per who-slot (founder / function lead / IC) in the messaging map
(`segments-and-offers.md`).

## 7. Channel and pace per signal

| Signal | First channel | Pace |
|---|---|---|
| Pricing or demo visitor (person level) | email within 1h, or a call if you have the number | 4 steps over 7 days, permission CTA |
| PQL | in-app or email within 2h | 4 steps over 5 days |
| Champion move | personal email, no ask → LinkedIn day 3 → value email day 7 | ~10 touches over 45 days |
| New hire / new exec | LinkedIn connect first, email ~day 14 | plus a parallel track to their boss |
| Post engagement (ours or a competitor's) | LinkedIn within 48h, then email | comments before likes |
| Third-party intent | email + multithread 2-4 personas | prioritize, don't fire instantly |
| Events | `conferences.md` | anchored to the event dates |
| Closed-lost | email from the original rep | 4-5 touches over 2-3 weeks |
| Funding / M&A / layoffs | email, low touch count, empathetic | resource first, pitch later |

## 8. Vendor claims

**Vendor reply claims, for calibration only** (all self-interested): champion move 12-20% (Unify)
to 40-50% (one case); closed-lost 10-15%; new hire 8-12%; G2 intent 4-8%; tech change 6-10%;
funding 3-6%; post engagement 13-28%; website visit 5-10% (Unify) to 30% positive (RB2B's own).
The consistent ordering is the useful part: **relationship and first-party > new hire > third-party
intent, tech, funding.**

## 9. Tags
Every signal campaign declares `trigger_type` (vocabulary in `testing.md` §5) and records
`trigger_age_days` at enrollment, so your reporting can tell you which signals and windows actually
work for your buyers. The windows above are starting values, not truths.
