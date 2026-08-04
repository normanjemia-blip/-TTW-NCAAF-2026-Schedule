# Phase 7D.3A — Batch 2 Straggler Resolution

**Date:** 2026-08-03 (America/New_York) · **Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.6_CANDIDATE.xlsx`
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.5:** unmodified · **Google Sheet:** never accessed · **NOT promoted.**

## Recommendation: **OPTION A — PROCEED TO FINAL G5 BATCH**

All seven stragglers **resolved** (none left as "unable to verify"), all regressions
pass, no structural issue, and the remaining backlog is **Group of Five only**.

**Two genuine defects were found and corrected** — Arkansas and UConn were both
carrying `M` codes that the evidence does not support.

## 1. Seven-team starting state (reproduced from v0.7.5)

| Team | Conf | Row | Code | D/F | Projected QB | Last verified | Unresolved reason |
|---|---|---:|---|---|---|---|---|
| Arkansas | SEC | 7 | M | 0/0 | KJ Jackson | 2026-07-21 | never live-verified |
| Mississippi State | SEC | 13 | M | 0/0 | Kamario Taylor | 2026-07-21 | never live-verified |
| Iowa | Big Ten | 24 | L | blank | Jeremy Hecklinski | 2026-07-21 | never live-verified |
| Houston | Big 12 | 46 | M | 0/0 | Conner Weigman | 2026-07-21 | never live-verified |
| Kansas | Big 12 | 48 | L | blank | Cole Ballard | 2026-07-21 | never live-verified |
| Duke | ACC | 59 | M | 0/0 | Walker Eget | 2026-07-21 | **CONFLICT** — Eget unconfirmed |
| UConn | Independent | 143 | M | 0/0 | Tucker McDonald | 2026-07-21 | never live-verified |

Machine-readable copies: `batch2_stragglers_starting_state.json` / `.csv`.

## 2. Seven team-specific verification reports

### Arkansas (row 7) — **DEFECT: M → L**
HC **Ryan Silverfield** ([Whole Hog Sports, 2026-08-03](https://www.wholehogsports.com/news/2026/aug/03/arkansas-football-ryan-silverfield-razorbacks-quarterback-qb-battle-kj-jackson-aj-hill/) — the Arkansas beat outlet, published **today**) says the **KJ Jackson vs. AJ Hill** battle **"could last until the Sept. 5 season opener"** vs North Alabama. He and OC Tim Cramsey called it **"wide open"** in February.
*Jackson:* RS-So, 4-star 2024, 33/54 (61%) 441 yds, 3 TD, 0 INT in 2025; 11 rush/52 yds/2 TD.
*Hill:* 6-4 232 RS-Fr, **Memphis transfer** (followed Silverfield), consensus 4-star 2025, two years in Cramsey's system.
→ Genuine open competition. **M is unsupportable → L.** Zeros cleared to blank.

### UConn (row 143) — **DEFECT: M → L**
The candidate named **Tucker McDonald** — **no located source corroborates him.** Verified instead: **Jim Mora left UConn for the Colorado State head job**; UConn's **2026 QB commit departed** after Mora's exit; and **2025 starter Joe Fagnano** (2,529 yds, 22 TD through nine games) was a **senior** and is gone.
→ **Projected starter cannot be verified** — the explicit L standard. **M → L.** Zeros cleared.
*(Side note for the G5 batch: Mora's move makes **Colorado State** a coaching-change team.)*

### Houston (row 46) — **UPGRADE: M → H**
**Conner Weigman** is the **returning starter entering his second season** at Houston; confirmed on the **official uhcougars.com roster**; publicly announced his return; coach praise reported for his offseason bounce-back; **no competition reported in any located source**.
→ Established healthy returning starter, no credible competition → **H**. This is the "returning starter" branch, **not** a media projection. **Zero initialization retained** (correct for H); status stays **OK**.

### Mississippi State (row 13) — **UPGRADE: M → H**
**Kamario Taylor** arrived at SEC Media Days as Mississippi State's **"unquestioned starter — no competition, no committee, no asterisk"**; described as **entrenched**, with only the **No. 2 job** open in fall camp. Confirmed on the **official hailstate.com roster** and in official MSU releases; new QB coach **Kevin Johns** calls him "very, very special." True-freshman production: 629 pass yds, 458 rush yds, incl. **173 rushing vs Ole Miss in his first career start**.
→ Settled starter → **H**. Zeros retained; status **OK**.

### Duke (row 59) — **CONFLICT RESOLVED, M CONFIRMED**
**Walker Eget is on the official Duke roster** (goduke.com), a **San Jose State transfer** who committed in **Jan 2026** ([Duke Chronicle](https://dukechronicle.com/article/duke-football-commitment-brief-walker-eget-manny-diaz-mensah-barkate-spartans-san-jose-state-20260126)), and is **expected to be Duke's Week 1 starter** after Mensah left for Miami. **Manny Diaz** expects him to be a **full participant in fall camp**. He competes with transfers **Blaine Hipa** and **Ari Patu** plus returners **Terry Walker III** and **Dan Mahan**. SJSU career: 5,555 yds, 30 TD, 19 INT.
→ Clear leader inside a **five-way competition** → **M retained (not H)**. The 7D.3 conflict is **closed, and the candidate entry was correct.**

### Iowa (row 24) — **L CONFIRMED**
HC **Kirk Ferentz has not decided** between **Jeremy Hecklinski** and **Hank Brown**; coaches have **consistently split first-team reps** with **"little separation"**; Ferentz says a decision may come in August but **"may be in-season."** Both spent 2025 learning OC **Tim Lester's** system behind Mark Gronowski. *(Sources: hawkcentral/Des Moines Register, OurQuadCities, Western Iowa Today 2026-08-02.)*
→ **L retained**; entry refined from one name to the real two-man race.

### Kansas (row 48) — **L CONFIRMED**
**Cole Ballard "may be"** Kansas's QB1 (SI's own hedged wording) replacing Jalon Daniels, with **real competition from Isaiah Marshall** — Ballard the better thrower, Marshall the better runner; Kansas QBs "totally fine with competition heading into camp." Ballard confirmed on the **official kuathletics.com roster**. **No naming by Lance Leipold located.**
→ **L retained.** This **vindicates the Phase 7D.3 decision** not to upgrade Kansas off a national projected-starter list.

## 3. QB correction log

| Team | Row | Prior starter | Corrected | Prior→New code | Prior→New D/F | Reason | Source | Date | Downstream |
|---|---:|---|---|---|---|---|---|---|---|
| **Arkansas** | 7 | KJ Jackson | **Open (KJ Jackson / AJ Hill)** | **M → L** | **0/0 → blank** | HC: battle may run to the Sept 5 opener; "wide open" since Feb | Whole Hog Sports 2026-08-03 | 2026-08-03 | OK → **UNCERTAIN** |
| **UConn** | 143 | Tucker McDonald | **Unverified (room in flux)** | **M → L** | **0/0 → blank** | Name uncorroborated; HC left for Colorado State; QB commit gone; 2025 starter graduated | SI UConn; UConn athletics | 2026-08-03 | OK → **UNCERTAIN** |
| **Houston** | 46 | Conner Weigman | *unchanged* | **M → H** | 0/0 retained | Returning starter, 2nd season, official roster, no competition | uhcougars.com; SI Houston | 2026-08-03 | stays **OK** |
| **Mississippi State** | 13 | Kamario Taylor | *unchanged* | **M → H** | 0/0 retained | "Unquestioned starter — no competition, no committee, no asterisk" | hailstate.com; WLBT; Mississippi Today | 2026-08-03 | stays **OK** |
| **Duke** | 59 | Walker Eget | **Walker Eget (expected Week 1 starter; 5-way competition)** | M (unchanged) | unchanged | Conflict resolved; entry confirmed | goduke.com; Duke Chronicle | 2026-08-03 | none |
| **Iowa** | 24 | Jeremy Hecklinski | **Open (Hecklinski / Hank Brown)** | L (unchanged) | unchanged | Reps split, no decision | hawkcentral; Western Iowa Today | 2026-08-03 | none |
| **Kansas** | 48 | Cole Ballard | **Cole Ballard (leader; Isaiah Marshall competing)** | L (unchanged) | unchanged | "May be" QB1; real competition | SI Kansas; kuathletics.com | 2026-08-03 | none |

**Numerical-cell repairs: 2** (Arkansas, UConn — both M→L, zeros cleared per the approved Akron methodology). **No nonzero value created anywhere.**

## 4. Source & conflict log

| # | Item | Claim A | Claim B | Resolution | Residual |
|---|---|---|---|---|---|
| E-17 | Arkansas QB1 | Candidate: KJ Jackson likely starter (M), July | HC Silverfield **2026-08-03**: battle may last to Sept 5 | Newer + higher authority (HC, beat outlet, same-day) → **L** | Who wins |
| E-18 | UConn QB1 | Candidate: Tucker McDonald (M), July | No source names him; HC/commit/starter all departed | Uncorroborated name + verified upheaval → **L** | Actual QB1 |
| E-19 | Duke QB1 (7D.3 conflict) | Candidate: Walker Eget | 7D.3: no source named the successor | **Resolved** — official roster + Duke Chronicle + Diaz confirm Eget | Competition outcome |
| E-20 | Houston H vs M | Candidate M | Returning starter, official roster, no competition | → **H** (returning-starter branch, not projection) | None material |
| E-21 | Miss. State H vs M | Candidate M | "Unquestioned starter… no asterisk" | → **H** | None material |
| E-22 | Kansas upgrade? | National list: Ballard projected starter | SI "**may be** QB1"; Marshall competing; no Leipold naming | **L retained** — 7D.3 call vindicated | Who wins |

## 5–6. Final counts (reproduced from the candidate)

| Metric | Result |
|---|---|
| Teams | **138 unique**, 0 missing / 0 duplicated / 0 shifted |
| **Final H/M/L** | **63 H / 43 M / 32 L** (= 138) |
| **Final status** | **102 OK / 36 UNCERTAIN**, 0 nonzero deltas |
| Blank vs zero | **36 blank / 102 zero** = 138 |
| L-coded with non-blank numerical cells | **0** |
| Cross-tab M/UNCERTAIN | 4 (UNC, Texas Tech, Ohio, Rutgers — all blank-gated) |
| **Backlog remaining** | **31 — Group of Five only** |

**Exact final G5 backlog (31):** Pac-12 6 (CSU, FRES, ORST, TXST, USU, WSU) ·
American 6 (ECU, NAVY, RICE, TEM, TLSA, UNT) · Mountain West 6 (NDSU, NEV, NIU,
SJSU, UTEP, WYO) · Sun Belt 6 (APP, ARST, CCU, GASO, JMU, ODU) · CUSA 4 (FIU,
KENN, MOST, NMSU) · MAC 3 (BUFF, **M-OH** *(carries the open 7D.2 conflict)*, SAC).

**P4 + Independent remaining: NONE — Batch 2 is COMPLETE.**

## 7. Regression-test report — all pass

| # | Test | Result |
|---|---|---|
| 1 | No confidence edit creates an unintended numerical adjustment | ✔ 0 nonzero deltas; the only numeric edits were zero→blank clears |
| 2 | No team rating changes | ✔ TEAM RATINGS not in diff |
| 3 | No projected spread changes | ✔ ENGINE not in diff |
| 4 | No formula changes | ✔ **0** |
| 5 | Formula columns A, B, G, M unchanged | ✔ intact on all 138 rows |
| 6 | PENDING LINE priority | ✔ outranks QB gate; 0 spreads loaded |
| 7 | FCS — NO PLAY priority | ✔ unchanged |
| 8 | TRANSITION UNCERTAIN priority | ✔ unchanged |
| 9 | BET-toggle behavior | ✔ SETTINGS not in diff |
| 10 | Blank vs zero preserve meanings | ✔ 36 / 102 = 138 |
| 11 | **Every L-coded team gated** | ✔ **0 L-coded teams have non-blank numerical cells** |
| 12 | H/M behave per existing logic | ✔ 63 H → OK; 39 M → OK; 4 M → UNCERTAIN (blank-gated) |
| 13 | 138 unique, no shift/duplication | ✔ |
| 14 | Input columns constants only | ✔ |

## 8–9. Diff v0.7.5 → v0.7.6

**40 changed cells · ZERO formula changes · zero unrelated / unauthorized / unknown.**

| Cells | Classification | Count |
|---|---|---|
| `E7, H7, K7, L7` | **VERIFIED ARKANSAS QB UPDATE** | 4 |
| `D7, F7` | **NUMERICAL-CELL CONSISTENCY REPAIR** (Arkansas M→L) | 2 |
| `E143, H143, K143, L143` | **VERIFIED UCONN QB UPDATE** | 4 |
| `D143, F143` | **NUMERICAL-CELL CONSISTENCY REPAIR** (UConn M→L) | 2 |
| `E59, K59, L59` | **VERIFIED DUKE QB UPDATE** | 3 |
| `H46, K46, L46` | **VERIFIED HOUSTON QB UPDATE** | 3 |
| `E24, K24, L24` | **VERIFIED IOWA QB UPDATE** | 3 |
| `E48, K48, L48` | **VERIFIED KANSAS QB UPDATE** | 3 |
| `H13, K13, L13` | **VERIFIED MISSISSIPPI STATE QB UPDATE** | 3 |
| `CHANGELOG!A75:D77` | **VERSION OR CHANGELOG** | 12 |
| `START HERE!A1` | **VERSION OR CHANGELOG** | 1 |

Formula count **123,011 → 123,011 (delta 0)**; 21 sheets, order and visibility identical.

## 10. Manifest / SHA-256

| File | SHA-256 |
|---|---|
| **v0.7.6 CANDIDATE** (new) | `080986dd5dc29dc23b22e104eb7aa523c757196562eb49846a4c3cae30d7a5bb` |
| v0.7.5 CANDIDATE | `8c273c2e9a1af917ab1badd937cd9fefe3f30c7ff4c9bc4cb0563fac34b37f5b` — **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` — **UNCHANGED**, = `PROJECT_MANIFEST.json` ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.**

## 11. Next step

**OPTION A — PROCEED TO FINAL G5 BATCH** (31 teams). Promotion remains **DEFERRED**.

Defect rate across the P4 stragglers was **2 of 7 (29%)** — the highest of any
batch so far, and both defects were *overstated* confidence (M on genuinely open
or unverifiable rooms). Team-specific beat sourcing clearly outperforms
conference roundups: **7 of 7 resolved here vs 9 of 16 in 7D.3.** I'd run the
final G5 batch the same way, in conference blocks of 5–6.
