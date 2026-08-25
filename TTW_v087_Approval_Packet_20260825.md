# TTW NCAAF 2026 — v0.8.7 APPROVAL PACKET

**Cutoff:** 2026-08-25 (America/New_York)
**Status:** **READ-ONLY. NOTHING APPLIED.** No production write.
**Base:** v0.8.6 AUTHORITATIVE, **frozen** — SHA-256
`bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` *(re-verified this session)*
**Scope:** **6 activations + 1 record-only correction + 3 text corrections.**
**Schedule work:** excluded by design — `schedule_candidate_v1/`, see Part 9.

---

## PART 0 — THE SOURCE-RULE INCONSISTENCY, ACKNOWLEDGED

You were right, and on both counts I had the facts wrong, not merely the judgement.

| | What I said | What is true |
|---|---|---|
| **Ohio** | "attribution is not stated… recommend holding" | **ESPN's Pete Thamel reported the naming**, announced Saturday **2026-08-22**. I had read only The Post's season preview, which carries no attribution, and never opened the Yahoo report that does. |
| **South Florida** | "soft, reporter-sourced… not activatable" | **Thamel, verbatim: "Sources: USF has named Michael Van Buren Jr. the school's starting quarterback."** 2026-08-24. Identical construction to Georgia Southern, Rutgers and Tulane. |

I applied a **stricter** standard to Ohio and USF than the precedent I had myself set for Georgia
Southern, North Carolina, Rutgers and Tulane. That is the inconsistency. Both qualify at **`M`**.

**A third correction, mine:** I flagged `Cooper` in USF's field as possibly stale. He is **KJ Cooper**,
a real competitor alongside Kromenhoek and Jayden Bradford. The recorded field was correct.

---

## PART 1 — OHIO, row 113 — **ACTIVATE at `M`**

### 1.1 Baseline determination → **MATCH. Zeros apply.**

The row's own note reads: *"HC John Hauser says **Nick Poulos 'is still in the lead'** for the starting
job."* Poulos was the coach-described leader — the quarterback the preseason blend assumed. The naming
**confirms** that assumption rather than departing from it, so the deviation is genuinely zero and
`0/0` is correct. This is the Tulane/Rutgers pattern, **not** the Oregon State pattern.

### 1.2 Complete current → proposed

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `A113` | `=IF('TEAM RATINGS'!$A113="","",'TEAM RATINGS'!$A113)` | **DO-NOT-WRITE** | formula |
| `B113` | `=IF('TEAM RATINGS'!$A113="","",'TEAM RATINGS'!$B113)` | **DO-NOT-WRITE** | formula |
| `C113` | *(blank)* | `Nick Poulos` | text |
| `D113` | *(blank)* | **`0`** | **numeric** |
| `E113` | `Nick Poulos (leader; not yet named)` | `Nick Poulos` | text |
| `F113` | *(blank)* | **`0`** | **numeric** |
| `G113` | `=IF(OR($D113="",$F113=""),"",$F113-$D113)` | **DO-NOT-WRITE** → computes `0` | formula |
| `H113` | `M` | `M` — **unchanged** | confidence |
| `I113` | `RotoWire MAC spring / Ohio Athletics (https://www.rotowire.com/cfootball/article/spring-practice-storylines-mid-american-conference-106501)` | `ESPN / Pete Thamel 2026-08-22 (https://sports.yahoo.com/articles/nick-poulos-wins-ohio-starting-004242764.html)` | metadata |
| `J113` | `2026` | **DO-NOT-REWRITE** | — |
| `K113` | `2026-08-03` | `2026-08-25` | metadata |
| `L113` | 2026-08-03 verification note | activation note (below) | text |
| `M113` | `=IF($A113="","",IF(OR($G113="",$H113="L",$J113<>SETTINGS!$B$3),"UNCERTAIN","OK"))` | **DO-NOT-WRITE** → resolves `OK` | formula |

**Source / date:** ESPN — Pete Thamel · naming announced **2026-08-22** · **Confidence `M`**
(reporter-sourced; no official depth chart located).
**Corroboration:** the naming specifies Week 1 **in Lincoln against Nebraska**. The workbook confirms:
`wk1 2026-09-05 Ohio Bobcats @ Nebraska Cornhuskers` — and independently cross-checks the Nebraska
activation in Part 4.3.

**Proposed `L113`:**

> `2026-08-25 ACTIVATED, confidence M (UNCHANGED from M). ESPN's Pete Thamel reported that Ohio named graduate student Nick Poulos its starting quarterback, announced Saturday 2026-08-22 by first-year HC John Hauser. M rather than H because this is a reporter-sourced naming rather than a team release or a coach announcement carried first-party, matching the precedent used for Georgia Southern, North Carolina, Rutgers, Tulane and South Florida. SUPERSEDES the 2026-08-03 entry, which recorded Hauser calling Poulos 'still in the lead' with no Week 1 starter named. BASELINE MATCH: Poulos was already the coach-described leader, so the confirmed starter IS the quarterback the preseason rating assumed and no deviation applies. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: the report that Ohio opens week one in Lincoln against Nebraska matches IMPORT SCHEDULE exactly (wk1 2026-09-05 Ohio Bobcats @ Nebraska Cornhuskers). Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. No nonzero QB adjustment and no model change.`

---

## PART 2 — SOUTH FLORIDA, row 89 — **ACTIVATE at `M`**

### 2.1 Baseline determination → **MATCH. Zeros apply.**

The row's own note reads: *"**Van Buren 'seems to have the edge'** on slightly more game experience,
but that is a preseason projection, not a staff decision."* That sentence was written to justify
withholding activation — but it is exactly the test for the **baseline**: column `C` records the
quarterback the preseason blend assumed, and the preseason projection had Van Buren ahead. The naming
confirms the assumption. **`0/0` applies.**

### 2.2 Complete current → proposed

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `A89` | `=IF('TEAM RATINGS'!$A89="","",'TEAM RATINGS'!$A89)` | **DO-NOT-WRITE** | formula |
| `B89` | `=IF('TEAM RATINGS'!$A89="","",'TEAM RATINGS'!$B89)` | **DO-NOT-WRITE** | formula |
| `C89` | *(blank)* | `Michael Van Buren Jr.` | text |
| `D89` | *(blank)* | **`0`** | **numeric** |
| `E89` | `OPEN (Kromenhoek / Van Buren Jr. / Cooper)` | `Michael Van Buren Jr.` | text |
| `F89` | *(blank)* | **`0`** | **numeric** |
| `G89` | `=IF(OR($D89="",$F89=""),"",$F89-$D89)` | **DO-NOT-WRITE** → computes `0` | formula |
| `H89` | `L` | **`M`** | confidence |
| `I89` | `Yahoo (USF lands portal QB) / Green Gold & Bold (https://sports.yahoo.com/articles/usf-lands-quarterback-transfer-portal-132621762.html)` | `ESPN / Pete Thamel 2026-08-24 (https://www.saturdaydownsouth.com/news/college-football/former-sec-qb-michael-van-buren-wins-fbs-starting-job-per-report/)` | metadata |
| `J89` | `2026` | **DO-NOT-REWRITE** | — |
| `K89` | `2026-08-04` | `2026-08-25` | metadata |
| `L89` | 2026-08-04 verification note | activation note (below) | text |
| `M89` | `=IF($A89="","",IF(OR($G89="",$H89="L",$J89<>SETTINGS!$B$3),"UNCERTAIN","OK"))` | **DO-NOT-WRITE** → resolves `OK` | formula |

**Source / date:** ESPN — Pete Thamel, **2026-08-24**, verbatim: *"**Sources:** USF has named Michael
Van Buren Jr. the school's starting quarterback."* · **Confidence `M`**.
**Corroboration:** Van Buren beat out Luke Kromenhoek, Jayden Bradford and KJ Cooper; opener vs FIU
matches the workbook: `wk1 2026-09-05 Florida International Panthers @ South Florida Bulls`.

> **One honest qualification.** You noted the naming was *acknowledged by USF Athletics*. I could not
> independently verify that acknowledgment in any source I was able to fetch — the article I retrieved
> explicitly does not mention it. **This does not change the outcome**, since an official acknowledgment
> would only argue for `H`, and `M` is what is proposed. Recorded so the packet does not assert
> something I did not see.

**Proposed `L89`:**

> `2026-08-25 ACTIVATED, confidence L -> M. ESPN's Pete Thamel, 2026-08-24: 'Sources: USF has named Michael Van Buren Jr. the school's starting quarterback.' Van Buren, a junior transfer from LSU and Mississippi State with 17 career games and 2,896 passing yards, beat out Luke Kromenhoek, Jayden Bradford and KJ Cooper. M rather than H because this is a reporter-sourced naming; a reported acknowledgment by USF Athletics could not be independently verified and is NOT relied on. Matches the precedent used for Georgia Southern, North Carolina, Rutgers, Tulane and Ohio. SUPERSEDES the 2026-08-04 entry, which recorded an open Kromenhoek-vs-Van Buren competition. BASELINE MATCH: that entry already recorded Van Buren as holding 'the edge' in the preseason projection, so the confirmed starter IS the quarterback the preseason rating assumed and no deviation applies. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: the reported FIU opener matches IMPORT SCHEDULE exactly (wk1 2026-09-05 Florida International Panthers @ South Florida Bulls). Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. No nonzero QB adjustment and no model change.`

---

## PART 3 — OREGON STATE, row 76 — **OPTION B ONLY: record-only, values blank, stays UNCERTAIN**

### 3.1 Complete current → proposed

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `A76` `B76` | *(TEAM MAP formulas)* | **DO-NOT-WRITE** | formula |
| `C76` | *(blank)* | `Maalik Murphy` — **the preseason baseline, preserved** | text |
| `D76` | *(blank)* | **NO CHANGE — stays blank** | — |
| `E76` | `Maalik Murphy (leader; Braden Atkinson pushing)` | `Braden Atkinson` | text |
| `F76` | *(blank)* | **NO CHANGE — stays blank** | — |
| `G76` | `=IF(OR($D76="",$F76=""),"",$F76-$D76)` | **DO-NOT-WRITE** → stays blank | formula |
| `H76` | `M` | `M` — **unchanged** | confidence |
| `I76` | `Athlon/ESPN/CBS Pac-12 2026 previews (https://www.espn.com/college-football/story/_/id/48892618/...)` | `ESPN / Pete Thamel via Columbia County Spotlight + Portland Tribune 2026-08-24 (https://columbiacountyspotlight.com/2026/08/24/oregon-state-names-braden-atkinson-starting-qb/)` | metadata |
| `J76` | `2026` | **DO-NOT-REWRITE** | — |
| `K76` | `2026-08-03` | `2026-08-25` | metadata |
| `L76` | 2026-08-03 note | correction note (below) | text |
| `M76` | `=IF($A76="","",IF(OR($G76="",$H76="L",$J76<>SETTINGS!$B$3),"UNCERTAIN","OK"))` | **DO-NOT-WRITE** → stays **UNCERTAIN** | formula |

**No numerical entry. No status change. `G76` stays blank, so the row remains UNCERTAIN by design.**

**Why Oregon State is treated differently from Ohio and USF:** for those two the named starter *was*
the presumptive leader, so a zero deviation is literally true. Here **Atkinson displaced the incumbent
the preseason priced** — Murphy. `C76` preserves Murphy as the baseline and `E76` records Atkinson as
active; the valuation of that swap is deferred rather than silently set to zero.

**Proposed `L76`:**

> `2026-08-25 RECORD CORRECTION - STARTER CHANGED, VALUATION DEFERRED (confidence M UNCHANGED, numerical values REMAIN BLANK, status stays UNCERTAIN). ESPN's Pete Thamel reported 2026-08-24 that Oregon State named BRADEN ATKINSON its starting quarterback for week one at Houston; Atkinson, a Mercer transfer and the reigning Jerry Rice Award winner, beat out incumbent MAALIK MURPHY and Brady Jones. A local report adds that the Oregon State football account subsequently confirmed it, but that first-party act is secondhand and is NOT relied on -> M, not H. SUPERSEDES the 2026-08-03 entry, which recorded Murphy as the leader. BASELINE MISMATCH - THE REASON NO ZEROS ARE WRITTEN: this is the first row in the project where the named starter is NOT the quarterback the preseason blend assumed. Column C preserves MAALIK MURPHY as the preseason baseline because the preseason rating priced Oregon State with Murphy, its returning starter. Writing 0/0 would assert that the Murphy-to-Atkinson change is worth exactly zero, which is a valuation claim the deviation-only convention was never intended to carry. Values therefore REMAIN BLANK and the row stays UNCERTAIN pending the QB-value rubric. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: the reported week-one game at Houston matches IMPORT SCHEDULE exactly (wk1 2026-09-05 Oregon State Beavers @ Houston Cougars, TDECU Stadium). RECHECK: official Oregon State depth chart, and the QB-value rubric.`

---

## PART 4 — THE OTHER FOUR ACTIVATIONS

Formula cells on every row: `A`, `B`, `G`, `M` **DO-NOT-WRITE**; `J` = `2026` **DO-NOT-REWRITE**.

### 4.1 Tulane — row 91 — `L → M` · ESPN/Thamel **2026-08-24**

| Cell | Current | Proposed |
|---|---|---|
| `C91` | *(blank)* | `Zeon Chriss-Gremillion` |
| `D91` | *(blank)* | **`0`** |
| `E91` | `Open (Semonza / Chriss-Gremillion / Johnson / Bruno)` | `Zeon Chriss-Gremillion` |
| `F91` | *(blank)* | **`0`** |
| `H91` | `L` | **`M`** |
| `I91` | `FOX 8 New Orleans, 2026-07-24 (https://www.fox8live.com/2026/07/24/four-qbs-battling-starting-spot-tulane/)` | `ESPN / Pete Thamel 2026-08-24, carried by On3 (https://www.on3.com/news/tulane-names-zeon-chriss-gremillion-starting-quarterback-for-season-opener/)` |
| `K91` | `2026-08-21` | `2026-08-25` |
| `L91` | prior note | activation note |

Baseline match: the prior note recorded the job "defaults to Chriss-Gremillion if no one separates."

### 4.2 Arkansas — row 7 — `L → H` · team announcement **2026-08-23**, reported **2026-08-24**

| Cell | Current | Proposed |
|---|---|---|
| `C7` | `KJ Jackson` | **NO CHANGE — already the baseline** |
| `D7` | *(blank)* | **`0`** |
| `E7` | `Open (KJ Jackson / AJ Hill)` | `KJ Jackson` |
| `F7` | *(blank)* | **`0`** |
| `H7` | `L` | **`H`** |
| `I7` | `Sports Illustrated (SEC QB projections)` | `Yahoo Sports / Whole Hog Sports 2026-08-24 (https://sports.yahoo.com/articles/why-arkansas-football-chose-kj-091055884.html)` |
| `K7` | `2026-08-03` | `2026-08-25` |
| `L7` | prior note | activation note |

`H`: *"the Hogs made things official on Sunday, Aug. 23, labeling Jackson as the starter"* + HC Ryan
Silverfield on the record. Deviation **literally zero** — `C7` already held KJ Jackson.

### 4.3 Florida — row 9 — `L → H` · **2026-08-24**

| Cell | Current | Proposed |
|---|---|---|
| `C9` | *(blank)* | `Aaron Philo` |
| `D9` | *(blank)* | **`0`** |
| `E9` | `Aaron Philo` | `Aaron Philo` |
| `F9` | *(blank)* | **`0`** |
| `H9` | `L` | **`H`** |
| `I9` | `Sports Illustrated (SEC QB projections)` | `Official Florida Athletics 2026-08-24 (https://floridagators.com/news/2026/8/24/football-philo-moves-to-top-of-qb-depth-chart-aug-24-2026); HC Jon Sumrall announcement (https://www.alligator.org/article/2026/08/aaron-philo-starting-quarterback)` |
| `K9` | `2026-08-04` | `2026-08-25` |
| `L9` | prior note | activation note, incl. Sumrall's *"this is not an anointing"* caveat verbatim |

`H`: official athletics release **and** a head-coach announcement. Baseline match — the prior note
recorded Philo as FAVORED, holding "the edge entering fall camp."

### 4.4 Nebraska — row 29 — `L → H` · Rhule announced **2026-08-22**

| Cell | Current | Proposed |
|---|---|---|
| `C29` | *(blank)* | `Anthony Colandrea` |
| `D29` | *(blank)* | **`0`** |
| `E29` | `Anthony Colandrea` | `Anthony Colandrea` |
| `F29` | *(blank)* | **`0`** |
| `H29` | `L` | **`H`** |
| `I29` | `Sports Illustrated (Big Ten QB projections)` | `HC Matt Rhule announcement 2026-08-22, reported 2026-08-24 (https://klin.com/2026/08/24/colandrea-named-starting-qb-for-opener/)` |
| `K29` | `2026-08-04` | `2026-08-25` |
| `L29` | prior note | activation note |

`H`: head-coach announcement, same tier as Alabama/DeBoer, Tennessee/Heupel, Florida/Sumrall.
Corroborated: opener vs **Ohio** — the mirror image of Part 1's corroboration.

---

## PART 5 — EVERY NUMERICAL ENTRY

| # | Cell | Value | Row |
|:--:|---|:--:|---|
| 1–2 | `D91` `F91` | **`0`** `0` | Tulane |
| 3–4 | `D7` `F7` | **`0`** `0` | Arkansas |
| 5–6 | `D9` `F9` | **`0`** `0` | Florida |
| 7–8 | `D29` `F29` | **`0`** `0` | Nebraska |
| 9–10 | `D113` `F113` | **`0`** `0` | Ohio |
| 11–12 | `D89` `F89` | **`0`** `0` | South Florida |

**Exactly 12 numerical entries across the six activations. Every one is the integer `0`.**
Oregon State contributes **none**. Parts 7 contribute **none**. **Zero nonzero QB values anywhere.**

Each activated row yields `G = 0 − 0 = 0`, so `ENGINE!M` contributes exactly nothing to any of the
888 games, and all five reference spreads are unchanged: `MEM at UNLV -5.6` · `UNC at TCU -4.2` ·
`NMSU at FSU -27.7` · `SJSU at USC -35.2` · `HAW at STAN -3.7`.

---

## PART 6 — CENSUS, COMPUTED DIRECTLY FROM ALL 138 ROWS

Every row re-evaluated through `UNCERTAIN if (G blank OR H="L" OR J≠2026)`. **Nothing assumed.**

| | v0.8.6 (frozen) | **v0.8.7** | Δ |
|---|:--:|:--:|:--:|
| **OK** | 110 | **116** | +6 |
| **UNCERTAIN** | 28 | **22** | −6 |
| **`H`** | 73 | **76** | +3 |
| **`M`** | 40 | **42** | +2 |
| **`L`** | 25 | **20** | −5 |
| Total | 138 | **138** | — |
| Nonzero QB values | 0 | **0** | — |

**Status `116 OK / 22 UNCERTAIN` — matches your expectation exactly.**
**Confidence computed, not assumed: `76 H / 42 M / 20 L`.**

Derivation — five confidence codes move: Arkansas, Florida, Nebraska each `L → H` (+3 `H`, −3 `L`);
Tulane and South Florida each `L → M` (+2 `M`, −2 `L`). Ohio was already `M` and Oregon State stays
`M`, so both move status only — and Oregon State does not even do that.

**Baseline-QB invariant verified:** after v0.8.7, **0 OK rows carry a blank column `C`** (116/116).

### The 22 rows remaining UNCERTAIN

| Row | Team | Conf | Row | Team | Conf |
|:--:|---|:--:|:--:|---|:--:|
| 21 | Vanderbilt | `L` | 112 | Miami (OH) | `L` |
| 24 | Iowa | `L` | 120 | Nevada | `L` |
| 48 | Kansas | `L` | 123 | Northern Illinois | `L` |
| 52 | **Texas Tech** | `H` *(medically gated)* | 125 | UNLV | `L` |
| 74 | Colorado State | `L` | 128 | Appalachian State | `L` |
| 75 | Fresno State | `L` | 129 | Arkansas State | `L` |
| 76 | **Oregon State** | `M` *(valuation deferred)* | 130 | Coastal Carolina | `L` |
| 85 | Memphis | `L` | 139 | Southern Miss | `L` |
| 99 | Liberty | `L` | 143 | UConn | `L` |
| 105 | Akron | `L` | 106 | Ball State | `L` |
| 108 | Buffalo | `L` | 109 | Central Michigan | `L` |

---

## PART 7 — TEXT CORRECTIONS, ECHOED EXACTLY

No status, numeric, formula or model change. All three stay `L` / UNCERTAIN.
`C`, `D`, `F`, `H`, `J` unchanged on every row; `G`, `M` **DO-NOT-WRITE**.

### 7.1 Memphis — row 85

| Cell | Current | Proposed |
|---|---|---|
| `E85` | `Marcus Stokes` | `Open (Marcus Stokes / Air Noland)` |
| `I85` | `Underdog Dynasty/Yahoo (American 2026 QB projections)` | `Daily Memphian / Yahoo Sports beat reporting, 2026-08-24 (https://sports.yahoo.com/articles/charles-huff-name-starting-quarterback-012920149.html)` |
| `K85` | `2026-08-04` | `2026-08-25` |
| `L85` | prior note | append correction note — two-man race with Air Noland; HC Charles Huff: *"You guys won't know until they flip the coin."* Memphis may stay UNCERTAIN into Week 0 by design. |

### 7.2 Vanderbilt — row 21

| Cell | Current | Proposed |
|---|---|---|
| `E21` | `Jared Curtis` | `Open (Jared Curtis / Blaze Berlowitz / Whit Muschamp)` |
| `I21` | `Sports Illustrated (SEC QB projections)` | `On3 + SI Vanderbilt + WSMV fall-camp reporting, 2026-08 (https://www.wsmv.com/2026/08/05/quarterback-competition-continues-dores-open-practice/)` |
| `K21` | `2026-08-04` | `2026-08-25` |
| `L21` | prior note | append correction note — three-way; neither Curtis nor Berlowitz separated in 15 practices; HC Clark Lea will name privately. |

### 7.3 Kansas — row 48

| Cell | Current | Proposed |
|---|---|---|
| `E48` | `Cole Ballard (leader; Isaiah Marshall competing)` | `Open (Cole Ballard / Isaiah Marshall)` |
| `I48` | `Sports Illustrated (Big 12 QB projections)` | `Yahoo Sports + WIBW fall-camp reporting, 2026-08 (https://www.wibw.com/2026/08/05/kus-quarterback-race-remains-open/)` |
| `K48` | `2026-08-03` | `2026-08-25` |
| `L48` | prior note | append correction note — HC Lance Leipold: *"very, very competitive"*; no timetable; Chase Jenkins in the room but **not** in the active field. |

---

## PART 8 — FORMULA CELLS, CONSOLIDATED

**DO-NOT-WRITE on every affected row** — 7, 9, 21, 29, 48, 76, 85, 89, 91, 113:

| Cell | Formula |
|---|---|
| `A{row}` | `=IF('TEAM RATINGS'!$A{row}="","",'TEAM RATINGS'!$A{row})` |
| `B{row}` | `=IF('TEAM RATINGS'!$A{row}="","",'TEAM RATINGS'!$B{row})` |
| `G{row}` | `=IF(OR($D{row}="",$F{row}=""),"",$F{row}-$D{row})` |
| `M{row}` | `=IF($A{row}="","",IF(OR($G{row}="",$H{row}="L",$J{row}<>SETTINGS!$B$3),"UNCERTAIN","OK"))` |

`J{row}` = `2026` on every affected row: **DO-NOT-REWRITE.**
Plus `START HERE!A1` — version identifier and confidence census — the only cell outside `QB VALUES`.

**Total cells: 10 rows × writable cells + banner.** Activations write `C`,`D`,`E`,`F`,`H`,`I`,`K`,`L`
(fewer where a cell is already correct: `C7` and `H113` are not written); Oregon State writes
`C`,`E`,`I`,`K`,`L`; text corrections write `E`,`I`,`K`,`L`.

---

## PART 9 — SCHEDULE CANDIDATE: SEPARATE, AND SEQUENCED AFTER v0.8.7

`schedule_candidate_v1/` stays **completely separate** from this packet and is **not promoted**.

**Agreed sequence, on your approval of v0.8.7:**

1. Promote **v0.8.7** with its own `verify_v087.py` identity certificate.
2. **Then** rebase the schedule candidate onto v0.8.7:
   `python3 schedule_candidate_v1/build_schedule_candidate.py --source promotion_v0.8.7/…v0.8.7_AUTHORITATIVE.xlsx`
3. Re-run the **41-check certificate** `verify_schedule_candidate.py`, updating only its base SHA and
   the QB-census expectations to v0.8.7's `116 OK / 22 UNCERTAIN` and `76 H / 42 M / 20 L`.
4. Re-run the **full validator chain**: `verify_v087`, `verify_v086`, `verify_v085`, `verify_v084`,
   `verify_v083`, `verify_v082`, `verify_v081`, Week 0 dry run, `validate_schedule.py`,
   `test_pipeline.py`, `git diff --check`.

**The 133 date corrections are unchanged by the rebase** — they touch `IMPORT SCHEDULE!D` only, and
v0.8.7 touches only `QB VALUES` and the banner. The two changesets are disjoint.

**The 403 placeholder-time games will NOT be altered.** They carry `timeValid = false`, already hold
the correct Eastern date, and remain flagged `needs_rederivation` for the day ESPN publishes real
kickoff times. No proposal in this packet or the candidate touches them.

---

## PART 10 — DECISIONS REQUESTED

| # | Item | Proposal |
|:--:|---|---|
| 1 | **Six activations** — Tulane `M`, Arkansas `H`, Florida `H`, Nebraska `H`, Ohio `M`, South Florida `M` | approve → 12 zeros |
| 2 | **Oregon State** record-only, Option B | approve → no zeros, stays UNCERTAIN |
| 3 | **Memphis, Vanderbilt, Kansas** text corrections | approve → no census movement |
| 4 | **Schedule candidate** | hold until after v0.8.7, then rebase per Part 9 |

**Nothing applied. v0.8.6 remains frozen and untouched. The QB closeout is NOT complete** — 22 rows
remain UNCERTAIN, including Texas Tech's medical gate and Oregon State's deferred valuation.
