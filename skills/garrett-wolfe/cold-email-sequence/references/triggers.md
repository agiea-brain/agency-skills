# Time-Based Triggers: Sports, Weather, Calendar and Company Events

Company and behavioral buying signals (visitors, hires, funding, job posts, intent and the rest)
are cataloged with their copy rules in `signals.md`, and events in `conferences.md`. This file covers
real-world time triggers (sports, weather, the calendar) and the freshness rules every trigger
shares.

A trigger is the **why now**. It earns one line, and the next line ties it to the buyer's problem.
The event is the reason for writing today, never the pitch. Researched 2026-10-26.

**Evidence quality:** data sources (NWS, SPC, ESPN, SEC) are solid. Decay windows and "3-5x lift"
claims come from vendors who sell signal data (Autobound, Landbase, FirstSales, Salesforge) and are
unverified. Treat every window as a starting value: tag `trigger_type` and `trigger_age_days`, and
let your own results calibrate them.

---

## 1. Rules for every trigger

1. **One line, then value.** Situational relevance (why this person, why now) beats name-drop
   personalization (Apollo).
2. **Facts come from a stored field, never from the model.** Store `event_date`, `event_source_url`
   and the raw values (score, hail size, county). The AI may phrase them; it never supplies them. A
   judge checks the line's facts appear in the source row before push.
3. **A freshness gate in code.** Block the send if the event is past its window, and re-check
   **in-flight** leads too: follow-up 3 must not mention a 5-week-old win. Aim to send within ~72
   hours of detection; a reference after 3 weeks reads as a stale scrape.
4. **Fallback = drop the line.** Use a two-version template: the base email must stand on its own
   when the trigger is empty or stale. Never let a model fill the gap with a plausible score or
   storm. Spintax can't hide a blank (`ai-lines-and-spintax.md`).
5. **Tone:** congratulate wins, stay neutral on weather, and never joke about or reference losses,
   layoffs, lawsuits, bankruptcies or disasters.
6. **Never send:**
   - into a county with an active Hurricane Warning, Tornado Emergency or Flash Flood Emergency,
     or a FEMA declaration in the last 14 days;
   - after the recipient's team was knocked out;
   - in the 24-72 hours after a national tragedy (pause all sequences);
   - on major holidays (Thanksgiving week, Dec 24 - Jan 1, July 4, regional holidays);
   - on a birthday (creepy in cold email; no data says otherwise).
7. **Stack signals** where you can: a raise in the last 6 months plus a VP Revenue hired in the
   last 30 days beats either alone.

---

## 2. Company and person triggers: recency windows

Sources disagree by up to 5x, so these are our defaults.

| Trigger | Send window | Notes | Example line |
|---|---|---|---|
| Funding round | 7-45 days | Inbox floods in week 1; spend runs ~6 months; indexes lag 3-4 months, so check the date | "congrats on the series b. the next step is usually hiring AEs before there's pipeline for them." |
| New exec (VP+, CRO, head of) | 14-90 days | First 90 days is when the stack gets reviewed | "saw you joined as vp sales last month." |
| Champion job change | 7-45 days | Congratulate fast, sell slower | "congrats on the move to {{companyName}}." |
| Job posts in your domain | while open, ≤60 days | 6+ related roles in a short window = a surge | "you've got 6 sdr roles open." |
| Product launch | 3-21 days | Fast decay | "saw the launch of [product] last week." |
| M&A | 14-120 days | Integration pain lasts months | "saw the [target] deal close." |
| Earnings / 10-K / 10-Q | 0-30 days | Quote their risk factors (Item 1A) or MD&A in their own words, not the call recap | "in the 10-K you flagged [risk, quoted]." |
| Fiscal year end | 4-8 weeks before | Pull FYE from the 10-K cover or EDGAR; private = assume December | "your fiscal year closes june 30." |
| Permits (building, construction) | 0-21 days | Bidding happens before work | "saw the permit for the 120k sqft build on elm st." |
| Tech install / uninstall | 30-90 days | Only detectable installs; never infer an absence | |
| Website change (pricing, new page) | 7-14 days | | |
| Reviews (G2, Google) | 0-30 days | Avoid quoting a complaint about *them* | |
| Lawsuit / regulatory action / WARN layoffs | don't name it | At most an industry framing | |

---

## 3. Sports

**Two uses, very different strength:**
- **The event is the business** (strong). Coaches and athletic directors after a game; sports bars,
  hospitality and ticketing around playoffs; venues, staffing, security and logistics in host
  cities. Eric Nowoslawski: "We've gone as deep as finding high school football scores on Friday to
  email coaches about on Monday."
- **Rapport** (weak, PS-level). A nod to a team the prospect publicly follows. This belongs in the PS
  (`ps-and-first-lines.md`), not the opener.

**Rules:**
- **Allegiance must be evidenced** (their LinkedIn, bio, a sponsorship). HQ city does not tell you
  who someone roots for, since transplants are common. Without evidence, talk about the city ("must be
  a loud week in philly"), not "your eagles".
- Wins and milestones only, within 4 days of the game. A loss, blowout or elimination drops the line.
  Never trash-talk.
- Send Monday or Tuesday after the game.

**Data:**
- ESPN's unofficial API (free, unkeyed, no SLA):
  `site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard` (same pattern for college
  football, NBA, MLB, NHL, soccer); `/teams` gives venue cities for a metro → team table.
- TheSportsDB (free shared key, low limits), API-Sports (100 requests a day free), SportsDataIO (~$99/mo+).
- High school: no official MaxPreps API (community tools read its undocumented JSON routes; check
  the terms first). State associations and local outlets publish weekly score roundups.
- Pipeline: geocode HQ → metro → teams; pull results daily; write `team, opponent, score, result,
  round, game_date` onto the lead; gate the line on a win within 4 days.
- 2026 World Cup (Jun 11 - Jul 19, 11 US host metros plus Toronto, Vancouver and 3 Mexican cities) is
  past. Use it only as a lookback ("running ops in kc during the quarterfinal weekend can't have been
  quiet").

**Examples:**
- Coach: "saw westlake took down lake travis 28-21 friday. congrats to you and the staff."
- Evidenced fan (PS): "ps congrats on the bills clinching, must be a good week in buffalo."

---

## 4. Weather

| Event | Who buys | Strength |
|---|---|---|
| Hail ≥1" | roofing, restoration, auto glass, PDR, adjusters, property managers | strong |
| Heat wave | HVAC, refrigeration, cold chain, utilities, construction safety, staffing | strong |
| Hard freeze | plumbing, pipe-burst restoration, ag, irrigation, propane | strong |
| Hurricane / tropical storm | restoration, generators, tree service, insurance, logistics (**after** only) | strong, very sensitive |
| Wildfire smoke | air purification, HVAC filtration, outdoor events, construction | medium |
| Snow and ice | snow removal, facilities, retail, logistics | medium |

**Windows:** hail 2-14 days after (claims and inspections run for weeks). Heat or freeze during the
warning, up to 7 days after. Hurricane: never during, only 2-6+ weeks into recovery, for recovery and
preparedness services. The **plan-ahead angle is always safe**: HVAC capacity in April and May,
freeze prep in October.

**Sensitivity:** never opportunistic. No discounts tied to a disaster, no humor, no silver lining,
never casualties (American Apparel's 2012 "Sandy Sale" drew boycott calls). Auto-suppress declared
disaster counties; a human approves every first send into a hit area.

**Data (free):**
- NWS Alerts API: `api.weather.gov/alerts/active?area=TX`. No key, but needs a `User-Agent`. Filter
  by event, severity, zone or county; 7 days of history.
- SPC Storm Reports: daily hail, wind and tornado CSVs. Size is in hundredths of an inch (175 =
  1.75"); days run 1200-1159 UTC; preliminary, so dedupe.
- OpenWeather One Call (1,000 calls a day free, includes alerts), Tomorrow.io (500 a day free). Paid
  hail swaths (HailTrace) map points to addresses.
- Pipeline: store company sites as county FIPS or NWS zone → poll daily → join with threshold rules
  (hail ≥1", Excessive Heat Warning, Hard Freeze Warning) → write `wx_event, wx_date, wx_county`.

**Examples:**
- "noaa logged 1.75 inch hail across collin county tuesday. if any of your properties need roof
  inspections before claims windows close, we can be on site this week."
- "first hard freeze usually hits dfw mid-november. are your sites winterized yet?"

---

## 5. The B2B calendar

Shift by the account's fiscal year (Microsoft and many states start July 1; the US federal year
starts October 1). Procurement takes 2-4 weeks, so reach out **4-8 weeks before** a deadline.

| Month | Trigger moments | Who |
|---|---|---|
| Jan | budgets released, SKOs, planning, CES | all B2B; CROs and sales leaders; consumer tech |
| Feb | Q4 earnings, tax-prep peak, HIMSS | public-company execs; CPAs; healthcare IT |
| Mar | Q1 close push, March Madness, northern construction starts | sales leaders; hospitality; GCs and subs |
| Apr | tax deadline (Apr 15), Q1 earnings, hail season starts, UK, India and Japan FY start | accounting; roofing and restoration; APAC and UK accounts |
| May | hail and tornado peak, HVAC pre-season, graduation hiring, mid-year review | roofing, insurance, HVAC; recruiting and HR |
| Jun | Q2 close, hurricane season opens (prep only), H2 planning, retail Q4 planning | sales and finance; restoration; retail |
| Jul | FY start (Microsoft, universities, many states), Q2 earnings, Prime Day | edu, state and local government; e-commerce |
| Aug | back-to-school, heat peak, next-year budget kickoff, harvest starts | edtech; HVAC and cold chain; CFOs and FP&A; ag |
| Sep | federal FY end (Sep 30), Dreamforce and conference season, Q3 close | federal contractors; SaaS and revops; sales leaders |
| Oct | open enrollment, **Q4 budget-flush outreach starts**, Q3 earnings, retail peak prep | HR and benefits brokers; all B2B; retail, 3PL, seasonal staffing |
| Nov | Medicare and ACA enrollment, BFCM, next-year budgets lock, freeze season | insurance and health plans; e-commerce; finance; plumbing |
| Dec | year-end close; **book January meetings**; sends slow Dec 20 - Jan 2 | finance and accounting; everyone ("for january") |

Also: regulatory dates (state privacy laws on Jan 1, 1099s on Jan 31, SOC 2 renewals); trade
shows (scrape the public exhibitor list, email 2-3 weeks before to book floor meetings, follow up
within 24 hours after); industry seasons (northern construction runs Mar-Nov, harvest Aug-Nov,
retail peak Oct-Dec).

**Budget flush:** don't lead with "use it or lose it" discounts (and never quote a price). The angle
is timing: "if [problem] is on next year's plan, now is when it gets budgeted." Frame it as a start date, not a deal.

**Holidays:** pause on major holidays. "Hope you had a good thanksgiving" adds nothing. For global
lists, suppress or soften around Ramadan, Diwali and Lunar New Year by region.

**Anniversaries:** company founding anniversaries are fine. Work anniversaries are borderline: use
one only with a business angle ("2 years running revops at X, what's changed since you took it
over?"), and better on LinkedIn. Never birthdays.

---

## 6. Building a trigger campaign

1. Pick a trigger where **the event changes what the buyer needs** this month. If the honest answer
   to "why does this matter to them?" is "it's a fun fact", it's a PS, not a trigger.
2. Write the source → field → gate pipeline first: `trigger_type, event_date, event_source_url,
   raw values`, plus the window and suppression rules above.
3. Write the base email (no trigger) first, so it works when the line drops.
4. Write the trigger line as a frame in the copy with the facts in variables ("saw {{team}} took
   down {{opponent}} {{score}} friday."). Never ask an AI to write a whole sentence about a score.
5. Tag the campaign `trigger_type` and record `trigger_age_days` at enrollment so you can
   tell whether fresher is actually better.
