# TTW NCAAF 2026 — TULANE PACKET + FINAL UNCERTAIN SWEEP

**Timestamp:** Monday, **2026-08-24, evening EDT** (America/New_York, owner timezone)
**Status:** **READ-ONLY. NOTHING APPLIED.** No workbook, no Google Sheet, no cell changed.
**Base:** v0.8.6 AUTHORITATIVE — `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9`
**Awaiting:** explicit owner approval for Tulane. **The QB closeout is NOT complete.**

---

# PART 1 — TULANE, row 91 — proposed **ACTIVATE at `M`**

## 1.1 The H-vs-M question you asked me to settle

**Answer: `M`. No H-level evidence exists.** I looked specifically for an official Tulane depth
chart or team announcement and found neither.

| Evidence tier | Found? | What I found |
|---|:--:|---|
| Official Tulane depth chart naming him | **NO** | The depth chart was *scheduled* for release 2026-08-24; the naming came **ahead of** it. The Tulane beat headline is literally *"Tulane Starting Quarterback Named **Leading Up to Roster Reveal**"*. |
| Official team announcement / release | **NO** | `tulanegreenwave.com` returned no article content; no release located. |
| Will Hall press-conference naming | **NO** | Not located. |
| **Reporter-sourced naming** | **YES** | ESPN's Pete Thamel, "**Sources:** Tulane fifth-year senior Zeon Chriss-Gremillion will start at quarterback for the Green Wave, making his debut at Duke on Sept. 5." |

Thamel's "**Sources:**" construction is the **exact** provenance class already precedented in this
workbook — Georgia Southern ("Sources: Georgia Southern has named veteran Max Johnson…"), North
Carolina, and Rutgers earlier today. All three were activated at `M`. **Tulane is `M` for the same
reason.** This is a provenance judgement, not a doubt about the fact.

> **Contrast with Washington State, decided hours earlier.** WSU earned `H` because the *program
> itself* posted the announcement. Tulane has no equivalent. The tiering is working exactly as
> designed.

## 1.2 Evidence

| Field | Value |
|---|---|
| Team / abbrev | Tulane Green Wave · `TULN` · row **91** |
| Player | **Zeon Chriss-Gremillion** (5th-year senior; Houston and Louisiana transfer) |
| Current | `L` / **UNCERTAIN** |
| Proposed | **`M`** / **OK** |
| Primary source | ESPN — Pete Thamel, "Sources:" report |
| Carried by | On3, `https://www.on3.com/news/tulane-names-zeon-chriss-gremillion-starting-quarterback-for-season-opener/` · Sports Illustrated (Tulane) · Yahoo Sports |
| Publication date | **2026-08-24** (Monday) |
| Beat out | **Kadin Semonza** in preseason camp |
| Corroboration | Reporting says he debuts **at Duke on Sept. 5**. The workbook independently confirms: `wk1 2026-09-05 Tulane Green Wave @ Duke Blue Devils`. |

### Sourcing limitation, stated plainly

**I could not fetch a primary page in full for Tulane.** On3 returned **HTTP 403**;
`tulanegreenwave.com/sports/football` returned navigation chrome with no article body; the SI article
was reachable only through its section index. The naming itself is corroborated **consistently and
independently** across ESPN/Thamel, On3, SI and Yahoo, and the Sept-5-at-Duke detail checks out
against the workbook's own schedule — but you should know the H-tier question was answered by
*absence of a locatable official source*, and absence is exactly what the standing rule says not to
treat as proof. **That limitation is itself the argument for `M` rather than `H`, so it does not
change the recommendation.**

### A stale source caught and rejected

An SI article titled *"Tulane Football Releases Depth Chart Showing Potential Starting QB"* surfaced
prominently and looked like exactly the H-level evidence sought. **It is dated 2024-08-28** — wrong
head coach (Jon Sumrall, not Will Hall) and wrong quarterbacks (Mensah / Thompson / Horton). Rejected.
A 2025 item naming **Jake Retzlaff** as Tulane's starter also surfaced and was rejected.

## 1.3 Baseline quarterback — and the `C91` requirement

**`C91` is currently blank.** As established in the v0.8.6 promotion, **every one of the 110 OK rows
carries a populated baseline quarterback in column `C` — 110 of 110, no exceptions.** Activating
Tulane with only the two zeros would create the first OK row with no baseline QB, leaving a zero
deviation that cannot be audited because nothing records *deviation from whom*.

`C91 = Zeon Chriss-Gremillion` is therefore **required**, on the same basis approved for Rutgers.
The workbook's own 2026-08-21 note already records the supporting fact: reporting that *"the job
defaults to Chriss-Gremillion if no one separates."* He was the presumptive baseline; the naming
confirms it, so the deviation is zero.

## 1.4 Exact cells

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C91` | *(blank)* | `Zeon Chriss-Gremillion` | text — **required, see 1.3** |
| `D91` | *(blank)* | **`0`** | **numerical** |
| `E91` | `Open (Semonza / Chriss-Gremillion / Johnson / Bruno)` | `Zeon Chriss-Gremillion` | text |
| `F91` | *(blank)* | **`0`** | **numerical** |
| `H91` | `L` | **`M`** | confidence |
| `I91` | `FOX 8 New Orleans, 2026-07-24 (https://www.fox8live.com/2026/07/24/four-qbs-battling-starting-spot-tulane/)` | `ESPN / Pete Thamel 2026-08-24, carried by On3 (https://www.on3.com/news/tulane-names-zeon-chriss-gremillion-starting-quarterback-for-season-opener/)` | metadata |
| `J91` | `2026` | **must not be rewritten** | — |
| `K91` | `2026-08-21` | `2026-08-24` | metadata |
| `L91` | prior correction note | activation note | text |
| **`G91`** | *(formula)* | **DO NOT WRITE** | formula |
| **`M91`** | *(formula)* | **DO NOT WRITE** | formula |

**Every proposed numerical entry: `D91 = 0` and `F91 = 0`. Two cells, both the integer `0`. No
nonzero value is proposed.** `G91 = 0 − 0 = 0`, so `ENGINE!M` contributes **nothing** to any game.

## 1.5 Resulting censuses — computed directly from the v0.8.6 rows

| | v0.8.6 now | **After Tulane** |
|---|:--:|:--:|
| QB status | 110 OK / 28 UNCERTAIN | **111 OK / 27 UNCERTAIN** |
| Confidence | 73 H / 40 M / 25 L | **73 H / 41 M / 24 L** |
| Total | 138 | **138** |
| Nonzero QB values | 0 | **0** |

Tulane `L → M` is the only confidence movement: **−1 `L`, +1 `M`**, `H` unchanged.

## 1.6 Formulas and model outputs

`G91` and `M91` remain the workbook's formulas and are marked DO-NOT-WRITE; `J91` is not rewritten.
`ENGINE` reads only `A`, `G`, `M` — the delta computes to `0`, so **every model output is unchanged**,
including `MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` · `SJSU at USC -35.2` ·
`HAW at STAN -3.7`. Tulane does not play in Week 0; its first game is Week 1, 2026-09-05 at Duke.

---

# PART 2 — FINAL SWEEP OF ALL 28 UNCERTAIN ROWS

**Result: Tulane is the only genuine activation candidate.** No other row cleared through the cutoff.
No settled row was reopened and no unsupported change is proposed.

## 2.1 Priority checked first — the Week 0 gated game

Memphis and UNLV are the only remaining UNCERTAIN teams playing in Week 0, and they play *each
other* in the single QB-gated Week 0 game. Both were checked directly.

| Team | Row | Finding | Ruling |
|---|:--:|---|:--:|
| **UNLV** | 125 | Dan Mullen **has not decided**. Reporting: he "has not decided on a starter," said both Jackson Arnold and Alex Orji "will play," and suggested playing both. A separate item that Arnold "figures to start" is a **reporter projection**, not a naming. | **UNRESOLVED — stays `L`** |
| **Memphis** | 85 | Charles Huff **has not named a starter**. Memphis rotated Marcus Stokes and Air Noland through fall camp. | **UNRESOLVED — stays `L`** |

**Consequence: Memphis at UNLV remains QB-gated going into Week 0**, and legitimately so — neither
team has named a starter with the game six days out. Both are `L`, so the gate would hold even if
zeros were written. Nothing to apply.

## 2.2 Power-conference rows — no namings

| Team | Row | Finding |
|---|:--:|---|
| Arkansas | 7 | KJ Jackson vs AJ Hill, unresolved under new HC Ryan Silverfield |
| Florida | 9 | competition unsettled |
| Vanderbilt | 21 | **Clark Lea did not name a starter** after the Aug 15 scrimmage |
| Iowa | 24 | Hank Brown vs Jeremy Hecklinski "neck-and-neck" |
| Nebraska | 29 | nothing located through the cutoff |
| Kansas | 48 | Leipold expects **both** Ballard and Marshall to play; equal reps |
| Oregon State | 76 | Murphy leading, not named |
| Texas Tech | 52 | **medically gated** — QB1 identity confirmed, not a competition question |

## 2.3 Group of Five rows — no namings

Akron 105 · Ball State 106 · Buffalo 108 · Central Michigan 109 · Miami (OH) 112 · Ohio 113 ·
Nevada 120 · Northern Illinois 123 · Appalachian State 128 · Arkansas State 129 · Coastal Carolina 130 ·
Southern Miss 139 · UConn 143 · Liberty 99 · South Florida 89 · Colorado State 74 · Fresno State 75

Everything located for these was **preseason preview or projection material**, which the standing
rule excludes as a basis for naming a starter. Two examples encountered and rejected: an Athlon Sun
Belt preview projecting **Malachi Singleton** at Appalachian State and **Ryan Beard** at Coastal
Carolina — both projections, neither a naming, and the Coastal projection conflicts with the
workbook's own recorded candidate field.

### Sweep depth — stated honestly

This was a **targeted** sweep, prioritised by operational exposure: the Week 0 gated pair
individually, the eight power-conference rows, and the Group of Five as a cluster. **I did not fetch
a primary source for each of the 28 rows individually.** For the G5 rows in 2.3 the finding is "no
naming surfaced through the cutoff," which is weaker than "verified no naming occurred." Those rows
correctly remain UNRESOLVED either way, since the rule requires positive evidence to activate.

## 2.4 Candidate-record discrepancies — FLAGGED, NOT APPLIED

The sweep surfaced four rows where the recorded candidate field may no longer match reporting. These
are **data-quality observations only** — no confidence change, no numerical change, no status change,
and **nothing is proposed for application without your approval and a verified source.**

| Team | Row | Recorded field | What reporting indicates |
|---|:--:|---|---|
| **Memphis** | 85 | `Marcus Stokes` *(alone)* | A **two-man rotation with Air Noland** through fall camp. Naming Stokes alone may overstate a settled situation — the same defect class corrected for Fresno State and Tulane. |
| **Vanderbilt** | 21 | `Jared Curtis` *(alone)* | **Blaze Berlowitz** is a live competitor; Lea named no starter after the Aug 15 scrimmage. |
| **Arkansas** | 7 | `Open (KJ Jackson / AJ Hill)` | **Braeden Fuller** (Angelo State) also reported in the competition. |
| **Kansas** | 48 | `Cole Ballard (leader; Isaiah Marshall competing)` | **Chase Jenkins** (Rice) also in the mix; reporting describes **equal reps**, not a clear leader. |

Memphis is the most consequential — it is a Week 0 team in the gated game. Its confidence is `L` and
its status UNCERTAIN either way, so **no rating or gate outcome depends on this**, but the record
would read more accurately as a two-man field. Say the word and I will draft the exact cells.

## 2.5 ⚠️ Schedule data anomaly — FLAGGED, NOT CHANGED

While verifying the Memphis–UNLV kickoff I found a discrepancy worth your attention. It is **not** a
QB matter and I have changed nothing.

**The workbook has Memphis @ UNLV on `2026-08-30`, a Sunday. Two independent outlets report the game
as Saturday, Aug 29, at 9 p.m. CT at Allegiant Stadium.**

9 p.m. CT Saturday Aug 29 = **02:00 UTC Sunday Aug 30**. That is the signature of a **UTC date being
stored instead of the local kickoff date**, and the schedule file's own `notes` confirm the rows came
from the ESPN API.

Testing that hypothesis across the full file: **70 games fall on a Sunday.** They cluster exactly
where a UTC roll would put them — late Pacific and Mountain kickoffs (Hawai'i, San Diego State,
Fresno State, Boise State, UNLV, Nevada, San José State, Oregon State, UTEP, New Mexico) plus ET
night games such as **Miami @ Notre Dame** and **Nevada @ UNLV on Sunday Nov 29**. Regular-season
Sunday games in late November are not plausible.

**Important caveats, so this is not overstated:**

- Part of the Sunday cluster is **genuine**. 2026 Labor Day is Monday Sept 7, so Sunday Sept 6 is a
  real television window — the Apple Cup on Sunday Sept 6 is independently confirmed, and the file's
  lone Monday game (SMU @ Florida State, Sept 7) is a real Labor Day game.
- `validate_schedule.py` passes **all hard-fail checks**, including the Week 0 / Week 1 boundary, so
  **no game is misclassified** and no rating is affected — dates do not enter the rating chain.
- I have **not** confirmed the true kickoff date from a primary source, only from reporting.

**Recommended check:** compare the file's `start_date` against ESPN's **local** kickoff time for a
handful of the November Sunday games. If they are Saturday-night games, the extractor should take the
local date, not the UTC date. **I have changed nothing and recommend no edit until that is verified.**

---

# PART 3 — WHAT REMAINS OPEN

| Item | Row | State |
|---|:--:|---|
| **Tulane** — Zeon Chriss-Gremillion | 91 | **Packet above. Awaiting your approval.** Not applied. |
| **Texas Tech** — Will Hammond | 52 | `H`, medically gated. QB1 identity not in question. |
| **Memphis / UNLV** | 85 / 125 | Genuinely unresolved six days before their Week 0 meeting. |
| 24 further competitions | — | Unresolved; recheck as namings land through Week 1. |
| **Record discrepancies** | 85, 21, 7, 48 | Flagged in 2.4, awaiting your call. |
| **Schedule date anomaly** | — | Flagged in 2.5, awaiting verification. |
| **Live-Sheet application** | — | v0.8.5, v0.8.6, NIU and Tulane corrections all remain **owner actions**. |

**The live Google Sheet has not been updated.** The connector cannot write cells — this is not a
claim that it was done.

**The QB closeout is NOT declared complete.**
