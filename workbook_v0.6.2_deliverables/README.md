# Phase 6.2 Deliverables — DATA INCOMPLETE Pathway Repair

## Authoritative workbook

- **Filename:** `TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx`
- **Version:** v0.6.2
- **Creation date:** 2026-07-21
- **SHA-256:** `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd`
- **Built from:** the authoritative v0.6.1 Google Sheet
  (`TTW_NCAAF_Power_Ratings_2026_v0.6.1_AUTHORITATIVE`, id
  `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`), exported to
  `v0.6.1_authoritative_export.xlsx`.

## What changed

The documented DATA INCOMPLETE pathway defect is repaired. `CLEAN!C6:C1005`
(Week) and `CLEAN!D6:D1005` (Date) now wrap their source reference in an
explicit blank guard, so a genuinely blank Week or Date propagates as blank
instead of numeric 0 / epoch — restoring reachability of the DATA
INCOMPLETE status. Exactly **2005 cell-level changes** vs v0.6.1: 2000
CLEAN formula cells, 1 banner cell, 4 CHANGELOG cells. Nothing else — no
other formula, no formatting, no sheet state, no ADJUSTMENTS/QB/HFA/
threshold/schedule logic — was touched.

## Package contents

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx` | The repaired authoritative workbook (deliverable 1). |
| `operational_test_plan.md` | Phase 6.2 test plan: baseline, method, repair verification, regression suite, fixture discipline, cleanup, final validation. |
| `before_after_formula_report.md` | Exact before/after formula text for CLEAN!C/D, dependency audit, and the non-formula (banner/CHANGELOG) changes. |
| `expected_vs_actual_v062.md` | Every regression test's expected vs actual result, generated from the raw harness output. |
| `validation_report.txt` | Full `validate_v062.py` output: structure, counts, clean state, audit, change-set. |
| `v0.6.2_vs_v0.6.1_cell_diff.tsv` | Machine-readable cell/formula diff vs the authoritative v0.6.1 baseline (2005 rows). |
| `fcs_classification_888.json` | Row-indexed FBS/FCS classification (761/127/0-BLOCK), computed via the real CLEAN!O/Q formulas; inputs proven byte-identical to this build. |
| `build_v062.py` | The build script: assert-before-overwrite repair of CLEAN!C/D, banner, CHANGELOG. |
| `validate_v062.py` / `diff_v062_vs_v061.py` | Final-validation and diff scripts. |
| `harness/` | Compact real-formula test harness (see below). |
| `fixtures/` | Full-scale fixture application + cleanup (see below). |
| `proof_of_removal/` | Zero-difference cleanup proof (see below). |
| `promotion/` | Phase 7 native Google Sheets promotion: promotion manifest, round-trip verification report/JSON, and the round-trip verification script. |

### `harness/`

| File | Purpose |
|---|---|
| `build_harness_v062.py` | Builds `h62_base.xlsx` from v0.6.2's byte-exact formulas (138 team rows + 7 real game rows). |
| `h62_base.xlsx` | The base harness. |
| `build_scenarios_v062.py` | Builds every regression scenario variant (`h62_*.xlsx`). |
| `run_scenarios_v062.py` | Live-calculates every scenario; writes `h62_raw_results.json`. |
| `h62_raw_results.json` | Raw calculated output for all scenarios (deliverable: raw harness results). |
| `build_fade_v062.py` / `h62_fade_table.xlsx` | Isolated prior-fade table test (F=0…10). |
| `build_audit_harness_v062.py` / `h62_audit_harness.xlsx` | AUDIT-invariant live-calc harness. |
| `probe_weekfix.xlsx`, `probe_weekfix2.xlsx` | Isolated probes reproducing the blank→0 coercion and confirming the fix. |
| `h62_datainc_*.xlsx`, `h62_stack_*.xlsx`, `h62_status_chain.xlsx`, `h62_adj_*.xlsx`, `h62_bet_*.xlsx`, `h62_ndsu_functional.xlsx`, `h62_fcs_protection.xlsx` | The scenario variant workbooks. |

### `fixtures/`

| File | Purpose |
|---|---|
| `apply_fixtures_v062.py` | Applies the full-scale fixture set to a copy of v0.6.2 (deliverable: fixture application script). |
| `v0.6.2_test_applied.xlsx` | The fixtures-applied copy (clearly marked TEST ONLY). |
| `cleanup_fixtures_v062.py` | Reverses every fixture (deliverable: cleanup script). |
| `original_real_cells_v062.json` | Exact recorded originals of the one real cell altered (IMPORT SCHEDULE!C8 = Week 0). |

### `proof_of_removal/`

| File | Purpose |
|---|---|
| `prove_zero_diff_v062.py` | Cell-by-cell comparison of the cleaned copy vs pristine v0.6.2. |
| `cleanup_zero_diff_proof_v062.tsv` | The proof output: **0 differences** (deliverable: zero-difference cleanup proof). |
| `v0.6.2_test_cleaned.xlsx` | The cleaned copy (proven cell-identical to pristine v0.6.2). |

## Reproduce from a clean folder

```
python3 build_v062.py                       # -> v0.6.2 workbook (from v0.6.1_authoritative_export.xlsx)
python3 diff_v062_vs_v061.py                # -> v0.6.2_vs_v0.6.1_cell_diff.tsv (2005 cells)
python3 validate_v062.py                    # -> validation_report.txt (all pass)
cd harness && python3 build_harness_v062.py && python3 build_scenarios_v062.py \
   && python3 build_fade_v062.py && python3 run_scenarios_v062.py   # -> h62_raw_results.json
cd ../fixtures && python3 apply_fixtures_v062.py && python3 cleanup_fixtures_v062.py
cd ../proof_of_removal && python3 prove_zero_diff_v062.py           # -> 0 differences
```
(`v0.6.1_authoritative_export.xlsx` is the exported baseline; not
redistributed here since v0.6.1 is unmodified and already delivered.)

## Scope confirmation

v0.5.2, v0.6, and v0.6.1 are unmodified. No preseason ratings, HFA, QB
values, thresholds, weights, schedule, rankings, or market logic were
altered. No additional defect was silently fixed (none was found).

## Promotion status (Phase 7)

v0.6.2 was **approved** and promoted to a new native Google Sheet
(`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`), round-trip verified
(PASS), and is now the **current authoritative production workbook**. The
v0.6.1 sheet (`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`) is preserved
unmodified as the rollback version. See `promotion/` in this directory and
the repository-root `PROJECT_MANIFEST.json` / `README.md`. Phase 7
(repository closeout and authoritative-version promotion) is complete; no
new model-development phase has been started.
