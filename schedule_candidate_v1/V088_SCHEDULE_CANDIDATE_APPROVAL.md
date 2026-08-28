# v0.8.8 SCHEDULE-DATE CANDIDATE — APPROVAL PACKET

> **UNPROMOTED CANDIDATE. NOT v0.8.8. NOT PRODUCTION.**
> Production remains **v0.8.7**. No current-state pointer was repointed, no production file was
> modified, and no write was made to the live Google Sheet.

**Rebased:** 2026-08-25 · **Scope:** schedule dates only · **Awaiting explicit approval.**

---

## 1. Identity

| | |
|---|---|
| **Candidate** | `schedule_candidate_v1/TTW_College_Football_Power_Ratings_v0.8.8_SCHEDULE_CANDIDATE.xlsx` |
| **Candidate SHA-256** | `5416ffcb4c07b8e741f24f51b9603ac44c064db943e144618d6ffa372ef62a84` |
| **Predecessor** | `promotion_v0.8.7/TTW_College_Football_Power_Ratings_v0.8.7_AUTHORITATIVE.xlsx` |
| **Predecessor commit** | `96e9a77` |
| **Predecessor SHA-256** | `46671deeaaa94d98c63cb32d0e94af9907e76e7e2638de431b918987df2e15cd` — **verified byte-identical, unmodified** |
| **Certificate** | `verify_schedule_candidate.py` — **53 passed, 0 failed** |
| **Companion CSV** | `TTW_2026_Verified_Schedule_ESPN_v1.1_LOCALDATES.csv` — 133 of 888 rows, `start_date` only |

### Scope of change

| | |
|---|---|
| **Cells changed** | **133** |
| **Sheet** | `IMPORT SCHEDULE` — **only** |
| **Range** | column **D** (`start_date`), rows 6–893 — **only** |
| **Direction** | every change exactly **−1 calendar day** |
| **Formulas changed** | **0** |
| **Any other sheet or cell** | **0** |

---

## 2. Preflight — all clear before any work began

| Check | Result |
|---|:--:|
| HEAD is `96e9a77` | ✅ `96e9a77141ddadb8f8498ee06c1afcedc9992a32` |
| Branch synchronised with origin | ✅ 0 ahead / 0 behind |
| Worktree clean | ✅ |
| v0.8.7 workbook SHA-256 matches | ✅ `46671dee…15cd` |
| `verify_v087` still passes | ✅ **89 / 0** |
| Audit artifacts located and committed | ✅ `phase12_date_audit/` (report, generator, 133-row diff), `schedule_candidate_v1/` (rule, generator, certificate, snapshot) |

The correction was **not reconstructed from memory.** The committed deterministic generator was
re-run against the committed 888-row ESPN evidence snapshot.

---

## 3. The rebase

```
python3 schedule_candidate_v1/build_schedule_candidate.py \
  --source promotion_v0.8.7/TTW_College_Football_Power_Ratings_v0.8.7_AUTHORITATIVE.xlsx
```

Result: **133 CSV rows changed, 133 `IMPORT SCHEDULE!D` cells changed** — identical to the v0.8.6-based
build, as expected, because v0.8.7 touched only `QB VALUES` and the banner. The two changesets are
disjoint.

**Determinism evidence:** the regenerated `TTW_2026_Verified_Schedule_ESPN_v1.1_LOCALDATES.csv` and
`espn_kickoff_snapshot.csv` came out **byte-identical** to the committed versions — `git diff` reports
no change to either. The generator is reproducible.

### Targeted edits only — no blanket replacement

Prior blanket search-and-replace corrupted historical rollback hashes, so every edit here was surgical:

| File | Edit |
|---|---|
| `build_schedule_candidate.py` | `DEFAULT_SRC_XLSX` → v0.8.7 · `OUT_XLSX` → the v0.8.8 candidate name · docstring base version + rebase history |
| `verify_schedule_candidate.py` | `BASE` → v0.8.7 · `CAND` → new name · `FROZEN_V086` → `FROZEN_V087` + SHA · QB expectations hoisted to named constants · **new** proofs added (§5) |

**No historical hash, report, or rollback entry was touched.** `phase12_date_audit/` is unmodified.

---

## 4. Date rule — preserved exactly as audited

```
timeValid = True    start_date = kickoff_utc.astimezone(venue_zone).date()
timeValid = False   start_date = kickoff_utc.astimezone(US/Eastern).date()   -- placeholder, preserved
```

- **Fails closed.** `venue_zone()` raises `UnresolvedVenueZone` for any unmapped venue. **There is no
  UTC fallback path.**
- **The 403 placeholder-time events are preserved untouched.** ESPN's midnight-Eastern placeholder is
  never converted as though it were a real kickoff.
- **Deterministic and idempotent** — proven twice over in §5, checks 8.3 and 8.4.

---

## 5. Certificate — all 20 required proofs, isolated

**Result: 53 passed, 0 failed.**

| # | Required proof | Check |
|:--:|---|---|
| 1 | Source byte-identical to authoritative v0.8.7 | 0.1 |
| 2 | Exactly 133 cells changed | 1.4 |
| 3 | Every changed cell in `IMPORT SCHEDULE!D` | 1.2, 1.3 |
| 4 | Every change `delta_days = −1` | 3.3 |
| 5 | No formula changed | 1.1 |
| 6 | All non-target sheets and cells unchanged | 1.2, 1.5, 2.x (8 columns) |
| 7 | **403 placeholder-time rows unchanged** | **6.7, 6.8** |
| 8 | **888 event IDs present and unique** | **6.9**, 9.1 |
| 9 | Zero games change week | 4.2, 4.3 |
| 10 | **Zero games cross the Week 0 boundary** | **6.13**, 4.4 |
| 11 | **Stored Sunday games fall 70 → 3** | **6.10** |
| 12 | **Memphis at UNLV becomes Saturday 2026-08-29** | **6.12**, 4.5 |
| 13 | **The three genuine Sunday games remain Sunday** | **6.11** |
| 14 | QB census remains 117 / 21 | 6.1 |
| 15 | Confidence census remains 76 / 43 / 19 | 6.2 |
| 16 | **QB zero count remains 234** | **6.4** |
| 17 | All five reference spreads unchanged | 5.x |
| 18 | No rating, edge, side, label, market line or QB gate change | 5.x, 6.3, **6.5**, **6.6**, 7.1–7.4 |
| 19 | **Second application produces zero additional changes** | 8.3, **8.4** |
| 20 | **Guard detects all 133 old UTC dates against v0.8.7** | 8.2, **8.2b** |

### ⚠️ The count is 53, not 41 — stated plainly

You expected 41/0. **The original 41 checks did not isolate 9 of the 20 proofs you require** (bolded
above). I added them rather than report 41 by omitting required evidence.

**No assertion was weakened, removed, or bypassed.** All 41 original checks remain and still pass;
the delta is +12 new checks (9 proofs, some contributing more than one check). Two original checks
had their *expected values* updated because the base genuinely changed — QB census and confidence
census now belong to v0.8.7 — which is exactly the update you authorised.

### Notable results

| Check | Value |
|---|---|
| 6.8 | all **403** placeholder rows unchanged — `[]` |
| 6.9 | `n=888 unique=888` |
| 6.10 | `before=70 after=3` |
| 6.11 | Louisville @ Ole Miss · Washington State @ Washington · Wisconsin @ Notre Dame — all still 2026-09-06 |
| 6.12 | `2026-08-30 → 2026-08-29`, weekday Saturday |
| 6.4 | `234` |
| 8.2b | guard flagged **133** against the v0.8.7 workbook itself |
| 8.4 | second application → `[]` |

---

## 6. Corrected weekday distribution

| Weekday | v0.8.7 stored | **Candidate** | Δ |
|---|:--:|:--:|:--:|
| Saturday | 720 | **751** | +31 |
| Friday | 45 | **66** | +21 |
| Thursday | 22 | **34** | +12 |
| Wednesday | 24 | **15** | −9 |
| Tuesday | 6 | **18** | +12 |
| **Sunday** | **70** | **3** | **−67** |
| Monday | 1 | **1** | 0 |
| **Total** | **888** | **888** | — |

The corrected shape is what a college-football season actually looks like. The three surviving Sunday
games are genuine Labor Day weekend fixtures (Labor Day 2026 is Monday Sept 7), and the single Monday
game — SMU @ Florida State, Sept 7 — is a real Labor Day game that was already correct.

---

## 7. Validation — complete chain

| Suite | Result |
|---|---|
| `schedule_candidate_v1/verify_schedule_candidate.py` *(rebased)* | **53 passed, 0 failed** |
| `promotion_v0.8.7/verify_v087.py` | **89 passed, 0 failed** |
| `promotion_v0.8.6/verify_v086.py` | 56 passed, 0 failed |
| `promotion_v0.8.5/verify_v085.py` | 53 passed, 0 failed |
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `git diff --check` | clean |

Every historical verifier still passes against its own frozen predecessor. **No test expectation was
relaxed to accommodate this candidate.**

---

## 8. Scope lock — confirmations

| Constraint | Status |
|---|:--:|
| No QB change of any kind | ✅ QB censuses identical, `QB VALUES` byte-identical |
| No quarterback researched or reconsidered | ✅ |
| Memphis, UNLV, Oregon State, Texas Tech unaltered | ✅ within the byte-identical `QB VALUES` sheet |
| No formula changed | ✅ check 1.1 |
| Game IDs, teams, venues, weeks, lines, ratings unchanged | ✅ checks 2.x, 4.2, 6.6, 6.9, 5.x |
| Kickoff times unchanged | ✅ the workbook stores no kickoff time; ESPN instants are input only |
| 403 placeholder-time games untouched | ✅ checks 6.7, 6.8 |
| Only `IMPORT SCHEDULE!D` modified | ✅ checks 1.2, 1.3 |
| Historical reports unaltered | ✅ `phase12_date_audit/` shows no git diff |
| Production / current-state pointers unaltered | ✅ `promotion_v0.8.7/`, `PROJECT_MANIFEST.json`, `README.md`, policy doc, Week 0 dry run — **no git diff** |
| Candidate not promoted as v0.8.8 | ✅ |
| **No live Google Sheet write** | ✅ **none attempted; the connector cannot write cells** |

### Superseded artifact still present

`TTW_College_Football_Power_Ratings_SCHED1_CANDIDATE.xlsx` — the earlier **v0.8.6-based** build —
remains in this directory and is **superseded**. No certificate now covers it. It was left in place
because deleting a tracked artifact was not authorised. **Do not promote it.** The current candidate
is the `v0.8.8_SCHEDULE_CANDIDATE` file named in §1.

---

## 9. If approved — the promotion that is NOT authorised yet

1. Copy the candidate to `promotion_v0.8.8/` and promote it as a **schedule** version with its own
   certificate.
2. Repoint current-state references (`PROJECT_MANIFEST.json`, `README.md`, policy doc, Week 0 dry run
   `EXPECTED_SHA`) — **targeted edits only, never a blanket replace.**
3. Wire `assert_not_utc_dates()` into the refresh job.
4. Apply the 133 date changes to the live Google Sheet **manually** — the connector cannot write cells.

**Known follow-up:** the **403** placeholder-time rows must be re-derived once ESPN publishes real
kickoff times; some will move a day then. This correction is not one-and-done for the season.

**STOPPED. Awaiting explicit approval before any v0.8.8 promotion.**
