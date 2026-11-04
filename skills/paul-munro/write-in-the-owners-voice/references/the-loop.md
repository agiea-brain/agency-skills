# The loop

The system improves every night from two signals that need nothing from the owner: everything they send, and the difference between your draft and what they actually sent. It runs inside a scheduled early-morning run on weekdays.

## The nightly order

1. Read yesterday's sent mail and chat messages through the connectors. Write them to a dated file in the corpus inbox, in the list shape in json-shapes.md.
2. Add them to the corpus:
   ```
   ingest --add INBOX/<date>_sent.json
   ```
   The same script also reads a mail export (`--mbox`), a chat export folder (`--slack-json`) or a social network data export (`--linkedin-dir`).
3. Match drafts to sent messages:
   ```
   reconcile
   ```
4. Pick the held-out items:
   ```
   evaluate sample --n 5
   ```
5. Do the agent's part of the test, below.
6. Score it:
   ```
   evaluate score <date>
   ```
7. Mondays only, the one-line summary:
   ```
   evaluate report
   ```

## Reconcile and swaps

Reconcile takes each saved draft from the last seven days and looks for the message the owner sent: same recipient, sent within 72 hours of the draft, sharing at least 5 distinct words that make up at least half of the shorter text's distinct words.

- A draft sent unchanged is recorded as a pass.
- A changed draft yields swaps. Each short stretch the owner replaced or cut becomes a swap: your phrase, their phrase. A swap is counted every time it recurs, and the check applies any swap seen twice or more.
- Several saved drafts of one note (same recipient, within 72 hours of each other, overlapping above the same floor) count as one note. Only the newest is matched. The earlier ones are recorded as superseded and never become swaps. Without this rule, your own successive rewrites get written up as the owner's corrections.

A correction the owner gives you directly goes into the swaps file the same turn, so it does not wait for the nightly match.

## The held-out test

Sample picks five messages the owner sent in the last 90 days. The same date always gives the same pick. A message qualifies when it has 15 to 400 words, passes the hard rules, was not used in an earlier test, and has at least two other messages to the same recipient (or of the same kind and channel), so the drafting side has examples to work from. It writes two files: the items the drafting side may see, and the answers, for the facts step and the scorer only.

Your part, for each item:

1. **A facts step** reads the answer and writes the bare facts as a short list: who, what, dates, numbers, the ask. Never the wording.
2. **A drafting step** that never sees the answer runs `examples --to ... --channel ... --exclude-eval <date>` and drafts from the facts and those examples. `--exclude-eval` leaves the held-out messages out, so a draft never sees its own answer.
3. **A separate model, the judge,** gets the draft and the real text as A and B in random order and guesses which one the owner wrote.

Write the results file, then score. The score gives the judge's accuracy, the length ratio and the hard-rule blocks, and keeps the trend. A judge accuracy of 0.5 means it cannot tell the two apart. That is the goal.

## Tests

Every script takes `--corpus DIR` to work on another folder. Test every change on a scratch folder, never on the real corpus.
