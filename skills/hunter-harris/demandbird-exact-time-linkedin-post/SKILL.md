---
name: demandbird-exact-time-linkedin-post
title: DemandBird exact-time LinkedIn post
description: |
  Use this skill when an approved LinkedIn post (text, image or PDF carousel)
  must go out at a specific minute through DemandBird. Produces a scheduled post
  whose stored copy, time and media match what was approved, confirmed by one
  read-back. Uses DemandBird's MCP server. "Schedule this post for Tuesday 10am",
  "queue the carousel", "schedule the week's LinkedIn posts".
category: Marketing
tags: [scheduling, content-distribution]
tools: [demandbird, linkedin]
---

Applies when approved LinkedIn copy has to land at an exact time, often for a client or a launch. Produces a scheduled DemandBird post that matches the approval, with the read-back saved as proof.

Needs DemandBird's MCP server connected with a token scoped to drafting and scheduling. Leave deletion out of the token.

## The play

1. Call `list_connected_accounts` and `list_scheduled_posts`. Take the LinkedIn account ID from the result, never from memory, and check nothing is already queued in that slot.
2. Save the approved copy verbatim with `save_draft`: `content`, `platforms: ["linkedin"]`, the account in `platform_account_ids`, and any media in `images`. Don't run it through a drafting or voice tool; that rewrites approved copy.
3. For a PDF carousel, set the document `title` explicitly. Otherwise LinkedIn shows the filename.
4. Call `schedule_post` with the post ID, `scheduled_at` as ISO 8601 with the UTC offset for that date, and `variance_minutes: 0`. Without the zero, the account's default jitter moves the time.
5. Call `get_post` once. Compare it with the approved file: copy (only a trailing newline may differ), time, media and status. Save that read-back. Don't poll.
6. Record the post as scheduled with its ID and time. There is no public URL until it publishes; fill it in afterwards.

Media and first-comment quirks, and the rate-limit behaviour, are in `references/demandbird-quirks.md`. Open it before a batch.

## What good looks like

- First check: the stored time and variance. A post "scheduled for 3pm" that stores a window instead of 3:00 never had its variance set to zero.
- The mediocre version loops `save_draft` over a week of posts. The first rate-limit rejection doesn't stop the loop, and every later call fails or, worse, half-succeeds.
- The output is right when each read-back matches the approved copy byte for byte (bar the trailing newline), the time is exact in the offset for that date, and there is exactly one post per slot.

## Rules

- MUST have approval for the copy, media, account and dated time of every post, batch rows included; save the copy verbatim.
- MUST set `variance_minutes: 0` when the time matters.
- MUST stop a batch on the first rejection, wait, and reconcile with `list_scheduled_posts` before retrying. A rejected write doesn't prove nothing was created.
- NEVER mark a first comment verified from `get_post`; it doesn't return them.
- NEVER give the agent a token that can delete posts or manage channels.
