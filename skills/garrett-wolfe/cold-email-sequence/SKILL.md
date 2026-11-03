---
name: cold-email-sequence
title: Cold email sequence that gets positive replies
description: |
  Use this skill when an agency is writing, rewriting or reviewing cold email for
  a client: a full sequence, a subject line, first line, P.S., CTA, offer,
  follow-up step, spintax, a signal or trigger campaign, conference outreach, a
  segment and offer map, or an A/B test. Walks the decisions in order (value
  lever, list and signal, offer, subject, first line, body framework, CTA,
  follow-ups), lints the copy and sizes or reads tests. Also use for "build a
  sequence", "why isn't this campaign getting replies", "did variant B win".
category: Sales
tags: [cold-email, outbound, copywriting, signals, ab-testing, sequences]
tools: [instantly]
---

# Cold Email Sequence

How we write cold email, every time. This skill owns **the copy craft**: what to say, in what
order, and how to check it. The campaign shape, naming and API push belong to
your sending setup, and the voice belongs to the client.

**Read before writing:**
- `references/playbook.md` is the full canonical doc: every rule with its source, the
  disagreements between experts and the call we made on each, and the benchmarks.
- `references/frameworks.md` holds body templates per situation (signal, no signal, creative
  ideas, lookalike, new leader, referral) and the follow-up templates.
- `references/offers.md` covers picking an offer or lead magnet and scoring it.
- `references/ai-lines-and-spintax.md` covers AI-written slots, blank-variable safety and
  Instantly spintax.
- `references/ps-and-first-lines.md`: first-line types, the bridge test, AI first-line prompting,
  P.S. types and rules .
- `references/signals.md`: **every buying signal** (website visitors, new hires, promotions, exec
  changes, job posts, hiring surges, funding, M&A, launches, competitor post engagement, our-post
  engagement, content downloads, webinars, champion moves, closed-lost, PQL, third-party intent,
  tech changes, reviews, layoffs, earnings and more): strength, window, whether to name it, angle,
  example line, pitfalls, stacking and who gets the email.
- `references/conferences.md`: pre / during / post conference outreach, roster gates, event-anchored
  copy and templates.
- `references/triggers.md`: time-based triggers (company events, sports, weather, the B2B calendar)
  with recency windows, data sources and the never-send list.
- `references/segments-and-offers.md`: the messaging map (segment → pain, lever, offer, proof, CTA),
  deterministic routing, and offer waterfalls.
- `references/testing.md`: test order, sample sizes, design, tags, the test log and the decision
  rubric. `references/ab_test.py` does the math.
- `references/voices-and-styles.md`: more practitioners (Crawford PQS/PVP, 30MPC, McKenna, Coleman,
  Abraham), the best 2025-26 episodes, and a verdict on each trending style.
- `references/evidence.md` has the benchmark numbers.

**Precedence:** the client's brief and voice guide > this skill > the experts. If a client rule
contradicts a default here, the client wins. Say so in the spec.

---

## The one idea

A positive reply needs three things to be true at once: **the right person**, a **reason now**,
and **an outcome they want, easy to say yes to**. Copy amplifies a good list and offer; it can't
rescue a bad one. Experts agree on the priority order for effort and testing:
**list > offer > subject > opener > CTA > timing > length**.

## The value lever (mandatory)

Every email names exactly one lever, in the prospect's nouns:

| Lever | The prospect hears | Sounds like |
|---|---|---|
| **Make money** | more revenue, pipeline, deals, customers | "every pool contractor in Texas with the owner's cell" |
| **Save time or money** | fewer hours, people, tools, dollars | "without adding a second SDR" |
| **Reduce risk** | fewer misses, mistakes, fines, churn, surprises | "before the audit, not after" |

- Pick E1's lever from the pain the **best current customer** had before buying. If the
  pain is unclear, that's the gap to fix, not something to paper over in copy.
- **Rotate levers across the sequence.** If E1 was "save time" and got no reply, that lever
  didn't land, so E3 tries "make money" or "reduce risk".
- State it as a **problem or a concrete outcome, not an ROI promise**. Gong found ROI claims in
  cold email cut success 15%. "know what each float costs before you price it" beats "boost
  margins 23%". Numbers belong in proof (what happened for someone), not in promises.

---

## The workflow

Run these in order. Steps 1-4 are decisions. Write them at the top of the campaign spec before any
copy exists. If a step can't be answered, stop and get the input; don't write around it.

### 1. Gather inputs (no copy yet)

From the client's graph or docs: what they sell (one sentence a buyer would recognise), the
persona and their day, the **#1 pain the best customer had before buying**, cleared proof points
(names and numbers you may use), what they **don't** do, banned claims, and the voice node.
Research the client's site: every case-study customer, their industry, size, metric and problem.
Challenge the ICP if the case studies show a broader buyer.

### 2. List and signal: why you, why now

- Name the **cohort** and the **trigger**. Tighter beats bigger: campaigns under ~200 contacts
  reply at roughly 2x the rate of 500-1,000 (Saleshandy 2026).
- **Relevance beats personalization** (Becc Holland). A line true of the whole cohort ("you run a
  title agency with no in-house marketing") beats a fake-personal token. Reply.io found generic
  personalized variables *cut* interested replies 26%.
- Signal strength, strongest first: a stuck mandate they told the world about (job post, public
  ask) > a dated event (new role under 90 days, raise, launch, expansion) > a structural fact (team
  shape, stack, geo) > none (go Billboard or Search, see step 5).
- Only cite signals you can **verify**. Never invert a tech-stack absence ("no enrichment tool
  detected" is wrong too often). Job titles and job posts are safe to invert.
- **Write to the signal with `references/signals.md`.** The naming rule decides the opener:
  public, self-announced events (job change, funding, job post, talk) may be named, with an
  observation attached. Tracked behavior (site visits, intent, G2, likes) is **never** stated; write
  to the problem it implies. First-party relationships (past champion, closed-lost, our webinar)
  are named, because the relationship is the hook. Events and conferences: `references/conferences.md`.
- **Time-based triggers** (company events, sports, weather, fiscal year, calendar) each have a send
  window and a never-send list. A freshness gate in code re-checks in-flight leads, and a stale or
  empty trigger drops the line, never the email (`references/triggers.md`).
- **More than one segment? Build the messaging map first** (`references/segments-and-offers.md`).
  Each segment keeps the core value but switches pain language, lever, proof and offer. Code assigns
  the segment (first matching rule wins, ending in `default`), and one segment = one campaign.
  3-6 live segments at most, each able to reach ~1,000-2,500 leads in a test window.

### 3. Offer: what they get for replying

Lead with what the prospect gets. A meeting is an ask, not an offer. Run `references/offers.md`:
generate 5-10 candidates, score each on four criteria (1-5 each: cheap to deliver, valuable enough
to pay for, shows competence, unique vs competitors), and **keep only those scoring 15/20 or
more**. Never gate it behind a form. The most you ask of them is a one-line reply.

### 4. Subject line

- **2-4 words**, specific, reads like an internal email. Sentence or lowercase per client voice.
  Belkins measured 2-4 words best.
- Pick one of three types: a **signal or name** ("title agency marketing", "the vp sales req"), the
  **whole offer** (the subject plus preview text self-select the reader), or a **problem
  indicator** ("looked you up on chatgpt").
- Test: could a colleague or customer have sent this? Never "quick question", "curious",
  "following up", "partnership opportunity", fake "re:", or clickbait.
- Threaded follow-ups (E2, E4) have a **blank** subject.

### 5. Email 1

Pick a framework from `references/frameworks.md` by situation:

| Situation | Framework |
|---|---|
| Real signal, want a conversation | **Signal 4-move** (Kellen): signal → three pains → insight → binary CTA |
| Real signal, clear offer | **Observation → lever → proof → soft CTA** |
| No signal, homogeneous niche list | **Billboard**: the whole offer up top; the reader self-selects |
| No signal, unknown pain | **Search**: "trying to find the [team] that [has X figured out]" |
| Broad list, varied businesses | **Creative ideas**: 3 slot-defined bullets from their site |
| Have a lookalike customer | **Lookalike**: "[similar company] had [problem]; [what changed]" |
| New in seat (< 90 days) | **New leader**: the window insight plus a state CTA |
| Unsure who owns it | **Referral** (Ross): find the right person |
| We hold data they can't easily get | **PVP** (Crawford): the finding *is* email 1 |
| Persona relevance, no signal | **4-sentence** (30MPC): reason → problem → solution → interest CTA |
| Exec / tier-1, strong signal | **POV** (Coleman): interpret what the signal means for them |

Rules for every E1:
- **First line is about them**, specific and observable, and puts the strongest phrase where the
  preview shows it. It must bridge: if deleting line 1 doesn't change line 2, it's decoration.
  Execs get company relevance; ICs can get personal (`references/ps-and-first-lines.md`). No "hope this finds you", "I wanted to reach out", "I came across", "my name
  is", or prefacing ("quick one", "I'll keep this short").
- **One email, one job, one lever, one CTA.** Aim for 50-90 words; 125 only when an AI slot earns
  it. Keep the reading grade at 7 or under, and keep sentences about them at 3:1 to sentences
  about you. It should read aloud in under 20 seconds.
- **Exactly one question, and it's the CTA**, answerable in five words or fewer. Default to
  the interest or state form: "worth a look?", "is that on your radar?", "already solved, or still
  manual?". **Never a calendar ask in E1.** Gong: specific-time asks book 15% cold vs 37% in
  active deals.
- **Proof** only if it matches the prospect's problem shape: one named customer and one number,
  stated as what happened, never a logo list. Otherwise hold it for E3.
- No links in E1, no images, no tracking, no attachments, no exclamation marks, no em dashes.

### 5b. P.S. (optional, E1)

One P.S., one sentence, ≤20 words, new information only, never a second pitch or a repeat of the
CTA. Its job is the human detail (fact + casual reaction) that would clutter a relevance-led body,
or a soft offer when the body has no question. The fact must be public and explainable. Abstain to
no P.S. rather than a filler one. Types and prompts: `references/ps-and-first-lines.md`.

### 6. The sequence (default 4 emails, 2 threads)

| Step | Thread | Job | Words | Lever |
|---|---|---|---|---|
| E1 | A, new subject | best signal, clearest offer | 50-90 | lever 1 |
| E2 | A, blank subject | one new fact or angle; reads like a reply | 25-50 | lever 1 or 2 |
| E3 | B, new subject | new angle; proof or a lower-commitment offer (audit, list, video) | 40-80 | a different lever |
| E4 | B, blank subject | exit: a redirect ("who owns X?") or a useful resource; no guilt | 20-40 | none |

- **Each email stands alone.** Never reference the last one ("following up", "bumping",
  "circling back", "did you see", "one more thought", "last note from me"). Gong: "I never heard
  back" raises replies but cuts meetings 14%; "Thoughts?" cuts meetings 20%.
- Follow-ups matter: 42-57% of replies (and 57% of positive replies) come after E1. But each step
  past the 4th roughly triples spam complaints. **Four steps is the default; never more than five.**
- Timing, delays and threading use delays of 2/2/3/2 days, and step 1's
  delay is never 0 (in Instantly, a step's delay is the wait after it).

### 7. AI lines and variables

AI fills **slots**, never whole emails. Keep the template, pitch and CTA human-written. Each slot
gets a fixed frame in the copy, a word cap and an abstain rule (empty string). Hand-write the
first three examples before any model runs, and review a batch of 10, never single rows. Then
preflight: every variable must be non-empty on every enrolled lead, including in-flight leads.
Instantly sends a blank variable silently, and spintax can't hide a blank. Full method:
`references/ai-lines-and-spintax.md`.

### 8. Spintax (Instantly)

`{{RANDOM|a|b}}`, never Smartlead's `{a|b}`. Use 3-5 blocks per cold open, 2-3 options each, on
the greeting, connectors, a mid-body verb and the CTA. Never spin variables, numbers, names,
proof, prices or technical terms. **Every combination must read as a grammatical sentence**, so
spin whole clauses rather than fragments that collide.

### 9. Check, then ship

1. `python3 references/lint_copy.py <spec.json|draft.txt>` must report 0 errors. It checks length,
   question count, subject words, banned phrases, spam words, links, dashes, spintax syntax and
   collisions across every rendered combination, reading grade, you:I ratio, variables used and
   step-1 delay.
2. Score it on the rubric in `references/playbook.md` §9. Ship at 85 or above; 70-84 needs one
   more pass; below 70, start over at step 2 or 3, not at the wording.
3. Edit every variant for AI writing patterns. Re-lint afterwards.
4. Render five real leads end to end and read them aloud. Ask: would I reply to this? AI judges
   reward cleverness humans don't, so show a person real renders early.
5. Hand off for campaign setup, preflight and push. Record the copy tags
   (lever, hook, CTA, offer, proof) with the campaign spec so you can
   attribute the result.

---

## Testing (how we learn what works)

- Test **one variable per campaign or arm**, in priority order: list > offer > subject > opener >
  CTA. An A/B variant that changes three things teaches nothing.
- **Sample size:** at a 1% baseline you need **~2,300 sends per arm to see a 2x lift and ~7,750 to
  see 1.5x** (`python3 references/ab_test.py n 0.01 2`). Vendor floors of 100-500 only detect 3x+. So
  at our volumes, test list, offer, angle and segment; pool small copy tweaks through tags.
- **Whole-sequence tests run as separate campaigns** split at random before upload. Step-1 tests
  (subject, first line, CTA) run as in-step variants. Turn Instantly auto-optimize off on a declared
  test, since it optimizes raw replies. Close only after every lead finishes the sequence plus 7 days.
  Log every test with the template and rubric in `references/testing.md`.
- **Grade on positive replies and meetings, never raw replies or opens.** Opens are inflated by
  Apple MPP. Bumps like "Thoughts?" buy replies and lose meetings.
- **Read results with** `python3 references/ab_test.py analyze <sendsA> <posA> <sendsB> <posB>`:
  promote at P(B>A) ≥ 0.90 with ≥10 positives on the winner and meetings not moving the other way.
- **Bars:** a positive reply rate of 1% or more is good and 2% or more is great. Message-market fit
  is at least 1 reply per 320 sends for a templated campaign. Below that after ~1,000 contacts,
  change the list or the offer, not the words. Pause any campaign at more than 0.3% hostile replies
  or more than 2% unsubscribes.
- Read your own results by copy tag before writing a new campaign. Your live read beats any rule
  here once n is large enough.

## What good looks like

- The lever, list, signal and offer are written at the top of the spec before any copy exists. If one can't be answered, stop and get the input.
- The copy lints at 0 errors, scores 85 or above on the playbook rubric, and five real lead renders read well aloud.
- Results are graded on positive replies and meetings, never opens or raw replies.
- Red flag: rewording a campaign that is under 1 reply per 320 sends after about 1,000 contacts. That is a list or offer problem, not a words problem.

## Hard rules (lint enforces most)

1. One lever, one job, one question-CTA per email. No calendar ask in E1.
2. First line about them. No pleasantries, no prefacing, no "following up".
3. Subject 2-4 words, specific, not clickbait. Threaded follow-ups have a blank subject.
4. 50-90 words for E1/E3 (hard max 125); follow-ups under 50.
5. No em dashes, exclamation marks, links in E1, images, tracking or attachments.
6. No hard spam phrases (`references/spam_words.json`); no agency vocabulary.
7. Never fabricate a fact, a mutual connection, a customer or a number. Claims come from the
   client's cleared proof.
8. Instantly spintax only. Every rendered combination is grammatical. Never spin variables, names
   or numbers.
9. Every variable is non-empty on every lead or the row is excluded. AI slots abstain to empty.
10. At most one P.S.: one sentence, new information, never a second pitch.
11. Trigger facts come from stored fields within their send window; a stale or empty trigger drops
    the line, never the email. Never send into disasters or tragedies.
12. Never imply silence ends it ("I'll take silence as a no"); give an easy out instead ("a quick
    'not for us' is enough and I'll stop").
