# TTW COLLEGE FOOTBALL POWER RATINGS — v0.8.4 PROMOTION

**Promotion date:** 2026-08-21 (America/New_York)
**Commit:** `14cf041` — pushed `05b8a52..14cf041`, 0 ahead / 0 behind, tree clean
**Branch:** `claude/2026-ncaaf-schedule-build-by6j5n`
**Scope:** Northern Illinois + Tulane record packet, NIU confidence M -> L,
Colorado State unchanged, Texas Tech medical gate preserved

---

## 0. HOW TO VERIFY THIS DOCUMENT

```bash
git rev-parse --short HEAD                 # expect 14cf041
git status --porcelain                     # expect no output

sha256sum promotion_v0.8.4/TTW_College_Football_Power_Ratings_v0.8.4_AUTHORITATIVE.xlsx
#   expect: ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff
sha256sum promotion_v0.8.3/TTW_College_Football_Power_Ratings_v0.8.3_AUTHORITATIVE.xlsx
#   expect: ff55782586ef1adb662eba59710e824dc382769a24579e48917b101fbcdd96b8  (frozen)

python3 promotion_v0.8.4/verify_v084.py    # expect: 49 passed, 0 failed
python3 promotion_v0.8.3/verify_v083.py    # expect: 42 passed, 0 failed
python3 promotion_v0.8.2/verify_v082.py    # expect: 33 passed, 0 failed
python3 promotion_v0.8.1/verify_v081.py    # expect: RESULT: 0 FAILURES
python3 phase11_week0_dryrun/week0_dryrun.py   # expect: 30 passed, 0 failed
python3 validate_schedule.py               # expect: ALL HARD-FAIL CHECKS PASSED
python3 phase8_4_qb_monitoring/scripts/test_pipeline.py   # expect: 15/15
git diff --check                           # expect no output

# proof the three predecessors were not touched
git diff --stat HEAD~1 -- promotion_v0.8.1/ promotion_v0.8.2/ promotion_v0.8.3/
#   expect: no output
```

The 45-cell diff is enumerated in `promotion_v0.8.4/diff_v083_to_v084.csv`, with each
row classified as RESYNC or CORRECTION.

---

## 1. RESULT

| | |
|---|---|
| Cells changed | **45** (44 QB VALUES + 1 START HERE) |
| Formula changes | **0** |
| Nonzero QB values | **0** |
| Rating / market-line / model-spread changes | **0** |
| QB status census | **104 OK / 34 UNCERTAIN** |
| Confidence census | **69 H / 40 M / 29 L** |
| Certificate | `verify_v084.py` — **49 passed, 0 failed** |

v0.8.3 remains frozen and byte-identical, as do v0.8.2 and v0.8.1.

---

## 2. TWO COMPONENTS, KEPT SEPARATE

### A. RESYNC — 5 QB rows, 35 cells

The repository artifact had drifted **five QB records behind** the live production
master. v0.8.3 stood at 100 OK / 38 UNCERTAIN while the live sheet was at
104 OK / 34 UNCERTAIN. Applying only the NIU/Tulane packet would have produced an
artifact matching neither state and validating against nothing.

Every value in this component is **transcribed verbatim from the live production
master**, read on 2026-08-21. Nothing here is authored.

| Team | Row | Result after resync |
|---|---|---|
| North Carolina | 65 | Billy Edwards Jr. · 0/0 · M · OK |
| Stanford | 68 | Davis Warren · 0/0 · H · OK |
| Missouri State | 101 | Skyler Locklear · 0/0 · H · OK |
| San Jose State | 124 | Luke Weaver · 0/0 · H · OK |
| Texas Tech | 52 | Will Hammond · blank/blank · H · UNCERTAIN |

### B. CORRECTIONS — 2 QB rows, 9 cells

| Team | Row | Cell | Before | After |
|---|---|---|---|---|
| Northern Illinois | 123 | E123 | Taron Dickens (Western Carolina transfer) | Open (Davidson / Macon / Hamric / Dickens) |
| Northern Illinois | 123 | H123 | M | **L** |
| Northern Illinois | 123 | I123 | Mountain West conference preview URL | HERO Sports NIU quarterback report |
| Northern Illinois | 123 | K123 | 2026-08-03 | 2026-08-21 |
| Northern Illinois | 123 | L123 | prior note | replacement note (section 3) |
| Tulane | 91 | E91 | Kadin Semonza | Open (Semonza / Chriss-Gremillion / Johnson / Bruno) |
| Tulane | 91 | I91 | Underdog Dynasty / Yahoo projections | FOX 8 New Orleans, 2026-07-24 |
| Tulane | 91 | K91 | 2026-08-04 | 2026-08-21 |
| Tulane | 91 | L91 | prior note | replacement note |

**Tulane confidence is UNCHANGED at L.** Plus `START HERE!A1` for the version
identifier and confidence census.

Protected on every touched row and asserted by the certificate: `G` and `M` remain
formulas, `J` remains `2026`.

---

## 3. NORTHERN ILLINOIS REVERSES A PRIOR DOCUMENTED DECISION

Recorded explicitly because it overturns an earlier review rather than refining it.

The v0.8.3 record carried this note:

> DEFECT CORRECTED 2026-08-03: prior entry listed 'Open (Davidson / Macon / Hamric)'
> — none appear in current NIU coverage. Verified: TARON DICKENS … is NIU's
> quarterback … High-profile transfer widely expected to start -> L upgraded to M.

**Current reporting contradicts that premise directly.** Coaches have not named a
starter among returners Brady Davidson and Jalen Macon and transfers Ean Hamric and
Taron Dickens — **all four appear in current coverage**, which is precisely what the
2026-08-03 review asserted was not the case. "Widely expected to start" is a
projection, not a naming, and does not support M.

Two further defects corrected on the same row:

1. **Citation mismatch.** The prior source was a **Mountain West** conference preview
   cited for a **MAC** team.
2. **Missing context.** Head coach Thomas Hammock departed for the NFL; Rob Harley is
   interim head coach.

Status is UNCERTAIN before and after — the numerical values were blank and remain
blank — so this changes accuracy and the confidence census, not the gate.

---

## 4. TEXAS TECH — MEDICAL GATE PRESERVED

Certificate checks 4.7 through 4.9 assert all three properties:

- identity confidence **H** — Hammond's QB1 status is settled and was not researched
  as an open competition
- **`D52` and `F52` remain blank** — the blank numerical record is what holds the gate
- status remains **UNCERTAIN**

Week 1 availability stays conditional on final Texas Tech **team** medical clearance
for full football activity. Surgeon clearance and scrimmage participation do not
satisfy it. Texas Tech does not play in Week 0.

---

## 5. COLORADO STATE — DELIBERATELY UNCHANGED

Certificate check 4.10 compares **all thirteen cells** of the Colorado State row
against v0.8.3 and asserts they are identical. The build script captures the row
before any write and re-compares it afterwards, aborting if anything moved.

---

## 6. CENSUSES, AND A CORRECTION TO THE SUPPLIED FIGURE

| | v0.8.3 (repo) | Live master | v0.8.4 |
|---|---|---|---|
| QB status | 100 OK / 38 UNCERTAIN | 104 OK / 34 UNCERTAIN | **104 OK / 34 UNCERTAIN** |
| Confidence | 65 H / 41 M / 32 L | 69 H / 41 M / 28 L | **69 H / 40 M / 29 L** |
| Nonzero QB values | 0 | 0 | **0** |

**The confidence census supplied with this task was `68 H / 42 M / 28 L`. Counted row
by row over the live QB VALUES block, the live sheet is `69 H / 41 M / 28 L`.**

The one-record difference is **Texas Tech**. Its own live note is dated 2026-08-21 and
raises it from M to H — "IDENTITY CONFIRMED, MEDICALLY GATED … Identity confidence H".
The quoted census predates that correction.

The **status** census 104 / 34 was correct as supplied, because Texas Tech's status
did not change: it was UNCERTAIN at M and remains UNCERTAIN at H, since D and F are
blank.

Arithmetic:

```
live:              69 H / 41 M / 28 L
NIU M -> L:        -1 M, +1 L
v0.8.4:            69 H / 40 M / 29 L      (69 + 40 + 29 = 138)
```

The first build used the supplied figure in the banner, **failed its own census
check**, and was rebuilt with the measured value.

---

## 7. MODEL OUTPUTS AND WEEK 0

**Nothing moved.** QB deltas are 0 or blank throughout, so `ENGINE!M` contributes 0 to
every game. The certificate re-derives five spreads from the workbook's own inputs and
asserts each is unchanged:

| Game | Model spread |
|---|---|
| Memphis at UNLV | UNLV -5.6 |
| North Carolina at TCU | TCU -4.2 |
| New Mexico State at Florida State | FSU -27.7 |
| San Jose State at USC | USC -35.2 |
| Hawaii at Stanford | STAN -3.7 |

Week 0 QB gating in the repository artifact now shows **1 of 8** games carrying QB
UNCERTAIN — **Memphis at UNLV**, blocked on both sides, with both head coaches on
record that they will not name a starter before kickoff.

Also verified: 888 games / 761 FBS-v-FBS / 127 FCS; MARKET LINES blank in the repo
artifact by design; BET toggle N; B22/B23 blank so totals stay unavailable; NDSU and
Sacramento State transitional; all ten AUDIT structural invariants pass.

### Declared checkpoint drift

The Phase 10 checkpoint (`week0_card.json`, captured 2026-08-15) is **preserved, not
rewritten**, per the standing instruction to flag reproducibility differences rather
than replace them. Two games now differ from it **on status only**:

| Game | Checkpoint | Now | Reason |
|---|---|---|---|
| UNC at TCU | QB UNCERTAIN | DATA INCOMPLETE | UNC activated 2026-08-19; QB gate cleared, status falls through while B4/B5 are blank |
| HAW at STAN | QB UNCERTAIN | DATA INCOMPLETE | Stanford activated 2026-08-21; same |

`week0_dryrun.py` now carries a `DECLARED_STATUS_DRIFT` table. **Model spreads, edges,
sides and labels remain hard gates that may never drift.** A status difference passes
only when it is declared there with its reason, and the harness **also fails if a
declaration stops applying**, so the table cannot rot silently.

---

## 8. VALIDATION

| Suite | Result |
|---|---|
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `git diff --check` | clean |

---

## 9. FILES CHANGED

**New — `promotion_v0.8.4/`:**

- `TTW_College_Football_Power_Ratings_v0.8.4_AUTHORITATIVE.xlsx`
- `build_v084.py` — deterministic build from frozen v0.8.3, asserts every precondition
- `verify_v084.py` — promotion certificate, read-only
- `make_v084_artifacts.py` — generates the diff CSV and regression log explicitly
- `diff_v083_to_v084.csv` — the 45-cell diff, classified RESYNC vs CORRECTION
- `regression_log_v084.txt` — captured verifier output
- `README.md` — promotion report

**Modified:**

- `PROJECT_MANIFEST.json` — current-version pointer and SHA
- `README.md` — current-version pointer and SHA
- `phase9a_production_config/MASTER_AND_WORKING_COPY_POLICY.md` — archive pointer
- `phase11_week0_dryrun/week0_dryrun.py` — repointed to v0.8.4; census expectation
  38 -> 34; Week 0 gate expectation 4 -> 1; `DECLARED_STATUS_DRIFT` added

**Not modified:** `promotion_v0.8.1/`, `promotion_v0.8.2/`, `promotion_v0.8.3/` —
all byte-identical.

---

## 10. ROLLBACK

Point current-state references back at
`promotion_v0.8.3/TTW_College_Football_Power_Ratings_v0.8.3_AUTHORITATIVE.xlsx`
(`ff55782586ef1adb662eba59710e824dc382769a24579e48917b101fbcdd96b8`). The repository
then returns to 100 OK / 38 UNCERTAIN and diverges from the live master again.

No model output is affected either way. This promotion changes QB record text, one
confidence code and the banner, and touches nothing the engine reads numerically.

---

## 11. OPEN ITEMS FOR THE OWNER

1. **The live Google Sheet still needs the same two corrections.** This promotion
   updated the repository artifact only; the connector cannot write cells. Northern
   Illinois `E123`/`H123`/`I123`/`K123`/`L123` and Tulane `E91`/`I91`/`K91`/`L91` must
   be applied by hand for the live master to match v0.8.4.
2. **The live confidence census will read 69 H / 40 M / 29 L** once the NIU downgrade
   is applied there, not 68 H / 41 M / 29 L. See section 6.
3. **Texas Tech clearance remains the open gate.** Recheck trigger: a Texas Tech team
   medical release, a direct McGuire confirmation, official game notes, or a Week 1
   depth chart listing Hammond at QB1 with no injury limitation and no "OR".
