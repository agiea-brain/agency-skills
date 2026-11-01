# icp-review setup

Run this once, with the user, before the first review. It takes one sitting: about 10 minutes of
questions, then however long it takes to read the transcripts. Paths are relative to this skill's
base directory.

**The goal:** a corpus of real, verbatim things buyers said, each tagged so the four seats can
slice it. The panel is only as honest as this corpus. Never pad it with invented or paraphrased
quotes to make a seat look fuller. A thin seat that says "I can't judge this" is working correctly.

## Step 1: Ask the setup questions

Ask these one or two at a time, in plain language. Write each answer into `references/profile.json`.

| # | Question | Goes into |
|---|---|---|
| 1 | What's your company called, and what do you sell, in one sentence? | `company`, `offer` |
| 2 | Who buys it? Their job title, and what kind of company they work at. | `buyer` |
| 3 | How do your buyers split into groups that think differently? Two to six groups, by size, industry, or situation (e.g. "Owner-led, under 20 staff", "Multi-location group"). | `personas` (exact labels, used as tags) |
| 4 | Where do your conversations with buyers live? (Granola, Fathom, Gong, Zoom or Teams transcripts, a folder of documents, interview notes.) Roughly how many calls? | `transcript_sources` |
| 5 | Which of those are sales or discovery calls, which are calls with current clients, and which are other conversations with your kind of buyer (podcast guests, research interviews)? | used to tag `source_type` |
| 6 | Optional: problems you hear over and over, in a few words each. Up to ten. | `patterns` |
| 7 | Do you have a positioning doc, message guide, website copy or sales script? List them; the panel must never read these as evidence. | `excluded_docs` |
| 8 | Can any buyer quote ever be used in public? Default: no, internal judgment only. | `public_quote_rule` |

Then replace every `{{COMPANY}}` in `references/seats.json` with the company name.

**Minimum to be useful:** about 20 sales or discovery calls. Fewer works, but most seats will come
back "thin" or "insufficient" and say so. If the user has fewer than 10 sales calls, tell them
plainly before starting that the panel will mostly decline to judge until more calls are added.

## Step 2: Get the transcripts

Use whatever the user named in question 4: a connected meeting-notes tool (search the available
tools for its own verbs, like `list_meetings` or `get_meeting_transcript`, before saying it is not
connected), a folder of files, or pasted text. Work in batches of 10 to 20 calls.

Skip a call entirely if the buyer barely speaks or it is not with your kind of buyer.

## Step 3: Extract and tag quotes

Read each transcript and pull out the **buyer's** words, never the user's own words, never a
teammate's. Take quotes that show what the buyer struggles with, wants, tried, doubts, or needs to
decide. Copy them **verbatim**: trim filler words and false starts, but never reword. A good call
yields 5 to 15 quotes; a weak one, zero.

Create `data/quotes/` in the skill folder if it is missing (`mkdir -p data/quotes`), then write one JSON object per line to `data/quotes/<source>-<YYYY-MM-DD>.jsonl` (for example
`data/quotes/gong-2026-11-03.jsonl`). One file per batch; never edit an older batch file.

```json
{"quote_key": "gong:8812734#3", "quote": "We tried two vendors before and both disappeared after month two.", "stance": "failed-solution", "stage": "Problem Aware", "persona": "Owner-led, under 20 staff", "pattern": "Vendors vanish", "topic": "past vendors", "source_type": "discovery-call", "confidence": "high", "date": "2026-09-14", "public_ok": false, "provenance": {"recording_id": "8812734", "call_title": "Discovery call"}}
```

### Codebook

| Field | Required | Values |
|---|---|---|
| `quote_key` | yes | `<source>:<call id>#<n>`: lowercase source name, the call's own ID from the tool, and the quote's number within that call. Must be stable: re-extracting the same call must produce the same keys. |
| `quote` | yes | Verbatim buyer words. |
| `stance` | yes | `problem` (a pain they have) · `desire` (an outcome they want) · `failed-solution` (something they tried that didn't work) · `objection` (a doubt or reason not to buy) · `proof` (evidence that would convince them) · `decision-trigger` (what makes them act now) |
| `stage` | yes | Where the speaker is at that moment: `Problem Aware` (feels the pain, not shopping) · `Solution/Category Aware` (knows the kind of fix exists) · `Product/Brand Aware` (comparing specific options, including yours) · `Most Aware` (deciding whether to buy from you) |
| `source_type` | yes | `discovery-call` · `sales-call` · `client-call` (anyone already paying you) · `interview` (your kind of buyer, not in a buying conversation) |
| `confidence` | yes | How sure you are of the tags: `high` · `med` · `low` |
| `persona` | no | One of the exact labels in `profile.json` `personas`, or leave it out if unclear. Never guess. |
| `pattern` | no | One of `profile.json` `patterns`, or leave it out. |
| `topic` | no | A few words on what the quote is about. |
| `date` | no, but strongly wanted | Call date, `YYYY-MM-DD`. Undated quotes can't be checked for staleness. |
| `public_ok` | no | `true` only if the user's rule in question 8 allows it. Default `false`. |
| `provenance` | no | `recording_id` (or `doc_id`) and `call_title`. The panel uses `recording_id` to count distinct calls, so include it. |

**Tagging rules that matter most:**
- The same person can be `Problem Aware` early in a call and `Most Aware` at the end. Tag the moment.
- An objection from a current client is about the work, not about buying. It is `client-call`,
  never `sales-call`.
- When unsure between two stances, pick the one that would change what the copy should say, and set
  `confidence` to `med`.

## Step 4: Build and check

```bash
python3 references/build_corpus.py
python3 references/panel.py seats
python3 references/test_gate.py
```

- `build_corpus.py` rejects any row that breaks the codebook and writes nothing until every row
  passes. Fix the rows in the batch file and rerun.
- `panel.py seats` shows how big each seat is. Under 12 means that seat can't give a full verdict
  yet. Tell the user which seats are thin and what kind of calls would fill them (for `decider`:
  late-stage sales calls; for `client`: client calls).
- `test_gate.py` must print `ALL 11 TESTS PASS`. It needs at least 6 quotes in the `objector` seat.

## Step 5: Finish

Set `setup_complete` to `true` in `references/profile.json`. Tell the user, in two or three sentences:
how many quotes from how many calls, which seats are ready, which are thin, and that they can now
say `/icp-review` and hand over a draft.
