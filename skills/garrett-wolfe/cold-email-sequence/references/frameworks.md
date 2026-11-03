# Frameworks and Templates

Body templates by situation, in Instantly syntax (`{{firstName}}`, `{{companyName}}`, custom
`{{var}}`, spintax `{{RANDOM|a|b}}`). Templates are shapes, not scripts: rewrite them in the
client's voice and run the lint. `[brackets]` are things you write per campaign. `{{vars}}` are
per-lead.

The skeleton under all of them: **their situation → one lever in their words → (proof or mechanism)
→ one low-effort question.**

---

## E1 frameworks

### 1. Signal 4-move (Kellen Casebeer). Real signal, want a conversation

```
Hey {{firstName}}, [signal ack: one observable fact, single hedge at most].

Figured you might be [verb] [pain 1], [pain 2], or [pain 3].

[Insight: one active, hedge-free sentence about their world.]

[Binary CTA: two states they might be in?]
```
- Name pains in Move 2, not features. Keep the three items about the same length.
- The insight earns a "yes, exactly". Patterns: "[Transition moments] are when [problem] is easiest
  to see." "After a [event], the question shifts from [old] to [new]." "[Tool] covers [X]; the
  hard part is [Y when Z]."
- The CTA offers two states: "Do you already have a system you love, or are you open to changes as
  you settle in?"
- Don't name the product until E3.

Example (Kellen, new hire):
```
Hey {{firstName}}, congrats on joining {{companyName}}.
Figured you might be getting a read on the field team, CRM habits, or what reps are actually doing day to day.
That first window is when it's easiest to spot what's working and what's already messy.
Do you already have a system you love, or are you open to making changes as you settle in?
```

### 2. Observation → lever → proof → ask. Real signal, clear offer

```
{{firstName}}, [observation about them].

[One sentence: the outcome, in their nouns, with one lever.] [Optional: how, in 6-12 words.]

[Proof: similar company went from X to Y.]   ← only if it matches their problem shape

[Soft question CTA?]
```
Example (Eric's "after" cut, 52 words):
```
Sarah, saw you sell to sales leaders.
Noticed John is a BDR on the team. Have you figured out how he could use better data and GPT-4 for prospecting, or still manual?
Most teams save 10 min per prospect and 3x volume without adding headcount.
Worth a look?
```

### 3. "So you can focus on" (Eric). Save-time lever, AI context varies by company

```
{{firstName}}, noticed {{companyName}} [situation].

[What we do, one line.]

So you can focus on {{ai_company_mission}} instead of [the chore].

Worth a look?
```

### 4. Billboard. No signal, homogeneous niche list

The whole offer goes in the subject and first line, and the right readers self-select.
```
Subject: [the offer or the pain, plainly]

{{firstName}}, [the question that names the pain, or the offer, in one line]?

[One line: what we do and the lever.] [One line: proof or mechanism.]

[Soft CTA?]
```
Example (Eric): subject "Tax bill" → "How do you know your current accountant is getting you as much
back as legally possible?"

### 5. Search frame (Kellen). No signal, finding the people with the pain

```
Hey {{firstName}}, I'm trying to find the [team type] that [has X figured out / is dealing with X].

Figured {{companyName}} might be [pain 1], [pain 2], or [pain 3].

[Insight.]

[Binary CTA?]
```

### 6. Creative ideas (Eric). Broad list, varied businesses, AI from their site

```
{{firstName}}, I was on your site and had a few ideas for {{companyName}}.

• {{idea_1}}
• {{idea_2}}
• {{idea_3}}

Of course, I wrote this without knowing your current bottlenecks.

[Soft CTA, e.g. "want me to show how we'd run the first one?"]
```
- **Slot discipline:** you define what bullet 1, 2 and 3 are about, fixed for every lead. Each
  idea must use a capability the client actually has (list 3-5 in the prompt). The model only fills
  in the company detail.
- Each bullet is 8-22 words, lowercase start, no trailing period, no competitor, $, headcount or
  named customer. **Any empty bullet excludes the row.**
- Hand-write 3 complete bullet sets for 3 real companies before any model call.
- Measured: 85 contacts per opportunity vs 176 for a new-hire trigger (Eric, Instantly test).

### 7. Lookalike. You have a customer that looks like them

```
{{firstName}}, [similar company / "a [type] firm like yours"] had [problem in their words].

[What changed, with the number and timeframe.]

Given what {{companyName}} does, figured it might be relevant. [Soft CTA?]
```

### 8. New leader (< 90 days in seat)

```
{{firstName}}, congrats on the [role] seat at {{companyName}}.

Most new [role]s I talk to are looking at [priority 1] or [priority 2] in the first quarter.

[Insight about the window.]

Is [specific thing] on your list, or already handled?
```

### 9. Referral (Aaron Ross, Cold Calling 2.0). Unsure who owns it

```
Subject: right person?

{{firstName}}, I'm trying to find whoever owns [function] at {{companyName}}.

[One line: what we do, the lever.]

Is that you, or is there someone better to ask?
```

### 10. Poke the bear (Josh Braun, 4T)

```
{{firstName}}, [Truth: a relevant fact about them].

[Think: a neutral question exposing a gap they may not have considered]?

[Third-party: teams like X handle it by ...].

[Talk: "worth a look?" / "feel free to say no".]
```

### 11. Hook → Relate → Bridge → Ask (Jeb Blount)

A hook that grabs attention, a line that relates (I get your world), a bridge (what's in it for
them), and an ask. Use a *targeted* bridge (common to the cohort) for scale and a *strategic*
bridge (built for one account) for tier 1.

### 12. Permissionless value / PVP (Jordan Crawford). We hold data they can't easily get

Email 1 *is* the deliverable: no offer to produce it, no call needed to get it.
```
Subject: [the finding, 2-4 words]

{{firstName}}, [what we looked at, for them specifically].

[The finding: 1-2 sentences, concrete, from data only we combined.] [Why it matters, in their lever.]

[Optional: "the full list / photo / breakdown is below" or attached-as-text.]

[Soft question: "want the rest?" / "useful, or already on it?"]
```
- **Gate test:** could you write the value sentence without reading their file? Then it fails.
- **Customer test:** a real customer would call it "really valuable to me".
- If the number is too small to matter to this person, send it up the chain (portfolio-level to the PE firm).
- Every fact comes from a stored source with a URL; nothing is model-asserted.
- PVPs can raise replies more than meetings (Abraham), so grade them on meetings.

### 13. 4-sentence (30 Minutes to President's Club). Clean default for persona-relevance lists

```
{{firstName}}, [reason: what people in your seat are dealing with right now].
[Problem: because of that, X is top of mind / getting harder.]
[Solution: we help [similar teams] do Y, which means Z.]
[Interest CTA: is this on your radar at all?]
```

### 14. POV (Kyle Coleman). Exec and tier-1 accounts with a strong signal

```
{{firstName}}, [signal].
[Interpretation: what that signal means for them, an operational or strategic consequence.]
[Implication: the thing that gets hard next, said plainly.]
[Low-pressure invite: happy to share what's working for teams making that shift, if useful.]
```
One strong POV can drive a 5-touch cascade: the insight → a second implication → proof plus a story →
a low-pressure invite → a graceful exit.

---

## Follow-ups

### E2: same thread, blank subject, 25-50 words. One new fact or a disarm

```
{{firstName}}, [one new fact about them or their market, or a second lever in one line].

[Question?]
```
- Disarming (Kellen): "Was this a misfire on the [thing] we're [doing]?"
- New context (Eric): "from my experience, most [role]s are focused on [quick-win category].
  [Problem in one sentence.] Is [specific problem] on your radar?"
- Findings (Eric):
  ```
  {{firstName}}, here's what stood out about {{companyName}}:
  • [fact 1]  • [fact 2]  • [fact 3]
  [What we do, one line.] Worth exploring?
  ```

### E3: new thread, new subject, 40-80 words. New lever, proof, lower-commitment offer

```
Subject: [customer type] [result]  /  [pain, plainly]

{{firstName}}, [similar company] was [bad state]. We [what we did], and [metric in timeframe].

[Product in one plain sentence, if not yet named.]

[Lower-commitment offer as a question: "want the 2-minute video?", "should I send the list?"]
```
Or the inherited-problem version (Eric): "when you took over at {{companyName}}, did you inherit
[specific problem]? If so, we've been [doing X] since [year]. Worth exploring?"

### E4: same thread, 20-40 words. Exit with a redirect or a resource

- Redirect: "{{firstName}}, if [area] isn't yours, who owns it at {{companyName}}? Happy to reach
  out to them instead."
- Resource: "{{firstName}}, if the timing's off, I have a short [guide/list] on [topic] that might
  still help with [benefit]. Want it?"
- Value bomb (Eric, when the offer can be shown): pull 3 real examples of the output for them and
  put them in the email. "Want to see how I did this?"

---

## Example: a full 4-step sequence

The client is fictional: a tool that logs field reps' visits from a voice note. The lever rotates
from save time (E1) to reduce risk (E3).

```
E1  subject: {{RANDOM|field visits|field rep visits}}
{{RANDOM|Hey|Hi}} {{firstName}}, {{RANDOM|saw|noticed}} {{companyName}} is hiring 4 field reps in Texas.

Figured you might be chasing visit notes, CRM updates, or what reps actually said on site.

Reps always have the activity. The logging is what slips once the team grows.

{{RANDOM|Already solved, or still a Friday cleanup?|Is that handled, or still manual?}}

E2  (blank subject)
{{firstName}}, {{RANDOM|most teams we see|the teams we work with}} lose about a third of visit notes in the first month a new rep is on the road.

{{RANDOM|Does that match what you see?|Sound familiar?}}

E3  subject: {{RANDOM|missed visits|2,000 visits}}
{{firstName}}, Acme {{RANDOM|was missing|used to lose}} 2,000 logged visits a year. Reps now {{RANDOM|leave|record}} a 20-second voice note and the CRM fills itself.

{{RANDOM|Want the 2-minute video?|Should I send a quick video?}}

E4  (blank subject)
{{firstName}}, if field reporting isn't yours, {{RANDOM|who owns it|who should I ask}} at {{companyName}}? {{RANDOM|Happy to reach out to them instead.|I'll take it to them instead.}}
```
