---
name: email-voice-setup
title: Email voice setup
description: |
  Use this skill when someone wants their AI to draft emails that sound like
  them, and the drafts it writes today read as AI-written or get rewritten
  line by line before they go out. Produces a personal email-voice skill built
  from the person's own sent mail and their own edits: a register map, rules
  backed by counts and quoted lines, three test drafts, and a routine that keeps
  it improving. Also use for "write emails in my voice", "make my drafts sound
  like me", "my AI emails sound like a robot", "build my email style guide",
  "teach my assistant how I write".
category: Operations
tags: [email, writing-voice, ai-drafting, style-guide, client-communication]
---

Applies when a person's AI-drafted emails need heavy editing before they send them. Produces a voice skill the person owns, built from evidence in their own outbox rather than adjectives about their style.

## The play

1. Ask permission and set the scope. Agree which mailbox, which date range, and that everything read stays in the user's own files. Confirm the user's address so only mail they wrote gets counted.
2. Pull the sample: 30 to 40 substantive sent emails from the last one to two months, spread across the kinds of people they write to. What to skip and how to spread it is in references/measurement-checklist.md.
3. Collect the rewrites: any AI draft the user edited before sending, with both versions. Diff each one with references/rewrite-diff-worksheet.md. What they cut is the strongest signal in the whole build.
4. Count before describing. Run the measurement checklist across the sample and write every finding as a number. "Warm" is not a finding. "One to three exclamation points in 37 of 40 emails" is.
5. Reconcile the two sources. The sent mail wins on how often something happens. A rewrite wins for the kind of email it came from. Scope every rule to the register it came from, or one client email ends up setting rules for every vendor note.
6. Interview for what the mail cannot show. Ask about ten questions from references/interview-questions.md, three or four at a time, and play back what you heard before moving on.
7. Build the register map: one row per kind of recipient, with median length, warmth, greeting, closer and exclamation range. Most people have five to eight. Record the real median length, not the one the user describes.
8. Write the skill from references/voice-skill-template.md and save it in the user's own skills folder. Every pattern carries its count and one quoted line from their mail.
9. Test it on real mail. Pick three emails the user owes, each in a different register. Draft them with the new skill loaded, have the user mark them up, and fold each fix back in. Stop when the edits are small.
10. Set up the loop. Every future rewrite gets diffed and becomes a pattern, not just a log line. Re-sweep the sent mail once a quarter.

Branches:
- Under 20 usable sent emails (new role, new mailbox): build from the rewrites and the interview, mark every rule provisional, and re-sweep at 30.
- Someone else writes part of their mail (an assistant, a shared inbox): exclude it, and ask the user which threads are theirs.
- They write in two languages: one register map per language. Habits rarely carry across.

## What good looks like

- First thing I check that most people skip: the length distribution. People describe their emails as longer and more careful than they are. A fifth are often under 50 words, so a skill that defaults to the 300-word email writes the top tenth of their mail.
- The mediocre version: a list of adjectives ("friendly, direct, professional") written from the user's self-description, plus rules from one rewrite applied to every email. It produces drafts that sound like a nicer AI.
- I know it is right when the user sends a test draft with only small edits, and every rule in the skill can point to a count or a line they actually wrote.
- Red flag: a draft more polished than their real mail. Typos, run-on sentences and asides are part of the voice. Smoothing them out is how a draft starts reading as AI-written.

## Rules

- MUST ask before reading any mailbox, and keep the sample and the finished skill in the user's own files.
- MUST count only mail the user wrote themselves.
- MUST back every rule with a count or a quoted line, and name the register it applies to.
- MUST write into the finished skill that it creates drafts only and never sends.
- MUST write into the finished skill that a reply stays in its original thread.
- MUST write into the finished skill that it never inserts a link or claims an attachment it has not verified, and leaves a visible placeholder instead.
- NEVER describe the voice from the user's self-description alone.
- NEVER polish out the user's real habits.
- NEVER keep other people's private details in the finished skill beyond what an example needs. Strip names before the skill is shared with anyone.
