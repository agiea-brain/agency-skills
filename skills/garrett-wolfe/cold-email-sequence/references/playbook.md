# The Cold Email Playbook

The canonical reference behind the `cold-email-sequence` skill. Each rule names its source, and
where experts disagree, §14 records the call we made and why. Researched 2026-10-26.

---

## 1. Sources

| Who | What to take from them | Where |
|---|---|---|
| **Eric Nowoslawski** (Growth Engine X; 1.5-8M emails a month) | Offer before copy; lead-magnet rubric; campaign-idea generation (broad → niche); creative-ideas campaign; slot-defined AI lines; message-market-fit bars; test like ads | `github.com/growthenginenowoslawski/coldoutboundskills` (MIT); Clay blog "validate cold outbound offers by finding message-market fit"; GTM Engineer podcast |
| **Kellen Casebeer** (The Deal Lab, Smartlead partner) | 4-move E1 (signal → three pains → insight → binary CTA); proof held to E3; disarming E2; segment by insight, trigger and signal | Smartlead talks "Cold Email Like a Pro" (2025) and "Creative Segmentation" (2025); our synced `kellen-copy-generator` skill |
| **Josh Braun** | Poke the Bear; detachment ("sort, don't sell"); 4T: Truth, Think, Third-party credibility, Talk | joshbraun.com |
| **Will Allred / Lavender** | Short, mobile-first, grade 3-7 reading level, about them, context first | Lavender Cold Email Benchmark Report (231,818 emails, to Feb 2026) |
| **Gong Labs** | Interest CTA beats time ask cold; ROI claims −15%; "Thoughts?" −20% meetings | Gong Labs CTA study (304,174 emails) |
| **Becc Holland** (Flip the Script) | Relevance vs personalization; premise → hook → CTA; one premise reused across the cadence | |
| **Jason Bay** (Outbound Squad) | REPLY: Results, Empathy, Personalization, Laser-focus, You. "Reps have an opening problem, not a closing problem" | |
| **Justin Michael** (*Tech-Powered Sales*) | The JM "spear": 1-3 sentences, pain or fear, a hinted fix, a binary close | |
| **Aaron Ross** (*Predictable Revenue*) | Cold Calling 2.0 referral email: find the right person, plain text | |
| **Jeb Blount** (*Fanatical Prospecting*) | Hook → Relate → Bridge → Ask; targeted vs strategic bridges | |
| **Alex Berman** | Neutral subjects; open on something they already believe | |
| **Patrick Spychalski** (The Kiln) | Offer beats personalization; work backwards from the value prop to data that quantifies it | |
| **Jordan Crawford** (Blueprint) | PQS (pain-qualified segments from detectable signals); PVP (the email *is* the value) | `voices-and-styles.md` |
| **30MPC** (Farrokh & Cegelski), **Sam McKenna**, **Kyle Coleman**, **Nick Abraham**, **Jeremy & Jack** | 4-sentence email; recipient-only subjects and objection pre-empts; POV-led emails; offer-first at 1.5M a month | `voices-and-styles.md` |
| **Benchmarks** | Instantly 2026 (2025 data), Smartlead State of Cold Email 2026 (850M+), Belkins 2025-26, Saleshandy 2026, Hunter | `evidence.md` |

---

## 2. The priority order

`list > offer > subject > opener > CTA > timing > length` (Eric; Spychalski; every benchmark that
slices by segment). Effort and testing follow this order. When a campaign underperforms, go back
up the list. Rewording an email aimed at the wrong list with a weak offer is wasted time.

**Unit economics first** (Eric): cold email pays when the TAM is more than ~100K contacts, LTV is
more than ~$10K and the sales cycle is under 6 months. Below that, use smaller, curated lists and
more manual research per lead. Judge campaigns by **sends per meeting** and **email-to-deal**,
not reply rate.

---

## 3. The three value levers

Every product sells at least one of these, and every email leads with exactly one:

1. **Make money**: revenue, pipeline, customers, deals, price, retention as revenue.
2. **Save time or money**: hours, headcount, tools, cost per X, cycle time.
3. **Reduce risk**: misses, errors, compliance, churn, bad hires, wasted spend, being caught out.

Eric's version splits "save time" and "save money" and adds "mitigate risk". His copywriting skill
only uses the first three. We merge time and money because buyers hear them together, and we keep
risk, which is often the strongest lever for regulated or high-stakes buyers.

**How to pick:**
- Start from the **#1 pain the best customer had before buying** (Eric's north star). Its lever
  is E1's lever.
- Break the product into component offers and tag each one with a lever (Eric, Clay article).
  That gives you the rotation for E2-E3.
- Say it in the **prospect's nouns**, never the vendor's. "know what each pool noodle costs to make
  before you price the next run", not "improve margins". Banned as too vague: "grow faster",
  "increase sales", "boost margins", "improve efficiency", "drive results", "your business".
- **Problem framing over ROI promises.** Gong: ROI claims cut success 15%. Put a number in proof
  ("Acme went from missing 2,000 visits a year to capturing all of them"), not in a promise.

**Rotate.** If E1's lever got no reply, it didn't resonate. E2 can deepen it with one new fact, but
E3 switches lever (Eric).

---

## 4. List, signal and relevance

- **Segment by insight, trigger and signal, not demographics** (Kellen). The tighter the
  list, the more the copy can name the filter itself ("you run a cost seg practice with 3-10
  people").
- **Broad → focused → niche** (Eric). A broad list (base filters only) needs strong AI
  relevance. A focused list adds one filter. A niche list stacks 3-4 filters and can run
  near-static copy. Generate 15-25 campaign ideas across all three levels before picking one.
- **Three campaigns worth always having** (Eric): Creative Ideas (AI bullets from their site), New
  Leader (in seat under 90 days), Lookalike (modeled on the best case study). Plus one no-AI
  campaign: short, snappy, a strong offer and tight targeting.
- **The 10-minute test:** what would a good rep look up in 10 minutes before writing? Automate that
  research, and that's the campaign.
- **Relevance vs personalization** (Becc Holland). Personalization is 1:1 and couldn't be sent to
  anyone else. Relevance fits a cohort. With no real individual premise, be relevant, not
  fake-personal. Research once and reuse the premise across the whole sequence.
- **Signals:** a public ask or job post > a dated event (new role under 90 days, raise, launch,
  hiring burst, expansion) > a structural fact > none. A funding index lags 3-4 months, so check
  the date. "Started a new role" includes internal moves (28%), so never write "you hired". Signals
  aren't a silver bullet (Eric). A signal with a weak offer still fails.
- **Never invert an undetectable signal.** "Has a VP Sales but no GTM engineer" is fine (titles are
  detectable). "Doesn't use an enrichment tool" is not (stack detection misses).
- Avoid: scraped review complaints from G2/Capterra, private revenue guesses, and existing
  freemium users (that's nurture, not cold).

---

## 5. Offers

Full method: `offers.md`. The essentials:
- A concrete free offer beats "book a call" by 3-10x (Eric). A meeting is an ask, not an offer.
- Ask: what could you do for this prospect in under 30 minutes that they'd pay $100 for?
- Score 1-5 each on: cheap to deliver, valuable enough to pay for, shows competence, unique
  vs competitors. Propose at 15/20 or more.
- Never gate it behind a form. The prospect's maximum effort is a one-line reply.
- Lower the risk of the first step: a free test, a sample, an audit, or pay only on result.
- Name why they wouldn't reply, and answer it in the offer (Eric).
- If a campaign fails, change **what they get**, not the wording.

---

## 6. Subject lines

- **Length:** 2-4 words (Belkins 5.5M: 46% opens at 2-4 words vs 34-39% at 7-10). Saleshandy argues for 5-7 words;
  §14 records our call.
- **Personalized subjects reply 7% vs 3%** (Belkins). That's the only reply-measured subject
  finding, so use a name, company, role or signal when you have a real one.
- **Three types** (Eric):
  - **A, intrigue or signal** (2-4 words): "question for {{firstName}}", "{{companyName}} field
    team", "the vp sales req", "title agency marketing".
  - **B, whole offer** (subject plus preview): "Ever chase renters to pay on time?" plus the first
    line, so the reader self-selects. Use it when data is thin.
  - **C, problem indicator**: "looked you up on chatgpt", "review from karen", "starter vs pro".
- Kellen's house style: 2-3 words, lowercase, no punctuation, named after the signal ("new role",
  "growing the team").
- **Colleague test:** could a coworker or customer have sent this? If not, rewrite it.
- **Banned:** "quick question", "curious", "following up", "touching base", "partnership
  opportunity", a fake "re:"/"fwd:", ALL CAPS, emoji, urgency, and anything promotional.
- The first 50-100 characters of the body show as preview text. Write the subject and first line
  as one unit.
- Open rates are inflated by Apple Mail Privacy Protection, so treat open-rate studies as weak
  evidence and favor reply-measured findings.

---

## 7. Openers

**The first line is about them, specific, observable and true.** Patterns:
- **Signal ack** (Kellen): "saw {{companyName}} is hiring for the field team." Name the real thing.
  No double hedge: "saw your team is looking at X", not "heard you may be looking at X".
- **Situation recognition** (Eric): "noticed you sell to {{ai_customer_type}}." One sentence
  describing their world.
- **Truth** (Braun): a relevant fact. "noticed you're hiring 3 SDRs."
- **Belief** (Berman): something the reader already believes is true about their market.
- **Search frame** (Kellen, with no signal): "I'm trying to find the [team] that [has X figured
  out]."
- **Poke the bear** (Braun, Eric), as a neutral question that surfaces an unconsidered gap:
  - "Do you already have a reliable way to {{problem}}?"
  - "Have you figured out {{outcome}} without adding headcount, or still manual?"
  - "Totally possible you've solved this. How do you handle {{process}} today?"

**Never:** "hope this finds you well", "I wanted to reach out", "I came across your profile", "my
name is", "I'm reaching out because", observer-fan voice ("I noticed your amazing…"), and
prefacing ("quick one", "I'll keep this short", "one more thought"). Never start an AI line with
"I noticed".

Gong found "Hope all is well" correlated with +24% meetings. It's correlation on 2020-era data,
and every practitioner disagrees, so we ban it (§14).

---

## 8. Body, CTA and proof

### Body
Pick a framework by situation (templates in `frameworks.md`). They all share one skeleton:

> **their situation** → **the pain or outcome in their words, with one lever** → **(optional) proof
> or the specific mechanism** → **one low-effort question**

- One email, one job. Aim for 50-90 words (Eric's best: 70-90; Smartlead: first emails under 50
  words replied best at 1.47%; Lavender: 0-50 words +23%). Go to 125 only when an AI slot earns it.
  §14 records our call.
- Reading grade 3-7: Lavender saw 1.66x replies. Short sentences, plain words, contractions
  everywhere (Kellen).
- **Keep sentences about them to sentences about you at 3:1** (Eric). "You" outnumbers "I/we".
- Active voice, no hedges ("usually", "might possibly"), no adjectives without data. Keep numbers
  as digits ("3x", "30 days").
- Light peer humor is fine ("equipment older than some employees").
- **The three-pass cut** (Eric):
  1. Delete fluff: greetings, "I wanted to", hedges (about −20%).
  2. Compress: "We built a platform that can do X" becomes "We do X" (about −15%).
  3. Cut adjectives without data (about −10%).
- Mobile-first: 2-4 short paragraphs, no paragraph longer than 2 lines on a phone (Lavender +24%).

### CTA
- **Exactly one question, and it's the CTA. It must be answerable in 5 words or fewer.**
- Three good forms:
  1. **Interest or state (default):** "worth a look?", "is that on your radar?", "already solved,
     or still manual?", "do you have a system you love, or open to changes as you settle in?"
     (Gong interest CTA ~2x next best; Kellen binary; Braun.)
  2. **Value exchange:** "want me to send the 3 we'd flag for {{companyName}}?", "should I send
     the list?" (pairs with an offer).
  3. **Confirmation:** "is this still the case?", "did I get that right?"
- **Never in E1:** a calendar link, a specific time, "15 minutes", "hop on a call", "let me know
  your thoughts", "thoughts?" (Gong −20% meetings), or two asks.

### Proof
- One customer, one number, framed as what happened: "[similar company] went from X to Y in Z."
  Third-party credibility over self-claims (Braun). Never a logo list, award or ranking (Holland).
- Pick proof by **problem shape**, not industry label. Name 2-3 relevant customers at most, never
  the list.
- **Placement:** in E1 only if it matches the prospect's problem shape exactly; otherwise E3
  (Kellen). See §14.
- Proof must be cleared by the client. Never generalise one client's result to "our clients".

---

## 9. Scoring rubric and QA

### Rubric (0-100; adapted from Eric's positive-reply scorer)

| Dimension | Points | Full marks when |
|---|---|---|
| Situation recognition | 25 | The first line is specific, true and about them; a colleague would recognise their company in it |
| Value clarity | 25 | One lever, in their nouns, concrete; the reader knows what they'd get within 2 seconds |
| Relevance / personalization | 20 | The reason-now is real; AI lines add relevance and would make the email generic if removed |
| CTA effort | 15 | One question, answerable in ≤5 words, no calendar ask |
| Punchiness | 10 | 50-90 words, grade ≤7, no hedges, reads aloud in under 20 seconds |
| Subject | 5 | 2-4 words, specific, passes the colleague test |

**85 or more: ship. 70-84: one more pass. Under 70: go back to the list or offer, not the words.**

### QA checklist
- [ ] Inputs written at the top of the spec: cohort, signal, lever, offer, proof cleared.
- [ ] `lint_copy.py` reports 0 errors; warnings each have a reason.
- [ ] Every claim traces to a cleared source; nothing invented (customers, numbers, mutuals).
- [ ] Every variable is non-empty on every lead (in-flight too), or the row is excluded.
- [ ] Five real leads rendered end to end and read aloud.
- [ ] Edited for AI writing patterns, then re-linted.
- [ ] Would I reply to this? Yes.

---

## 10. Sequence and follow-ups

**How much follow-ups add:**

| Source | Share of replies from follow-ups |
|---|---|
| Instantly | 42% |
| Smartlead | 52% with 3 steps; replies per 1,000 contacts go 12 → 25 → 33 → 40 for 1 / 3 / 5 / 7 steps |
| Saleshandy | 57% of positive replies |
| Belkins | step 3 alone = 35.6% of email-sourced meetings |

Against that, Belkins found 4+ steps more than triples unsubscribe and spam rates (complaints 0.5%
at E1 → 1.6% at E4). **Default: 4 steps; never more than 5.**

**What each step does:**
- **E1:** the strongest signal, the clearest offer, and the best-matched proof if any.
- **E2 (same thread, blank subject):** one new fact or angle, written like a reply (Instantly:
  reply-style E2s +30%). Or Kellen's disarming bump ("was this a misfire on the tool we're
  using?"). No re-pitch.
- **E3 (new thread, new subject):** a new lever and angle. Name the product plainly, give one proof
  point, and drop to a lower-commitment offer (audit, list, video, resource) (Eric, Kellen). Eric
  says to consider dropping all AI personalization here.
- **E4 (same thread):** exit. Either a redirect ("if this isn't yours, who owns X at
  {{companyName}}?") or a useful resource. No guilt, no "last chance".

**Rules:**
- Every email stands alone. Never reference the previous one: "following up", "bumping", "circling
  back", "just checking in", "did you see my last", "one more thought", "last note from me".
- Never imply silence is consent or ends it. Give an explicit easy out: "a quick 'not for us' is
  enough and I'll stop."
- Send on weekdays in business hours in the recipient's time zone. Tuesday-Wednesday and early
  morning lead in vendor data; check your own results.
- Contact each person about once a quarter at most (Eric). Re-approach with a new angle, never the
  same sequence.
- Gaps of 2-4 days between steps (2/2/3/2; step 1's delay is never 0).

---

## 11. Personalization and AI at scale

Full method: `ai-lines-and-spintax.md`; first lines and P.S. lines: `ps-and-first-lines.md`;
triggers: `triggers.md`; segment routing: `segments-and-offers.md`. The rules that matter:
- **AI fills slots, never emails.** The template, pitch and CTA stay human. In our testing,
  whole emails from top models scored well with AI judges and a human rejected them as clever but
  unclear.
- **Use AI context only when the prospect's business changes how the product helps them** (Eric).
  A commodity use case ("vacuums clean floors the same everywhere") or a homogeneous niche list
  should stay static.
- **Slot discipline:** the operator defines what each slot is about. Free-form "three ideas" was
  2/5 usable; slot-defined was 21/23 (Eric).
- **Abstain = empty string.** An empty slot excludes the row or routes it to a non-AI campaign,
  never to "there", "N/A" or "your company".
- **The model never establishes a fact.** Dates, counts and enums are computed in code; the model
  only phrases them.
- Generic merge-field personalization *hurts*: Reply.io measured −26% interested.

---

## 12. Deliverability rules for copy

Deliverability is about 80% infrastructure and 20% content (Eric). The 20%:
- Plain text. No images, logos, HTML signatures, attachments, open or link tracking.
- No links in E1. From E2 on, at most one link, to your own domain, written as text.
- No hard spam phrases (`spam_words.json`, tier `hard`). Treat soft words as a judgment call.
- No ALL CAPS, multiple "!", "$$$", or "free" offers phrased like ads ("100% free", "risk-free").
- Spintax on every cold open (3-5 blocks) so no two sends are byte-identical. AI lines vary the
  text too.
- Sender name is a real person. The signature carries the name, company and physical address
  where the client requires it; `{{accountSignature}}` in Instantly.
- Company names containing spam tokens get shortened ("Calcon Mutual Mortgage" → "Calcon Mutual").
- Bars: bounce under 2%, spam complaints under 0.3% (Google), and a reply rate of at least 1% per
  domain after 200 sends.

---

## 13. Testing

- **One hypothesis per test.** Hypothesis tests run as two separate campaigns (Eric); in-sequence
  A/B is for polishing, with 2-3 variants at most.
- **Sample size per arm (Eric):**

| Baseline | Detect | Sends per arm |
|---|---|---|
| 1% | 2x | ~2,300 |
| 1% | 1.5x | ~7,750 |
| 2% | 2x | ~1,150 |
| 2% | 1.5x | ~3,800 |

Corrected 2026-10-26 from the standard two-proportion formula (α .05, power .8). Eric's repo table
(500 / 2,000 / 250 / 1,000) is about 4x too small. Full table, test design, tags, log template and
decision rubric: `testing.md`. Math: `references/ab_test.py`.

- Close a test only after every lead finishes the sequence plus 7 days (typically 3-5 weeks). Promote
  at P(challenger > champion) ≥ 0.90 with ≥10 positives on the winner.
- **Message-market-fit bar** (Eric): at least 1 reply per 320 sends for a templated campaign and
  ~1 per 65 for curated ones. If a campaign is still failing at ~1,000 contacts, change the list or
  offer. Below the bar, switch to an information-gathering angle (asking their view, sharing
  expertise) instead of pitching.
- **Positive reply rate** = (interested + soft + referral) / sent, excluding OOO and bounces. 1% or
  more is good; 2% or more is great. A 1% reply rate at 70% positive (0.7%) beats 5% at 10%
  positive (0.5%).
- Weekly: a winner at 2x baseline or more gets scaled; a loser under 0.5x baseline gets killed.
  Pause at more than 0.3% hostile or more than 2% unsubscribe.

---

## 14. Where experts disagree, and our call

| Question | Positions | Our call |
|---|---|---|
| **Length** | Lavender/Smartlead: under 50 words. Eric: 70-90. Gong: 30-150 for meetings | **50-90**, max 125 only for AI-slot campaigns. |
| **Subject length** | Belkins: 2-4 words. Saleshandy: 5-7 | **2-4.** |
| **E1 CTA** | Gong/Braun/Kellen: interest or state. Eric/Instantly: a meeting or soft time ask | **Interest/state** in E1. A soft-time ask is allowed from E3, never a fixed time. |
| **Proof placement** | Eric: E1. Kellen: E3 | **E3 by default.** E1 only when it matches the prospect's problem shape. |
| **Greeting** | Eric's spam checker: no "Hi". Spintax skill and our house style: `{{RANDOM\|Hey\|Hi}}` | **Keep the greeting** (house style); spin it |
| **Pleasantries** | Gong: "hope all is well" +24% meetings. Everyone else: cut | **Cut.** Correlational, 2020-era, and it reads as filler |
| **Sequence length** | Belkins 2024: 1-3. Smartlead: 3-4. Instantly: 4-7 | **4**, max 5 |
| **Bump style** | JMM: "Thoughts?". Gong: −20% meetings | **No bare bumps.** E2 adds a fact or disarms |
| **Blank variables** | Some Eric playbooks drop the clause with spintax; his README bans that | **Banned.** Spintax can't gate a blank; exclude or split the row |
| **P.S.** | "Most-read part" folklore (no source); Nowoslawski: attention hacks, sparingly | **Optional, one sentence, a human fact or a soft offer**; never a second pitch |
| **Lead magnets / PVP** | Eric and Crawford: lead with value. Abraham: magnets raise replies, not always meetings | **Use them; grade on meetings, not replies** |
| **Spam word list** | Eric bans single words like "sales", "marketing", "new", "now", "problem" | **Phrases are hard bans; single words are warnings.** You can't sell to sales leaders without saying "sales" |

---

## 15. Handling replies (because the sequence is only half of it)

- Answer positive replies **fast**: within 30 minutes during business hours. A 2-minute answer vs a
  2-hour answer is a ~5x booking difference, and replies left 24h+ lose about half (Eric).
- Keep the reply shorter than their message. Offer two specific times plus a link as fallback.
- Negative: "Got it, appreciate the direct reply. I'll stop reaching out." No argument.
- Wrong person: thank them and ask who owns it. A referral is a positive reply.
- Classify only the first reply per lead (positive_interested / positive_soft / positive_referral
  / neutral_question / negative_notnow / negative_notfit / negative_hostile / unsubscribe / ooo).
