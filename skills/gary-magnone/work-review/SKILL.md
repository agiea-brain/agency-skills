---
name: work-review
title: Work review
description: Reviews something a teammate or vendor built for a client (a page on staging or live, a dashboard, a PDF, a report, a page revamp) and writes the feedback note that goes back to them. Opens the real thing first, not a summary of it, checks it against the plan it was built from, splits the read into "the good" and "opportunities" ranked high, medium, and low, keeps it at the strategy level, and frames it so nobody on the team feels graded. Use when the user says "/work-review", "[person] is asking me to review [the thing]", "draft of the new [page]. thoughts?", "what's good, what's not so good, any high priority items to flag", "check out [person]'s updated dashboard", "is this page organized the way we planned", or pastes a teammate's handoff and asks what to say. Never sends anything.
category: Operations
---

# /work-review

Somebody on the team built the thing: a writer drafted the page, a developer built it on staging, an analyst rebuilt the dashboard, a designer revamped the PDF. They asked the user to look at it. The user needs to know two things fast: is it good enough to move forward, and what are the few things that would make it better. Then they need a note they can paste into Slack, email, or a project task.

Two outputs: the read, and the note. The note is the deliverable.

## When to use
- A teammate or vendor sends a link and asks for a review or "thoughts"
- The user wants to confirm a staging page matches the plan before it goes live
- A dashboard or report was updated and needs a check before it goes to the client
- Not for the user's own finished deliverable before it ships. That is `/source-check`.
- Not for handing off the user's own work. That is `/rundown`.
- Not for passing client feedback to the person who builds it. That is `/direction`.

## Inputs
1. **The thing itself.** The live or staging URL, the dashboard link, the file. Open it. If it lives in a logged-in tool (CRM, ad platform, CMS), open it in the browser and read the real settings and report details, not a screenshot or an export of it.
2. **What it was supposed to be.** The plan the user wrote or approved: the content brief, the spec, the strategy doc, the notes from the call where it was agreed. Find it in the client's project folder, the meeting notes, or the task. The review is against that plan, not against a fresh opinion.
3. **Who built it and who gets the note.** Often different people. A team lead asks, but the writer reads it. One person gets the note, but three more are on the thread. Write for everyone who will see it.
4. **The old version, if there is one.** A revamp gets compared to what it replaced.
5. **Standing context.** Whatever account notes and recent work the project keeps for this client.

If the handoff has no context on what they were going for, ask the user once whether to ask them. Frame it as your limitation ("I'd be guessing at what you were going for"), never as their miss.

## Workflow

**1. Name the thing, the plan, and the reader.** One line each before reviewing. "New location page, against the content brief, note goes to the content lead for the writer."

**2. Open the real thing.** Every page, every chart, every link. Click the buttons. Read the report settings behind a number that looks off. If two numbers disagree, open both and find out why before calling it a problem. Do not review from the handoff message alone.

**3. Check it against the plan.** Did it follow the structure, the sections, the questions the brief asked? Did it pick up the requests other people made along the way (a change the client asked for, a fix agreed on a call)? Note anything the plan asked for that is missing, and anything new that was not in the plan.

**4. Assume odd choices were on purpose.** If something looks like a placeholder or a choice in progress, treat it as intentional and frame it as "confirming before we go live," not as direction.

**5. Write the read.** Two lists, in chat:
- **The good.** What landed, specific, credited to the work. This is real, not a cushion.
- **Opportunities.** Each item ranked High, Medium, or Low. Strategy level only: structure, positioning, what the reader needs and is not getting, what will not hold up, what breaks. No line edits, no rewrites of their copy. A risk flag (a claim that will not hold up, a broken link, a wrong number) always stays in.

Then stop and show the read. The reviewer changes the ranks and cuts anything they disagree with, and the note gets written from their version, not this one.

**6. Questions for the client only if they are needed.** Do not invent new questions for the client. Use the ones already in the brief or plan. If one more is truly needed, it goes as a sub-bullet under the opportunity it serves, not as its own list.

**7. Suggest a fix with each question.** When an opportunity is a "why is this happening," put your best guess and a concrete fix next to it ("my guess is nothing moves a deal out of the first stage, so deals sit there for months; a 90-day rule would clear most of them today").

**8. Write the note.** In the user's voice, using their style guide if they keep one. Unordered bullets. Short. The good first, then opportunities by priority. Team framing: "how we use the pipeline," never "how you set it up." No personal asides, no grades. If it goes into a task, give it as plain text they can paste, not an attachment.

**9. Verify every claim in the note.** Anything stated as fact (a button was fixed, a number, a rule that changed) gets checked live right before the note goes out. If you cannot say how you know it, cut it or check it.

**10. Show the draft and stop.** Nothing goes to Slack, email, or a task until the user says "send."

**11. Write it down.** Save the approved note in the client's project folder so the next review starts from it.

## Output format

The read, in chat:

```
[Thing] for [client], reviewed against [the plan]
Note goes to: [names]

The good
- [What landed, specific]
- [What landed, specific]

Opportunities
- HIGH: [issue]. [Why it matters]. [Fix]
- MEDIUM: [issue]. [Fix]
  - [Client question, only if needed]
- LOW: [issue]. [Fix]
```

The note, Slack length:

```
Hey [name]! [One line on what this is and that it's a big step up, if it is.]

The good:
- [bullet]
- [bullet]

A few opportunities:
- [High item]
- [Medium item]
- [Low item]

[One line on what happens next, or the one thing to confirm before it goes live.]
```

## Corrections that keep coming back

| What went wrong | The rule |
|---|---|
| Reviewed from the report or the handoff message without opening the account | Open the real thing. Never review from a report or a handoff alone |
| Added new questions for the client | No new client questions. Use the plan's, and nest any extra under its opportunity |
| Treated a placeholder as a mistake and wrote direction | Odd choices are on purpose. Confirm, don't direct |
| The note didn't sound like the user | Load the voice or style guide before the first draft, not after |
| Listed every detail found | Three to six opportunities. Cut the rest |
| One bullet carried a personal aside and ran long | Same shape and length for every bullet. No asides |
| A note about how the team uses a tool read like blame | Team framing. What we do and what is missing, never how well someone did |
| Stated a fact nobody had checked | Every fact in the note is checked live before it goes |
| Formatted the note when the task needed paste-ready text | Unordered bullets, plain text, ready to paste |

## Where output goes
The read and the approved note go in the client's project folder, in a named subfolder like `location-page-review/`.

## What good looks like

- First thing I check that most people skip: whether the real thing was opened. A review written from the report or the handoff message alone reads fine and misses what is actually on the page.
- The mediocre version lists every detail found. Three to six opportunities, ranked, is the output; the rest gets cut.
- I know the note is right when every fact in it was checked live, the bullets all have the same shape and length, and nothing in it reads as a comment on the person rather than the work.
- Odd choices are usually on purpose. Confirm before writing direction.

## Why this exists
Reviewing a teammate's work is where most of an agency's quality control happens, and the note is easy to get wrong. This skill came out of writing the same review by hand week after week across several clients and correcting the same things each time. It gives every review one shape: open the real thing, check it against the plan, credit what landed, rank what's left, and keep the note about the work.
