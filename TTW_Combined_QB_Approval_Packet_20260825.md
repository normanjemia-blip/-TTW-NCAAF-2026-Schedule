# TTW NCAAF 2026 — COMBINED QB APPROVAL PACKET

**Cutoff:** Tuesday, **2026-08-25, 06:57 EDT** (America/New_York)
**Status:** **READ-ONLY. NOTHING APPLIED.** No production write of any kind.
**Base:** v0.8.6 AUTHORITATIVE, **frozen at `c6bc5f8`** — SHA-256
`bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` *(re-verified)*
**Schedule work:** deliberately **excluded** from this packet — see `schedule_candidate_v1/`.

---

# PART A — RECONCILIATION OF THE THREE NAMED TEAMS

## A.1 Northwestern row 30 — **ALREADY OK. No action required.**

| Cell | Value |
|---|---|
| `C30` / `E30` | `Aidan Chiles` / `Aidan Chiles` |
| `D30` / `F30` | `0` / `0` → `G30 = 0` |
| `H30` | **`H`** |
| status | **OK** |

Northwestern never appeared in the UNCERTAIN population and needs nothing. It was activated at `H`
as an uncontested transfer QB1. **Not an activation candidate.**

> One housekeeping observation, not a proposal: `L30` still ends `VALUE PENDING RUBRIC APPROVAL` and
> `K30` reads `2026-07-21`, the oldest stamp among OK rows. The row is correct and the gate is
> properly cleared; only the note text is stale. Flagged, not proposed.

## A.2 Florida row 9 — **ACTIVATION CANDIDATE at `H`**

Meets your "official coach/team evidence" bar on both counts: the head coach announced it publicly
**and** the official athletics site published it.

| Field | Value |
|---|---|
| Current | `L` / **UNCERTAIN** · `E9` = `Aaron Philo` · `C9` blank |
| Proposed | **`H`** / **OK** |
| Source (first-party) | **Official Florida athletics** — `https://floridagators.com/news/2026/8/24/football-philo-moves-to-top-of-qb-depth-chart-aug-24-2026` |
| Source (coach) | The Independent Florida Alligator — `https://www.alligator.org/article/2026/08/aaron-philo-starting-quarterback` |
| Date | **2026-08-24** |
| Provenance | **HC Jon Sumrall announced Philo as the starter on Monday**, on the record: *"Philo will get the lion's share of reps with the ones as we start to try to create cohesion within our football team to be ready for game one."* |
| Beat out | Tramell Jones Jr. (RS freshman) |
| Corroboration | Reporting places Philo's debut vs **FAU**. Workbook confirms: `wk1 2026-09-05 Florida Atlantic Owls @ Florida Gators`. |

**Recorded caveat (does not block):** Sumrall added *"this is not an anointing… not some permanent,
you're the starter forever."* That is a caution about permanence, not a hedge on who starts Week 1.
It goes into the note verbatim.

## A.3 Oregon State row 76 — **ACTIVATION CANDIDATE at `M`, with a genuine methodological blocker**

Braden Atkinson **won the job — beating the incumbent the workbook records as the leader.**

| Field | Value |
|---|---|
| Current | `M` / **UNCERTAIN** · `E76` = `Maalik Murphy (leader; Braden Atkinson pushing)` · `C76` blank |
| Named starter | **Braden Atkinson** (Mercer transfer, 2025 Jerry Rice Award winner) |
| Source | Columbia County Spotlight / Portland Tribune — `https://columbiacountyspotlight.com/2026/08/24/oregon-state-names-braden-atkinson-starting-qb/` |
| Date | **2026-08-24** |
| Provenance | **Reporter-sourced.** *"Thamel reported Monday that Oregon State named Braden Atkinson… will be the Beavers' starting quarterback week one against No. 23 Houston."* The article adds that the Oregon State football account *"subsequently confirmed"* it — but that first-party act is reported **secondhand** and I could not retrieve the post itself. |
| Confidence | **`M`** — your stated default. I am **not** claiming `H`: the primary attribution is Thamel, and an unverified secondhand claim of team confirmation is not a first-party source I have seen. |
| Beat out | **Maalik Murphy** (incumbent) and Brady Jones (Western Michigan transfer) |
| Corroboration | Reporting places Week 1 at **Houston, TDECU Stadium**. Workbook confirms: `wk1 2026-09-05 Oregon State Beavers @ Houston Cougars [TDECU Stadium]`. |

### ⚠️ A.3.1 THE BLOCKER — Oregon State breaks the zero-deviation premise

**This is the first row in the project where the named starter is NOT the quarterback the preseason
blend assumed.** It deserves your explicit decision rather than a silent zero.

Every prior activation satisfied one of two conditions:

- `C` already held the named starter (Washington State, Arkansas, Northwestern), or
- `C` was blank and the named starter **was** the recorded presumptive leader (Rutgers, Tulane,
  Georgia Southern, Florida, Nebraska, Ohio).

**Oregon State satisfies neither.** The workbook's own note records **Maalik Murphy** as the leader —
an SI headline even said Murphy was "NAMED STARTER". The preseason rating priced Oregon State with
Murphy, its returning starter. Atkinson is an FCS transfer who displaced him.

The zeros carry a specific meaning in this workbook: *"the active starter **is** the quarterback the
preseason rating already assumed, so no deviation applies."* **For Oregon State that sentence is
false.** Writing `D76 = 0` / `F76 = 0` would assert that swapping Murphy → Atkinson has exactly zero
rating impact — a substantive modelling claim the convention was never built to carry, and one that
properly needs the QB-value rubric that is still pending.

**Two options. I recommend Option B.**

| | Option A — activate with zeros | **Option B — record correction only (recommended)** |
|---|---|---|
| `C76` | `Maalik Murphy` *(the true baseline)* | `Maalik Murphy` |
| `E76` | `Braden Atkinson` | `Braden Atkinson` |
| `D76` / `F76` | `0` / `0` | **stay blank** |
| `H76` | `M` (unchanged) | `M` (unchanged) |
| Status | UNCERTAIN → **OK** | **stays UNCERTAIN** |
| Meaning | asserts a QB change worth exactly 0.0 | records the change; defers the valuation |
| Census | 115 OK / 23 UNC | **114 OK / 24 UNC** |

Option B keeps the record honest and the gate closed until the rubric exists. Option A is defensible
only if you are content to rule the Murphy→Atkinson swap worth zero. **Say which and I will build it.**

---

# PART B — DELTA SWEEP OF EVERY UNCERTAIN ROW THROUGH 2026-08-25 06:57 EDT

**My previous sweep under-covered the 22–24 August naming window.** It reported "no naming" for
Arkansas (named 08-23) and did not surface Florida, Nebraska, Oregon State or Ohio. This sweep
checked all 28 UNCERTAIN rows again against that window. Findings below.

## B.1 New activation candidates found

| Team | Row | Conf | Starter | Date | Provenance |
|---|:--:|:--:|---|:--:|---|
| **Nebraska** | 29 | **`H`** | Anthony Colandrea | **2026-08-22** | **HC Matt Rhule announced it.** Multiple outlets: *"Nebraska officially names starting quarterback."* Corroborated: opener vs **Ohio** matches `wk1 2026-09-05 Ohio Bobcats @ Nebraska Cornhuskers`. |
| **Ohio** | 113 | **`M`** *(conditional)* | Nick Poulos | **2026-08-25** | The Post (Athens): *"graduate student Nick Poulos was named the starter for week one in Lincoln, Nebraska."* **Attribution is not stated** — the article does not say who announced it. See B.2. |

## B.2 Ohio — why it is marked conditional

Ohio is genuinely borderline and I am not going to overstate it. In favour: the workbook already
carries Poulos as HC John Hauser's stated leader at `M`; the naming comes from the outlet that covers
the team; and its detail — Week 1 **in Lincoln against Nebraska** — matches the workbook exactly and
independently corroborates the Nebraska finding. Against: **the article never says who named him**,
and it is a season preview rather than a news report of an announcement.

`M` would be defensible. **I recommend holding Ohio one more cycle** for a Hauser quote or a depth
chart. Your call — the cells are in §C.5 either way.

## B.3 Rows checked and remaining UNRESOLVED

| Team | Row | Finding |
|---|:--:|---|
| Iowa | 24 | **No decision.** 2026-08-24 beat report: the Hecklinski/Brown answer "will have to wait a little longer." |
| South Florida | 89 | **Not activatable.** On3's Kelly Quinlan says Van Buren "is set to be" the starter — soft, reporter-sourced, and the Tampa Bay Times (2026-08-10) still had it "down to 2 options." See D.4 for a record flag. |
| Liberty | 99 | **Projection only.** Jaylen Henderson is a *projected* starter on depth-chart projection sites. Not a naming. |
| Akron | 105 | Preview language ("slated to launch 2026 with Poffenbarger"). Projection, not a naming. |
| Memphis | 85 | **No public naming, and none expected.** HC Charles Huff: *"You guys won't know until they flip the coin."* |
| UNLV | 125 | **No decision.** Dan Mullen has not decided; may play both Arnold and Orji. |
| Vanderbilt · Kansas | 21 · 48 | No naming — see Part D corrections. |
| Colorado State · Fresno State | 74 · 75 | Unchanged; competitions genuinely open. |
| Texas Tech | 52 | `H`, **medically gated**. Identity not in question. |
| Ball State · Buffalo · Central Michigan · Miami (OH) · Nevada · Northern Illinois · Appalachian State · Arkansas State · Coastal Carolina · Southern Miss · UConn | 106 · 108 · 109 · 112 · 120 · 123 · 128 · 129 · 130 · 139 · 143 | Nothing beyond preview/projection material surfaced through the cutoff. |

**Sweep-depth caveat, stated plainly:** the eleven rows in the last line were swept as a cluster, not
individually with a fetched primary source each. "No naming surfaced" is weaker than "verified none
occurred." Given this sweep already corrected a miss, treat that line as the least certain part of
this packet. All those rows stay UNRESOLVED either way, since activation requires positive evidence.

---

# PART C — ACTIVATION CANDIDATES: EXACT CURRENT → PROPOSED CELLS

**Formula cells on every row below are DO-NOT-WRITE:**
`G{row}` = `=IF(OR($D{row}="",$F{row}=""),"",$F{row}-$D{row})` ·
`M{row}` = `=IF($A{row}="","",IF(OR($G{row}="",$H{row}="L",$J{row}<>SETTINGS!$B$3),"UNCERTAIN","OK"))` ·
`A{row}`, `B{row}` = `TEAM MAP` formulas · `J{row}` = `2026`, **DO-NOT-REWRITE**.

## C.1 Tulane — row 91 — `L → M`

| Cell | Current | Proposed |
|---|---|---|
| `C91` | *(blank)* | `Zeon Chriss-Gremillion` |
| `D91` | *(blank)* | **`0`** |
| `E91` | `Open (Semonza / Chriss-Gremillion / Johnson / Bruno)` | `Zeon Chriss-Gremillion` |
| `F91` | *(blank)* | **`0`** |
| `H91` | `L` | **`M`** |
| `I91` | `FOX 8 New Orleans, 2026-07-24 (…)` | `ESPN / Pete Thamel 2026-08-24, carried by On3 (https://www.on3.com/news/tulane-names-zeon-chriss-gremillion-starting-quarterback-for-season-opener/)` |
| `K91` | `2026-08-21` | `2026-08-24` |
| `L91` | prior note | activation note |

**Source/date:** ESPN/Thamel, **2026-08-24** · **Confidence `M`** — reporter-sourced "Sources:"
construction; no official depth chart (the naming preceded the scheduled release).

## C.2 Arkansas — row 7 — `L → H`

| Cell | Current | Proposed |
|---|---|---|
| `C7` | `KJ Jackson` | **NO CHANGE** — already the baseline |
| `D7` | *(blank)* | **`0`** |
| `E7` | `Open (KJ Jackson / AJ Hill)` | `KJ Jackson` |
| `F7` | *(blank)* | **`0`** |
| `H7` | `L` | **`H`** |
| `I7` | `Sports Illustrated (SEC QB projections)` | `Yahoo Sports / Whole Hog Sports 2026-08-24 (https://sports.yahoo.com/articles/why-arkansas-football-chose-kj-091055884.html)` |
| `K7` | `2026-08-03` | `2026-08-24` |
| `L7` | prior note | activation note |

**Source/date:** **2026-08-24**, reporting a **2026-08-23 team announcement** — *"the Hogs made
things official on Sunday, Aug. 23, labeling Jackson as the starter,"* with HC Ryan Silverfield on
the record. **Confidence `H`.** Deviation is **literally zero**: `C7` already held KJ Jackson.

## C.3 Florida — row 9 — `L → H`

| Cell | Current | Proposed |
|---|---|---|
| `C9` | *(blank)* | `Aaron Philo` |
| `D9` | *(blank)* | **`0`** |
| `E9` | `Aaron Philo` | `Aaron Philo` *(unchanged in substance; rewritten with the activation)* |
| `F9` | *(blank)* | **`0`** |
| `H9` | `L` | **`H`** |
| `I9` | `Sports Illustrated (SEC QB projections)` | `Official Florida Athletics 2026-08-24 (https://floridagators.com/news/2026/8/24/football-philo-moves-to-top-of-qb-depth-chart-aug-24-2026); HC Jon Sumrall announcement via The Independent Florida Alligator (https://www.alligator.org/article/2026/08/aaron-philo-starting-quarterback)` |
| `K9` | `2026-08-04` | `2026-08-24` |
| `L9` | prior note | activation note incl. the "not an anointing" caveat verbatim |

`C9 = Aaron Philo` is required by the baseline-QB invariant and is correct on the merits: the
workbook's own 2026-08-04 note already recorded Philo as FAVORED, holding "the edge entering fall camp."

## C.4 Nebraska — row 29 — `L → H`

| Cell | Current | Proposed |
|---|---|---|
| `C29` | *(blank)* | `Anthony Colandrea` |
| `D29` | *(blank)* | **`0`** |
| `E29` | `Anthony Colandrea` | `Anthony Colandrea` *(unchanged in substance)* |
| `F29` | *(blank)* | **`0`** |
| `H29` | `L` | **`H`** |
| `I29` | `Sports Illustrated (Big Ten QB projections)` | `HC Matt Rhule announcement 2026-08-22, reported 2026-08-24 (https://klin.com/2026/08/24/colandrea-named-starting-qb-for-opener/)` |
| `K29` | `2026-08-04` | `2026-08-24` |
| `L29` | prior note | activation note |

**Source/date:** Rhule announced **2026-08-22**; reported **2026-08-24**. **Confidence `H`** —
head-coach announcement, same tier as Alabama/DeBoer, Tennessee/Heupel and Florida/Sumrall.

## C.5 Ohio — row 113 — `M → M` *(CONDITIONAL — recommend holding)*

| Cell | Current | Proposed |
|---|---|---|
| `C113` | *(blank)* | `Nick Poulos` |
| `D113` | *(blank)* | **`0`** |
| `E113` | `Nick Poulos (leader; not yet named)` | `Nick Poulos` |
| `F113` | *(blank)* | **`0`** |
| `H113` | `M` | `M` — **unchanged** |
| `I113` | `RotoWire MAC spring / Ohio Athletics` | `The Post (Athens) 2026-08-25 (https://www.thepostathens.com/article/2026/08/ohio-season-preview-nick-poulos-named-starter)` |
| `K113` | `2026-08-03` | `2026-08-25` |
| `L113` | prior note | activation note recording the attribution gap |

## C.6 Oregon State — row 76 — **see A.3.1; two options, no default**

| Cell | Current | Option A (zeros) | **Option B (recommended)** |
|---|---|---|---|
| `C76` | *(blank)* | `Maalik Murphy` | `Maalik Murphy` |
| `D76` | *(blank)* | **`0`** | *(stays blank)* |
| `E76` | `Maalik Murphy (leader; Braden Atkinson pushing)` | `Braden Atkinson` | `Braden Atkinson` |
| `F76` | *(blank)* | **`0`** | *(stays blank)* |
| `H76` | `M` | `M` unchanged | `M` unchanged |
| `I76` | Athlon/ESPN/CBS Pac-12 previews | Columbia County Spotlight / Portland Tribune 2026-08-24 URL | same |
| `K76` | `2026-08-03` | `2026-08-24` | `2026-08-24` |
| `L76` | prior note | activation note + explicit zero-deviation assumption | correction note + deferred valuation |

---

# PART D — TEXT CORRECTIONS (no status, numeric, formula or model change)

All three stay `L` / UNCERTAIN. `G`/`M` **DO-NOT-WRITE** on every row. `C`, `D`, `F`, `H`, `J`: no change.

## D.1 Memphis — row 85

| Cell | Current | Proposed |
|---|---|---|
| `E85` | `Marcus Stokes` | `Open (Marcus Stokes / Air Noland)` |
| `I85` | `Underdog Dynasty/Yahoo (American 2026 QB projections)` | `Daily Memphian / Yahoo Sports beat reporting, 2026-08-24 (https://sports.yahoo.com/articles/charles-huff-name-starting-quarterback-012920149.html)` |
| `K85` | `2026-08-04` | `2026-08-24` |
| `L85` | prior note | append correction note (Huff: *"You guys won't know until they flip the coin"*) |

## D.2 Vanderbilt — row 21

| Cell | Current | Proposed |
|---|---|---|
| `E21` | `Jared Curtis` | `Open (Jared Curtis / Blaze Berlowitz / Whit Muschamp)` |
| `I21` | `Sports Illustrated (SEC QB projections)` | `On3 + SI Vanderbilt + WSMV fall-camp reporting, 2026-08 (https://www.wsmv.com/2026/08/05/quarterback-competition-continues-dores-open-practice/)` |
| `K21` | `2026-08-04` | `2026-08-24` |
| `L21` | prior note | append correction note (three-way; neither separated in 15 practices; Lea names privately) |

## D.3 Kansas — row 48

| Cell | Current | Proposed |
|---|---|---|
| `E48` | `Cole Ballard (leader; Isaiah Marshall competing)` | `Open (Cole Ballard / Isaiah Marshall)` |
| `I48` | `Sports Illustrated (Big 12 QB projections)` | `Yahoo Sports + WIBW fall-camp reporting, 2026-08 (https://www.wibw.com/2026/08/05/kus-quarterback-race-remains-open/)` |
| `K48` | `2026-08-03` | `2026-08-24` |
| `L48` | prior note | append correction note (Leipold: *"very, very competitive"*; no timetable) |

## D.4 South Florida — row 89 — **NEW FLAG, no proposal yet**

`E89` reads `OPEN (Kromenhoek / Van Buren Jr. / Cooper)`. The Tampa Bay Times (2026-08-10) has it
**down to two** — Kromenhoek and Van Buren — and USF's own camp-opening release names only those two.
"Cooper" may be stale. I am **not** proposing a cell change without a dated source that settles it.
Tell me if you want it pursued.

---

# PART E — ALL NUMERICAL ENTRIES, COMPLETE

| Cell | Value | Row | Included in |
|---|:--:|---|---|
| `D91` `F91` | **`0`**, **`0`** | Tulane | always |
| `D7` `F7` | **`0`**, **`0`** | Arkansas | always |
| `D9` `F9` | **`0`**, **`0`** | Florida | always |
| `D29` `F29` | **`0`**, **`0`** | Nebraska | always |
| `D113` `F113` | **`0`**, **`0`** | Ohio | only if Ohio approved |
| `D76` `F76` | **`0`**, **`0`** | Oregon State | **only under Option A** |

**Maximum 12 numerical entries. Every one is the integer `0`. Zero nonzero QB values are proposed
anywhere.** Parts D contributes **none**. Each activated row yields `G = 0 − 0 = 0`, so `ENGINE!M`
contributes exactly nothing to any of the 888 games, and all five reference spreads
(`MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` · `SJSU at USC -35.2` ·
`HAW at STAN -3.7`) are unchanged under every scenario.

---

# PART F — CENSUS, RECOMPUTED DIRECTLY FROM ALL 138 ROWS

Each row re-evaluated through `UNCERTAIN if (G blank OR H="L" OR J≠2026)`. No projection reused.

| Scenario | Status | Confidence |
|---|:--:|:--:|
| **v0.8.6 now (frozen)** | 110 OK / 28 UNCERTAIN | 73 H / 40 M / 25 L |
| **RECOMMENDED** — Tulane + Arkansas + Florida + Nebraska, Oregon State Option B, Ohio held | **114 OK / 24 UNCERTAIN** | **76 H / 41 M / 21 L** |
| + Ohio approved | 115 OK / 23 UNCERTAIN | 76 H / 41 M / 21 L |
| + Oregon State Option A instead of B | 115 OK / 23 UNCERTAIN | 76 H / 41 M / 21 L |
| + both Ohio and Oregon State Option A | 116 OK / 22 UNCERTAIN | 76 H / 41 M / 21 L |
| Total (every scenario) | **138** | **138** |

**Confidence is `76 H / 41 M / 21 L` under all five scenarios.** Only four rows move a confidence
code — Arkansas, Florida and Nebraska each `L → H` (+3 H, −3 L) and Tulane `L → M` (+1 M, −1 L).
Oregon State and Ohio are already `M`, so they move status only.

Part D moves nothing: **110 OK / 28 UNCERTAIN and 73 H / 40 M / 25 L are unchanged by the three text
corrections.**

---

# PART G — DECISIONS REQUESTED

1. **Tulane, Arkansas, Florida, Nebraska** — activate as specified? *(recommended: yes)*
2. **Oregon State** — Option A (zeros) or **Option B (record-only, recommended)**?
3. **Ohio** — approve at `M`, or **hold** for attribution? *(recommended: hold)*
4. **Memphis, Vanderbilt, Kansas** text corrections — apply?
5. **South Florida** — pursue the stale-candidate flag?

**Nothing has been applied. v0.8.6 remains frozen and untouched. The QB closeout is NOT complete.**
