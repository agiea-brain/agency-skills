---
name: direction
title: Builder direction note
description: Turns client or stakeholder feedback on something already built (a staging page, a deck, a PDF, a mockup) into a numbered change note for the person who builds it (designer, developer, editor). Reads the feedback and the live thing, sorts each comment by what it changes for the user to confirm, finds every other place the same line or number appears, and writes "Hey [builder], [client] went through [the thing]..." with exact old and new copy, grouped by asset, and a closing ask for timing. Use when the user says "/direction", "translate this into direction for [builder]", "help me pass this along to [builder]", "what do I need to pass along to the designer", "write this as a note to [builder]", "[client] also sent this", "create a task for [builder] for [person]'s request", or pastes a client email of revisions and asks what changes. Never sends anything.
category: Operations
---

# /direction

A client sent revisions on something the builder already made. The user has to turn a loose email ("can we make the chart pop more?", "combine the three middle bullets") into a note the builder can work straight down without calling them. The builder should never have to read the client's email, guess what "the PDF" means, or hunt for the other five places the old line lives.

One output: the builder note. The user's own read of the feedback stays in chat and stays short.

Siblings: `/work-review` is the user judging what a teammate built. `/rundown` goes out with finished work. `/direction` sits between the client's feedback and the builder's next pass.

## When to use
- "/direction", "/direction homepage revisions"
- "the client's feedback on the resources page. help me figure out next steps and what I need to pass along to the designer"
- "can you translate this into direction for the developer?"
- "[client] also sent this re: the sales deck" (a follow-up to a note already written)
- "create a task for the designer for [person]'s request, translate it as you see fit"
- "question from the developer on the last round" (the builder asked something about earlier direction; answer it as a short direction note)

Not this skill: the user wants to answer the client, or the user is reviewing the build with no client feedback in hand (`/work-review`).

## Inputs
1. **The feedback,** pasted or forwarded: client email, Slack thread, doc comments, a call transcript, or a mix. Several people's feedback on the same thing goes into one note.
2. **The thing being changed:** staging URL, slides or doc link, PDF in the client folder. If the user did not give it, find it in the client's recent work or the last note to the same builder.
3. **The builder's name and channel** (email, Slack, project task). Default from the client's account notes.
4. **The last note to this builder on this asset,** if one exists, so numbering, wording, and open items carry over.

## Workflow
1. **Load the client.** Read the client's account notes, including any decisions already made, and their recent work. Find the most recent note to the same builder. If an item from the last note is still open, carry it, do not repeat it as new.
2. **Open the real thing.** Load the staging page, open the deck or doc, open the PDF. Note slide numbers, section names, and card titles exactly as they appear. Never write direction off the client's description of the page alone.
3. **Sort every comment** into one of four buckets, in chat, in a short table:
   - **Change**: clear enough to do. Write the exact edit.
   - **Builder's call**: a design ask with no single right answer ("make it stand out more"). Give one idea and say the builder is the better judge.
   - **Decide first**: needs a fact, a number, or copy the user has to get or approve. Name what is missing and from whom. The note tells the builder to hold that piece.
   - **No change**: already done, out of scope, or the user disagrees. Say why in one line. These stay out of the builder note.
   Ask the user about the "Decide first" items, one question at a time. Sort everything else yourself and show the table above the note, so the user can move any comment before the note goes anywhere.
4. **Find every copy.** For each changed line, number, name, or title, search every asset in the client's set for the old wording: site pages, PDFs, decks, articles, and every audience version. List every location in the note. One correction from the client usually lives in three to six places.
5. **Write the note** (format below). Exact old text and exact new text in quotes. Slide and section numbers from the current version, and say so if a new slide will shift them.
6. **Check it.** Every item maps to a client comment or a "find every copy" hit. Nothing invented. No item asks the builder to decide content. Counts match ("in six places" lists six). Then run the user's style guide over the note; it should read like a note to a colleague they trust.
7. **Show it in chat in full** and save it. Do not send, post, or create the task until the user says "send." If they asked for a task, show the task title, assignee, and body first.

## Output format

```
Hey [builder], [who] went through [the thing] and sent [a few / one] change[s]. [One line on size: "Most are small. The bigger ones are X and Y." or "Everything else is approved, so once these are in we're ready to launch."]

[Asset name] ([link])

1. [Slide / section / card]: [what to do, in a plain sentence]. [Exact new copy in quotes when copy changes.] [One line of why, only when the client's reason changes how the builder should do it.]
2. ...

[Next asset name] ([link])

1. ...

[The cross-asset change], in [N] places

[One sentence on what changed and why.] Replace "[old]" with:
"[new]"
- [Asset, exact location]
- [Asset, exact location]

[Close: what to do if something doesn't fit the layout, plus one ask: "Can you give me a rough timeline on these?" or "Let me know once it's in and I'll take a look."]
```

Rules for the note:
- Open with "Hey [name]," and the who and what in the same sentence. No subject-line restatement, no recap of the project.
- Group by asset, then number inside each group. Restart numbering per asset in long notes; run it straight through in short ones.
- One change per number. The location comes first, then the action.
- Quote copy exactly. Never "update the wording to something like."
- Design asks get one idea plus "you're the better judge on this one." Never a pixel spec the user did not give.
- A piece that waits on the user says so and says what to leave in place meanwhile ("leave the number as is until I confirm").
- Short asks stay short. One copy change is a five-line note, not a template.
- No client quotes pasted in bulk. Paraphrase the reason in a few words.
- The builder never sees the "No change" bucket or the user's opinion of the client's feedback.

## Corrections that keep coming back
- The first draft gave recommendations about the feedback, and the user couldn't turn them into a note. Lead with the note. Analysis is three lines in chat at most.
- The note only went into a file. Put the full note in chat.
- One corrected line, every place it lives. A single updated count can sit on the site, two decks, and a set of PDFs. Missing one means a second round with the client.
- The note didn't sound like the user. Run the voice check before showing it.
- Do not add new client questions the user did not ask for. If the feedback raises one, put it in the "Decide first" bucket in chat.

## Where output goes
The client's project folder, as `<asset>-<who>-feedback/<builder>-note.md`. A follow-up from the same round goes in the same folder as `<builder>-note-followup.md`. After the changes ship, add any decision the client made (a new copy standard, a renamed title, a corrected count) to the client's account notes.

## What good looks like

- First thing I check that most people skip: every other place a corrected line lives. One updated count usually sits on the site, two decks and a set of PDFs, and missing one means a second round with the client.
- The mediocre version leads with recommendations about the feedback. Lead with the note; analysis is three lines in chat at most.
- I know the note is right when the builder can work straight down it without opening the client's email or calling to ask what something meant.
- A comment that needs a fact, a number or an approval is held, not guessed at. It goes in "Decide first" and the note tells the builder to hold that piece.

## Why this exists

Client revisions arrive as loose emails, and builders lose hours guessing what "make it pop" means or hunting for the other places an old line lives. Every round that has to be redone is time the agency usually doesn't bill. This skill turns each round of feedback into one note the builder can work straight down.
