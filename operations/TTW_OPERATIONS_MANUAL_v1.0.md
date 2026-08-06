# TTW COLLEGE FOOTBALL OPERATIONS MANUAL
## Version 1.0 — 2026 Season

**Workbook:** TTW College Football Power Ratings v0.8.1 AUTHORITATIVE (frozen)
**Author:** Director of Football Operations
**Governs:** the entire 2026 season

---

## GATE — DO THIS BEFORE WEEK 0

The manual does not start until these four are done. They are Phase 9B items I could
not apply through the connector.

1. **Timezone → America/New_York** (File → Settings). Lost on every import.
2. **Rename** the master, dropping the trailing ` 4`. Delete stray sibling copies.
3. **Owner note on SETTINGS** (below the last setting, ~`A33`) stating B4/B5 are weekly-required and that stale-line protection is off while B5 is blank.
4. **Protection** per `phase9a_production_config/SHEETS_PROTECTION_MAP.md`, amended: `IMPORT STATS!K6:K205` **RESTRICTED**, `A6:J205` editable.

**Until step 1 and the weekly B4/B5 habit exist, you are betting without stale-line
protection and the workbook will report a clean `STALE LINE = 0` while unprotected.**

---

## THE WEEK AT A GLANCE

| Day | Activity | Time |
|---|---|---|
| **Sunday PM** | Results land. Nothing to do. | — |
| **MONDAY** | **Section A** — Model refresh | 20–30 min |
| **MON PM / TUE** | **Section B** — Early market attack → Watch List | 30–45 min |
| **TUE–THU** | **Section C + D** — Research gauntlet → Card | 2–4 hrs across 3 days |
| **THU–FRI** | **Section E** — Content production | varies |
| **SATURDAY** | **Monitoring only.** No new opinions. | passive |
| **SUNDAY** | **Section F** — Grading | 30–45 min |

**Wagers are placed Tuesday–Thursday.** That is where CLV lives. Saturday is a
monitoring day, not a betting day.

---

# SECTION A — WEEKLY MODEL REFRESH (MONDAY)

**Goal: a healthy, current workbook. Not opinions. Do not look at a line yet.**

### A1 — Create the working copy (2 min)
File → Make a copy → `TTW WORKING YYYY-MM-DD Wk N`.
**Confirm the title bar reads WORKING before you type anything.**

### A2 — Set the week header (1 min)
`SETTINGS!B4` = week number · `SETTINGS!B5` = **today's date**.
**Verify `START HERE!C7` flips to `OK — week N`.** If it still says
`— set week + as-of date`, you have no staleness protection.

### A3 — Import last week's stats (3 min)
Pull the CFBD season-to-date file. Paste at **`IMPORT STATS!A6`**.
The documented format is **9 columns, A–I** — team, games, off_epa_play,
def_epa_play, off_success_rate, def_success_rate, off_ppp, def_ppp, pace.
Column J is a spacer; **column K is a formula — never paste over it.**

Verify `START HERE!C9` reads `N team rows loaded`.

### A4 — Schedule (30 sec)
Already loaded: **888 games**. Re-paste only if the schedule changed
(cancellations, reschedules). Verify `START HERE!C10` reads `888 games loaded`.

### A5 — Ratings update (0 min — automatic)
Ratings recompute from `IMPORT STATS` + `PRESEASON` priors. **No action.**
Movement is capped at `SETTINGS!B12 = 2.5` points per week.

### A6 — Review rating movement (5–10 min) ← **the analytical part of Monday**
Open `TEAM RATINGS`. Compare against last week's working copy.

**What you are looking for:**

| Signal | Meaning | Action |
|---|---|---|
| Move **> 2.5 pts** | Should be impossible — the cap prevents it | **Investigate immediately.** Possible data defect. |
| Move **2.0–2.5** (at cap) | The model wanted to move further | Note the team. Their number is still catching up — likely more movement next week. **These are your best early-market targets.** |
| Move **< 0.5** | Stable | Ignore |
| Rating moves with **no game played** | Opponent-adjustment ripple | Normal. Verify the opponent actually played. |

**Record the five largest movers each way.** They feed Section G.

### A7 — Data anomalies (3 min)
`DATA QUALITY`: **BLOCKED must be 0.** Anything blocked, clear it now — reasons are in
`ENGINE!AH`. Common causes: duplicate GameID, unmatched team, missing rating.

### A8 — Workbook health (1 min)
**`START HERE!C15` must read `OK — all invariants pass`.**
If it doesn't, **stop**. Nothing above it is trustworthy.

## ▣ DELIVERABLE — WEEKLY MODEL REFRESH CHECKLIST

```
MONDAY — MODEL REFRESH                          Week ___  Date ______
□ Working copy created, title reads WORKING
□ B4 = week    B5 = today        → C7 reads "OK — week N"
□ Stats pasted at IMPORT STATS!A6 (cols A–I only)  → C9 shows rows
□ C10 reads "888 games loaded"
□ TEAM RATINGS reviewed vs last week
    Top 5 risers  ______________________________
    Top 5 fallers ______________________________
    At-cap (2.0–2.5) movers → early-market targets ______________
□ Any move > 2.5?  □ No   □ YES → STOP, investigate
□ DATA QUALITY: BLOCKED = 0
□ C15 = "OK — all invariants pass"
□ Games 888 · Teams 138 · Failing invariants 0
SIGN-OFF: ____________
```

---

# SECTION B — EARLY MARKET ATTACK (MONDAY NIGHT / TUESDAY)

**Goal: find where you disagree with the opening market, and decide what deserves
research. This section produces a Watch List — never a bet.**

### B1 — Filter first. Always. (30 sec)
**`DASHBOARD` → filter Week = N → filter Major scope = Y.**

**This is the most important operating habit in the manual.** `START HERE!C12` will
say something like `Missing: 761 lines`. **That counts the whole season, not your
week.** Treating it as a to-do list is the single fastest way to lose a morning.
Your real weekly universe is **50–70 games**.

### B2 — Enter opening lines (20–30 min)
Openers typically post Sunday night. Enter them Monday night or first thing Tuesday —
**earlier is better; that is the entire CLV thesis.**

Per game in `MARKET LINES`:
- **`A` GameID** — copy from the DASHBOARD's rightmost column
- **`B`** — auto-echoes the matchup. **This is your only typo check. If it reads `GAMEID NOT IN SCHEDULE`, you mistyped. Look at it every single time.**
- **`C` Favorite** — team abbreviation
- **`D` Spread** — **POSITIVE number, always**
- **`E` Total** · **`G` Line date**

**Sign convention:** Georgia -7.5 at home → Favorite `UGA`, Spread `7.5`. The sheet
stores market home spread −7.5. **Edge = final margin + market home spread.**

**`Miami` is rejected on manual entry.** Use `MIA` (ACC) or `M-OH` (Miami OH).

### B3 — Read the disagreements (10 min)
Sort DASHBOARD by **Priority**. Read `ENGINE!V` (Spread EDGE) and `X` (Label).

| Label | Edge | What it means |
|---|---|---|
| *(blank)* | < 1.0 | Model agrees with market. **Ignore.** |
| `LEAN` | 1.0–1.5 | Mild disagreement. Watch only. |
| `INVESTIGATE` | ≥ 1.5 | **Research candidate.** |
| `BET` | ≥ 3.0 | Only if toggle = Y **and** status = READY |

### B4 — Triage into the Watch List
A game earns a Watch List slot when **all** of these hold:

1. Status is **READY** or **QB UNCERTAIN** (not BLOCKED / PENDING / STALE / FCS)
2. `|edge| ≥ 1.5`
3. It is in **Major scope**
4. You can realistically research it before Thursday

**Cap the list at 8–12 games.** More than that and the research quality collapses.
A shorter, better-researched list beats a long shallow one every week.

### B5 — Bet now, or wait?

**Bet immediately when:**
- Edge ≥ 3.0, status READY, and the research gauntlet is already satisfied by prior knowledge
- You hold **QB information the market has not priced** — this is the highest-value case and it is perishable by hours
- The number is at a key threshold (3, 7, 10) and likely to move through it

**Wait when:**
- QB status is UNCERTAIN and the depth chart lands mid-week
- An injury report is due before Thursday
- The edge sits at 1.5–2.5 — let research decide

**Never wait past Thursday to "see what happens."** That is how CLV dies.

## ▣ DELIVERABLE — RESEARCH WATCH LIST

```
RESEARCH WATCH LIST — Week ___     Generated: ____ (Mon PM / Tue AM)
# | Game | Model | Mkt | Edge | Side | Conf | Status | Why it's here | Bet now?
1 |      |       |     |      |      |      |        |               |
...
CAP: 12.   Excluded despite edge: ____________________ (reason)
NOT A BETTING RECOMMENDATION. Research required before any wager.
```

---

# SECTION C — TTW RESEARCH WORKFLOW

**Every candidate passes the same gauntlet, in this order. Order matters: it moves
from objective to subjective, so your priors get anchored by data before narrative.**

### 1. WORKBOOK — *the primary decision engine*
Record: model spread, edge, confidence (1–5), status.
**Ask:** does the model have full information? Check `ENGINE!AJ` — confidence starts
at 3, drops 1 each for small sample / QB uncertain / transitional / FCS, gains 1 at
≥6 effective games.
**Confidence 1–2 = the model is telling you it doesn't know. Respect that.**

### 2. MARKET — *the sharpest single opinion in the room*
Record opener and current. **Which way has it moved, and on what volume?**
- Line moved **toward** your side → market agrees; your edge is shrinking. Act fast.
- Line moved **away** → someone knows something. **Find out what before you bet.**
- Line static with heavy public money → sharp resistance. Interesting.

**The market is right more often than you are. Disagreement requires a reason, and
"my model says so" is not a reason — it is a starting point.**

### 3. VSiN COMPARISON — *professional peer review*
**Use VSiN to challenge or reinforce the workbook, never to replace it.**
- VSiN agrees → confidence up. Not a new edge, a confirmed one.
- **VSiN disagrees → the highest-value moment in the workflow.** One of you is wrong. Find out which. If you cannot articulate *why* VSiN is wrong, do not bet.

*Status: the VSiN reference library is not yet built (upload failed). Until it is, use
the guide manually.*

### 4. SP+ · 5. FPI · 6. TeamRankings — *the blend components*
These three are already inside your preseason prior (weights 0.30 / 0.25 / 0.15).
**Checking them is not independent confirmation — it is partially circular.**
Their value is in **divergence**: if SP+ and FPI disagree sharply with each other,
the team is genuinely hard to rate and your edge is less real than it looks.

*Known scale artifact: SP+ has a wider spread than FPI (SD 13.20 vs 11.33). A raw
point gap between them overstates disagreement, especially in the bottom third.
Compare ranks, not points.*

### 7. MASSEY — *the genuinely independent check*
Not in the blend. **This is your only truly external rating opinion.** Weight it
accordingly. Massey against you when the blend is with you = real signal.

### 8. INJURY REVIEW
Beyond QB: offensive line continuity, top-2 skill players, secondary. Log anything
material in `ADJUSTMENTS` (type `GAME`, **reason required**).
**Ask: is this priced already?** An injury reported Sunday is priced by Tuesday.

### 9. QB REVIEW — ***your single largest edge***
Check `QB VALUES` for both teams.
- **`L` code → QB UNCERTAIN** → the game is gated out of BET regardless of edge
- **`M` code** → leader identified, not officially named — **the fragile tier**
- **`H` code** → confirmed starter

**Why this matters more than anything else here:** across 80 team-specific
verification passes, **11 records were wrong — roughly one in seven.** Ten were
over-confident. If you know a starter the market hasn't priced, that is the edge.

**Note the asymmetry:** 33 teams are `L` and 61 `H`-coded records were never
independently verified. **An H code is an assumption, not a guarantee** — Missouri
proved it.

### 10. TRAVEL
Cross-country, altitude, short week, body-clock (west→east 12pm ET).
Log via `ADJUSTMENTS` type `TRAVEL/REST`.
**HFA is `SETTINGS!B6 = 2.5` flat, neutral `B7 = 0`.** The model does not know your
game is a 2,000-mile Thursday trip. **This is where you add value the workbook cannot.**

### 11. WEATHER
Wind > 15 mph matters most, and mostly to totals — **which are disabled this season,
so weather is a spread-side sanity check only.** Extreme cold/rain compresses margins;
favor the run-heavier team and the underdog.

### 12. MOTIVATION / SCHEDULING
Look-ahead spots, letdown after a rivalry, coach on the hot seat, senior day, bowl
eligibility late, opt-outs in December.
**Be honest: this is the most narrative-prone step and the easiest to fool yourself
with. Require a concrete mechanism, not a story.**

### → TTW FINAL OPINION
Write one paragraph, in your own words, stating **the number you would set** and
**why you disagree with the market.** If you cannot write it clearly, you do not have
a bet. **This is the gate.**

---

# SECTION D — CARD CONSTRUCTION

## Why a workbook edge is NOT automatically a wager

**This is the most important page in the manual.**

1. **The workbook is one opinion, and it says so.** The permanent disclaimer: *"Labels identify model-versus-market divergence, not guaranteed betting value."* An edge means the model and the market disagree. **It does not say who is right.**
2. **The market is sharper than the model on most games.** Your edge exists in specific pockets — QB information, situational spots the model can't see — not uniformly across 761 games.
3. **Early-season ratings are weak.** Weeks 0–2 run on preseason priors with no in-season data. The model docks confidence for small samples. **Believe it.**
4. **An edge from bad inputs is noise.** If a QB is `L`-coded, the model is projecting a team whose starter is unknown. The edge is real arithmetic on a fictional premise.
5. **Betting every edge guarantees betting your worst ones.** Volume is the enemy of a thin edge.

**The workbook nominates. You decide. Those are different jobs.**

## The wager record — every bet gets one

```
WAGER — Week ___  Game: ____________________  Date: ______
Workbook edge      : ____ pts    Model: ______   Confidence: _/5
Market number      : ______ @ ________ (book)   Opener: ______
Status             : READY / QB UNCERTAIN / other: ______

REASONS TO BET (min 2, at least one non-workbook):
  1. ______________________________________________
  2. ______________________________________________

REASONS NOT TO BET (min 2 — if you can't find two, you haven't looked):
  1. ______________________________________________
  2. ______________________________________________

BIGGEST RISK — the one thing that beats me: _______________
EXPECTED CLV: line should move ___ toward ___ because ___________
UNITS: ____        FINAL APPROVAL: □ BET   □ PASS   □ WAIT
If PASS/WAIT — why: ______________________
```

**The "reasons NOT to bet" field is mandatory and is the point of the form.** Two
genuine counter-arguments, every time. A card where every game has weak counter-
arguments is a card built on confirmation bias.

## Card rules

- **Cap the card.** 3–6 wagers a week. If you have 12, you have 3 bets and 9 opinions.
- **No bet without a completed Section C gauntlet.** All 12 steps.
- **No bet on `QB UNCERTAIN` unless the QB uncertainty *is* your edge** — i.e. you know the answer and the market doesn't.
- **No bet at confidence 1–2** except with an explicit written override.
- **Bet Tuesday–Thursday.** Friday is late. Saturday is too late.

---

# SECTION E — TTW CONTENT PRODUCTION

**Runs Thursday–Friday, after the card is substantially complete. Never before.**
Content follows conviction; conviction does not follow content. If you record before
the card is set, you will talk yourself into positions.

### E1 — Long-form episode *(the anchor asset)*
Structure that falls out of the workflow you already did:
1. Last week's grading — **lead with the losses and the process, not the wins**
2. Biggest rating movers (Section A6)
3. The week's model-vs-market disagreements (Section B)
4. 2–3 deep dives — the Section C gauntlet *is* your script
5. The card, with the *reasons not to bet* included
6. What would change your mind

**Record once. Everything downstream is cut from this.**

### E2 — YouTube Shorts *(3–5 per episode)*
Cut directly from the long-form. Each Short = one game, one idea, under 60s.
**Do not record Shorts separately** — that is duplicate work.

### E3 — Social
Text from Short transcripts. One card graphic. One "biggest disagreement" post.

### E4 — Graphics
Build from the Section G dashboard. **Same numbers, no re-derivation** — every
re-typed number is a chance to publish a wrong one.

### E5 — Publishing
Long-form → Shorts staggered → social. **All before Saturday kickoff**, so the record
is timestamped ahead of results.

### E6 — Record keeping
Archive: the working copy, the card, the episode, the published numbers. **This is
what makes Section F possible.** No archive, no grading, no improvement.

**Efficiency rule: one recording session, one graphics session, everything else is
cutting.** Content is downstream of work already done.

---

# SECTION F — WEEKLY REVIEW (SUNDAY)

**Grade the process, not the outcome.** A well-researched loss is a better bet than a
lucky win, and the season is too short for results to tell you which was which.

### Per wager

| Field | How to grade |
|---|---|
| **ATS result** | W / L / P |
| **Closing line** | The number at kickoff |
| **CLV** | Your number vs close, in points |
| **Beat the close?** | **Y / N — the primary metric** |
| **Model accuracy** | Model spread vs actual margin |
| **Market accuracy** | Closing spread vs actual margin |
| **Research quality** | Did the gauntlet surface what mattered? 1–5 |
| **Process quality** | Did you follow the manual? 1–5 |
| **Variance** | Did it hinge on a fluke — turnover luck, a missed FG, a bad spot? |
| **Missed information** | What was knowable Tuesday that you didn't know? |
| **Lesson** | One sentence |

### The hierarchy

1. **CLV is the primary metric.** Beating the close consistently means the process works, regardless of a 20-game sample's record.
2. **Model vs market accuracy** — over the season, whose number was closer? That tells you how much to trust the workbook next year.
3. **ATS record is the noisiest.** At 3–6 bets a week, a season is ~60 wagers. That is nowhere near enough to distinguish skill from luck. **Do not react to it.**

### Red flags — process problems, not bad luck
Negative CLV three weeks running · betting games that failed the gauntlet · card
creeping past 6 · "reasons not to bet" going thin · skipping Section A on a busy week.

---

# SECTION G — WEEKLY OPERATIONAL DASHBOARD

One page, filled Monday, updated Tuesday. **Feeds the episode and the graphics.**

```
TTW WEEK ___ OPERATIONS DASHBOARD              Date: ______

RATING CHANGES        risers ▲ _________________  fallers ▼ _________
                      at-cap (2.0–2.5) → early targets ______________
LARGEST MODEL EDGES   1. ____ (__)  2. ____ (__)  3. ____ (__)
VS MARKET             biggest disagreements _____________________
VS VSiN               agreements ______  DISAGREEMENTS ★ __________
INJURY IMPACTS        _______________________________________
UNRESOLVED QB         count ___ (season start 39) · affecting my week: ______
PRIORITY RESEARCH     1. ______  2. ______  3. ______
BETTING CARD          ___ wagers · ___ units · avg edge ___ · avg conf ___
PENDING DECISIONS     waiting on: ______________ deadline: ______

HEALTH   invariants ___  games ___  BLOCKED ___  B4/B5 set? ___
```

**The VSiN disagreement line is the one to look at first.** Agreement is comfortable;
disagreement is where you learn something.

---

# SECTION H — SEASON OPERATING RULES

## NEVER change during the season

| Setting | Value | Why frozen |
|---|---|---|
| `B6` HFA | **2.5** | Changing it silently re-prices every game |
| `B7` Neutral HFA | **0** | Verified correct (Dublin, Week 0) |
| `B8/B9/B10` thresholds | **1.0 / 1.5 / 3.0** | Changing rewrites your season's label history |
| `B12` movement cap | **2.5** | Your protection against a data spike |
| `B13` stale line | **5 days** | |
| `B14` margin cap | **28** | Blowout protection |
| `B15–B21` regression / EPA weights | as shipped | Methodology |
| `B28–B31` source weights | 0.30/0.25/0.20/0.15 | Methodology |
| `B22`/`B23` totals | **BLANK** | **Uncalibrated. Do not populate.** |
| **Any formula** | 123,011 of them | Frozen |

**Unit sizing philosophy** — you must define this before Week 0 and then freeze it.
I have deliberately not invented a scheme for you. Whatever you choose (flat, or tiered
by confidence 1–5), **write it down and do not change it mid-season.** Changing sizing
after losses is the most common way a good process produces a bad year.

**Grading standards** — Section F as written. **Do not change what counts as a win
mid-season.**

## The only permitted change
A **verified critical defect** — the workbook produces a *wrong number* or *fails to
compute*, and money is at risk. Not "this could be better." Evidence first, then a
decision, then a documented fix with a regression run. **Never a Saturday-morning edit.**

## Weekly monitoring
Invariants 0 · games 888 · teams 138 · BLOCKED 0 · B4/B5 set · no move > 2.5 ·
QB UNCERTAIN trending down.

## Monthly
Re-verify a sample of the **61 never-independently-verified H records.** Confirm the
master is unedited. Confirm the working-copy archive is intact.

---

# SECTION I — POSTSEASON REVIEW (DECEMBER–JANUARY)

**Nothing in this section may be acted on during the season.**

### I1 — Model performance
Model spread vs actual margin, all season. **Mean absolute error vs the closing line's
MAE.** If the market beat you across ~800 games, the model needs work, not the process.
Segment by: week (early vs late), conference, favorite vs dog, QB-confidence tier.

### I2 — CLV performance ← **the headline number**
% of wagers that beat the close, and average CLV in points. **Positive CLV with a
losing record means keep going.** Negative CLV with a winning record means you got
lucky — fix the process.

### I3 — ATS performance
Report it, weight it last. ~60 wagers cannot separate skill from variance.

### I4 — Workflow efficiency
Actual weekly time vs the 25–40 min target. Where did it go? What got skipped when
the week was busy? **The steps you skip under pressure are the ones to automate.**

### I5 — Recurring mistakes
Pull every "missed information" and "lesson" from Section F. **Cluster them.** Three
instances of the same mistake is a process defect, not bad luck.

### I6 — v2.0 opportunities
Only from the season's actual record. Likely candidates, based on what is already
known:
- **Automated line entry** — ~60% of weekly time; the biggest single win
- **Totals calibration** — a real project with its own historical dataset and audit; disabled all 2026
- **QB monitoring automation** — the Phase 8.4 pipeline exists but is manual-triggered
- **CLV tracking inside the workbook** — currently manual

**Every v2.0 item must trace to a documented in-season observation.** No hypothetical
improvements. That is the standing rule of this role.

---

## MANUAL CHANGE CONTROL

This manual is v1.0. Amendments require a **dated in-season observation** — what
happened, which week, what it cost. No speculative edits. Amendments are logged here.

| Ver | Date | Change | Triggering observation |
|---|---|---|---|
| 1.0 | 2026-08-06 | Initial | Phases 9A/9B/10 validation |
