# v0.8.4 AUTHORITATIVE — NIU/TULANE PACKET + LIVE RESYNC

**Promotion date:** 2026-08-21 (America/New_York)
**Predecessor:** v0.8.3 AUTHORITATIVE — **frozen and unmodified**

| | |
|---|---|
| **Workbook** | `promotion_v0.8.4/TTW_College_Football_Power_Ratings_v0.8.4_AUTHORITATIVE.xlsx` |
| **SHA-256** | `ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff` |
| **Predecessor SHA-256** | `ff55782586ef1adb662eba59710e824dc382769a24579e48917b101fbcdd96b8` (frozen) |
| **Certificate** | `verify_v084.py` — **49 passed, 0 failed** |
| **Change** | 45 input/note cells · **zero formula changes** · zero model-output changes |

---

## 1. Two components, kept separate

### A. RESYNC — 5 QB rows, 35 cells

The repository artifact had drifted **five QB records behind** the live production
master. v0.8.3 stood at 100 OK / 38 UNCERTAIN while the live sheet was at
104 OK / 34 UNCERTAIN. Promoting only the NIU/Tulane packet would have produced an
artifact matching neither state and validating against nothing.

Every value in this component is **transcribed verbatim from the live production
master**, read on 2026-08-21. Nothing is authored here.

| Team | Row | Result |
|---|:--:|---|
| North Carolina | 65 | Billy Edwards Jr. · 0/0 · **M** · OK |
| Stanford | 68 | Davis Warren · 0/0 · **H** · OK |
| Missouri State | 101 | Skyler Locklear · 0/0 · **H** · OK |
| San José State | 124 | Luke Weaver · 0/0 · **H** · OK |
| Texas Tech | 52 | Will Hammond · **blank/blank** · **H** · **UNCERTAIN** |

### B. CORRECTIONS — 2 QB rows, 9 cells

| Team | Row | Change |
|---|:--:|---|
| **Northern Illinois** | 123 | confidence **M → L**; candidates restored to the four-way; source and note replaced |
| **Tulane** | 91 | candidates corrected to the four-way; source and note replaced. **Confidence stays L.** |

Plus `START HERE!A1` — version identifier and confidence census.

---

## 2. Northern Illinois reverses a prior documented decision

This is recorded explicitly because it overturns an earlier review rather than
merely refining it.

The v0.8.3 record carried this note:

> *DEFECT CORRECTED 2026-08-03: prior entry listed 'Open (Davidson / Macon / Hamric)'
> — none appear in current NIU coverage. Verified: TARON DICKENS … is NIU's
> quarterback … High-profile transfer widely expected to start → L upgraded to M.*

**Current reporting contradicts that premise directly.** Coaches have not named a
starter among returners Brady Davidson and Jalen Macon and transfers Ean Hamric and
Taron Dickens — **all four appear in current coverage**, which is exactly what the
2026-08-03 review said was not the case. "Widely expected to start" is a projection,
not a naming, and does not support M.

Two further defects corrected on the same row:

- **Citation mismatch.** The prior source was a **Mountain West** conference preview
  cited for a **MAC** team.
- **Missing context.** Head coach Thomas Hammock departed for the NFL; Rob Harley is
  interim head coach.

Status is UNCERTAIN either way — the numerical values were blank before and remain
blank — so this changes accuracy and the confidence census, not the gate.

---

## 3. Texas Tech — medical gate preserved exactly

Certificate checks 4.7–4.9 assert all three properties:

- identity confidence **H** — Hammond's QB1 status is settled and is not questioned
- **`D52` and `F52` remain blank** — the gate is the missing numerical record
- status remains **UNCERTAIN**

Week 1 availability stays conditional on final Texas Tech **team** medical clearance
for full football activity. Surgeon clearance and scrimmage participation do not
satisfy it. Texas Tech does not play in Week 0.

## 4. Colorado State — deliberately unchanged

Certificate check 4.10 compares all thirteen cells of the Colorado State row against
v0.8.3 and asserts they are identical.

---

## 5. Censuses

| | v0.8.3 (repo) | Live master | **v0.8.4** |
|---|:--:|:--:|:--:|
| QB status | 100 OK / 38 UNCERTAIN | 104 OK / 34 UNCERTAIN | **104 OK / 34 UNCERTAIN** |
| Confidence | 65 H / 41 M / 32 L | 69 H / 41 M / 28 L | **69 H / 40 M / 29 L** |
| Nonzero QB values | 0 | 0 | **0** |

**A census correction worth recording.** The confidence census supplied with this
task was `68 H / 42 M / 28 L`. The live sheet, counted row by row over the QB VALUES
block, is **`69 H / 41 M / 28 L`**. The one-record difference is **Texas Tech**,
whose own live note is dated 2026-08-21 and raises it M → H; the quoted census
predates that correction. The status census (104 / 34) was correct as supplied,
because Texas Tech's status did not change.

v0.8.4 = live, then NIU M → L: **69 H / 40 M / 29 L**.

---

## 6. Model outputs and Week 0

**Nothing moved.** QB deltas are 0 or blank throughout, so `ENGINE!M` contributes 0
to every game. The certificate re-derives five spreads and asserts each is unchanged:

`MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` ·
`SJSU at USC -35.2` · `HAW at STAN -3.7`

Week 0 QB gating in the repository artifact now shows **1 of 8** games carrying QB
UNCERTAIN — **Memphis at UNLV**, blocked on both sides. Both head coaches have said
they will not name a starter before kickoff.

### Declared checkpoint drift

The Phase 10 checkpoint (`week0_card.json`, captured 2026-08-15) is **preserved, not
rewritten**. Two games now differ from it on *status only*:

| Game | Checkpoint | Now | Reason |
|---|---|---|---|
| UNC at TCU | QB UNCERTAIN | DATA INCOMPLETE | UNC activated 2026-08-19; QB gate cleared, status falls through while `B4`/`B5` are blank |
| HAW at STAN | QB UNCERTAIN | DATA INCOMPLETE | Stanford activated 2026-08-21; same |

`week0_dryrun.py` now carries a `DECLARED_STATUS_DRIFT` table. Model spreads, edges,
sides and labels remain **hard gates that may never drift**; a status difference
passes only if it is declared there with its reason, and the harness also fails if a
declaration stops applying — so the table cannot rot silently.

---

## 7. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.4_AUTHORITATIVE.xlsx` | the workbook |
| `build_v084.py` | deterministic build from frozen v0.8.3; asserts every precondition |
| `verify_v084.py` | promotion certificate — **read-only** |
| `make_v084_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v083_to_v084.csv` | the 45-cell diff, classified RESYNC vs CORRECTION |
| `regression_log_v084.txt` | captured verifier output |

## 8. Rollback

Point current-state references back at `promotion_v0.8.3/…v0.8.3_AUTHORITATIVE.xlsx`
(`ff557825…96b8`). The repository then returns to 100 OK / 38 UNCERTAIN and diverges
from the live master again. No model output is affected either way — this promotion
changes QB record text, one confidence code and the banner, and touches nothing the
engine reads numerically.
