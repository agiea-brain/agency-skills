---
name: youtube-transcript-panel-pull
title: YouTube transcript panel pull
description: |
  Use this skill when you need the words from a YouTube video as text: your own
  episode or webinar to repurpose, or a prospect's talk or podcast appearance to
  prepare for a call. Produces one timestamped .txt transcript per video.
  "Get the transcript of this video", "pull captions from my channel",
  "what did they say on that podcast".
category: Marketing
tags: [transcripts, content-repurposing, call-prep, browser]
tools: [youtube]
---

Applies when someone needs a YouTube video's spoken words as text. Produces one timestamped transcript file per video.

The reliable route is the transcript panel on the watch page, read by the agent in a browser. It works on public videos without signing in.

## The play

1. Collect the video IDs. For one video, take the `v=` value from the URL. For a channel, open its Videos tab and collect the IDs from the page links (snippet in `references/browser-snippets.md`). Skip Shorts and IDs you already have.
2. Open each watch page. Pause the video, expand the description, then click "Show transcript". The button lives inside the description, so it does not exist until the description is expanded.
3. Wait a few seconds, then read the transcript rows. Each row has a timestamp and a text span. Join them as `[m:ss] text`.
4. Get the text off the page through a temporary textarea and a copy command. Return the row count and the first and last rows, check the clipboard matches, then write the file. This keeps a long transcript out of the agent's context.
5. Zero rows usually means the panel hasn't loaded; it can also mean no captions or changed markup. Retry once, then report which; never save an empty file.
6. Save one file per video with a short header: video ID, title, language and whether the captions are auto-generated. Read the language and caption type from the page; don't assume them.
7. When pulling a batch, check that the counts agree: IDs collected, files written, unique IDs on disk.

Open `references/browser-snippets.md` for the exact selectors and the copy snippet.

## What good looks like

- First check: the row count. A real 30-minute episode returns hundreds of rows; a handful means the panel was still loading, or you grabbed a chapter list instead.
- The mediocre version calls YouTube's caption endpoint directly. Without a session token it now returns an empty body, so the agent reports success on blank files.
- The other mediocre version pastes the whole transcript into the chat to save it. It works once, then burns the agent's context on the second video.
- The output is right when every file has rows, the batch counts agree, and a spot-checked timestamp in the file matches the video at that moment.

## Rules

- MUST read the transcript panel, not the caption endpoint.
- MUST refuse to save a file with zero rows.
- MUST label auto-generated captions as auto-generated; speakers are not identified in them.
- NEVER quote a transcript line as a person's exact words without checking it against the audio. Auto-captions mishear names, numbers and jargon.
- NEVER pull a private or members-only video the reader has no right to.
