# Routing, seats and reporting

Open this on every review, after setup is done. It decides which seats run, what each seat may judge, and the order the findings are reported in.

## Routing

Work the play out from what the user hands over. Do not make them pick a seat. Say in one line which seats ran and why.

| What the user hands over | Play | Seats to run |
|---|---|---|
| A topic, keyword or brief, **no draft yet** | Brief | `cold_skeptic`, `unresolved_questions` **only**, no verdict |
| A top-of-funnel draft (blog, social post, ad, cold opener, homepage) | Gate | `objector`, then `cold_skeptic` |
| A close-stage draft (proposal, offer page, pricing, late-sequence email) | Gate | `objector`, then `decider` |
| A full sequence, or a page spanning stages | Gate | `cold_skeptic` on the opening, `decider` on the close, `objector` throughout, reported **separately** |
| Two or more variants | Choose | `cold_skeptic` on the differing unit only, then **pre-register** |
| A live URL plus a metric complaint | Diagnose | `objector` on the live copy + `cold_skeptic` `unresolved_questions`, paired with the user's real analytics |
| Anything about existing clients: retention, expansion, delivery | Retention | `client` |
| Ambiguous | Gate | `objector` + `cold_skeptic`, and say that is what was assumed |

**`objector` runs in every play except Brief.** It is the seat the user would never think to ask for and the one that carries most of the value. Infer the funnel stage from what the asset actually does, not from what it is called. Never blend seats into one verdict: the disagreement between them is the output.

### Play notes

- **Brief.** The returned questions are the outline: the piece answers them in the order they are felt. Better than a keyword outline, because it is what the reader wants answered, not what a tool says gets searched.
- **Gate.** Lead with `stopped_reading_at` and `strongest_objection`; fix those two. If the user waves the objection off without a reason, say plainly that the run produced nothing.
- **Choose.** Feed the seat the differing unit *in isolation*: two openers, not two whole posts. Then **pre-register**: if a real outcome is coming (an A/B test, a send, a title change), append the prediction to `predictions.jsonl` with `truth_winner: null` BEFORE the result exists. When the result lands, fill it in and run `python3 references/score.py`. Never skip it; it is the only way to learn whether the panel is right.
- **Diagnose.** The panel explains *why* an observed pattern happened. It never invents the pattern. Get that from real behaviour (analytics, reply rates, sales data).

`predictions.jsonl` lives in the skill folder, one JSON object per line:

```json
{"id": "2026-11-03-subject-lines", "date": "2026-11-03", "question": "...", "variants": ["A text", "B text"], "panel_pick": "A", "truth_winner": null, "metric": "open rate", "notes": ""}
```

## The seats

| Seat | Built from | Judges | Never |
|---|---|---|---|
| `cold_skeptic` | Problem and failed-solution quotes, Problem Aware, from sales calls and interviews | Does this land with no prior exposure | Buying, pricing, post-sale |
| `objector` | Objection and failed-solution quotes from sales calls | What makes them stop reading | Whether they would ultimately buy |
| `decider` | Most Aware objections and decision triggers from sales calls | Does close-stage copy resolve the last objection | Top-of-funnel resonance |
| `client` | Current-client calls | Post-sale reality only | **Any acquisition copy, ever** |

Run `python3 references/panel.py seats` for live sizes. A seat flagged too thin cannot judge anything until more quotes are added. Say so rather than running it.

**Seats are not characters.** Never give one a name, a backstory, a mood, or a biography. The moment it becomes a person it improvises to fill gaps, which is the failure this skill exists to prevent.

## Persona

Personas are the groups in `references/profile.json`. Map from what the asset says about its reader, not from who the user wishes were reading. If unsure, run unfiltered; the widening ladder drops persona and says so, which beats a wrong persona.

## Output files

All paths are relative to the skill folder.

| Path | Who reads it | What it holds |
|---|---|---|
| `data/quotes/<source>-<YYYY-MM-DD>.jsonl` | `build_corpus.py` | Verbatim quotes extracted from one batch of transcripts, one tagged quote per line (codebook in `references/setup.md`) |
| `data/corpus.json` | `panel.py`, `validate_verdict.py` | The merged, de-duplicated corpus; rebuilt only by `build_corpus.py`, never hand-edited |
| `runs/<YYYY-MM-DD>-<slug>/pack-<seat>.json` | `validate_verdict.py`, the user | The evidence pack one seat retrieved for one review |
| `runs/<YYYY-MM-DD>-<slug>/verdict-<seat>.json` | The user | The validated verdict for that seat |
| `predictions.jsonl` | `score.py` | One line per pre-registered prediction |
| `references/profile.json` | This skill | Setup answers; written by setup, updated by `build_corpus.py` |

## Reporting order, inverted on purpose

1. **`density_band` / `dropped`**: thin means weak signal; widened means not persona-specific.
2. **`age_mix.flag`**: a STALE slice describes what buyers said, not what they say now.
3. **`strongest_objection`**: the most useful field in the document.
4. **`unresolved_questions`**: second most useful.
5. **`verdict.answer`**: last, and most suspect. It tends to agree with whoever wrote the draft, because the draft came from the same instincts.

`distinct_calls` is the honest denominator: 12 quotes from 3 calls is not 12 data points. Watch `source_mix` for client-side creep. If client calls keep getting added, a pre-sale seat filling with them means the corpus is drifting toward your own language.

## When not to run it

- When the user has already decided and wants backing. This is not a second-opinion service.
- On every draft. Reserve it for assets that get spent on, or the dissent becomes noise and gets ignored on the one that mattered.
- On a stage the corpus barely covers, without saying so.

## What a passing verdict still does not prove

The gate proves the evidence exists and was retrieved. It cannot prove the *inference* is sound: a verdict can cite four real quotes and reason wrongly from them and still pass. Only `score.py` on real outcomes catches that, and it is underpowered until roughly 30 scored predictions. **Until then, say out loud that these are well-sourced opinions, not calibrated predictions.**
