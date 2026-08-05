# Phase 6.1 — Expected vs Actual Results

All results below are **actual calculated output** from a real
formula-evaluation engine (Python `formulas` library) running each
harness's byte-exact formula text — not a manual trace. Full raw output:
`harness_results_raw_v061.json`. This report covers only the **new**
Phase 6.1 tests; the 17 original Phase 6 line-level/status-chain tests are
unchanged and still hold (see the Phase 6 `expected_vs_actual_results.md`)
except where explicitly corrected below.

## 1. ADJUSTMENTS!K formula correction (item 1)

| Test | Fixture | Expected | Actual | Result |
|---|---|---|---|---|
| Non-numeric value ("abc") | `harness_test_E2.xlsx`, row 6 = "abc", Active=Y | K shows clean `"VALUE NOT NUMERIC; "` text, not `#VALUE!` | K = `"VALUE NOT NUMERIC; "` | ✅ defect fixed |
| Oversized numeric value (999) | `harness_test_D2.xlsx`, row 6 = 999, Active=Y | K shows `"LARGE ADJ (>4); "` | K = `"LARGE ADJ (>4); "` | ✅ |
| All 250 rows (6-255), byte-exact formula text | `v0.6.1_working.xlsx` | Matches user-specified pattern exactly | 0 mismatches across all 250 rows (`validate_v061.py`) | ✅ |

## 2. ADJUSTMENTS!J safety correction (item 2)

| Test | Fixture | Expected | Actual | Result |
|---|---|---|---|---|
| Non-numeric value, Active=Y | `harness_test_E2.xlsx` | J (Effective) = 0; margin unaffected | J = 0; `ENGINE!O10` (manual adj into G4's margin) = 0.0 | ✅ never flows into ENGINE |
| Oversized value (999), Active=Y | `harness_test_D2.xlsx` | J = 0; margin unaffected | J = 0; `ENGINE!O10` = 0.0 | ✅ |
| MARGIN OVERRIDE, value=15, Active=Y | `harness_test_F_override.xlsx` | Exempt from the >4 warning: K blank, J=1, override value adopted | K = blank; J = 1; `ENGINE!R10` (final margin) = 15.0 | ✅ override exemption confirmed |
| All 250 rows (6-255), byte-exact formula text | `v0.6.1_working.xlsx` | Matches the safety-corrected pattern exactly | 0 mismatches across all 250 rows (`validate_v061.py`) | ✅ |

## 3. DATA INCOMPLETE status test (item 3)

| Step | Fixture | Expected | Actual | Result |
|---|---|---|---|---|
| Control (G1, unmodified) | `harness_test_G_control.xlsx` | READY (both teams QB-resolved, valid line) | READY | ✅ |
| Test: `IMPORT SCHEDULE!C8` (week) cleared to blank | `harness_test_G_datainc.xlsx` | DATA INCOMPLETE | **READY** (unchanged) | ❌ genuine defect surfaced |
| Independent re-run of the same test | `harness_test_G_datainc2.xlsx` | DATA INCOMPLETE | **READY** (unchanged), confirms not a fluke | ❌ (same defect, reproduced) |
| Restore: `C8` set back to `0` (exact original) | `harness_test_G_restored.xlsx` | Returns to READY, matches control | READY, identical to control | ✅ restore verified exact |

**Root cause and full write-up:** `data_incomplete_finding.md`. Summary:
`CLEAN!C6`/`D6` fall through to a bare `'IMPORT SCHEDULE'!C6` reference
when `$A6` is non-blank; a bare reference to a blank cell evaluates to `0`
in Excel/Sheets (not `""`), so `ENGINE!AI`'s `OR($B6="",$C6="")` check can
never be satisfied. **DATA INCOMPLETE is unreachable dead code** for a
missing week or date field. Documented, not repaired this round — no
change was authorized to `CLEAN!C`/`D` or `ENGINE!AI`.

**Status-priority chain — full revalidation (7 of 8 statuses positively
demonstrated; the 8th, DATA INCOMPLETE, could not be, for the reason
above, and that inability is itself the finding):**

| Status | Demonstrated | Source |
|---|---|---|
| BLOCKED | ✅ | Phase 6 (unchanged formulas) |
| FCS — NO PLAY | ✅ | Phase 6 (unchanged formulas) |
| PENDING LINE | ✅ | Phase 6 (unchanged formulas) |
| STALE LINE | ✅ | Phase 6 (unchanged formulas) |
| QB UNCERTAIN | ✅ | Phase 6 (unchanged formulas) |
| TRANSITION UNCERTAIN | ✅ | Phase 6 (unchanged formulas) + reconfirmed functionally in item 5 below |
| DATA INCOMPLETE | ❌ **cannot occur** | genuine defect, documented above |
| READY | ✅ | Phase 6 + this round's genuine BET-toggle test (item 4) |

## 4. Genuine BET-toggle test (item 4)

Phase 6's BET-toggle test used G5 (JVST@NDSU), which never actually
reached READY (NDSU's transitional restriction kept it at TRANSITION
UNCERTAIN in both toggle variants) — so the toggle's effect on the label
was never genuinely observed. This round uses G1 (NCST@UVA) with a
deliberately small entered spread (1.0) to maximize the model-vs-market
edge, on the **exact same fixture** for both toggle states.

| Fixture | Toggle | Status | Edge | Label | Result |
|---|---|---|---|---|---|
| `harness_test_BET_N.xlsx` | N | READY | 4.328571428571427 | INVESTIGATE | ✅ |
| `harness_test_BET_Y.xlsx` | Y | READY | 4.328571428571427 (identical) | **BET** | ✅ toggle flips the label on an otherwise-identical fixture |

Both variants independently confirm READY (not masked by any
higher-priority status) and edge ≥ 3.0 (the BET threshold). The toggle
fixture was restored to N and all fixture data removed afterward (see
section 6 / cleanup proof). **The Phase 6 CHANGELOG/report claim that
this test had already passed is corrected in this build's own
CHANGELOG.**

## 5. Weekly-workflow validation strengthening (item 5)

**Prior-fade table, all 10 populated rows** (`fade_table_test.xlsx`,
synthetic F=0..10 fed into the real `TEAM RATINGS!G` formula):

| F | Expected (`SETTINGS!C37:C46`) | Actual | Result |
|---|---|---|---|
| 0 | 1.0 | 1.0 | ✅ |
| 1 | 0.8 | 0.8 | ✅ |
| 2 | 0.65 | 0.65 | ✅ |
| 3 | 0.5 | 0.5 | ✅ |
| 4 | 0.4 | 0.4 | ✅ |
| 5 | 0.3 | 0.3 | ✅ |
| 6 | 0.225 | 0.225 | ✅ |
| 7 | 0.175 | 0.175 | ✅ |
| 8 | 0.125 | 0.125 | ✅ |
| 9 | 0.1 | 0.1 | ✅ |
| 10 (out of table domain) | clamps to F=9 floor (0.1) | 0.1 | ✅ clamp confirmed |

**NDSU functional transitional-restriction test**
(`harness_test_NDSU_functional.xlsx`): 5 synthetic completed FBS games
added (opponents Air Force, UNLV, New Mexico, San José State, UTEP — all
NDSU wins), exceeding the model's 4-game reclassification threshold; G5
(JVST@NDSU) given a fresh market line, both teams' QBs resolved, BET
toggle=Y, and a deliberately small spread (0.5) to produce a large edge.

| Check | Expected | Actual | Result |
|---|---|---|---|
| `TEAM RATINGS!F122` (NDSU effective games played) | 5.0 (exceeds the 4-game threshold) | 5.0 | ✅ |
| `TEAM RATINGS!X122` (review-cleared) | blank — nothing auto-sets it | blank/unset | ✅ |
| `ENGINE!AF11` (transitional flag, G5) | still TRANSITIONAL | TRANSITIONAL | ✅ |
| `ENGINE!AI11` (status, G5) | still TRANSITION UNCERTAIN, despite games/edge/toggle | TRANSITION UNCERTAIN | ✅ |
| Edge | large (test designed to produce one) | 11.45614078674948 | — |
| Label | INVESTIGATE (never BET — status never reaches READY) | INVESTIGATE | ✅ restriction holds functionally, not just by label |

This proves the restriction is enforced structurally (only a manual
`TEAM RATINGS!X` review-clear entry can lift it) rather than merely
observing that a text label happened not to change.

## 6. Fixture removal proof (item 7)

`cleanup_script_v061.py` run against `v0.6.1_test_applied.xlsx` (44
`TEST_TAG` cells applied) produces `v0.6.1_test_cleaned.xlsx`, proven
**cell-by-cell identical (0 differences, all sheets)** to the pristine
`v0.6.1_working.xlsx` — see `cell_diff_proof_v061.tsv` and
`validation_report_v061.txt`. This includes exact restoration of the 5
real schedule games (rows 20-24) that the NDSU fixture had overwritten in
the real test-applied copy — caught and corrected while building the
cleanup script (see `operational_test_plan_v061.md`).

## 7. AUDIT invariants — 0 failing

See `validation_report_v061.txt` section K for the full live-calc +
direct-inspection proof of all 11 `AUDIT!B6:B19` invariants and the
`formulas`-engine `COUNTIF(range,"?*")`-on-blank-range library bug found
and cross-verified while checking `B16`.

## 8. Corrections to Phase 6's own CHANGELOG/report

Phase 6's CHANGELOG row 45 and `expected_vs_actual_results.md` both
stated the DATA INCOMPLETE and genuine BET-toggle tests had passed. They
had not — Phase 6 never actually built a DATA INCOMPLETE test, and its
BET-toggle test never reached READY on either variant. This build's
CHANGELOG (`v0.6.1_working.xlsx`, rows 45 and 51-56) corrects the row-45
overclaim and adds 6 new entries reflecting what was actually done this
round, including the newly found DATA INCOMPLETE defect.
