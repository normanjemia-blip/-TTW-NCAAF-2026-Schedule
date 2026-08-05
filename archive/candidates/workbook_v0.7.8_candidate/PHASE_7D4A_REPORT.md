# Phase 7D.4A — Final Five QB Resolution

**Date:** 2026-08-04 (America/New_York; the container clock is UTC and reads 2026-08-04 18:55, NY reads 14:55 — same calendar day, so no correction was needed this phase)
**Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.8_CANDIDATE.xlsx`
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.7:** unmodified · **Google Sheet:** never accessed · **NOT promoted.**

## Recommendation: **OPTION B — DEFER AND REPAIR**

The five teams are resolved and **the QB verification backlog is now 0**, which is what
Option A required. I am still recommending Option B, because completing the backlog
surfaced a defect in the ledger itself that a promotion audit would have to answer for.

**The backlog counter and the workbook disagree.** The ledger says 21 Tier-1 (M/L) teams
are verified. The workbook says otherwise: all 21 still carry their original **2026-07-21
build date and original build note**, with no verification stamp of any kind. Section 6
lays this out. It is a documentation defect, not a data defect — no rating, status, or
value is wrong because of it — but "the backlog is zero" is currently a claim the
workbook cannot substantiate for 21 of its 74 Tier-1 records. That is precisely the kind
of unverified-data import that Option A is supposed to prevent.

---

## 1. Starting state — reproduced from v0.7.7

Machine-readable: `final_five_starting_state.json` / `.csv`.

| AB | Team | Conf | Row | Code | D/F | Last verified | Entry |
|---|---|---|---:|:--:|:--:|---|---|
| TXST | Texas State | Pac-12 | 78 | M | 0 / 0 | 2026-07-21 | Brad Jackson |
| WSU | Washington State | Pac-12 | 80 | M | 0 / 0 | 2026-07-21 | Caden Pinnick |
| UNT | North Texas | American | 87 | M | 0 / 0 | 2026-07-21 | Tayven Jackson |
| GASO | Georgia Southern | Sun Belt | 131 | L | blank | 2026-07-21 | Open (Weston Bryan / Turner Helton) |
| ODU | Old Dominion | Sun Belt | 137 | M | 0 / 0 | 2026-07-21 | Quinn Henicle |

All five were sourced **team-specifically** — official athletics site, head-coach
statements, and the local beat — not conference roundups. That was the right call again:
the two defects below were both invisible to conference-level coverage.

## 2. Texas State — **CONFIRMED M**

Brad Jackson is the returning starter and there is no competition. He started 2025 as a
redshirt freshman (**3,050 pass yds, 18 TD, 7 INT, 71.5%**; **16–17 rushing TD**, a school
single-season record for a quarterback; **3,968 total yards, 7th nationally**), was a
third-team all-conference pick, and **announced his return on 2025-12-06** alongside WRs
Beau Sparks and Chris Dawn Jr. Coverage of the Pac-12 move states Texas State "returns a
starting quarterback for the first time under Kinne." The Athletic ranked him **the top
Group of Five quarterback**. He spoke to media at 2026 fall camp as the quarterback, and
the Ourlads projected depth chart lists him QB1 ahead of Gavin Parkhurst.

**H considered and declined.** No official 2026 naming or depth chart has been published,
and the project's own precedent is explicit: Western Michigan's Broc Lowry (returning
MAC-champion starter) and Toledo's John Alan Richter were both **confirmed at M**, not
upgraded. Ourlads is a projection aggregator, not an official chart. Consistency wins over
a documentary upgrade that has **zero mechanical effect** anyway — ENGINE reads only
QB VALUES columns A, G and M, and the status formula special-cases only `L`.

## 3. Washington State — **DEFECT: M → L**, zeros cleared

The entry asserted Caden Pinnick as the projected transfer QB1. The beat contradicts it:

- **HeraldNet, 2026-07-30:** WSU "set to open fall camp with **wide-open QB competition**."
- **The Columbian, 2026-08-01:** "Washington State football heads into fall with quarterback situation **unresolved**."
- **HC Kirby Moore declined to name a preference:** *"That's gonna continue through the summer… The team will decide who the quarterback is in terms of what happens on the field."*
- **Spokesman-Review:** Pinnick **"wasn't able to create meaningful separation from Eshelman"** in spring; his spring game ended in a pick-6. Staff may keep the decision in-house until kickoff.

Three-way with Owen Eshelman and Julian Dugger, no leader → **L**. Zeros cleared to blank
per the approved Akron/App State methodology; status becomes UNCERTAIN. Camp opened
2026-08-06.

*Cross-check that corroborates the room:* 2025 Coug **Jaxon Potter transferred out to Old
Dominion** (announced 2026-01-13) — he shows up as a competitor in the ODU record below.

## 4. North Texas — **CONFIRMED M**; entry was **not** stale

I expected this one to be stale — new staff, and Reese Poffenbarger had left for Akron —
but the record holds. **Tayven Jackson is on the roster and leads the race.**

- **Coaching change verified:** Eric Morris left for Oklahoma State; **Neal Brown** is head coach and rebuilt the roster with 75–90+ new players in roughly 12 days.
- **HC Neal Brown, American Kickoff broadcast, 2026-07-29:** senior UCF transfer Tayven Jackson **"now has a slight lead"** in a **three-man race** with sophomore East Carolina transfer **Chaston Ditta** and sophomore returner **Chris Jimerson Jr.** Brown did **not** name a starter; the battle carries into fall camp.
- Jackson's 2025 at UCF: 2,151 pass yds, 10 TD, 8 INT, 85 rush yds, 1 rush TD.

Clear leader stated by the head coach, no naming → **M retained**, entry refined to name
the competitors. Zeros retained (correct for M).

## 5. Georgia Southern — **STALE ENTRY: L → M**, values stay blank

The entry read `Open (Weston Bryan / Turner Helton)` and **omitted Max Johnson entirely**.

Johnson signed out of the portal on **2026-01-11** from North Carolina (previously LSU
2020–21, Texas A&M 2022–23). At **Sun Belt Media Days, 2026-07-15**, HC **Clay Helton
said: "Max Johnson is expected to be the starter if the season began today,"** citing
experience and high-level production. Turner Helton — second year in the program, Western
Kentucky transfer, the head coach's son, 14/26 for 74 yds and 1 TD in three 2025
appearances — is the other player with a shot at the **2026-09-05** opener; both took
first-team reps in the spring game.

A direct head-coach statement of who leads is **not** name recognition, so this clears the
bar that Appalachian State failed. No official naming → **M, not H** — the same treatment
Oregon State got. Per the L→M rule **values remain blank**, so status correctly stays
UNCERTAIN.

**Open risk recorded in the note:** Johnson's durability — season-ending injuries at Texas
A&M in 2022 and 2023, and a broken leg in UNC's 2024 opener.

## 6. Old Dominion — **CONFIRMED M**

The job opened when 2025 starter **Colton Joseph transferred to Wisconsin**. Quinn Henicle
(RS-So) started the 2025 Cure Bowl in his place and was **game MVP** in a 24–10 win over
South Florida (11/25, 127 yds; 24 carries, 107 yds, 2 rushing TD, incl. a 51-yard TD run).
He is **2–0 as a starter**.

Beat coverage says Henicle **"has a leg up"** and is **"the front runner to land the QB1
role,"** while also reporting he **"remains enmeshed in a three-way battle"** with RS-Jr
**Jaxon Potter** (Washington State transfer) and RS-Fr **Ryan Huff**, both taking
significant snaps. Henicle himself, 2026-04-03: *"I'm competing like I'm trying to earn
this job."* HC Ricky Rahne (7th season, off 10–3) has **not** named a starter — ODU's
official Sun Belt Media Day release does not address the position at all.

Leader backed by **on-field production rather than name recognition**, no naming → **M
retained**, entry refined. Zeros retained.

## 7. QB correction log

| Team | Row | Prior entry | Corrected entry | Code | D/F | Reason |
|---|---:|---|---|:--:|:--:|---|
| **Washington State** | 80 | Caden Pinnick | **Open (Pinnick / Eshelman / Dugger)** | **M → L** | **0/0 → blank** | "Wide-open"; HC declined to commit; no separation from Eshelman |
| **Georgia Southern** | 131 | Open (Weston Bryan / Turner Helton) | **Max Johnson (leader; Turner Helton competing)** | **L → M** | blank (unchanged) | Stale — omitted Max Johnson; HC says he'd start today |
| Texas State | 78 | Brad Jackson | Brad Jackson (returning starter) | M (unchanged) | 0/0 retained | Confirmed; entry refined |
| North Texas | 87 | Tayven Jackson | Tayven Jackson (slight lead; Ditta / Jimerson competing) | M (unchanged) | 0/0 retained | Confirmed by HC; entry refined |
| Old Dominion | 137 | Quinn Henicle | Quinn Henicle (leader; Potter / Huff competing) | M (unchanged) | 0/0 retained | Confirmed; entry refined |

**Numerical-cell consistency repairs: 1** (Washington State M→L, zeros cleared).
**No nonzero QB value created anywhere.** Baseline-QB column C left untouched on all five,
per the established convention (C = preseason baseline identity, E = active QB).

## 8. Source & conflict log

| # | Claim | Source 1 | Source 2 | Resolution | Residual |
|---|---|---|---|---|---|
| F-1 | Pinnick is WSU's projected QB1 | Candidate (July build); CougCenter "early frontrunner" | HeraldNet "wide-open"; Columbian "unresolved"; Moore non-commitment; Spokesman "wasn't able to create meaningful separation" | **Candidate wrong → L.** "Early frontrunner" is a media characterization contradicted by the beat writer's direct observation and by the head coach | Camp outcome; staff may not announce until kickoff |
| F-2 | GASO QB room = Bryan / Turner Helton | Candidate (July build) | Helton at Sun Belt Media Days 2026-07-15; portal signing 2026-01-11 | **Candidate stale → Max Johnson named leader; L→M** | Johnson's durability; no official naming |
| F-3 | Max Johnson's eligibility year | SI (2026-01-11): "sixth season of NCAA football in 2026" | WSAV/Helton: "seventh year of eligibility" | **Reconcilable** — six seasons played (2020–25), 2026 is the seventh year in college. Immaterial to QB1 | None |
| F-4 | UNT entry is stale (new staff, Poffenbarger gone) | My own Phase 7D.4 expectation | Neal Brown, 2026-07-29: Jackson "now has a slight lead" | **My expectation was wrong — entry confirmed current** | Three-man race unresolved |
| F-5 | Texas State merits H | Established-returning-starter evidence | No official naming; WMU/Toledo precedent confirmed at M | **H declined for consistency**; no mechanical effect either way | Official depth chart |
| F-6 | ODU has a settled QB1 | "Front runner", "has a leg up", "expected to be QB1" | "Remains enmeshed in a three-way battle"; Rahne silent | **Leader without naming → M**, not H | Camp outcome |
| **F-7** | **Backlog reached zero** | **Ledger: 5 → 0** | **Workbook: 21 Tier-1 rows still stamped 2026-07-21 with original build notes** | **Both true under different definitions — see §9. Ledger backlog IS 0; audit trail is not** | **Owner decision required** |

**Sourcing note:** eight fetches returned **HTTP 403** (CougCenter, The Columbian,
Underdog Dynasty, dentonrc, WSAV, collegefootballnews, universitystar, aol). Where a
403 blocked direct retrieval I did **not** rest a conclusion on the search snippet — every
determination above traces to a source I fetched successfully (Spokesman-Review, HeraldNet,
WTOC, ntdaily, Yahoo/ODU beat, SI) or to a head-coach quote corroborated across two or more
independent outlets.

## 9. Finding F-7 — the backlog counter and the workbook disagree

**The ledger backlog is 0.** Carried forward exactly as Phases 7D.1–7D.4 defined it, with
the five moved to `VERIFIED 7D.4A`, nothing remains marked `NOT VERIFIED`. Reproduced in
`qb_inventory_v078.json` → `backlog_remaining`.

**But 82 rows still carry the original 2026-07-21 build stamp**, and they are not who the
previous report said they were:

| Group | Count | Status |
|---|---:|---|
| H-coded (tier 2, never in Tier-1 scope) | **61** | Expected |
| **Tier 1 (M/L) credited as verified but never stamped** | **21** | **Defect** |
| Backlog | **0** | Resolved this phase |

**Correction to `PHASE_7D4_REPORT.md` §9.** It reported "87 — the 5 backlog teams **plus 82
H-coded tier-2 teams** that were never in Tier 1 scope (expected, not a defect)." That was
wrong. Only **61** of those 82 are H-coded; **21 are Tier-1 M/L records** whose verification
exists only in the phase ledger, never in the workbook. I wrote that sentence, and it
papered over this gap rather than surfacing it.

The 21: `ALA AUB FLA UK MIZ TENN VAN NEB UNC STAN SYR FAU MEM USF TULN BALL CMU TOL WMU UNLV USM`

They split into two kinds:

- **4 teams — pure documentation gap, cheap to close.** Ball State, Central Michigan, Toledo and Western Michigan were **live-verified in Phase 7D.1** and reported as CONFIRMED. 7D.1 deliberately refrained from refreshing dates for unverified teams and, in doing so, never stamped the verified ones either. The research exists in the 7D.1 report; only the workbook cells are missing.
- **17 teams — the credit itself is thin.** Credited as `verified 7A-7D`. But **Phase 7A was a ratings audit and 7B/7C were adjustment-candidate and HFA audits — none of them was a team-specific QB sourcing pass.** Vanderbilt is the clearest case: it was re-verified in Phase 8.3 and that verification **FAILED**, yet it sits in the ledger as verified. These 17 have never been through the discipline that found every defect in this project.

**Why this matters for promotion.** Every classification defect found in this project —
Akron, Arkansas, UConn, Buffalo, Northern Illinois, Appalachian State, and now Washington
State — was an **unsupported M or a named starter the evidence did not support**. Not one
was a team rated too uncertain. Of the 17 thinly-credited teams, **6 are M-coded**
(AUB, UK, MIZ, UNC, FAU, UNLV) — exactly the population that has produced every defect so
far. Counting Georgia Southern's stale entry, this project has found **8 defects across
the 59 teams that received a team-specific pass — roughly one in seven**.

**I did not act on this.** Re-verifying 21 teams is outside the five-team scope this phase
authorized, and refreshing their dates without doing the research would be the exact
failure mode the rule against date-refreshing exists to prevent. Flagging it and stopping.

## 10. Dataset integrity

| Check | Result |
|---|---|
| 138 unique teams / abbrevs, no missing, duplicate or shifted rows | ✔ |
| Invalid H/M/L codes | **0** ✔ |
| Every L-coded team has blank numerical inputs | ✔ **0 violations** |
| Every L-coded team resolves to UNCERTAIN | ✔ |
| Nonzero QB values / nonzero deltas | **0 / 0** ✔ |
| Formula columns A, B, G, M intact on all 138 rows | ✔ |
| Input columns C–F, H–L hold constants only | ✔ |
| **Final H/M/L** | **64 H / 43 M / 31 L** = 138 |
| **Final OK/UNCERTAIN** | **100 OK / 38 UNCERTAIN** |
| **Blank / zero numerical** | **38 blank / 100 zero** = 138 |
| **Ledger backlog** | **0** ✔ |
| **Tier-1 rows lacking an in-workbook verification stamp** | **21** ✗ (finding F-7) |

Code counts are **unchanged in aggregate by arithmetic, not by design** — WSU M→L and
GASO L→M offset exactly, the same coincidence as the 7D.1 Texas Tech / Akron pair.
Status moved **101 OK / 37 UNCERTAIN → 100 OK / 38 UNCERTAIN**; the single mover is
**Washington State**, correctly re-gated by its `L` code. Georgia Southern's L→M does
**not** move its status, because its values stay blank.

## 11. Regression battery — 34 of 35 pass; the one failure is finding F-7, reported deliberately

Full log: `verification_log_v078.txt`.

No formula changes (**0**) ✔ · formula count **123,011 → 123,011** ✔ · 21 sheets, order and
visibility identical ✔ · 138 unique teams, no row-alignment change ✔ · no invalid codes ✔ ·
0 nonzero QB values and 0 nonzero deltas ✔ · every L-coded team blank-gated and UNCERTAIN ✔ ·
**TEAM RATINGS, ENGINE, SETTINGS, ADJUSTMENTS, MARKET LINES, PRESEASON, IMPORT SCHEDULE all
untouched** ✔ · no confidence edit created a numerical adjustment ✔ · no team-rating or
projected-spread movement ✔ · `SETTINGS!B3`=2026, `B6`=2.5 HFA, `B11`="N" BET toggle
unchanged ✔ · `ENGINE!AI` status precedence, `ENGINE!M` (QB adj) and `ENGINE!AE` (QB status)
formulas byte-identical ✔ · WSU M→L applied with zeros cleared and status now UNCERTAIN ✔ ·
GASO L→M applied with values still blank and status still UNCERTAIN ✔ · TXST / UNT / ODU
retain M with zeros and status OK ✔ · all five stamped 2026-08-04 ✔ · **[FAIL] 25b — 21
Tier-1 rows credited as verified carry no in-workbook stamp** (finding F-7, out of scope).

**Status masking still holds:** with **0 market spreads loaded**, PENDING LINE outranks
QB UNCERTAIN, so every game still reads PENDING LINE and none of this is visible downstream.
Washington State's OK → UNCERTAIN move changes no game status, no rating, and no spread.

## 12. Diff v0.7.7 → v0.7.8

**32 changed cells · ZERO formula changes · zero unrelated / unauthorized / unknown.**
Cell-level detail: `diff_v077_to_v078.csv`.

| Classification | Count |
|---|---:|
| VERIFIED PAC-12 QB UPDATE | 7 |
| VERIFIED SUN BELT QB UPDATE | 7 |
| VERIFIED AMERICAN QB UPDATE | 3 |
| **NUMERICAL-CELL CONSISTENCY REPAIR** (WSU D80/F80) | **2** |
| VERSION OR CHANGELOG | 13 |
| **UNRELATED / UNAUTHORIZED / UNKNOWN** | **0** |

By sheet: QB VALUES 19 · CHANGELOG 12 · START HERE 1. Eighteen sheets untouched.

## 13. Manifest / SHA-256

| File | SHA-256 |
|---|---|
| **v0.7.8 CANDIDATE** (new) | `8f655e5e369a6a8c12fdb34f3309cff13a92c9310af6186b77081be4b3c389cb` |
| v0.7.7 CANDIDATE | `3da33d0c10a375c6bd3e43c06f1119b1a6a72cfb49d16abff65ed9c670d02a73` — **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` — **UNCHANGED**, = `PROJECT_MANIFEST.json` ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.** Rollback
sheet `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo` — **never accessed.** No rating, HFA,
formula, structure, threshold, schedule, source-weight or status-logic change.

## 14. Path to Option A

One decision, then a short piece of work:

1. **Close the 4-team documentation gap** — stamp Ball State, Central Michigan, Toledo and Western Michigan with their existing Phase 7D.1 findings. Research already done; this is transcription.
2. **Decide on the 17 thinly-credited teams.** Either (a) run a real team-specific pass over them — at the project's own one-in-seven rate I'd budget **2–3 corrections**, concentrated in the 6 M-coded ones; or (b) accept the 7A–7C credit as sufficient and record that decision explicitly, so the workbook's provenance claim matches what was actually done.

Option A becomes defensible once the workbook can substantiate every Tier-1 record it
claims is verified. It cannot today.
