# AI Lines, Variables and Spintax

## Part 1: AI-written lines

### When to use AI at all
Use AI context only when the prospect's business **changes how the product helps them** (Eric).
- **Yes:** broad targeting (a facilities manager at a hospital vs a hotel vs a school), variable
  use cases, creative-ideas campaigns.
- **No:** commodity use cases, narrow homogeneous lists, or anything that feels forced. Static copy
  wins there.
- **Checklist:** the targeting is broad enough that the context varies; the value changes with what
  they do; the line adds relevance; removing it would make the email generic. Fail any one, and
  keep it static.

### Slot discipline
AI fills **slots inside a human template**, never whole emails (in our testing, whole emails from
top models scored well with AI judges and a human rejected them as clever but unclear).

For each slot, define:
1. **The frame lives in the copy, not the variable.** "I think we can help you
   {{specificity_line}}." The variable holds only the tail, so the model can't drift the sentence.
2. **What it's about**, fixed for every lead (slot-defined bullets: 21/23 usable vs 2/5
   free-form).
3. **Caps:** words (≤20 for a line, 8-22 per bullet, 6-14 for a tail) and characters (≤90).
4. **The offer block:** 5-7 lines of what the client actually does, plus a **"What they do NOT do"**
   line. The model may only promise what's in that block.
5. **Banned words:** vague outcomes ("grow sales", "boost margins", "improve efficiency", "your
   business", "platform", "solutions", "leverage", "ecosystem"). If a line needs one, the anchor
   is too vague.
6. **Abstain rule:** if the input is thin (a description under ~20 characters or no evidence), the
   model returns an **empty string**. Never "N/A", "there", "your company" or "cannot be
   generated".
7. **Evidence quote:** each line quotes the source substring it's based on (`evidence_N`). Code
   checks the substring exists and blanks the line if not. That's a free hallucination check.
8. **Reading grade ≤ 7** on the generated part.

### Process (Eric's approval loop)
1. **Hand-write 3 complete examples** for 3 real companies before any model call. The AI never
   drafts the exemplars it is graded against.
2. Few-shot with 8-10 pairs, including at least 2 abstains.
3. Run 1 lead, then batches of 10, shown as a table. Each edit updates the prompt.
4. **Lock the prompt after 2 consecutive rounds with zero edits.** Judge a batch, never a row.
5. Run 5 rows before 5,000. Expect 10-20% blanks. **More than 30% blank means the list is wrong.**
   **Under 5% blank means the prompt got loose.**
6. Use a cheap model for slots (nano / mini class).

### Facts are computed, not generated
Dates, counts, tenure, funding amounts and enums come from code. The model only phrases them. For
signal lines:
- "started a new role", never "hired" (28% are internal moves).
- Funding: the round and amount, never the valuation or investors; indexes lag 3-4 months.
- Job posts: blank if older than 30 days.
- Never name the recipient to themselves as "another prospect"; never claim a mutual connection;
  never name a client's customer without approval.
- Skip personal, political, bereavement or charged social posts (fail closed).

## Part 2: Variables and blanks

**Instantly sends a blank variable as an empty string, silently.** No bounce, no error. "Hey ,"
goes out.
- Every variable in a subject or body must be non-empty on **every** enrolled lead, including
  in-flight leads, or have a fallback. Run a required-variable check before activating.
- **Word-level slots get a fallback:** `{{firstName | there}}`, `{{companyName | your team}}`. Instantly
  renders the fallback when the field is empty, so a blank becomes impossible. Pick a fallback that
  reads naturally in the sentence; lint renders the fallback to check.
- **Spintax can't gate an empty variable.** `{{RANDOM|Saw {{funding_line}}.|}}` renders "Saw ."
  about half the time. Use a **self-erasing whole-sentence variable** (the variable holds the full
  sentence, or is empty and the template still reads), or split the list: leads with the slot go
  to the AI campaign, leads without go to the static one.
- An empty creative-ideas bullet excludes the row.
- Namespace custom fields per campaign (`creative_idea_1_<campaign>`) so a re-run can't overwrite a
  live one.

## Part 3: Spintax (Instantly)

**Syntax:** `{{RANDOM|option a|option b|option c}}`. No spaces around the pipes (house convention).
Smartlead's single-brace `{a|b}` renders **literally** in Instantly, and lint flags it.

**Where:** 3-5 blocks per cold open, 2-3 options each, on:
- greetings `{{RANDOM|Hey|Hi}}`
- connectors `{{RANDOM|saw|noticed}}`
- a mid-body verb `{{RANDOM|help|work with}}`
- the CTA, whole sentence: `{{RANDOM|Worth a look?|Is that on your radar?|Useful?}}`
- an opt-out line, whole sentence

Subjects get at least 1 block; follow-ups get at least 2.

**Never spin:** variables, `{{accountSignature}}`, numbers and stats, customer or brand names,
proof, prices, technical terms. Spinning a case-study name is a fabrication.

**The golden rule: every combination is a grammatical sentence.** Adjacent blocks multiply, so:
- BAD: `{{RANDOM|let me know if|would}} {{name}} {{RANDOM|would be better to ask|be a better person}}`
  produces "would Sam would be better to ask".
- GOOD: spin the whole clause: `{{RANDOM|let me know if {{name}} would be better to ask.|would
  {{name}} be the better person to ask?|should I ask {{name}} instead?}}`
- Spun options must match the register. Don't pair "Worth a shot?" with "Would you be amenable to a
  trial?"
- Each option must keep the email's single question. Don't spin a statement against a question.

`lint_copy.py` renders combinations and flags doubled words, double spaces, " ." / " ?",
mismatched question counts across combinations, and stray `{`/`}`.
