# Record shapes

All files sit in the corpus folder on the owner's machine, except the pass files, which sit in the agent's own settings folder. Addresses below are placeholders.

## Corpus record

One per line in `corpus.jsonl`:

```json
{"id": "gmail:3f9a0c1d2e4b5a6c", "source": "gmail", "channel": "email",
 "date": "2026-10-26T10:15:00-04:00", "to": ["client@example.com"], "to_kind": "client",
 "subject": "Re: Plan", "thread_before": "the previous message, up to 600 characters",
 "text": "the owner's words only", "words": 54, "ingested": "2026-11-01T15:52:00+00:00"}
```

`source` is gmail, slack, linkedin or text. `channel` is email, dm, channel, post, comment or text. `to` holds addresses for email, names for direct messages, `#name` for a chat channel, and `public` for posts and comments.

## Add list

The input to `ingest --add`, a JSON list. Only source, channel, date and text are required. The full body may be pasted; it is cleaned the same way.

```json
[{"source": "gmail", "channel": "email", "date": "2026-10-31T14:02:00-04:00",
  "to": ["client@example.com"], "subject": "Re: plan", "thread_before": "their message",
  "text": "the full body as sent"}]
```

## Recipients

`recipients.json`, a flat map from an address, an `@domain` or a name to a kind: client, peer, vendor, friend, prospect, public or unknown. Keys starting with `_` are comments.

```json
{"client@example.com": "client", "@example.com": "client", "Sam": "vendor"}
```

## Pass file

`voice-pass/<sha256>.json`, the hash taken over the normalised text. `latest.json` adds `head`, the first 200 characters.

```json
{"ts": "2026-11-01T15:52:00+00:00", "epoch": 1793548320.0, "sha": "...", "tier": "FLAG",
 "to": ["client@example.com"], "channel": "email", "kind": null}
```

## Saved draft

`drafts/<YYYY-MM-DD>_<sha8>.json`:

```json
{"text": "...", "to": ["client@example.com"], "channel": "email", "kind": "client",
 "ts": "2026-11-01T15:52:00+00:00"}
```

## Pair

One per line in `pairs.jsonl`. `result` is unchanged, changed or superseded.

```json
{"draft_id": "2026-11-01_3f9a0c1d", "sent_id": "gmail:...", "to": ["client@example.com"],
 "date": "2026-11-01T16:20:00-04:00", "draft": "...", "sent": "...", "result": "changed",
 "overlap": 0.82, "changes": [["<your phrase>", "<their phrase>"]]}
```

## Swap

One per line in `swaps.jsonl`:

```json
{"my_phrase": "<your phrase>", "owners_phrase": "<their phrase>", "count": 2,
 "first_seen": "2026-10-31", "last_seen": "2026-11-02"}
```

## Held-out test

Items, answers and results, in `eval/`:

```json
{"date": "2026-11-02", "items": [{"item_id": "e1", "to": ["client@example.com"],
  "channel": "email", "kind": "client", "thread_before": "..."}]}
{"date": "2026-11-02", "answers": {"e1": {"record_id": "gmail:...", "date": "...",
  "text": "...", "words": 87}}}
{"date": "2026-11-02", "items": [{"item_id": "e1", "facts": ["..."], "draft": "...",
  "real": "...", "real_was": "A", "judge_pick": "B", "judge_correct": false}]}
```

In results, `item_id`, `draft`, `real` and `judge_correct` are required. `judge_correct` is true when the judge picked the owner's real text.

## Metrics

One line per scored date in `metrics.jsonl`:

```json
{"date": "2026-11-02", "n": 5, "judge_accuracy": 0.6, "length_ratio": 1.12,
 "drafts_blocked": 0, "block_hits": 0, "corpus_records": 1243, "swaps_applied": 3,
 "scored_at": "..."}
```
