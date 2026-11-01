---
name: rundown
title: Delivery rundown note
description: Writes the short note that goes out when someone hands a finished piece of work to a client, partner, or teammate (a deck, a tool, a strategy doc, a spreadsheet, a package of files). Opens the deliverable, pulls the last call with the person getting it, then drafts "Hey [name]! Here's [the thing]. Quick rundown:" with four to six plain bullets and a casual close, plus a short "before you send" list of anything sensitive. Use when the user says "/rundown", "bullets I can send along to [person]", "as I pass this over to them", "give them the rundown on what it is and how to use it", "a handful of bullet points to deliver with it", "tldr I can send via Slack", "brief note to go with this", or "match the bullets you wrote for the last one". Never sends anything.
category: Customer Success
---

# /rundown

The work is done. Now it has to land with the person getting it, and the note that goes with it decides whether they open it. The note has the same shape every time: a friendly hello, what the thing is and where it lives, a quick rundown in plain bullets, and a close that says where it is still soft. This skill writes that note from the deliverable itself, tuned to how the last conversation with that person ended.

Siblings: `/source-check` checks the deliverable before it ships. `/rundown` goes out with it. `/direction` handles the client's revisions after.

## When to use
- The user is about to share a deck, a tool or dashboard link, a doc, a spreadsheet, or a folder of files with a client, a partner, or a teammate
- They ask for "bullets to send along," "the rundown," "a tldr for Slack," or "a note to go with this"
- They ask to make a new note "match" one from earlier

## When not to use
- Recapping what a call agreed to
- Answering something someone sent
- Briefing a contractor to build something new from scratch. Write that as an invite to collaborate, not a work order.
- A long explainer or a doc of its own. This is the note, not the deliverable.

## Inputs
1. **The deliverable.** The file, deck, doc, or live URL. Open it and read what is in it now. If it is a tool, load it and click through the main controls. If it is a folder, list every file in it.
2. **The person getting it.** Whatever contact and account notes the project keeps. Note the channel they use (Slack, Teams, email).
3. **The last conversation with them about this work.** The meeting notes or transcript from whatever tool the team records with. Pull what they asked for, what was promised, and any objections they raised. If the user says the context was a few minutes at the end of the call, read the end of the call.
4. **The user's own opener, if they wrote one.** When they paste an intro line ("Hello! Here's a look at what a refreshed strategy could look like. It's dense, so here's the tldr:"), keep it word for word and write the bullets to match it.
5. **The last rundown they approved,** if one exists in the same client folder or this session. Match its shape unless they ask for something different.

## Workflow

**1. Read the thing being sent, not the conversation about it.** Bullets describe what is in the file today. Earlier drafts, rejected versions, and how the work got built stay out. If the numbers in the deliverable changed during the session, use the final ones.

**2. Pull how the last call ended.** One line to yourself: what this person is expecting to see. If the user promised "the next version will look a lot closer," the note should show that promise was kept. If the person pushed back on a number, the bullet that covers that number says where it landed.

**3. Load the voice.** Use the user's style guide if they keep one. The note should read like a Slack or Teams message from a person.

**4. Draft in the shape below.** Keep it to four to six bullets. Each bullet is one or two plain sentences. No bold labels at the front of bullets ("What it is:", "Sliders:"), no headers, no sub-bullets. Cover, in whatever order reads best for this deliverable:
- What it is and what it shows, in words the recipient would use
- How to use it, if it is a tool (the two or three controls that matter)
- The findings or numbers that matter most, if it is a deck or doc
- What changed since the last conversation
- Where it is still an estimate, a baseline, or a snapshot

**5. Check every claim bullet for the real reason.** When a bullet says why something is in or out, make sure the reason is the right one. A break-even ("one deal pays for it") is not the same as the reason ads were left out of the projections. If you are not sure of the reason, ask the user in one line.

**6. List the "before you send" checks under the draft.** Only real ones, one line each:
- Competitor or person names that appear in writing for the first time
- Dollar figures or recommendations the recipient's team has not seen yet
- Comp, salary, fee, or margin data, even when it can be backed into
- Files in a package that should not go (a transcript with candid notes on a person, another client's work)
- Passwords and sign-in links: send separately, and say if a link expires
If there are none, leave the section out.

**7. Show it and stop.** Never send to Slack, Teams, email, or anywhere else. Wait for "send," and even then the user usually pastes it themselves.

**8. Take their edits as the new template.** If the user rewrites a bullet, use their wording in the final version, not a cleaned-up version of it. If they ask for "more casual," cut the labels and the length first, then loosen the phrasing.

**9. Save it.** Write the approved note to the client folder so the next rundown can match it.

## Output format

```
Hey [Name]! Here's [the thing] [from our last call / we talked about]. [Where it lives: link, or "I attached two files: ..."]

Quick rundown:

- [What it is and what it shows]
- [How to use it, or the first finding that matters]
- [Next finding or control]
- [What changed since we talked]
- [Where it stands today, one number if there is one]

[One or two sentences: what is still an estimate or a snapshot, then an open invite, like "Let me know what feels off and we can keep tuning it."]

---

Before you send:
- [Only real checks, one line each]
```

If the deliverable is dense, this opener works: "Here's a look at [the thing]. It's dense, so here's the tldr:"

Rules:
- Four to six bullets. Eight is too many; cut the weakest.
- Plain bullets, no bold lead-ins. Bold only in the "before you send" list.
- Contractions. "Here's," "it's," "they've."
- The close invites. It does not assign a next step to the recipient.
- Follow the house style guide if there is one.

## Where output goes

The approved note goes in the client's project folder as `rundown-<deliverable-slug>.md`.

## Failure modes, from real corrections

| What went wrong | The fix |
|---|---|
| Eight bullets with bold labels ("What it is:", "Sliders:", "Next step:"); the user asked for "more casual, simple, clear, approachable" | Four to six plain bullets, no labels, an invite instead of a next-step bullet |
| A second note to the same person opened and closed differently from the one approved two days earlier | Read the last approved rundown first and match its opener, "Quick rundown:" line, and close |
| A bullet gave the break-even as the reason something sat outside the projections | Check each "because" against the reasoning in the deliverable |
| A package got a separate cover note, and a transcript with candid notes on a person was in the folder | The note goes in the channel, not inside the package; list every file and flag the sensitive ones |
| A bullet described how the tool works inside ("Scores each event by...") and the user said it didn't sound like them | Say what the thing does for the recipient, in their words |

## What good looks like

- First thing I check that most people skip: the last approved rundown to the same person. A second note that opens and closes differently from one approved two days earlier reads as written by someone else.
- The mediocre version is eight bullets with bold labels and a next-step bullet. Four to six plain bullets and an invite instead.
- I know the note is right when every bullet says what the thing does for the person receiving it, in their words, rather than how it works inside.
- Every "because" in the note is checked against the reasoning in the deliverable itself, not supplied from memory.

## Why this exists

The note that goes with finished work decides whether anyone opens it, and it gets rewritten from scratch every time. This skill writes the same short note every time, from the deliverable itself and the last conversation with the person getting it.
