# TTW NCAAF Power Ratings 2026 — Phase 6.2 Operational Test Plan

## Baseline

Authoritative source: the native Google Sheet
`TTW_NCAAF_Power_Ratings_2026_v0.6.1_AUTHORITATIVE`
(id `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`), exported to
`v0.6.1_authoritative_export.xlsx`. All Phase 6.2 work is built from this
export. The earlier standalone `Working_v0.6.1.xlsx` was **not** used.
v0.5.2, v0.6, and v0.6.1 are unmodified. Phase 7 was not started.

## Objective

Repair the documented DATA INCOMPLETE pathway defect — and nothing else.
Only `CLEAN!C6:C1005`, `CLEAN!D6:D1005`, the version banner, and one
CHANGELOG row were changed (see `before_after_formula_report.md` and
`v0.6.2_vs_v0.6.1_cell_diff.tsv`).

## Method (LibreOffice unavailable — same validated workflow as prior phases)

- **openpyxl** for controlled edits and structural inspection.
- The **`formulas`** engine for live formula calculation, driven from a
  compact real-formula harness (`h62_base.xlsx`) whose every formula is
  copied byte-for-byte from the authoritative v0.6.2 workbook at its
  original row/column, plus all 138 real team rows so INDEX/MATCH lookups
  behave exactly as in production.
- Cell-level and number-format diffs for change-set and cleanup proofs.
- No workbook rebuild; no recalculation of the full 1,000-row file (still
  not feasible in this sandbox).

## Repair verification

Before applying, the exact fix semantics were confirmed with two isolated
probes (`probe_weekfix.xlsx`, `probe_weekfix2.xlsx`) that faithfully
reproduce the real Excel/Sheets "bare reference to blank → 0" coercion:

| Input | OLD formula | NEW formula |
|---|---|---|
| blank Week + blank Date | week=0, date=0 → status READY (**defect**) | week="", date="" → **DATA INCOMPLETE** |
| Week 0 + valid date | week=0 → READY | week=0 preserved → READY (**not** misread as blank) |
| Week 5 + valid date | week=5 → READY | week=5 preserved → READY |

The build script (`build_v062.py`) asserted every one of the 2000 old
formulas byte-for-byte before overwriting.

## Regression suite (all live-calculated on v0.6.2's own formulas)

Every scenario is a compact harness variant built by
`build_scenarios_v062.py`; results are the real calculated output recorded
in `h62_raw_results.json` by `run_scenarios_v062.py`. Full expected-vs-
actual table in `expected_vs_actual_v062.md`.

1. **DATA INCOMPLETE repair** — G1 driven to READY, then Week blanked →
   DATA INCOMPLETE; Date blanked → DATA INCOMPLETE; Week restored to its
   real value (0) → back to READY.
2. **Stacked priority (the point of the repair)** — DATA INCOMPLETE must
   never override a higher-priority status. A blank Week was stacked onto a
   BLOCKED game, a PENDING-LINE game, a QB-UNCERTAIN game, and a
   TRANSITION-UNCERTAIN game; each retained its higher status.
3. **Full single-condition status chain** — BLOCKED, FCS — NO PLAY,
   PENDING LINE, STALE LINE, QB UNCERTAIN, TRANSITION UNCERTAIN, READY,
   plus the repaired DATA INCOMPLETE.
4. **ADJUSTMENTS** — valid (Effective=1, no flag, applies), oversized
   (Effective=0, `LARGE ADJ (>4)`, blocked from margin), non-numeric
   (Effective=0, `VALUE NOT NUMERIC`, no raw `#VALUE!`), missing reason
   (`REASON MISSING`), and MARGIN OVERRIDE (exempt from the 4-point warning,
   applies). No ADJUSTMENTS formula was changed (byte-identical to v0.6.1).
5. **BET toggle** — same READY fixture with a qualifying |edge| ≥ 3.0:
   toggle N → INVESTIGATE, toggle Y → BET; only the toggle differs.
6. **Transitional restriction** — NDSU with 5 completed FBS games (>4-game
   threshold), a large edge, a market line, and BET toggle = Y: still
   TRANSITION UNCERTAIN, still INVESTIGATE, never BET. Only a manual
   `TEAM RATINGS!X` review-clear entry could lift it, and nothing
   auto-populates that cell.
7. **Prior-fade table** — every populated `SETTINGS!C37:C46` value
   (F = 0…9) plus the F ≥ 9 floor/clamp, via the real `TEAM RATINGS!G`
   formula fed synthetic F = 0…10. The table itself was not altered.
8. **FCS protection** — a market line entered on an FCS game (G6): status
   stays FCS — NO PLAY, no spread/total/edge/label/confidence, and no
   lower-priority status overrides it.

## Fixture discipline

The compact harness uses only the 7 real game rows and 138 team rows; its
synthetic NDSU games sit on rows unused by the harness. The **full-scale**
test-applied copy (`v0.6.2_test_applied.xlsx`, built by
`apply_fixtures_v062.py`) follows the required discipline strictly:

- Synthetic NDSU games go on **genuinely unused schedule rows 894–898**
  (the 888 real games occupy rows 6–893; 894+ were verified blank before
  use).
- The **only** real (pristine-non-blank) cell altered is
  `IMPORT SCHEDULE!C8` (G1's Week 0), temporarily blanked for the DATA
  INCOMPLETE demo. Its exact original value is recorded in
  `original_real_cells_v062.json` and restored precisely on cleanup.
- Every other fixture writes into a cell that is blank in the pristine
  workbook.
- Every synthetic value carries the `TEST ONLY — NOT REAL DATA` tag.

## Cleanup proof

`cleanup_fixtures_v062.py` reverses every fixture (clearing only manual
cells, restoring the one real cell and the date-input number formats),
producing `v0.6.2_test_cleaned.xlsx`. `prove_zero_diff_v062.py` compares it
cell-by-cell against the pristine authoritative v0.6.2:
**0 cell differences, 0 number-format differences, 0 remaining TEST_TAG
cells, 0 residual market lines / adjustments / stats**
(`cleanup_zero_diff_proof_v062.tsv`).

## Final validation

`validate_v062.py` (full output `validation_report_v062.txt`): 21 sheets,
hidden/visible states preserved, `fullCalcOnLoad` = True, the change set vs
v0.6.1 is exactly the 2005 intended cells, ADJUSTMENTS J/K byte-identical,
0 market lines / 0 adjustments / 0 imports, 138 QB rows UNCERTAIN, BET
toggle N, 888 games / 761 FBS-vs-FBS / 127 FCS-involved / 0 BLOCK,
NDSU/Sac State transitional intact, 0 stored formula-error cells. AUDIT
invariants live-calculated in `h62_audit_harness.xlsx`: all OK (B16 is a
known `formulas`-engine COUNTIF-on-blank library artifact, cross-verified
as 0 market lines by direct inspection; B10/B19 proven by direct
argument), 0 genuine failing invariants.

## Newly discovered defects

None. The `formulas`-engine `COUNTIF(range,"?*")`-on-blank and
`SUMPRODUCT(--(...))`-on-blank behaviours are previously-documented
verification-tool limitations, not workbook defects.
