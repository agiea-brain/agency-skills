---
name: linkedin-watchlist-brief
title: LinkedIn watchlist brief
description: |
  Use this skill when an agency wants to track what specific clients, prospects,
  partners or companies are posting on LinkedIn without checking each profile by
  hand. Cleans a list of LinkedIn URLs, learns what kinds of posts matter, runs a
  test, then sets up a daily scheduled task that pulls the last 24 hours of posts
  through Bright Data and delivers a short brief with the posts worth engaging
  with. Also use for "daily LinkedIn digest", "keep an eye on these accounts",
  "what are my clients posting", "watch these LinkedIn profiles".
category: Sales
tags: [linkedin, signals, social-listening, account-monitoring, scheduled-brief]
tools: [linkedin, brightdata, composio, google-sheets]
---

# LinkedIn watchlist brief

This skill does setup. It collects the watchlist, learns what the user cares about, tests one run, then creates a scheduled task. The scheduled task does the daily work in a fresh session with no memory of this conversation, so its prompt has to carry everything it needs. The deliverable is a chat message in that session, not an email or a file.

For an agency, the watchlist is usually the people whose news should change the next conversation: client champions, open prospects, referral partners and the companies behind them.

## Requirements

Bright Data connected through Composio. Confirm the connection before anything else. If it isn't connected or has no active Bright Data account, tell the user what to connect and stop. Never ask for an API token in chat or put one in a prompt, because scheduled task prompts are stored in plain text.

The exact actions, fields and the quirks found in live test runs (async waits, engaged-with posts leaking into profile results, one-off `dead_page` failures) are in `references/bright-data-setup.md`. Read it before the test run.

## Step 1. Collect and clean the watchlist

Accept URLs pasted in chat, an attached CSV (a LinkedIn connections export or Sales Navigator export), or a Google Sheet link. Normalize each:

- Person: `https://www.linkedin.com/in/<slug>/`
- Company: `https://www.linkedin.com/company/<slug>/`
- Strip query strings, fragments, `/recent-activity/...`, `/posts/...`, and locale subpaths.
- Sales Navigator URLs (`/sales/lead/`, `/sales/company/`) can't be scraped. List them back and ask for the public profile URL.
- Drop duplicates. Reject post, search, and feed URLs.

Report counts (people, companies) and any rejects. Don't print the full list back unless asked.

**Where the list lives.** Up to about 75 URLs: embed it in the scheduled task prompt. Larger, or if the user wants to edit it without rerunning setup: a Google Sheet with columns `url`, `name`, `type`, `notes`, read on each run.

## Step 2. Confirm settings (one round of questions)

- **Schedule:** weekdays or every day, and a time in the user's time zone (default 6:45am).
- **Cost cap:** posts per account per run (default 5). Bright Data bills per record.
- **Focus:** what makes a post worth engaging with for them (for example, partnerships, hiring signals, product launches, funding). This drives the top-of-brief picks. Use their words in the task prompt.

## Step 3. Test run

Run the daily procedure in `references/scheduled-task-prompt.md` once, now, on up to 5 accounts. Post the brief in chat. If nothing posted in 24 hours, rerun with a 7-day window so the user can see the format, and label it as a test. Adjust format if asked, then create the task.

## Step 4. Create the scheduled task

Create the scheduled task with your scheduling tool:
- `name`: "LinkedIn watchlist brief"
- `cron_expression`: `CRON_TZ=<user's IANA zone> <min> <hour> * * <1-5 or *>`
- `initiation`: `human_request`
- `notifications`: `{push: true}`
- `prompt`: the template in `references/scheduled-task-prompt.md` with values filled in

Confirm in one line: schedule, account count, and the approval setting the result reports.

To change it later (new URLs, time, focus): find the existing "LinkedIn watchlist brief" task, rebuild the prompt and update it. Don't create a second task.

## What good looks like

- The brief only shows posts the account actually wrote inside the window. Engaged-with posts are filtered out by `only_authored_posts` and a user ID match, because one test returned two of them out of three results.
- "Worth engaging" uses the user's own words for what matters, and is skipped when nothing qualifies rather than padded.
- A failed URL is retried once before it is reported, and an empty result reads as "nothing returned," never "didn't post."
- Red flag: a cost surprise. If the test run suggests a high daily cost, say so before the task exists, and keep the per-account cap modest.

## Rules

- Read-only on LinkedIn. Never comment, react, connect, or message anyone.
- Empty results mean "nothing returned," not "didn't post."
- Keep the account cap modest. If a test run suggests the daily cost will be high, say so before creating the task.
