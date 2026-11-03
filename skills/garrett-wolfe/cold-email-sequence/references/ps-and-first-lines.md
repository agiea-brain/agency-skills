# First Lines and P.S. Lines

The two places personalization lives. **Relevance goes in the first line; personal flavor goes in
the P.S.** Personalization without relevance is decoration. Researched 2026-10-26.

**Evidence:** two often-quoted numbers have no primary source, so never cite them: "the P.S. is the
most-read part of an email" and "Lavender: a personalized P.S. lifts replies 35%". The most credible
personalization data is Gong Labs (30K+ emails, observational). The only randomized head-to-head
found is Saleshandy's 12K-send test (vendor-run). There is no clean public test of AI first line vs
no first line on the same list, so run your own (§5).

---

## Part 1: First lines

### What the data says
- **Who you're writing to changes what works** (Gong Labs). Individual personalization more than
  doubles replies from non-managers but adds only ~50% for directors and above. Company
  personalization triples replies from directors and above, with little effect below. **For
  executives, write about the company and its situation; for ICs, write about the person.**
- **AI research + human or rule-bound writing wins; free AI writing loses.** Saleshandy (12K, VP and
  Head of Sales): AI-only 4.1% reply / 1.4% positive / 7.8% spam-flagged; human-only 10.4% / 4.2%;
  hybrid (AI research, human writes) 14.7% / 7.3%.
- Hunter (31M emails, 2025): two custom attributes 5.6% vs 3.6% with none; hand-edited 5.2% vs fully
  automated 4.4%. 69% of surveyed buyers are bothered by AI-written email.
- **A wrong fact is worse than no line.** One error destroys the "a human looked" signal.

### The bridge principle
The first line must make sentence 2 inevitable. **If you can delete line 1 without changing line 2,
it's decoration.**
- Becc Holland: premise → bridge (premise to what you do) → CTA.
- Lavender: observation → informed conclusion (the pain it implies).
- Recipients care less about how much personal data you used than whether the email explains how
  the detail connects to the offer (White et al., 2008).
- **"I'm mentioning this because ___" test** (Rework): if the blank is a problem their role owns,
  keep it. If it's "to show I did research", cut it.
- **Swap test:** if a competitor's name fits the line, it fails.

### Nowoslawski's four levels (higher earns more replies)
1. Random (school, location). Belongs in the P.S.
2. Company or lead specific.
3. Recent, top of mind.
4. **Recent *and* product-related:** infers a likely problem tied to how you solve it. Aim here.

### Taxonomy

| Type | Example (good) | Notes |
|---|---|---|
| **Trigger / signal** | "your team posted three SDR roles this month. new reps usually start by sorting leads by hand." | Strongest when the next line names the problem it creates. Windows in `triggers.md` |
| **Company observation** | "powder-coating turnaround in 5 days is a bold promise most fabricators won't put on their homepage." | Specific, least-obvious fact; numbers and named things beat descriptions |
| **Observation + implication** | "opening a third austin location while payroll still runs from one office puts a lot on one coordinator." | Fact plus its consequence, no praise. The current best practice |
| **Role / persona relevance** | "as the cro, I'd imagine forecast accuracy is the number you get asked about most." | Scales 1:many (relevance) |
| **Pain hypothesis** | "teams that sell through brokers usually hear about lost deals last." | Works without per-person data |
| **Content they made** | "your point on [podcast] that sdr ramp is a data problem, not a coaching problem, is exactly what we see." | Only if engaged with; "I saw your post about leadership" is noise |
| **Tech stack** | "saw you're on hubspot and outreach." + a yes/no on a known gap | Only detectable installs; never an absence |
| **Mutual / affiliation** | "[mutual] said to say hi." | Only if true. The one personal type that earns line 1 |
| **Timeline / tenure** | "90 days into the role is when the stack gets a hard look." | New-leader windows good; tenure as praise weak |
| **Search / billboard** | "trying to find the [team] that [has X figured out]." | No-signal fallbacks (`frameworks.md`) |
| **Creative idea** | "had an idea for {{companyName}}: [slot]." | Slot-defined only |

Bad patterns, always:
- "Love what you're doing at {{companyName}}!", "impressive", "caught my eye": praise, and it fails the swap test.
- "I see you went to [university]!" as an opener: vanity. Put it in the P.S. if anywhere.
- "My name is… I work with…": about the sender.
- "Hi {firstName}, I saw you work at {companyName}": merge tags pretending to be research.
- "Congrats on the new role! Anyway, we sell…": no bridge.

### Prompting AI first lines (when an AI slot is justified)
- **Inputs:** structured upstream fields (site summary, news, job posts, LinkedIn summary), plus
  title and **the segment's pain line**, so the line can bridge. Never raw HTML.
- **A forced prefix written by a human carries the voice**; the model fills only the slot.
  - "I saw you're hiring for '[title]'. usually that means you're trying to ___"
  - "as the [title], I'd imagine you focus on ___"
- **Caps:** one sentence, 12-22 words (25 max).
- **Lead with the most specific, least obvious fact.** No greeting or name inside the line.
- **Banned:** impressive, love what you're doing, came across, I noticed, congrats, caught my eye,
  I was impressed, hope this finds you, and any construction that repeats across the review batch.
  LeadHaste added "while X, Y" after it took over a batch.
- **Never invent, and never merge facts across fields** into a claim neither supports.
- **Abstain:** return `NOT_FOUND` / empty. A formula routes the lead to the segment fallback line, so
  the sentinel is never sent.
- **Watch the abstain rate.** 18-27% is healthy. Near 0% means the model is inventing; over 30%
  means the source or list is wrong.
- **Review 10-25 rows in sequence before scaling.** Check each fact against its source, that it's
  current, the right person and the right company. Strip praise, and ban repeated constructions.
  Then audit a sample monthly.

---

## Part 2: P.S. lines

### What a P.S. is for
There's no proven lift, but it's a cheap slot whose most defensible job is to **carry a human or
attention detail without contaminating a relevance-led body** (Reddit consensus via vendor
roundups: semi-templated body plus one truly personal P.S.). Nowoslawski uses P.S. "attention hacks"
(college plus current city; count of past roles plus a question) but warns that SaaS and e-commerce
buyers spot automation, so use them sparingly.

### Rules
- **One P.S., one idea, one sentence** (two at most); ≤20 words. Never a P.P.S.
- After the sign-off, on its own line.
- **New information only.** Delete test: remove it and reread. If nothing's missing, cut it.
- **Never restate or compete with the main CTA**, and never a second pitch. The P.S. adds no second
  question unless the P.S. *is* the CTA (soft-offer type), in which case the body has none.
- The fact must be **public and explainable**: the prospect can guess its source in one second.
  Never family, health, age, religion or politics; never non-public data; never exact timestamps
  ("posted 6 hours ago"); never web-visit tracking.
- No praise and no grading the person ("impressive background").
- No fake urgency, no "I'm a real person, not a bot" (show it, don't assert it).
- Vary the construction; the same P.S. across 1,000 sends becomes a detectable template.
- Usually email 1 only. A follow-up can carry a different type (referral on E4).

### Types

| Type | Job | Use when | Example |
|---|---|---|---|
| **Human hook** (fact + reaction) | Shows a human looked; pattern break | Template or relevance-led body; a public fact exists | "ps saw you were a ski instructor at whistler, that's so cool." |
| **Former company** | Shared reference | Large, long-established past employer | "ps noticed you were at salesforce, were you there when they bought slack?" |
| **Location** | Cheap local touch | Tight geo segments, real local knowledge (never a chain) | "ps whenever I'm in sf I end up at the marin headlands for sunset." |
| **Social proof** | Credibility without bloating the body | Peer company in the same niche, cleared | "ps [customer] was skeptical too. their note after month two: '[quote]'." |
| **Soft offer** (is the CTA) | A lower-friction exit than a call | SMB, high volume; the body has no question | "ps if a call's too much, I can send a three-bullet teardown of your onboarding email instead." |
| **Referral / routing** | Finds the owner | Unsure of persona; E3-E4 | "ps if [area] sits with someone else, point me to them and I'll leave you be." |
| **Objection pre-empt** | Removes the obvious no | Known incumbent | "ps if you already have an agency, this runs alongside them, not instead." |
| **Signal** | Timely aside not core to the pitch | Real signal unrelated to the first line | "ps congrats on the bills clinching, must be a good week in buffalo." (allegiance evidenced) |
| **Opt-out** | Replies from not-now people | Late steps | "ps if now's not the time, a one-line 'not now' is more useful to me than silence." |

Anti-examples: "P.S. let me know if you want to chat!" (repeats the CTA). "P.S. only 2 spots left!"
(fake urgency). "P.S. saw you volunteer at a food bank, which is why pipeline matters to you" (a
stretch tie-in). "P.S. impressive background" (grading).

### Prompting AI P.S. lines
- Input only the profile fields you'll allow (education, prior roles, volunteering, location,
  certifications, public talks). Never the whole scrape.
- A forced prefix ("ps saw you ") plus the reaction list; 8-20 words.
- **Only a fact present in the input; never infer.** Abstain → empty → no P.S. (not a fallback
  P.S. that says nothing).
- A regex judge rejects grading and tie-ins (`impressive|smart|accomplished|bet that|shaped|honed|
  instincts`), then a cheap model judge checks the fact against the source.
- Don't say "cold email" in the prompt (Clay community tip). Describe the reader instead.

---

## Part 3: Testing them
Run a **three-arm first-line test**: AI line / segment line / none. Run **P.S. on vs off**
separately. Measure positive replies, not replies. These are step-1 variant tests, so the volume
math in `testing.md` §1 applies. At 1-2% PRR, only a ~2x difference will show up under ~2,000 sends
per arm, so pool through `hook_type` and `ps_type` tags across campaigns rather than expecting one
campaign to settle it.

