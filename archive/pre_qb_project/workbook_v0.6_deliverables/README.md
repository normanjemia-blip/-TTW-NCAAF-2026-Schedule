# Phase 6 Deliverables Index

1. **`TTW NCAAF Power Ratings 2026 - Working v0.6.xlsx`** — the clean
   delivered workbook. Cell-identical to approved v0.5.2 except the
   version banner and 7 new CHANGELOG rows documenting this phase.
2. **`operational_test_plan.md`** — what was tested, why two test
   artifacts were used, fixture design, cleanup methodology.
3. **`expected_vs_actual_results.md`** — every test's expected vs actual
   result, the full status-priority-chain proof table, and the one
   genuine formula defect found (documented, not repaired).
4. **`ipad_weekly_checklist.md`** — simplified weekly-operating
   checklist with exact cells/columns, grounded in the workbook's own
   `START HERE!A6:C15` routine.
5. **`test_fixtures.json`** — the 7 real schedule rows used for testing
   and what each one tests.
6. **`fcs_classification_888.json`** — the real, calculated FBS/FCS
   classification for all 888 schedule games (via the actual `CLEAN!O/Q`
   formulas), proving the 761/127 split.
7. **`v0.6_vs_v0.5.2_full_diff.tsv`** + **`validate_v06.py`** +
   **`validation_report.txt`** — the complete cell/formula diff versus
   approved v0.5.2 and the full validation battery (26/26 checks pass).
8. **`harness/`** — the compact real-formula test harness: every formula
   extracted byte-for-byte from v0.6 at its original row/column, run
   through a real formula-calculation engine. `build_harness.py` builds
   the base; `apply_fixtures.py` creates test variants A–E;
   `build_weekly_harness.py` and `build_threshold_test.py` build the
   weekly-workflow and threshold-boundary tests; `run_matrix.py` runs
   everything and produces `harness_results_raw.json`.
9. **`fixtures/`** — the reproducible test-fixture system applied to a
   real, full-scale workbook copy: `apply_to_real_workbook.py` (writes
   the fixtures), the resulting test-applied file (clearly marked
   TEST ONLY, not for real use), and `cleanup_script.py` (reverses every
   fixture).
10. **`proof_of_removal/`** — `cleanup_script.py` run against the
    test-applied copy, then diffed cell-by-cell against approved v0.5.2:
    **0 differences** across all 21 sheets (`cell_diff_proof.txt`). The
    cleaned file itself is included for inspection.
