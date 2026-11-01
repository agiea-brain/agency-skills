---
name: riverside-short-social-schedule
title: Riverside Shorts social schedule
description: |
  Use this skill when finished vertical clips from a Riverside recording are
  approved and need scheduling to YouTube Shorts, TikTok and Instagram. Produces
  one scheduled post per clip and platform, each read back and checked. Uses
  Riverside's MCP server. "Schedule the shorts", "post the clips this week",
  "fix the shorts schedule".
category: Marketing
tags: [podcast, video, shorts, social-scheduling]
tools: [riverside, youtube, tiktok, instagram]
---

Applies after clips are finished and approved, when they need to go out on a schedule. Produces scheduled posts, one per clip and platform, each verified by reading it back.

Riverside's MCP server (OAuth, signed in once by the human) exposes the social scheduling tools. Five clips on three platforms is fifteen writes, so the procedure is built around never doubling or losing one.

## The play

1. Get approval for everything that goes out: captions, titles, accounts, visibility and times. Scheduling is publishing.
2. Read what is already scheduled, then build the expected-state matrix before any write: one row per clip, platform and account. The columns are listed in `references/expected-state-matrix.md`.
3. Check the matrix. Every caption carries the approved call to action, usually the full-episode link rather than a hosting or bio page, and every time is converted to UTC for that date. Daylight saving moves the UTC hour.
4. Create each row with `social_upload_create`. Include `composeSettings: {}` on the first create. Without it, Riverside rejects an exported clip as "not exported yet".
5. Journal each write as it returns. If a write's result is unknown (timeout, dropped connection), don't retry it. Read the schedule once, then stop and ask.
6. Read every row back with `social_get_upload` and `social_get_upload_status`. Check account, UTC time, visibility, caption, title and source clip against the matrix. A create can return "waiting for greenlight" and read back as "scheduled". Only the read-back counts.
7. Repair only what failed: keep verified rows, write only the missing ones.

## What good looks like

- First check: the caption link. A Short without the full-episode link is reach that leads nowhere.
- The mediocre version fires fifteen creates in a loop, retries the ones that time out, and finds duplicate posts on TikTok two days later.
- The output is right when every matrix row reads back "scheduled" with the right account, UTC time and caption, and the journal shows exactly one create per row.

## Rules

- MUST have approval for copy, accounts and times before the first write.
- MUST read back every post; NEVER report a create response as success.
- NEVER retry a write whose outcome is unknown.
- NEVER cancel and recreate a scheduled post to fix it; edit it, or ask.
- NEVER run two scheduling sessions against the same Riverside account at once; parallel callers hit its rate limit.
